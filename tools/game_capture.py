"""Capture a specific window with Win32 GDI without third-party packages.

This module is intentionally read-only: it captures evidence but does not inject
mouse or keyboard input. Use an audited UI automation layer for interaction.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import struct
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from ctypes import wintypes


class CaptureError(RuntimeError):
    pass


@dataclass(frozen=True)
class WindowInfo:
    hwnd: int
    title: str
    process_name: str
    rect: tuple[int, int, int, int]


def select_unique_window(
    windows: Iterable[WindowInfo], title: str, process_name: str
) -> WindowInfo:
    matches = [
        window
        for window in windows
        if window.title.casefold() == title.casefold()
        and window.process_name.casefold() == process_name.casefold()
    ]
    if len(matches) != 1:
        raise CaptureError(
            f"Expected exactly one window title={title!r}, process={process_name!r}; "
            f"found {len(matches)}."
        )
    return matches[0]


def encode_bmp(width: int, height: int, bgra_pixels: bytes) -> bytes:
    if width <= 0 or height <= 0:
        raise CaptureError("Image dimensions must be positive.")
    expected = width * height * 4
    if len(bgra_pixels) != expected:
        raise CaptureError(
            f"Invalid pixel buffer: expected {expected} bytes, got {len(bgra_pixels)}."
        )
    pixel_offset = 14 + 40
    file_size = pixel_offset + expected
    file_header = struct.pack("<2sIHHI", b"BM", file_size, 0, 0, pixel_offset)
    dib_header = struct.pack(
        "<IiiHHIIiiII",
        40,
        width,
        -height,
        1,
        32,
        0,
        expected,
        2835,
        2835,
        0,
        0,
    )
    return file_header + dib_header + bgra_pixels


def write_capture_artifacts(
    output_dir: Path, window: WindowInfo, bitmap: bytes, stem: str | None = None
) -> tuple[Path, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_stem = stem or datetime.now().strftime("capture-%Y%m%d-%H%M%S")
    image_path = output_dir / f"{safe_stem}.bmp"
    metadata_path = output_dir / f"{safe_stem}.json"
    metadata = {
        "window": {
            **asdict(window),
            "rect": list(window.rect),
        },
        "image": image_path.name,
        "captured_at": datetime.now().astimezone().isoformat(),
    }
    image_path.write_bytes(bitmap)
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return image_path, metadata_path


def _require_windows() -> None:
    if os.name != "nt":
        raise CaptureError("Win32 capture is only available on Windows.")


def _window_rect(hwnd: int) -> tuple[int, int, int, int]:
    rect = wintypes.RECT()
    try:
        dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)
        dwmapi.DwmGetWindowAttribute.argtypes = [
            wintypes.HWND,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
        ]
        dwmapi.DwmGetWindowAttribute.restype = ctypes.c_long
        result = dwmapi.DwmGetWindowAttribute(
            wintypes.HWND(hwnd), 9, ctypes.byref(rect), ctypes.sizeof(rect)
        )
    except OSError:
        result = -1
    if result != 0:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        if not user32.GetWindowRect(wintypes.HWND(hwnd), ctypes.byref(rect)):
            raise ctypes.WinError(ctypes.get_last_error())
    return rect.left, rect.top, rect.right, rect.bottom


def _process_name(hwnd: int) -> str:
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.QueryFullProcessImageNameW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(wintypes.HWND(hwnd), ctypes.byref(pid))
    process = kernel32.OpenProcess(0x1000, False, pid.value)
    if not process:
        return ""
    try:
        capacity = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(capacity.value)
        if not kernel32.QueryFullProcessImageNameW(
            process, 0, buffer, ctypes.byref(capacity)
        ):
            return ""
        return Path(buffer.value).name
    finally:
        kernel32.CloseHandle(process)


def list_visible_windows() -> list[WindowInfo]:
    _require_windows()
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    results: list[WindowInfo] = []
    callback_errors: list[Exception] = []
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextLengthW.restype = ctypes.c_int
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetWindowTextW.restype = ctypes.c_int

    @callback_type
    def visit(hwnd: int, _lparam: int) -> bool:
        try:
            if not user32.IsWindowVisible(hwnd):
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            if length <= 0:
                return True
            title_buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, title_buffer, length + 1)
            rect = _window_rect(hwnd)
            if rect[2] > rect[0] and rect[3] > rect[1]:
                results.append(
                    WindowInfo(
                        hwnd=int(hwnd),
                        title=title_buffer.value,
                        process_name=_process_name(hwnd),
                        rect=rect,
                    )
                )
        except Exception as exc:
            callback_errors.append(exc)
        return True

    if not user32.EnumWindows(visit, 0):
        raise ctypes.WinError(ctypes.get_last_error())
    if callback_errors:
        raise CaptureError(f"Window enumeration failed: {callback_errors[0]}")
    return results


def find_window_by_exact_title(title: str) -> WindowInfo:
    """Find one exact top-level title without enumerating unrelated windows."""
    _require_windows()
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
    user32.FindWindowW.restype = wintypes.HWND
    hwnd = user32.FindWindowW(None, title)
    if not hwnd:
        raise CaptureError(f"Window title={title!r} was not found.")
    return WindowInfo(
        hwnd=int(hwnd),
        title=title,
        process_name=_process_name(hwnd),
        rect=_window_rect(hwnd),
    )


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]


def capture_desktop_region(rect: tuple[int, int, int, int]) -> bytes:
    _require_windows()
    left, top, right, bottom = rect
    width, height = right - left, bottom - top
    if width <= 0 or height <= 0:
        raise CaptureError(f"Invalid window rectangle: {rect!r}")

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
    screen_dc = user32.GetDC(None)
    memory_dc = gdi32.CreateCompatibleDC(screen_dc)
    bitmap = gdi32.CreateCompatibleBitmap(screen_dc, width, height)
    if not screen_dc or not memory_dc or not bitmap:
        raise CaptureError("Could not allocate GDI capture resources.")
    previous = gdi32.SelectObject(memory_dc, bitmap)
    try:
        if not gdi32.BitBlt(
            memory_dc, 0, 0, width, height, screen_dc, left, top, 0x40CC0020
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        info = BITMAPINFO()
        info.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        info.bmiHeader.biWidth = width
        info.bmiHeader.biHeight = -height
        info.bmiHeader.biPlanes = 1
        info.bmiHeader.biBitCount = 32
        info.bmiHeader.biCompression = 0
        pixels = ctypes.create_string_buffer(width * height * 4)
        rows = gdi32.GetDIBits(
            memory_dc, bitmap, 0, height, pixels, ctypes.byref(info), 0
        )
        if rows != height:
            raise CaptureError(f"GDI returned {rows}/{height} image rows.")
        raw = pixels.raw
        if not any(raw[index] for index in range(0, len(raw), 4096)):
            raise CaptureError("Captured frame appears empty or protected.")
        return encode_bmp(width, height, raw)
    finally:
        if previous:
            gdi32.SelectObject(memory_dc, previous)
        gdi32.DeleteObject(bitmap)
        gdi32.DeleteDC(memory_dc)
        user32.ReleaseDC(None, screen_dc)


def capture_window(title: str, process_name: str, output_dir: Path) -> tuple[Path, Path]:
    window = select_unique_window([find_window_by_exact_title(title)], title, process_name)
    bitmap = capture_desktop_region(window.rect)
    return write_capture_artifacts(output_dir, window, bitmap)


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a window using Win32 GDI")
    parser.add_argument("--title", default="EXILIUM")
    parser.add_argument("--process", default="GF2_Exilium.exe")
    parser.add_argument("--output", type=Path, default=Path("scratch/game-capture"))
    parser.add_argument("--list", action="store_true", help="List visible windows only")
    args = parser.parse_args()
    try:
        if args.list:
            print(json.dumps(asdict(find_window_by_exact_title(args.title)), ensure_ascii=False))
            return 0
        image_path, metadata_path = capture_window(args.title, args.process, args.output)
        print(image_path.resolve())
        print(metadata_path.resolve())
        return 0
    except (CaptureError, OSError) as exc:
        print(f"Capture failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
