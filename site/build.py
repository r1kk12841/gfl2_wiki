#!/usr/bin/env python3
"""
site/build.py
Static Site Generator for GFL2: Exilium Wiki.
Reads /data/*.json and /assets, renders Jinja2 templates into /dist,
and emits search-index.json for client-side search.
"""

from __future__ import annotations

import html
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

DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
IMAGE_DIR = ROOT / "image"
STATIC_DIR = ROOT / "site" / "static"
TEMPLATES_DIR = ROOT / "site" / "templates"
DIST_DIR = ROOT / "dist"

EFFECTS_DATA: dict[str, str] = {}
EFFECTS_PATTERN: re.Pattern | None = None


def load_effects() -> None:
    """Load effects dictionary from assets/effects.json and build regex."""
    global EFFECTS_DATA, EFFECTS_PATTERN
    effects_file = ASSETS_DIR / "effects.json"
    if effects_file.exists():
        try:
            EFFECTS_DATA = json.loads(effects_file.read_text(encoding="utf-8"))
            sorted_keys = sorted(EFFECTS_DATA.keys(), key=len, reverse=True)
            pattern_str = r'\b(' + '|'.join(re.escape(k) for k in sorted_keys) + r')\b'
            EFFECTS_PATTERN = re.compile(pattern_str)
            print(f"Loaded {len(EFFECTS_DATA)} status effects from assets/effects.json.")
        except Exception as e:
            print(f"Warning: Failed to load effects.json: {e}")


def generate_effects_js() -> None:
    """Generate site/static/js/effects-data.js with dual-language effects data and sub-effect relationships."""
    effects_vi_file = DATA_DIR / "effects_vi.json"
    effects_file = ASSETS_DIR / "effects.json"

    if effects_vi_file.exists():
        try:
            data = json.loads(effects_vi_file.read_text(encoding="utf-8"))
            js_dir = STATIC_DIR / "js"
            js_dir.mkdir(parents=True, exist_ok=True)
            out_file = js_dir / "effects-data.js"
            out_file.write_text(f"// Auto-generated GFL2 dual-language effects database\nwindow.GFL2_EFFECTS = {json.dumps(data, ensure_ascii=False, indent=2)};\n", encoding="utf-8")
            print(f"Generated {out_file.name} with {len(data)} dual-index effect entries.")
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

            data[name] = {
                "desc": desc,
                "type": eff_type,
                "sub_effects": subs
            }

        js_dir = STATIC_DIR / "js"
        js_dir.mkdir(parents=True, exist_ok=True)
        out_file = js_dir / "effects-data.js"
        out_file.write_text(f"// Auto-generated GFL2 effects database\nwindow.GFL2_EFFECTS = {json.dumps(data, ensure_ascii=False, indent=2)};\n", encoding="utf-8")
        print(f"Generated {out_file.name} with {len(data)} effect entries.")
    except Exception as e:
        print(f"Warning: Failed to generate effects-data.js: {e}")



