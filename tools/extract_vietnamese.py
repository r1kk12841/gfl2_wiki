#!/usr/bin/env python3
"""
tools/extract_vietnamese.py
Scans assets/LangPackageTableVtviData_decoded.json, extracts Vietnamese
localization for all characters, weapons, stats, terminology, and UI labels,
and exports:
  - data/i18n_vi.json (Canonical translation dataset)
  - site/static/js/i18n-vi.js (Client-side translation database)
"""

from __future__ import annotations

import html
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
LANG_FILE = ROOT / "assets" / "LangPackageTableVtviData_decoded.json"
DATA_DIR = ROOT / "data"
CHAR_DIR = DATA_DIR / "characters"
WEAPONS_FILE = DATA_DIR / "weapons.json"
OUTPUT_JSON = DATA_DIR / "i18n_vi.json"
OUTPUT_JS = ROOT / "site" / "static" / "js" / "i18n-vi.js"

# UI and terminology dictionary
UI_DICTIONARY = {
    "nav_home": "Trang Chủ",
    "nav_dolls": "Nhân Vật",
    "nav_weapons": "Vũ Khí",
    "nav_faq": "Hỏi Đáp",
    "brand_sub": "EXILIUM",
    "search_placeholder": "Tìm kiếm nhân vật, vũ khí…",
    "footer_title": "Girls' Frontline 2: Exilium Wiki — Tham khảo dữ liệu cộng đồng.",
    "footer_desc": "Dữ liệu do cộng đồng GFL2 tổng hợp. Tên trò chơi, nhãn hiệu và tài sản trò chơi thuộc về các chủ thể quyền tương ứng.",
    "footer_dolls": "Nhân Vật Tác Chiến",
    "footer_weapons": "Kho Vũ Khí",
    "footer_faq": "Hỏi Đáp",

    # Hero & Home
    "hero_tag": "CƠ SỞ DỮ LIỆU TÁC CHIẾN",
    "hero_desc": "Cơ sở dữ liệu tình báo tác chiến đầy đủ bao gồm Tactical Dolls, thông số Kho Vũ Khí, Cường Hóa Tâm Trí, Mạch Tâm Trí và cơ chế hiệu ứng.",
    "hero_stat_dolls": "Nhân Vật Tác Chiến",
    "hero_stat_weapons": "Vũ Khí",
    "hero_stat_classes": "Lớp Tác Chiến",
    "hero_stat_phases": "Thuộc Tính Nguyên Tố",
    "home_classes_title": "Lớp Tác Chiến",
    "home_featured_title": "Nhân Vật Tiêu Biểu",
    "home_view_all_dolls": "Xem Tất Cả Nhân Vật →",

    # Filter labels
    "label_class": "Lớp",
    "label_rarity": "Độ Hiếm",
    "label_phase": "Thuộc Tính",
    "label_weapon": "Vũ Khí",
    "label_weapon_type": "Loại Vũ Khí",
    "label_server": "Máy Chủ",
    "filter_all_classes": "Tất Cả Lớp",
    "filter_all_rarities": "Tất Cả Độ Hiếm",
    "filter_all_phases": "Tất Cả Thuộc Tính",
    "filter_all_weapons": "Tất Cả Vũ Khí",
    "filter_all_ammo_types": "Tất Cả Loại Đạn",
    "filter_all_types": "Tất Cả Loại",
    "filter_all_servers": "Tất Cả Máy Chủ",
    "filter_count_suffix": "nhân vật",
    "weapon_filter_count_suffix": "vũ khí",
    "dolls_page_title": "Nhân Vật Tác Chiến",
    "dolls_page_subtitle": "Tra cứu và lọc danh sách Tactical Doll tác chiến.",
    "weapons_page_title": "Kho Vũ Khí",
    "weapons_page_subtitle": "Duyệt và phân tích vũ khí tác chiến, đặc tính và hiệu ứng khắc ấn.",
    "label_trait_prefix": "Đặc Tính:",
    "helix_stats_subtitle": "Tăng Cường Chỉ Số",

    # Breadcrumbs & Headings
    "breadcrumb_home": "Trang Chủ",
    "breadcrumb_dolls": "Nhân Vật Tác Chiến",
    "breadcrumb_weapons": "Kho Vũ Khí",
    "base_stats_label": "Chỉ Số Cơ Bản (Lv. 60)",
    "sig_for_label": "Vũ Khí Đặc Trưng Cho:",
    "weapon_trait_title": "Đặc Tính Vũ Khí",
    "weapon_effect_title": "Hiệu Ứng Khắc Ấn / Bị Động",
    "skills_section_title": "Kỹ Năng & Năng Lực Tác Chiến",
    "fortifications_section_title": "Cường Hóa Tâm Trí",
    "neural_helix_section_title": "Mạch Tâm Trí",
    "keys_section_title": "Chìa Khóa Tâm Trí",
    "summons_section_title": "Vật Thể Triệu Hồi",

    # Character Stats Grid Labels
    "stat_hp": "HP",
    "stat_atk": "Tấn Công",
    "stat_def": "Phòng Thủ",
    "stat_stability": "Độ Ổn Định",
    "stat_mobility": "Di Chuyển",
    "stat_weakness": "Điểm Yếu",
    "stat_weapon_type": "Loại Vũ Khí",
    "stat_ammo_type": "Loại Đạn",
    "stat_signature_weapon": "Vũ Khí Đặc Trưng",

    # Skill labels
    "skill_cd": "Hồi chiêu:",
    "skill_cost": "Nhiên liệu:",
    "skill_range": "Tầm bắn:",
    "skill_area": "Phạm vi:",
    "skill_stab_dmg": "ST Ổn Định:",

    # Tag translations
    "tags": {
        "Basic Attack": "Đánh Thường",
        "Skill": "Chủ Động",
        "Ultimate": "Quyết Thắng",
        "Active": "Chủ Động",
        "Passive": "Bị Động",
        "Buff": "Cường Hóa",
        "Debuff": "Suy Yếu",
        "Targeted": "Chỉ Định",
        "AoE": "Phạm Vi",
        "Healing": "Trị Liệu",
        "Shield": "Tạo Khiên",
        "Summon": "Triệu Hồi",
        "Mobility": "Chuyển Vị",
        "Melee": "Cận Chiến",
        "Support": "Chi Viện"
    },

    # Classes
    "classes": {
        "Bulwark": "Hộ Vệ",
        "Vanguard": "Tiên Phong",
        "Support": "Hỗ Trợ",
        "Sentinel": "Vệ Binh"
    },

    # Phases / Elements
    "phases": {
        "Physical": "Vật Lý",
        "Burn": "Thiêu Đốt",
        "Hydro": "Hóa Lỏng",
        "Electric": "Dẫn Điện",
        "Freeze": "Băng Kết",
        "Corrosion": "Ăn Mòn",
        "Resonance": "Cộng Hưởng"
    },

    # Weapon Types
    "weapon_types": {
        "Assault Rifle": "Súng Trường",
        "SMG": "Súng Tiểu Liên",
        "Shotgun": "Súng Shotgun",
        "MG": "Súng Máy",
        "Sniper Rifle": "Súng Bắn Tỉa",
        "Handgun": "Súng Lục",
        "Blade": "Lưỡi Đao"
    },

    # Ammo Types
    "ammo_types": {
        "Light Ammo": "Đạn Nhẹ",
        "Medium Ammo": "Đạn Vừa",
        "Heavy Ammo": "Đạn Nặng",
        "Shotgun Ammo": "Súng Shotgun",
        "Melee": "Cận Chiến"
    },

    # Rarities
    "rarities": {
        "Elite": "Tinh Nhuệ",
        "Standard": "Tiêu Chuẩn",
        "SSR": "SSR",
        "SR": "SR",
        "R": "R"
    },
    "rarities_filter": {
        "Elite": "Tinh Nhuệ (SSR)",
        "Standard": "Tiêu Chuẩn (SR)",
        "SSR": "SSR",
        "SR": "SR",
        "R": "R"
    },
    "servers": {
        "cn": "Trung Quốc",
        "global": "Quốc Tế"
    }
}

