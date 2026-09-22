import json
from pathlib import Path
import sys
sys.path.insert(0, ".")

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_core.bundle import stage_i18n_bundle

ROOT = Path(".")
i18n_path = ROOT / "data" / "i18n_vi.json"
with open(i18n_path, "r", encoding="utf-8") as f:
    bundle = json.load(f)

# 1. Update weapons in i18n
bundle.setdefault("weapons", {})
bundle["weapons"]["snotra"] = {
    "name": "Snotra",
    "weapon_type": "Súng Trường Tấn Công",
    "rarity": "SSR",
    "stats": "Tấn Công +383\nTăng Tấn Công +15%",
    "trait": "Khi có Khiên bảo vệ, sát thương gây ra tăng 5%; nếu gây sát thương Thiêu Đốt, tăng thêm 5% nữa.",
    "effect": "Khi có Khiên bảo vệ, sát thương gây ra tăng 20/24/28/32/36/40% và sát thương bạo kích tăng 15%. Sau khi Đòn Đánh Hỗ Trợ gây sát thương Thiêu Đốt, nhận 3 điểm Chỉ Số Nhiên Liệu. Hiệu quả này có thể kích hoạt 1 lần mỗi hiệp.\n\nKỹ Năng Khắc Ấn: Sát thương gây ra lên mục tiêu chịu debuff Thiêu Đốt tăng 2.5%. Sát thương gây ra lên Paradeus tăng 2.5%.",
    "server": "cn"
}

bundle["weapons"]["silent-conviction"] = {
    "name": "Silent Conviction",
    "weapon_type": "Súng Lục",
    "rarity": "SSR",
    "stats": "Tấn Công +313\nTăng Tấn Công +15%",
    "trait": "Khi lượng sát thương gánh chịu tích lũy bằng 30% HP tối đa ban đầu, sát thương gây ra tăng 10%.",
    "effect": "HP tối đa của bản thân tăng 15/20/25/30/35/40%. Sát thương gây ra tăng 15/20/25/30/35/40% và sát thương gây ra lên mục tiêu chịu debuff Ăn Mòn tăng 10%.\n\nKỹ Năng Khắc Ấn: Sát thương gây ra lên đơn vị Kỹ Thuật Sycca tăng 2.5%. Nếu mục tiêu có debuff Ăn Mòn, tăng thêm 2.5% sát thương nữa.",
    "server": "cn"
}

