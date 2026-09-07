"""
tests/test_assets.py
Asset optimization and integrity tests (Phase 5).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
CHAR_DIR = ROOT / "data" / "characters"
WEAPONS_FILE = ROOT / "data" / "weapons.json"


def test_every_character_has_existing_portrait_webp():
    char_files = list(CHAR_DIR.glob("*.json"))
    assert len(char_files) == 64
    for cf in char_files:
        data = json.loads(cf.read_text(encoding="utf-8"))
        images = data.get("images", {})
        webp_rel = images.get("portrait_webp")
        assert webp_rel, f"Character {cf.stem} missing portrait_webp field in JSON"
        full_path = ROOT / webp_rel
        assert full_path.exists(), f"WebP portrait file does not exist: {webp_rel}"


def test_rendered_html_uses_picture_tag_with_webp_and_png(built_site: Path):
    groza_html = (built_site / "characters" / "groza.html").read_text(encoding="utf-8")
    assert "<picture>" in groza_html
    assert 'type="image/webp"' in groza_html
    assert 'portrait.webp' in groza_html
    assert 'portrait.png' in groza_html

    index_html = (built_site / "characters" / "index.html").read_text(encoding="utf-8")
    assert "<picture>" in index_html
    assert 'type="image/webp"' in index_html
    assert 'portrait.webp' in index_html


def test_no_public_html_references_root_image(built_site: Path):
    for html_file in built_site.glob("**/*.html"):
        content = html_file.read_text(encoding="utf-8")
        # Check that no src or href points to root image/ (except word 'image' inside assets/images)
        assert 'src="../image/' not in content, f"Reference to root image/ found in {html_file.name}"
        assert 'src="image/' not in content, f"Reference to root image/ found in {html_file.name}"
        assert 'href="../image/' not in content, f"Reference to root image/ found in {html_file.name}"
        assert 'href="image/' not in content, f"Reference to root image/ found in {html_file.name}"


def test_output_directory_size_limit(built_site: Path):
    total_bytes = sum(f.stat().st_size for f in built_site.glob("**/*") if f.is_file())
    total_mib = total_bytes / (1024 * 1024)
    # Clean build without root image/ must be under 135 MiB
    assert total_mib < 135.0, f"Output directory size too large: {total_mib:.2f} MiB (expected < 135 MiB without image/)"
