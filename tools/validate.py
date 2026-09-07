"""
validate.py — Pydantic v2 schema validation for all data/ JSON files.
Run before every build:  python tools/validate.py
Exits with code 1 if any file fails validation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator

ROOT = Path(__file__).parent.parent  # project root


# ─────────────────────────────────────────────────────────────────────────
#  ENUMS (as Literals to keep pydantic v2 compatible without importing Literal from typing_extensions)
# ─────────────────────────────────────────────────────────────────────────
VALID_CLASSES      = {"Bulwark", "Vanguard", "Support", "Sentinel"}
VALID_RARITIES     = {"Elite", "Standard"}
VALID_PHASES       = {"Physical", "Burn", "Hydro", "Electric", "Freeze", "Corrosion", "Resonance"}
VALID_WEAPON_TYPES = {"Assault Rifle", "SMG", "Shotgun", "MG", "Sniper Rifle", "Handgun", "Blade"}
VALID_AMMO_TYPES   = {"Light Ammo", "Medium Ammo", "Heavy Ammo", "Shotgun Ammo", "Melee"}
VALID_SKILL_TAGS   = {"Basic Attack", "Active", "Buff", "Debuff", "Targeted", "AoE", "Passive", "Healing", "Shield"}
VALID_W_RARITIES   = {"SSR", "SR", "R"}
VALID_SERVERS      = {"global", "cn"}


# ─────────────────────────────────────────────────────────────────────────
#  Character sub-models
# ─────────────────────────────────────────────────────────────────────────
class Stats(BaseModel):
    hp:  Optional[int] = None
    atk: Optional[int] = None
    def_: Optional[int] = Field(None, alias="def")

    model_config = {"populate_by_name": True}


class Skill(BaseModel):
    name:             str
    tags:             list[str] = []
    ammo_type:        Optional[str] = None
    stability_damage: Optional[Union[int, float]] = None
    cooldown:         Optional[str] = None
    confectance_cost: Optional[Union[int, float]] = None
    range:            Optional[Union[int, float]] = None
    effect_area:      Optional[str] = None
    description:      str = ""
    icon:             Optional[str] = None
    range_image:      Optional[str] = None

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v):
        unknown = set(v) - VALID_SKILL_TAGS
        if unknown:
            raise ValueError(f"Unknown skill tags: {unknown}. Valid: {VALID_SKILL_TAGS}")
        return v


class FortTier(BaseModel):
    tier:   int
    skill:  str
    level:  Optional[int] = None
    effect: str = ""


class NeuralHelixNode(BaseModel):
    node:      str
    level:     Optional[int] = None
    effect:    str = ""
    materials: Optional[str] = None
    image:     Optional[str] = None


class Key(BaseModel):
    name:      str
    level:     Optional[Union[int, str]] = None
    effect:    str = ""
    materials: Optional[str] = None
    image:     Optional[str] = None


class Images(BaseModel):
    portrait:   Optional[str] = None
    avatar:     Optional[str] = None
    class_icon: Optional[str] = None


class SummonStats(BaseModel):
    hp: Optional[Union[int, str]] = None
    atk: Optional[Union[int, str]] = None
    def_: Optional[Union[int, str]] = Field(None, alias="def")

    model_config = {"populate_by_name": True}


class SummonSkill(BaseModel):
    name: str
    description: str = ""
    icon: Optional[str] = None
    range_image: Optional[str] = None


class Summon(BaseModel):
    name: str
    description: Optional[str] = ""
    image: Optional[str] = None
    stats: Optional[SummonStats] = None
    stability_gauge: Optional[str] = None
    movement_speed: Optional[str] = None
    skills: list[SummonSkill] = []


# ─────────────────────────────────────────────────────────────────────────
#  Character (top-level)
# ─────────────────────────────────────────────────────────────────────────
class Character(BaseModel):
    slug:              str
    name:              str
    class_:            str  = Field(..., alias="class")
    rarity:            str
    phase:             str
    weapon_type:       str
    ammo_type:         Optional[str] = None
    signature_weapon:  Optional[str] = None
    stats:             Optional[Stats] = None
    skill_attribute:   Optional[str] = None
    weakness:          Optional[str] = None
    stability_gauge:   Optional[str] = None
    movement_speed:    Optional[str] = None
    effects_glossary:  Optional[list[str]] = None
    skills:            list[Skill] = []
    summons:           Optional[list[Summon]] = None
    fortification:     list[FortTier] = []
    neural_helix:      list[NeuralHelixNode] = []
    keys:              list[Key] = []
    images:            Optional[Images] = None
    server:            Optional[str] = "global"
    source_notes:      Optional[str] = None

    model_config = {"populate_by_name": True}

    @field_validator("server", mode="before")
    @classmethod
    def validate_server(cls, v):
        if v is not None and v.lower() not in VALID_SERVERS:
            raise ValueError(f"Invalid server '{v}'. Valid: {VALID_SERVERS}")
        return (v or "global").lower()

    @field_validator("class_", mode="before")
    @classmethod
    def validate_class(cls, v):
        if v not in VALID_CLASSES:
            raise ValueError(f"Invalid class '{v}'. Valid: {VALID_CLASSES}")
        return v

    @field_validator("rarity", mode="before")
    @classmethod
    def validate_rarity(cls, v):
        if v not in VALID_RARITIES:
            raise ValueError(f"Invalid rarity '{v}'. Valid: {VALID_RARITIES}")
        return v

    @field_validator("phase", mode="before")
    @classmethod
    def validate_phase(cls, v):
        if v not in VALID_PHASES:
            raise ValueError(f"Invalid phase '{v}'. Valid: {VALID_PHASES}")
        return v

    @field_validator("weapon_type", mode="before")
    @classmethod
    def validate_weapon_type(cls, v):
        if v not in VALID_WEAPON_TYPES:
            raise ValueError(f"Invalid weapon_type '{v}'. Valid: {VALID_WEAPON_TYPES}")
        return v

    @model_validator(mode="after")
    def check_fortification_length(self):
        if self.fortification and len(self.fortification) != 6:
            raise ValueError(
                f"fortification must have exactly 6 tiers, got {len(self.fortification)}"
            )
        return self


# ─────────────────────────────────────────────────────────────────────────
#  Weapon
# ─────────────────────────────────────────────────────────────────────────
class WeaponImages(BaseModel):
    weapon: Optional[str] = None


class Weapon(BaseModel):
    slug:        str
    name:        str
    weapon_type: Optional[str] = None
    rarity:      Optional[str] = None
    server:      Optional[str] = "global"
    stats:       Optional[str] = None
    trait:       Optional[str] = None
    effect:      Optional[str] = None
    images:      Optional[WeaponImages] = None

    @field_validator("server", mode="before")
    @classmethod
    def validate_weapon_server(cls, v):
        if v is not None and v.lower() not in VALID_SERVERS:
            raise ValueError(f"Invalid server '{v}'. Valid: {VALID_SERVERS}")
        return (v or "global").lower()



# ─────────────────────────────────────────────────────────────────────────
#  FAQ
# ─────────────────────────────────────────────────────────────────────────
class FaqEntry(BaseModel):
    question: str
    answer:   str


# ─────────────────────────────────────────────────────────────────────────
#  Runner
# ─────────────────────────────────────────────────────────────────────────
def validate_all() -> int:
    errors: list[str] = []
    ok = 0

    # Characters
    char_dir = ROOT / "data" / "characters"
    char_files = sorted(char_dir.glob("*.json")) if char_dir.exists() else []
    for path in char_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            Character.model_validate(data)
            ok += 1
        except Exception as e:
            errors.append(f"[CHARACTER] {path.name}: {e}")

    # Weapons
    weapons_path = ROOT / "data" / "weapons.json"
    if weapons_path.exists():
        try:
            data = json.loads(weapons_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                errors.append("[WEAPONS] weapons.json must be a JSON array")
            else:
                for i, w in enumerate(data):
                    try:
                        Weapon.model_validate(w)
                        ok += 1
                    except Exception as e:
                        errors.append(f"[WEAPON #{i}] {e}")
        except Exception as e:
            errors.append(f"[WEAPONS] {e}")

    # FAQ
    faq_path = ROOT / "data" / "faq.json"
    if faq_path.exists():
        try:
            data = json.loads(faq_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                errors.append("[FAQ] faq.json must be a JSON array")
            else:
                for i, q in enumerate(data):
                    try:
                        FaqEntry.model_validate(q)
                        ok += 1
                    except Exception as e:
                        errors.append(f"[FAQ #{i}] {e}")
        except Exception as e:
            errors.append(f"[FAQ] {e}")

    print(f"\nValidated {ok} record(s) across {len(char_files)} character file(s).")
    if errors:
        print(f"\n❌  {len(errors)} error(s) found:\n")
        for err in errors:
            print(f"  • {err}")
        return 1
    else:
        print("✅  All records valid.")
        return 0


if __name__ == "__main__":
    sys.exit(validate_all())
