"""
tests/test_data_integrity.py
Negative tests and cross-file data integrity tests (Phase 4).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from tools.validate import (
    Character,
    Weapon,
    FaqEntry,
    _check_asset_path,
    validate_all
)


def test_extra_field_rejected_in_character():
    data = {
        "slug": "test-char",
        "name": "Test Char",
        "class": "Bulwark",
        "rarity": "Elite",
        "phase": "Physical",
        "weapon_type": "Blade",
        "unknown_extra_field": "disallowed"
    }
    with pytest.raises(ValidationError) as excinfo:
        Character.model_validate(data)
    assert "extra_forbidden" in str(excinfo.value) or "Extra inputs are not permitted" in str(excinfo.value)


def test_extra_field_rejected_in_weapon():
    data = {
        "slug": "test-weapon",
        "name": "Test Weapon",
        "weapon_type": "Blade",
        "rarity": "SSR",
        "bogus_field": 123
    }
    with pytest.raises(ValidationError) as excinfo:
        Weapon.model_validate(data)
    assert "extra_forbidden" in str(excinfo.value) or "Extra inputs are not permitted" in str(excinfo.value)


def test_slug_invalid_format_rejected():
    invalid_slugs = ["Test_Char", "test char", "test/char", "test--char", "test@", "-test"]
    for s in invalid_slugs:
        with pytest.raises(ValidationError):
            Character.model_validate({
                "slug": s,
                "name": "Valid Name",
                "class": "Bulwark",
                "rarity": "Elite",
                "phase": "Physical",
                "weapon_type": "Blade"
            })


def test_empty_name_rejected():
    with pytest.raises(ValidationError):
        Character.model_validate({
            "slug": "valid-slug",
            "name": "   ",
            "class": "Bulwark",
            "rarity": "Elite",
            "phase": "Physical",
            "weapon_type": "Blade"
        })


def test_negative_stats_rejected():
    with pytest.raises(ValidationError):
        Character.model_validate({
            "slug": "valid-slug",
            "name": "Valid Name",
            "class": "Bulwark",
            "rarity": "Elite",
            "phase": "Physical",
            "weapon_type": "Blade",
            "stats": {"hp": -100}
        })


def test_fortification_duplicate_tiers_rejected():
    tiers = [
        {"tier": 1, "skill": "s1"},
        {"tier": 1, "skill": "s2"},  # duplicate tier 1
        {"tier": 3, "skill": "s3"},
        {"tier": 4, "skill": "s4"},
        {"tier": 5, "skill": "s5"},
        {"tier": 6, "skill": "s6"},
    ]
    with pytest.raises(ValidationError) as excinfo:
        Character.model_validate({
            "slug": "valid-slug",
            "name": "Valid Name",
            "class": "Bulwark",
            "rarity": "Elite",
            "phase": "Physical",
            "weapon_type": "Blade",
            "fortification": tiers
        })
    assert "fortification must contain tiers 1 through 6 without duplicates" in str(excinfo.value)


def test_neural_helix_duplicate_nodes_rejected():
    nodes = [
        {"node": "Node A"},
        {"node": "Node A"},  # duplicate
    ]
    with pytest.raises(ValidationError) as excinfo:
        Character.model_validate({
            "slug": "valid-slug",
            "name": "Valid Name",
            "class": "Bulwark",
            "rarity": "Elite",
            "phase": "Physical",
            "weapon_type": "Blade",
            "neural_helix": nodes
        })
    assert "neural_helix contains duplicate nodes" in str(excinfo.value)


def test_weapon_rarity_invalid_rejected():
    with pytest.raises(ValidationError) as excinfo:
        Weapon.model_validate({
            "slug": "my-weapon",
            "name": "My Weapon",
            "weapon_type": "Blade",
            "rarity": "UR"  # invalid
        })
    assert "Invalid rarity" in str(excinfo.value)


def test_asset_path_traversal_rejected():
    errors = []
    _check_asset_path("assets/../../secret.txt", "test", errors)
    assert len(errors) == 1
    assert "cannot contain '..'" in errors[0]


def test_asset_path_absolute_rejected():
    errors = []
    _check_asset_path("/etc/passwd", "test", errors)
    assert len(errors) == 1
    assert "must be relative" in errors[0]


def test_asset_path_url_rejected():
    errors = []
    _check_asset_path("https://example.com/image.png", "test", errors)
    assert len(errors) == 1
    assert "cannot be an external URL" in errors[0]


def test_nonexistent_asset_path_rejected():
    errors = []
    _check_asset_path("assets/images/nonexistent_image_123456.png", "test", errors)
    assert len(errors) == 1
    assert "Asset file does not exist" in errors[0]


def test_signature_weapon_strict_validation_passes():
    # Every signature weapon is represented in the weapons database.
    res = validate_all(strict_signature_weapons=True)
    assert res == 0, "Strict signature weapon validation should pass when all signature weapons are linked"


def test_validate_all_passes_standard():
    assert validate_all(strict_signature_weapons=False) == 0
