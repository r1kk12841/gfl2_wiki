"""
tests/test_data_schema.py
Validates all data/ JSON files against Pydantic models.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from tools.validate import (
    Character,
    Weapon,
    FaqEntry,
    VALID_CLASSES,
    VALID_RARITIES,
    VALID_PHASES,
    VALID_WEAPON_TYPES
)

ROOT = Path(__file__).resolve().parent.parent
CHAR_DIR = ROOT / "data" / "characters"
WEAPONS_FILE = ROOT / "data" / "weapons.json"
FAQ_FILE = ROOT / "data" / "faq.json"


def test_character_files_exist():
    char_files = list(CHAR_DIR.glob("*.json"))
    assert len(char_files) > 0, "No character JSON files found in data/characters/"


@pytest.mark.parametrize("char_path", list(CHAR_DIR.glob("*.json")), ids=lambda p: p.stem)
def test_each_character_schema(char_path: Path):
    data = json.loads(char_path.read_text(encoding="utf-8"))
    char = Character.model_validate(data)

    assert char.slug == char_path.stem
    assert "effects_glossary" not in data, f"{char.name} still contains effects_glossary"
    assert char.class_ in VALID_CLASSES
    assert char.rarity in VALID_RARITIES
    assert char.phase in VALID_PHASES
    assert char.weapon_type in VALID_WEAPON_TYPES
    if char.fortification:
        assert len(char.fortification) == 6, f"{char.name} does not have 6 fortification tiers"
    if char.neural_helix:
        assert len(char.neural_helix) == 6, f"{char.name} does not have 6 neural helix nodes"


def test_weapons_schema():
    assert WEAPONS_FILE.exists(), "weapons.json does not exist"
    weapons = json.loads(WEAPONS_FILE.read_text(encoding="utf-8"))
    assert isinstance(weapons, list)
    assert len(weapons) > 0

    for idx, w in enumerate(weapons):
        weapon = Weapon.model_validate(w)
        assert weapon.slug
        assert weapon.name


def test_faq_schema():
    assert FAQ_FILE.exists(), "faq.json does not exist"
    faqs = json.loads(FAQ_FILE.read_text(encoding="utf-8"))
    assert isinstance(faqs, list)
    assert len(faqs) > 0

    for idx, f in enumerate(faqs):
        faq = FaqEntry.model_validate(f)
        assert faq.question
        assert faq.answer
