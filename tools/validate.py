"""
validate.py — Pydantic v2 schema validation for all data/ JSON files.
Run before every build:  python tools/validate.py
Exits with code 1 if any file fails validation.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ROOT = Path(__file__).parent.parent  # project root

SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


# ─────────────────────────────────────────────────────────────────────────
#  Base Strict Model
# ─────────────────────────────────────────────────────────────────────────
class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_default=True,
    )


# ─────────────────────────────────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────────────────────────────────
VALID_CLASSES      = {"Bulwark", "Vanguard", "Support", "Sentinel"}
VALID_RARITIES     = {"Elite", "Standard"}
VALID_PHASES       = {"Physical", "Burn", "Hydro", "Electric", "Freeze", "Corrosion", "Resonance"}
VALID_WEAPON_TYPES = {"Assault Rifle", "SMG", "Shotgun", "MG", "Sniper Rifle", "Handgun", "Blade"}
VALID_AMMO_TYPES   = {"Light Ammo", "Medium Ammo", "Heavy Ammo", "Shotgun Ammo", "Melee"}
VALID_SKILL_TAGS   = {"Basic Attack", "Active", "Buff", "Debuff", "Targeted", "AoE", "Passive", "Healing", "Shield", "Skill", "Ultimate", "Summon"}
VALID_W_RARITIES   = {"SSR", "SR", "R"}
VALID_SERVERS      = {"global", "cn"}


# ─────────────────────────────────────────────────────────────────────────
#  Character sub-models
# ─────────────────────────────────────────────────────────────────────────
class Stats(StrictModel):
    hp:  Optional[int] = None
    atk: Optional[int] = None
    def_: Optional[int] = Field(None, alias="def")

    @field_validator("hp", "atk", "def_")
    @classmethod
    def validate_non_negative_stats(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} must be non-negative")
        return v


class Skill(StrictModel):
    name:             str
    tags:             list[str] = Field(default_factory=list)
    ammo_type:        Optional[str] = None
    stability_damage: Optional[Union[int, float]] = None
    cooldown:         Optional[str] = None
    confectance_cost: Optional[Union[int, float]] = None
    range:            Optional[Union[int, float, str]] = None
    effect_area:      Optional[str] = None
    description:      str = ""
    icon:             Optional[str] = None
    range_image:      Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()

    @field_validator("stability_damage", "confectance_cost")
    @classmethod
    def validate_non_negative(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} must be non-negative")
        return v

    @field_validator("range")
    @classmethod
    def validate_range(cls, v):
        if isinstance(v, (int, float)) and v < 0:
            raise ValueError("range must be non-negative")
        return v


class FortTier(StrictModel):
    tier:   int
    skill:  str
    level:  Optional[int] = None
    effect: str = ""

    @field_validator("tier")
    @classmethod
    def validate_tier(cls, v):
        if not (1 <= v <= 6):
            raise ValueError(f"tier must be between 1 and 6, got {v}")
        return v


class NeuralHelixNode(StrictModel):
    node:      str
    level:     Optional[int] = None
    effect:    str = ""
    materials: Optional[str] = None
    image:     Optional[str] = None


class Key(StrictModel):
    name:      str
    level:     Optional[Union[int, str]] = None
    effect:    str = ""
    materials: Optional[str] = None
    image:     Optional[str] = None


class Images(StrictModel):
    portrait:      Optional[str] = None
    avatar:        Optional[str] = None
    class_icon:    Optional[str] = None
    portrait_webp: Optional[str] = None


class SummonStats(StrictModel):
    hp: Optional[Union[int, str]] = None
    atk: Optional[Union[int, str]] = None
    def_: Optional[Union[int, str]] = Field(None, alias="def")


class SummonSkill(Skill):
    pass


class Summon(StrictModel):
    name: str
    description: Optional[str] = ""
    image: Optional[str] = None
    stats: Optional[SummonStats] = None
    stability_gauge: Optional[str] = None
    movement_speed: Optional[str] = None
    skills: list[SummonSkill] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────
#  Character (top-level)
# ─────────────────────────────────────────────────────────────────────────
class Character(StrictModel):
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
    skills:            list[Skill] = Field(default_factory=list)
    summons:           Optional[list[Summon]] = None
    fortification:     list[FortTier] = Field(default_factory=list)
    neural_helix:      list[NeuralHelixNode] = Field(default_factory=list)
    keys:              list[Key] = Field(default_factory=list)
    images:            Optional[Images] = None
    server:            Optional[str] = "global"
    source_notes:      Optional[str] = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if not SLUG_REGEX.match(v):
            raise ValueError(f"slug '{v}' must be lowercase kebab-case matching regex ^[a-z0-9]+(?:-[a-z0-9]+)*$")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()

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
    def check_character_relations(self):
        # Fortification must have exactly tiers 1 through 6 without duplicate tiers
        if self.fortification:
            if len(self.fortification) != 6:
                raise ValueError(
                    f"fortification must have exactly 6 tiers, got {len(self.fortification)}"
                )
            tiers = [f.tier for f in self.fortification]
            if sorted(tiers) != [1, 2, 3, 4, 5, 6]:
                raise ValueError(
                    f"fortification must contain tiers 1 through 6 without duplicates, got {tiers}"
                )
        # Neural Helix must not have duplicate nodes
        if self.neural_helix:
            nodes = [n.node for n in self.neural_helix]
            if len(nodes) != len(set(nodes)):
                raise ValueError(f"neural_helix contains duplicate nodes: {nodes}")
        return self


# ─────────────────────────────────────────────────────────────────────────
#  Weapon
# ─────────────────────────────────────────────────────────────────────────
class WeaponImages(StrictModel):
    weapon: Optional[str] = None


class Weapon(StrictModel):
    slug:        str
    name:        str
    weapon_type: Optional[str] = None
    rarity:      Optional[str] = None
    server:      Optional[str] = "global"
    stats:       Optional[str] = None
    trait:       Optional[str] = None
    effect:      Optional[str] = None
    images:      Optional[WeaponImages] = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if not SLUG_REGEX.match(v):
            raise ValueError(f"slug '{v}' must be lowercase kebab-case matching regex ^[a-z0-9]+(?:-[a-z0-9]+)*$")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()

    @field_validator("weapon_type")
    @classmethod
    def validate_weapon_type(cls, v):
        if v is not None and v not in VALID_WEAPON_TYPES:
            raise ValueError(f"Invalid weapon_type '{v}'. Valid: {VALID_WEAPON_TYPES}")
        return v

    @field_validator("rarity")
    @classmethod
    def validate_rarity(cls, v):
        if v is not None and v not in VALID_W_RARITIES:
            raise ValueError(f"Invalid rarity '{v}'. Valid: {VALID_W_RARITIES}")
        return v

    @field_validator("server", mode="before")
    @classmethod
    def validate_weapon_server(cls, v):
        if v is not None and v.lower() not in VALID_SERVERS:
            raise ValueError(f"Invalid server '{v}'. Valid: {VALID_SERVERS}")
        return (v or "global").lower()


# ─────────────────────────────────────────────────────────────────────────
#  FAQ
# ─────────────────────────────────────────────────────────────────────────
class FaqEntry(StrictModel):
    question: str
    answer:   str

    @field_validator("question", "answer")
    @classmethod
    def validate_not_empty(cls, v, info):
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v.strip()


# ─────────────────────────────────────────────────────────────────────────
#  Guide Models
# ─────────────────────────────────────────────────────────────────────────
class GuideHeadingBlock(StrictModel):
    type: Literal["heading"]
    level: int
    text: str

    @field_validator("level")
    @classmethod
    def validate_level(cls, v):
        if not (1 <= v <= 6):
            raise ValueError(f"Heading level must be between 1 and 6, got {v}")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Heading text cannot be empty")
        return v.strip()


class GuideParagraphBlock(StrictModel):
    type: Literal["paragraph"]
    html: str

    @field_validator("html")
    @classmethod
    def validate_html(cls, v):
        if not v or not v.strip():
            raise ValueError("Paragraph HTML cannot be empty")
        # Ensure no dangerous tags
        dangerous = ["<script", "javascript:", "onload=", "onerror=", "onclick=", "<iframe", "<style", "<object", "<embed"]
        for d in dangerous:
            if d in v.lower():
                raise ValueError(f"Dangerous content detected in paragraph HTML: '{d}'")
        return v


class GuideLinkBlock(StrictModel):
    type: Literal["link"]
    url: str
    text: Optional[str] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        v = v.strip()
        if not (v.startswith("http://") or v.startswith("https://") or v.startswith("/") or v.startswith("./") or v.startswith("../")):
            raise ValueError(f"Invalid or unsafe URL in guide link: '{v}'")
        return v


class GuideCharCardBlock(StrictModel):
    type: Literal["char_card"]
    slug: str


class GuideWeaponCardBlock(StrictModel):
    type: Literal["weapon_card"]
    slug: str


class GuideSkillRefBlock(StrictModel):
    type: Literal["skill_ref"]
    char: str
    skill_idx: int

    @field_validator("skill_idx")
    @classmethod
    def validate_idx(cls, v):
        if v < 0:
            raise ValueError("skill_idx must be non-negative")
        return v


class GuideSummonSkillRefBlock(StrictModel):
    type: Literal["summon_skill_ref"]
    char: str
    summon_idx: int
    skill_idx: int

    @field_validator("summon_idx", "skill_idx")
    @classmethod
    def validate_idx(cls, v, info):
        if v < 0:
            raise ValueError(f"{info.field_name} must be non-negative")
        return v


class GuideTableBlock(StrictModel):
    type: Literal["table"]
    headers: list[str] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)


class GuideImageBlock(StrictModel):
    type: Literal["image"]
    src: str
    caption: Optional[str] = None
    alt: Optional[str] = None


GuideBlock = Annotated[
    Union[
        GuideHeadingBlock,
        GuideParagraphBlock,
        GuideLinkBlock,
        GuideCharCardBlock,
        GuideWeaponCardBlock,
        GuideSkillRefBlock,
        GuideSummonSkillRefBlock,
        GuideTableBlock,
        GuideImageBlock,
    ],
    Field(discriminator="type"),
]


class Guide(StrictModel):
    slug: str
    title: str
    char_slug: Optional[str] = None
    last_updated: Optional[str] = None
    author: Optional[str] = None
    blocks: list[GuideBlock] = Field(default_factory=list)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if not SLUG_REGEX.match(v):
            raise ValueError(f"slug '{v}' must be lowercase kebab-case matching regex ^[a-z0-9]+(?:-[a-z0-9]+)*$")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()


# ─────────────────────────────────────────────────────────────────────────
#  Asset Path Helper
# ─────────────────────────────────────────────────────────────────────────
def _check_asset_path(path_str: str | None, context: str, errors: list[str]) -> None:

    if not path_str:
        return
    # Must be relative, no path traversal, no URL
    if path_str.startswith("/") or path_str.startswith("\\") or re.match(r"^[a-zA-Z]:", path_str):
        errors.append(f"[{context}] Asset path must be relative: '{path_str}'")
        return
    parts = path_str.replace("\\", "/").split("/")
    if ".." in parts:
        errors.append(f"[{context}] Asset path cannot contain '..': '{path_str}'")
        return
    if path_str.startswith("http://") or path_str.startswith("https://"):
        errors.append(f"[{context}] Asset path cannot be an external URL: '{path_str}'")
        return
    full_path = ROOT / path_str
    if not full_path.exists():
        errors.append(f"[{context}] Asset file does not exist: '{path_str}'")


# ─────────────────────────────────────────────────────────────────────────
#  Runner
# ─────────────────────────────────────────────────────────────────────────
def validate_all(strict_signature_weapons: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    ok = 0

    loaded_characters: list[Character] = []
    loaded_weapons: list[Weapon] = []
    loaded_faq: list[FaqEntry] = []

    # 1. Characters validation
    char_dir = ROOT / "data" / "characters"
    char_files = sorted(char_dir.glob("*.json")) if char_dir.exists() else []
    char_slugs_seen: set[str] = set()

    for path in char_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            char = Character.model_validate(data)
            loaded_characters.append(char)
            ok += 1

            # Check filename matches slug
            if char.slug != path.stem:
                errors.append(f"[CHARACTER FILE] Filename '{path.name}' does not match slug '{char.slug}'")

            # Check unique slug
            if char.slug in char_slugs_seen:
                errors.append(f"[CHARACTER] Duplicate character slug '{char.slug}' in {path.name}")
            char_slugs_seen.add(char.slug)

            # Check asset paths in character
            if char.images:
                _check_asset_path(char.images.portrait, f"CHAR:{char.slug}:portrait", errors)
                _check_asset_path(char.images.avatar, f"CHAR:{char.slug}:avatar", errors)
                _check_asset_path(char.images.class_icon, f"CHAR:{char.slug}:class_icon", errors)
                _check_asset_path(char.images.portrait_webp, f"CHAR:{char.slug}:portrait_webp", errors)

            for idx, sk in enumerate(char.skills):
                _check_asset_path(sk.icon, f"CHAR:{char.slug}:skill[{idx}]:icon", errors)
                _check_asset_path(sk.range_image, f"CHAR:{char.slug}:skill[{idx}]:range_image", errors)

            for idx, nh in enumerate(char.neural_helix):
                _check_asset_path(nh.image, f"CHAR:{char.slug}:neural_helix[{idx}]", errors)

            for idx, k in enumerate(char.keys):
                _check_asset_path(k.image, f"CHAR:{char.slug}:key[{idx}]", errors)

            if char.summons:
                for s_idx, sm in enumerate(char.summons):
                    _check_asset_path(sm.image, f"CHAR:{char.slug}:summon[{s_idx}]", errors)
                    for sk_idx, s_sk in enumerate(sm.skills):
                        _check_asset_path(s_sk.icon, f"CHAR:{char.slug}:summon[{s_idx}]:skill[{sk_idx}]:icon", errors)
                        _check_asset_path(s_sk.range_image, f"CHAR:{char.slug}:summon[{s_idx}]:skill[{sk_idx}]:range_image", errors)

        except Exception as e:
            errors.append(f"[CHARACTER] {path.name}: {e}")

    # 2. Weapons validation
    weapons_path = ROOT / "data" / "weapons.json"
    weapon_slugs_seen: set[str] = set()

    if weapons_path.exists():
        try:
            data = json.loads(weapons_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                errors.append("[WEAPONS] weapons.json must be a JSON array")
            else:
                for i, w in enumerate(data):
                    try:
                        weapon = Weapon.model_validate(w)
                        loaded_weapons.append(weapon)
                        ok += 1

                        if weapon.slug in weapon_slugs_seen:
                            errors.append(f"[WEAPON #{i}] Duplicate weapon slug '{weapon.slug}'")
                        weapon_slugs_seen.add(weapon.slug)

                        if weapon.images:
                            _check_asset_path(weapon.images.weapon, f"WEAPON:{weapon.slug}:weapon", errors)

                    except Exception as e:
                        errors.append(f"[WEAPON #{i}] {e}")
        except Exception as e:
            errors.append(f"[WEAPONS] {e}")

    # 3. FAQ validation
    faq_path = ROOT / "data" / "faq.json"
    faq_seen: set[str] = set()

    if faq_path.exists():
        try:
            data = json.loads(faq_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                errors.append("[FAQ] faq.json must be a JSON array")
            else:
                for i, q in enumerate(data):
                    try:
                        faq_entry = FaqEntry.model_validate(q)
                        loaded_faq.append(faq_entry)
                        ok += 1

                        norm_q = " ".join(faq_entry.question.lower().split())
                        if norm_q in faq_seen:
                            errors.append(f"[FAQ #{i}] Duplicate FAQ question: '{faq_entry.question}'")
                        faq_seen.add(norm_q)

                    except Exception as e:
                        errors.append(f"[FAQ #{i}] {e}")
        except Exception as e:
            errors.append(f"[FAQ] {e}")

    # 4. Guides validation
    guides_dir = ROOT / "data" / "guides"
    loaded_guides: list[Guide] = []
    guide_slugs_seen: set[str] = set()

    if guides_dir.exists():
        char_map = {c.slug: c for c in loaded_characters}
        weapon_map = {w.slug: w for w in loaded_weapons}

        for path in sorted(guides_dir.glob("*.json")):
            if path.name.startswith("."):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                guide = Guide.model_validate(data)
                loaded_guides.append(guide)
                ok += 1

                if guide.slug != path.stem:
                    errors.append(f"[GUIDE FILE] Filename '{path.name}' does not match slug '{guide.slug}'")

                if guide.slug in guide_slugs_seen:
                    errors.append(f"[GUIDE] Duplicate guide slug '{guide.slug}' in {path.name}")
                guide_slugs_seen.add(guide.slug)

                # Relational checks
                if guide.char_slug and guide.char_slug not in char_map:
                    errors.append(f"[GUIDE:{guide.slug}] char_slug '{guide.char_slug}' not found in characters")

                for b_idx, block in enumerate(guide.blocks):
                    if block.type == "char_card":
                        if block.slug not in char_map:
                            errors.append(f"[GUIDE:{guide.slug}] block[{b_idx}] char_card slug '{block.slug}' not found")
                    elif block.type == "weapon_card":
                        if block.slug not in weapon_map:
                            errors.append(f"[GUIDE:{guide.slug}] block[{b_idx}] weapon_card slug '{block.slug}' not found")
                    elif block.type == "skill_ref":
                        if block.char not in char_map:
                            errors.append(f"[GUIDE:{guide.slug}] block[{b_idx}] skill_ref char '{block.char}' not found")
                        else:
                            c = char_map[block.char]
                            if block.skill_idx >= len(c.skills):
                                errors.append(f"[GUIDE:{guide.slug}] block[{b_idx}] skill_ref index {block.skill_idx} out of range for '{block.char}' ({len(c.skills)} skills)")
                    elif block.type == "summon_skill_ref":
                        if block.char not in char_map:
                            errors.append(f"[GUIDE:{guide.slug}] block[{b_idx}] summon_skill_ref char '{block.char}' not found")
                        else:
                            c = char_map[block.char]
                            if not c.summons or block.summon_idx >= len(c.summons):
                                errors.append(f"[GUIDE:{guide.slug}] block[{b_idx}] summon_idx {block.summon_idx} out of range for '{block.char}'")
                            else:
                                sm = c.summons[block.summon_idx]
                                if block.skill_idx >= len(sm.skills):
                                    errors.append(f"[GUIDE:{guide.slug}] block[{b_idx}] skill_idx {block.skill_idx} out of range for summon '{sm.name}'")
                    elif block.type == "image":
                        _check_asset_path(block.src, f"GUIDE:{guide.slug}:image[{b_idx}]", errors)

            except Exception as e:
                errors.append(f"[GUIDE] {path.name}: {e}")

    # 5. Cross-file relational integrity: Signature Weapon
    valid_weapon_names_or_slugs = {
        w.name.strip().lower() for w in loaded_weapons
    } | {
        w.slug.strip().lower() for w in loaded_weapons
    }

    for char in loaded_characters:
        if char.signature_weapon:
            sig_clean = char.signature_weapon.strip().lower()
            if sig_clean not in valid_weapon_names_or_slugs:
                msg = f"Character '{char.slug}' signature_weapon '{char.signature_weapon}' does not match any known weapon in weapons.json"
                if strict_signature_weapons:
                    errors.append(f"[RELATION] {msg}")
                else:
                    warnings.append(f"[RELATION WARNING] {msg}")


    print(f"\nValidated {ok} record(s) across {len(char_files)} character file(s).")
    if warnings:
        for w in warnings:
            print(f"  ⚠️  {w}")

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
