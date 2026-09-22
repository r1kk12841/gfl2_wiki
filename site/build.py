#!/usr/bin/env python3
"""
site/build.py
Static Site Generator for GFL2: Exilium Wiki.
Reads /data/*.json and /assets, renders Jinja2 templates into /dist,
and emits search-index.json for client-side search.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import html
from html.parser import HTMLParser
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

import jinja2
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.validate import validate_all
from tools.effects_catalog import browser_catalog, canonicalize_effects, effect_id

DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
STATIC_DIR = ROOT / "site" / "static"
TEMPLATES_DIR = ROOT / "site" / "templates"
DIST_DIR = ROOT / "dist"

DEFAULT_SITE_URL = "https://r1kk12841.github.io/gfl2_wiki"
SITE_URL = os.environ.get("GFL2_SITE_URL", DEFAULT_SITE_URL).rstrip("/")

EFFECTS_DATA: dict[str, str] = {}
EFFECT_IDS_BY_NAME: dict[str, str] = {}
EFFECTS_PATTERN: re.Pattern | None = None



def load_effects() -> None:
    """Load effects dictionary from assets/effects.json and build regex."""
    global EFFECTS_DATA, EFFECTS_PATTERN, EFFECT_IDS_BY_NAME
    effects_file = ASSETS_DIR / "effects.json"
    if effects_file.exists():
        try:
            raw_data = json.loads(effects_file.read_text(encoding="utf-8"))
            localized_file = DATA_DIR / "effects_vi.json"
            localized = canonicalize_effects(json.loads(localized_file.read_text(encoding="utf-8-sig"))) if localized_file.exists() else {}

            EFFECTS_DATA = {}
            EFFECT_IDS_BY_NAME = {}
            for key, entry in localized.items():
                name_en = entry.get("name_en")
                if name_en:
                    EFFECT_IDS_BY_NAME[name_en] = entry["id"]
                    EFFECTS_DATA[name_en] = entry.get("desc_en") or entry.get("desc") or ""

            for key, entry in raw_data.items():
                if isinstance(entry, dict):
                    name_en = entry.get("name_en")
                    if name_en and name_en not in EFFECT_IDS_BY_NAME:
                        EFFECT_IDS_BY_NAME[name_en] = entry.get("id", key)
                        EFFECTS_DATA[name_en] = entry.get("desc_en") or entry.get("desc") or ""
                elif isinstance(entry, str) and key not in EFFECT_IDS_BY_NAME:
                    EFFECT_IDS_BY_NAME[key] = effect_id(key)
                    EFFECTS_DATA[key] = entry

            sorted_keys = sorted(EFFECT_IDS_BY_NAME.keys(), key=len, reverse=True)
            pattern_str = r'\b(' + '|'.join(re.escape(k) for k in sorted_keys) + r')\b'
            EFFECTS_PATTERN = re.compile(pattern_str)
            print(f"Loaded {len(EFFECT_IDS_BY_NAME)} status effects for HTML markup.")
        except Exception as e:
            print(f"Warning: Failed to load effects.json: {e}")


def generate_effects_js(output_file: Path) -> None:
    """Generate effects-data.js with dual-language effects data and sub-effect relationships."""
    effects_vi_file = DATA_DIR / "effects_vi.json"
    effects_file = ASSETS_DIR / "effects.json"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if effects_vi_file.exists():
        try:
            data = canonicalize_effects(json.loads(effects_vi_file.read_text(encoding="utf-8-sig")))
            payload = browser_catalog(data)
            output_file.write_text(f"// Auto-generated GFL2 ID-keyed effects database\nwindow.GFL2_EFFECTS = {json.dumps(payload, ensure_ascii=False, indent=2)};\n", encoding="utf-8")
            print(f"Generated {output_file.name} with {len(data)} ID-keyed effect entries.")
            return
        except Exception as e:
            print(f"Warning: Failed to load effects_vi.json: {e}")

    if not effects_file.exists():
        return

    try:
        eff = json.loads(effects_file.read_text(encoding="utf-8"))
        sorted_names = sorted(eff.keys(), key=len, reverse=True)

        data = {}
        for name, desc in eff.items():
            desc_lower = desc.lower()
            if "debuff" in desc_lower:
                eff_type = "debuff"
            elif "buff" in desc_lower:
                eff_type = "buff"
            else:
                eff_type = "effect"

            # Find all direct and transitive sub-effects using compiled pattern
            subs = []
            seen = {name}
            queue = [name]
            while queue:
                curr = queue.pop(0)
                curr_desc = eff.get(curr, "")
                if EFFECTS_PATTERN:
                    for other in EFFECTS_PATTERN.findall(curr_desc):
                        if other not in seen and len(other) > 2:
                            seen.add(other)
                            subs.append(other)
                            queue.append(other)

            current_id = effect_id(name)
            data[current_id] = {
                "id": current_id,
                "name": name,
                "name_en": name,
                "desc": desc,
                "desc_en": desc,
                "type": eff_type,
                "sub_effect_ids": [effect_id(sub) for sub in subs]
            }

        payload = browser_catalog(data)
        output_file.write_text(f"// Auto-generated GFL2 ID-keyed effects database\nwindow.GFL2_EFFECTS = {json.dumps(payload, ensure_ascii=False, indent=2)};\n", encoding="utf-8")
        print(f"Generated {output_file.name} with {len(data)} effect entries.")
    except Exception as e:
        print(f"Warning: Failed to generate effects-data.js: {e}")



# Damage types regex mapping to Dandegate colors
DMG_PATTERNS = [
    (re.compile(r'\b(Freeze\s+[Dd]amage|ST\s+Băng\s+Kết|ST\s+Băng)\b'), 'dmg-freeze'),
    (re.compile(r'\b(Burn\s+[Dd]amage|ST\s+Thiêu\s+Đốt)\b'), 'dmg-burn'),
    (re.compile(r'\b(Corrosion\s+[Dd]amage|ST\s+Ăn\s+Mòn)\b'), 'dmg-corrosion'),
    (re.compile(r'\b(Hydro\s+[Dd]amage|ST\s+Hóa\s+Lỏng)\b'), 'dmg-hydro'),
    (re.compile(r'\b(Electric\s+[Dd]amage|ST\s+Dẫn\s+Điện|Sát\s+[Tt]hương\s+Dẫn\s+Điện|ST\s+Điện\s+Từ|ST\s+Điện)\b'), 'dmg-electric'),
    (re.compile(r'\b(Physical\s+[Dd]amage|ST\s+Vật\s+Lý)\b'), 'dmg-physical'),
    (re.compile(r'\b([Ff]ixed\s+[Dd]amage|[Rr]eal\s+[Dd]amage|ST\s+cố\s+định|ST\s+Chuẩn\s+Xác)\b'), 'dmg-fixed'),
    (re.compile(r'\b([Ss]tability\s+[Dd]amage|ST\s+Ổn\s+Định)\b'), 'dmg-stability'),
]

# Percentages e.g. 80%, 100%, or chained 5%/6%/7%/8%/9%/15%
PERCENT_PATTERN = re.compile(r'\b(?:\d+(?:\.\d+)?%(?:\s*/\s*)?)+')

# Range/mobility tiles e.g. 6 tiles, 1 tile, 8 tiles, 4 to 8 tiles, 2/2/3/3 tiles, 1 tile radius, 5 tiles wide
TILE_PATTERN = re.compile(r'\b(?:\d+(?:\.\d+)?(?:\s*(?:[/to-]|to)\s*|\s*,\s*))*\d+(?:\.\d+)?\s*-?\s*tiles?(?:\s+(?:radius|wide))?\b', re.IGNORECASE)


def highlight_plain_text(content: str) -> str:
    """Highlight damage types, percentages, and tile ranges within plain text."""
    # 1. Damage types
    for pattern, css_class in DMG_PATTERNS:
        content = pattern.sub(rf'<span class="{css_class}">\1</span>', content)
    # 2. Percentages
    content = PERCENT_PATTERN.sub(r'<span class="val-highlight">\g<0></span>', content)
    # 3. Tiles
    content = TILE_PATTERN.sub(r'<span class="val-highlight">\g<0></span>', content)
    return content


def format_rich_text(text: str) -> str:
    """Format rich text preserving existing HTML tags and their attributes."""
    parts = re.split(r'(<[^>]+>)', text)
    for i in range(0, len(parts), 2):
        if parts[i]:
            parts[i] = highlight_plain_text(parts[i])
    return "".join(parts)


def render_effects_filter(text: Any) -> Markup:
    """Jinja2 filter to highlight status effects, damage types, and numerical values."""
    if not text:
        return Markup("")

    text_str = str(text)
    escaped_text = html.escape(text_str)

    if EFFECTS_PATTERN:
        def repl(m: re.Match) -> str:
            name = m.group(1)
            desc = EFFECTS_DATA.get(name, "")
            escaped_name = html.escape(name, quote=True)
            escaped_desc = html.escape(desc, quote=True)
            escaped_id = html.escape(EFFECT_IDS_BY_NAME.get(name, effect_id(name)), quote=True)
            desc_lower = desc.lower()
            if "debuff" in desc_lower:
                eff_type = "debuff"
            elif "buff" in desc_lower:
                eff_type = "buff"
            else:
                eff_type = "effect"
            return f'<span class="effect-trigger effect-{eff_type}" data-effect-id="{escaped_id}" data-effect="{escaped_name}" data-type="{eff_type}" data-desc="{escaped_desc}" tabindex="0">{name}</span>'

        result = EFFECTS_PATTERN.sub(repl, escaped_text)
    else:
        result = escaped_text

    result = format_rich_text(result)
    return Markup(result)


FORT_SKILL_ALIASES: dict[str, str] = {
    "medical contigency": "medical contingency",
    "pre-op preparation": "surgical preparation",
    "pre op preparation": "surgical preparation",
    "unyielding chi": "grand aura",
    "sweet stockpile": "sweets stockpile",
    "reliable cover fire": "reliable cover",
    "absolute mental defence": "absolute mental defense",
    "silent breakthrough": "joint breakthrough",
    "makeup organisation": "makeup organization",
    "annihilation star": "morte lumina",
}


def normalize_skill_name(s: str) -> str:
    return s.strip().lower().replace("-", " ").replace("’", "'")


def enrich_doll_fortifications(doll: dict) -> None:
    """Attach skill icons to each fortification item based on skill name match."""
    # Keep source upgrades separate from the base description; never guess a rewrite.
    for skill in doll.get("skills", []):
        name = normalize_skill_name(skill.get("name", ""))
        name = FORT_SKILL_ALIASES.get(name, name)
        skill["level_upgrades"] = []
        for fort in doll.get("fortification", []):
            target = normalize_skill_name(fort.get("skill", ""))
            target = FORT_SKILL_ALIASES.get(target, target)
            if name and name == target and str(fort.get("level")) in {"2", "3"}:
                skill["level_upgrades"].append(fort)
        skill["level_upgrades"].sort(key=lambda item: (int(item["level"]), int(item["tier"])))
    skill_map: dict[str, str] = {}
    for s in doll.get("skills", []):
        if s.get("name") and s.get("icon"):
            skill_map[normalize_skill_name(s["name"])] = s["icon"]
    for sm in doll.get("summons", []):
        for s in sm.get("skills", []):
            if s.get("name") and s.get("icon"):
                skill_map[normalize_skill_name(s["name"])] = s["icon"]

    for fort in doll.get("fortification", []):
        raw_name = fort.get("skill", "")
        norm = normalize_skill_name(raw_name)
        target = FORT_SKILL_ALIASES.get(norm, norm)
        icon = skill_map.get(target)
        if not icon:
            for k, ic in skill_map.items():
                if k in target or target in k:
                    icon = ic
                    break
        fort["skill_icon"] = icon


def load_data() -> tuple[list[dict], list[dict], list[dict]]:
    """Load and sort characters, weapons, and FAQ entries."""
    char_dir = DATA_DIR / "characters"
    dolls = []
    if char_dir.exists():
        for p in sorted(char_dir.glob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                enrich_doll_fortifications(data)
                dolls.append(data)
            except Exception as e:
                print(f"Warning: Failed to parse {p.name}: {e}")

    # Sort dolls alphabetically by name
    dolls.sort(key=lambda d: d.get("name", "").lower())

    # Weapons
    weapons_file = DATA_DIR / "weapons.json"
    weapons = []
    if weapons_file.exists():
        try:
            weapons = json.loads(weapons_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to parse weapons.json: {e}")

    # Sort weapons: SSR first, then SR, then R, then by name
    rarity_order = {"SSR": 0, "SR": 1, "R": 2}
    weapons.sort(key=lambda w: (rarity_order.get(w.get("rarity", ""), 9), w.get("name", "").lower()))

    # Enrich dolls with signature weapon image path for template rendering
    weapon_name_to_img: dict[str, str] = {}
    for w in weapons:
        img = (w.get("images") or {}).get("weapon", "")
        name = (w.get("name") or "").strip()
        slug = (w.get("slug") or "").strip()
        if name and img:
            weapon_name_to_img[name.lower()] = img
        if slug and img:
            weapon_name_to_img[slug.lower()] = img

    for d in dolls:
        sig = (d.get("signature_weapon") or "").strip()
        d["sig_weapon_image"] = weapon_name_to_img.get(sig.lower(), "")

    # FAQ
    faq_file = DATA_DIR / "faq.json"
    faq_entries = []
    if faq_file.exists():
        try:
            faq_entries = json.loads(faq_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to parse faq.json: {e}")

    return dolls, weapons, faq_entries


ALLOWED_GUIDE_TAGS = {"b", "strong", "i", "em", "u", "span", "code", "br", "a", "p", "ul", "ol", "li", "img"}
ALLOWED_GUIDE_ATTRS = {"class", "href", "target", "rel", "title", "src", "alt", "loading", "data-effect", "data-type", "data-desc", "tabindex"}
ALLOWED_GUIDE_CLASSES = {
    "guide-text-red", "guide-text-orange", "guide-text-blue", "guide-text-green",
    "guide-text-burn", "guide-text-electric", "guide-text-hydro", "guide-text-corrosion",
    "guide-text-physical", "guide-text-freeze", "guide-text-resonance",
    "guide-highlight-yellow", "guide-highlight-green", "guide-highlight-blue", "guide-highlight-pink",
    "guide-font-small", "guide-font-large", "guide-font-xlarge",
    "guide-align-left", "guide-align-center", "guide-align-right",
    "guide-inline-ref", "guide-inline-character", "guide-inline-weapon",
    "guide-inline-skill", "guide-inline-effect", "guide-inline-icon",
    "guide-ref-popover", "guide-weapon-popover", "guide-weapon-popover-image",
    "guide-weapon-popover-name", "guide-weapon-popover-desc",
    "guide-skill-popover", "guide-skill-popover-name", "guide-skill-popover-desc",
    "effect-trigger", "effect-buff", "effect-debuff", "effect-effect",
}


def is_safe_guide_image_src(value: str) -> bool:
    return bool(re.fullmatch(r"(?:(?:\.\./)+|\./|/)?assets/images/[^<>]+", value.strip(), re.IGNORECASE))


class GuideHTMLSanitizer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ALLOWED_GUIDE_TAGS:
            safe_attrs = []
            for k, v in attrs:
                k_lower = k.lower()
                if k_lower.startswith("on"):
                    continue
                if k_lower == "href" and (v.strip().lower().startswith("javascript:") or v.strip().lower().startswith("data:") or v.strip().lower().startswith("vbscript:")):
                    continue
                if k_lower == "src" and not is_safe_guide_image_src(v):
                    continue
                if k_lower == "class":
                    safe_classes = [name for name in v.split() if name in ALLOWED_GUIDE_CLASSES]
                    if safe_classes:
                        safe_attrs.append(f'class="{html.escape(" ".join(safe_classes))}"')
                elif k_lower in ALLOWED_GUIDE_ATTRS or k_lower.startswith("data-"):
                    safe_attrs.append(f'{k}="{html.escape(v)}"')
            attr_str = (" " + " ".join(safe_attrs)) if safe_attrs else ""
            self.result.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag):
        if tag.lower() in ALLOWED_GUIDE_TAGS and tag.lower() not in {"br", "img"}:
            self.result.append(f"</{tag}>")

    def handle_data(self, data):
        self.result.append(html.escape(data))

    def handle_entityref(self, name):
        self.result.append(f"&{name};")

    def handle_charref(self, name):
        self.result.append(f"&#{name};")

    def get_html(self):
        return "".join(self.result)


def sanitize_guide_html(html_str: str) -> str:
    if not html_str:
        return ""
    sanitizer = GuideHTMLSanitizer()
    sanitizer.feed(html_str)
    return sanitizer.get_html()


def load_guides(dolls: list[dict]) -> list[dict]:
    """Load guides from data/guides/*.json. Fails build if any guide fails to parse."""
    guides_dir = DATA_DIR / "guides"
    guides = []
    if not guides_dir.exists():
        return guides
    for p in sorted(guides_dir.glob("*.json")):
        if p.name.startswith("."):
            continue
        try:
            g = json.loads(p.read_text(encoding="utf-8"))
            for block in g.get("blocks", []):
                if block.get("type") == "paragraph" and "html" in block:
                    block["html"] = sanitize_guide_html(block["html"])
                elif block.get("type") == "table":
                    block["rows"] = [
                        [sanitize_guide_html(cell) for cell in row]
                        for row in block.get("rows", [])
                    ]
            guides.append(g)
        except Exception as e:
            raise RuntimeError(f"Failed to parse guide {p.name}: {e}") from e
    return guides




def copy_static_assets(output_dir: Path) -> None:
    """Copy assets/ and site/static/ to output_dir/."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy site/static -> output_dir/static
    dist_static = output_dir / "static"
    if dist_static.exists():
        shutil.rmtree(dist_static)
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, dist_static, ignore=shutil.ignore_patterns("effects-data.js"))

    # Copy assets -> output_dir/assets (excluding huge raw dumps and LangPackage)
    dist_assets = output_dir / "assets"
    if dist_assets.exists():
        shutil.rmtree(dist_assets)
    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, dist_assets, ignore=shutil.ignore_patterns("raw", "*LangPackage*"))

    print(f"Static assets copied to {output_dir.name}/.")


def generate_search_index(dolls: list[dict], weapons: list[dict], guides: list[dict] | None = None, output_dir: Path = DIST_DIR) -> None:
    """Generate search-index.json in output_dir for client-side search."""
    guides = guides or []
    search_records = []

    for d in dolls:
        search_records.append({
            "name": d.get("name", ""),
            "slug": d.get("slug", ""),
            "category": "doll",
            "class": d.get("class", ""),
            "rarity": d.get("rarity", ""),
            "phase": d.get("phase", ""),
            "weapon_type": d.get("weapon_type", ""),
            "server": (d.get("server") or "global").lower(),
            "url": f"characters/{d.get('slug')}.html",
            "image": f"assets/images/characters/{d.get('slug')}/portrait.png"
        })

    for w in weapons:
        search_records.append({
            "name": w.get("name", ""),
            "slug": w.get("slug", ""),
            "category": "weapon",
            "rarity": w.get("rarity", ""),
            "weapon_type": w.get("weapon_type", ""),
            "server": (w.get("server") or "global").lower(),
            "url": f"weapons/{w.get('slug')}.html",
            "image": w.get("images", {}).get("weapon", "")
        })

    doll_server_map = {d.get("slug"): (d.get("server") or "global").lower() for d in dolls}
    for g in guides:
        char_server = doll_server_map.get(g.get("char_slug"), "global")
        search_records.append({
            "name": g.get("title", ""),
            "slug": g.get("slug", ""),
            "category": "guide",
            "char_slug": g.get("char_slug", ""),
            "server": char_server,
            "url": f"guides/{g.get('slug')}.html",
        })


    out_file = output_dir / "search-index.json"
    out_file.write_text(json.dumps(search_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated search index with {len(search_records)} entries.")


def generate_sitemap(rendered_pages: list[str], output_dir: Path, site_url: str) -> None:
    """Generate sitemap.xml listing all rendered public pages."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = []
    for page in sorted(rendered_pages):
        loc = f"{site_url}/{page}"
        priority = "1.0" if page == "index.html" else ("0.8" if page.endswith("index.html") else "0.6")
        changefreq = "weekly"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"\n".join(urls)}
</urlset>
"""
    (output_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    print(f"Generated sitemap.xml with {len(rendered_pages)} pages.")


def generate_robots_txt(output_dir: Path, site_url: str) -> None:
    """Generate robots.txt referencing the sitemap."""
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {site_url}/sitemap.xml
"""
    (output_dir / "robots.txt").write_text(robots_content, encoding="utf-8")
    print("Generated robots.txt.")


def _safe_swap_dist(staging_dir: Path, target_dir: Path) -> None:

    """Safely replace target_dir with staging_dir on Windows/POSIX."""
    target_dir = target_dir.resolve()
    if not (target_dir == DIST_DIR.resolve() or target_dir.is_relative_to(ROOT)):
        raise ValueError(f"Target dir {target_dir} is not inside project root")

    backup_dir = target_dir.parent / f".{target_dir.name}_backup"
    if backup_dir.exists():
        shutil.rmtree(backup_dir, ignore_errors=True)

    if target_dir.exists():
        target_dir.rename(backup_dir)

    try:
        staging_dir.rename(target_dir)
    except Exception:
        if backup_dir.exists() and not target_dir.exists():
            backup_dir.rename(target_dir)
        raise
    finally:
        if backup_dir.exists():
            shutil.rmtree(backup_dir, ignore_errors=True)


def build_site(output_dir: Path | None = None) -> int:
    """Main build entry point. Supports custom output_dir for isolated testing."""
    print("=== GFL2: Exilium Wiki — Static Site Builder ===")

    # 1. Validation check
    print("\n[1/5] Validating data files...")
    if validate_all() != 0:
        print("Build aborted due to validation errors.")
        return 1

    is_custom_output = output_dir is not None
    final_dir = (output_dir or DIST_DIR).resolve()

    if is_custom_output:
        target_dir = final_dir
        target_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Build into staging directory first for atomic swap
        target_dir = ROOT / ".dist_staging"
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        target_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 2. Load data
        print(f"\n[2/5] Loading data records...")
        dolls, weapons, faq_entries = load_data()
        guides = load_guides(dolls)
        load_effects()
        print(f"Loaded: {len(dolls)} dolls, {len(weapons)} weapons, {len(faq_entries)} FAQ entries, {len(guides)} guides.")

        # 3. Copy static assets & generate effects js
        print(f"\n[3/5] Copying static assets...")
        copy_static_assets(target_dir)
        generate_effects_js(target_dir / "static" / "js" / "effects-data.js")

        # 4. Setup Jinja2 Environment
        print("\n[4/5] Rendering Jinja2 templates...")
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )
        env.filters["render_effects"] = render_effects_filter
        asset_inputs = (
            STATIC_DIR / "css" / "style.css",
            STATIC_DIR / "css" / "readability.css",
            STATIC_DIR / "js" / "search.js",
            STATIC_DIR / "js" / "i18n-vi.js",
            STATIC_DIR / "js" / "i18n.js",
            DATA_DIR / "effects_vi.json",
        )
        asset_digest = hashlib.sha256()
        for asset_path in asset_inputs:
            asset_digest.update(asset_path.read_bytes())
        env.globals["asset_version"] = asset_digest.hexdigest()[:12]

        # Build lookup dicts for guide rendering
        chars_by_slug = {d.get("slug"): d for d in dolls}
        weapons_by_slug = {w.get("slug"): w for w in weapons}
        guides_by_char = {g.get("char_slug"): g for g in guides if g.get("char_slug")}

        # Subdirectories in target_dir
        (target_dir / "characters").mkdir(parents=True, exist_ok=True)
        (target_dir / "weapons").mkdir(parents=True, exist_ok=True)
        (target_dir / "guides").mkdir(parents=True, exist_ok=True)

        # Mapping from weapon name/slug to doll for signature weapon links
        weapon_to_doll = {}
        for d in dolls:
            if d.get("signature_weapon"):
                sig = d["signature_weapon"].strip().lower()
                weapon_to_doll[sig] = d

        rendered_pages: list[str] = []

        # Render Home (index.html)
        featured_slugs = ["soppo", "loreley", "alva", "ots-14", "voymastina", "klukai"]
        dolls_by_slug = {doll["slug"]: doll for doll in dolls}
        featured_dolls = [dolls_by_slug[slug] for slug in featured_slugs if slug in dolls_by_slug]
        home_tmpl = env.get_template("home.html")
        home_html = home_tmpl.render(
            active_page="home",
            rel_prefix="",
            site_url=SITE_URL,
            canonical_url=f"{SITE_URL}/index.html",
            dolls=dolls,
            weapons=weapons,
            featured_dolls=featured_dolls
        )
        (target_dir / "index.html").write_text(home_html, encoding="utf-8")
        rendered_pages.append("index.html")

        # Render Character Index (characters/index.html)
        char_index_tmpl = env.get_template("character_index.html")
        char_index_html = char_index_tmpl.render(
            active_page="characters",
            rel_prefix="../",
            site_url=SITE_URL,
            canonical_url=f"{SITE_URL}/characters/index.html",
            dolls=dolls
        )
        (target_dir / "characters" / "index.html").write_text(char_index_html, encoding="utf-8")
        rendered_pages.append("characters/index.html")

        # Render Each Character Detail (characters/{slug}.html)
        char_tmpl = env.get_template("character.html")
        for d in dolls:
            char_guide = guides_by_char.get(d["slug"])
            char_html = char_tmpl.render(
                active_page="characters",
                rel_prefix="../",
                site_url=SITE_URL,
                canonical_url=f"{SITE_URL}/characters/{d['slug']}.html",
                doll=d,
                guide=char_guide,
                chars_by_slug=chars_by_slug,
                weapons_by_slug=weapons_by_slug,
            )
            (target_dir / "characters" / f"{d['slug']}.html").write_text(char_html, encoding="utf-8")
            rendered_pages.append(f"characters/{d['slug']}.html")

        # Render Weapons Index (weapons/index.html)
        weapons_index_tmpl = env.get_template("weapons_index.html")
        weapons_index_html = weapons_index_tmpl.render(
            active_page="weapons",
            rel_prefix="../",
            site_url=SITE_URL,
            canonical_url=f"{SITE_URL}/weapons/index.html",
            weapons=weapons
        )
        (target_dir / "weapons" / "index.html").write_text(weapons_index_html, encoding="utf-8")
        rendered_pages.append("weapons/index.html")

        # Render Each Weapon Detail (weapons/{slug}.html)
        weapon_tmpl = env.get_template("weapon.html")
        for w in weapons:
            sig_doll = weapon_to_doll.get(w.get("name", "").strip().lower()) or weapon_to_doll.get(w.get("slug", "").strip().lower())
            weapon_html = weapon_tmpl.render(
                active_page="weapons",
                rel_prefix="../",
                site_url=SITE_URL,
                canonical_url=f"{SITE_URL}/weapons/{w['slug']}.html",
                weapon=w,
                signature_doll=sig_doll
            )
            (target_dir / "weapons" / f"{w['slug']}.html").write_text(weapon_html, encoding="utf-8")
            rendered_pages.append(f"weapons/{w['slug']}.html")

        # Render FAQ (faq.html)
        faq_tmpl = env.get_template("faq.html")
        faq_html = faq_tmpl.render(
            active_page="faq",
            rel_prefix="",
            site_url=SITE_URL,
            canonical_url=f"{SITE_URL}/faq.html",
            faq_entries=faq_entries
        )
        (target_dir / "faq.html").write_text(faq_html, encoding="utf-8")
        rendered_pages.append("faq.html")

        # Render Guides Index (guides/index.html)
        try:
            guides_index_tmpl = env.get_template("guides_index.html")
            guides_index_html = guides_index_tmpl.render(
                active_page="guides",
                rel_prefix="../",
                site_url=SITE_URL,
                canonical_url=f"{SITE_URL}/guides/index.html",
                guides=guides,
                chars_by_slug=chars_by_slug,
            )
            (target_dir / "guides" / "index.html").write_text(guides_index_html, encoding="utf-8")
            rendered_pages.append("guides/index.html")
        except jinja2.TemplateNotFound:
            pass

        # Render Each Guide (guides/{slug}.html)
        guide_tmpl = env.get_template("guide.html")
        for g in guides:
            char_slug = g.get("char_slug", "")
            guide_char = chars_by_slug.get(char_slug)
            guide_html_out = guide_tmpl.render(
                active_page="guides",
                rel_prefix="../",
                site_url=SITE_URL,
                canonical_url=f"{SITE_URL}/guides/{g['slug']}.html",
                guide=g,
                char=guide_char,
                chars_by_slug=chars_by_slug,
                weapons_by_slug=weapons_by_slug,
            )
            (target_dir / "guides" / f"{g['slug']}.html").write_text(guide_html_out, encoding="utf-8")
            rendered_pages.append(f"guides/{g['slug']}.html")
        if guides:
            print(f"Rendered {len(guides)} guide(s) to {target_dir.name}/guides/.")

        # 5. Search Index
        print("\n[5/5] Generating search index...")
        generate_search_index(dolls, weapons, guides, output_dir=target_dir)

        # 6. SEO Assets: sitemap.xml & robots.txt
        print("\nGenerating SEO files (sitemap.xml, robots.txt)...")
        generate_sitemap(rendered_pages, target_dir, SITE_URL)
        generate_robots_txt(target_dir, SITE_URL)

        # Atomic swap if default output
        if not is_custom_output:
            _safe_swap_dist(target_dir, final_dir)

        total_pages = len(rendered_pages)
        print(f"\n✅ Build complete! {total_pages} HTML pages rendered in {final_dir.name}.")

        return 0

    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        if not is_custom_output and target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        return 1


if __name__ == "__main__":
    sys.exit(build_site())
