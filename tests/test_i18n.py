"""
tests/test_i18n.py
Unit tests verifying Vietnamese localization data, language switcher button,
and template internationalization attributes.
"""

import json
import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_i18n_vi_json_exists_and_valid():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    assert i18n_path.exists(), "data/i18n_vi.json must exist"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    assert "ui" in data, "Must contain 'ui' dictionary"
    assert "weapons" in data, "Must contain 'weapons' dictionary"
    assert "characters" in data, "Must contain 'characters' dictionary"
    assert len(data["weapons"]) == 187, "Must contain all 187 weapons"
    assert len(data["characters"]) == 64, "Must contain all 64 characters"
    assert data["ui"]["nav_home"] == "Trang Chủ"
    assert data["ui"]["nav_dolls"] == "Nhân Vật"
    assert data["ui"]["nav_weapons"] == "Vũ Khí"
    assert data["ui"]["nav_faq"] == "Hỏi Đáp"


def test_i18n_vi_js_bundle():
    js_path = ROOT / "site" / "static" / "js" / "i18n-vi.js"
    assert js_path.exists(), "site/static/js/i18n-vi.js must exist"
    content = js_path.read_text(encoding="utf-8")
    assert "window.GFL2_I18N_VI =" in content
    assert "ST AR-15 Kiểu Cũ" in content


def test_i18n_js_engine():
    engine_path = ROOT / "site" / "static" / "js" / "i18n.js"
    assert engine_path.exists(), "site/static/js/i18n.js must exist"
    content = engine_path.read_text(encoding="utf-8")
    assert "window.GFL2_I18N =" in content
    assert "lang-toggle-btn" in content
    assert "applyLanguage" in content


def test_base_template_has_switcher_and_scripts():
    base_html = (ROOT / "site" / "templates" / "base.html").read_text(encoding="utf-8")
    assert 'id="lang-toggle-btn"' in base_html
    assert 'data-i18n="nav_home"' in base_html
    assert 'data-i18n="nav_dolls"' in base_html
    assert 'data-i18n="nav_weapons"' in base_html
    assert 'data-i18n="nav_faq"' in base_html
    assert "i18n-vi.js" in base_html
    assert "i18n.js" in base_html


def test_character_template_has_i18n_hooks():
    char_html = (ROOT / "site" / "templates" / "character.html").read_text(encoding="utf-8")
    assert "data-char-slug" in char_html
    assert 'data-i18n="stat_hp"' in char_html
    assert 'data-i18n="stat_atk"' in char_html
    assert 'data-i18n="stat_def"' in char_html
    assert 'data-i18n="stat_stability"' in char_html
    assert 'data-i18n="stat_mobility"' in char_html
    assert 'data-i18n="stat_weapon_type"' in char_html
    assert 'data-i18n="stat_ammo_type"' in char_html
    assert 'data-i18n="stat_signature_weapon"' in char_html
    assert 'data-i18n="skills_section_title"' in char_html


def test_weapon_template_has_i18n_hooks():
    weapon_html = (ROOT / "site" / "templates" / "weapon.html").read_text(encoding="utf-8")
    assert "data-weapon-slug" in weapon_html
    assert 'data-i18n="base_stats_label"' in weapon_html
    assert 'data-i18n="sig_for_label"' in weapon_html
    assert 'data-i18n="weapon_trait_title"' in weapon_html
    assert 'data-i18n="weapon_effect_title"' in weapon_html


def test_dist_rendered_pages_contain_switcher():
    dist_home = (ROOT / "dist" / "index.html").read_text(encoding="utf-8")
    assert 'id="lang-toggle-btn"' in dist_home
    assert "i18n-vi.js" in dist_home
    assert "i18n.js" in dist_home

    dist_andoris = (ROOT / "dist" / "characters" / "andoris.html").read_text(encoding="utf-8")
    assert 'data-char-slug="andoris"' in dist_andoris
    assert 'id="lang-toggle-btn"' in dist_andoris


def test_effects_vi_data():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    assert "effects" in data, "Must contain 'effects' dictionary"
    effects = data["effects"]
    assert "Shelter" in effects, "Must contain English key"
    assert "Nơi Trú Ẩn" in effects, "Must contain Vietnamese key"
    assert effects["Shelter"]["name"] == "Nơi Trú Ẩn"
    assert "Bảo Vệ Độ Ổn Định" in effects["Shelter"]["desc"]


