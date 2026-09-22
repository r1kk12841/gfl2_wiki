#!/usr/bin/env python3
"""
tools/apply_batch4_accurate_translations.py
Applies 100% faithful, accurate Vietnamese translations for Batch 4 (13 dolls):
  florence, helen, lenna, leva, lewis, lind, liushih,
  loreley, mechty, papasha, peri, ullrid, yoohee.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_core.bundle import stage_i18n_bundle

from tools.batch4_data.group1 import GROUP_1_DATA
from tools.batch4_data.group2 import GROUP_2_DATA
from tools.batch4_data.group3 import GROUP_3_DATA

I18N_PATH = ROOT / "data" / "i18n_vi.json"
EFFECTS_PATH = ROOT / "data" / "effects_vi.json"

BATCH_4_DATA = {}
BATCH_4_DATA.update(GROUP_1_DATA)
BATCH_4_DATA.update(GROUP_2_DATA)
BATCH_4_DATA.update(GROUP_3_DATA)


def main():
    print(f"Loading {I18N_PATH}...")
    with open(I18N_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    chars = data.setdefault("characters", {})

    updated_count = 0
    for slug, payload in BATCH_4_DATA.items():
        if slug in chars:
            target = chars[slug]
            target["name"] = payload["name"]
            target["en_name"] = payload["en_name"]
            target["class"] = payload["class"]
            target["phase"] = payload["phase"]
            target["rarity"] = payload["rarity"]
            target["weapon_type"] = payload["weapon_type"]
            target["ammo_type"] = payload["ammo_type"]
            target["signature_weapon"] = payload["signature_weapon"]
            target["weakness"] = payload["weakness"]
            target["skills"] = payload["skills"]
            target["fortification"] = payload["fortification"]
            if "keys" in payload:
                target["keys"] = payload["keys"]
            if "summons" in payload:
                target["summons"] = payload["summons"]
            updated_count += 1
            print(f"Updated character: {slug} ({payload['name']})")
        else:
            chars[slug] = payload
            updated_count += 1
            print(f"Added character: {slug} ({payload['name']})")

    # Load and update effects
    effects_data = json.loads(EFFECTS_PATH.read_text(encoding="utf-8"))
    if "effect_d34d5b4955a8" not in effects_data:
        effects_data["effect_d34d5b4955a8"] = {
            "id": "effect_d34d5b4955a8",
            "name": "Giảm ST III",
            "name_en": "Damage Reduction III",
            "desc": "Sát thương phải chịu giảm 30%. Thuộc loại Buff.",
            "desc_en": "Reduces damage received by 30%. This is considered as a buff",
            "type": "buff",
            "sub_effect_ids": []
        }
        print("Added effect_d34d5b4955a8 (Giảm ST III) to effects_vi.json")

    # Use stage_i18n_bundle inside RepositoryTransaction with effects_data
    print("\nStaging i18n bundle across repository...")
    with RepositoryTransaction(ROOT) as tx:
        stage_i18n_bundle(ROOT, tx, data, effects_data=effects_data)
        tx.commit()


    print(f"\nSuccessfully updated {updated_count} characters and synced effects + i18n bundle!")


if __name__ == "__main__":
    main()
