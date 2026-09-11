#!/usr/bin/env python3
"""
tools/export_characters.py
Reads 'GFL2 Official Release Info Compilation.xlsx', enriches character data
with live online info (Dandegate API & gfl2.help), and exports formatted JSON
files to data/characters/{slug}.json conforming to the Data Entry tool and validate.py schema.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.validate import Character, validate_all

EXCEL_FILE = ROOT / "GFL2 Official Release Info Compilation.xlsx"
OUTPUT_DIR = ROOT / "data" / "characters"

VALID_CLASSES = {"Bulwark", "Vanguard", "Support", "Sentinel"}
VALID_RARITIES = {"Elite", "Standard"}
VALID_PHASES = {"Physical", "Burn", "Hydro", "Electric", "Freeze", "Corrosion", "Resonance"}
VALID_WEAPON_TYPES = {"Assault Rifle", "SMG", "Shotgun", "MG", "Sniper Rifle", "Handgun", "Blade"}
VALID_AMMO_TYPES = {"Light Ammo", "Medium Ammo", "Heavy Ammo", "Shotgun Ammo", "Melee"}
VALID_SKILL_TAGS = {"Basic Attack", "Active", "Buff", "Debuff", "Targeted", "AoE", "Passive", "Healing", "Shield"}

CHAR_KEY_ORDER = [
    "slug", "name", "class", "rarity", "phase", "weapon_type", "ammo_type",
    "signature_weapon", "stats", "skill_attribute", "weakness", "stability_gauge",
    "movement_speed", "effects_glossary", "skills", "summons", "fortification",
    "neural_helix", "keys", "images", "source_notes"
]


def clean_str(val: Any) -> str:
    if val is None:
        return ""
    return str(val).strip()


def clean_num(val: Any) -> Optional[int | float]:
    if val is None:
        return None
    try:
        f = float(val)
        return int(f) if f.is_integer() else f
    except (ValueError, TypeError):
        return None


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def compact_dict(obj: Any) -> Any:
    """Recursively remove None, empty strings, empty lists, empty dicts."""
    if isinstance(obj, list):
        out_list = [compact_dict(x) for x in obj]
        return [x for x in out_list if x is not None]
    if isinstance(obj, dict):
        out_dict = {}
        for k, v in obj.items():
            cv = compact_dict(v)
            if cv is not None and cv != "" and not (isinstance(cv, (list, dict)) and len(cv) == 0):
                out_dict[k] = cv
        return out_dict if out_dict else None
    return obj


def ordered_dict(d: dict, key_order: list[str]) -> dict:
    ordered = {}
    for k in key_order:
        if k in d:
            ordered[k] = d[k]
    for k in d:
        if k not in ordered:
            ordered[k] = d[k]
    return ordered


def fetch_online_metadata() -> dict[str, dict]:
    """Fetch live dolls metadata from Dandegate API."""
    print("Fetching live dolls metadata from Dandegate (https://api.dandegate.net/api/dolls)...")
    req = urllib.request.Request(
        "https://api.dandegate.net/api/dolls",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    meta_by_name = {}
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            dolls = payload.get("data", [])
            for d in dolls:
                d_name = d.get("name", "").strip()
                sig = d.get("weaponImprint", {}).get("name") if d.get("weaponImprint") else None
                ammo = None
                if d.get("ammoTypes"):
                    try:
                        raw_a = json.loads(d["ammoTypes"]) if isinstance(d["ammoTypes"], str) else d["ammoTypes"]
                        if raw_a and raw_a[0] in VALID_AMMO_TYPES:
                            ammo = raw_a[0]
                    except Exception:
                        pass

                raw_wt = d.get("weaponImprintType", "")
                wt_norm = {
                    "Submachine Gun": "SMG",
                    "Machine Gun": "MG",
                    "Rifle": "Sniper Rifle",
                }.get(raw_wt, raw_wt)

                entry = {
                    "name": d_name,
                    "class": d.get("class"),
                    "rarity": d.get("rarity"),
                    "phase": d.get("phase"),
                    "weapon_type": wt_norm if wt_norm in VALID_WEAPON_TYPES else None,
                    "ammo_type": ammo,
                    "signature_weapon": sig,
                    "search_tags": d.get("searchTags", [])
                }
                meta_by_name[d_name.lower()] = entry
                meta_by_name[slugify(d_name)] = entry
                for st in d.get("searchTags", []):
                    meta_by_name[st.lower()] = entry
                    meta_by_name[slugify(st)] = entry

        print(f"Successfully loaded metadata for {len(dolls)} dolls from Dandegate.")
    except Exception as e:
        print(f"Warning: Failed to fetch live metadata: {e}. Falling back to sheet extraction.")

    return meta_by_name


def parse_character_sheet(ws: Any, online_meta: dict[str, dict]) -> dict:
    rows = list(ws.iter_rows(values_only=True))

    raw_name = clean_str(rows[1][1]) if len(rows) > 1 and len(rows[1]) > 1 else ""
    if not raw_name:
        raw_name = ws.title.strip()

    slug = slugify(raw_name)

    # Online enrichment
    meta = online_meta.get(raw_name.lower()) or online_meta.get(slug) or {}

    # Official Name
    name = meta.get("name") or raw_name

    # Class
    c_class = clean_str(rows[11][1]) if len(rows) > 11 and len(rows[11]) > 1 else ""
    if meta.get("class"):
        c_class = meta["class"]
    elif c_class not in VALID_CLASSES:
        c_class = c_class.capitalize()

    # Rarity
    rarity = meta.get("rarity")
    if not rarity:
        sheet_text = " ".join([clean_str(c) for r in rows[:20] for c in r if c])
        if "4*" in sheet_text or "4-star" in sheet_text:
            rarity = "Standard"
        else:
            rarity = "Elite"
    if rarity not in VALID_RARITIES:
        rarity = "Elite"

    # Weapon Type
    weapon_type = meta.get("weapon_type")
    if not weapon_type:
        weapon_type = "Assault Rifle"
    if weapon_type not in VALID_WEAPON_TYPES:
        weapon_type = "Assault Rifle"

    # Phase
    phase = meta.get("phase")
    if not phase:
        if len(rows) > 13 and len(rows[13]) > 6:
            p_val = clean_str(rows[13][6])
            if p_val in VALID_PHASES:
                phase = p_val
    if not phase or phase not in VALID_PHASES:
        phase = "Physical"

    # Ammo Type
    ammo_type = meta.get("ammo_type")
    if not ammo_type and len(rows) > 11:
        for c_idx in [6, 8]:
            if len(rows[11]) > c_idx:
                val = clean_str(rows[11][c_idx])
                if val in VALID_AMMO_TYPES:
                    ammo_type = val
                    break

    # Stats
    hp = clean_num(rows[12][2]) if len(rows) > 12 and len(rows[12]) > 2 else None
    atk = clean_num(rows[12][3]) if len(rows) > 12 and len(rows[12]) > 3 else None
    def_ = clean_num(rows[12][4]) if len(rows) > 12 and len(rows[12]) > 4 else None
    stats = {}
    if hp is not None:
        stats["hp"] = int(hp)
    if atk is not None:
        stats["atk"] = int(atk)
    if def_ is not None:
        stats["def"] = int(def_)

    # Skill Attribute & Weakness
    skill_attr = clean_str(rows[13][6]) if len(rows) > 13 and len(rows[13]) > 6 else None
    weakness = clean_str(rows[13][8]) if len(rows) > 13 and len(rows[13]) > 8 else None

    # Stability Gauge & Movement Speed
    stab_gauge = clean_str(rows[14][0]) if len(rows) > 14 and len(rows[14]) > 0 else None
    move_speed = clean_str(rows[14][2]) if len(rows) > 14 and len(rows[14]) > 2 else None

    # Effects Glossary
    glossary = []
    if len(rows) > 15 and len(rows[15]) > 1:
        raw_effects = clean_str(rows[15][1])
        if raw_effects:
            for eff in raw_effects.split("\n\n"):
                eff = eff.strip()
                if eff and len(eff) > 3:
                    glossary.append(eff)

    # Signature weapon
    sig_weapon = meta.get("signature_weapon")

    # Locate sections: Skills, Summon Unit, Vertebrae, Neural Helix
    vert_start = None
    helix_start = None
    summon_start = None

    for r_idx, row in enumerate(rows):
        c0 = clean_str(row[0]) if len(row) > 0 else ""
        c1 = clean_str(row[1]) if len(row) > 1 else ""
        if "Vertebrae Upgrade" in [c0, c1] and any(
            "Upgrade" in clean_str(x) or "Icon" in clean_str(x)
            for x in rows[min(r_idx + 1, len(rows) - 1)][:3]
        ):
            vert_start = r_idx
        elif any(h in c0 or h in c1 for h in ["Neural Helix", "Digimind Helix"]):
            helix_start = r_idx
        elif r_idx > 25 and (c0 == "Unit Information" or c1 == "Unit Information") and not vert_start:
            summon_start = r_idx

    end_char_skills = summon_start if summon_start else (vert_start if vert_start else len(rows))

    def parse_skill_card(r_idx: int, max_r: int) -> dict:
        name_line = clean_str(rows[r_idx][1])
        parts = name_line.split("\n\n")
        skill_name = parts[0].strip()
        tags_raw = parts[1] if len(parts) > 1 else (name_line[name_line.find("(") :] if "(" in name_line else "")

        tags = []
        clean_tags = tags_raw.replace("(", "").replace(")", "").split("/")
        tag_map = {
            "basic attack": "Basic Attack",
            "active": "Active",
            "buff": "Buff",
            "debuff": "Debuff",
            "targeted": "Targeted",
            "single target": "Targeted",
            "aoe": "AoE",
            "passive": "Passive",
            "healing": "Healing",
            "shield": "Shield",
            "ultimate": "Active",
            "support": "Buff",
            "attack": "Active",
            "tile": "AoE",
            "cleanse": "Buff",
            "dispel": "Debuff",
            "ambush": "Passive",
        }
        for t in clean_tags:
            t_norm = t.strip().lower()
            if t_norm in tag_map:
                mapped = tag_map[t_norm]
                if mapped not in tags:
                    tags.append(mapped)

        if "basic attack" in tags_raw.lower() and "Basic Attack" not in tags:
            tags.append("Basic Attack")
        if "targeted" in tags_raw.lower() or "single target" in tags_raw.lower():
            if "Targeted" not in tags:
                tags.append("Targeted")

        stab_dmg = None
        cd = None
        cost = None
        desc = ""
        s_range = None
        eff_area = None
        s_ammo = None

        for k in range(r_idx + 1, min(r_idx + 25, max_r)):
            r = rows[k]
            for cell in r:
                c_s = clean_str(cell)
                if c_s in VALID_AMMO_TYPES:
                    s_ammo = c_s

            row_text = " | ".join([clean_str(c) for c in r if c])

            # Check stats row (only match actual Stat label pattern, not inside description text)
            if stab_dmg is None and re.search(r"Stability Damage:\s*[\d\.]+", row_text, re.IGNORECASE):
                m_sd = re.search(r"Stability Damage:\s*([\d\.]+)", row_text, re.IGNORECASE)
                if m_sd:
                    stab_dmg = clean_num(m_sd.group(1))
                m_cd = re.search(r"Cooldown:\s*([^\s\|]+(?:\s+turns)?)", row_text, re.IGNORECASE)
                if m_cd:
                    cd = m_cd.group(1).strip()
                m_cc = re.search(r"Confectance Cost:\s*([\d\.]+)", row_text, re.IGNORECASE)
                if m_cc:
                    cost = clean_num(m_cc.group(1))

                # Look for skill description in following rows
                if not desc:
                    for d_idx in range(k + 1, min(k + 5, max_r)):
                        d_cell = clean_str(rows[d_idx][0]) if len(rows[d_idx]) > 0 else ""
                        if not d_cell and len(rows[d_idx]) > 1:
                            d_cell = clean_str(rows[d_idx][1])
                        if d_cell and not any(
                            x in d_cell for x in ["Range", "Eff. Area", "Stability Damage:", ">", "Recommended"]
                        ):
                            desc = d_cell
                            break

            for c_i, cell in enumerate(r):
                c_s = clean_str(cell)
                if c_s == "Range" and c_i + 1 < len(r):
                    val = r[c_i + 1]
                    s_range = clean_num(val)
                elif c_s == "Eff. Area" and c_i + 1 < len(r):
                    val = r[c_i + 1]
                    eff_num = clean_num(val)
                    if eff_num is not None:
                        eff_area = str(eff_num)
                    else:
                        eff_area = clean_str(val)

        return {
            "name": skill_name,
            "tags": tags,
            "ammo_type": s_ammo,
            "stability_damage": stab_dmg,
            "cooldown": cd,
            "confectance_cost": cost,
            "range": s_range,
            "effect_area": eff_area,
            "description": desc,
        }

    # Extract character skills
    skills = []
    r_idx = 18
    while r_idx < end_char_skills:
        row = rows[r_idx]
        c1 = clean_str(row[1]) if len(row) > 1 else ""
        if "(" in c1 and any(tag in c1 for tag in ["Attack", "Active", "Passive", "Ultimate"]):
            skill_obj = parse_skill_card(r_idx, end_char_skills)
            skills.append(skill_obj)
        r_idx += 1

    # Extract Summons if summon_start exists
    summons = []
    if summon_start:
        s_end = vert_start if vert_start else len(rows)
        s_name = ""
        s_hp, s_atk, s_def = None, None, None
        s_stab = None
        s_move = None

        for k in range(summon_start, min(summon_start + 15, s_end)):
            r = rows[k]
            if len(r) > 4 and clean_num(r[2]) is not None and clean_num(r[3]) is not None:
                s_hp = clean_num(r[2])
                s_atk = clean_num(r[3])
                s_def = clean_num(r[4])
            row_text = " ".join([clean_str(c) for c in r if c])
            if "Stability Gauge" in row_text:
                s_stab = clean_str(r[0]) if clean_str(r[0]) and "Stability" not in clean_str(r[0]) else None
            if "Movement Speed" in row_text:
                s_move = (
                    clean_str(r[2])
                    if len(r) > 2 and clean_str(r[2]) and "Movement" not in clean_str(r[2])
                    else None
                )
            if len(r) > 1 and ":" in clean_str(r[1]) and not s_name:
                s_name = clean_str(r[1]).split(":")[0].strip()

        if not s_name:
            s_name = f"{name}'s Summon"

        s_skills = []
        k = summon_start + 5
        while k < s_end:
            c1 = clean_str(rows[k][1]) if len(rows[k]) > 1 else ""
            if "(" in c1 and any(tag in c1 for tag in ["Attack", "Active", "Passive", "Ultimate"]):
                s_card = parse_skill_card(k, s_end)
                s_skills.append({
                    "name": s_card["name"],
                    "description": s_card["description"],
                })
            k += 1

        s_stats = None
        if s_hp is not None or s_atk is not None or s_def is not None:
            s_stats = {}
            if s_hp is not None:
                s_stats["hp"] = int(s_hp)
            if s_atk is not None:
                s_stats["atk"] = int(s_atk)
            if s_def is not None:
                s_stats["def"] = int(s_def)

        summons.append({
            "name": s_name,
            "stats": s_stats,
            "stability_gauge": s_stab,
            "movement_speed": s_move,
            "skills": s_skills,
        })

    # Parse Vertebrae Upgrade (Fortification)
    fortification = []
    if vert_start:
        header_idx = vert_start + 1
        for k in range(header_idx + 1, header_idx + 7):
            if k < len(rows):
                r = rows[k]
                tier = len(fortification) + 1
                sk_name = clean_str(r[2]) if len(r) > 2 else ""
                lvl = clean_num(r[4]) if len(r) > 4 else None
                eff = clean_str(r[5]) if len(r) > 5 else ""
                fortification.append({
                    "tier": tier,
                    "skill": sk_name,
                    "level": int(lvl) if lvl is not None else None,
                    "effect": eff,
                })

    # Parse Neural Helix & Keys
    neural_helix = []
    keys = []
    if helix_start:
        header_idx = helix_start + 1
        # Enhancements 1 to 6
        for k in range(header_idx + 1, header_idx + 7):
            if k < len(rows):
                r = rows[k]
                node_name = clean_str(r[1]) if len(r) > 1 and clean_str(r[1]) else f"Enhancement {len(neural_helix)+1}"
                lvl = clean_num(r[2]) if len(r) > 2 else None
                eff = clean_str(r[3]) if len(r) > 3 else ""
                mats = clean_str(r[8]) if len(r) > 8 else (clean_str(r[-1]) if r else "")
                neural_helix.append({
                    "node": node_name,
                    "level": int(lvl) if lvl is not None else None,
                    "effect": eff,
                    "materials": mats if mats else None,
                })

        # Keys (from header_idx + 7 onwards)
        for k in range(header_idx + 7, min(header_idx + 18, len(rows))):
            r = rows[k]
            k_name = clean_str(r[1]) if len(r) > 1 else ""
            if any(kp in k_name for kp in ["Fixed Key", "Affinity Key", "Common Key", "Expansion Key"]):
                lvl_raw = r[2] if len(r) > 2 else ""
                lvl_val = clean_num(lvl_raw)
                if lvl_val is not None:
                    k_lvl: Any = int(lvl_val)
                else:
                    k_lvl = clean_str(lvl_raw) if clean_str(lvl_raw) else ""
                eff = clean_str(r[3]) if len(r) > 3 else ""
                mats = clean_str(r[8]) if len(r) > 8 else (clean_str(r[-1]) if r else "")
                keys.append({
                    "name": k_name,
                    "level": k_lvl if k_lvl != "" else None,
                    "effect": eff,
                    "materials": mats if mats else None,
                })

    # Images
    images = {
        "portrait": f"assets/images/characters/{slug}/portrait.png",
        "class_icon": f"assets/images/class/{c_class}.png",
    }

    char_dict = {
        "slug": slug,
        "name": name,
        "class": c_class,
        "rarity": rarity,
        "phase": phase,
        "weapon_type": weapon_type,
        "ammo_type": ammo_type,
        "signature_weapon": sig_weapon,
        "stats": stats if stats else None,
        "skill_attribute": skill_attr,
        "weakness": weakness,
        "stability_gauge": stab_gauge,
        "movement_speed": move_speed,
        "effects_glossary": glossary,
        "skills": skills,
        "fortification": fortification,
        "neural_helix": neural_helix,
        "keys": keys,
        "images": images,
        "source_notes": "Extracted from GFL2 Official Release Info Compilation.xlsx with online Dandegate/gfl2.help enrichment.",
    }
    if summons:
        char_dict["summons"] = summons

    return char_dict


def export_all() -> int:
    if not EXCEL_FILE.exists():
        print(f"Error: Excel file not found: {EXCEL_FILE}")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    online_meta = fetch_online_metadata()

    print(f"Opening Excel workbook: {EXCEL_FILE.name}...")
    wb = openpyxl.load_workbook(str(EXCEL_FILE), read_only=True, data_only=True)
    sheet_names = wb.sheetnames
    print(f"Found {len(sheet_names)} character sheets.")

    exported_count = 0
    errors = []

    for idx, s_name in enumerate(sheet_names, 1):
        ws = wb[s_name]
        try:
            char_data = parse_character_sheet(ws, online_meta)
            # Validate schema
            Character.model_validate(char_data)

            # Compact & sort keys
            compact_data = compact_dict(char_data)
            ordered_data = ordered_dict(compact_data, CHAR_KEY_ORDER)

            slug = ordered_data.get("slug") or slugify(s_name)
            out_file = OUTPUT_DIR / f"{slug}.json"
            out_file.write_text(json.dumps(ordered_data, indent=2, ensure_ascii=False), encoding="utf-8")
            exported_count += 1
            print(f"[{idx:02d}/{len(sheet_names)}] Exported: {ordered_data['name']} -> {out_file.name}")
        except Exception as e:
            errors.append(f"Sheet '{s_name}': {e}")
            print(f"[{idx:02d}/{len(sheet_names)}] ERROR in {s_name}: {e}")

    print(f"\nCompleted export: {exported_count}/{len(sheet_names)} characters written.")
    if errors:
        print(f"Encountered {len(errors)} errors:")
        for err in errors:
            print(f"  - {err}")

    # Run overall validation
    print("\nRunning overall validation...")
    val_res = validate_all()
    return val_res


if __name__ == "__main__":
    sys.exit(export_all())
