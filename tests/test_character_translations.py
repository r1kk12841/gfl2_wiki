import json
import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
I18N_PATH = ROOT / "data" / "i18n_vi.json"

BATCH_1_SLUGS = [
    "cheeta", "colphne", "groza", "krolik", "ksenia",
    "littara", "lotta", "nagant", "nemesis", "sharkry"
]

BATCH_2_SLUGS = [
    "suomi", "tololo", "sabrina", "qiongjiu", "daiyan",
    "klukai", "centaureissi", "andoris", "balthilde", "basti",
    "belka", "cheyanne", "dushevnaya", "faye"
]

BATCH_3_SLUGS = [
    "springfield", "peritya", "vepley", "mosin-nagant", "jiangyu",
    "vector", "makiatto", "robella", "eagletta", "asteria",
    "soppo", "welrod"
]

BATCH_4_SLUGS = [
    "florence", "helen", "lenna", "leva", "lewis",
    "lind", "liushih", "loreley", "mechty", "papasha",
    "peri", "ullrid", "yoohee"
]

BATCH_5_SLUGS = [
    "faelynn", "harpsy", "koleda", "lainie",
    "mityl", "nemesis-gnosis", "nikketa", "ots-14",
    "phaetusa", "qiuhua", "sakura", "sextans", "zhaohui",
    "cecilia"
]

ALL_BATCHES_SLUGS = BATCH_1_SLUGS + BATCH_2_SLUGS + BATCH_3_SLUGS + BATCH_4_SLUGS + BATCH_5_SLUGS
GOLDEN_SLUGS = ["alva", "voymastina"] + ALL_BATCHES_SLUGS


VALID_TAGS = {
    "Đánh Thường", "Chủ Động", "Tuyệt Kỹ", "Bị Động",
    "Chỉ Định", "Phạm Vi", "AoE", "Cận Chiến", "Chuẩn Xác",
    "Cường Hóa", "Suy Yếu", "Hỗ Trợ", "Trị Liệu", "Triệu Hồi",
    "Phản Kích", "Chặn Đánh", "Phục Kích", "Dịch Chuyển", "Giải Trừ",
    "Ô Địa Hình", "Phá Hủy Vật Cản", "Khống Chế", "Phòng Ngự"
}

ENG_WORDS = [
    r"\bwhen\b", r"\bdeals?\b", r"\bincreases?\b", r"\bgrants?\b", r"\bdecreases?\b",
    r"\btargets?\b", r"\benem(y|ies)\b", r"\ball(y|ies)\b", r"\bturns?\b", r"\bcooldown\b",
    r"\bapplies\b", r"\bwithin\b", r"\brange\b", r"\btiles?\b", r"\battack\b", r"\bdefense\b",
    r"\bcritical\b", r"\bdamage\b", r"\bchance\b", r"\bcurrent\b", r"\bmaximum\b",
    r"\breduce[sd]?\b", r"\btrigger[sd]?\b", r"\bactive\b", r"\bpassive\b",
    r"\bstack[sd]?\b", r"\bobtain[sd]?\b", r"\bgain[sd]?\b"
]
eng_regex = re.compile("|".join(ENG_WORDS), re.IGNORECASE)

