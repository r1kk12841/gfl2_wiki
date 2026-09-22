from __future__ import annotations

import argparse
import json
import socket
import sys
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.editor_server import create_editor_server


def probe_server_health(host: str, port: int, timeout: float = 1.0) -> tuple[bool, dict[str, Any]]:
    """Probes http://<host>:<port>/api/health to verify if it is a gfl2-editor-server."""
    url = f"http://{host}:{port}/api/health"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "gfl2-editor-launcher"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("service") == "gfl2-editor-server":
                    return True, data
    except Exception:
        pass
    return False, {}


def check_port_status(host: str, port: int) -> tuple[str, dict[str, Any]]:
    """
    Checks if a port is free, already running the editor server, or occupied by an alien process.
    Returns:
      ("free", {})
      ("running_editor", health_dict)
      ("conflict", {})
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.connect((host, port))
        except (socket.error, OSError):
            return "free", {}

    # Connection succeeded, probe health
    is_editor, info = probe_server_health(host, port)
    if is_editor:
        return "running_editor", info
    return "conflict", {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Khởi động bộ công cụ GFL2 Exilium Wiki Editor Hub")
    parser.add_argument("--host", default="127.0.0.1", help="Địa chỉ host (mặc định: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Cổng lắng nghe (mặc định: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Không tự động mở trình duyệt")
    args = parser.parse_args()

    hub_url = f"http://{args.host}:{args.port}/tools/index.html"

    status, details = check_port_status(args.host, args.port)
    if status == "running_editor":
        print(f"[*] Editor Server đã đang chạy tại http://{args.host}:{args.port}")
        print(f"[*] Mở Editor Hub: {hub_url}")
        if not args.no_browser:
            webbrowser.open(hub_url)
        sys.exit(0)

    if status == "conflict":
        print(f"[!] LỖI: Cổng {args.port} tại {args.host} đang bị chiếm bởi một tiến trình khác (hoặc static server).", file=sys.stderr)
        print(f"[!] Hướng dẫn giải quyết:", file=sys.stderr)
        print(f"    1. Tắt tiến trình đang chiếm cổng (ví dụ cửa sổ chạy 'python -m http.server {args.port}').", file=sys.stderr)
        print(f"    2. Hoặc khởi động editor server trên cổng khác: python tools/start_editors.py --port 8080", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Đang khởi động GFL2 Unified Editor Server tại http://{args.host}:{args.port}...")
    server = create_editor_server(repo_root=ROOT, host=args.host, port=args.port)
    actual_port = server.server_port
    actual_hub_url = f"http://{args.host}:{actual_port}/tools/index.html"

    print(f"[✓] Server sẵn sàng tại: http://{args.host}:{actual_port}")
    print(f"[✓] Editor Hub: {actual_hub_url}")
    print(f"[✓] Data Entry: http://{args.host}:{actual_port}/tools/data-entry/index.html")
    print(f"[✓] Effect Editor: http://{args.host}:{actual_port}/tools/effect_editor/index.html")
    print(f"[✓] Guide Editor: http://{args.host}:{actual_port}/tools/guide-editor/index.html")
    print("[*] Nhấn Ctrl+C để dừng server.\n")

    if not args.no_browser:
        webbrowser.open(actual_hub_url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Đang dừng server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
