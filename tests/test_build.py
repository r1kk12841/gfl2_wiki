"""
tests/test_build.py
Verifies static site generation output in dist/.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
CHAR_DIR = ROOT / "data" / "characters"
WEAPONS_FILE = ROOT / "data" / "weapons.json"


def test_core_pages_generated():
    assert (DIST_DIR / "index.html").exists(), "dist/index.html missing"
    assert (DIST_DIR / "characters" / "index.html").exists(), "dist/characters/index.html missing"
    assert (DIST_DIR / "weapons" / "index.html").exists(), "dist/weapons/index.html missing"
    assert (DIST_DIR / "faq.html").exists(), "dist/faq.html missing"
    assert (DIST_DIR / "search-index.json").exists(), "dist/search-index.json missing"


def test_static_assets_copied():
    assert (DIST_DIR / "static" / "css" / "style.css").exists()
    assert (DIST_DIR / "static" / "js" / "search.js").exists()


@pytest.mark.parametrize("char_path", list(CHAR_DIR.glob("*.json")), ids=lambda p: p.stem)
def test_each_character_html_exists(char_path: Path):
    slug = char_path.stem
    html_path = DIST_DIR / "characters" / f"{slug}.html"
    assert html_path.exists(), f"Generated HTML missing for doll: {slug}"

    content = html_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "Status Effects Glossary" not in content, f"Status Effects Glossary still present in {slug}.html"
    data = json.loads(char_path.read_text(encoding="utf-8"))
    assert data["name"] in content


def test_search_index_content():
    idx_path = DIST_DIR / "search-index.json"
    assert idx_path.exists()
    index_data = json.loads(idx_path.read_text(encoding="utf-8"))
    assert isinstance(index_data, list)
    assert len(index_data) >= 64 + 187

    categories = set(item.get("category") for item in index_data)
    assert "doll" in categories
    assert "weapon" in categories


def test_effects_popover_integration():
    andoris_html = DIST_DIR / "characters" / "andoris.html"
    assert andoris_html.exists()
    content = andoris_html.read_text(encoding="utf-8")
    assert "effect-trigger" in content
    assert 'data-effect="Electro-Charge"' in content
    assert 'data-type="debuff"' in content

    css_path = DIST_DIR / "static" / "css" / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    assert ".effect-trigger" in css_content
    assert "#effect-popover" in css_content

    js_path = DIST_DIR / "static" / "js" / "search.js"
    js_content = js_path.read_text(encoding="utf-8")
    assert "initEffectPopovers" in js_content


def test_text_highlighting_and_damage_colors():
    css_path = DIST_DIR / "static" / "css" / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    assert "243, 109, 28" in css_content
    assert ".val-highlight" in css_content
    assert ".dmg-freeze" in css_content
    assert "66, 205, 224" in css_content

    suomi_html = DIST_DIR / "characters" / "suomi.html"
    assert suomi_html.exists()
    suomi_content = suomi_html.read_text(encoding="utf-8")
    assert 'class="dmg-freeze"' in suomi_content
    assert 'class="val-highlight"' in suomi_content


def test_sub_effects_popover():
    effects_js = DIST_DIR / "static" / "js" / "effects-data.js"
    assert effects_js.exists(), "dist/static/js/effects-data.js missing"
    content = effects_js.read_text(encoding="utf-8")
    assert "window.GFL2_EFFECTS" in content
    assert '"sub_effects"' in content

    andoris_html = DIST_DIR / "characters" / "andoris.html"
    assert "effects-data.js" in andoris_html.read_text(encoding="utf-8")

    css_path = DIST_DIR / "static" / "css" / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    assert ".popover-subeffects" in css_content
    assert ".popover-subeffect-mention" in css_content


def test_summon_stat_bar():
    andoris_html = DIST_DIR / "characters" / "andoris.html"
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


def test_andoris_images_remapped():
    andoris_html = DIST_DIR / "characters" / "andoris.html"
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


def test_server_badges_and_filters():
    cn_dolls = {"asteria", "eagletta", "faelynn", "koleda", "mityl", "soppo", "welrod"}
    for p in CHAR_DIR.glob("*.json"):
        cdata = json.loads(p.read_text(encoding="utf-8"))
        expected_server = "cn" if p.stem in cn_dolls else "global"
        assert cdata.get("server") == expected_server, f"Doll {p.stem} has wrong server: {cdata.get('server')}"

    # Characters index has filter and badges
    char_index = (DIST_DIR / "characters" / "index.html").read_text(encoding="utf-8")
    assert 'data-filter="server"' in char_index
    assert 'data-server="global"' in char_index
    assert 'data-server="cn"' in char_index
    assert "badge-server-cn" in char_index
    assert "badge-server-global" in char_index

    # Weapons index has filter and badges
    weapons_index = (DIST_DIR / "weapons" / "index.html").read_text(encoding="utf-8")
    assert 'data-filter="server"' in weapons_index
    assert 'data-server="global"' in weapons_index
    assert 'data-server="cn"' in weapons_index
    assert "badge-server-cn" in weapons_index
    assert "badge-server-global" in weapons_index

    # Detail pages have badges
    asteria_html = (DIST_DIR / "characters" / "asteria.html").read_text(encoding="utf-8")
    assert 'badge-server-cn' in asteria_html
    assert 'data-doll-server="cn"' in asteria_html

    groza_html = (DIST_DIR / "characters" / "groza.html").read_text(encoding="utf-8")
    assert 'badge-server-global' in groza_html
    assert 'data-doll-server="global"' in groza_html

    # Search index includes server
    search_idx = json.loads((DIST_DIR / "search-index.json").read_text(encoding="utf-8"))
    for item in search_idx:
        assert item.get("server") in {"global", "cn"}