@pytest.fixture(scope="module")
def i18n_data():
    with open(I18N_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_characters_presence(i18n_data):
    chars = i18n_data.get("characters", {})
    for slug in ALL_BATCHES_SLUGS:
        assert slug in chars, f"Character {slug} missing from i18n_vi.json"

@pytest.mark.parametrize("slug", ALL_BATCHES_SLUGS)
def test_skill_tags_valid(i18n_data, slug):
    char = i18n_data["characters"][slug]
    for s in char.get("skills", []):
        for tag in s.get("tags", []):
            assert tag in VALID_TAGS, f"[{slug}] Invalid/English tag found: '{tag}' in skill '{s.get('name')}'"
    for sm in char.get("summons", []):
        for s in sm.get("skills", []):
            for tag in s.get("tags", []):
                assert tag in VALID_TAGS, f"[{slug}] Invalid tag in summon skill '{s.get('name')}': '{tag}'"

@pytest.mark.parametrize("slug", ALL_BATCHES_SLUGS)
def test_no_english_leakage(i18n_data, slug):
    char = i18n_data["characters"][slug]
    
    # Check skills
    for s in char.get("skills", []):
        desc = re.sub(r"<[^>]+>", "", s.get("description", ""))
        matches = eng_regex.findall(desc)
        assert not matches, f"[{slug}] English text found in skill '{s.get('name')}': {matches}"
        
    # Check fortification
    for f_item in char.get("fortification", []):
        eff = re.sub(r"<[^>]+>", "", f_item.get("effect", ""))
        matches = eng_regex.findall(eff)
        assert not matches, f"[{slug}] English text found in fort tier {f_item.get('tier')}: {matches}"

    # Check keys
    for k_item in char.get("keys", []):
        eff = re.sub(r"<[^>]+>", "", k_item.get("effect", ""))
        matches = eng_regex.findall(eff)
        assert not matches, f"[{slug}] English text found in key '{k_item.get('name')}': {matches}"

    # Check summons
    for sm in char.get("summons", []):
        for s in sm.get("skills", []):
            desc = re.sub(r"<[^>]+>", "", s.get("description", ""))
            matches = eng_regex.findall(desc)
            assert not matches, f"[{slug}] English text in summon skill '{s.get('name')}': {matches}"

@pytest.mark.parametrize("slug", ALL_BATCHES_SLUGS)
def test_color_tag_balancing(i18n_data, slug):
    char = i18n_data["characters"][slug]
    texts = []
    for s in char.get("skills", []):
        texts.append(s.get("description", ""))
    for f_item in char.get("fortification", []):
        texts.append(f_item.get("effect", ""))
    for k_item in char.get("keys", []):
        texts.append(k_item.get("effect", ""))
    for sm in char.get("summons", []):
        for s in sm.get("skills", []):
            texts.append(s.get("description", ""))

    for t in texts:
        opens = len(re.findall(r"<color=[^>]+>", t))
        closes = len(re.findall(r"</color>", t))
        assert opens == closes, f"[{slug}] Unbalanced color tags: {opens} open vs {closes} close in '{t}'"

@pytest.mark.parametrize("slug", ALL_BATCHES_SLUGS)
def test_schema_parity(i18n_data, slug):
    char = i18n_data["characters"][slug]
    en_path = ROOT / "data" / "characters" / f"{slug}.json"
    with open(en_path, "r", encoding="utf-8") as f:
        en_char = json.load(f)

    assert len(char.get("skills", [])) == len(en_char.get("skills", []))
    assert len(char.get("fortification", [])) == 6
    assert len(char.get("neural_helix", [])) == 6
    assert len(char.get("keys", [])) == len(en_char.get("keys", []))
    if "summons" in en_char:
        assert len(char.get("summons", [])) == len(en_char.get("summons", []))


@pytest.fixture(scope="module")
def browser_effects_catalog():
    from tools.effects_catalog import browser_catalog, canonicalize_effects
    effects_file = ROOT / "data" / "effects_vi.json"
    with open(effects_file, "r", encoding="utf-8-sig") as f:
        data = canonicalize_effects(json.load(f))
    return browser_catalog(data)


@pytest.mark.parametrize("slug", ALL_BATCHES_SLUGS)
def test_effects_resolve(i18n_data, browser_effects_catalog, slug):
    """Every effect enclosed in <color=#3487e0> must resolve to an effect in the catalog."""
    char = i18n_data["characters"][slug]
    name_index = browser_effects_catalog["nameIndex"]

    texts = []
    for s in char.get("skills", []):
        texts.append(s.get("description", ""))
    for f_item in char.get("fortification", []):
        texts.append(f_item.get("effect", ""))
    for k_item in char.get("keys", []):
        texts.append(k_item.get("effect", ""))
    for sm in char.get("summons", []):
        for s in sm.get("skills", []):
            texts.append(s.get("description", ""))

    color_re = re.compile(r"<color=#3487e0>(.*?)</color>")
    unresolved = []
    for t in texts:
        for match in color_re.findall(t):
            cleaned = match.strip()
            lower = cleaned.casefold()
            if lower not in name_index:
                unresolved.append(cleaned)

    assert not unresolved, f"[{slug}] Unresolved status effects without popover: {unresolved}"