# Damage types regex mapping to Dandegate colors
DMG_PATTERNS = [
    (re.compile(r'\b(Freeze\s+[Dd]amage)\b'), 'dmg-freeze'),
    (re.compile(r'\b(Burn\s+[Dd]amage)\b'), 'dmg-burn'),
    (re.compile(r'\b(Corrosion\s+[Dd]amage)\b'), 'dmg-corrosion'),
    (re.compile(r'\b(Hydro\s+[Dd]amage)\b'), 'dmg-hydro'),
    (re.compile(r'\b(Electric\s+[Dd]amage)\b'), 'dmg-electric'),
    (re.compile(r'\b(Physical\s+[Dd]amage)\b'), 'dmg-physical'),
    (re.compile(r'\b([Ff]ixed\s+[Dd]amage|[Rr]eal\s+[Dd]amage)\b'), 'dmg-fixed'),
    (re.compile(r'\b([Ss]tability\s+[Dd]amage)\b'), 'dmg-stability'),
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
            desc_lower = desc.lower()
            if "debuff" in desc_lower:
                eff_type = "debuff"
            elif "buff" in desc_lower:
                eff_type = "buff"
            else:
                eff_type = "effect"
            return f'<span class="effect-trigger effect-{eff_type}" data-effect="{escaped_name}" data-type="{eff_type}" data-desc="{escaped_desc}" tabindex="0">{name}</span>'

        result = EFFECTS_PATTERN.sub(repl, escaped_text)
    else:
        result = escaped_text

    result = format_rich_text(result)
    return Markup(result)


def load_data() -> tuple[list[dict], list[dict], list[dict]]:
    """Load and sort characters, weapons, and FAQ entries."""
    char_dir = DATA_DIR / "characters"
    dolls = []
    if char_dir.exists():
        for p in sorted(char_dir.glob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
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

    # FAQ
    faq_file = DATA_DIR / "faq.json"
    faq_entries = []
    if faq_file.exists():
        try:
            faq_entries = json.loads(faq_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to parse faq.json: {e}")

    return dolls, weapons, faq_entries


def load_guides(dolls: list[dict]) -> list[dict]:
    """Load guides from data/guides/*.json."""
    guides_dir = DATA_DIR / "guides"
    guides = []
    if not guides_dir.exists():
        return guides
    for p in sorted(guides_dir.glob("*.json")):
        try:
            g = json.loads(p.read_text(encoding="utf-8"))
            guides.append(g)
        except Exception as e:
            print(f"Warning: Failed to parse guide {p.name}: {e}")
    return guides



def copy_static_assets() -> None:
    """Copy assets/, image/, and site/static/ to dist/."""
    # Ensure dist exists
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # Copy site/static -> dist/static
    dist_static = DIST_DIR / "static"
    if dist_static.exists():
        shutil.rmtree(dist_static)
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, dist_static)

    # Copy assets -> dist/assets (excluding huge raw dumps)
    dist_assets = DIST_DIR / "assets"
    if dist_assets.exists():
        shutil.rmtree(dist_assets)
    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, dist_assets, ignore=shutil.ignore_patterns("raw", "*LangPackage*"))

    # Copy image -> dist/image
    dist_image = DIST_DIR / "image"
    if dist_image.exists():
        shutil.rmtree(dist_image)
    if IMAGE_DIR.exists():
        shutil.copytree(IMAGE_DIR, dist_image)

    print("Static assets copied to dist/.")


def generate_search_index(dolls: list[dict], weapons: list[dict], guides: list[dict] | None = None) -> None:
    """Generate dist/search-index.json for client-side search."""
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

    for g in guides:
        search_records.append({
            "name": g.get("title", ""),
            "slug": g.get("slug", ""),
            "category": "guide",
            "char_slug": g.get("char_slug", ""),
            "url": f"guides/{g.get('slug')}.html",
        })


    out_file = DIST_DIR / "search-index.json"
    out_file.write_text(json.dumps(search_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated search index with {len(search_records)} entries.")


def build_site() -> int:
    """Main build entry point."""
    print("=== GFL2: Exilium Wiki — Static Site Builder ===")

    # 1. Validation check
    print("\n[1/5] Validating data files...")
    if validate_all() != 0:
        print("Build aborted due to validation errors.")
        return 1

    # 2. Load data
    print(f"\n[2/5] Loading data records...")
    dolls, weapons, faq_entries = load_data()
    guides = load_guides(dolls)
    load_effects()
    generate_effects_js()
    print(f"Loaded: {len(dolls)} dolls, {len(weapons)} weapons, {len(faq_entries)} FAQ entries, {len(guides)} guides.")

    # 3. Copy static assets
    print("\n[3/5] Copying static assets...")
    copy_static_assets()

    # 4. Setup Jinja2 Environment
    print("\n[4/5] Rendering Jinja2 templates...")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=jinja2.select_autoescape(["html", "xml"])
    )
    env.filters["render_effects"] = render_effects_filter

    # Build lookup dicts for guide rendering
    chars_by_slug = {d.get("slug"): d for d in dolls}
    weapons_by_slug = {w.get("slug"): w for w in weapons}

    # Subdirectories in dist
    (DIST_DIR / "characters").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "weapons").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "guides").mkdir(parents=True, exist_ok=True)

    # Mapping from weapon name/slug to doll for signature weapon links
    weapon_to_doll = {}
    for d in dolls:
        if d.get("signature_weapon"):
            sig = d["signature_weapon"].strip().lower()
            weapon_to_doll[sig] = d

    # Render Home (index.html)
    home_tmpl = env.get_template("home.html")
    home_html = home_tmpl.render(
        active_page="home",
        rel_prefix="",
        dolls=dolls,
        weapons=weapons,
        featured_dolls=dolls[:8]
    )
    (DIST_DIR / "index.html").write_text(home_html, encoding="utf-8")

    # Render Character Index (characters/index.html)
    char_index_tmpl = env.get_template("character_index.html")
    char_index_html = char_index_tmpl.render(
        active_page="characters",
        rel_prefix="../",
        dolls=dolls
    )
    (DIST_DIR / "characters" / "index.html").write_text(char_index_html, encoding="utf-8")

    # Render Each Character Detail (characters/{slug}.html)
    char_tmpl = env.get_template("character.html")
    for d in dolls:
        char_html = char_tmpl.render(
            active_page="characters",
            rel_prefix="../",
            doll=d
        )
        (DIST_DIR / "characters" / f"{d['slug']}.html").write_text(char_html, encoding="utf-8")

    # Render Weapons Index (weapons/index.html)
    weapons_index_tmpl = env.get_template("weapons_index.html")
    weapons_index_html = weapons_index_tmpl.render(
        active_page="weapons",
        rel_prefix="../",
        weapons=weapons
    )
    (DIST_DIR / "weapons" / "index.html").write_text(weapons_index_html, encoding="utf-8")

    # Render Each Weapon Detail (weapons/{slug}.html)
    weapon_tmpl = env.get_template("weapon.html")
    for w in weapons:
        sig_doll = weapon_to_doll.get(w.get("name", "").strip().lower()) or weapon_to_doll.get(w.get("slug", "").strip().lower())
        weapon_html = weapon_tmpl.render(
            active_page="weapons",
            rel_prefix="../",
            weapon=w,
            signature_doll=sig_doll
        )
        (DIST_DIR / "weapons" / f"{w['slug']}.html").write_text(weapon_html, encoding="utf-8")

    # Render FAQ (faq.html)
    faq_tmpl = env.get_template("faq.html")
    faq_html = faq_tmpl.render(
        active_page="faq",
        rel_prefix="",
        faq_entries=faq_entries
    )
    (DIST_DIR / "faq.html").write_text(faq_html, encoding="utf-8")

    # Render Guides Index (guides/index.html)
    try:
        guides_index_tmpl = env.get_template("guides_index.html")
        guides_index_html = guides_index_tmpl.render(
            active_page="guides",
            rel_prefix="../",
            guides=guides,
            chars_by_slug=chars_by_slug,
        )
        (DIST_DIR / "guides" / "index.html").write_text(guides_index_html, encoding="utf-8")
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
            guide=g,
            char=guide_char,
            chars_by_slug=chars_by_slug,
            weapons_by_slug=weapons_by_slug,
        )
        (DIST_DIR / "guides" / f"{g['slug']}.html").write_text(guide_html_out, encoding="utf-8")
    if guides:
        print(f"Rendered {len(guides)} guide(s) to dist/guides/.")

    # 5. Search Index
    print("\n[5/5] Generating search index...")
    generate_search_index(dolls, weapons, guides)

    total_pages = 1 + 1 + len(dolls) + 1 + len(weapons) + 1 + len(guides)
    print(f"\n✅ Build complete! {total_pages} HTML pages rendered in /dist.")
    return 0


if __name__ == "__main__":
    sys.exit(build_site())
