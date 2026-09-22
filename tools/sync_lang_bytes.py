"""Sync unambiguous official EN/VI localization pairs into project JSON."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from tools.parse_lang_bytes import parse_file

ROOT = Path(__file__).resolve().parents[1]
I18N_PATH = ROOT / "data" / "i18n_vi.json"
EFFECTS_PATH = ROOT / "data" / "effects_vi.json"
WEAPONS_PATH = ROOT / "data" / "weapons.json"
WEAPON_HELPERS_PATH = ROOT / "data" / "weapons_vi.json"
I18N_JS_PATH = ROOT / "site" / "static" / "js" / "i18n-vi.js"

WEAPON_TYPES = {
    "Assault Rifle": "Súng Trường", "SMG": "Súng Tiểu Liên", "Shotgun": "Súng Shotgun",
    "MG": "Súng Máy", "Sniper Rifle": "Súng Bắn Tỉa", "Handgun": "Súng Lục", "Blade": "Đao",
}

WEAPON_OVERRIDES = {
    "dona-eis-requiem": {
        "trait": "ST AoE do bản thân và Vật Triệu Hồi của bản thân gây ra tăng 5%. Nếu gây ST AoE Ăn Mòn, ST AoE gây ra tăng thêm 5%.",
        "effect": "ST Ăn Mòn do tất cả đơn vị đồng minh gây ra tăng 10%. Với mỗi đơn vị được triệu hồi, ST Ăn Mòn do bản thân và Vật Triệu Hồi của bản thân gây ra tăng 5%/7%/9%/11%/13%/15%, tối đa 15%/21%/27%/33%/39%/45%.\n\nKỹ Năng Khắc Ấn: ST gây ra lên mục tiêu có Debuff Ăn Mòn tăng 2.5%. ST gây ra lên đơn vị Tài Phiệt Orlog tăng 2.5%.",
    },
    "silver-winged-pistis": {
        "trait": "Nếu kỹ năng không tiêu hao Chỉ Số Nhiên Liệu, ST Bạo Kích tăng 10%.",
        "effect": "ST Băng Kết gây ra tăng 20%/25%/30%/35%/40%/45%. Nếu kỹ năng không tiêu hao Chỉ Số Nhiên Liệu và gây ST lên kẻ địch đứng trên ô Băng Kết, bỏ qua 5% Phòng Thủ của mục tiêu.\n\nKỹ Năng Khắc Ấn: ST gây ra lên mục tiêu có Debuff Băng Kết tăng 2.5%. ST gây ra lên Varjager tăng 2.5%.",
    },
    "dulcet-defender": {
        "trait": "ST Vật Lý phải chịu giảm 8%.",
        "effect": "Phòng Thủ của bản thân tăng 15%/20%/25%/30%/35%/40% và ST do Đánh Thường gây ra tăng 25%/30%/35%/40%/45%/50%. Khi hành động kết thúc, hồi phục HP bằng 5% HP tối đa.\n\nKỹ Năng Khắc Ấn: ST gây ra lên đơn vị Công Nghệ Sycca tăng 2.5%. Nếu mục tiêu có Debuff Băng Kết, ST gây ra tăng thêm 2.5%.",
    },
    "transience": {
        "trait": "Khi hành động kết thúc, Vật Triệu Hồi Vật Lý của bản thân nhận 1 Buff ngẫu nhiên, duy trì 2 hiệp.",
        "effect": "ST Hóa Lỏng do bản thân và Vật Triệu Hồi Vật Lý của bản thân gây ra tăng 20%/24%/28%/32%/36%/40%. ST Bạo Kích do Đánh Thường của bản thân gây ra tăng 15%/18%/21%/24%/27%/30%.\n\nKỹ Năng Khắc Ấn: ST gây ra lên mục tiêu có Debuff Hóa Lỏng tăng 2.5%. ST gây ra lên mục tiêu không có phe tăng 2.5%.",
    },
    "chinchilla-nova": {
        "trait": "ST do bản thân và Vật Triệu Hồi Vật Lý của bản thân gây ra tăng 5%. Nếu gây ST Hóa Lỏng, ST gây ra tăng thêm 5%.",
        "effect": "ST do bản thân và Vật Triệu Hồi Vật Lý của bản thân gây ra tăng 10%/12%/14%/16%/18%/20%. Nếu mục tiêu đứng trên ô Hóa Lỏng, ST gây ra và ST Bạo Kích tăng thêm 10%/12%/14%/16%/18%/20%.\n\nKỹ Năng Khắc Ấn: ST gây ra lên mục tiêu có Debuff Hóa Lỏng tăng 2.5%. ST gây ra lên đơn vị Varjager tăng 2.5%.",
    },
    "sibyl": {
        "trait": "ST do Tấn Công Chi Viện gây ra tăng 10%.",
        "effect": "ST Ăn Mòn do bản thân gây ra tăng 20%/24%/28%/32%/36%/40%. ST Bạo Kích do Tấn Công Chi Viện gây ra tăng 10%.\n\nKỹ Năng Khắc Ấn: ST gây ra lên mục tiêu có Debuff Ăn Mòn tăng 2.5%. ST gây ra lên đơn vị Paradeus tăng 2.5%.",
    },
    "cause-and-effect": {
        "trait": "ST AoE gây ra tăng 5%. Khi gây ST AoE Ăn Mòn, ST AoE gây ra tăng thêm 5%.",
        "effect": "ST Ăn Mòn tăng 15%/18%/21%/24%/27%/30%. Nếu kỹ năng chủ động không gây ST, ST Bạo Kích của lần tấn công tiếp theo tăng 15%/18%/21%/24%/27%/30%.\n\nKỹ Năng Khắc Ấn: ST gây ra lên mục tiêu có Debuff Ăn Mòn tăng 2.5%. ST gây ra lên đơn vị P.M.C. tăng 2.5%.",
    },
    "sparkling-centerstage": {
        "trait": "Khi bắt đầu hành động, nếu bản thân đầy HP, nhận 1 Buff ngẫu nhiên, duy trì 1 hiệp.",
        "effect": "Khi đơn vị đồng minh chủ động gây ST Vật Lý, bỏ qua 10% Phòng Thủ của mục tiêu địch. Với mỗi Buff áp dụng cho đơn vị đồng minh (không gồm bản thân), ST Vật Lý do tấn công chủ động của bản thân gây ra bỏ qua thêm 4% Phòng Thủ của mục tiêu, tối đa 20%/24%/28%/32%/36%/40%.\n\nKỹ Năng Khắc Ấn: ST gây ra lên mục tiêu có Debuff Phòng Thủ tăng 2.5%. ST gây ra lên đơn vị Công Nghệ Sycca tăng 2.5%.",
    },
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def official_lookup(en_rows: list[dict], vi_rows: list[dict]):
    vi_by_id = {row["id"]: row["text"] for row in vi_rows if isinstance(row.get("text"), str)}
    grouped: dict[str, set[str]] = defaultdict(set)
    ids: dict[str, list[int]] = defaultdict(list)
    for row in en_rows:
        english = row.get("text")
        vietnamese = vi_by_id.get(row.get("id"))
        if isinstance(english, str) and isinstance(vietnamese, str):
            key = norm(english)
            grouped[key].add(vietnamese)
            ids[key].append(row["id"])

    def lookup(english):
        if not isinstance(english, str) or not english.strip():
            return None
        candidates = grouped.get(norm(english), set())
        return next(iter(candidates)) if len(candidates) == 1 else None

    return lookup, grouped, ids


def update_field(target: dict, key: str, english, lookup, stats: Counter) -> None:
    translated = lookup(english)
    if translated is None:
        stats["unmatched_or_ambiguous"] += 1
    elif target.get(key) == translated:
        stats["already_exact"] += 1
    else:
        target[key] = translated
        stats["updated"] += 1


def update_list(source: dict, target: dict, section: str, pairs, lookup, stats: Counter) -> None:
    src_items = source.get(section) or []
    dst_items = target.get(section) or []
    while len(dst_items) < len(src_items):
        dst_items.append({})
        stats["target_items_added"] += 1
    target[section] = dst_items
    for index, src_item in enumerate(src_items):
        if not isinstance(dst_items[index], dict):
            stats["missing_target_item"] += 1
            continue
        dst_item = dst_items[index]
        for src_key, dst_key in pairs:
            value = src_item.get(src_key)
            if isinstance(value, list):
                current = dst_item.get(dst_key)
                if not isinstance(current, list):
                    current = []
                while len(current) < len(value):
                    current.append("")
                for sub_index, english in enumerate(value):
                    translated = lookup(english)
                    if translated is None:
                        stats["unmatched_or_ambiguous"] += 1
                        if not isinstance(current[sub_index], str) or not current[sub_index].strip():
                            current[sub_index] = english if isinstance(english, str) else ""
                            stats["source_fallback"] += 1
                    elif current[sub_index] == translated:
                        stats["already_exact"] += 1
                    else:
                        current[sub_index] = translated
                        stats["updated"] += 1
                dst_item[dst_key] = current
            else:
                update_field(dst_item, dst_key, value, lookup, stats)


def translate_stats(value: str) -> str:
    replacements = (("Attack Boost", "Tăng Tấn Công"), ("Attack", "Tấn Công"),
                    ("CRIT DMG", "ST Bạo Kích"), ("CRIT Rate", "TL Bạo Kích"),
                    ("Defense", "Phòng Thủ"))
    for english, vietnamese in replacements:
        value = re.sub(rf"\b{re.escape(english)}\b", vietnamese, value)
    return value


def fallback_weapon_text(value: str | None, helpers: dict, section: str) -> str | None:
    if not value:
        return value
    direct = helpers.get(section, {}).get(value)
    return direct if direct is not None else value


def run(source_dir: Path, apply: bool) -> dict:
    en_path = source_dir / "LangPackageTableEnusData.bytes"
    vi_path = source_dir / "LangPackageTableVtviData.bytes"
    if not en_path.exists() or not vi_path.exists():
        raise FileNotFoundError("source directory must contain ENUS and VTVI language package files")
    en_rows = parse_file(en_path)
    vi_rows = parse_file(vi_path)
    lookup, _, _ = official_lookup(en_rows, vi_rows)

    i18n = read_json(I18N_PATH)
    effects = read_json(EFFECTS_PATH)
    weapons = read_json(WEAPONS_PATH)
    helpers = read_json(WEAPON_HELPERS_PATH)
    stats: Counter = Counter()

    for path in sorted((ROOT / "data" / "characters").glob("*.json")):
        source = read_json(path)
        target = i18n["characters"].get(source["slug"])
        if not target:
            stats["missing_character"] += 1
            continue
        update_field(target, "name", source.get("name"), lookup, stats)
        update_list(source, target, "skills", (("name", "name"), ("description", "description"), ("tags", "tags")), lookup, stats)
        update_list(source, target, "fortification", (("skill", "skill"), ("effect", "effect")), lookup, stats)
        update_list(source, target, "neural_helix", (("node", "node"), ("effect", "effect")), lookup, stats)
        update_list(source, target, "keys", (("name", "name"), ("effect", "effect")), lookup, stats)
        update_list(source, target, "summons", (("name", "name"), ("description", "description")), lookup, stats)

    translated_weapons = i18n["weapons"]
    for weapon in weapons:
        slug = weapon["slug"]
        if slug not in translated_weapons:
            translated_weapons[slug] = {
                "name": lookup(weapon.get("name")) or weapon.get("name"),
                "en_name": weapon.get("name"),
                "weapon_type": lookup(weapon.get("weapon_type")) or WEAPON_TYPES.get(weapon.get("weapon_type"), weapon.get("weapon_type")),
                "rarity": weapon.get("rarity"),
                "stats": translate_stats(weapon.get("stats", "")),
                "trait": lookup(weapon.get("trait")) or fallback_weapon_text(weapon.get("trait"), helpers, "traits"),
                "effect": lookup(weapon.get("effect")) or fallback_weapon_text(weapon.get("effect"), helpers, "paragraphs"),
                "server": weapon.get("server"),
            }
            stats["weapons_added"] += 1
        target = translated_weapons[slug]
        for field in ("name", "weapon_type", "stats", "trait", "effect"):
            update_field(target, field, weapon.get(field), lookup, stats)
        for field, value in WEAPON_OVERRIDES.get(slug, {}).items():
            if target.get(field) != value:
                target[field] = value
                stats["verified_overrides"] += 1

    for effect in effects.values():
        update_field(effect, "name", effect.get("name_en"), lookup, stats)
        update_field(effect, "desc", effect.get("desc_en"), lookup, stats)
    i18n["effects"] = effects

    if apply:
        from tools.editor_core.bundle import stage_i18n_bundle
        from tools.editor_core.transaction import RepositoryTransaction

        tx = RepositoryTransaction(ROOT)
        with tx:
            stage_i18n_bundle(ROOT, tx, i18n_bundle=i18n, effects_data=effects)
            tx.commit()
    return {"language_entries": {"en": len(en_rows), "vi": len(vi_rows)}, "changes": dict(stats), "applied": apply}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path, help="directory containing LangPackageTableEnusData.bytes and LangPackageTableVtviData.bytes")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.source_dir, args.apply), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
