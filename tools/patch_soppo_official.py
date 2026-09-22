"""Patch Soppo character data, translations, effects, and guides with official infographic details."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Update data/effects_vi.json
effects_path = ROOT / "data" / "effects_vi.json"
effects_data = json.loads(effects_path.read_text(encoding="utf-8"))

effects_to_update = {
    "effect_5ae2c6eed3cb": {
        "name": "Chế Độ Chó Điên",
        "name_en": "Mad Dog Mode",
        "desc": "Khi ở dạng này, một số kỹ năng gây ST Thiêu Đốt. Có thể chuyển sang Chế Độ Chó Săn.",
        "desc_en": "While in this state, certain skills deal Burn damage. Can switch to Hunting Hound Mode.",
    },
    "effect_731a96515b90": {
        "name": "Chế Độ Chó Săn",
        "name_en": "Hunting Hound Mode",
        "desc": "Khi ở dạng này, một số kỹ năng gây ST Băng Kết. Có thể chuyển sang Chế Độ Chó Điên.",
        "desc_en": "While in this state, certain skills deal Freeze damage. Can switch to Mad Dog Mode.",
    },
    "effect_fa8f59c100ac": {
        "name": "Dấu Ấn Săn Mồi",
        "name_en": "Hunting Mark",
        "desc": "Ấn ký độc quyền của Soppo. Có thể cộng dồn tối đa 16 tầng. Không thể giải trừ.",
        "desc_en": "Soppo exclusive mark. Can stack up to 16 times. Cannot be dispelled.",
    },
    "effect_725efe82415d": {
        "name": "Dấu Ấn Săn Mồi Vĩnh Viễn",
        "name_en": "Permanent Hunting Mark",
        "desc": "Ấn ký độc quyền của Soppo. Không thể bị tiêu hao. Không thể giải trừ.",
        "desc_en": "Soppo exclusive mark. Cannot be consumed. Cannot be dispelled.",
    },
    "effect_6bb0f520500a": {
        "name": "Dấu Vết Tàn Sát",
        "name_en": "Slaughtertrail",
        "desc": "Trước khi tấn công chủ động, tạo các ô địa hình Băng Giá trong bán kính 2 ô xung quanh mục tiêu trong 2 hiệp, và sát thương gây ra khi tấn công các đơn vị địch đứng trên ô nguyên tố sẽ tăng thêm 20%. Thuộc loại Buff và không thể giải trừ.",
        "desc_en": "Before actively attacking, creates Frost tiles within 2 tiles radius around the target for 2 rounds, and damage dealt when attacking enemy units on phase tiles is increased by 20%. Considered a buff, cannot be cleansed.",
    },
    "effect_fb8802d4262c": {
        "name": "Nhân Tố Cuồng Bạo",
        "name_en": "Rabid Factor",
        "desc": "Tăng 5% sát thương Bạo Kích. Có thể cộng dồn. Thuộc loại Buff và không thể giải trừ.",
        "desc_en": "Increases critical damage dealt by 5%. Can stack up to 10 times. Considered a buff and cannot be cleansed.",
    },
    "effect_85349ba10dfa": {
        "name": "Nhân Tố Cuồng Bạo I",
        "name_en": "Rabid Factor I",
        "desc": "Khi chủ động tấn công mục tiêu địch trên ô địa hình Dị Vị, bản thân bỏ qua 10% Phòng Thủ của mục tiêu; với mỗi 1 cấp ô địa hình, bỏ qua thêm 10% Phòng Thủ. Buff không thể giải trừ.",
        "desc_en": "When attacking an enemy target on a phase tile with active attacks, ignores 10% of the target's defense. For each level of the tile, ignores an additional 10% of the target's defense. Considered a buff and cannot be cleansed.",
    },
    "effect_d7b3752f7c62": {
        "name": "Nhân Tố Cuồng Bạo II",
        "name_en": "Rabid Factor II",
        "desc": "Bản thân cứ có 1 hiệu ứng Buff loại Băng Kết hoặc Thiêu Đốt, ST Băng Kết và ST Thiêu Đốt gây ra tăng 5%, nếu cộng dồn đến 20 tầng, sát thương tăng thêm 5%. Buff không thể giải trừ.",
        "desc_en": "For each Freeze or Burn buff on Soppo, Freeze and Burn damage dealt is increased by 5%. Considered a buff and cannot be cleansed.",
    },
    "effect_020d65de45b5": {
        "name": "Nhân Tố Cuồng Bạo III",
        "name_en": "Rabid Factor III",
        "desc": "Trước khi gây sát thương, tạo ra ô địa hình tương ứng trong phạm vi 4 ô xung quanh mục tiêu duy trì 2 hiệp. Khi tấn công mục tiêu địch trên ô địa hình Dị Vị, sát thương gây ra tăng 15%, nếu cộng dồn đến 20 tầng, sát thương tăng thêm 15%. Mỗi cấp ô địa hình tăng thêm 10% sát thương gây ra. Buff không thể giải trừ.",
        "desc_en": "Before dealing damage, generates Frost tiles around the target. If Soppo is in Mad Dog Mode, instead generates Incineration tiles. Damage dealt to enemy targets on phase tiles is increased by 15%. For each level of the tile, damage dealt is further increased by 10%. Considered a buff and cannot be cleansed.",
    },
    "effect_a3b66642114a": {
        "name": "Xung Kích Băng Kết",
        "name_en": "Boreal Assault",
        "desc": "Tăng Tấn Công thêm 10%. Thuộc loại Buff Băng Kết.",
        "desc_en": "Increases attack by 10%. Considered a Freeze buff.",
    }
}

for eid, patch in effects_to_update.items():
    if eid in effects_data:
        effects_data[eid].update(patch)

effects_path.write_text(json.dumps(effects_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Updated {len(effects_to_update)} effects in data/effects_vi.json")

# 2. Update data/characters/soppo.json
soppo_char_path = ROOT / "data" / "characters" / "soppo.json"
soppo_char = json.loads(soppo_char_path.read_text(encoding="utf-8"))

soppo_char["skills"] = [
    {
        "name": "Hunting Fang",
        "tags": [
            "Basic Attack",
            "Targeted"
        ],
        "ammo_type": "Medium Ammo",
        "stability_damage": 2,
        "cooldown": "0 turns",
        "confectance_cost": 0,
        "range": 8,
        "effect_area": "Target",
        "description": "Deals Freeze damage equal to 80% of attack to the target. Soppo gains Confectance Index and 2 points of Hunting Mark, which is her personal mark. If Soppo is in Mad Dog Mode, this skill instead deals Burn damage.\n\n[Mad Dog Mode]: In this state, certain skills deal Burn damage. Can switch to [Hunting Hound Mode].\n[Hunting Hound Mode]: In this state, certain skills deal Freeze damage. Can switch to [Mad Dog Mode].",
        "icon": "assets/images/characters/soppo/skill1-icon.png",
        "range_image": "assets/images/characters/soppo/skill1-range.png"
    },
    {
        "name": "Vicious Bite",
        "tags": [
            "Active",
            "AoE",
            "Tile"
        ],
        "stability_damage": 3,
        "cooldown": "1 turns",
        "confectance_cost": 0,
        "range": 6,
        "effect_area": "3",
        "description": "Deals AoE Freeze damage equal to 80% of attack to the target and all enemy targets within a 3-tile radius around it, generating Frost tiles for 2 turns. After this skill, Soppo performs the basic attack Hunting Fang on the nearest enemy target within 8 tiles and gains Extra Command.\n\nIf Soppo is in Mad Dog Mode, this skill instead deals AoE Burn damage and generates Incineration tiles. Soppo does not gain Extra Command.",
        "icon": "assets/images/characters/soppo/skill2-icon.png",
        "range_image": "assets/images/characters/soppo/skill2-range.png",
        "ammo_type": "Medium Ammo"
    },
    {
        "name": "Lunar Howl",
        "tags": [
            "Active",
            "AoE"
        ],
        "stability_damage": 0,
        "cooldown": "1 turns",
        "confectance_cost": 0,
        "effect_area": "8",
        "description": "Lands on the selected empty Freeze or Burn tile within the battlefield and applies Slaughtertrail to all nearby allied Dolls within an 8-tile radius (excluding Soppo herself) for 3 turns, allowing them to generate Frost tiles around the target after performing an active attack; and damage dealt to enemy units on phase tiles is increased. After this skill, Soppo switches to Mad Dog Mode.\n\nIf Soppo is in Mad Dog Mode, instead deals AoE Burn damage equal to 120% of attack to all enemy targets nearby within a 4-tile radius. This damage is shared evenly among all targets within the effective area. After this skill, Soppo performs the basic attack Hunting Fang on the nearest enemy target within 8 tiles and gains Extra Action.",
        "icon": "assets/images/characters/soppo/skill3-icon.png",
        "range_image": "assets/images/characters/soppo/skill3-range.png",
        "range": "Full map"
    },
    {
        "name": "Fatal Pounce",
        "tags": [
            "Ultimate",
            "AoE",
            "Interception"
        ],
        "stability_damage": 5,
        "cooldown": "2 turns",
        "confectance_cost": 4,
        "effect_area": "6",
        "description": "Selects all enemy targets within a 6-tile radius, expends all stacks of Hunting Mark, and deals AoE Freeze damage equal to number of Hunting Mark stacks × 30% of attack. If this attack hits enemy targets on phase tiles, additionally deals Freeze damage equal to 50% of attack to them. After this skill, Soppo switches to Hunting Hound Mode.\n\nPassive: Before nearby enemy units within 8 tiles launch an active attack, performs Interception on them, dealing Freeze damage equal to 30% of attack and 4 points of stability damage. Can trigger at most once per turn.",
        "icon": "assets/images/characters/soppo/ult-icon.png",
        "range_image": "assets/images/characters/soppo/ult-range.png",
        "ammo_type": "Medium Ammo",
        "range": "Self"
    },
    {
        "name": "Vampup Syndrome",
        "tags": [
            "Passive"
        ],
        "stability_damage": 0,
        "cooldown": "0 turns",
        "confectance_cost": 0,
        "effect_area": "Target",
        "description": "At the start of the battle, Soppo begins in Hunting Hound Mode and expends Confectance Index (consumes 3 points of own Confectance Index) to gain a Frost Barrier for 3 turns. Frost Barrier absorbs damage equal to 65% of initial attack, up to a maximum of 60% of max HP.\n\nAt the start of the battle, if there are 3 or more allied Burn attributed Dolls on the battlefield (excluding Soppo herself), then when she uses the basic attack Hunting Fang or the active skill Vicious Bite and is in Hunting Hound Mode, damage dealt to enemy targets with Burn debuffs is increased by 100%. If there are 3 or more allied Freeze attributed Dolls on the battlefield (excluding Soppo herself), then when she uses the abovementioned skills or the active skill Lunar Howl and is in Mad Dog Mode, damage dealt to enemy targets with Freeze debuffs is increased by 100%. If neither condition is met, Soppo gains 2 stacks of Permanent Hunting Mark.\n\nAfter performing an active attack, Soppo gains Rabid Factor, increasing her critical damage dealt (up to a maximum of 10 stacks). When she has 4 stacks of Rabid Factor, she gains Rabid Factor I. When she has 6 stacks of Rabid Factor, she gains Rabid Factor II. When she has 8 or more stacks of Rabid Factor, she gains Rabid Factor III.\n\n[Rabid Factor I]: When attacking an enemy target on a phase tile with active attacks, ignores 10% of the target's defense. For each level of the tile, ignores an additional 10% of the target's defense.\n[Rabid Factor II]: For each Freeze or Burn buff on Soppo, Freeze and Burn damage dealt is increased by 5%.\n[Rabid Factor III]: Before dealing damage, generates Frost tiles around the target. If Soppo is in Mad Dog Mode, instead generates Incineration tiles. Damage dealt to enemy targets on phase tiles is increased by 15%. For each level of the tile, damage dealt is further increased by 10%.",
        "icon": "assets/images/characters/soppo/passive.png",
        "range_image": "assets/images/characters/soppo/passive-range.png",
        "range": "Self"
    }
]

soppo_char["fortification"] = [
    {
        "tier": 1,
        "skill": "Vicious Bite",
        "level": 2,
        "effect": "The damage multiplier is increased to 130%.\nIf in Hunting Hound Mode, gains 2 stacks of Hunting Mark after attacking, and gains Extra Action instead of Extra Command."
    },
    {
        "tier": 2,
        "skill": "Lunar Howl",
        "level": 2,
        "effect": "After moving onto the target tile, if that tile is a Freeze or Burn tile, deals Freeze damage or Burn damage equal to 80% of attack to the 3 nearest enemy targets within 8 tiles.\nIf that tile is an Ashen (Freeze-Burn) tile, instead deals 1 instance of Freeze damage and 1 instance of Burn damage, each equal to 80% of attack, to the 3 nearest enemy targets within 8 tiles.\nIf in Mad Dog Mode, gains 1 stack of Hunting Mark after skill usage."
    },
    {
        "tier": 3,
        "skill": "Lunar Howl",
        "level": 3,
        "effect": "The effect of Slaughtertrail is enhanced: the range for creating Frost tiles is increased by 2 tiles; before performing an active attack, Soppo gains 1 stack of Rabid Factor.\nIf in Mad Dog Mode, the damage multiplier is increased to 150%. If the enemy target is standing on a Level 1 tile, the damage is increased by 10%; for every 1 tile level, the damage is further increased by 10%."
    },
    {
        "tier": 4,
        "skill": "Vampup Syndrome",
        "level": 2,
        "effect": "The damage increase from team conditions against enemy targets is raised to 150% and no longer requires the target to have any debuffs. The number of Permanent Hunting Mark stacks gained is increased by 2."
    },
    {
        "tier": 5,
        "skill": "Fatal Pounce",
        "level": 2,
        "effect": "The multiplier is increased to number of Hunting Mark stacks × 50% of attack. When using this skill, consumes all Confectance Index; for each additional 1 point of Confectance Index consumed, the base multiplier is increased by 5%. After skill usage, restores 2 points of Confectance Index.\nAfter triggering Interception, gains 2 stacks of Hunting Mark. The damage multiplier of Interception is increased to 60%."
    },
    {
        "tier": 6,
        "skill": "Vampup Syndrome",
        "level": 3,
        "effect": "At the start of battle, gains 3 stacks of Rabid Factor.\nThe maximum number of Rabid Factor stacks is increased to 20, and after performing an active attack, the number of Rabid Factor stacks gained is additionally increased by 1.\nIn addition, when Rabid Factor reaches 20 stacks, its effects are enhanced:\nRabid Factor I — when actively attacking an enemy target standing on a phase tile, defense ignore is increased to 20%;\nRabid Factor II — the increase to Freeze damage and Burn damage is raised to 10%;\nRabid Factor III — when attacking an enemy target standing on a phase tile, the damage increase is raised to 30%."
    }
]

soppo_char["keys"] = [
    {
        "name": "Fixed Key 1 - This Is My Turf",
        "level": 20,
        "effect": "At the start of the battle, gains Rabid Factor.",
        "materials": "3\n\n\n3000",
        "image": "assets/images/characters/soppo/fixed (1).png"
    },
    {
        "name": "Fixed Key 2 - Beware of Sopdog",
        "level": 20,
        "effect": "After attacking enemy targets on phase tiles, cleanses a buff from them.",
        "materials": "3\n\n\n3000",
        "image": "assets/images/characters/soppo/fixed (2).png"
    },
    {
        "name": "Fixed Key 3 - Cocytus",
        "level": 30,
        "effect": "At the start of the turn, Soppo generates [Frost] tiles around of herself.",
        "materials": "3\n\n\n8000",
        "image": "assets/images/characters/soppo/fixed (3).png"
    },
    {
        "name": "Fixed Key 4 - Licking Wounds",
        "level": 30,
        "effect": "If Soppo takes damage while she is on a phase tile, damage and stability damage taken is reduced.",
        "materials": "3\n\n\n8000",
        "image": "assets/images/characters/soppo/fixed (4).png"
    },
    {
        "name": "Fixed Key 5 - Unfettered Bloodlust",
        "level": 40,
        "effect": "When Soppo has a shield, Freeze damage and Burn damage dealt is increased.",
        "materials": "3\n\n\n12000",
        "image": "assets/images/characters/soppo/fixed (5).png"
    },
    {
        "name": "Fixed Key 6 - Group Coordination",
        "level": 40,
        "effect": "After an allied unit (excluding Soppo herself) performs an out-of-turn attack, Soppo gains any missing effects among [Blazing Assault I] and [Boreal Assault].",
        "materials": "3\n\n\n12000",
        "image": "assets/images/characters/soppo/fixed (6).png"
    },
    {
        "name": "Affinity Key - Frolic chord",
        "level": "-",
        "effect": "ATK +3%, HP +3%, CRIT +3%",
        "materials": "Unlocked at Affinity Lvl 5",
        "image": "assets/images/characters/soppo/affi.png"
    },
    {
        "name": "Common Key - Call of the Wild",
        "level": 40,
        "effect": "When attacking an enemy unit on a Freeze or Burn tile, phase damage dealt is increased.",
        "materials": "None",
        "image": "assets/images/characters/soppo/common.png"
    }
]

soppo_char_path.write_text(json.dumps(soppo_char, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated data/characters/soppo.json")

# 3. Update data/i18n_vi.json
i18n_path = ROOT / "data" / "i18n_vi.json"
i18n_data = json.loads(i18n_path.read_text(encoding="utf-8"))

# Sync effects in i18n_data
if "effects" in i18n_data:
    for eid, patch in effects_to_update.items():
        if eid in i18n_data["effects"]:
            i18n_data["effects"][eid].update(patch)

soppo_vi = i18n_data["characters"]["soppo"]
soppo_vi["skills"] = [
    {
        "name": "Nanh Săn Mồi",
        "tags": [
            "Đánh Thường",
            "Chuẩn Xác"
        ],
        "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Băng Kết bằng <color=#f26c1c>80%</color> Tấn Công. Soppo nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu và <color=#f26c1c>2 tầng</color> <color=#3487e0>Dấu Ấn Săn Mồi</color>. Nếu Soppo đang ở <color=#3487e0>Chế Độ Chó Điên</color>, kỹ năng này sẽ chuyển sang gây ST Thiêu Đốt.\n\n<color=#3487e0>Chế Độ Chó Điên</color>: Ở trạng thái này, một số kỹ năng chuyển sang gây ST Thiêu Đốt. Có thể chuyển sang <color=#3487e0>Chế Độ Chó Săn</color>.\n<color=#3487e0>Chế Độ Chó Săn</color>: Ở trạng thái này, một số kỹ năng gây ST Băng Kết. Có thể chuyển sang <color=#3487e0>Chế Độ Chó Điên</color>."
    },
    {
        "name": "Cắn Xé Hung Bạo",
        "tags": [
            "Chủ Động",
            "Phạm Vi",
            "Ô Địa Hình"
        ],
        "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Băng Kết phạm vi bằng <color=#f26c1c>80%</color> Tấn Công lên mục tiêu và tất cả mục tiêu địch trong bán kính <color=#f26c1c>3 ô</color> xung quanh, đồng thời tạo các ô địa hình <color=#3487e0>Băng Giá</color> duy trì <color=#f26c1c>2 hiệp</color>. Sau kỹ năng này, Soppo thực hiện đòn đánh thường Nanh Săn Mồi lên mục tiêu địch gần nhất <color=#f26c1c>trong phạm vi 8 ô</color> và nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>.\nNếu Soppo đang ở <color=#3487e0>Chế Độ Chó Điên</color>, kỹ năng này chuyển sang gây ST Thiêu Đốt phạm vi và tạo các ô địa hình <color=#3487e0>Thiêu Rụi</color>. Soppo không nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
    },
    {
        "name": "Tiếng Hú Ánh Trăng",
        "tags": [
            "Chủ Động",
            "Phạm Vi"
        ],
        "description": "Đáp xuống ô trống mang thuộc tính Băng Kết hoặc Thiêu Đốt được chọn trên chiến trường và áp dụng <color=#3487e0>Dấu Vết Tàn Sát</color> cho tất cả Búp Bê đồng minh xung quanh trong bán kính <color=#f26c1c>8 ô</color> (ngoại trừ bản thân Soppo) duy trì <color=#f26c1c>3 hiệp</color>, cho phép họ tạo các ô địa hình <color=#3487e0>Băng Giá</color> xung quanh mục tiêu sau khi thực hiện tấn công chủ động; và sát thương gây ra cho các đơn vị địch đứng trên ô địa hình Dị Vị được tăng thêm. Sau kỹ năng này, Soppo chuyển sang <color=#3487e0>Chế Độ Chó Điên</color>.\n\nNếu Soppo đang ở <color=#3487e0>Chế Độ Chó Điên</color>, chuyển sang gây ST Thiêu Đốt phạm vi bằng <color=#f26c1c>120%</color> Tấn Công lên tất cả mục tiêu địch xung quanh trong bán kính <color=#f26c1c>4 ô</color>. Sát thương này được chia đều cho tất cả mục tiêu trong phạm vi hiệu lực. Sau kỹ năng này, Soppo thực hiện đòn đánh thường Nanh Săn Mồi lên mục tiêu địch gần nhất <color=#f26c1c>trong phạm vi 8 ô</color> và nhận <color=#3487e0>Tăng Hành Động</color>."
    },
    {
        "name": "Vồ Mồi Chí Mạng",
        "tags": [
            "Tuyệt Kỹ",
            "Phạm Vi",
            "Chặn Đánh"
        ],
        "description": "Tiêu hao toàn bộ số tầng <color=#3487e0>Dấu Ấn Săn Mồi</color> và gây ST Băng Kết phạm vi bằng số tầng Dấu Ấn Săn Mồi × <color=#f26c1c>30%</color> Tấn Công lên các mục tiêu trong bán kính <color=#f26c1c>6 ô</color>. Nếu đòn đánh này trúng mục tiêu địch đang đứng trên ô địa hình Dị Vị, gây thêm <color=#f26c1c>1 lần</color> ST Băng Kết bằng <color=#f26c1c>50%</color> Tấn Công lên mục tiêu đó. Sau kỹ năng này, Soppo chuyển sang <color=#3487e0>Chế Độ Chó Săn</color>.\n\nBị động: Trước khi đơn vị địch xung quanh <color=#f26c1c>trong phạm vi 8 ô</color> tung đòn tấn công chủ động, kích hoạt <color=#3487e0>Chặn Đánh</color> lên chúng, gây ST Băng Kết bằng <color=#f26c1c>30%</color> Tấn Công và <color=#f26c1c>4 điểm</color> ST Ổn Định. Chỉ có thể kích hoạt tối đa <color=#f26c1c>1 lần</color> mỗi hiệp."
    },
    {
        "name": "Hội Chứng Vampup",
        "tags": [
            "Bị Động"
        ],
        "description": "Khi bắt đầu trận chiến, Soppo khởi đầu ở <color=#3487e0>Chế Độ Chó Săn</color> và tiêu hao <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu để nhận <color=#3487e0>Lá Chắn Hàn Sương</color> duy trì <color=#f26c1c>3 hiệp</color>. Lá Chắn Hàn Sương hấp thụ lượng sát thương bằng <color=#f26c1c>65%</color> Tấn Công ban đầu, tối đa không quá <color=#f26c1c>60%</color> HP tối đa.\n\nKhi bắt đầu trận chiến, nếu có từ <color=#f26c1c>3</color> Búp Bê đồng minh hệ Thiêu Đốt trở lên trên chiến trường (ngoại trừ bản thân Soppo), thì khi dùng đòn đánh thường Nanh Săn Mồi hoặc kỹ năng chủ động Cắn Xé Hung Bạo và đang ở <color=#3487e0>Chế Độ Chó Săn</color>, sát thương gây ra lên mục tiêu địch chịu Debuff Thiêu Đốt được tăng thêm <color=#f26c1c>100%</color>. Nếu có từ <color=#f26c1c>3</color> Búp Bê đồng minh hệ Băng Kết trở lên trên chiến trường (ngoại trừ bản thân Soppo), thì khi dùng các kỹ năng nói trên hoặc kỹ năng chủ động Tiếng Hú Ánh Trăng và đang ở <color=#3487e0>Chế Độ Chó Điên</color>, sát thương gây ra lên mục tiêu địch chịu Debuff Băng Kết được tăng thêm <color=#f26c1c>100%</color>. Nếu không thỏa mãn điều kiện nào, Soppo nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Dấu Ấn Săn Mồi Vĩnh Viễn</color>.\n\nSau khi thực hiện tấn công chủ động, Soppo nhận <color=#3487e0>Nhân Tố Cuồng Bạo</color>, tăng sát thương Bạo Kích gây ra (tối đa <color=#f26c1c>10 tầng</color>). Khi đạt <color=#f26c1c>4 tầng</color> Nhân Tố Cuồng Bạo, nhận <color=#3487e0>Nhân Tố Cuồng Bạo I</color>. Khi đạt <color=#f26c1c>6 tầng</color> Nhân Tố Cuồng Bạo, nhận <color=#3487e0>Nhân Tố Cuồng Bạo II</color>. Khi đạt từ <color=#f26c1c>8 tầng</color> Nhân Tố Cuồng Bạo trở lên, nhận <color=#3487e0>Nhân Tố Cuồng Bạo III</color>.\n\n<color=#3487e0>Nhân Tố Cuồng Bạo I</color>: Khi tấn công mục tiêu địch trên ô địa hình Dị Vị bằng tấn công chủ động, bỏ qua <color=#f26c1c>10%</color> Phòng Thủ của mục tiêu. Mỗi cấp của ô địa hình bỏ qua thêm <color=#f26c1c>10%</color> Phòng Thủ của mục tiêu.\n<color=#3487e0>Nhân Tố Cuồng Bạo II</color>: Với mỗi Buff Băng Kết hoặc Thiêu Đốt trên bản thân Soppo, ST Băng Kết và ST Thiêu Đốt gây ra được tăng thêm <color=#f26c1c>5%</color>.\n<color=#3487e0>Nhân Tố Cuồng Bạo III</color>: Trước khi gây sát thương, tạo các ô địa hình <color=#3487e0>Băng Giá</color> xung quanh mục tiêu. Nếu Soppo đang ở <color=#3487e0>Chế Độ Chó Điên</color>, thay vào đó sẽ tạo các ô địa hình <color=#3487e0>Thiêu Rụi</color>. Sát thương gây ra lên mục tiêu địch trên ô địa hình Dị Vị tăng <color=#f26c1c>15%</color>. Mỗi cấp của ô địa hình, sát thương gây ra được tăng thêm <color=#f26c1c>10%</color>."
    }
]

soppo_vi["fortification"] = [
    {
        "tier": 1,
        "level": 2,
        "skill": "Cắn Xé Hung Bạo",
        "effect": "Hệ số sát thương tăng lên <color=#f26c1c>130%</color>.\nNếu đang ở <color=#3487e0>Chế Độ Chó Săn</color>, nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Dấu Ấn Săn Mồi</color> sau khi tấn công, và nhận <color=#3487e0>Tăng Hành Động</color> thay vì <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
    },
    {
        "tier": 2,
        "level": 2,
        "skill": "Tiếng Hú Ánh Trăng",
        "effect": "Sau khi di chuyển đến ô chỉ định, nếu ô đó là ô loại <color=#3487e0>Băng Giá</color> hoặc <color=#3487e0>Thiêu Đốt</color>, gây ST Băng Kết hoặc ST Thiêu Đốt bằng <color=#f26c1c>80%</color> Tấn Công lên <color=#f26c1c>3 mục tiêu</color> địch gần nhất <color=#f26c1c>trong phạm vi 8 ô</color>.\nNếu ô đó là ô Tro Tàn (Băng-Nhiệt), sẽ gây đồng thời <color=#f26c1c>1 lần</color> ST Băng Kết và <color=#f26c1c>1 lần</color> ST Thiêu Đốt, mỗi lần bằng <color=#f26c1c>80%</color> Tấn Công lên 3 mục tiêu địch gần nhất trong phạm vi 8 ô.\nNếu đang ở <color=#3487e0>Chế Độ Chó Điên</color>, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Dấu Ấn Săn Mồi</color> sau khi dùng kỹ năng."
    },
    {
        "tier": 3,
        "level": 2,
        "skill": "Tiếng Hú Ánh Trăng",
        "effect": "Hiệu ứng của <color=#3487e0>Dấu Vết Tàn Sát</color> được cường hóa: phạm vi tạo ô <color=#3487e0>Băng Giá</color> tăng thêm <color=#f26c1c>2 ô</color>; trước khi chủ động tấn công, Soppo nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Nhân Tố Cuồng Bạo</color>.\nNếu đang ở <color=#3487e0>Chế Độ Chó Điên</color>, hệ số sát thương tăng lên <color=#f26c1c>150%</color>. Nếu mục tiêu địch đang đứng trên ô địa hình Cấp 1, sát thương tăng thêm <color=#f26c1c>10%</color>; mỗi cấp ô địa hình tăng thêm, sát thương tăng thêm <color=#f26c1c>10%</color>."
    },
    {
        "tier": 4,
        "level": 2,
        "skill": "Hội Chứng Vampup",
        "effect": "Lượng sát thương tăng theo điều kiện đội hình lên mục tiêu địch tăng lên <color=#f26c1c>150%</color> và không còn yêu cầu mục tiêu phải chịu bất kỳ Debuff nào. Số tầng <color=#3487e0>Dấu Ấn Săn Mồi Vĩnh Viễn</color> nhận được tăng thêm <color=#f26c1c>2 tầng</color>."
    },
    {
        "tier": 5,
        "level": 2,
        "skill": "Vồ Mồi Chí Mạng",
        "effect": "Hệ số sát thương tăng lên số tầng Dấu Ấn Săn Mồi × <color=#f26c1c>50%</color> Tấn Công. Khi sử dụng kỹ năng này, tiêu hao toàn bộ Chỉ Số Nhiên Liệu; với mỗi <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu tiêu hao thêm, hệ số cơ bản tăng thêm <color=#f26c1c>5%</color>. Sau khi dùng kỹ năng, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.\nSau khi kích hoạt <color=#3487e0>Chặn Đánh</color>, nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Dấu Ấn Săn Mồi</color>. Hệ số sát thương của Chặn Đánh tăng lên <color=#f26c1c>60%</color>."
    },
    {
        "tier": 6,
        "level": 3,
        "skill": "Hội Chứng Vampup",
        "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 tầng</color> <color=#3487e0>Nhân Tố Cuồng Bạo</color>.\nSố tầng tối đa của Nhân Tố Cuồng Bạo tăng lên <color=#f26c1c>20 tầng</color>, và sau khi chủ động tấn công, số tầng Nhân Tố Cuồng Bạo nhận được tăng thêm <color=#f26c1c>1 tầng</color>.\nNgoài ra, khi Nhân Tố Cuồng Bạo đạt 20 tầng, các hiệu ứng được cường hóa:\n<color=#3487e0>Nhân Tố Cuồng Bạo I</color> — khi chủ động tấn công mục tiêu địch đang đứng trên ô địa hình Dị Vị, bỏ qua Phòng Thủ tăng lên <color=#f26c1c>20%</color>;\n<color=#3487e0>Nhân Tố Cuồng Bạo II</color> — lượng tăng ST Băng Kết và ST Thiêu Đốt nâng lên <color=#f26c1c>10%</color>;\n<color=#3487e0>Nhân Tố Cuồng Bạo III</color> — khi tấn công mục tiêu địch đang đứng trên ô địa hình Dị Vị, lượng sát thương tăng lên <color=#f26c1c>30%</color>."
    }
]

soppo_vi["keys"] = [
    {
        "name": "Khóa Cố Định 1 - Lãnh Địa Của Ta",
        "effect": "Khi bắt đầu trận chiến, nhận <color=#3487e0>Nhân Tố Cuồng Bạo</color>."
    },
    {
        "name": "Khóa Cố Định 2 - Coi Chừng Sopdog",
        "effect": "Sau khi tấn công mục tiêu địch đang đứng trên ô địa hình Dị Vị, thanh tẩy <color=#f26c1c>1</color> Buff của mục tiêu."
    },
    {
        "name": "Khóa Cố Định 3 - Cocytus",
        "effect": "Khi bắt đầu hiệp, Soppo tạo các ô địa hình <color=#3487e0>Băng Giá</color> xung quanh bản thân."
    },
    {
        "name": "Khóa Cố Định 4 - Liếm Vết Thương",
        "effect": "Nếu Soppo chịu sát thương khi đang đứng trên ô địa hình Dị Vị, sát thương và ST Ổn Định phải chịu sẽ giảm."
    },
    {
        "name": "Khóa Cố Định 5 - Khát Máu Vô Song",
        "effect": "Khi Soppo sở hữu Khiên, ST Băng Kết và ST Thiêu Đốt gây ra được tăng thêm."
    },
    {
        "name": "Khóa Cố Định 6 - Phối Hợp Tác Chiến",
        "effect": "Sau khi một đơn vị đồng minh (ngoại trừ Soppo) thực hiện <color=#3487e0>Đòn Đánh Ngoài Lượt</color>, Soppo nhận bất kỳ hiệu ứng nào còn thiếu trong số <color=#3487e0>Thế Công Rực Lửa I</color> và <color=#3487e0>Xung Kích Băng Kết</color>."
    },
    {
        "name": "Khóa Tương Thích - Giai Điệu Vui Vẻ",
        "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%"
    },
    {
        "name": "Khóa Chung - Tiếng Gọi Hoang Dã",
        "effect": "Khi tấn công một đơn vị địch trên ô Băng Kết hoặc Thiêu Đốt, sát thương Dị Vị gây ra được tăng thêm."
    }
]

i18n_path.write_text(json.dumps(i18n_data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated data/i18n_vi.json")

# 4. Update site/static/js/i18n-vi.js
i18n_js_path = ROOT / "site" / "static" / "js" / "i18n-vi.js"
js_content = "// Auto-generated Vietnamese Localization Bundle for GFL2: Exilium Wiki\nwindow.GFL2_I18N_VI = " + json.dumps(i18n_data, ensure_ascii=False, indent=2) + ";\n"
i18n_js_path.write_text(js_content, encoding="utf-8")
print("Updated site/static/js/i18n-vi.js")

# 5. Update data/guides/soppo.json
guide_path = ROOT / "data" / "guides" / "soppo.json"
if guide_path.exists():
    guide_content = guide_path.read_text(encoding="utf-8")
    replacements = [
        ("Dạng Thợ Săn", "Chế Độ Chó Săn"),
        ("Dạng Dã Thú", "Chế Độ Chó Điên"),
        ("Tiếng Hú Nửa Đêm", "Tiếng Hú Ánh Trăng"),
        ("Dấu Ấn Thợ Săn", "Dấu Ấn Săn Mồi"),
        ("Truy Lùng Con Mồi", "Nanh Săn Mồi"),
        ("Hội Chứng Chó Điên", "Hội Chứng Vampup"),
        ("Muốn Thêm Miếng Nữa Không?", "Coi Chừng Sopdog"),
        ("Địa Ngục Băng Giá", "Cocytus"),
        ("Khôi Phục Lãnh Thổ", "Liếm Vết Thương"),
        ("Cơn Say Sát Nhân", "Khát Máu Vô Song"),
        ("Sức Mạnh Bầy Đàn", "Phối Hợp Tác Chiến"),
    ]
    for old_s, new_s in replacements:
        guide_content = guide_content.replace(old_s, new_s)
    guide_path.write_text(guide_content, encoding="utf-8")
    print("Updated data/guides/soppo.json")

print("All Soppo files successfully patched!")
