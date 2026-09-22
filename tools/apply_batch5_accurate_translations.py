#!/usr/bin/env python3
"""
tools/apply_batch5_accurate_translations.py
Applies 100% faithful, accurate Vietnamese translations for Batch 5 (13 dolls):
  faelynn, harpsy, koleda, lainie,
  mityl, nemesis-gnosis, nikketa, ots-14,
  phaetusa, qiuhua, sakura, sextans, zhaohui.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_core.bundle import stage_i18n_bundle

from tools.batch5_data.group1 import GROUP_1_DATA
from tools.batch5_data.group2 import GROUP_2_DATA
from tools.batch5_data.group3 import GROUP_3_DATA

I18N_PATH = ROOT / "data" / "i18n_vi.json"
EFFECTS_PATH = ROOT / "data" / "effects_vi.json"

BATCH_5_DATA = {}
BATCH_5_DATA.update(GROUP_1_DATA)
BATCH_5_DATA.update(GROUP_2_DATA)
BATCH_5_DATA.update(GROUP_3_DATA)


def main():
    print(f"Loading {I18N_PATH}...")
    with open(I18N_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    chars = data.setdefault("characters", {})

    updated_count = 0
    for slug, payload in BATCH_5_DATA.items():
        if slug in chars:
            target = chars[slug]
            if "name" in payload:
                target["name"] = payload["name"]
            if "en_name" in payload:
                target["en_name"] = payload["en_name"]
            for prop in ["class", "phase", "rarity", "weapon_type", "ammo_type", "signature_weapon", "weakness"]:
                if prop in payload:
                    target[prop] = payload[prop]
            if "skills" in payload:
                target["skills"] = payload["skills"]
            if "fortification" in payload:
                target["fortification"] = payload["fortification"]
            if "keys" in payload:
                target["keys"] = payload["keys"]
            if "summons" in payload:
                target["summons"] = payload["summons"]
            updated_count += 1
            print(f"Updated character: {slug} ({target.get('name')})")
        else:
            chars[slug] = payload
            updated_count += 1
            print(f"Added character: {slug} ({payload.get('name')})")

    # Load and verify effects
    effects_data = json.loads(EFFECTS_PATH.read_text(encoding="utf-8"))
    if "effect_20e87f8738e4" not in effects_data:
        effects_data["effect_20e87f8738e4"] = {
            "id": "effect_20e87f8738e4",
            "name": "Chính Nghĩa",
            "name_en": "Righteousness",
            "desc": "Tăng 30% TL Bạo Kích và 30% ST Bạo Kích của bản thân. Khi chủ động dùng KN Tuyệt Kỹ Phán Quyết Chính Nghĩa, tiêu hao 5 lớp hiệu ứng này để thi triển KN Tuyệt Kỹ thêm 1 lần. Tối đa cộng dồn 5 lớp, không thể giải trừ.",
            "desc_en": "Increases own Critical Rate by 30% and Critical Damage by 30%. When actively using the Ultimate Skill Righteous Judgment, consumes 5 stacks of this effect to cast the Ultimate Skill an additional time. Can stack up to 5 times. Cannot be dispelled.",
            "type": "buff",
            "sub_effect_ids": []
        }
        print("Added effect_20e87f8738e4 (Chính Nghĩa) to effects_vi.json")

    # Use stage_i18n_bundle inside RepositoryTransaction with effects_data
    print("\nStaging i18n bundle across repository...")
    with RepositoryTransaction(ROOT) as tx:
        stage_i18n_bundle(ROOT, tx, data, effects_data=effects_data)
        tx.commit()

    print(f"\nSuccessfully updated {updated_count} characters and synced effects + i18n bundle!")


if __name__ == "__main__":
    main()
