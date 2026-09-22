"""Tests for accessibility (a11y), keyboard controls, and mobile navigation contracts."""
from html.parser import HTMLParser
from pathlib import Path
import pytest


class SimpleTag:
    def __init__(self, tag: str, attrs: dict):
        self.tag = tag
        self.attrs = attrs


class DOMCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append(SimpleTag(tag, dict(attrs)))

    def find_all(self, tag: str, **kwargs):
        results = []
        for el in self.elements:
            if el.tag != tag:
                continue
            match = True
            for k, v in kwargs.items():
                attr_name = "class" if k == "class_" else k
                if attr_name not in el.attrs:
                    match = False
                    break
                if k == "class_":
                    classes = el.attrs[attr_name].split()
                    if v not in classes:
                        match = False
                        break
                elif el.attrs[attr_name] != v:
                    match = False
                    break
            if match:
                results.append(el)
        return results

    def find(self, tag: str, **kwargs):
        res = self.find_all(tag, **kwargs)
        return res[0] if res else None


def parse_html(file_path: Path) -> DOMCollector:
    collector = DOMCollector()
    collector.feed(file_path.read_text(encoding="utf-8"))
    return collector


def test_search_input_and_mobile_menu_a11y(built_site: Path):
    """Verify base template accessibility features across generated pages."""
    index_html = built_site / "index.html"
    assert index_html.exists(), "index.html must exist"

    doc = parse_html(index_html)

    # Mobile menu button
    menu_btn = doc.find("button", id="mobile-menu-btn")
    assert menu_btn is not None, "Mobile menu button #mobile-menu-btn must exist"
    assert menu_btn.attrs.get("type") == "button"
    assert menu_btn.attrs.get("aria-expanded") == "false"
    assert menu_btn.attrs.get("aria-controls") == "nav-links"
    assert menu_btn.attrs.get("aria-label")

    # Nav links container
    nav_links = doc.find("ul", id="nav-links")
    assert nav_links is not None, "#nav-links list must exist"

    # Search combobox
    search_input = doc.find("input", id="global-search-input")
    assert search_input is not None, "#global-search-input must exist"
    assert search_input.attrs.get("role") == "combobox"
    assert search_input.attrs.get("aria-autocomplete") == "list"
    assert search_input.attrs.get("aria-controls") == "search-dropdown"
    assert search_input.attrs.get("aria-expanded") == "false"

    # Search dropdown
    dropdown = doc.find("div", id="search-dropdown")
    assert dropdown is not None, "#search-dropdown must exist"
    assert dropdown.attrs.get("role") == "listbox"

    # Screen reader label for search
    sr_label = doc.find("label", class_="sr-only")
    assert sr_label is not None, "A .sr-only label for search must exist"
    assert sr_label.attrs.get("for") == "global-search-input"


def test_character_and_weapon_filter_chips_are_buttons(built_site: Path):
    """Filter chips must be semantic <button type='button'> with aria-pressed."""
    for page_rel in ["characters/index.html", "weapons/index.html"]:
        page = built_site / page_rel
        assert page.exists(), f"{page_rel} must exist"

        doc = parse_html(page)
        chips = [
            c for c in doc.find_all("button", class_="chip")
            if not any(cls in c.attrs.get("class", "").split() for cls in ["filter-toggle", "filter-reset", "view-toggle"])
        ]
        assert len(chips) > 0, f"{page_rel} should contain button.chip elements"

        legacy_chips = doc.find_all("span", class_="chip")
        assert len(legacy_chips) == 0, f"{page_rel} should not contain span.chip elements"

        for chip in chips:
            assert chip.attrs.get("type") == "button", f"Chip must have type='button'"
            assert chip.attrs.get("aria-pressed") in ["true", "false"], f"Chip must have aria-pressed"
            classes = chip.attrs.get("class", "").split()
            if "active" in classes:
                assert chip.attrs.get("aria-pressed") == "true"
            else:
                assert chip.attrs.get("aria-pressed") == "false"


def test_faq_accordion_accessibility(built_site: Path):
    """FAQ questions must be semantic buttons with aria-expanded and controlled regions."""
    faq_html = built_site / "faq.html"
    assert faq_html.exists(), "faq.html must exist"

    doc = parse_html(faq_html)
    questions = doc.find_all("button", class_="faq-question")
    assert len(questions) > 0, "FAQ page must have button.faq-question elements"

    for q in questions:
        assert q.attrs.get("type") == "button"
        assert q.attrs.get("aria-expanded") == "false"
        controls_id = q.attrs.get("aria-controls")
        assert controls_id, f"FAQ question must specify aria-controls"

        answer = doc.find("div", id=controls_id)
        assert answer is not None, f"Element #{controls_id} referenced by question must exist"
        assert answer.attrs.get("role") == "region"
        assert answer.attrs.get("aria-labelledby") == q.attrs.get("id")
        assert "hidden" in answer.attrs, f"Answer #{controls_id} should be hidden initially"


def test_css_accessibility_and_mobile_rules(built_site: Path):
    """Verify essential CSS rules: focus-visible, sr-only, reduced-motion, mobile media query."""
    css_file = built_site / "static" / "css" / "style.css"
    assert css_file.exists(), "style.css must exist"

    content = css_file.read_text(encoding="utf-8")

    assert ":focus-visible" in content, "style.css must define :focus-visible rules"
    assert ".sr-only" in content, "style.css must define .sr-only utility"
    assert "prefers-reduced-motion" in content, "style.css must support prefers-reduced-motion"
    assert "@media (max-width: 768px)" in content, "style.css must define 768px responsive rules"
    assert ".mobile-menu-btn" in content, "style.css must define .mobile-menu-btn"
