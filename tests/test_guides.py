"""Tests for Guides system hardening, validation schema, HTML sanitization, and CSS properties."""
import json
from pathlib import Path
import pytest
from pydantic import ValidationError

from tools.validate import (
    Guide,
    GuideHeadingBlock,
    GuideParagraphBlock,
    GuideLinkBlock,
    GuideCharCardBlock,
    GuideWeaponCardBlock,
    GuideSkillRefBlock,
    GuideSummonSkillRefBlock,
    validate_all,
)
from tests.conftest import sanitize_guide_html, load_guides



def test_guides_index_empty_state_and_no_editor_link(built_site: Path):
    """Empty state must not link to local tools/guide-editor."""
    guides_index = built_site / "guides" / "index.html"
    assert guides_index.exists(), "guides/index.html must be generated"

    content = guides_index.read_text(encoding="utf-8")
    assert "tools/guide-editor" not in content, "Empty state must not link to local editor"
    assert "data-i18n=\"guides_empty\"" in content or "No guides yet" in content


def test_valid_guide_model():
    """A well-formed guide passes validation."""
    valid_guide_data = {
        "slug": "groza-starter-guide",
        "title": "Groza Starter Guide",
        "char_slug": "groza",
        "last_updated": "2026-09-07",
        "author": "Commander",
        "blocks": [
            {"type": "heading", "level": 2, "text": "Overview"},
            {"type": "paragraph", "html": "Groza is an <b>excellent</b> Assault Rifle doll."},
            {"type": "char_card", "slug": "groza"},
            {"type": "weapon_card", "slug": "alps"},
            {"type": "skill_ref", "char": "groza", "skill_idx": 0},
            {"type": "link", "url": "https://example.com/guide", "text": "Community Guide"},
        ],
    }
    guide = Guide.model_validate(valid_guide_data)
    assert guide.slug == "groza-starter-guide"
    assert len(guide.blocks) == 6


def test_invalid_block_type_rejected():
    """Unknown block types must be rejected by the discriminator schema."""
    invalid_data = {
        "slug": "bad-guide",
        "title": "Bad Guide",
        "blocks": [
            {"type": "unsupported_block", "foo": "bar"},
        ],
    }
    with pytest.raises(ValidationError):
        Guide.model_validate(invalid_data)


def test_invalid_heading_level_rejected():
    """Heading levels must be 1 through 6."""
    with pytest.raises(ValidationError):
        GuideHeadingBlock(type="heading", level=7, text="Too Deep")
    with pytest.raises(ValidationError):
        GuideHeadingBlock(type="heading", level=0, text="Zero Level")


def test_dangerous_paragraph_html_rejected_by_validator():
    """Paragraph HTML with script tags or handlers must be rejected by validator."""
    with pytest.raises(ValidationError):
        GuideParagraphBlock(type="paragraph", html="<script>alert(1)</script>")

    with pytest.raises(ValidationError):
        GuideParagraphBlock(type="paragraph", html="<img src=x onerror='steal()'>")


def test_sanitize_guide_html_strips_dangerous_elements():
    """Sanitizer escapes or drops dangerous tags and event handlers."""
    dirty_html = '<p>Safe <b>bold</b> text <script>alert("hack")</script><a href="javascript:alert(1)">bad link</a></p>'
    cleaned = sanitize_guide_html(dirty_html)
    assert "<script" not in cleaned
    assert "javascript:" not in cleaned
    assert "<b>bold</b>" in cleaned


def test_corrupted_guide_file_fails_load_guides(tmp_path: Path):
    """If a guide file contains corrupted JSON, load_guides must raise RuntimeError."""
    guides_dir = tmp_path / "data" / "guides"
    guides_dir.mkdir(parents=True)
    (guides_dir / "broken.json").write_text("{ broken json content", encoding="utf-8")

    # Temporarily point DATA_DIR
    import sys
    site_build = sys.modules["gfl2_site_builder"]
    orig_data_dir = site_build.DATA_DIR
    try:
        site_build.DATA_DIR = tmp_path / "data"
        with pytest.raises(RuntimeError) as exc_info:
            load_guides([])
        assert "broken.json" in str(exc_info.value)
    finally:
        site_build.DATA_DIR = orig_data_dir


def test_style_css_has_no_undefined_guide_variables(built_site: Path):
    """CSS should use canonical tokens (--bg-surface, etc.) rather than undefined variables."""
    css_file = built_site / "static" / "css" / "style.css"
    content = css_file.read_text(encoding="utf-8")

    # Ensure bare undefined variables are not present in guide styles
    assert "var(--surface)" not in content, "var(--surface) should be replaced with var(--bg-surface)"
    assert "var(--surface-hover)" not in content, "var(--surface-hover) should be replaced with var(--bg-card-hover)"
    assert "var(--border)" not in content, "var(--border) should be replaced with var(--border-subtle)"
    assert "var(--radius)" not in content, "var(--radius) should be replaced with var(--radius-md)"
