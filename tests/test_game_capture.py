import json
import struct

import pytest

from tools.game_capture import (
    CaptureError,
    WindowInfo,
    encode_bmp,
    select_unique_window,
    write_capture_artifacts,
)


def test_select_unique_window_requires_exact_title_and_process():
    windows = [
        WindowInfo(hwnd=1, title="EXILIUM", process_name="GF2_Exilium.exe", rect=(10, 20, 810, 620)),
        WindowInfo(hwnd=2, title="EXILIUM", process_name="other.exe", rect=(0, 0, 100, 100)),
    ]

    selected = select_unique_window(windows, "EXILIUM", "GF2_Exilium.exe")

    assert selected.hwnd == 1


def test_select_unique_window_rejects_missing_or_ambiguous_target():
    target = WindowInfo(hwnd=1, title="EXILIUM", process_name="GF2_Exilium.exe", rect=(0, 0, 100, 100))
    with pytest.raises(CaptureError, match="found 0"):
        select_unique_window([], "EXILIUM", "GF2_Exilium.exe")
    with pytest.raises(CaptureError, match="found 2"):
        select_unique_window([target, target], "EXILIUM", "GF2_Exilium.exe")


def test_encode_bmp_writes_valid_top_down_32_bit_header():
    pixels = bytes.fromhex("0000ffff 00ff00ff")

    bitmap = encode_bmp(width=2, height=1, bgra_pixels=pixels)

    assert bitmap[:2] == b"BM"
    assert struct.unpack_from("<I", bitmap, 2)[0] == len(bitmap)
    assert struct.unpack_from("<I", bitmap, 10)[0] == 54
    assert struct.unpack_from("<i", bitmap, 22)[0] == -1
    assert struct.unpack_from("<H", bitmap, 28)[0] == 32
    assert bitmap[54:] == pixels


def test_encode_bmp_rejects_wrong_pixel_count():
    with pytest.raises(CaptureError, match="pixel buffer"):
        encode_bmp(width=2, height=2, bgra_pixels=b"short")


def test_write_capture_artifacts_writes_image_and_metadata(tmp_path):
    window = WindowInfo(hwnd=7, title="EXILIUM", process_name="GF2_Exilium.exe", rect=(5, 6, 7, 7))
    bitmap = encode_bmp(2, 1, bytes.fromhex("0000ffff 00ff00ff"))

    image_path, metadata_path = write_capture_artifacts(tmp_path, window, bitmap, "sample")

    assert image_path.read_bytes() == bitmap
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["window"] == {
        "hwnd": 7,
        "title": "EXILIUM",
        "process_name": "GF2_Exilium.exe",
        "rect": [5, 6, 7, 7],
    }
    assert metadata["image"] == "sample.bmp"
