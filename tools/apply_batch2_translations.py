#!/usr/bin/env python3
"""
tools/apply_batch2_translations.py
Applies verified, high-quality Vietnamese translations for Batch 2 (14 Global 5-star dolls Part 1):
  suomi, tololo, sabrina, qiongjiu, daiyan, klukai, centaureissi,
  andoris, balthilde, basti, belka, cheyanne, dushevnaya, faye.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_core.bundle import stage_i18n_bundle

I18N_PATH = ROOT / "data" / "i18n_vi.json"

BATCH_2_DATA = {
    "suomi": {
        "name": "Suomi",
        "en_name": "Suomi",
        "class": "Phòng Ngự",
        "phase": "Băng Kết",
        "rarity": "Elite",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Giọng Hát Băng Tuyết",
        "weakness": "Thiêu Đốt",
        "server": "global",
        "skills": [
            {
                "name": "Bông Tuyết Rơi",
                "en_name": "Pelting Snowflake",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Cơn Thịnh Nộ Mùa Đông",
                "en_name": "Winter's Wrath",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#42cce0>ST Băng Kết</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công lên mục tiêu đó và tất cả kẻ địch <color=#f26c1c>trong phạm vi 2 ô xung quanh</color>."
            },
            {
                "name": "Ân Huệ Của Tuyết",
                "en_name": "Snow's Grace",
                "tags": ["Chủ Động", "Chỉ Định", "Trị Liệu", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, áp dụng <color=#3487e0>Lá Chắn Hàn Sương</color> và <color=#3487e0>Hỗ Trợ Phòng Thủ</color> trong <color=#f26c1c>2 hiệp</color>. Nếu mục tiêu đã sở hữu Lá Chắn Hàn Sương, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Đồng thời tạo ra các ô địa hình <color=#3487e0>Băng Giá</color> <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Ánh Sáng Tuyết Nguyên",
                "en_name": "Snowfield's Radiance",
                "tags": ["Tuyệt Kỹ", "Phạm Vi", "Khống Chế", "Ô Địa Hình", "Cường Hóa"],
                "description": "Chọn 1 ô địa hình trống <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Cố Định bằng <color=#f26c1c>50%</color> Phòng Thủ lên tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> và áp dụng <color=#3487e0>Khiêu Khích</color> trong <color=#f26c1c>1 hiệp</color>. Tạo ra các ô địa hình <color=#3487e0>Pháo Đài Băng Tuyết</color> hình bông tuyết bán kính <color=#f26c1c>3 ô</color> trong <color=#f26c1c>3 hiệp</color>. Áp dụng <color=#3487e0>Lá Chắn Hàn Sương</color>, <color=#3487e0>Yểm Hộ</color> và <color=#3487e0>Tuyết Lở</color> cho tất cả đơn vị đồng minh."
            },
            {
                "name": "Nguồn Ấm Áp",
                "en_name": "Source of Warmth",
                "tags": ["Bị Động", "Hỗ Trợ", "Trị Liệu"],
                "description": "Khi đơn vị đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color> chịu ST, Suomi tiến hành 1 lần Hỗ Trợ Phòng Thủ, hồi phục HP bằng <color=#f26c1c>50%</color> Tấn Công và áp dụng <color=#3487e0>ST tăng I</color> cho mục tiêu trong <color=#f26c1c>1 hiệp</color>. Khi kích hoạt Tuyết Lở, gây <color=#42cce0>ST Băng Kết</color> AoE bằng <color=#f26c1c>60%</color> Tấn Công và nhận <color=#3487e0>ST Bạo Kích Tăng I</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ánh Sáng Tuyết Nguyên",
                "effect": "Khi dùng Ánh Sáng Tuyết Nguyên, áp dụng <color=#3487e0>Yểm Hộ</color> và <color=#3487e0>Duy Trì Chữa Lành I</color> cho tất cả đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Nguồn Ấm Áp",
                "effect": "Hỗ Trợ Phòng Thủ áp dụng thêm <color=#3487e0>Ánh Sáng Bảo Vệ</color> trong <color=#f26c1c>2 hiệp</color> và lượng hấp thụ của Lá Chắn Hàn Sương tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Ân Huệ Của Tuyết",
                "effect": "KN chủ động Ân Huệ Của Tuyết nhận thêm hiệu ứng: Áp dụng <color=#3487e0>Hồi Phục Khi Bị Đánh I</color> cho mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Nguồn Ấm Áp",
                "effect": "Hệ số trị liệu của Hỗ Trợ Phòng Thủ tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Nguồn Ấm Áp",
                "effect": "Số lần kích hoạt tối đa của Hỗ Trợ Phòng Thủ tăng thêm <color=#f26c1c>1 lần</color> mỗi hiệp."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Ánh Sáng Tuyết Nguyên",
                "effect": "Ánh Sáng Tuyết Nguyên áp dụng thêm <color=#3487e0>Phòng Thủ Tăng II</color> cho đồng minh trong <color=#f26c1c>2 hiệp</color>, đồng thời bản thân miễn dịch với <color=#3487e0>Choáng</color> và <color=#3487e0>Chạy Trốn</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +35\nPhòng Thủ +21", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +88\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +52\nPhòng Thủ +36", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +64\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +146\nPhòng Thủ +44", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +74\nPhòng Thủ +51", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Đà Tiến Bất Khuất",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Hộ Vệ Nhỏ",
                "level": "20",
                "effect": "Khi đồng minh có <color=#3487e0>Lá Chắn Hàn Sương</color> chịu ST, Suomi hồi phục HP bằng <color=#f26c1c>40%</color> Tấn Công cho mục tiêu đó.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Phản Hồi Tích Cực",
                "level": "30",
                "effect": "Khi <color=#3487e0>Lá Chắn Hàn Sương</color> bị phá vỡ, áp dụng <color=#3487e0>Hồi Phục Khi Bị Đánh I</color> cho mục tiêu trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Di Chuyển Mau Lẹ",
                "level": "30",
                "effect": "Tầm Di Chuyển tăng thêm <color=#f26c1c>1 ô</color>. Khi ở trên ô địa hình Băng Kết, bản thân miễn dịch với Debuff loại di chuyển.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Bất Động",
                "level": "40",
                "effect": "Khi bản thân có <color=#3487e0>Lá Chắn Hàn Sương</color>, ST Ổn Định phải chịu giảm <color=#f26c1c>2 điểm</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Hậu Cần Đang Tiến Hành",
                "level": "40",
                "effect": "Khi kết thúc hành động, áp dụng <color=#3487e0>Lá Chắn Hàn Sương</color> cho đồng minh có tỷ lệ HP thấp nhất <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Rock and Roll",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Phước Lành Nhiệm Vụ",
                "level": "40",
                "effect": "HP +3.0% / Khi dùng kỹ năng hồi máu chủ động, có <color=#f26c1c>50%</color> xác suất áp dụng <color=#f26c1c>1</color> hiệu ứng Buff ngẫu nhiên lên mục tiêu trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "60",
                "effect": "Lượng hấp thụ của <color=#3487e0>Lá Chắn Hàn Sương</color> tăng thêm <color=#f26c1c>20%</color>. Ô địa hình Băng Tuyết mở rộng thêm <color=#f26c1c>1 ô</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "tololo": {
        "name": "Tololo",
        "en_name": "Tololo",
        "class": "Hỏa Lực",
        "phase": "Hóa Lỏng",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Lời Kêu Gọi Vì Sao",
        "weakness": "Điện Từ",
        "server": "global",
        "skills": [
            {
                "name": "Sao Băng",
                "en_name": "Meteor",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Tái Hiện Hố Đen",
                "en_name": "Black Hole Inversion",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>130%</color> Tấn Công. Nếu khai thác Điểm Yếu Thuộc Tính, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Xung Kích Siêu Tân Tinh",
                "en_name": "Supernova Impact",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Nếu bản thân có từ <color=#f26c1c>2 hiệu ứng Buff trở lên</color>, ST gây ra tăng <color=#f26c1c>20%</color> và nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Ánh Sáng Hủy Diệt",
                "en_name": "Morte Lumina",
                "tags": ["Tuyệt Kỹ", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>180%</color> Tấn Công. Nếu bản thân có từ <color=#f26c1c>3 hiệu ứng Buff trở lên</color>, ST gây ra tăng <color=#f26c1c>15%</color> và thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Màn Cực Quang",
                "en_name": "Aurora Curtain",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Khi bắt đầu chiến đấu, nạp đầy Chỉ Số Nhiên Liệu lên mức tối đa. Sau khi tấn công, nếu Chỉ Số Nhiên Liệu đạt tối đa, tiêu hao tất cả và nhận <color=#f26c1c>1 lần</color> <color=#3487e0>Tăng Hành Động</color>.\n\nKhi bắt đầu mỗi hành động, cứ mỗi <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu, nhận <color=#f26c1c>1</color> hiệu ứng Buff ngẫu nhiên duy trì đến hết hành động đó. Mỗi khi một đơn vị đồng minh gây ST Hóa Lỏng, bản thân nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Gai Ánh Sáng</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Sao Băng",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tái Hiện Hố Đen",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Xung Kích Siêu Tân Tinh",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Màn Cực Quang",
                "effect": "Khi Màn Cực Quang kích hoạt Tăng Hành Động, nhận thêm <color=#3487e0>Chuẩn Xác Tăng II</color>, <color=#3487e0>TL Bạo Kích Tăng II</color>, <color=#3487e0>Dị Vị Tăng II</color> và <color=#3487e0>Xuyên Thấu II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Màn Cực Quang",
                "effect": "Mỗi lớp <color=#3487e0>Gai Ánh Sáng</color> tăng ST Bạo Kích thêm <color=#f26c1c>3%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Ánh Sáng Hủy Diệt",
                "effect": "Thời gian hồi chiêu của Ánh Sáng Hủy Diệt giảm thêm <color=#f26c1c>1 hiệp</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +37\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +76\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +58\nPhòng Thủ +31", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +71\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +126\nPhòng Thủ +38", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +83\nPhòng Thủ +45", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Đuôi Sao Băng Quá Cảnh",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Nguyên Lý Thiên Văn Quan Sát",
                "level": "20",
                "effect": "Khi bản thân sở hữu từ <color=#f26c1c>3 hiệu ứng Buff trở lên</color>, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Ánh Sáng Vô Hình",
                "level": "30",
                "effect": "Khi gây <color=#2caadb>ST Hóa Lỏng</color>, bỏ qua <color=#f26c1c>20%</color> Phòng Thủ của mục tiêu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Chuyển Động Nghịch Hành",
                "level": "30",
                "effect": "Khi kích hoạt <color=#3487e0>Tăng Hành Động</color>, giải trừ <color=#f26c1c>2</color> hiệu ứng Debuff trên bản thân.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Tuần Du Ngân Hà",
                "level": "40",
                "effect": "Khi có <color=#3487e0>Gai Ánh Sáng</color>, Tầm Di Chuyển của bản thân tăng thêm <color=#f26c1c>1 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Nhật Thực Tinh Tú",
                "level": "40",
                "effect": "Khi dùng Ánh Sáng Hủy Diệt tiêu diệt mục tiêu địch, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Lời Thì Thầm Của Bụi Sao",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Ánh Hoàng Hôn",
                "level": "40",
                "effect": "TL Bạo Kích +3.0% / ST Hóa Lỏng gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "60",
                "effect": "Khi kích hoạt <color=#3487e0>Tăng Hành Động</color>, ST gây ra trong hành động tiếp theo tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng Bậc 2",
                "level": "60",
                "effect": "Triệu hồi Vệ Tinh Cố Định hỗ trợ chi viện hỏa lực <color=#2caadb>ST Hóa Lỏng</color> trên diện rộng.",
                "materials": "1\n\n\n3000"
            }
        ],
        "summons": [
            {
                "name": "Vệ Tinh Cố Định",
                "type": "Vật Triệu Hồi Hóa Lỏng",
                "description": "Thiết bị vệ tinh dẫn đường quỹ đạo, cung cấp tầm nhìn chiến thuật và kích hoạt các đòn đánh chi viện năng lượng.",
                "stats": {
                    "hp": "<color=#f26c1c>100%</color> HP ban đầu của Tololo",
                    "atk": "<color=#f26c1c>100%</color> Tấn Công ban đầu của Tololo",
                    "def": "<color=#f26c1c>100%</color> Phòng Thủ ban đầu của Tololo"
                },
                "skills": [
                    {
                        "name": "Triệu Hồi Vì Sao",
                        "description": "Khi kết thúc hiệp phe ta, gây ST Chuẩn Xác Hóa Lỏng bằng <color=#f26c1c>130%</color> Tấn Công lên đơn vị địch trong phạm vi 7 ô xung quanh sở hữu Dấu Ấn Trọng Lực. Nếu không có đơn vị nào có Dấu Ấn Trọng Lực, chỉ định đơn vị địch gần nhất."
                    },
                    {
                        "name": "Đồng Bộ Tĩnh Lặng",
                        "description": "Miễn dịch với các hiệu ứng khống chế như <color=#3487e0>Choáng</color>, <color=#3487e0>Khiêu Khích</color> và Cấm Lệnh."
                    }
                ]
            }
        ]
    },
    "sabrina": {
        "name": "Sabrina",
        "en_name": "Sabrina",
        "class": "Phòng Ngự",
        "phase": "Hóa Lỏng",
        "rarity": "Elite",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Nước Sốt Độc Quyền",
        "weakness": "Điện Từ",
        "server": "global",
        "skills": [
            {
                "name": "Tôi Mời Khách",
                "en_name": "My Treat",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Bữa Tiệc Thịnh Soạn",
                "en_name": "Delicious Feast",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu", "Ô Địa Hình"],
                "description": "Gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>85%</color> Tấn Công lên tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> bản thân, tạo ô địa hình Hóa Lỏng trong <color=#f26c1c>2 hiệp</color> và áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Chuẩn Bị Bữa Ăn",
                "en_name": "Meal Preparation",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 hướng, đẩy lùi tất cả mục tiêu địch trong phạm vi 3×5 ô phía trước đi <color=#f26c1c>2 ô</color>, gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công và áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Tinh Thần Ẩm Thực",
                "en_name": "Gourmet Spirit",
                "tags": ["Tuyệt Kỹ", "Cường Hóa", "Phản Kích"],
                "description": "Bản thân nhận <color=#3487e0>No Bụng</color>, <color=#f26c1c>3 lớp</color> <color=#3487e0>Yểm Hộ</color> trong <color=#f26c1c>2 hiệp</color>. Số lần <color=#3487e0>Phản Kích</color> trong hiệp này tăng thêm <color=#f26c1c>3 lần</color>. Nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Cải Tiến Linh Hoạt",
                "en_name": "Flexible Modification",
                "tags": ["Bị Động", "Phản Kích", "Cường Hóa"],
                "description": "Khi bắt đầu hiệp, nếu có kẻ địch trên đường thẳng 8 ô phía trước, phun 1 Thủy Cầu gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>80%</color> Tấn Công lên mục tiêu và kẻ địch trong phạm vi 3 ô xung quanh. Khi chịu ST, Sabrina tiến hành 1 lần Phản Kích, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>100%</color> Tấn Công."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Cải Tiến Linh Hoạt",
                "effect": "Khi bắn Thủy Cầu, áp dụng <color=#f26c1c>1 lớp</color> <color=#3487e0>Yểm Hộ</color> cho tất cả đơn vị đồng minh trong phạm vi 6 ô xung quanh trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Bữa Tiệc Thịnh Soạn",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Chuẩn Bị Bữa Ăn",
                "effect": "Khoảng cách đẩy lùi tăng thêm <color=#f26c1c>1 ô</color> và phạm vi mở rộng thành 3×6 ô."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tinh Thần Ẩm Thực",
                "effect": "Khi có hiệu ứng <color=#3487e0>No Bụng</color>, ST Phản Kích gây ra tăng thêm <color=#f26c1c>25%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Tinh Thần Ẩm Thực",
                "effect": "Sau khi dùng Tinh Thần Ẩm Thực, nhận thêm <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Cải Tiến Linh Hoạt",
                "effect": "ST phải chịu giảm <color=#f26c1c>15%</color>. Khi Chỉ Số Ổn Định lớn hơn 0, mức giảm thương tăng thành <color=#f26c1c>30%</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +33\nPhòng Thủ +24", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +92\nHP +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +51\nPhòng Thủ +39", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +62\nPhòng Thủ +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +152\nPhòng Thủ +48", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +72\nPhòng Thủ +55", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Ăn Uống Là Phước",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Chia Sẻ Món Ngon",
                "level": "20",
                "effect": "Khi dùng Bữa Tiệc Thịnh Soạn, hồi phục HP bằng <color=#f26c1c>30%</color> Tấn Công cho tất cả đồng minh trong phạm vi.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Ninh Kỹ Mọi Thứ",
                "level": "30",
                "effect": "Kẻ địch đứng trên ô địa hình Hóa Lỏng của Sabrina chịu ST tăng thêm <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Ăn Ngon Ngủ Kỹ",
                "level": "30",
                "effect": "Khi HP lớn hơn <color=#f26c1c>70%</color>, Phòng Thủ tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Calo Quá Tải",
                "level": "40",
                "effect": "Mỗi lần Phản Kích thành công, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Công Thức Lạ Miệng",
                "level": "40",
                "effect": "Khi kích hoạt Phản Kích, giải trừ <color=#f26c1c>1</color> Buff trên người mục tiêu tấn công.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Giờ Ăn Tráng Miệng",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Bảo Hộ Dầu Nóng",
                "level": "40",
                "effect": "HP +3.0% / ST AoE phải chịu giảm <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Công Thức Truyền Kỳ",
                "level": "60",
                "effect": "Khi có <color=#3487e0>No Bụng</color>, ST Ổn Định gây ra tăng thêm <color=#f26c1c>2 điểm</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "qiongjiu": {
        "name": "Qiongjiu",
        "en_name": "Qiongjiu",
        "class": "Hỗ Trợ",
        "phase": "Thiêu Đốt",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Lời Thề Kiên Định",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Mồi Lửa",
                "en_name": "Fuse",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Đường Đạn Chung",
                "en_name": "Common Rail",
                "tags": ["Chủ Động", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Áp dụng <color=#3487e0>Tăng Chi Viện I</color> cho tất cả đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Chỉ Dẫn Thắng Lợi",
                "en_name": "Guide to Victory",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>140%</color> Tấn Công và áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Truy Kích Đoạt Thế",
                "en_name": "Pressing the Momentum",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>170%</color> Tấn Công. Áp dụng <color=#3487e0>Tăng Chi Viện II</color> cho bản thân và tất cả đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Mưu Lược Ổn Định",
                "en_name": "Steady Plan",
                "tags": ["Bị Động", "Hỗ Trợ"],
                "description": "Khi đơn vị đồng minh phát động tấn công chủ động lên kẻ địch trong tầm bắn, Qiongjiu ưu tiên tiến hành 1 lần Hành Động Chi Viện, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn Định. Mỗi hiệp tối đa kích hoạt <color=#f26c1c>3 lần</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Đường Đạn Chung",
                "effect": "Nếu tiêu diệt được mục tiêu, mức tăng sát thương của <color=#3487e0>Tăng Chi Viện I</color> tăng thành <color=#f26c1c>30%</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Chỉ Dẫn Thắng Lợi",
                "effect": "Nếu mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, Tỷ Lệ Bạo Kích của đòn tấn công này tăng <color=#f26c1c>100%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Mưu Lược Ổn Định",
                "effect": "Sau khi tiến hành Hành Động Chi Viện, áp dụng <color=#3487e0>Tràn Lửa</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>. Sát thương của Hành Động Chi Viện tăng <color=#f26c1c>10%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Truy Kích Đoạt Thế",
                "effect": "Áp dụng <color=#3487e0>Dễ Bị Thương I</color> trong <color=#f26c1c>1 hiệp</color> lên các mục tiêu không được Vật Cản bảo vệ."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Truy Kích Đoạt Thế",
                "effect": "Khi tiến hành Hành Động Chi Viện, áp dụng <color=#3487e0>ST Tăng II</color> cho bản thân và đơn vị đồng minh trong <color=#f26c1c>1 hiệp</color> trước khi đồng minh đó phát động tấn công."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Mưu Lược Ổn Định",
                "effect": "Sát thương gây ra lên mục tiêu không được Vật Cản bảo vệ tăng <color=#f26c1c>10%</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +36\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +74\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +56\nPhòng Thủ +31", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +69\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +124\nPhòng Thủ +38", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +80\nPhòng Thủ +45", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Tập Trung Cao Độ",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Hoạch Định Hiệu Quả",
                "level": "20",
                "effect": "Khi tiến hành Hành Động Chi Viện, nếu mục tiêu đang trong trạng thái Sụp Đổ Ổn Định, ST gây ra tăng <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Huấn Luyện Trọng Điểm",
                "level": "30",
                "effect": "Số lần kích hoạt tối đa mỗi hiệp của Hành Động Chi Viện tăng thêm <color=#f26c1c>1 lần</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Điểm Yếu Trọng Yếu",
                "level": "30",
                "effect": "Khi tấn công mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Điều Chỉnh Cần Thiết",
                "level": "40",
                "effect": "Khi đồng minh kích hoạt đòn chi viện của Qiongjiu, đồng minh đó nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Vững Vàng",
                "level": "40",
                "effect": "Khi kết thúc hành động, nếu chưa di chuyển trong hiệp này, ST gây ra trong hiệp sau tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Ấm Áp Như Ngọc",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Đàm Phán Chiến Lược",
                "level": "40",
                "effect": "Tấn Công +3.0% / ST chi viện gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Ngọc Nát",
                "level": "60",
                "effect": "Khi tiến hành Hành Động Chi Viện, bỏ qua <color=#f26c1c>20%</color> Phòng Thủ của mục tiêu.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "daiyan": {
        "name": "Daiyan",
        "en_name": "Daiyan",
        "class": "Hỏa Lực",
        "phase": "Vật Lý",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Hạc Tiên Tung Cánh",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Gảy Đàn",
                "en_name": "Plucking Strings",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Tiếng Vàng Điệu Ngọc",
                "en_name": "Absolute Tuning",
                "tags": ["Chủ Động", "Chỉ Định", "Giải Trừ"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, giải trừ <color=#f26c1c>1</color> hiệu ứng Buff trên mục tiêu và gây ST Vật Lý bằng <color=#f26c1c>150%</color> Tấn Công."
            },
            {
                "name": "Hòa Điệu Thanh Thương",
                "en_name": "Qing Shang Harmony",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Bản thân nhận <color=#f26c1c>3 lớp</color> <color=#3487e0>Chỉnh Âm</color>, nhận <color=#3487e0>Định Âm</color> trong <color=#f26c1c>1 hiệp</color> và nhận <color=#f26c1c>1 lần</color> <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "name": "Âm Vang Mê Hoặc",
                "en_name": "Ethereal Resonance",
                "tags": ["Tuyệt Kỹ", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>190%</color> Tấn Công. Cứ mỗi <color=#f26c1c>1 lớp</color> <color=#3487e0>Chỉnh Âm</color>, thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>1 hiệp</color>.\n\nSau khi tấn công, tiêu hao tất cả các lớp <color=#3487e0>Chỉnh Âm</color> và nhận vĩnh viễn <color=#f26c1c>1 lớp</color> <color=#3487e0>Chỉnh Âm</color>, tối đa cộng dồn <color=#f26c1c>3 lớp</color>."
            },
            {
                "name": "Tiếng Đàn Tiếp Viện",
                "en_name": "Swift Harmony",
                "tags": ["Bị Động", "Cường Hóa", "Phục Kích"],
                "description": "Khi bắt đầu hành động, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu và <color=#f26c1c>1 lớp</color> <color=#3487e0>Chỉnh Âm</color>. Khi phát động tấn công chủ động lên mục tiêu không được Vật Cản bảo vệ, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\n\nTrước khi chịu ST Chuẩn Xác, nếu số lớp <color=#3487e0>Chỉnh Âm</color> lớn hơn <color=#f26c1c>2</color>, tiến hành 1 lần <color=#3487e0>Phục Kích</color>, gây ST Vật Lý loại đạn nhẹ bằng <color=#f26c1c>150%</color> Tấn Công và <color=#f26c1c>4 điểm</color> ST Ổn Định, đồng thời nhận vĩnh viễn <color=#f26c1c>1 lớp</color> <color=#3487e0>Chỉnh Âm</color>. Mỗi hiệp tối đa kích hoạt 1 lần.\n\nNếu số lớp <color=#3487e0>Chỉnh Âm</color> lớn hơn <color=#f26c1c>3</color>, ST gây ra tăng <color=#f26c1c>20%</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Tiếng Vàng Điệu Ngọc",
                "effect": "Nếu mục tiêu có hiệu ứng Buff, sau khi giải trừ nhận thêm <color=#f26c1c>1 lớp</color> <color=#3487e0>Chỉnh Âm</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Hòa Điệu Thanh Thương",
                "effect": "Số lớp <color=#3487e0>Chỉnh Âm</color> nhận được tăng thêm <color=#f26c1c>1 lớp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Âm Vang Mê Hoặc",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tiếng Đàn Tiếp Viện",
                "effect": "Sát thương do <color=#3487e0>Phục Kích</color> gây ra tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Tiếng Đàn Tiếp Viện",
                "effect": "Số lớp tích lũy tối đa của <color=#3487e0>Chỉnh Âm</color> tăng thêm <color=#f26c1c>1 lớp</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Âm Vang Mê Hoặc",
                "effect": "Số lớp <color=#3487e0>Chỉnh Âm</color> vĩnh viễn nhận được sau khi tấn công tăng thêm <color=#f26c1c>1 lớp</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +36\nPhòng Thủ +20", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +74\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +56\nPhòng Thủ +33", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +69\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +124\nPhòng Thủ +40", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +80\nPhòng Thủ +48", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Giai Điệu Vang Vọng",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Giấc Mơ Chưa Tròn",
                "level": "20",
                "effect": "Khi có từ <color=#f26c1c>2 lớp</color> <color=#3487e0>Chỉnh Âm</color> trở lên, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Khúc Hát Sương Mù",
                "level": "30",
                "effect": "Khi kích hoạt <color=#3487e0>Phục Kích</color>, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho bản thân.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Dạ Khúc Thanh Bình",
                "level": "30",
                "effect": "Khi ở gần Vật Cản, ST Chuẩn Xác gây ra tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Đội Hình Tan Vỡ",
                "level": "40",
                "effect": "Đòn <color=#3487e0>Phục Kích</color> gây thêm <color=#f26c1c>2 điểm</color> ST Ổn Định lên mục tiêu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Di Sản Bất Hủ",
                "level": "40",
                "effect": "Khi dùng Âm Vang Mê Hoặc tiêu diệt mục tiêu, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Khúc Hát Ngọt Ngào",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Phá Đá Xé Lụa",
                "level": "40",
                "effect": "Tấn Công +3.0% / ST Chuẩn Xác gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "60",
                "effect": "Khi kích hoạt <color=#3487e0>Phục Kích</color>, bỏ qua <color=#f26c1c>20%</color> Phòng Thủ của mục tiêu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng Bậc 2",
                "level": "60",
                "effect": "Khi có tối đa lớp <color=#3487e0>Chỉnh Âm</color>, ST Bạo Kích tăng thêm <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "klukai": {
        "name": "Klukai",
        "en_name": "Klukai",
        "class": "Hỏa Lực",
        "phase": "Ăn Mòn",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Lời Tuyên Thệ Tối Hậu",
        "weakness": "Điện Từ",
        "server": "global",
        "skills": [
            {
                "name": "Tấn Công Nhanh",
                "en_name": "Swift Strike",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Điểm Kích Nổ",
                "en_name": "Pinpoint Detonation",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng <color=#f26c1c>130%</color> Tấn Công và áp dụng <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Ăn Mòn Áp Đảo",
                "en_name": "Overpowering Corrosion",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>90%</color> Tấn Công lên mục tiêu và tất cả kẻ địch <color=#f26c1c>trong phạm vi 2 ô xung quanh</color>, áp dụng <color=#3487e0>Độc Tính Xâm Nhập</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Lướt Hủy Diệt",
                "en_name": "Devastating Drift",
                "tags": ["Tuyệt Kỹ", "Phạm Vi", "Dịch Chuyển"],
                "description": "Chọn 1 hướng và di chuyển đến ô xa nhất <color=#f26c1c>trong phạm vi 7 ô</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>160%</color> Tấn Công lên tất cả mục tiêu địch trên đường đi và nhận thêm <color=#f26c1c>5 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color>."
            },
            {
                "name": "Niềm Tự Hào Của Tinh Anh",
                "en_name": "Elite's Pride",
                "tags": ["Bị Động", "Cường Hóa", "Suy Yếu"],
                "description": "Bản thân nhận <color=#3487e0>Hiếu Thắng</color>. Khi kẻ địch chịu trạng thái <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> bị tiêu diệt, phát nổ gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>60%</color> Tấn Công lên tất cả kẻ địch xung quanh trong phạm vi 2 ô."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ăn Mòn Áp Đảo",
                "effect": "Thời gian duy trì của <color=#3487e0>Độc Tính Xâm Nhập</color> tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Niềm Tự Hào Của Tinh Anh",
                "effect": "Hiệu ứng tăng sát thương của <color=#3487e0>Hiếu Thắng</color> tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Lướt Hủy Diệt",
                "effect": "Lướt Hủy Diệt áp dụng thêm <color=#3487e0>Phòng Thủ Giảm II</color> lên tất cả mục tiêu trúng đòn trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Điểm Kích Nổ",
                "effect": "Điểm Kích Nổ tạo ô địa hình Ăn Mòn dưới chân mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Ăn Mòn Áp Đảo",
                "effect": "Hệ số ST của Ăn Mòn Áp Đảo tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Lướt Hủy Diệt",
                "effect": "Lướt Hủy Diệt áp dụng thêm <color=#3487e0>Hoảng Sợ</color> lên kẻ địch trúng đòn trong <color=#f26c1c>1 hiệp</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +38\nPhòng Thủ +20", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +76\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +59\nPhòng Thủ +33", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +72\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +128\nPhòng Thủ +40", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +84\nPhòng Thủ +48", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Dây Leo Chết Chóc",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Một Đòn Quét Sạch",
                "level": "20",
                "effect": "Khi dùng Lướt Hủy Diệt tiêu diệt từ 2 mục tiêu trở lên, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Không Khoan Nhượng",
                "level": "30",
                "effect": "ST gây ra cho mục tiêu có Debuff loại Ăn Mòn tăng thêm <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Chi Viện Vững Vàng",
                "level": "30",
                "effect": "Tầm Di Chuyển của bản thân tăng thêm <color=#f26c1c>1 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Phá Vỡ Giới Hạn",
                "level": "40",
                "effect": "Khi có hiệu ứng <color=#3487e0>Hiếu Thắng</color>, Tỷ Lệ Bạo Kích tăng thêm <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Thời Khắc Tận Diệt",
                "level": "40",
                "effect": "Khi mục tiêu chịu <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> tử vong, thời gian hồi chiêu của Lướt Hủy Diệt giảm <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Sát Khí Quay Về",
                "level": "40",
                "effect": "Tấn Công +3.0% / ST Ăn Mòn gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Niềm Kiêu Hãnh Tinh Anh",
                "level": "60",
                "effect": "Khi gây ST Ăn Mòn, bỏ qua <color=#f26c1c>20%</color> Phòng Thủ của mục tiêu.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "centaureissi": {
        "name": "Centaureissi",
        "en_name": "Centaureissi",
        "class": "Hỗ Trợ",
        "phase": "Thiêu Đốt",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Hương Vị Trà Nồng",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Giờ Dọn Dẹp",
                "en_name": "Cleaning Time",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Đón Tiếp Chu Đáo",
                "en_name": "Careful Hospitality",
                "tags": ["Chủ Động", "Chỉ Định", "Trị Liệu", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, hồi phục HP bằng <color=#f26c1c>120%</color> Tấn Công, giải trừ <color=#f26c1c>1</color> Debuff và áp dụng <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Thức Uống Đặc Biệt Zucchero",
                "en_name": "Zucchero's Special Drink",
                "tags": ["Chủ Động", "Phạm Vi", "Trị Liệu", "Giải Trừ"],
                "description": "Gây <color=#e67129>ST Thiêu Đốt</color> AoE bằng <color=#f26c1c>80%</color> Tấn Công lên kẻ địch <color=#f26c1c>trong phạm vi 3 ô xung quanh</color>, giải trừ <color=#f26c1c>1</color> Debuff cho tất cả đồng minh trong phạm vi và áp dụng <color=#3487e0>Tràn Lửa</color> lên kẻ địch trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Tiệc Trà Chiều",
                "en_name": "Afternoon Tea Break",
                "tags": ["Tuyệt Kỹ", "Trị Liệu", "Giải Trừ", "Cường Hóa"],
                "description": "Hồi phục HP bằng <color=#f26c1c>140%</color> Tấn Công và <color=#f26c1c>4 điểm</color> Chỉ Số Ổn Định cho tất cả đơn vị đồng minh toàn trận, giải trừ <color=#f26c1c>2</color> Debuff, xóa bỏ hiệu ứng <color=#3487e0>Choáng</color> và <color=#3487e0>Chạy Trốn</color>, đồng thời áp dụng <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Bổn Phận Hầu Gái",
                "en_name": "Maid's Duty",
                "tags": ["Bị Động", "Hỗ Trợ", "Cường Hóa"],
                "description": "Khi đơn vị đồng minh tấn công kẻ địch trong tầm bắn, Centaureissi tiến hành 1 lần Hành Động Chi Viện, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định, đồng thời nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Mỗi hiệp tối đa kích hoạt <color=#f26c1c>2 lần</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Bổn Phận Hầu Gái",
                "effect": "Hành Động Chi Viện áp dụng thêm <color=#3487e0>Thế Công Rực Lửa II</color> và <color=#3487e0>ST Tăng II</color> cho đồng minh trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Bổn Phận Hầu Gái",
                "effect": "Hành Động Chi Viện áp dụng thêm <color=#3487e0>Tràn Lửa</color> lên kẻ địch trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Đón Tiếp Chu Đáo",
                "effect": "Đón Tiếp Chu Đáo áp dụng thêm <color=#3487e0>Tuần Hoàn Nhiệt</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tiệc Trà Chiều",
                "effect": "Tiệc Trà Chiều xóa bỏ thêm hiệu ứng <color=#3487e0>Khiêu Khích</color> và <color=#3487e0>Dẫn Dụ</color> trên tất cả đơn vị đồng minh."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Tiệc Trà Chiều",
                "effect": "Lượng hồi phục HP của Tiệc Trà Chiều tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Thức Uống Đặc Biệt Zucchero",
                "effect": "Thời gian hồi chiêu của Thức Uống Đặc Biệt Zucchero giảm <color=#f26c1c>1 hiệp</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +26\nPhòng Thủ +21", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +80\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +44\nPhòng Thủ +35", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +54\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +134\nPhòng Thủ +43", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +63\nPhòng Thủ +50", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Món Tráng Miệng Trước Bữa",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Quyết Tâm Hầu Gái",
                "level": "20",
                "effect": "Nếu đồng minh trong phạm vi 7 ô rơi vào trạng thái Sụp Đổ Ổn Định, chuyển <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color> từ bản thân sang cho đồng minh đó.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Xử Lý Hiệu Quả",
                "level": "30",
                "effect": "Khi kích hoạt <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>, giải trừ <color=#f26c1c>1</color> Buff trên kẻ tấn công và <color=#f26c1c>2</color> Debuff trên đồng minh sở hữu hiệu ứng.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Pha Chế Xoa Dịu",
                "level": "30",
                "effect": "Chọn 1 hướng, gây ST Vật Lý AoE bằng <color=#f26c1c>75%</color> Tấn Công lên kẻ địch trong phạm vi 5×3 ô phía trước và đẩy lùi <color=#f26c1c>1 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Chuẩn Bị Chu Toàn",
                "level": "40",
                "effect": "Khi trị liệu cho đồng minh bằng kỹ năng chủ động, giải trừ thêm <color=#f26c1c>1</color> Debuff nếu mục tiêu có <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Thực Đơn May Mắn",
                "level": "40",
                "effect": "Khi trị liệu cho đồng minh có <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>, áp dụng ngẫu nhiên <color=#f26c1c>1</color> Buff mạnh mẽ trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Đồ Uống Nóng Thiết Yếu",
                "level": "40",
                "effect": "HP +3.0% / Khi di chuyển từ 3 ô trở lên trước khi tấn công chủ động, ST gây ra tăng <color=#f26c1c>5%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Ý Chí Bảo Vệ",
                "level": "60",
                "effect": "Sau khi dùng Tiệc Trà Chiều hoặc Thức Uống Đặc Biệt Zucchero, áp dụng hiệu ứng phòng hộ toàn diện cho tất cả đồng minh trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "andoris": {
        "name": "Andoris",
        "en_name": "Andoris",
        "class": "Phòng Ngự",
        "phase": "Điện Từ",
        "rarity": "Elite",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Điện Cực Bình Yên",
        "weakness": "Vật Lý",
        "server": "global",
        "skills": [
            {
                "name": "Bắn Tập",
                "en_name": "Practice Shot",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>4 điểm</color> ST Ổn Định."
            },
            {
                "name": "Tấn Công Dịu Dàng",
                "en_name": "Gentle Offensive",
                "tags": ["Chủ Động", "Triệu Hồi"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 3 ô</color> và triệu hồi 1 Pháo Tự Hành. Tối đa có thể tồn tại cùng lúc <color=#f26c1c>2</color> Pháo Tự Hành trên sân. Khi số lượng Pháo Tự Hành vượt quá 2, Pháo Tự Hành được triệu hồi sớm nhất sẽ tự động bị phá hủy. Khi Pháo Tự Hành bị phá hủy, tăng <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\n\nSau khi sử dụng, kỹ năng này có thể được dùng thêm 1 lần nữa trong hiệp."
            },
            {
                "name": "Chiến Thuật Tinh Gọn",
                "en_name": "Streamlined Tactics",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô</color>, áp dụng <color=#3487e0>Tụ Điện</color> trong <color=#f26c1c>2 hiệp</color> trước khi tấn công, sau đó gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>110%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn Định."
            },
            {
                "name": "Nghi Thức Gia Cố",
                "en_name": "Fortification Protocol",
                "tags": ["Tuyệt Kỹ", "Phòng Ngự", "Cường Hóa"],
                "description": "Bản thân hồi phục <color=#f26c1c>8 điểm</color> Chỉ Số Ổn Định và nhận <color=#3487e0>Tư Thế Mạnh Mẽ</color> trong <color=#f26c1c>2 hiệp lớn</color> (thời gian duy trì giảm khi kết thúc hiệp hiện tại). Áp dụng <color=#f26c1c>2 lớp</color> <color=#3487e0>Yểm Hộ</color> và trạng thái <color=#3487e0>Điện Tích Dương</color> trong <color=#f26c1c>3 hiệp</color> cho tất cả đơn vị đồng minh."
            },
            {
                "name": "Phản Ứng Chậm Trễ",
                "en_name": "Delayed Response",
                "tags": ["Bị Động", "Hỗ Trợ", "Cường Hóa"],
                "description": "Khi bắt đầu chiến đấu, bản thân nhận <color=#3487e0>Tự Sửa Chữa</color>. Hiệu ứng này có thể tái kích hoạt sau <color=#f26c1c>3 hiệp lớn</color>.\n\nKhi đồng minh có <color=#3487e0>Điện Tích Dương</color> chịu sát thương, Andoris gánh chịu thay <color=#f26c1c>45%</color> Sát Thương Ban Đầu. Khi Andoris dùng tấn công chủ động lên kẻ địch có <color=#3487e0>Điện Tích Âm</color>, bản thân hồi phục HP bằng <color=#f26c1c>20%</color> HP tối đa.\n\nKhi chịu sát thương, bản thân hồi phục HP bằng <color=#f26c1c>5%</color> HP tối đa, tăng <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu, đồng thời nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Sức Ì</color> cho bản thân và tất cả Pháo Tự Hành trên sân. Nếu Andoris không đứng sau Vật Cản (Yểm Hộ), giảm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu và sát thương phải chịu giảm <color=#f26c1c>20%</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Tấn Công Dịu Dàng",
                "effect": "Tăng cự ly triệu hồi của Pháo Tự Hành thêm <color=#f26c1c>3 ô</color>. Tăng tầm bắn của Pháo Tự Hành thêm <color=#f26c1c>1 ô</color>.\n\nMô Phỏng Va Chạm nhận thêm hiệu ứng: Bản thân tăng <color=#f26c1c>30%</color> <color=#d4a017>ST Điện Từ</color> gây ra.\n\nBổ sung kỹ năng bị động mới Bắt Tốt Qua Đường cho Pháo Tự Hành."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Nghi Thức Gia Cố",
                "effect": "Nhận thêm hiệu ứng: Bản thân hồi đầy Chỉ Số Ổn Định, hồi phục HP bằng <color=#f26c1c>20%</color> HP tối đa và giải trừ toàn bộ Debuff trên bản thân.\n\nKhi Andoris có mặt trên sân, áp dụng <color=#3487e0>Di Chuyển Tăng II</color> và <color=#3487e0>ST Tăng II</color> cho tất cả đồng minh mang <color=#3487e0>Điện Tích Dương</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Phản Ứng Chậm Trễ",
                "effect": "Nhận thêm hiệu ứng: ST Ổn Định phải chịu giảm <color=#f26c1c>1 điểm</color>. Khi bắt đầu chiến đấu, tăng Tấn Công cho bản thân và Pháo Tự Hành bằng <color=#f26c1c>30%</color> Phòng Thủ ban đầu của Andoris. Khi Pháo Tự Hành chịu sát thương cũng sẽ nhận <color=#3487e0>Sức Ì</color>.\n\nHiệu ứng Sức Ì nhận thêm: Tăng Phòng Thủ thêm <color=#f26c1c>20%</color> và tăng giới hạn số tầng tối đa thêm <color=#f26c1c>3 tầng</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Phản Ứng Chậm Trễ",
                "effect": "Khi bắt đầu chiến đấu, tăng Chỉ Số Ổn Định tối đa thêm <color=#f26c1c>6 điểm</color>.\n\nCường hóa hiệu ứng Tự Sửa Chữa: Khi chịu sát thương chí tử, hồi phục HP bằng <color=#f26c1c>60%</color> HP tối đa, hồi đầy Chỉ Số Ổn Định và nhận <color=#3487e0>Tư Thế Mạnh Mẽ</color> trong <color=#f26c1c>2 hiệp lớn</color> (thời gian duy trì giảm khi kết thúc hiệp hiện tại)."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Chiến Thuật Tinh Gọn",
                "effect": "Tụ Điện nhận thêm hiệu ứng: Khi mục tiêu mang <color=#3487e0>Tụ Điện</color> kết thúc hành động, áp dụng Tụ Điện trong <color=#f26c1c>2 hiệp</color> cho tất cả đồng minh chưa có Tụ Điện trong phạm vi 3 ô xung quanh. Khi chịu ST Điện Từ, sát thương phải chịu tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Tấn Công Dịu Dàng",
                "effect": "Số lượng Pháo Tự Hành có thể cùng tồn tại trên sân tăng lên <color=#f26c1c>3</color>. Tiêu hao Chỉ Số Nhiên Liệu để kích hoạt kỹ năng này giảm <color=#f26c1c>1 điểm</color>. Sau khi dùng kỹ năng, Andoris nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color> thay vì chỉ có thể dùng lại Tấn Công Dịu Dàng.\n\nNhận thêm hiệu ứng: Với mỗi Pháo Tự Hành trên sân, khi đồng minh gây ST Điện Từ, Tấn Công tăng thêm <color=#f26c1c>10%</color> trong đòn đánh đó."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +28\nPhòng Thủ +27", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +96\nHP +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 25, "effect": "Tấn Công +33\nPhòng Thủ +37", "materials": "40\n\n\n4000"},
            {"node": "Cường Hóa 4", "level": 30, "effect": "HP +133\nHP +5.0%", "materials": "80\n\n\n8000"},
            {"node": "Cường Hóa 5", "level": 35, "effect": "Tấn Công +39\nPhòng Thủ +49", "materials": "120\n\n\n10000"},
            {"node": "Cường Hóa 6", "level": 40, "effect": "Tấn Công +45\nHP +173", "materials": "160\n\n\n12000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Lắng Nghe Cẩn Thận",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Mạch Điện Trì Trệ",
                "level": "20",
                "effect": "Khi gây ST Điện Từ, nếu mục tiêu đang trong trạng thái Sụp Đổ Ổn Định và có <color=#3487e0>Tụ Điện</color>, gây thêm ST cố định bằng <color=#f26c1c>10%</color> Tấn Công.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Chậm Mà Chắc",
                "level": "30",
                "effect": "Khi Andoris áp dụng <color=#3487e0>Điện Tích Dương</color> cho đồng minh, giải trừ <color=#f26c1c>2</color> Debuff trên đồng minh đó và tất cả Pháo Tự Hành.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4-Kết Nối Đồng Điệu",
                "level": "30",
                "effect": "Khi Andoris có mặt trên sân, nếu đồng minh mang <color=#3487e0>Điện Tích Dương</color> kết thúc hành động trong phạm vi 3 ô quanh 1 đồng minh khác cũng có Điện Tích Dương, họ nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Yểm Hộ</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5-Tình Báo Chia Sẻ",
                "level": "40",
                "effect": "Khi bắt đầu chiến đấu, áp dụng <color=#3487e0>Điện Tích Dương</color> cho tất cả đồng minh trong <color=#f26c1c>3 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6-Trinh Sát Nâng Cao",
                "level": "40",
                "effect": "Khi bắt đầu chiến đấu, áp dụng <color=#3487e0>Tụ Điện</color> lên kẻ địch có HP cao nhất trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "Unlocked at Affinity Lvl 5"
            },
            {
                "name": "Khóa Chung-Từ Trường Cảm Ứng",
                "level": "40",
                "effect": "Phòng Thủ +5% / Với mỗi Debuff loại Điện Từ hiện diện trên sân, sát thương gây ra tăng <color=#f26c1c>5%</color>, tối đa <color=#f26c1c>10%</color>, duy trì cho đến khi kết thúc hiệp lớn.",
                "materials": "None"
            },
            {
                "name": "Khóa Mở Rộng-Canh Gác Bất Diệt",
                "level": "60",
                "effect": "Khi Pháo Tự Hành kết thúc hành động mà không gây ra bất kỳ sát thương nào, tăng <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu cho Andoris. Trước khi Pháo Tự Hành tấn công mục tiêu mang <color=#3487e0>Điện Tích Âm</color>, Tấn Công của bản thân tăng <color=#f26c1c>50%</color>.\n\nKhi đồng minh mang <color=#3487e0>Điện Tích Dương</color> chịu sát thương, Andoris gánh chịu thay <color=#f26c1c>65%</color> Sát Thương Ban Đầu. Sau khi Andoris gánh chịu sát thương thay đồng minh, với mỗi tầng <color=#3487e0>Sức Ì</color> mà tất cả đồng minh đang giữ, Andoris hồi phục HP bằng <color=#f26c1c>0.5%</color> HP tối đa.\n\nKhi Andoris kết thúc hành động, áp dụng <color=#3487e0>Điện Tích Dương</color> cho đồng minh gần nhất trong <color=#f26c1c>3 hiệp</color>.",
                "materials": "3\n\n\n15000"
            }
        ],
        "summons": [
            {
                "name": "Pháo Tự Hành",
                "type": "Vật Triệu Hồi Điện Từ",
                "description": "Pháo Tự Hành không thể di chuyển, có khả năng áp dụng Điện Tích Âm và tự động tấn công khi kết thúc hiệp của Andoris.",
                "stats": {
                    "hp": "<color=#f26c1c>50%</color> HP ban đầu của Andoris",
                    "atk": "<color=#f26c1c>50%</color> Tấn Công ban đầu của Andoris",
                    "def": "<color=#f26c1c>100%</color> Phòng Thủ ban đầu của Andoris"
                },
                "skills": [
                    {
                        "name": "Bắn Tích Điện",
                        "description": "Chọn 1 mục tiêu địch trong phạm vi 6 ô, áp dụng <color=#3487e0>Điện Tích Âm</color> trong <color=#f26c1c>2 hiệp</color> và gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>100%</color> Tấn Công cùng <color=#f26c1c>1 điểm</color> ST Ổn Định."
                    },
                    {
                        "name": "Chuyển Tiếp Thông Tin",
                        "description": "Khi kết thúc hành động, áp dụng <color=#3487e0>Điện Tích Âm</color> trong <color=#f26c1c>2 hiệp</color> lên <color=#f26c1c>2 mục tiêu</color> trong phạm vi 6 ô."
                    },
                    {
                        "name": "Mô Phỏng Va Chạm",
                        "description": "Pháo Tự Hành không thể nhận trị liệu hoặc Lá Chắn, nhưng miễn nhiễm với các hiệu ứng khống chế."
                    },
                    {
                        "name": "Bắt Tốt Qua Đường",
                        "description": "Khi kẻ địch trong tầm bắn chịu ST Điện Từ đơn mục tiêu từ đòn tấn công chủ động của đồng minh, Pháo Tự Hành sẽ kích hoạt Hành Động Chi Viện trước lên kẻ địch đó, gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>100%</color> Tấn Công, <color=#f26c1c>1 điểm</color> ST Ổn Định và áp dụng <color=#3487e0>Điện Tích Âm</color> trong <color=#f26c1c>2 hiệp</color>.\n\nKỹ năng bị động này được mở khóa sau khi đạt Cường Hóa Tâm Trí Bậc 1."
                    }
                ]
            }
        ]
    },
    "balthilde": {
        "name": "Balthilde",
        "en_name": "Balthilde",
        "class": "Phòng Ngự",
        "phase": "Băng Kết",
        "rarity": "Elite",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Cờ Lê Đột Phá",
        "weakness": "Thiêu Đốt",
        "server": "global",
        "skills": [
            {
                "name": "Đòn Băng Vỡ",
                "en_name": "Cryoshatter Strike",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Nghi Thức Tăng Viện",
                "en_name": "Reinforcement Protocol",
                "tags": ["Chủ Động", "Triệu Hồi", "Phòng Ngự"],
                "description": "Chọn 1 ô địa hình trống <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, triệu hồi Cấu Trúc Phòng Thủ để bảo vệ đồng minh và Vật Cản trong phạm vi 3 ô."
            },
            {
                "name": "Nghi Thức Phá Hủy",
                "en_name": "Demolition Protocol",
                "tags": ["Chủ Động", "Triệu Hồi"],
                "description": "Chọn 1 ô địa hình trống <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, triệu hồi Cấu Trúc Tác Chiến để tấn công kẻ địch gần nhất trong phạm vi 3 ô."
            },
            {
                "name": "Bộc Phá Liên Hoàn Cuồng Nộ",
                "en_name": "Raging Chainblast",
                "tags": ["Tuyệt Kỹ", "Phạm Vi"],
                "description": "Chọn 1 ô địa hình <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#42cce0>ST Băng Kết</color> AoE bằng <color=#f26c1c>140%</color> Tấn Công lên tất cả kẻ địch trong phạm vi 3 ô và nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Hiệu Chuẩn Cờ Lê",
                "en_name": "Wrench Calibration",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Khi có Cấu Trúc trên sân, Balthilde nhận <color=#3487e0>Đột Phá Tính Năng</color>. ST Ổn Định do bản thân và các Cấu Trúc gây ra tăng thêm <color=#f26c1c>2 điểm</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Nghi Thức Phá Hủy",
                "effect": "Khi Cấu Trúc Tác Chiến tấn công, áp dụng <color=#3487e0>Khe Nứt Ứng Lực</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Nghi Thức Tăng Viện",
                "effect": "Khi triệu hồi Cấu Trúc Phòng Thủ, áp dụng <color=#3487e0>Phòng Thủ Tăng I</color> cho tất cả đồng minh trong phạm vi 3 ô trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Bộc Phá Liên Hoàn Cuồng Nộ",
                "effect": "Bộc Phá Liên Hoàn Cuồng Nộ nhận thêm hiệu ứng: Bản thân nhận <color=#3487e0>Phụ Kiện Chịu Lực</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Hiệu Chuẩn Cờ Lê",
                "effect": "Thời gian tồn tại của các Cấu Trúc tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Nghi Thức Tăng Viện",
                "effect": "HP tối đa của các Cấu Trúc tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Hiệu Chuẩn Cờ Lê",
                "effect": "Khi có Cấu Trúc trên sân, hiệu ứng của <color=#3487e0>Đột Phá Tính Năng</color> được tăng cường, Tấn Công tăng thêm <color=#f26c1c>15%</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +34\nPhòng Thủ +23", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +90\nHP +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +52\nPhòng Thủ +38", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +63\nPhòng Thủ +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +150\nPhòng Thủ +46", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +73\nPhòng Thủ +54", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Không Thể Nhổ Ra",
                "level": "20",
                "effect": "Trước khi dùng tấn công chủ động, áp dụng <color=#3487e0>Khe Nứt Ứng Lực</color> lên kẻ địch trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Nóng Vội",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Ý Đồ Bị Hiểu Lầm",
                "level": "30",
                "effect": "Khi kết thúc hành động, áp dụng giảm thương cho tất cả đồng minh không ở gần Vật Cản trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Mô-đun Loại Trừ Lỗi",
                "level": "30",
                "effect": "Khi kết thúc hành động, hồi phục <color=#f26c1c>3 điểm</color> Chỉ Số Ổn Định cho đồng minh có Chỉ Số Ổn Định thấp nhất.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Cải Tiến Thực Dụng",
                "level": "40",
                "effect": "Trước khi đồng minh bị tấn công, Cấu Trúc Phòng Thủ hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định cho họ.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Điều Khiển Cơ Khí",
                "level": "40",
                "effect": "Khi có Cấu Trúc trên sân, ST Ổn Định do bản thân gây ra tăng thêm <color=#f26c1c>3 điểm</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Thợ Rèn Lành Nghề",
                "level": "40",
                "effect": "Phòng Thủ +3.0% / Khi di chuyển từ 3 ô trở lên, ST gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Thức Tỉnh Thép",
                "level": "60",
                "effect": "Khi kích hoạt, tiêu hao Chỉ Số Nhiên Liệu để gây <color=#42cce0>ST Băng Kết</color> AoE và nhận <color=#3487e0>Phụ Kiện Chịu Lực</color>.",
                "materials": "1\n\n\n3000"
            }
        ],
        "summons": [
            {
                "name": "Cấu Trúc Phòng Thủ",
                "type": "Vật Triệu Hồi Băng Kết",
                "description": "Kế thừa thuộc tính của Balthilde, bảo vệ đồng minh và Vật Cản trong phạm vi 3 ô xung quanh.",
                "stats": {
                    "hp": "<color=#f26c1c>100%</color> HP ban đầu của Balthilde",
                    "atk": "<color=#f26c1c>80%</color> Tấn Công ban đầu của Balthilde",
                    "def": "<color=#f26c1c>80%</color> Phòng Thủ ban đầu của Balthilde"
                },
                "skills": [
                    {
                        "name": "Ý Thức An Toàn",
                        "description": "Khi được triệu hồi, áp dụng <color=#3487e0>Phòng Thủ Tăng I</color> trong <color=#f26c1c>2 hiệp</color> và hồi phục HP bằng <color=#f26c1c>100%</color> Phòng Thủ cho tất cả đồng minh trong phạm vi 3 ô."
                    },
                    {
                        "name": "Bảo Trì Trọng Điểm",
                        "description": "Vật Cản trong phạm vi 3 ô không bị mất độ bền. Giảm <color=#f26c1c>30%</color> sát thương phải chịu cho đồng minh trong phạm vi không được hưởng giảm thương từ Vật Cản."
                    }
                ]
            },
            {
                "name": "Cấu Trúc Tác Chiến",
                "type": "Vật Triệu Hồi Băng Kết",
                "description": "Kế thừa thuộc tính của Balthilde, tự động tấn công kẻ địch gần nhất trong phạm vi 3 ô.",
                "stats": {
                    "hp": "<color=#f26c1c>100%</color> HP ban đầu của Balthilde",
                    "atk": "<color=#f26c1c>80%</color> Tấn Công ban đầu của Balthilde",
                    "def": "<color=#f26c1c>80%</color> Phòng Thủ ban đầu của Balthilde"
                },
                "skills": [
                    {
                        "name": "Bí Quyết Tháo Dỡ",
                        "description": "Chọn mục tiêu địch gần nhất trong phạm vi 3 ô và gây ST Vật Lý bằng <color=#f26c1c>100%</color> Phòng Thủ. Mỗi hiệp có thể dùng <color=#f26c1c>2 lần</color>."
                    }
                ]
            }
        ]
    },
    "basti": {
        "name": "Basti",
        "en_name": "Basti",
        "class": "Tiên Phong",
        "phase": "Ăn Mòn",
        "rarity": "Elite",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Sơn Xịt Nổi Loạn",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Khiêu Khích Liều Lĩnh",
                "en_name": "Reckless Provocation",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Ảnh Hưởng Xấu",
                "en_name": "Bad Influence",
                "tags": ["Chủ Động", "Dịch Chuyển", "Trị Liệu"],
                "description": "Chọn 1 đồng minh trong phạm vi 6 ô rồi chọn 1 ô địa hình Độc Chướng của phe ta, dịch chuyển đồng minh đến đó, hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công, <color=#f26c1c>5 điểm</color> Chỉ Số Ổn Định, giải trừ 2 Debuff và áp dụng <color=#3487e0>Duy Trì Chữa Lành II</color> trong <color=#f26c1c>2 hiệp</color>. Dịch chuyển Basti đến gần đồng minh đó và nhận <color=#f26c1c>6 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color>."
            },
            {
                "name": "Bé Gái Đặt Mìn",
                "en_name": "Landmine Gal",
                "tags": ["Chủ Động", "Triệu Hồi", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 ô trống trong phạm vi 6 ô và triệu hồi Cục Cưng. Sau khi dùng kỹ năng, Basti có thể dùng tiếp kỹ năng chủ động hoặc tuyệt kỹ. Mỗi hiệp tối đa dùng 2 lần.\n\nKhi kẻ địch tiến vào phạm vi 3 ô quanh Cục Cưng, nó tự phát nổ gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công, <color=#f26c1c>2 điểm</color> ST Ổn Định, tạo ô địa hình <color=#3487e0>Độc Chướng</color>, áp dụng <color=#3487e0>Ngập Tràn Độc Tố</color> và <color=#3487e0>Choáng</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Bẫy Bọc Đường",
                "en_name": "Sugar-Coated Trap",
                "tags": ["Tuyệt Kỹ", "Phạm Vi", "Ô Địa Hình", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch trong phạm vi 8 ô, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>150%</color> Tấn Công lên mục tiêu và tất cả kẻ địch trong phạm vi 8 ô xung quanh, tạo ô địa hình <color=#3487e0>Độc Chướng</color> trong <color=#f26c1c>2 hiệp</color> và áp dụng <color=#f26c1c>1 lớp</color> <color=#3487e0>Ghi Hận</color>."
            },
            {
                "name": "Thế Giới Graffiti",
                "en_name": "The World of Graffiti",
                "tags": ["Bị Động", "Ô Địa Hình", "Suy Yếu", "Cường Hóa"],
                "description": "Khi bắt đầu hiệp, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Tạo ô địa hình <color=#3487e0>Độc Chướng</color> dưới chân đồng minh khi bắt đầu chiến đấu và xung quanh bản thân sau khi di chuyển. Kẻ địch đứng trên Độc Chướng nhận <color=#3487e0>Mặt Quỷ Nhăn Nhó</color>. Khi triệu hồi Cục Cưng, đồng minh trên Độc Chướng nhận <color=#3487e0>Dấu Ấn Đồng Đội</color> và <color=#3487e0>Tấn Công Tăng II</color> trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Bé Gái Đặt Mìn",
                "effect": "Số lượng Cục Cưng có thể tồn tại đồng thời tăng thêm <color=#f26c1c>1</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Thế Giới Graffiti",
                "effect": "Đồng minh đứng trên ô Độc Chướng nhận thêm hiệu ứng <color=#3487e0>Nước Tăng Lực</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Thế Giới Graffiti",
                "effect": "Hiệu quả của <color=#3487e0>Dấu Ấn Đồng Đội</color> và <color=#3487e0>Mặt Quỷ Nhăn Nhó</color> tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Bẫy Bọc Đường",
                "effect": "Bẫy Bọc Đường áp dụng thêm <color=#3487e0>Giải Phóng Phụ Thuộc</color> lên kẻ địch trúng đòn trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Bẫy Bọc Đường",
                "effect": "Bẫy Bọc Đường áp dụng thêm <color=#3487e0>Choáng</color> và <color=#3487e0>Dẫn Dụ</color> lên mục tiêu chính trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Bé Gái Đặt Mìn",
                "effect": "Thời gian hồi chiêu của Bé Gái Đặt Mìn giảm <color=#f26c1c>1 hiệp</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +33\nPhòng Thủ +24", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +92\nHP +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +51\nPhòng Thủ +39", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +62\nPhòng Thủ +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +152\nPhòng Thủ +48", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +72\nPhòng Thủ +55", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Khoảnh Khắc Cảm Hứng",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Nghệ Thuật Đường Phố",
                "level": "20",
                "effect": "Phạm vi tạo ô địa hình Độc Chướng mở rộng thêm <color=#f26c1c>1 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Phụ Thuộc Nỗi Đau",
                "level": "30",
                "effect": "Khi đứng trên ô Độc Chướng, ST phải chịu giảm <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Thiên Tài Tai Họa",
                "level": "30",
                "effect": "Khi Cục Cưng phát nổ, hồi phục thêm <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho Basti.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Món Quà Đáng Sợ",
                "level": "40",
                "effect": "Sát thương do Cục Cưng phát nổ gây ra tăng thêm <color=#f26c1c>25%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Vệt Sơn Tình Yêu",
                "level": "40",
                "effect": "Khi đồng minh đứng trên ô Độc Chướng phát động tấn công, ST gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Hat Trick",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Chiếm Hữu Chết Người",
                "level": "40",
                "effect": "HP +3.0% / ST Ăn Mòn gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            }
        ],
        "summons": [
            {
                "name": "Cục Cưng",
                "type": "Vật Triệu Hồi Ăn Mòn",
                "description": "Vật triệu hồi kế thừa thuộc tính cơ bản của Basti. Tự phát nổ gây sát thương Ăn Mòn và tạo ô Độc Chướng khi kẻ địch lại gần.",
                "stats": {
                    "hp": "<color=#f26c1c>100%</color> HP ban đầu của Basti",
                    "atk": "<color=#f26c1c>100%</color> Tấn Công ban đầu của Basti",
                    "def": "<color=#f26c1c>100%</color> Phòng Thủ ban đầu của Basti"
                },
                "skills": []
            }
        ]
    },
    "belka": {
        "name": "Belka",
        "en_name": "Belka",
        "class": "Đột Kích",
        "phase": "Điện Từ",
        "rarity": "Elite",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Hạt Dẻ Điện Quang",
        "weakness": "Vật Lý",
        "server": "global",
        "skills": [
            {
                "name": "Vỏ Hạt Kẹp Bổ",
                "en_name": "Nutcracker Shell",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Nhảy Vọt Rừng Già",
                "en_name": "Sylvan Vault",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>130%</color> Tấn Công và áp dụng <color=#3487e0>Điện Tích Âm</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Lõi Lách Tách",
                "en_name": "Crackling Core",
                "tags": ["Chủ Động", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>130%</color> Tấn Công và bản thân nhận <color=#3487e0>Tác Chiến Tích Cực</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Vòng Cung Nhảy Múa",
                "en_name": "Leaping Arc",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>180%</color> Tấn Công, áp dụng <color=#3487e0>Dẫn Điện</color> và <color=#3487e0>Duy Trì Phóng Điện</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Bí Mật Rừng Sâu",
                "en_name": "Forest's Secrets",
                "tags": ["Bị Động", "Suy Yếu", "Cường Hóa"],
                "description": "Khi kết thúc hành động, áp dụng <color=#3487e0>Điện Tích Âm</color> lên kẻ địch gần nhất trong phạm vi 6 ô trong <color=#f26c1c>2 hiệp</color> và bản thân nhận <color=#3487e0>Ẩn Náu</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Lõi Lách Tách",
                "effect": "Lõi Lách Tách áp dụng thêm <color=#3487e0>Điện Tích Âm</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Vòng Cung Nhảy Múa",
                "effect": "Khi dùng Vòng Cung Nhảy Múa, nhận thêm <color=#3487e0>Điện Tử Tràn Ra</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Bí Mật Rừng Sâu",
                "effect": "Khi kích hoạt Bí Mật Rừng Sâu, bản thân nhận <color=#3487e0>Lưu Trữ Điện Năng</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Bí Mật Rừng Sâu",
                "effect": "Số lớp tích lũy tối đa của <color=#3487e0>Lưu Trữ Điện Năng</color> tăng thêm <color=#f26c1c>1 lớp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Nhảy Vọt Rừng Già",
                "effect": "Hệ số ST của Nhảy Vọt Rừng Già tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Vòng Cung Nhảy Múa",
                "effect": "Thời gian duy trì của <color=#3487e0>Duy Trì Phóng Điện</color> tăng thêm <color=#f26c1c>1 hiệp</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +37\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +76\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +58\nPhòng Thủ +31", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +71\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +126\nPhòng Thủ +38", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +83\nPhòng Thủ +45", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Năng Lượng Sôi Nổi",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Đợt Tấn Công Lệ Rơi",
                "level": "20",
                "effect": "Khi Belka có <color=#3487e0>Duy Trì Phóng Điện</color>, bản thân miễn dịch với các hiệu ứng dịch chuyển vị trí.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Khuấy Động Không Khí",
                "level": "30",
                "effect": "Khi bắt đầu hiệp, nếu có kẻ địch trong phạm vi 5 ô, nhận <color=#3487e0>Di Chuyển Tăng I</color> trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Chiếc Đuôi Dựng Đứng",
                "level": "30",
                "effect": "Khi đồng minh gây <color=#d4a017>ST Dẫn Điện</color> lên kẻ địch có <color=#3487e0>Điện Tích Âm</color>, Tấn Công tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Khen Ngợi Mong Mỏi",
                "level": "40",
                "effect": "Khi kết thúc hành động, nếu có đơn vị Boss chịu <color=#3487e0>Điện Tích Âm</color>, nhận <color=#3487e0>TL Bạo Kích Tăng I</color> và <color=#3487e0>ST tăng I</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Động Cơ Quyết Định",
                "level": "40",
                "effect": "Trước khi dùng Vòng Cung Nhảy Múa, giải trừ <color=#f26c1c>2</color> Buff trên người mục tiêu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Ý Chí Tranh Sủng",
                "level": "40",
                "effect": "TL Bạo Kích +3.0% / ST Điện Từ gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Giác Ngộ Của Sóc",
                "level": "60",
                "effect": "Khi dùng kỹ năng chủ động tiêu hao Di Chuyển lớn hơn 10 điểm, chỉ tính là tiêu hao 10 điểm.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "cheyanne": {
        "name": "Cheyanne",
        "en_name": "Cheyanne",
        "class": "Hỏa Lực",
        "phase": "Ăn Mòn",
        "rarity": "Elite",
        "weapon_type": "Súng Bắn Tỉa",
        "ammo_type": "Đạn Nặng",
        "signature_weapon": "Lời Tỏ Tình Nhút Nhát",
        "weakness": "Vật Lý",
        "server": "global",
        "skills": [
            {
                "name": "Phát Huy Tiềm Năng",
                "en_name": "Playing to Potential",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Bức Tường Bản Ngã",
                "en_name": "Wall of One's Self",
                "tags": ["Chủ Động", "Ô Địa Hình", "Cường Hóa"],
                "description": "Tạo ô địa hình Vật Cản / Điểm Cao, nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>, <color=#3487e0>Đài Hoa E Thẹn</color> và tạo <color=#3487e0>Khói</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Kiên Trì Truy Đuổi",
                "en_name": "Steadfast Pursuit",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công và áp dụng <color=#3487e0>Tâm Bia</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Xuyên Mây Hướng Mặt Trời",
                "en_name": "Piercing the Clouds, Into the Sun",
                "tags": ["Tuyệt Kỹ", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng <color=#f26c1c>180%</color> Tấn Công, nhận <color=#3487e0>Giá Trị Phân Tích</color>."
            },
            {
                "name": "Kế Hoạch Tỉ Mỉ",
                "en_name": "Meticulous Planning",
                "tags": ["Bị Động", "Chỉ Định", "Cường Hóa"],
                "description": "Khi bắt đầu hành động, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Tích lũy <color=#3487e0>Giá Trị Phân Tích</color> khi tấn công kẻ địch bị đánh dấu <color=#3487e0>Tâm Bia</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Kế Hoạch Tỉ Mỉ",
                "effect": "Lượng <color=#3487e0>Giá Trị Phân Tích</color> tích lũy tăng thêm <color=#f26c1c>1 điểm</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Xuyên Mây Hướng Mặt Trời",
                "effect": "Khi dùng Xuyên Mây Hướng Mặt Trời, áp dụng <color=#3487e0>Tâm Bia</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Kiên Trì Truy Đuổi",
                "effect": "Hệ số ST của Kiên Trì Truy Đuổi tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Bức Tường Bản Ngã",
                "effect": "Khi đứng trên ô do Bức Tường Bản Ngã tạo ra, bản thân nhận <color=#3487e0>Cảm Giác An Toàn</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Xuyên Mây Hướng Mặt Trời",
                "effect": "Hệ số ST của Xuyên Mây Hướng Mặt Trời tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Kế Hoạch Tỉ Mỉ",
                "effect": "Kế Hoạch Tỉ Mỉ nhận thêm hiệu ứng: Bản thân nhận <color=#3487e0>Tích Lũy Làm Nóng</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +38\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +76\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +59\nPhòng Thủ +31", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +72\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +128\nPhòng Thủ +38", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +84\nPhòng Thủ +45", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Đừng Lại Gần, Tôi Ngại",
                "level": "20",
                "effect": "Khi gây ST Chuẩn Xác, đẩy lùi mục tiêu <color=#f26c1c>2 ô</color> và áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Tôi Tự Do",
                "level": "20",
                "effect": "Cheyanne miễn dịch với các Debuff <color=#3487e0>Khiêu Khích</color>, <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Chạy Trốn</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Một Bước Nhỏ Dũng Cảm",
                "level": "30",
                "effect": "Khi bắt đầu chiến đấu, Tầm Di Chuyển tăng <color=#f26c1c>2 ô</color> trong <color=#f26c1c>1 hiệp</color>. Tạo 1 Điểm Cao ở ô trống gần nhất.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Cách Ly Xã Hội",
                "level": "30",
                "effect": "Khi kẻ địch chịu <color=#3487e0>Tâm Bia</color> tử vong, chuyển Tâm Bia sang cho kẻ địch có lượng HP cao nhất trên sân.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Tinh Thần Kiên Cường",
                "level": "40",
                "effect": "Khi bản thân ở trên ô địa hình Ăn Mòn, ST gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Tập Trung Toàn Lực",
                "level": "40",
                "effect": "Khi mục tiêu chịu Tâm Bia kết thúc hành động, phát động 1 đòn tấn công phụ lên mục tiêu và hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Hồi Hộp Ngóng Trông",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Hội Ngộ Bấy Lâu",
                "level": "40",
                "effect": "Tấn Công +3.0% / Khi ở trên ô địa hình Ăn Mòn, ST gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "dushevnaya": {
        "name": "Dushevnaya",
        "en_name": "Dushevnaya",
        "class": "Hỗ Trợ",
        "phase": "Băng Kết",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Bản Hùng Ca Băng Giá",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Rạng Đông",
                "en_name": "Daybreak",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Quy Tắc Dũng Sĩ",
                "en_name": "Hero's Code",
                "tags": ["Chủ Động", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây <color=#42cce0>ST Băng Kết</color> bằng <color=#f26c1c>130%</color> Tấn Công và nhận <color=#3487e0>Chúc Phúc Hàn Băng</color>."
            },
            {
                "name": "Trừng Phạt Của Marzanna",
                "en_name": "Marzanna's Sanction",
                "tags": ["Chủ Động", "Suy Yếu", "Ô Địa Hình"],
                "description": "Tạo ô địa hình Băng Kết trong phạm vi, gây <color=#42cce0>ST Băng Kết</color> AoE và áp dụng <color=#3487e0>Cứng Đờ</color> cùng <color=#3487e0>Băng Giá</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Sách Tiên Tri",
                "en_name": "Book of Prophecy",
                "tags": ["Tuyệt Kỹ", "Cường Hóa", "Hỗ Trợ"],
                "description": "Áp dụng <color=#3487e0>Lời Chúc Cực Hàn</color> và tạo <color=#3487e0>Lĩnh Vực Cực Hàn</color> cho tất cả đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Tác Phẩm Được Ban Phước",
                "en_name": "Blessed Artwork",
                "tags": ["Bị Động", "Cường Hóa", "Hỗ Trợ"],
                "description": "Bản thân nhận <color=#3487e0>Nhìn Thấu</color>. Khi đồng minh đứng trên ô Băng Giá phát động tấn công, Dushevnaya chi viện tăng cường sát thương."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Sách Tiên Tri",
                "effect": "Sách Tiên Tri áp dụng thêm <color=#3487e0>Di Chuyển Tăng II</color> cho đồng minh trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tác Phẩm Được Ban Phước",
                "effect": "Ô địa hình Băng Giá tạo thêm <color=#3487e0>Băng Giá</color> lên kẻ địch đi vào."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Trừng Phạt Của Marzanna",
                "effect": "Thời gian hồi chiêu của Trừng Phạt Của Marzanna giảm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Quy Tắc Dũng Sĩ",
                "effect": "Quy Tắc Dũng Sĩ nhận thêm <color=#f26c1c>1 lớp</color> <color=#3487e0>Chúc Phúc Hàn Băng</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Sách Tiên Tri",
                "effect": "Thời gian duy trì của Lời Chúc Cực Hàn tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Tác Phẩm Được Ban Phước",
                "effect": "Tác Phẩm Được Ban Phước áp dụng thêm <color=#3487e0>Dễ Bị Thương II</color> lên kẻ địch trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +36\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +74\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +56\nPhòng Thủ +31", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +69\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +124\nPhòng Thủ +38", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +80\nPhòng Thủ +45", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Thương Longinus",
                "level": "20",
                "effect": "Với mỗi lớp <color=#3487e0>Chúc Phúc Hàn Băng</color> dư ra, tăng <color=#f26c1c>5%</color> TL Bạo Kích cho Quy Tắc Dũng Sĩ, tối đa tăng <color=#f26c1c>30%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Ý Chí Nhà Thám Hiểm",
                "level": "20",
                "effect": "Kèm <color=#3487e0>Chúc Phúc Hàn Băng</color> trước khi tấn công chủ động, ST gây ra tăng <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Hỗ Trợ Ma Pháp",
                "level": "30",
                "effect": "Khi kỹ năng chủ động tạo ô Băng Giá, giải trừ <color=#f26c1c>1</color> Buff trên kẻ địch và nhận <color=#3487e0>Chúc Phúc Hàn Băng</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Trọng Kiếm Can Đảm",
                "level": "30",
                "effect": "Khi dùng Trừng Phạt Của Marzanna gây Sụp Đổ Ổn Định, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Trái Tim Hiền Triết",
                "level": "40",
                "effect": "Khi có <color=#3487e0>Lĩnh Vực Cực Hàn</color>, bản thân miễn dịch với Debuff loại di chuyển.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Ánh Sáng Thánh",
                "level": "40",
                "effect": "Khi bắt đầu hiệp, nếu đứng trên ô Băng Giá của đồng minh, giải trừ <color=#f26c1c>2</color> Debuff trên bản thân.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Ký Ức Lấp Lánh",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Cảm Hứng Nghệ Thuật",
                "level": "40",
                "effect": "Tấn Công +3.0% / ST Băng Kết gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Khúc Ca Mùa Đông Dũng Sĩ",
                "level": "60",
                "effect": "Khi đồng minh gây ST Băng Kết, nhận <color=#3487e0>Chúc Phúc Hàn Băng</color> và tăng <color=#42cce0>ST Băng Kết</color> của toàn đội thêm <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "faye": {
        "name": "Faye",
        "en_name": "Faye",
        "class": "Tiên Phong",
        "phase": "Hóa Lỏng",
        "rarity": "Elite",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Lưỡi Rìu Săn Thú",
        "weakness": "Ăn Mòn",
        "server": "global",
        "skills": [
            {
                "name": "Bắn Tập",
                "en_name": "Practice Shot",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Vòng Xoay Hủy Diệt",
                "en_name": "Ruinous Whirl",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>110%</color> Tấn Công lên tất cả kẻ địch trong phạm vi 2 ô, nhận thêm <color=#f26c1c>3 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color>, áp dụng <color=#3487e0>Vô Hiệu Hóa Di Chuyển</color>, <color=#3487e0>Liệt Thương</color> và <color=#3487e0>Di Hình</color>."
            },
            {
                "name": "Tia Sáng Phân Hạch",
                "en_name": "Fissioned Firelight",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>140%</color> Tấn Công và áp dụng <color=#3487e0>Liệt Thương</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Không Ai Sống Sót",
                "en_name": "No Survivors",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>180%</color> Tấn Công, áp dụng <color=#3487e0>Liệt Thương</color> và <color=#3487e0>Vết Thương</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Liên Hoàn Rìu Chiến",
                "en_name": "Tomahawk Combo",
                "tags": ["Bị Động", "Suy Yếu", "Cường Hóa"],
                "description": "Khi tấn công mục tiêu chịu <color=#3487e0>Liệt Thương</color>, ST gây ra tăng thêm <color=#f26c1c>15%</color> và gây thêm <color=#f26c1c>2 điểm</color> ST Ổn Định."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Liên Hoàn Rìu Chiến",
                "effect": "Sát thương do <color=#3487e0>Liệt Thương</color> kích hoạt tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tia Sáng Phân Hạch",
                "effect": "Tia Sáng Phân Hạch áp dụng thêm <color=#3487e0>Vết Thương</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Liên Hoàn Rìu Chiến",
                "effect": "Khi đánh trúng kẻ địch có Liệt Thương, áp dụng thêm <color=#3487e0>Vô Hiệu Hóa Di Chuyển</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Không Ai Sống Sót",
                "effect": "Hệ số ST của Không Ai Sống Sót tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Vòng Xoay Hủy Diệt",
                "effect": "Vòng Xoay Hủy Diệt nhận thêm hiệu ứng: Tăng thời gian duy trì của <color=#3487e0>Di Hình</color> thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Không Ai Sống Sót",
                "effect": "Sau khi dùng Không Ai Sống Sót tiêu diệt mục tiêu, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +34\nPhòng Thủ +23", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +90\nHP +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +52\nPhòng Thủ +38", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +63\nPhòng Thủ +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +150\nPhòng Thủ +46", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +73\nPhòng Thủ +54", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1-Lần Theo Mùi Hương",
                "level": "20",
                "effect": "Với mỗi kẻ địch trên sân chịu <color=#3487e0>Liệt Thương</color>, Tầm Di Chuyển của Faye tăng thêm <color=#f26c1c>1 ô</color>, tối đa tăng <color=#f26c1c>3 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2-Nhát Chém Tất Tay",
                "level": "20",
                "effect": "ST Bạo Kích tăng <color=#f26c1c>25%</color>, Tấn Công tăng <color=#f26c1c>20%</color>, ST Ổn Định tăng <color=#f26c1c>8 điểm</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3-Vật Tư Tiếp Cứu",
                "level": "30",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4-Phương Án Khẩn Cấp",
                "level": "30",
                "effect": "ST gây ra tăng <color=#f26c1c>30%</color>, ST phải chịu tăng <color=#f26c1c>50%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5-Bảo Hộ Nguy Cấp",
                "level": "40",
                "effect": "Khi kết thúc hành động, nếu có kẻ địch chịu <color=#3487e0>Liệt Thương</color> trong phạm vi 2 ô, Faye nhận giảm thương trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6-Trong Hỗn Chiến",
                "level": "40",
                "effect": "Khi kẻ địch có <color=#3487e0>Liệt Thương</color> tử vong, bản thân tăng <color=#f26c1c>4%</color> Tấn Công, tối đa tăng <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Tử Đấu",
                "level": "40",
                "effect": "TL Bạo Kích +3.0% / ST Hóa Lỏng gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "60",
                "effect": "ST Hóa Lỏng gây ra cho kẻ địch có từ 2 Debuff trở lên tăng thêm <color=#f26c1c>30%</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    }
}

def main():
    print("Loading data/i18n_vi.json...")
    with open(I18N_PATH, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    chars = bundle.setdefault("characters", {})

    for slug, new_data in BATCH_2_DATA.items():
        print(f"Updating {slug} in i18n_vi...")
        existing = chars.get(slug, {})
        # Update fields
        existing["name"] = new_data["name"]
        existing["en_name"] = new_data["en_name"]
        existing["class"] = new_data["class"]
        existing["phase"] = new_data["phase"]
        existing["rarity"] = new_data["rarity"]
        existing["weapon_type"] = new_data["weapon_type"]
        existing["ammo_type"] = new_data["ammo_type"]
        existing["signature_weapon"] = new_data["signature_weapon"]
        existing["weakness"] = new_data["weakness"]
        existing["server"] = new_data["server"]
        existing["skills"] = new_data["skills"]
        existing["fortification"] = new_data["fortification"]
        existing["neural_helix"] = new_data["neural_helix"]
        existing["keys"] = new_data["keys"]
        if "summons" in new_data:
            existing["summons"] = new_data["summons"]
        chars[slug] = existing

    # Save transactional changes
    tx = RepositoryTransaction(ROOT)
    try:
        stage_i18n_bundle(ROOT, tx, bundle)
        tx.commit()
        print("Successfully committed Batch 2 changes to data/i18n_vi.json and site/static/js/i18n-vi.js.")
    except Exception as e:
        tx.rollback()
        print(f"Error applying Batch 2: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