def test_no_unresolved_placeholders():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    for slug, c in data.get("characters", {}).items():
        for s in c.get("skills", []):
            assert not re.search(r"\{[0-9]+\}", s.get("description", "")), f"Found unresolved placeholder in {slug} skill: {s.get('name')}"
        for f in c.get("fortification", []):
            assert not re.search(r"\{[0-9]+\}", f.get("effect", "")), f"Found unresolved placeholder in {slug} fort: {f.get('skill')}"
        for k in c.get("keys", []):
            assert not re.search(r"\{[0-9]+\}", k.get("effect", "")), f"Found unresolved placeholder in {slug} key: {k.get('name')}"


def test_summons_vi_localization():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    andoris = data["characters"]["andoris"]
    assert "summons" in andoris and len(andoris["summons"]) > 0
    sm = andoris["summons"][0]
    assert sm["name"] == "Ụ Pháo Tự Động"
    assert "không thể di chuyển" in sm["description"]
    assert "HP ban đầu của Andoris" in sm["stats"]["hp"]

    basti = data["characters"]["basti"]
    assert basti["summons"][0]["name"] == "Cục Cưng"
    assert "Vật triệu hồi kế thừa" in basti["summons"][0]["description"]


def test_weapons_vi_localization():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    weapons = data["weapons"]
    assert len(weapons) == 187
    sample_w = weapons.get("guerno")
    assert sample_w is not None
    assert "đầy HP" in sample_w["trait"] or "Buff" in sample_w["trait"]
    assert "đồng minh" in sample_w["effect"]


def test_server_translations():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    ui = data.get("ui", {})
    assert "label_server" in ui
    assert ui["label_server"] == "Máy Chủ"
    assert "filter_all_servers" in ui
    assert "servers" in ui
    assert ui["servers"]["cn"] == "Trung Quốc"
    assert ui["servers"]["global"] == "Quốc Tế"


def test_resonance_phase_translation():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    assert data["ui"]["phases"]["Resonance"] == "Cộng Hưởng"
    assert data["characters"]["ots-14"]["phase"] == "Cộng Hưởng"


def test_rarity_tag_translation():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    ui = data.get("ui", {})
    # Card badges must be concise without suffix
    assert ui["rarities"]["Elite"] == "Tinh Nhuệ"
    assert ui["rarities"]["Standard"] == "Tiêu Chuẩn"
    # Filter chips include the (SSR) / (SR) clarify
    assert ui["rarities_filter"]["Elite"] == "Tinh Nhuệ (SSR)"
    assert ui["rarities_filter"]["Standard"] == "Tiêu Chuẩn (SR)"


def test_all_summon_skills_localized():
    i18n_path = ROOT / "data" / "i18n_vi.json"
    data = json.loads(i18n_path.read_text(encoding="utf-8"))
    
    total_skills = 0
    characters_with_summon_skills = ["andoris", "balthilde", "florence", "koleda", "lainie", "liushih", "mityl", "nikketa", "papasha", "tololo"]
    
    for slug in characters_with_summon_skills:
        char_data = data["characters"].get(slug, {})
        assert "summons" in char_data, f"Character {slug} must have summons"
        sms = char_data["summons"]
        assert len(sms) > 0, f"Character {slug} must have at least 1 summon"
        sks = sms[0].get("skills", [])
        assert len(sks) > 0, f"Character {slug} summon must have skills"
        for sk in sks:
            total_skills += 1
            assert sk.get("name"), f"Skill in {slug} must have a non-empty name"
            assert not re.search(r"\{[0-9]+\}", sk.get("name", "")), f"Placeholder found in {slug} summon skill name"
            assert not re.search(r"\{[0-9]+\}", sk.get("description", "")), f"Placeholder found in {slug} summon skill description"
    
    assert total_skills == 23, f"Expected 23 summon skills, found {total_skills}"


def test_effects_zero_english_contamination():
    effects_path = ROOT / "data" / "effects_vi.json"
    assert effects_path.exists(), "data/effects_vi.json must exist"
    effs = json.loads(effects_path.read_text(encoding="utf-8"))
    
    en_detector = re.compile(
        r"\b(damage|attack|increases|decreases|target|enemy|enemies|when|after|before|"
        r"turn|turns|within|tiles|range|gains|reducing|taken|dealt|stack|stacks|"
        r"cannot|could|would|should|their|they|them|which|where|there|from|with|"
        r"into|about|under|over|per|deals|takes|has|have|unit|units|allies|ally|"
        r"applies|applied|rate|crit|defense|maximum|movement|speed|mobility)\b",
        re.IGNORECASE,
    )
    
    seen = set()
    for k, v in effs.items():
        name_en = v.get("name_en")
        if name_en in seen:
            continue
        seen.add(name_en)
        desc_vi = v.get("desc", "")
        matches = en_detector.findall(desc_vi)
        assert not matches, f"Effect '{name_en}' contains English words: {matches} in desc: '{desc_vi}'"
    
    assert len(seen) == 381, f"Expected 381 unique effects, checked {len(seen)}"


