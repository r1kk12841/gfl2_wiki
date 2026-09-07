"""Tests for SEO metadata, canonical links, Open Graph, Twitter cards, sitemap.xml, and robots.txt."""
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import pytest
from html.parser import HTMLParser


class MetaTagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.og_tags = {}
        self.twitter_tags = {}
        self.json_ld = []
        self._in_json_ld = False
        self._json_ld_buf = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "link" and attr_dict.get("rel") == "canonical":
            self.canonical = attr_dict.get("href")
        elif tag == "meta":
            prop = attr_dict.get("property")
            name = attr_dict.get("name")
            content = attr_dict.get("content")
            if prop and prop.startswith("og:"):
                self.og_tags[prop] = content
            elif name and name.startswith("twitter:"):
                self.twitter_tags[name] = content
        elif tag == "script" and attr_dict.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_ld_buf = []

    def handle_endtag(self, tag):
        if tag == "script" and self._in_json_ld:
            self._in_json_ld = False
            raw = "".join(self._json_ld_buf).strip()
            if raw:
                try:
                    self.json_ld.append(json.loads(raw))
                except Exception:
                    pass

    def handle_data(self, data):
        if self._in_json_ld:
            self._json_ld_buf.append(data)


def parse_page_seo(file_path: Path) -> MetaTagCollector:
    collector = MetaTagCollector()
    collector.feed(file_path.read_text(encoding="utf-8"))
    return collector


def test_sitemap_generated_and_valid(built_site: Path):
    """sitemap.xml must exist, be valid XML, contain public pages, and no tool links."""
    sitemap_path = built_site / "sitemap.xml"
    assert sitemap_path.exists(), "sitemap.xml must be generated"

    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [el.text for el in root.findall("sm:url/sm:loc", namespace)]
    assert len(locs) >= 255, f"Expected at least 255 URLs in sitemap, got {len(locs)}"

    for loc in locs:
        assert loc.startswith("https://"), f"URL {loc} must start with https://"
        assert "tools" not in loc, f"Internal tool path should not be in sitemap: {loc}"
        assert "editor" not in loc, f"Editor path should not be in sitemap: {loc}"


def test_robots_txt_generated_and_references_sitemap(built_site: Path):
    """robots.txt must exist and point to sitemap.xml."""
    robots_path = built_site / "robots.txt"
    assert robots_path.exists(), "robots.txt must be generated"

    content = robots_path.read_text(encoding="utf-8")
    assert "User-agent: *" in content
    assert "Allow: /" in content
    assert "Sitemap:" in content
    assert "sitemap.xml" in content


def test_canonical_urls_and_no_duplicates(built_site: Path):
    """Every page must have a canonical link, and canonicals must be unique per page."""
    html_files = list(built_site.glob("**/*.html"))
    assert len(html_files) >= 255

    canonical_map = {}
    for html_file in html_files:
        seo = parse_page_seo(html_file)
        rel_path = html_file.relative_to(built_site).as_posix()
        assert seo.canonical is not None, f"Page {rel_path} must have a canonical link"
        assert seo.canonical.startswith("https://r1kk12841.github.io/gfl2_wiki/"), f"Canonical for {rel_path} has wrong base: {seo.canonical}"
        assert seo.canonical.endswith(rel_path), f"Canonical {seo.canonical} must match page {rel_path}"

        if seo.canonical in canonical_map:
            pytest.fail(f"Duplicate canonical URL '{seo.canonical}' found in {rel_path} and {canonical_map[seo.canonical]}")
        canonical_map[seo.canonical] = rel_path


def test_open_graph_and_twitter_metadata(built_site: Path):
    """Key pages must provide Open Graph and Twitter Card tags with valid assets."""
    for test_page in ["index.html", "characters/groza.html", "weapons/st-ar-15.html"]:
        page_path = built_site / test_page
        assert page_path.exists(), f"{test_page} must exist"

        seo = parse_page_seo(page_path)
        assert "og:title" in seo.og_tags, f"{test_page} missing og:title"
        assert "og:description" in seo.og_tags, f"{test_page} missing og:description"
        assert "og:type" in seo.og_tags, f"{test_page} missing og:type"
        assert "og:url" in seo.og_tags, f"{test_page} missing og:url"
        assert "og:image" in seo.og_tags, f"{test_page} missing og:image"

        assert seo.twitter_tags.get("twitter:card") == "summary_large_image"
        assert "twitter:title" in seo.twitter_tags
        assert "twitter:description" in seo.twitter_tags
        assert "twitter:image" in seo.twitter_tags

        # Verify OG image points to an asset that actually exists in built output
        og_img_url = seo.og_tags["og:image"]
        match = re.search(r"/gfl2_wiki/(assets/.*)$", og_img_url)
        if match:
            asset_rel = match.group(1)
            assert (built_site / asset_rel).exists(), f"OG image {asset_rel} does not exist in build output"


def test_json_ld_structured_data(built_site: Path):
    """Character and weapon detail pages should have valid JSON-LD schemas."""
    char_page = built_site / "characters" / "groza.html"
    seo = parse_page_seo(char_page)
    assert len(seo.json_ld) > 0, "groza.html must contain JSON-LD block"
    ld = seo.json_ld[0]
    assert ld.get("@context") == "https://schema.org"
    assert ld.get("@type") == "ItemPage"
    assert "Groza" in ld.get("name", "")
