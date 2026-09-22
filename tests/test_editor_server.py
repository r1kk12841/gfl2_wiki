from __future__ import annotations

import json
import socket
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_server import EditorServerHandler, create_editor_server


@pytest.fixture
def test_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    data_dir = repo / "data"
    data_dir.mkdir()
    char_dir = data_dir / "characters"
    char_dir.mkdir()
    guide_dir = data_dir / "guides"
    guide_dir.mkdir()
    js_dir = repo / "site" / "static" / "js"
    js_dir.mkdir(parents=True)

    # Effects fixture
    shield = {
        "id": "effect_shield",
        "name": "Khiên",
        "name_en": "Shield",
        "desc": "Hấp thụ sát thương.",
        "desc_en": "Absorbs damage.",
        "type": "buff",
        "sub_effect_ids": [],
    }
    interception = {
        "id": "effect_interception",
        "name": "Đánh chặn",
        "name_en": "Interception",
        "desc": "Chặn đòn tấn công.",
        "desc_en": "Intercepts attacks.",
        "type": "buff",
        "sub_effect_ids": [],
    }
    fort = {
        "id": "effect_fortress",
        "name": "Pháo Đài",
        "name_en": "Fortress",
        "desc": "Tạo khiên bảo vệ.",
        "desc_en": "Grants shield.",
        "type": "buff",
        "sub_effect_ids": ["effect_shield"],
    }
    effects = {"effect_shield": shield, "effect_interception": interception, "effect_fortress": fort}
    (data_dir / "effects_vi.json").write_text(json.dumps(effects, ensure_ascii=False, indent=2), encoding="utf-8")

    # i18n_vi fixture
    i18n_vi = {
        "ui": {"title": "GFL2 Wiki"},
        "effects": effects,
        "characters": {
            "alva": {"name": "Alva VI", "server": "global"}
        },
    }
    (data_dir / "i18n_vi.json").write_text(json.dumps(i18n_vi, ensure_ascii=False, indent=2), encoding="utf-8")

    # i18n-vi.js fixture
    (js_dir / "i18n-vi.js").write_text(
        f"window.I18N_VI = {json.dumps(i18n_vi, ensure_ascii=False, indent=2)};\n", encoding="utf-8"
    )

    # Character EN fixture
    (char_dir / "alva.json").write_text(
        json.dumps({"slug": "alva", "name": "Alva", "source_notes": "keep"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Guide fixture
    (guide_dir / "alva-starter.json").write_text(
        json.dumps({"slug": "alva-starter", "title": "Hướng dẫn Alva", "content": "Nội dung"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return repo


@pytest.fixture
def running_server(test_repo: Path):
    server = create_editor_server(repo_root=test_repo, host="127.0.0.1", port=0)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{port}"
    yield base_url
    server.shutdown()
    server.server_close()


def _request_json(url: str, method: str = "GET", body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if body is not None else {},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read().decode("utf-8"))


def test_api_health(running_server: str):
    status, payload = _request_json(f"{running_server}/api/health")
    assert status == 200
    assert payload["service"] == "gfl2-editor-server"
    assert payload["api_version"] == 1
    assert "characters" in payload["capabilities"]
    assert "effects" in payload["capabilities"]
    assert "guides" in payload["capabilities"]


def test_static_asset_path_decodes_url_escaped_spaces(running_server: str, test_repo: Path):
    weapon_dir = test_repo / "assets" / "images" / "weapons"
    weapon_dir.mkdir(parents=True)
    expected = b"weapon-thumbnail"
    (weapon_dir / "Thorn Criterion.png").write_bytes(expected)

    with urllib.request.urlopen(
        f"{running_server}/assets/images/weapons/Thorn%20Criterion.png",
        timeout=5,
    ) as response:
        assert response.status == 200
        assert response.read() == expected


def test_static_asset_path_cannot_escape_repository(running_server: str, test_repo: Path):
    (test_repo.parent / "outside.txt").write_text("private", encoding="utf-8")

    with pytest.raises(urllib.error.HTTPError) as error:
        urllib.request.urlopen(f"{running_server}/%2e%2e/outside.txt", timeout=5)

    assert error.value.code == 404


def test_list_effects(running_server: str):
    status, payload = _request_json(f"{running_server}/api/effects")
    assert status == 200
    assert "effects" in payload
    effects = {e["id"]: e for e in payload["effects"]}
    assert "effect_shield" in effects
    assert "effect_fortress" in effects
    # Verify reverse relationship
    assert any(ref["id"] == "effect_fortress" for ref in effects["effect_shield"]["referenced_by"])


def test_update_effect_success_and_bundle_sync(running_server: str, test_repo: Path):
    status, payload = _request_json(
        f"{running_server}/api/effects/effect_shield",
        method="PUT",
        body={"name": "Lá Chắn Mới", "desc": "Mô tả mới", "type": "buff"},
    )
    assert status == 200
    assert payload["effect"]["name"] == "Lá Chắn Mới"

    # Check files updated atomically
    effects_file = json.loads((test_repo / "data" / "effects_vi.json").read_text(encoding="utf-8"))
    i18n_file = json.loads((test_repo / "data" / "i18n_vi.json").read_text(encoding="utf-8"))
    js_file = (test_repo / "site" / "static" / "js" / "i18n-vi.js").read_text(encoding="utf-8")

    assert effects_file["effect_shield"]["name"] == "Lá Chắn Mới"
    assert i18n_file["effects"]["effect_shield"]["name"] == "Lá Chắn Mới"
    assert "Lá Chắn Mới" in js_file


def test_update_effect_sub_effects_add_and_remove(running_server: str, test_repo: Path):
    # 1. Add 'effect_interception' as sub-effect of 'effect_shield'
    status, payload = _request_json(
        f"{running_server}/api/effects/effect_shield",
        method="PUT",
        body={
            "name": "Khiên",
            "desc": "Hấp thụ sát thương.",
            "type": "buff",
            "sub_effect_ids": ["effect_interception"],
        },
    )
    assert status == 200
    assert payload["effect"]["sub_effect_ids"] == ["effect_interception"]

    # Verify 'effect_interception' now references 'effect_shield' in referenced_by
    _, list_payload = _request_json(f"{running_server}/api/effects")
    effects_map = {e["id"]: e for e in list_payload["effects"]}
    assert any(ref["id"] == "effect_shield" for ref in effects_map["effect_interception"]["referenced_by"])

    # 2. Remove 'effect_interception'
    status, payload = _request_json(
        f"{running_server}/api/effects/effect_shield",
        method="PUT",
        body={
            "name": "Khiên",
            "desc": "Hấp thụ sát thương.",
            "type": "buff",
            "sub_effect_ids": [],
        },
    )
    assert status == 200
    assert payload["effect"]["sub_effect_ids"] == []

    # Verify 'effect_interception' no longer has 'effect_shield' in referenced_by
    _, list_payload = _request_json(f"{running_server}/api/effects")
    effects_map = {e["id"]: e for e in list_payload["effects"]}
    assert not any(ref["id"] == "effect_shield" for ref in effects_map["effect_interception"]["referenced_by"])


def test_update_effect_rejects_self_reference(running_server: str):
    status, payload = _request_json(
        f"{running_server}/api/effects/effect_shield",
        method="PUT",
        body={
            "name": "Khiên",
            "desc": "Hấp thụ sát thương.",
            "type": "buff",
            "sub_effect_ids": ["effect_shield"],
        },
    )
    assert status == 400
    assert "tự tham chiếu" in payload["error"].lower() or "self" in payload["error"].lower()


def test_update_effect_rejects_nonexistent_sub_effect(running_server: str):
    status, payload = _request_json(
        f"{running_server}/api/effects/effect_shield",
        method="PUT",
        body={
            "name": "Khiên",
            "desc": "Hấp thụ sát thương.",
            "type": "buff",
            "sub_effect_ids": ["non_existent_effect_id"],
        },
    )
    assert status == 400
    assert "không tồn tại" in payload["error"].lower()


def test_update_character_en(running_server: str, test_repo: Path):
    status, payload = _request_json(
        f"{running_server}/api/characters/alva?lang=en",
        method="PUT",
        body={"slug": "alva", "name": "Alva Updated EN", "source_notes": "keep"},
    )
    assert status == 200
    saved = json.loads((test_repo / "data" / "characters" / "alva.json").read_text(encoding="utf-8"))
    assert saved["name"] == "Alva Updated EN"
    assert saved["source_notes"] == "keep"


def test_update_character_vi(running_server: str, test_repo: Path):
    status, payload = _request_json(
        f"{running_server}/api/characters/alva?lang=vi",
        method="PUT",
        body={"name": "Alva Mới VI"},
    )
    assert status == 200
    i18n = json.loads((test_repo / "data" / "i18n_vi.json").read_text(encoding="utf-8"))
    assert i18n["characters"]["alva"]["name"] == "Alva Mới VI"
    js = (test_repo / "site" / "static" / "js" / "i18n-vi.js").read_text(encoding="utf-8")
    assert "Alva Mới VI" in js


def test_guide_endpoints(running_server: str, test_repo: Path):
    # 1. Read existing guide
    status, payload = _request_json(f"{running_server}/api/guides/alva-starter")
    assert status == 200
    assert payload["title"] == "Hướng dẫn Alva"

    # 2. Update existing guide
    status, payload = _request_json(
        f"{running_server}/api/guides/alva-starter",
        method="PUT",
        body={"slug": "alva-starter", "title": "Hướng dẫn Alva V2", "content": "Updated"},
    )
    assert status == 200
    saved = json.loads((test_repo / "data" / "guides" / "alva-starter.json").read_text(encoding="utf-8"))
    assert saved["title"] == "Hướng dẫn Alva V2"

    # 3. Create new guide
    status, payload = _request_json(
        f"{running_server}/api/guides",
        method="POST",
        body={"slug": "new-guide", "title": "Guide Mới", "content": "Mới"},
    )
    assert status == 200
    assert (test_repo / "data" / "guides" / "new-guide.json").exists()

    # 4. Reject path traversal
    status, payload = _request_json(f"{running_server}/api/guides/..%2Fsecret")
    assert status in (400, 404)


def test_create_effect_endpoint(running_server: str, test_repo: Path):
    # 1. Successful creation
    status, payload = _request_json(
        f"{running_server}/api/effects",
        method="POST",
        body={
            "name_en": "Critical Rate Boost III",
            "name": "Tăng Tỷ Lệ Bạo Kích III",
            "desc_en": "Increases Crit Rate by 30%.",
            "desc": "Tỷ lệ bạo kích tăng 30%.",
            "type": "buff",
            "sub_effect_ids": ["effect_shield"],
        },
    )
    assert status == 201
    assert "effect" in payload
    created_id = payload["effect"]["id"]
    assert created_id.startswith("effect_")
    assert payload["effect"]["name"] == "Tăng Tỷ Lệ Bạo Kích III"

    # Check files updated
    effects_file = json.loads((test_repo / "data" / "effects_vi.json").read_text(encoding="utf-8"))
    i18n_file = json.loads((test_repo / "data" / "i18n_vi.json").read_text(encoding="utf-8"))
    js_file = (test_repo / "site" / "static" / "js" / "i18n-vi.js").read_text(encoding="utf-8")

    assert created_id in effects_file
    assert effects_file[created_id]["name"] == "Tăng Tỷ Lệ Bạo Kích III"
    assert created_id in i18n_file["effects"]
    assert "Tăng Tỷ Lệ Bạo Kích III" in js_file

    # 2. Reject duplicate name_en
    dup_status, dup_payload = _request_json(
        f"{running_server}/api/effects",
        method="POST",
        body={
            "name_en": "Critical Rate Boost III",
            "name": "Bản Sao",
            "desc": "Mô tả",
            "type": "buff",
        },
    )
    assert dup_status == 400
    assert "đã tồn tại" in dup_payload["error"]

    # 3. Reject missing required fields
    err_status, err_payload = _request_json(
        f"{running_server}/api/effects",
        method="POST",
        body={"name_en": "", "name": "Thiếu", "desc": "Mô tả"},
    )
    assert err_status == 400
    assert "tiếng Anh" in err_payload["error"]
