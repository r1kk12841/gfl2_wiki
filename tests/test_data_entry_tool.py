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


def test_skill_tag_matching_ignores_null_or_non_string_values():
    source = APP_JS.read_text(encoding="utf-8")
    skill_source = source.split("function addSkillCard(data = {})", 1)[1].split(
        "function addSummonCard", 1
    )[0]
    assert "typeof tag === 'string'" in skill_source
    assert "const selectedTags" in skill_source


def test_key_add_button_is_present_and_wired():
    index_html = (ROOT / "tools" / "data-entry" / "index.html").read_text(encoding="utf-8")
    assert 'id="btn-add-key"' in index_html
    assert 'data-i18n="btn_add_key"' in index_html

    app_source = APP_JS.read_text(encoding="utf-8")
    assert "$('btn-add-key').addEventListener('click', () => addKeyRow());" in app_source

    i18n_source = (ROOT / "tools" / "data-entry" / "i18n.js").read_text(encoding="utf-8")
    assert "btn_add_key: '+ Add Key'" in i18n_source
    assert "btn_add_key: '+ Thêm Khóa'" in i18n_source


def test_character_server_field_is_present_and_wired():
    index_html = (ROOT / "tools" / "data-entry" / "index.html").read_text(encoding="utf-8")
    assert 'id="c-server"' in index_html
    assert 'data-i18n="field_server"' in index_html
    assert 'data-i18n="server_global"' in index_html
    assert 'data-i18n="server_cn"' in index_html

    app_source = APP_JS.read_text(encoding="utf-8")
    assert "server: $('c-server')?.value || 'global'" in app_source
    assert "c-source-notes').value = viChar.server" not in app_source
    assert "server: $('c-source-notes')" not in app_source

    i18n_source = (ROOT / "tools" / "data-entry" / "i18n.js").read_text(encoding="utf-8")
    assert "field_server: 'Server'" in i18n_source
    assert "field_server: 'Máy Chủ'" in i18n_source


