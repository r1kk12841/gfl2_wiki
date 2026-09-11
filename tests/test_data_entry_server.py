import json
import subprocess
import sys
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

import pytest

from tools.data_entry_server import DataEntryHandler, DataEntryStore, DataEntryValidationError


ROOT = Path(__file__).resolve().parents[1]


def _fixture(tmp_path: Path) -> DataEntryStore:
    char_dir = tmp_path / "data" / "characters"
    char_dir.mkdir(parents=True)
    (char_dir / "alva.json").write_text(
        json.dumps({"slug": "alva", "name": "Alva", "source_notes": "keep"}),
        encoding="utf-8",
    )
    i18n = {"ui": {"title": "Wiki"}, "characters": {"alva": {"name": "Alva VI", "server": "global"}}}
    (tmp_path / "data" / "i18n_vi.json").write_text(json.dumps(i18n), encoding="utf-8")
    (tmp_path / "site" / "static" / "js").mkdir(parents=True)
    return DataEntryStore(tmp_path)


def test_updates_existing_english_character_without_creating_new_file(tmp_path: Path):
    store = _fixture(tmp_path)
    result = store.update_character("alva", "en", {"slug": "alva", "name": "Alva Updated"})

    saved = json.loads((tmp_path / "data" / "characters" / "alva.json").read_text(encoding="utf-8"))
    assert result["path"] == "data/characters/alva.json"
    assert saved["name"] == "Alva Updated"
    assert saved["source_notes"] == "keep"


def test_rejects_missing_source_and_slug_change(tmp_path: Path):
    store = _fixture(tmp_path)
    with pytest.raises(DataEntryValidationError, match="không tồn tại"):
        store.update_character("missing", "en", {"slug": "missing", "name": "Missing"})
    with pytest.raises(DataEntryValidationError, match="được đổi slug"):
        store.update_character("alva", "en", {"slug": "renamed", "name": "Alva"})
    assert not (tmp_path / "data" / "characters" / "missing.json").exists()


def test_updates_existing_vietnamese_record_and_generated_bundle(tmp_path: Path):
    store = _fixture(tmp_path)
    result = store.update_character("alva", "vi", {"name": "Alva Mới"})

    i18n = json.loads((tmp_path / "data" / "i18n_vi.json").read_text(encoding="utf-8"))
    generated = (tmp_path / "site" / "static" / "js" / "i18n-vi.js").read_text(encoding="utf-8")
    assert result["path"] == "data/i18n_vi.json#characters.alva"
    assert i18n["ui"] == {"title": "Wiki"}
    assert i18n["characters"]["alva"] == {"name": "Alva Mới", "server": "global"}
    assert '"name": "Alva Mới"' in generated


def test_rejects_new_vietnamese_record(tmp_path: Path):
    store = _fixture(tmp_path)
    with pytest.raises(DataEntryValidationError, match="không tồn tại"):
        store.update_character("missing", "vi", {"name": "Thiếu"})


def test_combined_editor_server_exposes_effect_api():
    server = ThreadingHTTPServer(("127.0.0.1", 0), DataEntryHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f"http://127.0.0.1:{server.server_port}/api/effects") as response:
            payload = json.load(response)
        assert response.status == 200
        assert payload["effects"]
        assert {"id", "name", "name_en"} <= payload["effects"][0].keys()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_editor_server_script_can_start_from_readme_command():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "data_entry_server.py"), "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "GFL2 local editor server" in result.stdout
