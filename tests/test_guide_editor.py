from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDITOR_DIR = ROOT / "tools" / "guide-editor"


def test_loreley_template_builds_complete_character_guide() -> None:
    script = r"""
const template = require('./tools/guide-editor/template.js');
const guide = template.createLoreleyStyleGuide({
  slug: 'alva',
  name: 'Alva',
  date: '2026-09-14',
});
process.stdout.write(JSON.stringify(guide));
"""
    result = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    guide = json.loads(result.stdout)

    assert guide["slug"] == "alva"
    assert guide["char_slug"] == "alva"
    assert guide["title"].startswith("Hướng dẫn toàn diện Alva")
    assert guide["last_updated"] == "2026-09-14"
    assert guide["author"]
    assert guide["blocks"][1] == {"type": "char_card", "slug": "alva"}
    assert all("id" not in block for block in guide["blocks"])

    headings = [block["text"] for block in guide["blocks"] if block["type"] == "heading"]
    assert headings == [
        "Tổng quan (Overview)",
        "Đột phá & Cung mệnh (Fortifications)",
        "Trang bị Vũ khí (Weapons)",
        "Phụ kiện & Chỉ số (Attachments)",
        "Khóa Cố Định (Fixed Keys)",
        "Khóa Chung & Khóa Hảo Cảm (Common & Affinity Keys)",
        "Dữ liệu Tái Cấu Trúc & Lõi Tăng Trưởng (Remolding Core)",
        "Chu kỳ Kỹ năng (Rotation)",
        "Đội hình đề xuất (Team Compositions)",
        "Tổng kết & Lời khuyên Gacha (Verdict)",
    ]


def test_editor_exposes_fast_template_and_existing_guide_controls() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert 'src="template.js"' in html
    assert 'id="btn-load-existing"' in html
    assert 'id="btn-use-template"' in html
    assert 'id="guide-author"' in html
    assert 'id="guide-date"' in html
    assert "async function loadExistingGuide" in app
    assert "function useLoreleyTemplate" in app
    assert app.count("async function saveGuide()") == 1
    assert app.count("function loadGuide(e)") == 1
    assert "char_slug:" in app
    assert "last_updated:" in app


def test_editor_supports_duplicate_blocks_and_multiline_table_cells() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert "function duplicateBlock" in app
    assert "table-cell-editor" in app
    assert "createRichEditor(row[ci] || ''" in app


def test_table_columns_can_be_resized_and_widths_are_persisted() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    editor_css = (EDITOR_DIR / "style.css").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")

    assert "function normalizeTableColumnWidths" in app
    assert "column_widths" in app
    assert "table-column-resize-handle" in app
    assert "pointerdown" in app
    assert "pointermove" in app
    assert "setPointerCapture" in app
    assert "<colgroup>" in app
    assert "guide-table-scroll" in app
    assert ".table-column-resize-handle" in editor_css
    assert ".guide-table-scroll" in editor_css
    assert ".guide-table-scroll" in site_css
    assert 'href="style.css?v=20260916-table-resize-1"' in html


def test_editor_has_word_style_quick_format_toolbar() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    editor_css = (EDITOR_DIR / "style.css").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")

    for control_id in ["fmt-bold", "fmt-italic", "fmt-underline", "fmt-text-color", "fmt-highlight"]:
        assert f'id="{control_id}"' in html
    assert "function applyQuickFormat" in app
    assert "function rememberEditableSelection" in app
    assert ".format-btn" in editor_css
    assert ".guide-text-red" in site_css
    assert ".guide-highlight-yellow" in site_css


def test_editor_exposes_full_rich_text_toolbar_and_contenteditable_fields() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert 'src="rich-text.js"' in html
    for control_id in [
        "fmt-undo",
        "fmt-redo",
        "fmt-font-size",
        "fmt-align-left",
        "fmt-align-center",
        "fmt-align-right",
        "fmt-ul",
        "fmt-ol",
        "fmt-link",
        "fmt-clear",
    ]:
        assert f'id="{control_id}"' in html

    assert "function createRichEditor" in app
    assert "contenteditable: 'true'" in app
    assert "function handleRichPaste" in app
    assert "sanitizeRichHTML" in app
    assert "function applyRichTextCommand" in app


def test_text_color_menu_exposes_all_game_elements() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    editor_css = (EDITOR_DIR / "style.css").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    rich_text = (EDITOR_DIR / "rich-text.js").read_text(encoding="utf-8")

    elements = {
        "burn": "Thiêu đốt",
        "electric": "Dẫn điện",
        "hydro": "Hóa lỏng",
        "corrosion": "Ăn mòn",
        "physical": "Vật lý",
        "freeze": "Băng kết",
        "resonance": "Cộng hưởng",
    }
    for element, label in elements.items():
        class_name = f"guide-text-{element}"
        assert f'<option value="{class_name}">{label}</option>' in html
        assert f".{class_name}" in editor_css
        assert f".{class_name}" in site_css
        assert f"'{class_name}'" in rich_text