ELEMENT_MAP = {
    "Physical": "Vật Lý",
    "Hydro": "Hóa Lỏng",
    "Freeze": "Băng Kết",
    "Electric": "Dẫn Điện",
    "Burn": "Thiêu Đốt",
    "Corrosion": "Ăn Mòn",
    "Resonance": "Cộng Hưởng"
}

# Known weapon name mappings (English -> Vietnamese)
WEAPON_NAME_MAP = {
    "Compass of Repentance": "La Bàn Sám Hối",
    "Guerno": "Guerno",
    "Aglaea": "Aglaea",
    "OTs-14": "OTs-14",
    "Arcana": "Arcana",
    "Mjölnir": "Mjölnir",
    "Svarog": "Svarog",
    "Section 200": "Triệt Đoạn 200",
    "OHWS XXIII": "OHWS XXIII",
    "Styler SMG": "Styler SMG",
    "Sportivo Calibro 12": "Sportivo Calibro 12",
    "Three-Line Rifle M1891": "Three-Line Rifle M1891",
    "Kalashnikova-15": "Kalashnikova-15",
    "Model ARM": "Model ARM",
    "Model 100": "Model 100",
    "Manuscript": "Manuscript",
    "Lewis Gun": "Súng Lewis",
}


def clean_markup(text: str) -> str:
    """Strip Unity markup tags like <color=...> or <size=...> for raw comparison."""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


def translate_stat_expression(text: str) -> str:
    """Translate standard character & neural helix stat strings."""
    if not text:
        return ""
    res = text
    res = re.sub(r"\bATK\b", "Tấn Công", res)
    res = re.sub(r"\bDEF\b", "Phòng Thủ", res)
    res = re.sub(r"\bCRIT DMG\b", "ST Bạo Kích", res)
    res = re.sub(r"\bCRIT Rate\b", "TL Bạo Kích", res)
    res = re.sub(r"\bCRIT\b", "TL Bạo Kích", res)
    res = re.sub(r"\bStability\b", "Độ Ổn Định", res)
    res = re.sub(r"\bMobility\b", "Di Chuyển", res)
    res = re.sub(r"\bEnhancement\s+(\d+)\b", r"Cường Hóa \1", res)
    return res


def translate_weapon_stats(stats_en: str) -> str:
    if not stats_en:
        return ""
    text = stats_en
    replacements = [
        ("Attack Boost", "Tăng Tấn Công"),
        ("Attack", "Tấn Công"),
        ("CRIT DMG", "ST Bạo Kích"),
        ("CRIT Rate", "TL Bạo Kích"),
        ("Defense Boost", "Tăng Phòng Thủ"),
        ("Defense", "Phòng Thủ"),
        ("HP Boost", "Tăng HP"),
        ("HP", "HP"),
    ]
    for en, vi in replacements:
        text = re.sub(rf"\b{re.escape(en)}\b", vi, text)
    return text


