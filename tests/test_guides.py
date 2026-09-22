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
    GuideTableBlock,
    GuideCharCardBlock,
    GuideWeaponCardBlock,
    GuideSkillRefBlock,
    GuideSummonSkillRefBlock,
    validate_all,
)
from tests.conftest import sanitize_guide_html, load_guides



def test_guides_index_empty_state_and_no_editor_link(built_site: Path):
    """Guides index must not link to local tools/guide-editor, in empty or populated state."""
    guides_index = built_site / "guides" / "index.html"
    assert guides_index.exists(), "guides/index.html must be generated"

    content = guides_index.read_text(encoding="utf-8")
    assert "tools/guide-editor" not in content, "Guide page must not link to local editor"
    if "guide-index-card" in content:
        assert "guide-index-title" in content
    else:
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


def test_sanitize_guide_html_preserves_word_style_lists_and_safe_classes():
    rich_html = (
        '<ul><li><span class="guide-text-red guide-font-large bad-class" '
        'style="position:fixed" onclick="steal()">Important</span></li></ul>'
        '<span class="guide-align-center">Centered</span>'
    )

    cleaned = sanitize_guide_html(rich_html)

    assert "<ul><li>" in cleaned
    assert "guide-text-red" in cleaned
    assert "guide-font-large" in cleaned
    assert "guide-align-center" in cleaned
    assert "bad-class" not in cleaned
    assert "style=" not in cleaned
    assert "onclick=" not in cleaned


def test_sanitize_guide_html_preserves_element_text_colors():
    element_classes = [
        "guide-text-burn",
        "guide-text-electric",
        "guide-text-hydro",
        "guide-text-corrosion",
        "guide-text-physical",
        "guide-text-freeze",
        "guide-text-resonance",
    ]
    rich_html = "".join(
        f'<span class="{class_name}">{class_name}</span>'
        for class_name in element_classes
    )

    cleaned = sanitize_guide_html(rich_html)

    for class_name in element_classes:
        assert f'class="{class_name}"' in cleaned


def test_sanitize_guide_html_preserves_safe_inline_reference_images():
    rich_html = (
        '<a class="guide-inline-ref guide-inline-character bad-class" '
        'href="../characters/ots-14.html" onclick="steal()">'
        '<img class="guide-inline-icon" '
        'src="../assets/images/characters/ots-14/avatar.png" '
        'alt="OTs-14" onerror="steal()">OTs-14</a>'
    )

    cleaned = sanitize_guide_html(rich_html)

    assert 'class="guide-inline-ref guide-inline-character"' in cleaned
    assert 'href="../characters/ots-14.html"' in cleaned
    assert '<img class="guide-inline-icon"' in cleaned
    assert 'src="../assets/images/characters/ots-14/avatar.png"' in cleaned
    assert 'alt="OTs-14"' in cleaned
    assert "bad-class" not in cleaned
    assert "onclick" not in cleaned
    assert "onerror" not in cleaned


def test_sanitize_guide_html_preserves_weapon_and_skill_popover_structure():
    rich_html = (
        '<a class="guide-inline-ref guide-inline-weapon" href="../weapons/capitoline.html">'
        '<img class="guide-inline-icon" src="../assets/images/weapons/Capitoline.png" alt="Capitoline">Capitoline'
        '<span class="guide-ref-popover guide-weapon-popover">'
        '<img class="guide-weapon-popover-image" src="../assets/images/weapons/Capitoline.png" alt="">'
        '<span class="guide-weapon-popover-name">Capitoline</span>'
        '<span class="guide-weapon-popover-desc">Mô tả</span></span></a>'
        '<span class="guide-inline-ref guide-inline-skill" tabindex="0">Kỹ năng'
        '<span class="guide-ref-popover guide-skill-popover">'
        '<span class="guide-skill-popover-name">Kỹ năng</span>'
        '<span class="guide-skill-popover-desc">Mô tả kỹ năng</span></span></span>'
    )

    cleaned = sanitize_guide_html(rich_html)

    for class_name in [
        "guide-ref-popover",
        "guide-weapon-popover",
        "guide-weapon-popover-image",
        "guide-weapon-popover-name",
        "guide-weapon-popover-desc",
        "guide-skill-popover",
        "guide-skill-popover-name",
        "guide-skill-popover-desc",
    ]:
        assert class_name in cleaned


def test_sanitize_guide_html_rejects_unsafe_inline_image_source():
    cleaned = sanitize_guide_html(
        '<img class="guide-inline-icon" src="javascript:alert(1)" alt="bad">'
    )

    assert "javascript:" not in cleaned
    assert '<img class="guide-inline-icon" alt="bad">' in cleaned


def test_sanitize_guide_html_preserves_localized_inline_effect_metadata():
    cleaned = sanitize_guide_html(
        '<span class="guide-inline-ref guide-inline-effect effect-trigger effect-buff" '
        'data-effect-id="effect_glowing_embers" data-effect="Tàn Lửa Rực" data-type="buff" '
        'data-desc="Mô tả tiếng Việt" title="Tàn Lửa Rực: Mô tả tiếng Việt">'
        'Tàn Lửa Rực</span>'
    )

    assert 'class="guide-inline-ref guide-inline-effect effect-trigger effect-buff"' in cleaned
    assert 'data-effect-id="effect_glowing_embers"' in cleaned
    assert 'data-effect="Tàn Lửa Rực"' in cleaned
    assert 'data-type="buff"' in cleaned
    assert 'data-desc="Mô tả tiếng Việt"' in cleaned
    assert 'Tàn Lửa Rực' in cleaned


def test_guide_template_renders_rich_table_cells_as_sanitized_html():
    template = (Path(__file__).resolve().parents[1] / "site" / "templates" / "guide_blocks.html").read_text(encoding="utf-8")

    assert '<div class="guide-paragraph">{{ block.html | safe }}</div>' in template
    assert "{{ cell | safe }}" in template


def test_rich_table_cells_reject_dangerous_html_before_save():
    with pytest.raises(ValidationError):
        GuideTableBlock(
            type="table",
            headers=["Build"],
            rows=[["<img src=x onerror='steal()'>"]],
        )


def test_table_column_widths_are_validated_and_rendered() -> None:
    block = GuideTableBlock(
        type="table",
        headers=["Build", "Notes"],
        rows=[["A", "B"]],
        column_widths=[180, 320],
    )
    assert block.column_widths == [180, 320]

    with pytest.raises(ValidationError):
        GuideTableBlock(
            type="table",
            headers=["Build", "Notes"],
            rows=[["A", "B"]],
            column_widths=[180],
        )

    with pytest.raises(ValidationError):
        GuideTableBlock(
            type="table",
            headers=["Build"],
            rows=[["A"]],
            column_widths=[40],
        )

    template = (Path(__file__).resolve().parents[1] / "site" / "templates" / "guide_blocks.html").read_text(encoding="utf-8")
    assert 'class="guide-table-scroll"' in template
    assert "<colgroup>" in template
    assert "block.column_widths" in template


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
