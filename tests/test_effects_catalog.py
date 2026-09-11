from tools.effects_catalog import browser_catalog, canonicalize_effects, effect_id


def test_effect_id_is_deterministic_and_distinct():
    assert effect_id("Shield") == effect_id("Shield")
    assert effect_id("Shield") != effect_id("Shelter")


def test_legacy_aliases_migrate_to_id_keys_and_id_references():
    shield = {"name": "Khiên", "name_en": "Shield", "desc": "VI", "desc_en": "EN", "type": "buff", "sub_effects": []}
    guard = {"name": "Hộ Vệ", "name_en": "Guard", "desc": "VI", "desc_en": "EN", "type": "buff", "sub_effects": ["Shield"]}
    migrated = canonicalize_effects({"Shield": shield, "Khiên": shield, "Guard": guard})

    assert set(migrated) == {effect_id("Shield"), effect_id("Guard")}
    assert migrated[effect_id("Guard")]["sub_effect_ids"] == [effect_id("Shield")]


def test_browser_name_index_keeps_duplicate_names_as_separate_ids():
    first = {"id": "effect_a", "name": "Ẩn Nấp", "name_en": "Concealed", "desc": "", "desc_en": "", "type": "buff", "sub_effect_ids": []}
    second = {"id": "effect_b", "name": "Ẩn Nấp", "name_en": "Concealment", "desc": "", "desc_en": "", "type": "buff", "sub_effect_ids": []}
    payload = browser_catalog({"effect_a": first, "effect_b": second})

    assert payload["nameIndex"]["ẩn nấp"] == ["effect_a", "effect_b"]