def translate_key_fallback(text: str) -> str:
    """Fallback translation for Key effects."""
    if not text:
        return ""
    res = text
    replacements = [
        (r"When additional points of Confectance Index is consumed, increases CRIT DMG dealt by (\d+%)", r"Khi tiêu hao thêm Chỉ Số Nhiên Liệu, ST Bạo Kích gây ra tăng \1"),
        (r"When this effect is triggered, restores HP equivalent to (\d+%) max HP", r"Sau khi kích hoạt hiệu ứng này, hồi phục HP bằng \1 HP tối đa"),
        (r"Before skill usage, dispels (\d+) random buff from the target", r"Trước khi dùng kỹ năng, giải trừ \1 Buff ngẫu nhiên trên người mục tiêu"),
        (r"Before an active attack, cleanse (\d+) buff from the target", r"Trước khi tấn công chủ động, giải trừ \1 Buff của mục tiêu"),
        (r"When this effect is active, increases ATK by (\d+%)", r"Khi hiệu ứng này có hiệu lực, Tấn Công của bản thân tăng \1"),
        (r"increases attack range of basic attack and skills by (\d+) tiles", r"Tầm bắn của Đánh Thường và tất cả KN chủ động tăng \1 ô"),
        (r"When dealing Ammo-type damage, increases damage dealt by (\d+%)", r"Khi gây ST Đạn, ST gây ra tăng \1"),
        (r"increases mobility by (\d+) tiles?", r"Tầm Di Chuyển tăng \1 ô"),
        (r"Gains (\d+) points of Confectance Index at the start of the battle", r"Khi bắt đầu chiến đấu, nhận \1 điểm Chỉ Số Nhiên Liệu"),
        (r"When under attack, defense is increased by (\d+%)", r"Khi bị tấn công, Phòng Thủ tăng \1"),
        (r"While on Hydro tiles, defense is increased by (\d+%)", r"Khi đứng trên ô địa hình Hóa Lỏng, Phòng Thủ tăng \1"),
        (r"Unlocked at Affinity Lvl (\d+)", r"Mở khóa khi Độ Tương Thích đạt Lv.\1"),
        (r"At the start of the action, gains Movement Up I for (\d+) turn", r"Khi bắt đầu hành động, nhận Tăng Di Chuyển I duy trì \1 hiệp"),
        (r"When the user causes the enemy to enter into Stability Break", r"Khi bản thân khiến kẻ địch rơi vào trạng thái Sụp Đổ Ổn Định"),
        (r"If the enemy target enters into Stability Break", r"Nếu mục tiêu địch rơi vào trạng thái Sụp Đổ Ổn Định"),
        (r"enters into Stability Break", r"rơi vào trạng thái Sụp Đổ Ổn Định"),
        (r"causes the enemy target to enter Stability Break", r"khiến mục tiêu địch rơi vào trạng thái Sụp Đổ Ổn Định"),
        (r"enter Stability Break", r"rơi vào trạng thái Sụp Đổ Ổn Định"),
        (r"Stability Break", r"Sụp Đổ Ổn Định"),
        (r"When self HP is below (\d+%), increase healing received by (\d+%)", r"Khi HP bản thân dưới \1, lượng trị liệu nhận được tăng \2"),
        (r"When the user is under the effects of Shelter, reduces AoE damage taken by (\d+%)", r"Khi bản thân có hiệu ứng Nơi Trú Ẩn, ST AoE phải chịu giảm \1"),
        (r"When having Shelter, reduces stability damage taken by (\d+) points?", r"Khi có Nơi Trú Ẩn, ST Ổn Định phải chịu giảm \1 điểm"),
        (r"When Shelter is active", r"Khi có Nơi Trú Ẩn"),
        (r"When Groza enters into Stability Break, restore (\d+%) of self max HP, (\d+) points of stability index, and cleanse (\d+) debuffs", r"Khi Groza rơi vào trạng thái Sụp Đổ Ổn Định, hồi phục \1 HP tối đa của bản thân, \2 điểm Chỉ Số Ổn Định và giải trừ \3 hiệu ứng Debuff"),
        (r"When Groza's action ends, applies Attack Down (\w+) on the enemy with the highest ATK", r"Khi kết thúc hành động của Groza, áp dụng Giảm Tấn Công \1 lên kẻ địch có Tấn Công cao nhất"),
        (r"Extends the duration of Movement Down (\w+) increases by (\d+) turns?", r"Thời gian duy trì Giảm Di Chuyển \1 tăng \2 hiệp"),
        (r"Restores (\d+) points of stability index", r"Hồi phục \1 điểm Chỉ Số Ổn Định"),
        (r"Before attacking, if the target's Stability is more than 0, increases damage dealt by (\d+%)", r"Trước khi tấn công, nếu Chỉ Số Ổn Định của mục tiêu lớn hơn 0, ST gây ra tăng \1"),
        (r"Increases damage dealt to enemy targets with Freeze type debuffs by (\d+%)", r"ST gây ra với mục tiêu địch có Debuff loại Băng Kết tăng \1"),
        (r"Extra Action increases mobility by (\d+) tiles?", r"Hành Động Bổ Sung tăng Tầm Di Chuyển \1 ô"),
        (r"reduces the Confectance Index consumption of the active skill ([^,]+) by (\d+)", r"giảm \2 điểm tiêu hao Chỉ Số Nhiên Liệu của KN chủ động \1"),
        (r"deals (\d+%) increased damage", r"ST gây ra tăng \1"),
        (r"At the start of (?:the )?battle, gains? (\d+) points? of Confectance Index", r"Khi bắt đầu chiến đấu, nhận \1 điểm Chỉ Số Nhiên Liệu"),
        (r"At the start of (?:the )?battle, increases? Confectance Index by (\d+) points?", r"Khi bắt đầu chiến đấu, nhận \1 điểm Chỉ Số Nhiên Liệu"),
        (r"applies Defen[sc]e Down (\w+) for (\d+) turns?", r"áp dụng Giảm Phòng Thủ \1 trong \2 hiệp"),
        (r"At the start of (?:the )?battle, gains? (\d+) stacks? of ([^,\.]+)", r"Khi bắt đầu chiến đấu, nhận \1 lớp \2"),
        (r"At the start of (?:the )?battle, applies ([^,\.]+) to ([^,\.]+)", r"Khi bắt đầu chiến đấu, áp dụng \1 lên \2"),
        (r"At the end of (?:the )?allied turn", r"Khi kết thúc hiệp đồng minh"),
        (r"At the start of (?:the )?turn", r"Khi bắt đầu hiệp"),
        (r"When using an active heal, there is a (\d+%) chance to apply ([^,\.]+)", r"Khi dùng kỹ năng hồi máu chủ động, có \1 tỷ lệ áp dụng \2"),
        (r"Before using a single target active heal, cleanses? (\d+) random buff", r"Trước khi dùng kỹ năng hồi máu chủ động đơn mục tiêu, giải trừ \1 buff ngẫu nhiên"),
        (r"Before using the basic attack ([^,]+), applies ([^,\.]+)", r"Trước khi dùng đánh thường \1, áp dụng \2"),
        (r"recovers (\d+) points? of stability for ([^,\.]+)", r"hồi phục \1 điểm ổn định cho \2"),
        (r"When inflicted with ([^,]+), immediately cleanses? ([^,\.]+)", r"Khi chịu \1, lập tức giải trừ \2"),
        (r"When healing an allied target other than the user, applies (\d+) stacks? of ([^,]+)", r"Khi trị liệu cho đơn vị đồng minh ngoài bản thân, áp dụng \1 lớp \2"),
        (r"increases damage dealt against enemy targets with movement debuffs by (\d+%)", r"ST gây ra với mục tiêu địch có Debuff loại di chuyển tăng \1"),
        (r"additionally applies Attack Up (\w+) for (\d+) turns?", r"áp dụng thêm Tăng Tấn Công \1 trong \2 hiệp"),
    ]
    for pattern, repl in replacements:
        res = re.sub(pattern, repl, res, flags=re.IGNORECASE)
    res = translate_stat_expression(res)
    return res


