"""
tests/test_build.py
Verifies static site generation output in isolated build directories.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from tests.conftest import build_site

ROOT = Path(__file__).resolve().parent.parent
CHAR_DIR = ROOT / "data" / "characters"
WEAPONS_FILE = ROOT / "data" / "weapons.json"


def test_core_pages_generated(built_site: Path):
    assert (built_site / "index.html").exists(), "dist/index.html missing"
    assert (built_site / "characters" / "index.html").exists(), "dist/characters/index.html missing"
    assert (built_site / "weapons" / "index.html").exists(), "dist/weapons/index.html missing"
    assert (built_site / "faq.html").exists(), "dist/faq.html missing"
    assert (built_site / "guides" / "index.html").exists(), "dist/guides/index.html missing"
    assert (built_site / "search-index.json").exists(), "dist/search-index.json missing"


def test_homepage_branding_balanced_classes_and_featured_dolls(built_site: Path):
    home = (built_site / "index.html").read_text(encoding="utf-8")
    css = (built_site / "static" / "css" / "style.css").read_text(encoding="utf-8")

    assert "GF2: Lưu Đày Wiki Tiếng Việt (beta)" in home
    assert 'class="class-nav-grid"' in home
    assert 'class="class-nav-card"' in home
    assert ".class-nav-grid" in css
    assert ".class-nav-card" in css

    featured_slugs = ["soppo", "loreley", "alva", "ots-14", "voymastina", "klukai"]
    featured_positions = [home.index(f'characters/{slug}.html') for slug in featured_slugs]
    assert featured_positions == sorted(featured_positions)
    assert home.count('class="doll-card ') == len(featured_slugs)


def test_character_quick_filters_use_class_phase_and_ammo_icons():
    template = (ROOT / "site" / "templates" / "character_index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    search_js = (ROOT / "site" / "static" / "js" / "search.js").read_text(encoding="utf-8")

    assert "assets/images/class/{{ cls }}.png" in template
    assert "assets/images/phase/{{ ph }}.png" in template
    for ammo_asset in ["LightAmmo.png", "MediumAmmo.png", "HeavyAmmo.png", "ShotgunAmmo.png", "Melee.png"]:
        assert ammo_asset in template
        assert (ROOT / "assets" / "images" / "ammo" / ammo_asset).exists()

    assert 'data-filter="ammo_type"' in template
    assert 'data-ammo_type="{{ doll.ammo_type }}"' in template
    assert "ammo_type: 'all'" in search_js
    assert ".filter-chip-icon" in css
    for phase in ["physical", "burn", "hydro", "electric", "freeze", "corrosion", "resonance"]:
        assert f".phase-chip.phase-{phase}" in css


def test_static_assets_copied(built_site: Path):
    assert (built_site / "static" / "css" / "style.css").exists()
    assert (built_site / "static" / "js" / "search.js").exists()


@pytest.mark.parametrize("char_path", list(CHAR_DIR.glob("*.json")), ids=lambda p: p.stem)
def test_each_character_html_exists(built_site: Path, char_path: Path):
    slug = char_path.stem
    html_path = built_site / "characters" / f"{slug}.html"
    assert html_path.exists(), f"Generated HTML missing for doll: {slug}"

    content = html_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "Status Effects Glossary" not in content, f"Status Effects Glossary still present in {slug}.html"
    data = json.loads(char_path.read_text(encoding="utf-8"))
    assert data["name"] in content


def test_search_index_content(built_site: Path):
    idx_path = built_site / "search-index.json"
    assert idx_path.exists()
    index_data = json.loads(idx_path.read_text(encoding="utf-8"))
    assert isinstance(index_data, list)
    assert len(index_data) >= 64 + 187

    categories = set(item.get("category") for item in index_data)
    assert "doll" in categories
    assert "weapon" in categories


def test_effects_popover_integration(built_site: Path):
    andoris_html = built_site / "characters" / "andoris.html"
    assert andoris_html.exists()
    content = andoris_html.read_text(encoding="utf-8")
    assert "effect-trigger" in content
    assert 'data-effect="Electro-Charge"' in content
    assert 'data-effect-id="effect_' in content
    assert 'data-type="debuff"' in content

    css_path = built_site / "static" / "css" / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    assert ".effect-trigger" in css_content
    assert "#effect-popover" in css_content

    js_path = built_site / "static" / "js" / "search.js"
    js_content = js_path.read_text(encoding="utf-8")
    assert "initEffectPopovers" in js_content


def test_text_highlighting_and_damage_colors(built_site: Path):
    css_path = built_site / "static" / "css" / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    assert "243, 109, 28" in css_content
    assert ".val-highlight" in css_content
    assert ".dmg-freeze" in css_content
    assert "66, 205, 224" in css_content

    suomi_html = built_site / "characters" / "suomi.html"
    assert suomi_html.exists()
    suomi_content = suomi_html.read_text(encoding="utf-8")
    assert 'class="dmg-freeze"' in suomi_content
    assert 'class="val-highlight"' in suomi_content


def test_sub_effects_popover(built_site: Path):
    effects_js = built_site / "static" / "js" / "effects-data.js"
    assert effects_js.exists(), "dist/static/js/effects-data.js missing"
    content = effects_js.read_text(encoding="utf-8")
    assert "window.GFL2_EFFECTS" in content
    assert '"byId"' in content
    assert '"nameIndex"' in content
    assert '"sub_effect_ids"' in content

    andoris_html = built_site / "characters" / "andoris.html"
    assert "effects-data.js" in andoris_html.read_text(encoding="utf-8")

    css_path = built_site / "static" / "css" / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    assert ".popover-subeffects" in css_content
    assert ".popover-subeffect-mention" in css_content


def test_summon_stat_bar(built_site: Path):
    andoris_html = built_site / "characters" / "andoris.html"
    assert andoris_html.exists()
    content = andoris_html.read_text(encoding="utf-8")
    assert "summon-stats-grid" in content
    assert "Auto-Turret" in content
    assert "50%" in content
    assert "Andoris" in content
    assert '<span class="stat-box-label">HP</span>' in content
    assert '<span class="stat-box-label">ATK</span>' in content
    assert '<span class="stat-box-label">DEF</span>' in content
    assert '<span class="stat-box-label">Stability</span>' in content
    assert '<span class="stat-box-label">Mobility</span>' in content


def test_andoris_images_remapped(built_site: Path):
    andoris_html = built_site / "characters" / "andoris.html"
    assert andoris_html.exists()
    content = andoris_html.read_text(encoding="utf-8")
    assert "assets/images/characters/andoris/avatar.png" in content
    assert "assets/images/characters/andoris/skill1-icon.png" in content
    assert "assets/images/characters/andoris/skill1-range.png" in content
    assert "assets/images/characters/andoris/summon1.png" in content
    assert "assets/images/characters/andoris/summon1-skill1-icon.png" in content
    assert "assets/images/characters/andoris/common.png" in content
    assert "assets/images/characters/andoris/expan.png" in content
    assert "skill-icon-img" in content
    assert "skill-range-img" in content
    assert "summon-unit-img" in content
    assert "key-icon-img" in content
    assert "char-avatar-img" in content


def test_server_badges_and_filters(built_site: Path):
    character_servers = set()
    for p in CHAR_DIR.glob("*.json"):
        cdata = json.loads(p.read_text(encoding="utf-8"))
        server = cdata.get("server")
        assert server in {"global", "cn"}, f"Doll {p.stem} has invalid server: {server}"
        character_servers.add(server)

        # Character data is the source of truth. The generated detail page must
        # follow edits made through the data-entry tool instead of a hard-coded
        # list of dolls assigned to each server.
        detail_html = (built_site / "characters" / f"{p.stem}.html").read_text(encoding="utf-8")
        assert f'badge-server-{server}' in detail_html
        assert f'data-doll-server="{server}"' in detail_html

    assert character_servers == {"global", "cn"}

    # Characters index has filter and badges
    char_index = (built_site / "characters" / "index.html").read_text(encoding="utf-8")
    assert 'data-filter="server"' in char_index
    assert 'data-server="global"' in char_index
    assert 'data-server="cn"' in char_index
    assert "badge-server-cn" in char_index
    assert "badge-server-global" in char_index

    # Weapons index has filter and badges
    weapons_index = (built_site / "weapons" / "index.html").read_text(encoding="utf-8")
    assert 'data-filter="server"' in weapons_index
    assert 'data-server="global"' in weapons_index
    assert 'data-server="cn"' in weapons_index
    assert "badge-server-cn" in weapons_index
    assert "badge-server-global" in weapons_index

    # Search index includes server
    search_idx = json.loads((built_site / "search-index.json").read_text(encoding="utf-8"))
    for item in search_idx:
        assert item.get("server") in {"global", "cn"}


# =========================================================================
# Phase 2 & 3 New Isolation and Quality Tests
# =========================================================================

def test_build_into_custom_output_dir(tmp_path: Path):
    custom_dir = tmp_path / "custom_site"
    res = build_site(output_dir=custom_dir)
    assert res == 0
    assert (custom_dir / "index.html").exists()
    assert (custom_dir / "static" / "js" / "effects-data.js").exists()


def test_build_does_not_modify_site_static():
    static_effects_js = ROOT / "site" / "static" / "js" / "effects-data.js"
    assert not static_effects_js.exists(), "site/static/js/effects-data.js should not exist in source tree"


def test_output_does_not_contain_image_dir(built_site: Path):
    assert not (built_site / "image").exists(), "Ignored root 'image/' directory should not be copied to output"


def test_output_contains_effects_data_js(built_site: Path):
    assert (built_site / "static" / "js" / "effects-data.js").exists()


def test_parallel_independent_builds(tmp_path: Path):
    out1 = tmp_path / "site1"
    out2 = tmp_path / "site2"
    assert build_site(output_dir=out1) == 0
    assert build_site(output_dir=out2) == 0
    assert (out1 / "index.html").exists()
    assert (out2 / "index.html").exists()


def test_all_character_jsons_have_exactly_one_html(built_site: Path):
    char_files = list(CHAR_DIR.glob("*.json"))
    assert len(char_files) > 0
    for cf in char_files:
        html_file = built_site / "characters" / f"{cf.stem}.html"
        assert html_file.exists(), f"Missing HTML for character {cf.stem}"


def test_all_weapon_jsons_have_exactly_one_html(built_site: Path):
    weapons = json.loads(WEAPONS_FILE.read_text(encoding="utf-8"))
    assert len(weapons) > 0
    for w in weapons:
        slug = w["slug"]
        html_file = built_site / "weapons" / f"{slug}.html"
        assert html_file.exists(), f"Missing HTML for weapon {slug}"


def test_all_search_index_urls_exist(built_site: Path):
    idx_path = built_site / "search-index.json"
    records = json.loads(idx_path.read_text(encoding="utf-8"))
    for item in records:
        target = built_site / item["url"]
        assert target.exists(), f"search-index URL does not exist: {item['url']}"


def test_search_index_has_no_duplicate_slugs(built_site: Path):
    idx_path = built_site / "search-index.json"
    records = json.loads(idx_path.read_text(encoding="utf-8"))
    seen_by_cat: dict[str, set[str]] = {}
    for item in records:
        cat = item.get("category", "")
        slug = item.get("slug", "")
        if cat not in seen_by_cat:
            seen_by_cat[cat] = set()
        assert slug not in seen_by_cat[cat], f"Duplicate slug in search-index for category '{cat}': {slug}"
        seen_by_cat[cat].add(slug)


def test_all_character_and_weapon_asset_references_exist_in_output(built_site: Path):
    # Characters
    for p in CHAR_DIR.glob("*.json"):
        cdata = json.loads(p.read_text(encoding="utf-8"))
        images = cdata.get("images", {})
        for img_type, rel_path in images.items():
            if rel_path:
                assert (built_site / rel_path).exists(), f"Character {p.stem} asset missing in output: {rel_path}"

    # Weapons
    weapons = json.loads(WEAPONS_FILE.read_text(encoding="utf-8"))
    for w in weapons:
        weapon_img = w.get("images", {}).get("weapon")
        if weapon_img:
            assert (built_site / weapon_img).exists(), f"Weapon {w.get('slug')} asset missing in output: {weapon_img}"


def test_no_internal_links_to_guide_editor(built_site: Path):
    for html_file in built_site.glob("**/*.html"):
        content = html_file.read_text(encoding="utf-8")
        assert "guide-editor" not in content, f"Internal link to guide-editor found in {html_file.name}"


def test_no_windows_local_paths_in_output(built_site: Path):
    for html_file in built_site.glob("**/*.html"):
        content = html_file.read_text(encoding="utf-8")
        assert "C:\\" not in content, f"Windows local path 'C:\\' found in {html_file.name}"
        assert "D:\\" not in content, f"Windows local path 'D:\\' found in {html_file.name}"
        assert "file:///" not in content, f"file:/// URI found in {html_file.name}"


def test_fortification_skill_icons(built_site: Path):
    import re

    char_files = list(CHAR_DIR.glob("*.json"))
    assert len(char_files) > 0
    img_tag_pattern = re.compile(r'<img\b[^>]*\bclass="[^"]*fort-skill-icon[^"]*"[^>]*>')
    src_pattern = re.compile(r'src="([^"]+)"')

    for cf in char_files:
        html_file = built_site / "characters" / f"{cf.stem}.html"
        assert html_file.exists(), f"Missing HTML for character {cf.stem}"
        content = html_file.read_text(encoding="utf-8")
        tags = img_tag_pattern.findall(content)
        # All characters in the game have 6 fortification tiers
        assert len(tags) == 6, f"{html_file.name} expected 6 fort-skill-icon images, found {len(tags)}"
        for tag in tags:
            m = src_pattern.search(tag)
            assert m, f"No src in img tag: {tag}"
            clean_src = m.group(1).lstrip("../").lstrip("/")
            assert (built_site / clean_src).exists(), f"Skill icon in {html_file.name} not found in output: {clean_src}"


def test_helix_stats_and_materials_removed(built_site: Path):
    char_files = list(CHAR_DIR.glob("*.json"))
    assert len(char_files) > 0

    for cf in char_files:
        html_file = built_site / "characters" / f"{cf.stem}.html"
        assert html_file.exists(), f"Missing HTML for character {cf.stem}"
        content = html_file.read_text(encoding="utf-8")
        assert "data-helix-node" not in content, f"Found neural helix stat node in {html_file.name}"
        assert "Stat Enhancements" not in content, f"Found Stat Enhancements in {html_file.name}"
        assert "data-key-materials" not in content, f"Found data-key-materials in {html_file.name}"
        assert "<th>Materials</th>" not in content, f"Found <th>Materials</th> in {html_file.name}"
