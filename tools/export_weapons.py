#!/usr/bin/env python3
"""
tools/export_weapons.py
Reads tools/weapons.xlsx, extracts embedded weapon images to image/weapons/
and exports weapon metadata to data/weapons.json.
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.validate import Weapon, validate_all

EXCEL_PATH = ROOT / "tools" / "weapons.xlsx"
IMAGE_DIR = ROOT / "image" / "weapons"
ASSETS_IMAGE_DIR = ROOT / "assets" / "images" / "weapons"
OUTPUT_JSON = ROOT / "data" / "weapons.json"

TYPE_MAP = {
    "Submachine Gun": "SMG",
    "Machine Gun": "MG",
    "Sword": "Blade",
    "Assault Rifle": "Assault Rifle",
    "Sniper Rifle": "Sniper Rifle",
    "Shotgun": "Shotgun",
    "Handgun": "Handgun",
}

RARITY_MAP = {
    "5*": "SSR",
    "4*": "SR",
    "3*": "R",
    "SSR": "SSR",
    "SR": "SR",
    "R": "R",
}


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def sanitize_filename(name: str) -> str:
    # Replace Windows illegal characters: \ / : * ? " < > |
    cleaned = re.sub(r'[\/\\:\*\?\"<>\|]', '-', name)
    # Collapse consecutive dashes/spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def extract_weapons() -> int:
    if not EXCEL_PATH.exists():
        print(f"Error: {EXCEL_PATH} not found.")
        return 1

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    print(f"Opening {EXCEL_PATH.name} and extracting images...")
    wb = openpyxl.load_workbook(str(EXCEL_PATH), data_only=True)
    ws = wb.active

    # Parse drawings XML to map row -> media path
    img_by_row = {}
    with zipfile.ZipFile(str(EXCEL_PATH), "r") as z:
        rels_xml = z.read("xl/drawings/_rels/drawing1.xml.rels")
        rels_tree = ET.fromstring(rels_xml)
        rel_map = {r.attrib.get("Id"): r.attrib.get("Target") for r in rels_tree}

        draw_xml = z.read("xl/drawings/drawing1.xml")
        draw_tree = ET.fromstring(draw_xml)

        for elem in draw_tree:
            from_el = elem.find("{*}from")
            if from_el is None:
                continue
            col = int(from_el.find("{*}col").text)
            row = int(from_el.find("{*}row").text)

            blip = elem.find(".//{*}blip")
            if blip is None:
                continue
            embed_id = blip.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            target = rel_map.get(embed_id, "")

            # col == 1 or 1 <= col < 4 is the weapon image column
            if col == 1 or (1 <= col < 4):
                excel_row = row + 1
                img_by_row[excel_row] = target.replace("../", "xl/")

        weapons_data: List[Dict[str, Any]] = []
        exported_images = 0

        # Scan all rows in worksheet
        for r in range(2, ws.max_row + 1):
            name_val = ws.cell(r, 5).value
            if not name_val or not str(name_val).strip() or str(name_val).strip() == "Name":
                continue

            raw_name = str(name_val).strip()
            rarity_val = str(ws.cell(r, 8).value).strip() if ws.cell(r, 8).value else ""
            type_val = str(ws.cell(r, 9).value).strip() if ws.cell(r, 9).value else ""
            stats_val = str(ws.cell(r, 10).value).strip() if ws.cell(r, 10).value else ""
            trait_val = str(ws.cell(r, 11).value).strip() if ws.cell(r, 11).value else ""
            effect_val = str(ws.cell(r, 14).value).strip() if ws.cell(r, 14).value else ""

            # Disambiguate duplicate name at row 567 (3* Retired MP5H1 vs row 572 4* MP5H1)
            name = raw_name
            if name == "MP5H1" and rarity_val == "3*":
                name = "Retired MP5H1"

            slug = slugify(name)
            weapon_type = TYPE_MAP.get(type_val, type_val) if type_val else None
            rarity = RARITY_MAP.get(rarity_val, rarity_val) if rarity_val else None

            # Find mapped image
            img_target = img_by_row.get(r)
            if not img_target:
                for delta in [-1, 1, -2, 2]:
                    if (r + delta) in img_by_row:
                        img_target = img_by_row[r + delta]
                        break

            image_filename = f"{sanitize_filename(name)}.png"
            image_rel_path = f"image/weapons/{image_filename}"

            if img_target:
                try:
                    img_bytes = z.read(img_target)
                    # Write to image/weapons/
                    out_img_path = IMAGE_DIR / image_filename
                    out_img_path.write_bytes(img_bytes)

                    # Also write to assets/images/weapons/
                    (ASSETS_IMAGE_DIR / image_filename).write_bytes(img_bytes)

                    exported_images += 1
                except Exception as e:
                    print(f"Warning: Failed to extract image for {name} ({img_target}): {e}")
            else:
                print(f"Warning: No image found for row {r} ({name})")

            entry: Dict[str, Any] = {
                "slug": slug,
                "name": name,
                "weapon_type": weapon_type,
                "rarity": rarity,
            }
            if stats_val:
                entry["stats"] = stats_val
            if trait_val and trait_val != "-":
                entry["trait"] = trait_val
            if effect_val and effect_val != "-":
                entry["effect"] = effect_val

            entry["images"] = {
                "weapon": image_rel_path
            }

            weapons_data.append(entry)

    print(f"Extracted {exported_images} images to {IMAGE_DIR.relative_to(ROOT)}")
    print(f"Writing {len(weapons_data)} weapons to {OUTPUT_JSON.relative_to(ROOT)}...")

    OUTPUT_JSON.write_text(json.dumps(weapons_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {OUTPUT_JSON.name} successfully.")

    # Validate output
    print("\nValidating weapons.json and all workspace data...")
    val_res = validate_all()
    return val_res


if __name__ == "__main__":
    sys.exit(extract_weapons())
