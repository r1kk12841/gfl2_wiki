import json
from pathlib import Path

import pytest

from tools.effect_editor.store import EffectStore, EffectValidationError


def _write_fixture(tmp_path: Path) -> tuple[Path, Path]:
    shield = {
        "id": "effect_shield",
        "name": "Khiên",
        "name_en": "Shield",
        "desc": "Hấp thụ sát thương.",
        "desc_en": "Absorbs damage.",
        "type": "buff",
        "sub_effect_ids": [],
    }
    guard = {
        "id": "effect_guard",
        "name": "Hộ Vệ",
        "name_en": "Guard",
        "desc": "Nhận Khiên.",
        "desc_en": "Gains Shield.",
        "type": "buff",
        "sub_effect_ids": ["effect_shield"],
    }
    effects = {"effect_shield": shield, "effect_guard": guard}
    effects_path = tmp_path / "effects_vi.json"
    i18n_path = tmp_path / "i18n_vi.json"
    effects_path.write_text(json.dumps(effects, ensure_ascii=False), encoding="utf-8")
    i18n_path.write_text(
        json.dumps({"ui": {"title": "Wiki"}, "effects": effects}, ensure_ascii=False),
        encoding="utf-8",
    )
    return effects_path, i18n_path


def test_list_effects_returns_one_row_per_english_effect_with_references(tmp_path: Path):
    effects_path, i18n_path = _write_fixture(tmp_path)
    rows = EffectStore(effects_path, i18n_path).list_effects()

    assert [row["name_en"] for row in rows] == ["Guard", "Shield"]
    shield = next(row for row in rows if row["name_en"] == "Shield")
    assert shield["id"] == "effect_shield"
    assert shield["referenced_by"] == [
        {"id": "effect_guard", "name_en": "Guard", "name": "Hộ Vệ"}
    ]


def test_rename_preserves_id_references_and_updates_i18n_bundle(tmp_path: Path):
    effects_path, i18n_path = _write_fixture(tmp_path)
    store = EffectStore(effects_path, i18n_path)

    result = store.update_effect(
        "effect_shield",
        {"name": "Lá Chắn", "desc": "Hấp thụ lượng sát thương nhận vào.", "type": "buff"},
    )

    effects = json.loads(effects_path.read_text(encoding="utf-8"))
    i18n = json.loads(i18n_path.read_text(encoding="utf-8"))
    assert result["preserved_references"] == 1
    assert set(effects) == {"effect_shield", "effect_guard"}
    assert effects["effect_shield"]["name"] == "Lá Chắn"
    assert effects["effect_shield"]["desc"] == "Hấp thụ lượng sát thương nhận vào."
    assert effects["effect_guard"]["sub_effect_ids"] == ["effect_shield"]
    assert i18n["ui"] == {"title": "Wiki"}
    assert i18n["effects"] == effects


def test_id_mapping_allows_duplicate_vietnamese_names_without_overwriting(tmp_path: Path):
    effects_path, i18n_path = _write_fixture(tmp_path)
    EffectStore(effects_path, i18n_path).update_effect(
        "effect_shield", {"name": "Hộ Vệ", "desc": "Mô tả", "type": "buff"}
    )
    effects = json.loads(effects_path.read_text(encoding="utf-8"))
    assert effects["effect_shield"]["name"] == "Hộ Vệ"
    assert effects["effect_guard"]["name"] == "Hộ Vệ"


def test_update_rejects_unknown_effect_and_invalid_type(tmp_path: Path):
    effects_path, i18n_path = _write_fixture(tmp_path)
    store = EffectStore(effects_path, i18n_path)

    with pytest.raises(EffectValidationError, match="không tồn tại"):
        store.update_effect("effect_missing", {"name": "Thiếu", "desc": "Mô tả", "type": "effect"})
    with pytest.raises(EffectValidationError, match="Loại hiệu ứng"):
        store.update_effect("effect_shield", {"name": "Khiên", "desc": "Mô tả", "type": "other"})


def test_existing_shared_vietnamese_name_remains_two_distinct_ids(tmp_path: Path):
    effects_path, i18n_path = _write_fixture(tmp_path)
    effects = json.loads(effects_path.read_text(encoding="utf-8"))
    second = {
        "id": "effect_barrier",
        "name": "Khiên",
        "name_en": "Barrier",
        "desc": "Khiên khác.",
        "desc_en": "Another shield.",
        "type": "buff",
        "sub_effect_ids": [],
    }
    effects["effect_barrier"] = second
    effects_path.write_text(json.dumps(effects, ensure_ascii=False), encoding="utf-8")

    EffectStore(effects_path, i18n_path).update_effect(
        "effect_shield", {"name": "Khiên", "desc": "Mô tả mới.", "type": "buff"}
    )

    updated = json.loads(effects_path.read_text(encoding="utf-8"))
    assert updated["effect_shield"]["desc"] == "Mô tả mới."
    assert updated["effect_barrier"]["name_en"] == "Barrier"


def test_create_effect_success(tmp_path: Path):
    effects_path, i18n_path = _write_fixture(tmp_path)
    store = EffectStore(effects_path, i18n_path)

    result = store.create_effect({
        "name_en": "Attack Boost I",
        "name": "Tăng Tấn Công I",
        "desc_en": "Attack is boosted by 10%.",
        "desc": "Tấn Công tăng 10%.",
        "type": "buff",
        "sub_effect_ids": ["effect_shield"],
    })

    effects = json.loads(effects_path.read_text(encoding="utf-8"))
    i18n = json.loads(i18n_path.read_text(encoding="utf-8"))

    new_id = result["effect"]["id"]
    assert new_id.startswith("effect_")
    assert new_id in effects
    assert effects[new_id]["name_en"] == "Attack Boost I"
    assert effects[new_id]["name"] == "Tăng Tấn Công I"
    assert effects[new_id]["sub_effect_ids"] == ["effect_shield"]
    assert i18n["effects"][new_id]["name"] == "Tăng Tấn Công I"


def test_create_effect_validations(tmp_path: Path):
    effects_path, i18n_path = _write_fixture(tmp_path)
    store = EffectStore(effects_path, i18n_path)

    # Empty name_en
    with pytest.raises(EffectValidationError, match="tiếng Anh"):
        store.create_effect({"name_en": "", "name": "A", "desc": "B", "type": "buff"})

    # Duplicate name_en
    with pytest.raises(EffectValidationError, match="đã tồn tại"):
        store.create_effect({"name_en": "Shield", "name": "Khiên 2", "desc": "B", "type": "buff"})

    # Empty name_vi
    with pytest.raises(EffectValidationError, match="tiếng Việt"):
        store.create_effect({"name_en": "New Effect", "name": "", "desc": "B", "type": "buff"})

    # Empty desc
    with pytest.raises(EffectValidationError, match="Mô tả"):
        store.create_effect({"name_en": "New Effect", "name": "Mới", "desc": "", "type": "buff"})

    # Invalid type
    with pytest.raises(EffectValidationError, match="Loại hiệu ứng"):
        store.create_effect({"name_en": "New Effect", "name": "Mới", "desc": "Mô tả", "type": "invalid"})

