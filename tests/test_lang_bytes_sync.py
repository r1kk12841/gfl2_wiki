import json
import struct
from pathlib import Path

from tools.parse_lang_bytes import parse_bytes


ROOT = Path(__file__).resolve().parents[1]


def _varint(value: int) -> bytes:
    result = bytearray()
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value)
    return bytes(result)


def test_parse_bytes_reads_language_entries_without_writing():
    text = "Yểm Hộ".encode("utf-8")
    inner = b"\x08" + _varint(22472) + b"\x12" + _varint(len(text)) + text
    body = b"\x0a" + _varint(len(inner)) + inner
    assert parse_bytes(struct.pack("<I", 0) + body) == [{"id": 22472, "text": "Yểm Hộ"}]


def test_all_weapons_have_vietnamese_records():
    weapons = json.loads((ROOT / "data/weapons.json").read_text(encoding="utf-8"))
    i18n = json.loads((ROOT / "data/i18n_vi.json").read_text(encoding="utf-8"))
    assert {weapon["slug"] for weapon in weapons} <= set(i18n["weapons"])


def test_verified_official_language_ids_are_applied():
    i18n = json.loads((ROOT / "data/i18n_vi.json").read_text(encoding="utf-8"))
    effects = json.loads((ROOT / "data/effects_vi.json").read_text(encoding="utf-8"))

    assert i18n["characters"]["alva"]["skills"][4]["name"] == "Chạm Vào Băng Kết"
    assert effects["effect_a8fbb45be7f6"]["name"] == "Yểm Hộ"
    assert i18n["effects"] == effects


def test_character_translation_lists_cover_source_records():
    i18n = json.loads((ROOT / "data/i18n_vi.json").read_text(encoding="utf-8"))
    for path in (ROOT / "data/characters").glob("*.json"):
        source = json.loads(path.read_text(encoding="utf-8"))
        translated = i18n["characters"][source["slug"]]
        for section in ("skills", "fortification", "neural_helix", "keys", "summons"):
            assert len(translated.get(section, [])) >= len(source.get(section, [])), f"{source['slug']}:{section}"


def test_character_skill_tags_are_non_empty_strings():
    i18n = json.loads((ROOT / "data/i18n_vi.json").read_text(encoding="utf-8"))
    for slug, character in i18n["characters"].items():
        for index, skill in enumerate(character.get("skills", [])):
            for tag in skill.get("tags", []):
                assert isinstance(tag, str) and tag.strip(), f"{slug}:skills[{index}].tags"
