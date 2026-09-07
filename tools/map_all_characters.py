#!/usr/bin/env python3
"""
tools/map_all_characters.py
Maps all character images (skills, summons, keys, avatars, and card portraits)
from assets/images/raw/ and Dandegate API into assets/images/characters/<slug>/
and updates data/characters/<slug>.json for all 64 dolls.
"""

import glob
import json
import os
import re
import shutil
import urllib.request
from pathlib import Path
from PIL import Image
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "characters"
RAW_DIR = ROOT / "assets" / "images" / "raw"
CHAR_DIR = ROOT / "assets" / "images" / "characters"
EXCEL_PATH = ROOT / "GFL2 Official Release Info Compilation.xlsx"

EIGHT_PRE_EXTRACTED = {
    "alva", "andoris", "balthilde", "basti", "belka", "centaureissi", "cheeta", "groza"
}

def clean_str(val):
    if val is None:
        return ""
    return str(val).strip()

def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def main():
    print("Loading Dandegate dolls API...")
    req = urllib.request.Request(
        "https://api.dandegate.net/api/dolls",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        dandegate_data = json.loads(resp.read().decode("utf-8"))
    dandegate_dolls = {}
    for d in dandegate_data.get("data", []):
        d_name = d.get("name", "")
        clean_n = d_name.lower().replace(" ", "_").replace("-", "_")
        dandegate_dolls[clean_n] = d
        dandegate_dolls[slugify(d_name).replace("-", "_")] = d
        for st in d.get("searchTags", []):
            dandegate_dolls[st.lower().replace(" ", "_").replace("-", "_")] = d

    print(f"Loaded metadata for {len(dandegate_data.get('data', []))} dolls from Dandegate.")

    print(f"Loading Excel workbook {EXCEL_PATH.name}...")
    wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True)
    clean_sheets = {}
    for s in wb.sheetnames:
        cs = s.strip().lower().replace(" ", "_").replace("-", "_")
        clean_sheets[cs] = s

    raw_folders = set(os.listdir(RAW_DIR))

    json_files = sorted(DATA_DIR.glob("*.json"))
    print(f"Found {len(json_files)} character JSON files to process.\n")

    for json_path in json_files:
        slug = json_path.stem
        with open(json_path, "r", encoding="utf-8") as f:
            char_data = json.load(f)

        name = char_data.get("name", slug)
        clean_slug = slug.lower().replace("-", "_")
        clean_name = name.lower().replace(" ", "_").replace("-", "_")

        dest_dir = CHAR_DIR / slug
        dest_dir.mkdir(parents=True, exist_ok=True)

        print(f"[{slug}] Processing: {name}")

        # ── 1. Dandegate Card Portrait & Avatar ──
        dg = dandegate_dolls.get(clean_slug) or dandegate_dolls.get(clean_name)
        card_url = None
        avatar_url = None
        if dg:
            card_url = next((img["imageUrl"] for img in dg.get("dollImages", []) if img.get("category") == "Card"), None)
            avatar_url = dg.get("avatarUrl")

        # Avatar Handling
        avatar_file = dest_dir / "avatar.png"
        raw_char_dir = None
        for rf in raw_folders:
            if (rf == slug or rf == clean_slug or rf == clean_name or
                rf.replace("_", "-") == slug or rf.replace("-", "_") == clean_slug or
                rf.replace("_", "").replace("-", "") == clean_slug.replace("_", "")):
                raw_char_dir = RAW_DIR / rf
                break

        # Check existing avatar or 2_1.png
        if not avatar_file.exists():
            if raw_char_dir and (raw_char_dir / "2_1.png").exists():
                shutil.copy2(raw_char_dir / "2_1.png", avatar_file)
            elif (dest_dir / "portrait.png").exists():
                try:
                    im = Image.open(dest_dir / "portrait.png")
                    if im.size == (512, 512):
                        im.save(avatar_file)
                except Exception:
                    pass
            if not avatar_file.exists() and avatar_url:
                try:
                    av_req = urllib.request.Request(avatar_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(av_req, timeout=15) as av_resp:
                        av_bytes = av_resp.read()
                    tmp_av = dest_dir / "tmp_av.webp"
                    tmp_av.write_bytes(av_bytes)
                    Image.open(tmp_av).save(avatar_file)
                    if tmp_av.exists():
                        tmp_av.unlink()
                except Exception as e:
                    print(f"  Warning: failed to fetch avatar from Dandegate for {slug}: {e}")

        # Card Portrait Handling
        card_webp = dest_dir / "portrait.webp"
        card_png = dest_dir / "portrait.png"
        
        # We want true Card portrait
        # Check if portrait.png is currently a 512x512 avatar headshot
        need_card_download = True
        if card_webp.exists() and card_webp.stat().st_size > 10000:
            try:
                im = Image.open(card_webp)
                if im.size[1] > im.size[0] * 1.3:  # vertical card
                    im.save(card_png)
                    need_card_download = False
            except Exception:
                pass

        if need_card_download and card_url:
            try:
                c_req = urllib.request.Request(card_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(c_req, timeout=15) as c_resp:
                    c_bytes = c_resp.read()
                card_webp.write_bytes(c_bytes)
                im = Image.open(card_webp)
                im.save(card_png)
                print(f"  Saved Card portrait ({im.size}) -> portrait.png & portrait.webp")
            except Exception as e:
                print(f"  Warning: failed to fetch Card portrait for {slug}: {e}")

        # Update char_data images
        c_class = char_data.get("class", "bulwark").lower()
        char_data["images"] = {
            "portrait": f"assets/images/characters/{slug}/portrait.png",
            "avatar": f"assets/images/characters/{slug}/avatar.png",
            "class_icon": f"assets/images/class/{c_class}.png"
        }

        # ── 2. Skills, Summons, and Keys ──
        if slug in EIGHT_PRE_EXTRACTED:
            # Map pre-extracted files already in dest_dir
            existing_files = set(os.listdir(dest_dir))
            
            # Skills
            skills = char_data.get("skills", [])
            for i, sk in enumerate(skills):
                if i == 3:
                    icon = "ult-icon.png"
                    rng = "ult-range.png"
                elif i == 4:
                    icon = "passive.png" if "passive.png" in existing_files else "passive-icon.png"
                    rng = "passive-range.png" if "passive-range.png" in existing_files else ("passive-rangre.png" if "passive-rangre.png" in existing_files else None)
                else:
                    icon = f"skill{i+1}-icon.png"
                    rng = f"skill{i+1}-range.png"
                
                if icon in existing_files:
                    sk["icon"] = f"assets/images/characters/{slug}/{icon}"
                if rng and rng in existing_files:
                    sk["range_image"] = f"assets/images/characters/{slug}/{rng}"

            # Summons
            if char_data.get("summons"):
                for s_idx, summon in enumerate(char_data["summons"]):
                    if f"summon{s_idx+1}.png" in existing_files:
                        summon["image"] = f"assets/images/characters/{slug}/summon{s_idx+1}.png"
                    for j, s_sk in enumerate(summon.get("skills", [])):
                        # Look for candidate names
                        c_icons = [
                            f"summon{s_idx+1}-skill{j+1}-icon.png",
                            f"summon{s_idx+1}-passive{j}-icon.png",
                            f"summon{s_idx+1}-passive{j+1}-icon.png",
                            f"summon2-skill{j+1}-icon.png"
                        ]
                        for c_i in c_icons:
                            if c_i in existing_files:
                                s_sk["icon"] = f"assets/images/characters/{slug}/{c_i}"
                                rng_cand = c_i.replace("-icon.png", "-range.png")
                                if rng_cand in existing_files:
                                    s_sk["range_image"] = f"assets/images/characters/{slug}/{rng_cand}"
                                break

            # Keys
            for k in char_data.get("keys", []):
                k_name = k.get("name", "")
                if "Fixed Key" in k_name:
                    m = re.search(r"Fixed Key\s*(\d+)", k_name)
                    num = m.group(1) if m else "1"
                    if f"fixed ({num}).png" in existing_files:
                        k["image"] = f"assets/images/characters/{slug}/fixed ({num}).png"
                elif "Affinity Key" in k_name and "affi.png" in existing_files:
                    k["image"] = f"assets/images/characters/{slug}/affi.png"
                elif "Common Key" in k_name and "common.png" in existing_files:
                    k["image"] = f"assets/images/characters/{slug}/common.png"
                elif "Expansion Key tier 2" in k_name and "expan2.png" in existing_files:
                    k["image"] = f"assets/images/characters/{slug}/expan2.png"
                elif "Expansion Key" in k_name and "expan.png" in existing_files:
                    k["image"] = f"assets/images/characters/{slug}/expan.png"

        else:
            # Extract from Excel & raw_char_dir
            if not raw_char_dir or not raw_char_dir.exists():
                print(f"  Error: raw folder not found for {slug}!")
                continue

            raw_files = set(os.listdir(raw_char_dir))

            sheet_title = clean_sheets.get(clean_slug) or clean_sheets.get(clean_name)
            if not sheet_title:
                for cs, orig in clean_sheets.items():
                    if cs in clean_slug or clean_slug in cs:
                        sheet_title = orig
                        break

            if not sheet_title:
                print(f"  Error: Excel sheet not found for {slug}!")
                continue

            ws = wb[sheet_title]
            rows = list(ws.iter_rows(values_only=True))

            # Detect boundaries
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

            # Find character skill rows in Excel
            skill_cards = []
            for k in range(18, end_char_skills):
                c1 = clean_str(rows[k][1]) if len(rows[k]) > 1 else ""
                if "(" in c1 and any(tag in c1 for tag in ["Attack", "Active", "Passive", "Ultimate"]):
                    name_part = c1.split("\n")[0].split("(")[0].strip()
                    skill_cards.append((k + 1, name_part, c1))  # 1-indexed

            # Map skills
            for i, sk in enumerate(char_data.get("skills", [])):
                sk_name = sk.get("name", "")
                matched_row = None
                for r_num, np, full in skill_cards:
                    if sk_name.lower() in np.lower() or np.lower() in sk_name.lower():
                        matched_row = r_num
                        break
                if not matched_row and i < len(skill_cards):
                    matched_row = skill_cards[i][0]

                if matched_row:
                    if i == 3:
                        icon_dst = "ult-icon.png"
                        rng_dst = "ult-range.png"
                    elif i == 4:
                        icon_dst = "passive.png"
                        rng_dst = "passive-range.png"
                    else:
                        icon_dst = f"skill{i+1}-icon.png"
                        rng_dst = f"skill{i+1}-range.png"

                    # Copy Icon
                    src_icon = f"{matched_row}_1.png"
                    if src_icon in raw_files:
                        shutil.copy2(raw_char_dir / src_icon, dest_dir / icon_dst)
                        sk["icon"] = f"assets/images/characters/{slug}/{icon_dst}"

                    # Copy Range
                    for delta in range(0, 13):
                        candidate = f"{matched_row + delta}_8.png"
                        if candidate in raw_files:
                            shutil.copy2(raw_char_dir / candidate, dest_dir / rng_dst)
                            sk["range_image"] = f"assets/images/characters/{slug}/{rng_dst}"
                            break

            # Map Summons
            if char_data.get("summons"):
                s_start = 135
                s_end = vert_start if vert_start else len(rows)
                for s_idx, summon in enumerate(char_data["summons"]):
                    s_name = summon.get("name", "")
                    # find unit row
                    unit_row = None
                    for k in range(s_start, s_end):
                        c1 = clean_str(rows[k][1]) if len(rows[k]) > 1 else ""
                        if s_name.lower() in c1.lower() and "(" not in c1 and len(c1) < 40:
                            unit_row = k + 1
                            break
                    if unit_row and f"{unit_row}_1.png" in raw_files:
                        shutil.copy2(raw_char_dir / f"{unit_row}_1.png", dest_dir / f"summon{s_idx+1}.png")
                        summon["image"] = f"assets/images/characters/{slug}/summon{s_idx+1}.png"

                    # Summon skills
                    s_skill_cards = []
                    for k in range(s_start, s_end):
                        c1 = clean_str(rows[k][1]) if len(rows[k]) > 1 else ""
                        if "(" in c1 and any(tag in c1 for tag in ["Attack", "Active", "Passive", "Ultimate"]):
                            name_part = c1.split("\n")[0].split("(")[0].strip()
                            s_skill_cards.append((k + 1, name_part, c1))

                    for j, s_sk in enumerate(summon.get("skills", [])):
                        sk_name = s_sk.get("name", "")
                        matched_s_row = None
                        for r_num, np, full in s_skill_cards:
                            if sk_name.lower() in np.lower() or np.lower() in sk_name.lower():
                                matched_s_row = r_num
                                break
                        if not matched_s_row and j < len(s_skill_cards):
                            matched_s_row = s_skill_cards[j][0]

                        if matched_s_row:
                            is_passive = "Passive" in s_skill_cards[j][2] if j < len(s_skill_cards) else False
                            prefix = f"summon{s_idx+1}-passive{j}" if (is_passive and j > 0) else f"summon{s_idx+1}-skill{j+1}"
                            s_icon_dst = f"{prefix}-icon.png"
                            s_rng_dst = f"{prefix}-range.png"

                            src_icon = f"{matched_s_row}_1.png"
                            if src_icon in raw_files:
                                shutil.copy2(raw_char_dir / src_icon, dest_dir / s_icon_dst)
                                s_sk["icon"] = f"assets/images/characters/{slug}/{s_icon_dst}"

                            for delta in range(0, 13):
                                candidate = f"{matched_s_row + delta}_8.png"
                                if candidate in raw_files:
                                    shutil.copy2(raw_char_dir / candidate, dest_dir / s_rng_dst)
                                    s_sk["range_image"] = f"assets/images/characters/{slug}/{s_rng_dst}"
                                    break

            # Map Keys
            if char_data.get("keys"):
                search_start = helix_start + 6 if helix_start else (vert_start + 8 if vert_start else 150)
                key_cards = []
                for k in range(search_start, min(search_start + 25, len(rows))):
                    c1 = clean_str(rows[k][1]) if len(rows[k]) > 1 else ""
                    if any(kp in c1 for kp in ["Fixed Key", "Affinity Key", "Common Key", "Expansion Key"]):
                        key_cards.append((k + 1, c1))

                for key in char_data["keys"]:
                    k_name = key.get("name", "")
                    matched_k_row = None
                    for r_num, full in key_cards:
                        if k_name.lower() in full.lower() or full.lower() in k_name.lower():
                            matched_k_row = r_num
                            break
                        prefix = k_name.split(" - ")[0].strip().lower()
                        if prefix in full.lower():
                            matched_k_row = r_num
                            break

                    if matched_k_row and f"{matched_k_row}_1.png" in raw_files:
                        if "Fixed Key" in k_name:
                            m = re.search(r"Fixed Key\s*(\d+)", k_name)
                            num = m.group(1) if m else "1"
                            dst_name = f"fixed ({num}).png"
                        elif "Affinity Key" in k_name:
                            dst_name = "affi.png"
                        elif "Common Key" in k_name:
                            dst_name = "common.png"
                        elif "Expansion Key tier 2" in k_name:
                            dst_name = "expan2.png"
                        elif "Expansion Key" in k_name:
                            dst_name = "expan.png"
                        else:
                            dst_name = f"key_{matched_k_row}.png"

                        shutil.copy2(raw_char_dir / f"{matched_k_row}_1.png", dest_dir / dst_name)
                        key["image"] = f"assets/images/characters/{slug}/{dst_name}"

        # Write back updated JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(char_data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    print("\nAll 64 characters successfully mapped!")

if __name__ == "__main__":
    main()