def translate_fort_fallback(text: str) -> str:
    """Fallback translation for Fortification effects."""
    if not text:
        return ""
    res = text
    replacements = [
        (r"Increases the damage multiplier by (\d+%)", r"Hệ số ST tăng \1"),
        (r"Increases damage multiplier by (\d+%)", r"Hệ số ST tăng \1"),
        (r"Increases damage multiplier to (\d+%) ATK", r"Hệ số ST tăng lên \1 Tấn Công"),
        (r"Increases damage multiplier to (\d+%)", r"Hệ số ST tăng lên \1"),
        (r"Damage multiplier increased by (\d+%)", r"Hệ số ST tăng \1"),
        (r"Increases Shield amount applied by allies by (\d+%)", r"Lượng Khiên đồng minh áp dụng tăng \1"),
        (r"reduces the cooldown of this skill by (\d+) turns?", r"Thời gian hồi chiêu kỹ năng này giảm \1 hiệp"),
        (r"Cleanses (\d+) debuffs?", r"Giải trừ \1 hiệu ứng Debuff"),
        (r"increases the effect range by (\d+) tiles?", r"Phạm vi hiệu lực tăng \1 ô"),
        (r"increases effect range by (\d+) tiles?", r"Phạm vi hiệu lực tăng \1 ô"),
        (r"Doubles the effects of ([^,\.]+) for self", r"Hiệu ứng \1 của bản thân được nhân đôi"),
        (r"Restores (\d+) points of stability index", r"Hồi phục \1 điểm Chỉ Số Ổn Định"),
        (r"If this skill causes the enemy to enter into Stability Break, the user gains (\d+) points? of Confection", r"Nếu kỹ năng này khiến kẻ địch rơi vào trạng thái Sụp Đổ Ổn Định, bản thân nhận \1 điểm Chỉ Số Nhiên Liệu"),
        (r"If this skill causes the enemy to enter into Stability Break, the user gains (\d+) points? of Confectance Index", r"Nếu kỹ năng này khiến kẻ địch rơi vào trạng thái Sụp Đổ Ổn Định, bản thân nhận \1 điểm Chỉ Số Nhiên Liệu"),
        (r"When Groza's action ends, applies Attack Down (\w+) on the enemy with the highest ATK", r"Khi kết thúc hành động của Groza, áp dụng Giảm Tấn Công \1 lên kẻ địch có Tấn Công cao nhất"),
        (r"Extends the duration of Movement Down (\w+) increases by (\d+) turns?", r"Thời gian duy trì Giảm Di Chuyển \1 tăng \2 hiệp"),
        (r"When having Shelter, reduces stability damage taken by (\d+) points?", r"Khi có Nơi Trú Ẩn, ST Ổn Định phải chịu giảm \1 điểm"),
    ]
    for pattern, repl in replacements:
        res = re.sub(pattern, repl, res, flags=re.IGNORECASE)
    res = translate_stat_expression(res)
    return res


def translate_basic_attack_fallback(text: str, element_vi: str) -> str:
    """Translate standard basic attack string if no exact line match."""
    match = re.search(r"within\s+(?:a\s+)?(\d+)\s+tile\s+radius\s+and\s+deals\s+([A-Za-z]+)\s+damage\s+equivalent\s+to\s+(\d+(?:\.\d+)?%)\s+ATK", text, re.IGNORECASE)
    if match:
        tiles, dmg_type, pct = match.groups()
        elem = ELEMENT_MAP.get(dmg_type.capitalize(), element_vi or "Vật Lý")
        return f"Chọn 1 mục tiêu địch trong phạm vi {tiles} ô xung quanh, gây ST {elem} bằng {pct} Tấn Công."
    return text


def numeric_tokens(text: str) -> Set[str]:
    """Return gameplay numbers while treating 3 and 3.0 as the same token."""
    result: Set[str] = set()
    # Color markup contains hex fragments such as ``#f26c1c`` which must not be
    # interpreted as gameplay values 26 and 1.
    plain = re.sub(r"\{\d+\}", "", clean_markup(text or ""))
    for token in re.findall(r"\b\d+(?:\.\d+)?\b", plain):
        result.add(token.rstrip("0").rstrip(".") if "." in token else token)
    return result


def numeric_signature(text: str) -> Tuple[str, ...]:
    """Numeric signature that preserves repeated gameplay values."""
    plain = re.sub(r"\{\d+\}", "", clean_markup(text or ""))
    values = []
    for token in re.findall(r"\b\d+(?:\.\d+)?\b", plain):
        values.append(token.rstrip("0").rstrip(".") if "." in token else token)
    return tuple(sorted(values))


def localized_match_score(
    english: str,
    vietnamese: str,
    *,
    element_vi: str = "",
    anchor_bonus: int = 0,
) -> int:
    """Score structural agreement without relying on translated prose."""
    en_pcts = set(re.findall(r"\b\d+(?:\.\d+)?%", english or ""))
    vi_pcts = set(re.findall(r"\b\d+(?:\.\d+)?%", vietnamese or ""))
    if en_pcts and not en_pcts.intersection(vi_pcts):
        return -1000
    if not en_pcts and vi_pcts:
        return -1000

    en_nums = numeric_tokens(english)
    vi_nums = numeric_tokens(vietnamese)
    common = en_nums.intersection(vi_nums)
    missing = en_nums - vi_nums
    extra = vi_nums - en_nums
    score = anchor_bonus + 18 * len(en_pcts.intersection(vi_pcts)) + 5 * len(common)
    score -= 9 * len(missing) + 3 * min(len(extra), 8)
    if en_nums and en_nums == vi_nums:
        score += 22
    if en_pcts and en_pcts == vi_pcts:
        score += 18
    if element_vi and element_vi in vietnamese:
        score += 10
    concepts = {
        "attack": ("Tấn Công",),
        "defense": ("Phòng Thủ",),
        "shield": ("Khiên",),
        "stability": ("Ổn Định",),
        "freeze": ("Băng Kết",),
        "frost": ("Băng", "Sương"),
        "burn": ("Thiêu Đốt",),
        "electric": ("Dẫn Điện",),
        "corrosion": ("Ăn Mòn",),
        "physical": ("Vật Lý",),
        "critical": ("Bạo Kích",),
        "brumal barrier": ("Bình Chướng Băng", "Khiên"),
        "battle prep": ("Chuẩn Bị Tác Chiến",),
        "liquid n2 fang": ("Châm Độc Nitơ Lỏng",),
        "tile": (" ô",),
        "turn": ("hiệp",),
        "cleanse": ("giải trừ",),
        "summon": ("triệu hồi", "Vật Triệu Hồi"),
        "support attack": ("tấn công chi viện",),
        "counterattack": ("phản kích",),
        "interception": ("phục kích",),
        "movement": ("Di Chuyển",),
        "healing": ("hồi phục", "trị liệu"),
        "stack": ("lớp",),
        "enemy": ("địch",),
        "allies": ("đồng minh",),
        "ally": ("đồng minh",),
        "buff": ("Buff", "hiệu ứng tăng cường"),
        "target": ("mục tiêu",),
        "dispel": ("giải trừ",),
    }
    english_low = (english or "").casefold()
    for english_term, vietnamese_terms in concepts.items():
        if english_term in english_low:
            score += 10 if any(term.casefold() in vietnamese.casefold() for term in vietnamese_terms) else -12
    return score