# 2. Add Cecilia to i18n
bundle.setdefault("characters", {})
bundle["characters"]["cecilia"] = {
    "name": "Cecilia",
    "title": "Người Lắng Nghe",
    "class": "Lính Gác",
    "rarity": "Ưu Tú",
    "phase": "Thiêu Đốt",
    "weapon_type": "Súng Trường Tấn Công",
    "ammo_type": "Đạn Vừa",
    "signature_weapon": "Snotra",
    "stability_gauge": "9 điểm",
    "movement_speed": "6 ô",
    "server": "cn",
    "quote": "Bình tĩnh nào, mọi chuyện rồi sẽ ổn thỏa cả thôi. Hãy để tôi lắng nghe tiếng lòng của bạn.",
    "skills": [
        {
            "name": "Lời An Ủi",
            "tags": ["Đánh Thường", "Chỉ Định"],
            "stability_damage": 3,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": 8,
            "effect_area": "Mục Tiêu",
            "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công lên mục tiêu đó."
        },
        {
            "name": "Lời An Ủi - Lan",
            "tags": ["Đánh Thường", "AoE"],
            "stability_damage": 3,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": 8,
            "effect_area": "5x5 ô",
            "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST <color=#ed4f12>Thiêu Đốt</color> AoE bằng <color=#f26c1c>70%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 5x5 ô xung quanh mục tiêu đó. Áp dụng <color=#3487e0>Cháy Bỏng</color> và <color=#3487e0>Bực Bội</color> trong <color=#f26c1c>2 hiệp</color>, đồng thời tạo ô địa hình <color=#3487e0>Thiêu Đốt</color> trong <color=#f26c1c>2 hiệp</color>."
        },
        {
            "name": "Lời An Ủi - Chuẩn Xác",
            "tags": ["Đánh Thường", "Chỉ Định"],
            "stability_damage": 3,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": 8,
            "effect_area": "Mục Tiêu",
            "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST <color=#ed4f12>Thiêu Đốt</color> bằng <color=#f26c1c>100%</color> Tấn Công lên mục tiêu đó. Áp dụng <color=#3487e0>Cháy Bỏng</color> trong <color=#f26c1c>2 hiệp</color>. Nhận <color=#3487e0>Tự Ám Thị</color> trong <color=#f26c1c>3 hiệp</color>."
        },
        {
            "name": "Nguyên Tắc An Toàn Là Trên Hết",
            "tags": ["Bị Động", "Cường Hóa"],
            "stability_damage": 0,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": "Bản thân",
            "effect_area": "Bản thân",
            "description": "Khi bắt đầu trận chiến, nhận <color=#3487e0>Dẫn Nhiệt</color>. Khi đòn đánh thường hoặc <color=#3487e0>Hành Động Hỗ Trợ</color> gây sát thương diện rộng, nhận <color=#f26c1c>6 điểm</color> <color=#3487e0>Lửa Thiêu</color>. Khi đòn đánh thường hoặc <color=#3487e0>Hành Động Hỗ Trợ</color> gây sát thương chuẩn xác, nhận <color=#f26c1c>3 điểm</color> <color=#3487e0>Lửa Thiêu</color>.\nKhi nhận <color=#3487e0>Tâm Trí Bền Bỉ</color>, chuyển hóa thành một lượng tương đương <color=#3487e0>Tâm Trí Kiên Định</color> trong <color=#f26c1c>2 hiệp</color>.\nKhi một đơn vị địch trong tầm đánh chịu sát thương chuẩn xác từ đồng minh, nếu Cecilia đang có Lời An Ủi - Lan hoặc Lời An Ủi - Chuẩn Xác, tiêu hao <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu và thực hiện <color=#f26c1c>1 lần</color> <color=#3487e0>Hành Động Hỗ Trợ</color> lên kẻ đó, tạo hiệu quả kỹ năng tương đương với Lời An Ủi hiện tại. Kích hoạt tối đa <color=#f26c1c>3 lần</color> mỗi hiệp.\nSau khi <color=#3487e0>Hành Động Hỗ Trợ</color> kết thúc, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Tận Tụy Cống Hiến</color> trong <color=#f26c1c>2 hiệp</color> và <color=#3487e0>Tâm Trí Bền Bỉ</color> trong <color=#f26c1c>2 hiệp</color>. Lượng hấp thụ của <color=#3487e0>Tâm Trí Bền Bỉ</color> bằng <color=#f26c1c>50%</color> Tấn Công của người thi triển, tối đa <color=#f26c1c>100%</color> HP tối đa mục tiêu, không cộng dồn; đồng thời áp dụng <color=#3487e0>Cộng Hưởng Đôi</color> lên các Doll đồng minh khác trong <color=#f26c1c>2 hiệp</color>.\nVới mỗi lần thực hiện <color=#3487e0>Hành Động Hỗ Trợ</color>, khi bắt đầu hiệp kế tiếp sẽ nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.\nKhi Centaureissi ra trận, sát thương và lượng hồi máu do cô ấy gây ra tăng <color=#f26c1c>100%</color>, hệ số sát thương đánh thường và <color=#3487e0>Hành Động Hỗ Trợ</color> của Cecilia tăng <color=#f26c1c>30%</color>. Cecilia cũng có thể nhận <color=#3487e0>Ánh Mắt Cảnh Giác</color> do Centaureissi áp dụng."
        },
        {
            "name": "Hòa Giải Mang Tính Xây Dựng",
            "tags": ["Chủ Động", "Cường Hóa"],
            "stability_damage": 0,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": "Bản thân",
            "effect_area": "Toàn Đội",
            "description": "Đánh thường Lời An Ủi chuyển thành Lời An Ủi - Lan trong <color=#f26c1c>1 hiệp</color>.\nNhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color> và trao <color=#3487e0>Tâm Trí Bền Bỉ</color> cho toàn bộ Doll đồng minh trong <color=#f26c1c>2 hiệp</color>. Kỹ năng này hoặc kỹ năng chủ động Liệu Pháp Giảm Mẫn Cảm có thể dùng tối đa <color=#f26c1c>1 lần</color> mỗi hiệp."
        },
        {
            "name": "Liệu Pháp Giảm Mẫn Cảm",
            "tags": ["Chủ Động", "Cường Hóa"],
            "stability_damage": 0,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": "Bản thân",
            "effect_area": "Toàn Đội",
            "description": "Đánh thường Lời An Ủi chuyển thành Lời An Ủi - Chuẩn Xác trong <color=#f26c1c>1 hiệp</color>.\nNhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color> và trao <color=#3487e0>Tâm Trí Bền Bỉ</color> cho toàn bộ Doll đồng minh trong <color=#f26c1c>2 hiệp</color>. Kỹ năng này hoặc kỹ năng chủ động Hòa Giải Mang Tính Xây Dựng có thể dùng tối đa <color=#f26c1c>1 lần</color> mỗi hiệp."
        },
        {
            "name": "Hàn Gắn Mối Quan Hệ",
            "tags": ["Tuyệt Kỹ", "Chỉ Định"],
            "stability_damage": 5,
            "cooldown": "2 hiệp",
            "confectance_cost": 0,
            "range": 8,
            "effect_area": "Mục Tiêu",
            "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST <color=#ed4f12>Thiêu Đốt</color> bằng <color=#f26c1c>130%</color> Tấn Công lên mục tiêu đó.\nNhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>.\nCứ mỗi đòn đánh thường hoặc <color=#3487e0>Hành Động Hỗ Trợ</color> đã thực hiện, hệ số sát thương của lần thi triển kế tiếp của kỹ năng này tăng thêm <color=#f26c1c>25%</color>."
        }
    ],
    "keys": [
        {
            "name": "Khóa Cố Định 1 - Cảm Xúc Ổn Định",
            "level": 20,
            "effect": "Nhận 3 điểm Chỉ Số Nhiên Liệu khi bắt đầu trận chiến."
        },
        {
            "name": "Khóa Cố Định 2 - Lực Hút Thân Thiện",
            "level": 20,
            "effect": "Trước khi thực hiện đòn đánh thường, thanh tẩy 1 buff trên mục tiêu địch."
        },
        {
            "name": "Khóa Cố Định 3 - Khéo Léo Chuyển Mình",
            "level": 30,
            "effect": "Sau khi dùng đòn đánh thường Lời An Ủi, nhận 4 ô Di Chuyển Bổ Sung và tự thanh tẩy 1 debuff trên bản thân."
        },
        {
            "name": "Khóa Cố Định 4 - Ngụy Trang Vô Hại",
            "level": 30,
            "effect": "Sau khi kết thúc hành động, nhận <color=#3487e0>Tâm Trí Bền Bỉ</color> trong 2 hiệp."
        },
        {
            "name": "Khóa Cố Định 5 - Thấu Thị Trí Mạng",
            "level": 40,
            "effect": "Khi sở hữu <color=#3487e0>Tâm Trí Kiên Định</color>, sát thương Thiêu Đốt gây ra từ <color=#3487e0>Tấn Công Ngoài Lượt</color> tăng 15%."
        },
        {
            "name": "Khóa Cố Định 6 - Tự Tạo Động Lực",
            "level": 40,
            "effect": "Trước khi gây sát thương diện rộng, nhận <color=#3487e0>Tăng Sát Thương Lan II</color> trong 2 hiệp. Trước khi gây sát thương chuẩn xác, nhận <color=#3487e0>Tăng Sát Thương Chuẩn Xác II</color> trong 2 hiệp."
        },
        {
            "name": "Khóa Đồng Điệu - Liệu Pháp ASMR",
            "level": 1,
            "effect": "Tăng cường khả năng phối hợp tác chiến và tương tác cảm xúc cùng Chỉ Huy."
        },
        {
            "name": "Khóa Đa Năng - Thấu Hiểu Là Sức Mạnh",
            "level": 40,
            "effect": "Khi đơn vị này sở hữu hiệu ứng <color=#3487e0>Khiên</color>, sát thương Thiêu Đốt gây ra tăng 10%."
        }
    ],
    "fortification": [
        {
            "tier": 1,
            "skill": "Hòa Giải Mang Tính Xây Dựng",
            "level": 2,
            "effect": "Hệ số sát thương của Lời An Ủi - Lan tăng lên <color=#f26c1c>100%</color>.\nCường hóa hiệu ứng <color=#3487e0>Bực Bội</color>: Sát thương gánh chịu từ Cecilia tăng lên <color=#f26c1c>60%</color>."
        },
        {
            "tier": 2,
            "skill": "Liệu Pháp Giảm Mẫn Cảm",
            "level": 2,
            "effect": "Hệ số sát thương của Lời An Ủi - Chuẩn Xác tăng lên <color=#f26c1c>130%</color> và tạo ô địa hình <color=#3487e0>Thiêu Đốt</color> trong phạm vi 2 ô trong <color=#f26c1c>2 hiệp</color>.\nCường hóa hiệu ứng <color=#3487e0>Tự Ám Thị</color>: Sát thương Thiêu Đốt gây ra tăng <color=#f26c1c>30%</color>, tỷ lệ bạo kích tăng <color=#f26c1c>50%</color>, sát thương bạo kích tăng <color=#f26c1c>50%</color>."
        },
        {
            "tier": 3,
            "skill": "Hàn Gắn Mối Quan Hệ",
            "level": 2,
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>160%</color>, và mức tăng hệ số sát thương cộng thêm nâng lên <color=#f26c1c>50%</color>.\nTrước khi kỹ năng giải quyết, áp dụng <color=#3487e0>Dễ Tổn Thương II</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>.\nThời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>."
        },
        {
            "tier": 4,
            "skill": "Nguyên Tắc An Toàn Là Trên Hết",
            "level": 2,
            "effect": "Sát thương gây ra bởi <color=#3487e0>Hành Động Hỗ Trợ</color> tăng <color=#f26c1c>40%</color> và sát thương ổn định gây ra tăng thêm <color=#f26c1c>2 điểm</color>.\nCường hóa hiệu ứng <color=#3487e0>Cộng Hưởng Đôi</color>: Sát thương Thiêu Đốt gây ra bởi <color=#3487e0>Tấn Công Ngoài Lượt</color> tăng <color=#f26c1c>30%</color> và sát thương ổn định gánh chịu giảm đi <color=#f26c1c>1 điểm</color>."
        },
        {
            "tier": 5,
            "skill": "Hàn Gắn Mối Quan Hệ",
            "level": 3,
            "effect": "Nếu đòn đánh thường Lời An Ủi được sử dụng sau khi kỹ năng này kết thúc, sát thương gây ra tăng <color=#f26c1c>100%</color>. Khi sở hữu <color=#3487e0>Tâm Trí Kiên Định</color>, tỷ lệ bạo kích tăng <color=#f26c1c>100%</color> và sát thương bạo kích tăng <color=#f26c1c>50%</color>, cộng dồn tối đa 2 lần."
        },
        {
            "tier": 6,
            "skill": "Nguyên Tắc An Toàn Là Trên Hết",
            "level": 3,
            "effect": "Giới hạn cộng dồn của <color=#3487e0>Tận Tụy Cống Hiến</color> nâng lên <color=#f26c1c>10 tầng</color>.\nKhi đơn vị địch trong tầm chịu sát thương chuẩn xác từ đồng minh, Cecilia nhận 1 tầng <color=#3487e0>Tận Tụy Cống Hiến</color> trong 2 hiệp.\nNếu tỷ lệ bạo kích của Cecilia vượt quá 100%, lượng vượt mức sẽ chuyển thành tỷ lệ tương đương gia tăng hệ số sát thương đòn đánh thường."
        }
    ],
    "neural_helix": [
        {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +36\nPhòng Ngự +21"},
        {"node": "Cường Hóa 2", "level": 1, "effect": "HP +245\nPhòng Ngự +24"},
        {"node": "Cường Hóa 3", "level": 1, "effect": "Tấn Công +42\nPhòng Ngự +27"},
        {"node": "Cường Hóa 4", "level": 1, "effect": "HP +326\nTấn Công +48"},
        {"node": "Cường Hóa 5", "level": 1, "effect": "Tấn Công +54\nPhòng Ngự +33"},
        {"node": "Cường Hóa 6", "level": 1, "effect": "HP +408\nTấn Công +60\nPhòng Ngự +39"}
    ]
}

# 3. Update Mityl in i18n
bundle["characters"]["mityl"] = {
    "name": "Mityl",
    "title": "Ngôi Sao Đang Lên",
    "class": "Lính Gác",
    "rarity": "Ưu Tú",
    "phase": "Hóa Lỏng",
    "weapon_type": "Tiểu Liên",
    "ammo_type": "Đạn Nhẹ",
    "signature_weapon": "Fluffy Nova",
    "stability_gauge": "9 điểm",
    "movement_speed": "6 ô",
    "server": "cn",
    "quote": "Diễn xuất chính là cuộc sống thứ hai của tôi! Hãy cùng tạo nên một thước phim để đời nào!",
    "skills": [
        {
            "name": "Phục Kích",
            "tags": ["Đánh Thường", "Chỉ Định"],
            "stability_damage": 2,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": 6,
            "effect_area": "Mục Tiêu",
            "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công lên mục tiêu đó."
        },
        {
            "name": "Hình Chiếu Sóc Con",
            "tags": ["Chủ Động", "Ô Địa Hình", "Triệu Hồi", "Dịch Chuyển"],
            "stability_damage": 0,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": 6,
            "effect_area": "Mục Tiêu",
            "description": "Chọn 1 mục tiêu địch trong phạm vi 6 ô (không bao gồm vật triệu hồi), sau đó chọn 1 ô trống trong phạm vi 3 ô xung quanh mục tiêu đó để triệu hồi Hình Chiếu - Mô Phỏng của kẻ địch, đồng thời tạo các ô địa hình <color=#3487e0>Lối Nước</color> trong phạm vi 5 ô xung quanh vật triệu hồi trong <color=#f26c1c>2 hiệp</color>. Tối đa tồn tại 2 Hình Chiếu cùng lúc. Nếu mục tiêu là Doll, Trùm hoặc đơn vị Cỡ Lớn, sẽ triệu hồi Hình Chiếu - Phân Thân thay thế.\nCũng có thể chọn 1 Hình Chiếu trong phạm vi 6 ô và dịch chuyển tức thời nó tới 1 ô trống trong phạm vi 5 ô.\nSau khi thi triển kỹ năng, nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Kích hoạt tối đa 1 lần mỗi hiệp."
        },
        {
            "name": "Phi Thân Nhào Lộn",
            "tags": ["Chủ Động", "Chỉ Định", "Dịch Chuyển"],
            "stability_damage": 3,
            "cooldown": "0 hiệp",
            "confectance_cost": 2,
            "range": 6,
            "effect_area": "Mục Tiêu",
            "description": "Chọn 1 ô trong phạm vi chữ thập từ 3 đến 6 ô và hạ xuống ô đó, gây ST <color=#2caada>Hóa Lỏng</color> bằng <color=#f26c1c>130%</color> Tấn Công lên mục tiêu địch gần nhất trong phạm vi 6 ô xung quanh.\nNếu cả trước khi dùng kỹ năng và khi gây sát thương Mityl đều đứng trên ô địa hình hệ Hóa Lỏng, cô có thể dùng kỹ năng chủ động Phi Thân Nhào Lộn thêm <color=#f26c1c>1 lần</color>, và sát thương gây ra tăng thêm <color=#f26c1c>30%</color>. Kích hoạt 1 lần mỗi hiệp."
        },
        {
            "name": "Hội Tụ Hư Không",
            "tags": ["Tuyệt Kỹ", "Ô Địa Hình", "Cường Hóa"],
            "stability_damage": 0,
            "cooldown": "2 hiệp",
            "confectance_cost": 0,
            "range": "Bản thân",
            "effect_area": "5 ô",
            "description": "Nhận <color=#3487e0>Tràn Bão Hòa</color> trong <color=#f26c1c>2 hiệp</color>. Tạo các ô địa hình <color=#3487e0>Lối Nước</color> trong phạm vi 5 ô xung quanh bản thân trong <color=#f26c1c>2 hiệp</color>.\nSau khi thi triển kỹ năng, Mityl nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
        },
        {
            "name": "Kỹ Xảo Điện Ảnh",
            "tags": ["Bị Động", "Cường Hóa"],
            "stability_damage": 0,
            "cooldown": "0 hiệp",
            "confectance_cost": 0,
            "range": "Bản thân",
            "effect_area": "Bản thân",
            "description": "Khi kết thúc lượt của phe ta, toàn bộ Hình Chiếu sẽ thi triển <color=#3487e0>Cộng Hưởng Hội Tụ</color> <color=#f26c1c>1 lần</color>. Sau khi Mityl hoặc Hình Chiếu gây ST Hóa Lỏng, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Nếu người tấn công hoặc mục tiêu đứng trên ô địa hình Hóa Lỏng, nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu nữa. Tối đa nhận <color=#f26c1c>6 điểm</color> Chỉ Số Nhiên Liệu mỗi hiệp.\nKhi bắt đầu trận chiến, nhận Danh Hiệu Màn Bạc cấp 1. Cứ mỗi khi tích lũy 6 điểm Chỉ Số Nhiên Liệu, cấp bậc <color=#3487e0>Danh Hiệu Màn Bạc</color> sẽ được thăng hạng liên tiếp."
        }
    ],
    "keys": [
        {
            "name": "Khóa Cố Định 1 - Trình Chiếu Điện Ảnh",
            "level": 20,
            "effect": "Khi bắt đầu trận chiến, nhận 2 điểm Chỉ Số Nhiên Liệu. Khi triệu hồi Hình Chiếu, trao cho nó 1 điểm Chỉ Số Ổn Định."
        },
        {
            "name": "Khóa Cố Định 2 - Màn Diễn Cải Trang",
            "level": 20,
            "effect": "Sát thương mà Hình Chiếu phải chịu giảm 20%. Khi Hình Chiếu bị tiêu diệt, Mityl nhận 1 điểm Chỉ Số Nhiên Liệu."
        },
        {
            "name": "Khóa Cố Định 3 - Nhào Lộn Đánh Chặn",
            "level": 30,
            "effect": "Sau khi thi triển Phi Thân Nhào Lộn, hồi phục 2 điểm Chỉ Số Ổn Định cho bản thân."
        },
        {
            "name": "Khóa Cố Định 4 - Phân Cảnh Bi Thương",
            "level": 30,
            "effect": "Khi một Hình Chiếu bị tiêu diệt, áp dụng Giảm ST I lên toàn bộ kẻ địch trong phạm vi 3 ô xung quanh nó trong 2 hiệp."
        },
        {
            "name": "Khóa Cố Định 5 - Chuyến Tàu Nổi Tiếng",
            "level": 40,
            "effect": "Sát thương Hóa Lỏng gây ra bởi Mityl và Hình Chiếu tăng 10%."
        },
        {
            "name": "Khóa Cố Định 6 - Thật Hay Giả?",
            "level": 40,
            "effect": "Tỷ lệ bạo kích của đòn đánh thường tăng 15%. Khi kích hoạt bạo kích, hồi phục 5% HP tối đa."
        },
        {
            "name": "Khóa Đồng Điệu - Trái Tim Ngôi Sao",
            "level": 1,
            "effect": "Tăng cường tình cảm và gắn bó sâu sắc cùng Chỉ Huy."
        },
        {
            "name": "Khóa Đa Năng - Mitty Thông Minh",
            "level": 40,
            "effect": "Khi đứng trên ô địa hình Lối Nước, Tấn Công tăng 10%."
        }
    ],
    "fortification": [
        {
            "tier": 1,
            "skill": "Kỹ Xảo Điện Ảnh",
            "level": 2,
            "effect": "Hệ số sát thương của <color=#3487e0>Cộng Hưởng Hội Tụ</color> tăng lên <color=#f26c1c>60%</color>.\nKhi cấp bậc của <color=#3487e0>Danh Hiệu Màn Bạc</color> tăng lên, Hình Chiếu sẽ lập tức kích hoạt <color=#f26c1c>1 lần</color> <color=#3487e0>Cộng Hưởng Hội Tụ</color>."
        },
        {
            "tier": 2,
            "skill": "Hình Chiếu Sóc Con",
            "level": 2,
            "effect": "Mỗi khi <color=#3487e0>Cộng Hưởng Hội Tụ</color> được kích hoạt, Hình Chiếu nhận 1 tầng hiệu ứng giảm sát thương gánh chịu.\nHệ số sát thương đòn đánh thường của Hình Chiếu - Phân Thân tăng lên <color=#f26c1c>120%</color>."
        },
        {
            "tier": 3,
            "skill": "Hội Tụ Hư Không",
            "level": 2,
            "effect": "Phạm vi tạo ô địa hình <color=#3487e0>Lối Nước</color> mở rộng lên <color=#f26c1c>7 ô</color>.\nMức tăng Tấn Công từ <color=#3487e0>Tràn Bão Hòa</color> nâng lên <color=#f26c1c>40%</color> và áp dụng cho cả Hình Chiếu."
        },
        {
            "tier": 4,
            "skill": "Phi Thân Nhào Lộn",
            "level": 2,
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>160%</color>.\nĐiều kiện để tái kích hoạt kỹ năng này được nới lỏng: chỉ cần ô trước khi thi triển hoặc ô hạ xuống là ô địa hình Hóa Lỏng."
        },
        {
            "tier": 5,
            "skill": "Phi Thân Nhào Lộn",
            "level": 3,
            "effect": "Sau khi sử dụng kỹ năng này, Hình Chiếu - Phân Thân sẽ kích hoạt <color=#f26c1c>1 lần</color> <color=#3487e0>Hành Động Hỗ Trợ</color>, gây ST Hóa Lỏng bằng <color=#f26c1c>60%</color> Tấn Công và 2 điểm sát thương ổn định."
        },
        {
            "tier": 6,
            "skill": "Kỹ Xảo Điện Ảnh",
            "level": 3,
            "effect": "Cường hóa <color=#3487e0>Danh Hiệu Màn Bạc</color>: Cứ mỗi 4 điểm Chỉ Số Nhiên Liệu nhận được, toàn bộ Hình Chiếu sẽ kích hoạt <color=#f26c1c>1 lần</color> <color=#3487e0>Cộng Hưởng Hội Tụ</color>.\nKhi một Hình Chiếu kích hoạt <color=#3487e0>Cộng Hưởng Hội Tụ</color>, trao cho toàn đội <color=#f26c1c>1 tầng</color> <color=#3487e0>Khuếch Đại Hội Tụ</color>."
        }
    ],
    "neural_helix": [
        {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +36\nPhòng Ngự +21"},
        {"node": "Cường Hóa 2", "level": 1, "effect": "HP +245\nPhòng Ngự +24"},
        {"node": "Cường Hóa 3", "level": 1, "effect": "Tấn Công +42\nPhòng Ngự +27"},
        {"node": "Cường Hóa 4", "level": 1, "effect": "HP +326\nTấn Công +48"},
        {"node": "Cường Hóa 5", "level": 1, "effect": "Tấn Công +54\nPhòng Ngự +33"},
        {"node": "Cường Hóa 6", "level": 1, "effect": "HP +408\nTấn Công +60\nPhòng Ngự +39"}
    ],
    "summons": [
        {
            "name": "Hình Chiếu - Phân Thân",
            "description": "Phân thân ảo ảnh của Mityl, mô phỏng hành động và kích hoạt Cộng Hưởng Hội Tụ vào cuối lượt phe ta.",
            "skills": [
                {
                    "name": "Đòn Đánh Hình Chiếu",
                    "tags": ["Đánh Thường", "Chỉ Định"],
                    "description": "Chọn 1 mục tiêu địch trong phạm vi 6 ô, gây ST <color=#2caada>Hóa Lỏng</color> bằng <color=#f26c1c>100%</color> Tấn Công lên mục tiêu đó."
                },
                {
                    "name": "Hồi Quy Dữ Liệu",
                    "tags": ["Bị Động"],
                    "description": "Khi thi triển <color=#3487e0>Cộng Hưởng Hội Tụ</color>, hồi phục <color=#f26c1c>50%</color> HP tối đa, và tăng HP tối đa thêm <color=#f26c1c>5%</color>, tối đa lên tới <color=#f26c1c>20%</color>."
                }
            ]
        },
        {
            "name": "Hình Chiếu - Mô Phỏng",
            "description": "Hình chiếu mô phỏng từ mục tiêu địch, kế thừa ngoại hình và thuộc tính cơ bản của mục tiêu.",
            "skills": []
        }
    ]
}

# 4. Update Welrod signature weapon in i18n
if "welrod" in bundle["characters"]:
    bundle["characters"]["welrod"]["signature_weapon"] = "Silent Conviction"

# 5. Commit using Transaction and stage_i18n_bundle
tx = RepositoryTransaction(ROOT)
with tx:
    stage_i18n_bundle(ROOT, tx, i18n_bundle=bundle)
    tx.commit()

print("Synchronized i18n_vi.json and i18n-vi.js via transaction!")
