from __future__ import annotations

import socket
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.start_editors import check_port_status, probe_server_health


def test_probe_server_health_detects_editor_server(tmp_path: Path):
    from tools.editor_server import create_editor_server
    server = create_editor_server(repo_root=tmp_path, host="127.0.0.1", port=0)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        is_editor, info = probe_server_health("127.0.0.1", port)
        assert is_editor is True
        assert info.get("service") == "gfl2-editor-server"
    finally:
        server.shutdown()
        server.server_close()


def test_probe_server_health_detects_alien_server():
    # Run a dummy HTTP server returning 404 for /api/health (like python -m http.server)
    server = ThreadingHTTPServer(("127.0.0.1", 0), SimpleHTTPRequestHandler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        is_editor, info = probe_server_health("127.0.0.1", port)
        assert is_editor is False
    finally:
        server.shutdown()
        server.server_close()


def test_check_port_status_free_port():
    # Find a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    # Port is now free
    status, details = check_port_status("127.0.0.1", port)
    assert status == "free"