def test_editor_supports_dragging_any_block_without_changing_json_schema() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert "function reorderBlock" in app
    assert "dragstart" in app
    assert "dragover" in app
    assert "drop" in app
    assert "draggable: 'true'" in app
    assert "const cleanBlocks = state.blocks.map(({ id, _objectUrl, ...rest }) => rest);" in app


def test_reference_toolbar_appends_compact_inline_refs_to_active_editor() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    editor_css = (EDITOR_DIR / "style.css").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")

    assert ' Character</button>' in html
    assert ' Weapon</button>' in html
    assert ' Skill</button>' in html
    assert "function insertInlineReference" in app
    assert "function characterInlineHTML" in app
    assert "function weaponInlineHTML" in app
    assert "function skillInlineHTML" in app
    assert "function preserveInlineSelection" in app
    assert "['tb-char-card', 'tb-weapon-card', 'tb-skill-ref', 'tb-summon-ref', 'tb-effect-ref']" in app
    assert "range.insertNode(fragment)" in app
    assert "requestAnimationFrame(() => rememberEditableSelection({ target: editor }))" in app
    assert "insertInlineReference(characterInlineHTML" in app
    assert "insertInlineReference(weaponInlineHTML" in app
    assert "insertInlineReference(skillInlineHTML" in app
    assert "addBlock({type:'char_card', slug})" not in app
    assert "addBlock({type:'weapon_card', slug})" not in app
    assert ".guide-inline-ref" in editor_css
    assert ".guide-inline-icon" in editor_css
    assert ".guide-inline-ref" in site_css
    assert ".guide-inline-icon" in site_css


def test_weapon_thumbnails_use_the_image_path_from_search_data() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert "wp?.image" in app
    assert "assets/images/weapons/${b.slug}.png" not in app


def test_skill_references_use_vietnamese_character_localization() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert "viCharacters: {}" in app
    assert "async function loadVietnameseData" in app
    assert "function localizedSkill" in app
    assert "const skill = localizedSkill(charSlug, skillIdx, summonIdx);" in app
    assert "localizedSkill(charSel.value, i)" in app
    assert "await Promise.all([loadSearchIndex(), loadVietnameseData(), loadWeaponData()])" in app


def test_weapon_references_use_vietnamese_name_and_description() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert "viWeapons: {}" in app
    assert "function localizedWeapon" in app
    assert "const localized = localizedWeapon(slug);" in app
    assert "localizedWeapon(w.slug)" in app
    assert "localized.effect || localized.trait" in app


def test_weapon_reference_has_image_popover_and_signature_weapon_is_prioritized() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    editor_css = (EDITOR_DIR / "style.css").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    rich_text = (EDITOR_DIR / "rich-text.js").read_text(encoding="utf-8")

    assert "guide-weapon-popover" in app
    assert "guide-weapon-popover-image" in app
    assert "function signatureWeaponForCharacter" in app
    assert "function populateWeaponPicker" in app
    assert "signature_weapon" in app
    assert "★ Vũ khí đặc trưng" in app
    assert ".guide-weapon-popover" in editor_css
    assert ".guide-weapon-popover-image" in editor_css
    assert ".guide-weapon-popover" in site_css
    assert ".guide-weapon-popover-image" in site_css
    for class_name in [
        "guide-weapon-popover",
        "guide-weapon-popover-image",
        "guide-weapon-popover-name",
        "guide-weapon-popover-desc",
    ]:
        assert f"'{class_name}'" in rich_text


def test_inline_reference_popovers_are_formatted_and_viewport_safe() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    editor_css = (EDITOR_DIR / "style.css").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    site_js = (ROOT / "site" / "static" / "js" / "search.js").read_text(encoding="utf-8")

    assert "guide-skill-popover" in app
    assert "guide-skill-popover-name" in app
    assert "guide-skill-popover-desc" in app
    assert "stripGameMarkup" in app
    assert ".guide-ref-popover" in editor_css
    assert ".guide-ref-popover" in site_css
    assert "position: fixed" in site_css
    assert "positionGuideReferencePopover" in site_js
    assert "Math.max(viewportPadding" in site_js
    assert ".guide-ref-popover,\n.guide-weapon-popover" in site_css
    assert "existingPopover.classList.add('guide-ref-popover')" in site_js


def test_guide_reference_popovers_are_scrollable_complete_and_hoverable() -> None:
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    site_js = (ROOT / "site" / "static" / "js" / "search.js").read_text(encoding="utf-8")

    open_rule = site_css.split(".guide-ref-popover.is-open", 1)[1].split("}", 1)[0]
    weapon_desc_rule = site_css.split(".guide-weapon-popover-desc", 1)[1].split("}", 1)[0]
    assert "pointer-events: auto" in open_rule
    assert "overflow-y: auto" in site_css
    assert "-webkit-line-clamp" not in weapon_desc_rule
    assert "const hideDelay = 700" in site_js
    assert "popover.addEventListener('pointerenter'" in site_js
    assert "weapon.stats" in site_js
    assert "weapon.trait" in site_js
    assert "weapon.effect" in site_js
    assert "stripGuideGameMarkup(skill.description" in site_js


