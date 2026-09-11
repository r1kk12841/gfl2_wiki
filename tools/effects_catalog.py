from __future__ import annotations

import copy
import hashlib
from typing import Any


def effect_id(name_en: str) -> str:
    """Return a stable, name-independent-at-runtime identifier for an English effect."""
    digest = hashlib.sha1(name_en.strip().encode("utf-8")).hexdigest()[:12]
    return f"effect_{digest}"


def canonicalize_effects(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Read legacy name-keyed or v2 ID-keyed data and return the v2 ID map."""
    unique_by_en: dict[str, dict[str, Any]] = {}
    for key, raw in data.items():
        if not isinstance(raw, dict):
            continue
        name_en = raw.get("name_en")
        if not isinstance(name_en, str) or not name_en.strip():
            continue
        entry = copy.deepcopy(raw)
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id.startswith("effect_"):
            entry_id = key if key.startswith("effect_") else effect_id(name_en)
        entry["id"] = entry_id
        unique_by_en.setdefault(name_en, entry)

    id_by_en = {name_en: entry["id"] for name_en, entry in unique_by_en.items()}
    result: dict[str, dict[str, Any]] = {}
    for name_en, entry in unique_by_en.items():
        sub_ids = entry.get("sub_effect_ids")
        if not isinstance(sub_ids, list):
            sub_ids = [id_by_en[name] for name in entry.get("sub_effects", []) if name in id_by_en]
        normalized = {
            "id": entry["id"],
            "name": str(entry.get("name", name_en)),
            "name_en": name_en,
            "desc": str(entry.get("desc", entry.get("desc_en", ""))),
            "desc_en": str(entry.get("desc_en", entry.get("desc", ""))),
            "type": str(entry.get("type", "effect")),
            "sub_effect_ids": [item for item in sub_ids if item in {e["id"] for e in unique_by_en.values()}],
        }
        result[normalized["id"]] = normalized
    return result


def build_name_index(effects: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    """Build a collision-safe secondary index; duplicate names keep every matching ID."""
    index: dict[str, list[str]] = {}
    for effect_key, entry in effects.items():
        for field in ("name_en", "name"):
            name = str(entry.get(field, "")).strip()
            if not name:
                continue
            bucket = index.setdefault(name.casefold(), [])
            if effect_key not in bucket:
                bucket.append(effect_key)
    return index


def browser_catalog(effects: dict[str, dict[str, Any]]) -> dict[str, Any]:
    canonical = canonicalize_effects(effects)
    return {"schemaVersion": 2, "byId": canonical, "nameIndex": build_name_index(canonical)}
