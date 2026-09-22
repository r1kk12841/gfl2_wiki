"""Tests for Character Detail Tab Navigation (Information & Guide tabs)."""
import json
from pathlib import Path
import pytest


def test_character_page_has_tabs_and_panes(built_site: Path):
    """Character page must have tab navigation bar and two tab panes."""
    char_file = built_site / "characters" / "groza.html"
    assert char_file.exists(), "groza.html must exist"

    html = char_file.read_text(encoding="utf-8")

    # Tab navigation bar
    assert 'class="char-tabs-nav"' in html, "char-tabs-nav must be present"
    assert 'data-tab="info"' in html, "Info tab must be present"
    assert 'data-tab="guide"' in html, "Guide tab must be present"
    assert 'data-i18n="tab_info"' in html
    assert 'data-i18n="tab_guide"' in html

    # Tab panes
    assert 'id="tab-pane-info"' in html, "#tab-pane-info must exist"
    assert 'id="tab-pane-guide"' in html, "#tab-pane-guide must exist"

    # Skills section must be present inside page
    assert 'data-i18n="skills_section_title"' in html

    # Since groza has no guide file yet, empty state should be rendered in guide pane
    assert 'class="guide-empty-state"' in html
    assert 'data-i18n="guide_empty_title"' in html
    assert 'data-i18n="guide_empty_desc"' in html


def test_i18n_tab_keys():
    """Verify that translation files and character template have tab keys."""
    i18n_vi_json_path = Path("data/i18n_vi.json")
    i18n_vi_js_path = Path("site/static/js/i18n-vi.js")
    char_template_path = Path("site/templates/character.html")

    assert i18n_vi_json_path.exists()
    assert i18n_vi_js_path.exists()
    assert char_template_path.exists()

    vi_json = json.loads(i18n_vi_json_path.read_text(encoding="utf-8"))
    vi_js_content = i18n_vi_js_path.read_text(encoding="utf-8")
    tmpl_content = char_template_path.read_text(encoding="utf-8")

    keys = ["tab_info", "tab_guide", "guide_empty_title", "guide_empty_desc", "guide_last_updated"]
    for key in keys:
        assert key in vi_json["ui"], f"Missing {key} in data/i18n_vi.json"
        assert f'"{key}"' in vi_js_content, f"Missing {key} in site/static/js/i18n-vi.js"

    # Verify template contains hooks for tab keys
    assert 'data-i18n="tab_info"' in tmpl_content
    assert 'data-i18n="tab_guide"' in tmpl_content
    assert 'data-i18n="guide_empty_title"' in tmpl_content
    assert 'data-i18n="guide_empty_desc"' in tmpl_content


def test_character_page_renders_guide_when_available(tmp_path: Path):
    """When a guide JSON exists for a character, its blocks must be rendered in #tab-pane-guide."""
    import sys
    site_build = sys.modules["gfl2_site_builder"]
    build_site = site_build.build_site

    guides_dir = site_build.DATA_DIR / "guides"
    test_guide_path = guides_dir / "test-groza-guide.json"
    guide_data = {
        "slug": "test-groza-guide",
        "title": "Test Groza Combat Guide",
        "char_slug": "groza",
        "last_updated": "2026-09-14",
        "author": "Commander",
        "blocks": [
            {"type": "heading", "level": 2, "text": "Groza Combat Strategy"},
            {"type": "paragraph", "html": "Groza provides strong tactical firepower."},
            {"type": "char_card", "slug": "groza"},
        ],
    }

    try:
        test_guide_path.write_text(json.dumps(guide_data), encoding="utf-8")
        out_dir = tmp_path / "dist"
        rc = build_site(output_dir=out_dir)
        assert rc == 0 or rc is None

        groza_html = (out_dir / "characters" / "groza.html").read_text(encoding="utf-8")

        # Check guide content rendered in groza page
        assert "Groza Combat Strategy" in groza_html
        assert "Groza provides strong tactical firepower." in groza_html
        assert 'id="tab-pane-guide"' in groza_html

        # Standalone guide must also render properly
        standalone_guide = (out_dir / "guides" / "test-groza-guide.html").read_text(encoding="utf-8")
        assert "Groza Combat Strategy" in standalone_guide

    finally:
        if test_guide_path.exists():
            test_guide_path.unlink()
