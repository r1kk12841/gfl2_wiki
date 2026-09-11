from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import tempfile
import threading
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.effect_editor.store import EffectStore, EffectValidationError


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class DataEntryValidationError(ValueError):
    pass


class DataEntryStore:
    """Update existing source records only; never create a character implicitly."""

    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self._lock = threading.Lock()

    @staticmethod
    def _read_object(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DataEntryValidationError(f"Không thể đọc {path.name}: {exc}") from exc
        if not isinstance(value, dict):
            raise DataEntryValidationError(f"{path.name} phải chứa JSON object.")
        return value

    @staticmethod
    def _json_text(value: dict[str, Any]) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"

    @staticmethod
    def _stage(path: Path, content: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        return Path(temp_name)

    def _replace_all(self, outputs: list[tuple[Path, str]]) -> None:
        staged = [(path, self._stage(path, content)) for path, content in outputs]
        originals = {path: path.read_bytes() if path.exists() else None for path, _ in staged}
        replaced: list[Path] = []
        try:
            for path, temp_path in staged:
                os.replace(temp_path, path)
                replaced.append(path)
        except Exception:
            for path in reversed(replaced):
                original = originals[path]
                if original is not None:
                    rollback = self._stage(path, original.decode("utf-8-sig"))
                    os.replace(rollback, path)
            raise
        finally:
            for _, temp_path in staged:
                temp_path.unlink(missing_ok=True)

    def update_character(self, slug: str, lang: str, payload: dict[str, Any]) -> dict[str, str]:
        if not SLUG_RE.fullmatch(slug):
            raise DataEntryValidationError("Slug không hợp lệ.")
        if lang not in {"en", "vi"}:
            raise DataEntryValidationError("Ngôn ngữ phải là en hoặc vi.")
        if not isinstance(payload, dict) or not str(payload.get("name", "")).strip():
            raise DataEntryValidationError("Dữ liệu nhân vật phải có tên.")

        with self._lock:
            if lang == "en":
                path = self.root / "data" / "characters" / f"{slug}.json"
                if not path.is_file():
                    raise DataEntryValidationError(f"File gốc data/characters/{slug}.json không tồn tại; nút này không tạo file mới.")
                payload_slug = str(payload.get("slug", slug)).strip()
                if payload_slug != slug:
                    raise DataEntryValidationError("Không được đổi slug khi cập nhật file gốc.")
                merged = self._read_object(path)
                merged.update(copy.deepcopy(payload))
                self._replace_all([(path, self._json_text(merged))])
                return {"path": f"data/characters/{slug}.json", "lang": lang}

            i18n_path = self.root / "data" / "i18n_vi.json"
            js_path = self.root / "site" / "static" / "js" / "i18n-vi.js"
            bundle = self._read_object(i18n_path)
            characters = bundle.get("characters")
            if not isinstance(characters, dict) or slug not in characters:
                raise DataEntryValidationError(f"Bản ghi gốc characters.{slug} không tồn tại trong i18n_vi.json; nút này không tạo bản ghi mới.")
            existing = characters[slug]
            if not isinstance(existing, dict):
                raise DataEntryValidationError(f"Bản ghi characters.{slug} không hợp lệ.")
            merged = copy.deepcopy(existing)
            merged.update(copy.deepcopy(payload))
            characters[slug] = merged
            json_text = self._json_text(bundle)
            js_text = (
                "// Auto-generated Vietnamese Localization Bundle for GFL2: Exilium Wiki\n"
                f"window.GFL2_I18N_VI = {json.dumps(bundle, ensure_ascii=False, indent=2)};\n"
            )
            self._replace_all([(i18n_path, json_text), (js_path, js_text)])
            return {"path": f"data/i18n_vi.json#characters.{slug}", "lang": lang}


STORE = DataEntryStore(ROOT)
EFFECT_STORE = EffectStore(
    ROOT / "data" / "effects_vi.json",
    ROOT / "data" / "i18n_vi.json",
    ROOT / "site" / "static" / "js" / "i18n-vi.js",
)
EDITOR_WRITE_LOCK = threading.Lock()


class DataEntryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/effects":
            try:
                self._send_json({"effects": EFFECT_STORE.list_effects()})
            except EffectValidationError as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if path == "/":
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/tools/data-entry/index.html")
            self.end_headers()
            return
        super().do_GET()

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        character_prefix = "/api/characters/"
        effect_prefix = "/api/effects/"
        if not parsed.path.startswith((character_prefix, effect_prefix)):
            self._send_json({"error": "Không tìm thấy API."}, HTTPStatus.NOT_FOUND)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 2_000_000:
                raise DataEntryValidationError("Nội dung lưu không hợp lệ.")
            payload = json.loads(self.rfile.read(size).decode("utf-8"))
            if not isinstance(payload, dict):
                raise DataEntryValidationError("Nội dung lưu phải là JSON object.")
            with EDITOR_WRITE_LOCK:
                if parsed.path.startswith(effect_prefix):
                    result = EFFECT_STORE.update_effect(
                        unquote(parsed.path[len(effect_prefix) :]), payload
                    )
                else:
                    lang = parse_qs(parsed.query).get("lang", ["en"])[0]
                    result = STORE.update_character(
                        unquote(parsed.path[len(character_prefix) :]), lang, payload
                    )
            self._send_json(result)
        except (
            DataEntryValidationError,
            EffectValidationError,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ) as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except OSError as exc:
            self._send_json({"error": f"Không thể ghi dữ liệu: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)


def main() -> int:
    parser = argparse.ArgumentParser(description="GFL2 local editor server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DataEntryHandler)
    url = f"http://{args.host}:{server.server_port}/tools/data-entry/index.html"
    print(f"Data entry tool: {url}")
    print(f"Effect editor: http://{args.host}:{server.server_port}/tools/effect_editor/")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