def test_guide_popover_runtime_is_cache_busted_and_has_css_fallback() -> None:
    base_template = (ROOT / "site" / "templates" / "base.html").read_text(encoding="utf-8")
    build = (ROOT / "site" / "build.py").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")

    assert 'static/js/search.js?v={{ asset_version }}' in base_template
    assert 'STATIC_DIR / "js" / "search.js"' in build

    base_popover_rule = site_css.split(".guide-ref-popover,", 1)[1].split("}", 1)[0]
    open_popover_rule = site_css.split(".guide-ref-popover.is-open", 1)[1].split("}", 1)[0]
    assert "position: absolute" in base_popover_rule
    assert "bottom: calc(100% + 8px)" in base_popover_rule
    assert "position: fixed" in open_popover_rule


def test_guide_popover_repositions_after_scroll_without_stale_coordinates() -> None:
    site_js = (ROOT / "site" / "static" / "js" / "search.js").read_text(encoding="utf-8")
    hide_body = site_js.split("function hideGuideReferencePopover", 1)[1].split("\n  }", 1)[0]

    assert "popover.style.removeProperty('left')" in hide_body
    assert "popover.style.removeProperty('top')" in hide_body
    assert "function repositionVisibleGuideReferencePopovers" in site_js
    assert "window.addEventListener('scroll', scheduleGuideReferenceReposition" in site_js
    assert "window.addEventListener('resize', scheduleGuideReferenceReposition" in site_js


def test_add_reference_modals_offer_accent_insensitive_search() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    for search_id in [
        "modal-char-card-search",
        "modal-weapon-card-search",
        "modal-skill-char-search",
        "modal-skill-summon-search",
        "modal-skill-pick-search",
        "modal-effect-search",
    ]:
        assert f'id="{search_id}"' in html
    assert "function normalizeSearchText" in app
    assert "function bindSelectSearch" in app
    assert "function cacheSelectOptions" in app
    assert ".normalize('NFD')" in app


def test_clearing_reference_search_restores_the_cached_full_list() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    reset_body = app.split("function resetSelectSearch", 1)[1].split("\n}", 1)[0]

    assert "filterSelectOptions(input, select)" in reset_body
    assert "cacheSelectOptions(selectId)" not in reset_body

    effect_body = app.split("$('tb-effect-ref').addEventListener", 1)[1].split("$('tb-table')", 1)[0]
    assert "cacheSelectOptions(picker);" in effect_body
    assert effect_body.index("cacheSelectOptions(picker);") < effect_body.index("resetSelectSearch('modal-effect-search'")


def test_inline_reference_is_inserted_at_saved_range_and_survives_editing() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    insert_body = app.split("function insertInlineReference", 1)[1].split("\n}", 1)[0]

    assert "range.deleteContents()" in insert_body
    assert "range.insertNode(fragment)" in insert_body
    assert "range.setStartAfter(lastInsertedNode)" in insert_body
    assert "target.append(template.content)" not in insert_body
    assert "editor.addEventListener('cut'" in app


def test_editor_blur_does_not_replace_dom_and_invalidate_saved_range() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    blur_body = app.split("editor.addEventListener('blur'", 1)[1].split("\n  });", 1)[0]

    assert "sanitizeStoredHTML(editor.innerHTML)" in blur_body
    assert "editor.innerHTML = cleaned" not in blur_body


def test_editor_loads_canonical_weapon_data_for_complete_picker() -> None:
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")

    assert "async function loadWeaponData" in app
    assert "../../data/weapons.json" in app
    assert "loadWeaponData()" in app
    assert "images?.weapon" in app


def test_effect_toolbar_filters_vietnamese_effects_for_current_character() -> None:
    html = (EDITOR_DIR / "index.html").read_text(encoding="utf-8")
    app = (EDITOR_DIR / "app.js").read_text(encoding="utf-8")
    editor_css = (EDITOR_DIR / "style.css").read_text(encoding="utf-8")
    site_css = (ROOT / "site" / "static" / "css" / "style.css").read_text(encoding="utf-8")

    assert 'id="tb-effect-ref"' in html
    assert 'id="modal-effect"' in html
    assert 'id="modal-effect-pick"' in html
    assert "effects: {}" in app
    assert "function relatedEffectsForCharacter" in app
    assert "function effectInlineHTML" in app
    assert "state.charSlug || $('char-sel').value" in app
    assert "insertInlineReference(effectInlineHTML" in app
    assert "guide-inline-effect" in editor_css
    assert "guide-inline-effect" in site_css


def test_editor_sanitizer_preserves_safe_effect_popover_metadata() -> None:
    rich_text = (EDITOR_DIR / "rich-text.js").read_text(encoding="utf-8")

    for attribute in (
        "data-effect-id", "data-effect", "data-effect-en", "data-text-en",
        "data-type", "data-desc", "data-desc-en", "tabindex",
    ):
        assert f"'{attribute}'" in rich_text
    assert "SAFE_EFFECT_ATTRIBUTES" in rich_text