def key_semantic_match(english: str, vietnamese: str) -> bool:
    """Require most explicit gameplay concepts to agree for global key matches."""
    concepts = {
        "shield": ("Khiên",),
        "stability": ("Ổn Định",),
        "freeze": ("Băng Kết",),
        "frost": ("Băng", "Sương"),
        "stack": ("lớp",),
        "enemy": ("địch",),
        "allies": ("đồng minh",),
        "tile": (" ô",),
        "turn": ("hiệp",),
        "dispel": ("giải trừ",),
        "summon": ("triệu hồi", "Vật Triệu Hồi"),
        "critical": ("Bạo Kích",),
    }
    english_low = (english or "").casefold()
    expected = [values for term, values in concepts.items() if term in english_low]
    if len(expected) < 2:
        return True
    vietnamese_low = vietnamese.casefold()
    matched = sum(
        any(value.casefold() in vietnamese_low for value in values)
        for values in expected
    )
    return matched / len(expected) >= 0.75


def extract_all() -> int:
    print("=== Extracting Vietnamese Localization Data ===")

    previous_bundle: Dict[str, Any] = {}
    if OUTPUT_JSON.exists():
        previous_bundle = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))

    if not LANG_FILE.exists():
        print(f"Error: {LANG_FILE} does not exist.")
        return 1

    t0 = time.time()
    print(f"Loading {LANG_FILE.name} (approx 65 MB)...")
    raw_data = json.loads(LANG_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(raw_data)} raw records in {time.time() - t0:.2f}s.")

    # 1. Build indexed lookup structures
    id_to_text: Dict[int, str] = {}
    clean_to_id: Dict[str, int] = {}
    lower_to_clean: Dict[str, str] = {}
    kieu_cu_map: Dict[str, str] = {}
    pct_to_cids: Dict[str, List[int]] = {}
    cid_to_data: Dict[int, Tuple[str, Set[str], Set[str]]] = {}
    num_signature_to_cids: Dict[Tuple[str, ...], List[int]] = {}
    key_headers: Dict[int, Tuple[str, str, str]] = {}  # cid -> (prefix, key_name, desc_cand)

    for it in raw_data:
        raw_txt = it.get("text")
        if not raw_txt:
            continue
        txt = raw_txt.strip()
        idx = it["id"]
        id_to_text[idx] = txt

        cl = clean_markup(txt)
        if cl:
            if cl not in clean_to_id:
                clean_to_id[cl] = idx
            cl_low = cl.lower()
            if cl_low not in lower_to_clean:
                lower_to_clean[cl_low] = cl
            if cl.endswith("Kiểu Cũ"):
                base = cl[:-len("Kiểu Cũ")].strip().lower()
                kieu_cu_map[base] = cl

            # Key headers
            for pfx in ["Khóa Cố Định-", "Khóa Chung-", "Khóa Mở Rộng-", "Khóa Tương Thích-"]:
                if cl.startswith(pfx):
                    kname = cl[len(pfx):].strip()
                    desc_c = ""
                    for dlt in range(1, 5):
                        nxt = clean_markup(id_to_text.get(idx + dlt, ""))
                        if nxt and not any(nxt.startswith(p) for p in ["Khóa", "Skin-", "Rương", "Hộp"]):
                            desc_c = nxt
                            break
                    key_headers[idx] = (pfx, kname, desc_c)

        # Inverted index for lines with %
        if "%" in txt:
            pcts = set(re.findall(r"\b\d+(?:\.\d+)?%", txt))
            nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", txt))
            cid_to_data[idx] = (txt, pcts, nums)
            for p in pcts:
                if p not in pct_to_cids:
                    pct_to_cids[p] = []
                pct_to_cids[p].append(idx)

        if any(
            term in txt
            for term in (
                "Tấn Công", "Phòng Thủ", "Ổn Định", "Băng Kết", "Thiêu Đốt",
                "Dẫn Điện", "Ăn Mòn", "Vật Lý", "Bạo Kích", "hồi phục",
                "giải trừ", "triệu hồi", "Khiên", " ô", "hiệp",
            )
        ):
            signature = numeric_signature(txt)
            if signature:
                num_signature_to_cids.setdefault(signature, []).append(idx)

    print(f"Indexed {len(id_to_text)} texts, {len(cid_to_data)} lines with %, {len(key_headers)} key headers.")

    # 2. Extract Weapons Localization
    print("\nExtracting Weapon translations...")
    weapons_data = json.loads(WEAPONS_FILE.read_text(encoding="utf-8"))
    weapons_i18n: Dict[str, Any] = {}

    for w in weapons_data:
        slug = w["slug"]
        en_name = w["name"]
        vi_name = None

        if en_name.startswith("Retired "):
            base_en = en_name[len("Retired "):].strip()
            base_low = base_en.lower()
            if base_low in kieu_cu_map:
                vi_name = kieu_cu_map[base_low]
            else:
                tr_base = WEAPON_NAME_MAP.get(base_en, base_en)
                tr_low = tr_base.lower()
                if tr_low in kieu_cu_map:
                    vi_name = kieu_cu_map[tr_low]
                else:
                    vi_name = f"{tr_base} Kiểu Cũ"
        else:
            if en_name in WEAPON_NAME_MAP:
                vi_name = WEAPON_NAME_MAP[en_name]
            elif en_name.lower() in lower_to_clean:
                vi_name = lower_to_clean[en_name.lower()]
            else:
                vi_name = en_name

        vi_stats = translate_weapon_stats(w.get("stats", ""))
        vi_type = UI_DICTIONARY["weapon_types"].get(w.get("weapon_type", ""), w.get("weapon_type", ""))
        vi_rarity = UI_DICTIONARY["rarities"].get(w.get("rarity", ""), w.get("rarity", ""))
        vi_trait = w.get("trait")
        vi_effect = w.get("effect")

        weapons_i18n[slug] = {
            "name": vi_name,
            "en_name": en_name,
            "weapon_type": vi_type,
            "rarity": vi_rarity,
            "stats": vi_stats,
            "trait": vi_trait,
            "effect": vi_effect,
        }

    print(f"Extracted translations for {len(weapons_i18n)} weapons.")

    # 3. Extract Characters Localization
    print("\nExtracting Character translations...")
    char_files = sorted(CHAR_DIR.glob("*.json"))
    chars_i18n: Dict[str, Any] = {}

    # Locate character skill/imprint and neural helix anchors
    imprint_anchors: Dict[str, int] = {}
    neural_anchors: Dict[str, int] = {}
    for cl, idx in clean_to_id.items():
        if cl.startswith("Kỹ Năng Khắc Ấn-"):
            cname = cl[len("Kỹ Năng Khắc Ấn-"):].strip().lower()
            imprint_anchors[cname] = idx
        elif cl.startswith("Mạch Tâm Trí-"):
            cname = cl[len("Mạch Tâm Trí-"):].strip().lower()
            neural_anchors[cname] = idx

    for p in char_files:
        cdata = json.loads(p.read_text(encoding="utf-8"))
        slug = cdata["slug"]
        en_name = cdata.get("name", slug.title())
        elem_vi = ELEMENT_MAP.get(cdata.get("phase", ""), "")

        # Collect all anchor IDs for this character
        char_anchors: List[int] = []
        name_variations = [
            slug.lower(),
            en_name.lower(),
            slug.lower().replace("-", " "),
            en_name.lower().replace("-", " "),
            slug.lower().replace("-", ""),
            en_name.lower().replace("-", ""),
        ]
        if slug == "nemesis-gnosis":
            name_variations.extend(["nemesis-tia sáng", "nemesis tia sáng"])
        elif slug == "ots-14":
            name_variations.extend(["ots-14", "ots 14"])

        for nv in name_variations:
            if nv in imprint_anchors and imprint_anchors[nv] not in char_anchors:
                char_anchors.append(imprint_anchors[nv])
            if nv in neural_anchors and neural_anchors[nv] not in char_anchors:
                char_anchors.append(neural_anchors[nv])

        # 3.1 Translate Skills
        vi_skills = []
        used_skill_cids: Set[int] = set()

        for s_idx, s in enumerate(cdata.get("skills", [])):
            s_name_en = s.get("name", "")
            s_desc_en = s.get("description", "")
            s_tags_en = s.get("tags", [])
            s_pcts = set(re.findall(r"\b\d+(?:\.\d+)?%", s_desc_en))
            s_nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", s_desc_en))
            s_tiles = set(re.findall(r"\b(\d+)\s*tiles?\b", s_desc_en, re.IGNORECASE))
            s_turns = set(re.findall(r"\b(\d+)\s*turns?\b", s_desc_en, re.IGNORECASE))
            is_aoe = "AoE" in s_tags_en or "AoE" in s_desc_en

            s_name_vi = None
            s_desc_vi = None

            # Attempt matching via percentage inverted index and anchor ranges
            candidate_cids: Set[int] = set()
            for aid in char_anchors:
                for d in range(aid - 300, aid + 300):
                    if d in cid_to_data or d in id_to_text:
                        candidate_cids.add(d)

            best_cid = None
            best_score = -100
            for cid in candidate_cids:
                if cid in used_skill_cids:
                    continue
                txt, vi_pcts, vi_nums = cid_to_data.get(cid, (id_to_text.get(cid, ""), set(), set()))
                if not txt:
                    continue

                score = localized_match_score(
                    s_desc_en, txt, element_vi=elem_vi, anchor_bonus=25
                )
                if score <= -1000:
                    continue

                vi_tiles = set(re.findall(r"\b(\d+)\s*ô\b", txt))
                if s_tiles:
                    score += len(s_tiles.intersection(vi_tiles)) * 15

                vi_turns = set(re.findall(r"\b(\d+)\s*hiệp\b", txt))
                if s_turns:
                    score += len(s_turns.intersection(vi_turns)) * 12

                if is_aoe and "AoE" in txt:
                    score += 8

                if score > best_score:
                    best_score = score
                    best_cid = cid

            basic_attack = "Basic Attack" in s_tags_en or s_idx == 0
            exact_basic_numbers = (
                best_cid is not None
                and numeric_tokens(s_desc_en) == numeric_tokens(id_to_text[best_cid])
            )
            if best_cid and best_score >= 35 and (not basic_attack or exact_basic_numbers):
                used_skill_cids.add(best_cid)
                s_desc_vi = id_to_text[best_cid]
                # Look for skill name at best_cid - 1 or best_cid - 2
                for offset in [-1, -2, -3]:
                    cand_name = id_to_text.get(best_cid + offset, "").strip()
                    cand_cl = clean_markup(cand_name)
                    if cand_cl and len(cand_cl) <= 35 and not any(ch in cand_cl for ch in ["%", "áp dụng", "gây", "hồi phục", "chọn", "<color", "duy trì"]):
                        s_name_vi = cand_cl
                        break

            # Fallback for Basic Attack
            if not s_desc_vi and basic_attack:
                s_desc_vi = translate_basic_attack_fallback(s_desc_en, elem_vi)
                s_name_vi = "Bắn Thường" if not s_name_vi else s_name_vi

            # Final fallbacks
            s_tags_vi = [UI_DICTIONARY["tags"].get(t, t) for t in s_tags_en]

            vi_skills.append({
                "name": s_name_vi or s_name_en,
                "description": s_desc_vi or s_desc_en,
                "tags": s_tags_vi,
                "en_name": s_name_en,
            })

        # Collect local anchor keys and fortifications across all anchors
        local_fixed_keys: List[Tuple[int, str, str]] = []
        local_common_keys: List[Tuple[int, str, str]] = []
        local_expansion_keys: List[Tuple[int, str, str]] = []
        local_fort_cids: List[int] = []

        for aid in char_anchors:
            for chk_id in sorted(key_headers.keys()):
                if abs(chk_id - aid) < 300:
                    pfx, kname, desc_c = key_headers[chk_id]
                    nxt = id_to_text.get(chk_id + 1, "")
                    if nxt and not any(nxt.startswith(p) for p in ["Khóa ", "Skin-", "Rương", "Hộp", "“...", "Tham khảo"]):
                        full_desc = nxt
                    elif desc_c and not any(desc_c.startswith(p) for p in ["Khóa ", "Skin-", "Rương", "Hộp", "“...", "Tham khảo"]):
                        full_desc = desc_c
                    else:
                        full_desc = ""

                    if pfx == "Khóa Cố Định-" and (chk_id, f"Khóa Cố Định-{kname}", full_desc) not in local_fixed_keys:
                        local_fixed_keys.append((chk_id, f"Khóa Cố Định-{kname}", full_desc))
                    elif pfx == "Khóa Chung-" and (chk_id, f"Khóa Chung-{kname}", full_desc) not in local_common_keys:
                        local_common_keys.append((chk_id, f"Khóa Chung-{kname}", full_desc))
                    elif pfx == "Khóa Mở Rộng-" and (chk_id, f"Khóa Mở Rộng-{kname}", full_desc) not in local_expansion_keys:
                        local_expansion_keys.append((chk_id, f"Khóa Mở Rộng-{kname}", full_desc))

            for chk_id in range(aid - 300, aid + 300):
                chk_txt = id_to_text.get(chk_id, "")
                if any(kw in chk_txt for kw in ["Hệ số ST tăng", "nhận hiệu ứng mới", "đổi thành", "giải trừ", "Tầm bắn", "nhận thêm", "áp dụng thêm", "Bản thân hồi phục", "Thời gian duy trì", "hồi phục", "Khi Sụp Đổ Ổn Định", "Sụp Đổ Ổn Định"]):
                    if chk_id not in local_fort_cids:
                        local_fort_cids.append(chk_id)

        # 3.2 Translate Fortifications
        vi_fortifications = []
        known_skill_names_vi = [s.get("name") for s in vi_skills if s.get("name") and s.get("name") != s.get("en_name")]
        used_fort_cids: Set[int] = set()

        for f in cdata.get("fortification", []):
            f_tier = f.get("tier")
            f_skill = f.get("skill", "")
            f_eff = f.get("effect", "")
            f_pcts = set(re.findall(r"\b\d+(?:\.\d+)?%", f_eff))
            f_nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", f_eff))

            f_eff_vi = None

            candidate_cids: Set[int] = set(local_fort_cids)
            for aid in char_anchors:
                for d in range(aid - 250, aid + 250):
                    if d in id_to_text:
                        candidate_cids.add(d)

            best_cid = None
            best_score = -100
            for cid in candidate_cids:
                if cid in used_fort_cids:
                    continue
                txt, vi_pcts, vi_nums = cid_to_data.get(cid, (id_to_text.get(cid, ""), set(), set()))
                if any(txt.startswith(p) for p in ["Khóa ", "Skin-", "Rương", "Hộp", "“...", "Tham khảo"]):
                    continue

                score = localized_match_score(
                    f_eff, txt, element_vi=elem_vi, anchor_bonus=20
                )
                if score <= -1000:
                    continue
                if any(k in txt for k in ["Hệ số ST tăng", "nhận hiệu ứng mới", "đổi thành", "giải trừ", "Tầm bắn", "nhận thêm", "Bản thân hồi phục"]):
                    score += 10
                if any(kn in txt for kn in known_skill_names_vi):
                    score += 25

                if score > best_score:
                    best_score = score
                    best_cid = cid

            if best_cid and best_score >= 32:
                used_fort_cids.add(best_cid)
                f_eff_vi = id_to_text[best_cid]
            else:
                f_eff_vi = translate_fort_fallback(f_eff)

            vi_fortifications.append({
                "tier": f_tier,
                "level": f.get("level"),
                "skill": f_skill,
                "effect": f_eff_vi,
            })

        # 3.3 Translate Neural Helix
        vi_helix = []
        for h in cdata.get("neural_helix", []):
            h_node = h.get("node", "")
            h_node_vi = re.sub(r"\bEnhancement\s+(\d+)\b", r"Cường Hóa \1", h_node)
            h_eff_vi = translate_stat_expression(h.get("effect", ""))
            vi_helix.append({
                "node": h_node_vi,
                "level": h.get("level"),
                "effect": h_eff_vi,
                "materials": h.get("materials"),
            })

        # 3.4 Translate Keys
        vi_keys = []
        used_key_cids: Set[int] = set()

        def best_local_key(
            entries: List[Tuple[int, str, str]], english_effect: str, prefix: str
        ) -> Tuple[int, str, str] | None:
            scored = [
                (localized_match_score(english_effect, entry[2]), entry)
                for entry in entries
                if entry[0] not in used_key_cids and entry[2]
                and numeric_signature(english_effect) == numeric_signature(entry[2])
                and key_semantic_match(english_effect, entry[2])
            ]
            if scored:
                score, entry = max(scored, key=lambda item: (item[0], -item[1][0]))
                if score >= 28:
                    used_key_cids.add(entry[0])
                    return entry

            signature = numeric_signature(english_effect)
            global_scored = []
            candidate_ids = list(num_signature_to_cids.get(signature, []))
            # Vietnamese often writes an explicit "1" for English "each/a/an".
            with_implicit_one = tuple(sorted((*signature, "1")))
            candidate_ids.extend(num_signature_to_cids.get(with_implicit_one, []))
            for cid in dict.fromkeys(candidate_ids):
                if cid in used_key_cids:
                    continue
                candidate = id_to_text[cid]
                if not key_semantic_match(english_effect, candidate):
                    continue
                score = localized_match_score(english_effect, candidate)
                if en_name.casefold() in candidate.casefold():
                    score += 12
                if any(abs(cid - anchor) < 300 for anchor in char_anchors):
                    score += 20
                global_scored.append((score, cid, candidate))
            if not global_scored:
                return None
            score, cid, candidate = max(global_scored, key=lambda item: (item[0], -item[1]))
            if score < 40:
                return None
            title = clean_markup(id_to_text.get(cid - 1, ""))
            if (
                not title
                or len(title) > 55
                or numeric_tokens(title)
                or "/" in title
                or title.casefold().startswith(("chủ động", "bị động", "quyết thắng"))
            ):
                title = ""
            used_key_cids.add(cid)
            return cid, f"{prefix}{title}" if title else prefix.rstrip("-"), candidate

        for k_idx, k in enumerate(cdata.get("keys", [])):
            k_name = k.get("name", "")
            k_eff = k.get("effect", "")
            k_mat = k.get("materials", "")
            k_pcts = set(re.findall(r"\b\d+(?:\.\d+)?%", k_eff))
            k_nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", k_eff))

            k_name_vi = None
            k_eff_vi = None
            k_mat_vi = None

            if "Affinity Key" in k_name:
                k_name_vi = "Khóa Tương Thích"
                k_eff_vi = translate_stat_expression(k_eff)
                k_mat_vi = translate_key_fallback(k_mat)
            elif k_name.startswith("Fixed Key"):
                matched_key = best_local_key(local_fixed_keys, k_eff, "Khóa Cố Định-")
                if matched_key:
                    _, k_name_vi, k_eff_vi = matched_key
                else:
                    k_eff_vi = translate_key_fallback(k_eff)
                k_mat_vi = translate_key_fallback(k_mat)
            elif "Common Key" in k_name:
                common_parts = [part.strip() for part in k_eff.split("/", 1)]
                match_effect = common_parts[-1]
                matched_key = best_local_key(local_common_keys, match_effect, "Khóa Chung-")
                if matched_key:
                    _, k_name_vi, k_eff_vi = matched_key
                    if len(common_parts) == 2:
                        k_eff_vi = f"{translate_stat_expression(common_parts[0])} / {k_eff_vi}"
                else:
                    k_eff_vi = translate_key_fallback(k_eff)
                k_mat_vi = translate_key_fallback(k_mat)
            elif "Expansion Key" in k_name:
                matched_key = best_local_key(local_expansion_keys, k_eff, "Khóa Mở Rộng-")
                if matched_key:
                    _, k_name_vi, k_eff_vi = matched_key
                else:
                    k_eff_vi = translate_key_fallback(k_eff)
                k_mat_vi = translate_key_fallback(k_mat)
            else:
                # Try finding matching key in key_headers or pct_to_cids
                candidate_cids: Set[int] = set()
                for aid in char_anchors:
                    for d in range(aid - 300, aid + 300):
                        if d in id_to_text:
                            candidate_cids.add(d)

                if k_pcts:
                    for pct in k_pcts:
                        if pct in pct_to_cids:
                            candidate_cids.update(pct_to_cids[pct])

                best_cid = None
                best_score = -100
                for cid in candidate_cids:
                    txt, vi_pcts, vi_nums = cid_to_data.get(cid, (id_to_text.get(cid, ""), set(), set()))
                    if any(txt.startswith(p) for p in ["Khóa ", "Skin-", "Rương", "Hộp", "“...", "Tham khảo", "Báo cáo", "Nội dung"]):
                        continue

                    comm_pcts = k_pcts.intersection(vi_pcts)
                    if k_pcts and not comm_pcts:
                        continue
                    if not k_pcts and vi_pcts:
                        continue
                    if not k_pcts and not any(kw in txt for kw in ["Tấn Công", "Phòng Thủ", "HP", "Chỉ Số", "ST", "hiệp", "ô", "lớp", "hồi phục", "giải trừ", "kỹ năng", "KN"]):
                        continue

                    score = len(comm_pcts) * 20
                    if k_pcts and comm_pcts == k_pcts:
                        score += 15
                    score += len(k_nums.intersection(vi_nums)) * 3
                    for aid in char_anchors:
                        if abs(cid - aid) < 300:
                            score += 20
                            break
                    if score > best_score:
                        best_score = score
                        best_cid = cid

                min_score = 25 if not k_pcts else 15
                if best_cid and best_score >= min_score:
                    k_eff_vi = id_to_text[best_cid]
                    cand_h = id_to_text.get(best_cid - 1, "")
                    if cand_h.startswith("Khóa "):
                        k_name_vi = cand_h
                else:
                    k_eff_vi = translate_key_fallback(k_eff)

                k_mat_vi = translate_key_fallback(k_mat)

            # Format key name prefix if not official
            if not k_name_vi:
                if k_name.startswith("Fixed Key"):
                    num_m = re.search(r"Fixed Key\s+(\d+)", k_name)
                    k_num = num_m.group(1) if num_m else str(k_idx + 1)
                    k_name_vi = f"Khóa Cố Định {k_num}"
                elif "Common Key" in k_name:
                    k_name_vi = "Khóa Chung"
                elif "Expansion Key" in k_name:
                    k_name_vi = "Khóa Mở Rộng"
                else:
                    k_name_vi = k_name

            vi_keys.append({
                "name": k_name_vi,
                "level": k.get("level"),
                "effect": k_eff_vi or k_eff,
                "materials": k_mat_vi or k_mat,
            })

        # 3.5 Translate Summons
        vi_summons = []
        for sm in cdata.get("summons", []):
            sm_name = sm.get("name", "")
            sm_desc = sm.get("description", "")
            sm_stats = sm.get("stats")

            vi_sm_stats = None
            if sm_stats:
                vi_sm_stats = {}
                for skey, sval in sm_stats.items():
                    if isinstance(sval, str):
                        # Translate "50% of Andoris' initial HP" -> "50% HP ban đầu của Andoris"
                        m = re.search(r"(\d+(?:\.\d+)?%)\s+of\s+([^']+)'\s+initial\s+([A-Za-z]+)", sval)
                        if m:
                            pct, char_n, stat_n = m.groups()
                            vi_stat = translate_stat_expression(stat_n)
                            vi_sm_stats[skey] = f"{pct} {vi_stat} ban đầu của {char_n}"
                        else:
                            vi_sm_stats[skey] = translate_stat_expression(sval)
                    else:
                        vi_sm_stats[skey] = sval

            vi_summons.append({
                "name": sm_name,
                "type": sm.get("type"),
                "description": sm_desc,
                "stats": vi_sm_stats,
            })

        # Class, Phase, Weapon Type, Ammo Type translations
        vi_class = UI_DICTIONARY["classes"].get(cdata.get("class", ""), cdata.get("class", ""))
        vi_phase = UI_DICTIONARY["phases"].get(cdata.get("phase", ""), cdata.get("phase", ""))
        vi_rarity = UI_DICTIONARY["rarities"].get(cdata.get("rarity", ""), cdata.get("rarity", ""))
        vi_weapon_type = UI_DICTIONARY["weapon_types"].get(cdata.get("weapon_type", ""), cdata.get("weapon_type", ""))
        vi_ammo_type = UI_DICTIONARY["ammo_types"].get(cdata.get("ammo_type", ""), cdata.get("ammo_type", ""))
        vi_sig_weapon = WEAPON_NAME_MAP.get(cdata.get("signature_weapon", ""), cdata.get("signature_weapon", ""))
        vi_weakness = UI_DICTIONARY["phases"].get(cdata.get("weakness", ""), cdata.get("weakness", ""))

        chars_i18n[slug] = {
            "name": en_name,
            "en_name": en_name,
            "class": vi_class,
            "phase": vi_phase,
            "rarity": vi_rarity,
            "weapon_type": vi_weapon_type,
            "ammo_type": vi_ammo_type,
            "signature_weapon": vi_sig_weapon,
            "weakness": vi_weakness,
            "skills": vi_skills,
            "fortification": vi_fortifications,
            "neural_helix": vi_helix,
            "keys": vi_keys,
            "summons": vi_summons,
        }

    print(f"Extracted translations for {len(chars_i18n)} characters.")

    # 4. Construct Full I18n Bundle
    i18n_bundle = {
        "ui": UI_DICTIONARY,
        # This extractor is authoritative for character strings only. Preserve
        # the curated weapon catalog produced by build_vietnamese_effects.py.
        "weapons": previous_bundle.get("weapons", weapons_i18n),
        "characters": chars_i18n,
    }
    if "effects" in previous_bundle:
        i18n_bundle["effects"] = previous_bundle["effects"]

    # Save to data/i18n_vi.json and site/static/js/i18n-vi.js atomically
    print(f"\nWriting to {OUTPUT_JSON.relative_to(ROOT)}...")
    from tools.editor_core.bundle import stage_i18n_bundle
    from tools.editor_core.transaction import RepositoryTransaction

    tx = RepositoryTransaction(ROOT)
    with tx:
        stage_i18n_bundle(ROOT, tx, i18n_bundle=i18n_bundle)
        tx.commit()

    print(f"✅ Successfully exported Vietnamese localization ({OUTPUT_JSON.stat().st_size // 1024} KB).")
    return 0


if __name__ == "__main__":
    sys.exit(extract_all())
