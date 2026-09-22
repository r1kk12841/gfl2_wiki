from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from tools.effect_editor.store import EffectStore, EffectValidationError
else:
    from .store import EffectStore, EffectValidationError


ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = Path(__file__).resolve().parent
STORE = EffectStore(
    ROOT / "data" / "effects_vi.json",
    ROOT / "data" / "i18n_vi.json",
    ROOT / "site" / "static" / "js" / "i18n-vi.js",
)


class EffectEditorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

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
                self._send_json({"effects": STORE.list_effects()})
            except EffectValidationError as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_PUT(self) -> None:
        path = urlparse(self.path).path
        prefix = "/api/effects/"
        if not path.startswith(prefix):
            self._send_json({"error": "Không tìm thấy API."}, HTTPStatus.NOT_FOUND)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 100_000:
                raise EffectValidationError("Nội dung lưu không hợp lệ.")
            payload = json.loads(self.rfile.read(size).decode("utf-8"))
            if not isinstance(payload, dict):
                raise EffectValidationError("Nội dung lưu phải là JSON object.")
            result = STORE.update_effect(unquote(path[len(prefix) :]), payload)
            self._send_json(result)
        except (EffectValidationError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except OSError as exc:
            self._send_json({"error": f"Không thể ghi dữ liệu: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/effects":
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > 100_000:
                    raise EffectValidationError("Nội dung tạo không hợp lệ.")
                payload = json.loads(self.rfile.read(size).decode("utf-8"))
                if not isinstance(payload, dict):
                    raise EffectValidationError("Nội dung tạo phải là JSON object.")
                result = STORE.create_effect(payload)
                self._send_json(result, HTTPStatus.CREATED)
            except (EffectValidationError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except OSError as exc:
                self._send_json({"error": f"Không thể ghi dữ liệu: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        self._send_json({"error": "Không tìm thấy API."}, HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {format % args}")


def main() -> int:
    parser = argparse.ArgumentParser(description="GFL2 Vietnamese effect editor (Wrapper)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    from tools.editor_server import create_editor_server
    server = create_editor_server(ROOT, host=args.host, port=args.port)
    url = f"http://{args.host}:{server.server_port}/tools/effect_editor/index.html"
    print(f"Effect editor: {url}")
    print(f"Editor Hub: http://{args.host}:{server.server_port}/tools/index.html")
    print("Nhấn Ctrl+C để dừng.")
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

