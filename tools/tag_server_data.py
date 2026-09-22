import json
import glob
from pathlib import Path

CN_DOLLS = {"asteria", "eagletta", "faelynn", "koleda", "mityl", "soppo", "welrod", "cecilia"}

CN_WEAPONS = {
    "compass-of-repentance",
    "argent-wing-pisty",
    "bristlefang-beast",
    "chernobog",
    "fluffy-nova",
    "skysunderer-s-howl",
    "sopmod-2-tactical-rifle",
    "retired-sopmod-2-tactical-rifle",
    "welrod-mk-ii",
    "retired-welrod-mk-ii",
    "silent-conviction",
    "snotra"
}

def tag_characters():
    char_files = glob.glob("data/characters/*.json")
    cn_count = 0
    global_count = 0
    for fpath in char_files:
        p = Path(fpath)
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        slug = data.get("slug")
        if slug in CN_DOLLS:
            data["server"] = "cn"
            cn_count += 1
        else:
            data["server"] = "global"
            global_count += 1
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(f"Characters tagged: {cn_count} CN, {global_count} Global (Total {cn_count + global_count})")

def tag_weapons():
    weapons_file = Path("data/weapons.json")
    with open(weapons_file, "r", encoding="utf-8") as f:
        weapons = json.load(f)
    cn_count = 0
    global_count = 0
    for w in weapons:
        slug = w.get("slug")
        if slug in CN_WEAPONS:
            w["server"] = "cn"
            cn_count += 1
        else:
            w["server"] = "global"
            global_count += 1
    with open(weapons_file, "w", encoding="utf-8") as f:
        json.dump(weapons, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Weapons tagged: {cn_count} CN, {global_count} Global (Total {cn_count + global_count})")

def update_i18n_vi():
    i18n_path = Path("data/i18n_vi.json")
    with open(i18n_path, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    ui = bundle.setdefault("ui", {})
    ui["label_server"] = "Máy Chủ"
    ui["filter_all_servers"] = "Tất Cả Máy Chủ"
    ui["servers"] = {
        "all": "Tất Cả",
        "global": "Quốc Tế",
        "cn": "Trung Quốc"
    }

    # Tag characters in i18n bundle if present
    for slug, cdata in bundle.get("characters", {}).items():
        cdata["server"] = "cn" if slug in CN_DOLLS else "global"

    # Tag weapons in i18n bundle if present
    for slug, wdata in bundle.get("weapons", {}).items():
        wdata["server"] = "cn" if slug in CN_WEAPONS else "global"

    root = Path(__file__).resolve().parents[1]
    import sys
    sys.path.insert(0, str(root))
    from tools.editor_core.bundle import stage_i18n_bundle
    from tools.editor_core.transaction import RepositoryTransaction

    tx = RepositoryTransaction(root)
    with tx:
        stage_i18n_bundle(root, tx, i18n_bundle=bundle)
        tx.commit()
    print("i18n_vi.json and i18n-vi.js updated with server translations.")

if __name__ == "__main__":
    tag_characters()
    tag_weapons()
    update_i18n_vi()