def test_summon_skill_template_and_js_hooks():
    char_tmpl = (ROOT / "site" / "templates" / "character.html").read_text(encoding="utf-8")
    assert "data-summon-skill-idx" in char_tmpl
    assert "data-summon-skill-name" in char_tmpl
    assert "data-summon-skill-desc" in char_tmpl

    i18n_js = (ROOT / "site" / "static" / "js" / "i18n.js").read_text(encoding="utf-8")
    assert "data-summon-skill-idx" in i18n_js
    assert "data-summon-skill-name" in i18n_js
    assert "data-summon-skill-desc" in i18n_js

    tololo_html = (ROOT / "dist" / "characters" / "tololo.html").read_text(encoding="utf-8")
    assert 'data-summon-skill-idx="0"' in tololo_html
    assert "data-summon-skill-name" in tololo_html
    assert "Call of the Stars" in tololo_html


def test_search_js_vietnamese_highlighting():
    search_js = (ROOT / "site" / "static" / "js" / "search.js").read_text(encoding="utf-8")
    assert "ST\\s+Băng" in search_js
    assert "ST\\s+Thiêu\\s+Đốt" in search_js
    assert "ST\\s+Ăn\\s+Mòn" in search_js
    assert "ST\\s+Hóa\\s+Lỏng" in search_js
    assert "ST\\s+Dẫn\\s+Điện" in search_js
    assert "ST\\s+Vật\\s+Lý" in search_js
    assert "ST\\s+cố\\s+định" in search_js
    assert "ST\\s+Ổn\\s+Định" in search_js
    assert "ô" in search_js


def test_card_badge_selectors_do_not_clobber_rarity():
    i18n_js = (ROOT / "site" / "static" / "js" / "i18n.js").read_text(encoding="utf-8")
    # Must explicitly guard against doll-card and weapon-card container elements
    assert "el.classList.contains('doll-card')" in i18n_js
    assert "document.querySelectorAll('[data-doll-rarity], [data-weapon-rarity]')" in i18n_js
    assert "document.querySelectorAll('.filter-chip[data-server]')" in i18n_js
    assert "document.querySelectorAll('[data-doll-server], [data-weapon-server]')" in i18n_js
    
    char_index_html = (ROOT / "dist" / "characters" / "index.html").read_text(encoding="utf-8")
    assert 'data-doll-rarity="Elite"' in char_index_html
    assert 'data-doll-server="global"' in char_index_html


def test_weapons_card_translation_and_zero_english():
    weapons_tmpl = (ROOT / "site" / "templates" / "weapons_index.html").read_text(encoding="utf-8")
    assert "data-weapon-card-trait" in weapons_tmpl

    i18n_js = (ROOT / "site" / "static" / "js" / "i18n.js").read_text(encoding="utf-8")
    assert "data-weapon-card-trait" in i18n_js

    i18n_data = json.loads((ROOT / "data" / "i18n_vi.json").read_text(encoding="utf-8"))
    w6p33 = i18n_data["weapons"]["6p33"]
    assert "Nếu đầy HP khi kết thúc hành động" in w6p33["trait"]
    assert "nhận 1 Buff ngẫu nhiên duy trì 1 hiệp" in w6p33["trait"]

    en_detector = re.compile(
        r"\b(damage|attack|increases|decreases|target|enemy|enemies|when|after|before|"
        r"turn|turns|within|tiles|range|gains|reducing|taken|dealt|stack|stacks|"
        r"cannot|could|would|should|their|they|them|which|where|there|from|with|"
        r"into|about|under|over|per|deals|takes|has|have|unit|units|allies|ally|"
        r"applies|applied|rate|crit|defense|maximum|movement|speed|mobility|lasting|"
        r"random|full)\b",
        re.IGNORECASE,
    )
    for slug, w in i18n_data["weapons"].items():
        tr = w.get("trait")
        if tr:
            matches = en_detector.findall(tr)
            assert not matches, f"Weapon '{slug}' trait contains English words: {matches} in: '{tr}'"

