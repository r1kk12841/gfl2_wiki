from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_JS = ROOT / "tools" / "data-entry" / "app.js"
README = ROOT / "README.md"


def test_app_does_not_redeclare_i18n_global_bindings():
    source = APP_JS.read_text(encoding="utf-8")
    assert "const t = (key" not in source
    assert "const mapTerm = (term" not in source
    assert "const getTermList = (cat" not in source


def test_character_save_updates_source_through_local_api():
    source = APP_JS.read_text(encoding="utf-8")
    save_source = source.split("async function saveToFileSystem()", 1)[1].split(
        "async function downloadFullI18nVi()", 1
    )[0]
    assert "/api/characters/" in save_source
    assert "showSaveFilePicker" not in save_source
    assert "downloadFile(" not in save_source


def test_readme_starts_api_capable_editor_server():
    source = README.read_text(encoding="utf-8")
    assert "python tools/data_entry_server.py" in source
    assert "python -m http.server 8000" not in source
