#!/usr/bin/env python3
"""
tools/apply_batch1_translations.py
Applies verified, high-quality Vietnamese translations for Batch 1 (10 Standard 4-star dolls):
  cheeta, colphne, groza, krolik, ksenia, littara, lotta, nagant, nemesis, sharkry.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_core.bundle import stage_i18n_bundle
I18N_PATH = ROOT / "data" / "i18n_vi.json"

BATCH_1_DATA = {
    "cheeta": {
        "name": "Cheeta",
        "en_name": "Cheeta",
        "class": "Đột Kích",
        "phase": "Vật Lý",
        "rarity": "Standard",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Tia Sáng Nhỏ",
        "weakness": "Điện Từ",
        "server": "global",
        "skills": [
            {
                "name": "Quà Gặp Mặt",
                "en_name": "Welcome Gift",
                "tags": ["Đánh Thường", "Chuẩn Xác"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Kẹo Cay",
                "en_name": "Spicy Candy",
                "tags": ["Chủ Động", "Chuẩn Xác"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý loại đạn nhẹ bằng <color=#f26c1c>120%</color> Tấn Công."
            },
            {
                "name": "Dạ Tiệc Pháo Hoa",
                "en_name": "Fireworks Festival",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Gây ST Vật Lý AoE bằng <color=#f26c1c>75%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định lên tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 2 ô xung quanh</color> mục tiêu. Nếu mục tiêu có Debuff loại di chuyển, ST gây ra tăng <color=#f26c1c>20%</color>."
            },
            {
                "name": "Hộp Mù Bất Ngờ",
                "en_name": "Surprise Box",
                "tags": ["Chủ Động", "Cường Hóa", "Hỗ Trợ"],
                "description": "Áp dụng ngẫu nhiên <color=#f26c1c>2</color> hiệu ứng Buff trong <color=#3487e0>Tấn Công Tăng I</color>, <color=#3487e0>Phòng Thủ Tăng I</color>, <color=#3487e0>Di Chuyển Tăng I</color> hoặc <color=#3487e0>TL Bạo Kích Tăng I</color> cho tất cả đơn vị đồng minh <color=#f26c1c>trong phạm vi 3 ô xung quanh</color>, duy trì <color=#f26c1c>2 hiệp</color>. Nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Phát Minh Của Thế Kỷ",
                "en_name": "Invention of the Century",
                "tags": ["Bị Động", "Trị Liệu"],
                "description": "Khi kết thúc hiệp, hồi phục HP bằng <color=#f26c1c>50%</color> Tấn Công cho đơn vị đồng minh có tỷ lệ phần trăm HP thấp nhất <color=#f26c1c>trong phạm vi 3 ô xung quanh</color>. Nếu đồng minh có từ <color=#f26c1c>3 hiệu ứng Buff trở lên</color>, hồi phục thêm <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Hộp Mù Bất Ngờ",
                "effect": "Số lượng hiệu ứng Buff ngẫu nhiên nhận được tăng thêm <color=#f26c1c>1</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Kẹo Cay",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Dạ Tiệc Pháo Hoa",
                "effect": "Tiêu hao Chỉ Số Nhiên Liệu giảm <color=#f26c1c>1 điểm</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Phát Minh Của Thế Kỷ",
                "effect": "Mỗi khi bản thân có 1 hiệu ứng Buff, hệ số trị liệu tăng <color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>30%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Phát Minh Của Thế Kỷ",
                "effect": "Hệ số trị liệu tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Hộp Mù Bất Ngờ",
                "effect": "Lượng Chỉ Số Nhiên Liệu nhận được tăng thêm <color=#f26c1c>1 điểm</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +28\nPhòng Thủ +21", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +78\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +46\nPhòng Thủ +35", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +56\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +130\nPhòng Thủ +42", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +65\nPhòng Thủ +49", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Phạm vi của <color=#3487e0>Hành Động Chi Viện</color> tăng <color=#f26c1c>2 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "KN chủ động Kẹo Cay nhận thêm hiệu ứng: Khi bản thân có <color=#3487e0>Thế Công Rực Lửa I</color>, hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công cho 1 mục tiêu đồng minh gần nhất (ngoại trừ bản thân).",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Mỗi khi bản thân có 1 hiệu ứng Buff, Tấn Công tăng <color=#f26c1c>3%</color>, tối đa tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "KN chủ động Dạ Tiệc Pháo Hoa không còn gây ST lên mục tiêu địch. Hiệu ứng đổi thành: hồi phục HP bằng <color=#f26c1c>90%</color> Tấn Công cho các mục tiêu đồng minh trong phạm vi và giải trừ <color=#f26c1c>1</color> hiệu ứng Debuff.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Khi kết thúc hành động, nếu bản thân có <color=#3487e0>Thế Công Rực Lửa I</color>, hồi phục HP bằng <color=#f26c1c>20%</color> Tấn Công cho bản thân.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Vận May Thiên Tài",
                "level": "20",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Phát Minh Vi Diệu",
                "level": "20",
                "effect": "Tấn Công +3.0% / Khi dùng kỹ năng hồi máu chủ động, có <color=#f26c1c>50%</color> xác suất áp dụng <color=#f26c1c>1</color> hiệu ứng Buff ngẫu nhiên lên mục tiêu trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "20",
                "effect": "Hộp Mù Bất Ngờ: Sau khi dùng tấn công chủ động, thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "colphne": {
        "name": "Colphne",
        "en_name": "Colphne",
        "class": "Hỗ Trợ",
        "phase": "Hóa Lỏng",
        "rarity": "Standard",
        "weapon_type": "Súng Ngắn",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Trọng Kích",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Phản Ứng Nhanh",
                "en_name": "Quick Reaction",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Cứu Hộ Khẩn Cấp",
                "en_name": "Crisis Aid",
                "tags": ["Chủ Động", "Trị Liệu", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công, áp dụng <color=#3487e0>Duy Trì Chữa Lành II</color> và <color=#3487e0>Hồi Phục Ổn Định Liên Tục I</color> cho mục tiêu trong <color=#f26c1c>1 hiệp</color>. Nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Ánh Sáng Chiến Trường",
                "en_name": "Faint Glow of the Battlefield",
                "tags": ["Chủ Động", "Chỉ Định", "Trị Liệu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>130%</color> Tấn Công. Đồng thời, hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công cho đơn vị đồng minh có lượng HP thấp nhất."
            },
            {
                "name": "Xử Lý Khẩn Cấp",
                "en_name": "Emergency Treatment",
                "tags": ["Tuyệt Kỹ", "Trị Liệu", "Giải Trừ"],
                "description": "Chọn 1 mục tiêu đồng minh <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, hồi phục HP bằng <color=#f26c1c>140%</color> Tấn Công và <color=#f26c1c>4 điểm</color> Chỉ Số Ổn Định, giải trừ <color=#f26c1c>2</color> hiệu ứng Debuff đồng thời xóa bỏ hiệu ứng <color=#3487e0>Khiêu Khích</color> và <color=#3487e0>Chạy Trốn</color>."
            },
            {
                "name": "Phác Đồ Điều Trị",
                "en_name": "Medical Contingency",
                "tags": ["Bị Động", "Hỗ Trợ"],
                "description": "Khi đơn vị địch trong tầm bắn chịu ST chuẩn xác từ đơn vị đồng minh, ưu tiên tiến hành 1 lần Hành Động Chi Viện, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn Định, đồng thời áp dụng <color=#3487e0>Tấn Công Tăng I</color> cho đơn vị đồng minh đó trong <color=#f26c1c>2 hiệp</color>. Nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Mỗi hiệp tối đa kích hoạt 1 lần.\n\nKhi dùng kỹ năng trị liệu chủ động lên đơn vị đồng minh, nếu mục tiêu đang trong trạng thái Sụp Đổ Ổn Định, hồi phục thêm <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định. Thời gian hồi: <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Cứu Hộ Khẩn Cấp",
                "effect": "Nếu HP của mục tiêu được hồi phục đầy sau khi trị liệu, nhận ngẫu nhiên <color=#f26c1c>1</color> hiệu ứng Buff trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Ánh Sáng Chiến Trường",
                "effect": "Trong hiệp này, số lần Hành Động Chi Viện tăng thêm <color=#f26c1c>1 lần</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Phác Đồ Điều Trị",
                "effect": "Lượng hồi phục Chỉ Số Ổn Định tăng thêm <color=#f26c1c>2 điểm</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Xử Lý Khẩn Cấp",
                "effect": "Hệ số trị liệu tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Phác Đồ Điều Trị",
                "effect": "Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Xử Lý Khẩn Cấp",
                "effect": "Lượng hồi phục Chỉ Số Ổn Định tăng thêm <color=#f26c1c>1 điểm</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +24\nPhòng Thủ +21", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +75\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +41\nPhòng Thủ +35", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +50\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +126\nPhòng Thủ +43", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +59\nPhòng Thủ +50", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "KN chủ động Cứu Hộ Khẩn Cấp áp dụng <color=#3487e0>Phòng Thủ Tăng I</color> và <color=#3487e0>Yểm Hộ</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Nếu mục tiêu đồng minh rơi vào trạng thái Sụp Đổ Ổn Định sau khi bị tấn công, bản thân nhận <color=#3487e0>Di Chuyển Tăng II</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Hiệu ứng KN chủ động Ánh Sáng Chiến Trường được tăng cường, hồi phục thêm HP cho các mục tiêu đồng minh trong <color=#f26c1c>phạm vi 3 ô xung quanh</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Khi HP của bản thân trên <color=#f26c1c>80%</color>, Tấn Công tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Sau khi trị liệu, giải trừ ngẫu nhiên <color=#f26c1c>1</color> hiệu ứng Debuff trên mục tiêu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Khi dùng kỹ năng trị liệu chủ động lên mục tiêu có HP dưới <color=#f26c1c>50%</color>, hiệu quả trị liệu tăng <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Liệu Pháp Trị Liệu",
                "level": "20",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Sinh Mệnh Nhân Tạo",
                "level": "20",
                "effect": "HP +3.0% / Trước khi dùng kỹ năng hồi máu chủ động đơn mục tiêu, giải trừ <color=#f26c1c>1</color> hiệu ứng Debuff ngẫu nhiên trên mục tiêu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Chuyên Gia Điều Tiết Cảm Xúc",
                "level": "20",
                "effect": "Khi tiến hành Hành Động Chi Viện, đơn vị đồng minh phát động tấn công chuẩn xác được hồi phục HP bằng <color=#f26c1c>50%</color> Tấn Công và <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "groza": {
        "name": "Groza",
        "en_name": "Groza",
        "class": "Tiên Phong",
        "phase": "Vật Lý",
        "rarity": "Standard",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Lời Thề OTs-14",
        "weakness": "Ăn Mòn",
        "server": "global",
        "skills": [
            {
                "name": "Chỉ Lệnh Bắn",
                "en_name": "Fire Command",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Áp Chế Cường Lực",
                "en_name": "Heavy Suppression",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công và áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Yểm Hộ Hoàn Mỹ",
                "en_name": "Perfect Cover",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Áp dụng <color=#f26c1c>2 lớp</color> <color=#3487e0>Yểm Hộ</color> và <color=#3487e0>Phòng Thủ Tăng II</color> cho tất cả đơn vị đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color> trong <color=#f26c1c>2 hiệp</color>. Với mỗi 1 đơn vị đồng minh trong phạm vi, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Số lần Phản Kích trong hiệp này tăng thêm <color=#f26c1c>2 lần</color>."
            },
            {
                "name": "Oanh Tạc Bộc Phá",
                "en_name": "Explosive Bombardment",
                "tags": ["Tuyệt Kỹ", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 ô địa hình <color=#f26c1c>trong phạm vi 7 ô xung quanh</color> bản thân để phát động tấn công, gây ST Vật Lý AoE bằng <color=#f26c1c>90%</color> Tấn Công lên tất cả mục tiêu địch trong phạm vi 3×3 ô và áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Hiệu Chỉnh Tức Thời",
                "en_name": "Timely Maintenance",
                "tags": ["Bị Động", "Cường Hóa", "Phản Kích"],
                "description": "Khi đơn vị đồng minh (ngoại trừ bản thân) kết thúc hành động <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu, đồng thời áp dụng <color=#f26c1c>1 lớp</color> <color=#3487e0>Yểm Hộ</color> lên đơn vị đồng minh đó và bản thân. Với mỗi 1 lớp <color=#3487e0>Yểm Hộ</color>, ST Groza gây ra tăng <color=#f26c1c>5%</color>.\n\nNếu kẻ địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color> gây ST chuẩn xác lên đơn vị đồng minh, Groza tiến hành 1 lần Phản Kích, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>4 điểm</color> ST Ổn Định lên kẻ địch đó. Mỗi hiệp tối đa kích hoạt 1 lần."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Áp Chế Cường Lực",
                "effect": "Nếu kỹ năng này khiến kẻ địch rơi vào trạng thái Sụp Đổ Ổn Định, bản thân nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu và hồi phục <color=#f26c1c>4 điểm</color> Chỉ Số Ổn Định."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Yểm Hộ Hoàn Mỹ",
                "effect": "Hồi phục <color=#f26c1c>5 điểm</color> Chỉ Số Ổn Định."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Oanh Tạc Bộc Phá",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Hiệu Chỉnh Tức Thời",
                "effect": "Khi kết thúc hành động của Groza, áp dụng <color=#3487e0>Tấn Công Giảm I</color> lên kẻ địch có Tấn Công cao nhất <color=#f26c1c>trong phạm vi 7 ô xung quanh</color> bản thân trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Oanh Tạc Bộc Phá",
                "effect": "Thời gian duy trì của <color=#3487e0>Di Chuyển Giảm II</color> tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Hiệu Chỉnh Tức Thời",
                "effect": "Khi có <color=#3487e0>Yểm Hộ</color>, ST Ổn Định phải chịu giảm <color=#f26c1c>1 điểm</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +25\nPhòng Thủ +23", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +84\nHP +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +43\nPhòng Thủ +38", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +52\nPhòng Thủ +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +140\nPhòng Thủ +45", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +61\nPhòng Thủ +53", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Khi bản thân khiến kẻ địch rơi vào trạng thái Sụp Đổ Ổn Định, áp dụng <color=#3487e0>Phòng Thủ Giảm I</color> và <color=#3487e0>Tấn Công Giảm I</color> lên kẻ địch trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Khi dùng Yểm Hộ Hoàn Mỹ, áp dụng thêm <color=#3487e0>Tấn Công Tăng I</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Khi HP của bản thân dưới <color=#f26c1c>30%</color>, lượng trị liệu nhận được tăng <color=#f26c1c>50%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Nếu Áp Chế Cường Lực khiến mục tiêu địch rơi vào trạng thái Sụp Đổ Ổn Định, áp dụng <color=#3487e0>Khiêu Khích</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Khi bản thân có hiệu ứng <color=#3487e0>Yểm Hộ</color>, ST AoE phải chịu giảm <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Khi Groza rơi vào trạng thái Sụp Đổ Ổn Định, hồi phục <color=#f26c1c>20%</color> HP tối đa, <color=#f26c1c>5 điểm</color> Chỉ Số Ổn Định và giải trừ <color=#f26c1c>4</color> hiệu ứng Debuff của bản thân. Mỗi trận chiến chỉ kích hoạt <color=#f26c1c>1 lần</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Trầm Tư Đêm Khuya",
                "level": "20",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Duy Trì Bền Bỉ",
                "level": "20",
                "effect": "HP +3.0% / Khi hiệu ứng Nơi Trú Ẩn có hiệu lực, miễn dịch dịch chuyển vị trí <color=#f26c1c>1 lần</color>. Thời gian hồi: <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Ý Nghĩa Phòng Thủ Tuyệt Đối",
                "level": "20",
                "effect": "Khi dùng kỹ năng chủ động Yểm Hộ Hoàn Mỹ, nhận <color=#3487e0>Phòng Thủ Tuyệt Đối</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "krolik": {
        "name": "Krolik",
        "en_name": "Krolik",
        "class": "Đột Kích",
        "phase": "Thiêu Đốt",
        "rarity": "Standard",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Người Giữ Cửa",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Trảm Nhanh",
                "en_name": "Instantaneous Slash",
                "tags": ["Đánh Thường", "Chỉ Định", "Cận Chiến"],
                "description": "Chọn 1 mục tiêu <color=#f26c1c>trong phạm vi 1 ô xung quanh</color>, gây ST Vật Lý cận chiến bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Vòng Xoáy Nghiền Nát",
                "en_name": "Crushing Revolution",
                "tags": ["Chủ Động", "Phạm Vi", "Cận Chiến"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 1 ô xung quanh</color>, gây ST Vật Lý cận chiến AoE bằng <color=#f26c1c>120%</color> Tấn Công lên mục tiêu và tất cả đơn vị địch trong phạm vi 3×3 ô, đồng thời nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Sau khi tấn công, nếu không có đơn vị đồng minh nào khác <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> bản thân, nhận thêm <color=#f26c1c>5 ô</color> Di Chuyển Bổ Sung."
            },
            {
                "name": "Đòn Trảm Luyện Lửa",
                "en_name": "Quenching Slash",
                "tags": ["Chủ Động", "Chỉ Định", "Cận Chiến", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 1 ô xung quanh</color>, áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>2 hiệp</color>, gây <color=#e67129>ST Thiêu Đốt</color> cận chiến bằng <color=#f26c1c>150%</color> Tấn Công và nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu. Sau khi tấn công, quay trở lại vị trí ban đầu trước khi hành động."
            },
            {
                "name": "Trình Tự Trảm Sát",
                "en_name": "Slaughter Sequence",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Cận Chiến"],
                "description": "Chọn 1 hướng và di chuyển đến ô xa nhất <color=#f26c1c>trong phạm vi 7 ô</color>, gây <color=#e67129>ST Thiêu Đốt</color> cận chiến bằng <color=#f26c1c>130%</color> Tấn Công lên kẻ địch đầu tiên gặp phải. Nếu mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, bỏ qua giảm thương từ Vật Cản của mục tiêu và nhận thêm <color=#f26c1c>5 ô</color> Di Chuyển Bổ Sung."
            },
            {
                "name": "Tàn Tro",
                "en_name": "Embers",
                "tags": ["Bị Động", "Suy Yếu"],
                "description": "Khi tấn công mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, ST gây ra tăng <color=#f26c1c>15%</color>. Khi kết thúc hành động, áp dụng <color=#3487e0>Tràn Lửa</color> lên 2 mục tiêu địch gần nhất <color=#f26c1c>trong phạm vi 5 ô xung quanh</color> trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Vòng Xoáy Nghiền Nát",
                "effect": "Nếu mục tiêu đang trong trạng thái Sụp Đổ Ổn Định, bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Đòn Trảm Luyện Lửa",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Trình Tự Trảm Sát",
                "effect": "Nếu kỹ năng này tiêu diệt mục tiêu, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tàn Tro",
                "effect": "Phạm vi tăng thêm <color=#f26c1c>2 ô</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Trình Tự Trảm Sát",
                "effect": "Nếu mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>100%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Tàn Tro",
                "effect": "Khi tấn công mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, ST Bạo Kích tăng <color=#f26c1c>20%</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +29\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +59\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +49\nPhòng Thủ +31", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +60\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +110\nPhòng Thủ +39", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +69\nPhòng Thủ +45", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Giảm tiêu hao Chỉ Số Nhiên Liệu của kỹ năng Trình Tự Trảm Sát đi <color=#f26c1c>1 điểm</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "KN chủ động Vòng Xoáy Nghiền Nát gây ST tăng <color=#f26c1c>30%</color> khi chỉ đánh trúng 1 mục tiêu đơn lẻ.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Nếu không có đơn vị đồng minh nào khác <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> bản thân, ST gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Khi KN chủ động Đòn Trảm Luyện Lửa tiêu diệt mục tiêu địch, thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Khi bắt đầu hành động, nếu trên sân có đơn vị địch chịu <color=#3487e0>Tràn Lửa</color>, nhận <color=#3487e0>Thế Công Rực Lửa II</color> trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Trước khi tấn công, nếu bản thân di chuyển từ <color=#f26c1c>3 ô trở lên</color>, Tỷ Lệ Bạo Kích của bản thân tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Bảo Hộ Thiêu Đốt",
                "level": "20",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Nghệ Thuật Bạo Lực",
                "level": "20",
                "effect": "TL Bạo Kích +3.0% / Nếu có hiệu ứng Buff loại Thiêu Đốt, nhận miễn dịch <color=#3487e0>Ngưng Tụ</color> và <color=#3487e0>Rét Buốt</color>, đồng thời ST gây ra tăng <color=#f26c1c>5%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Thỏ Không Kích",
                "level": "20",
                "effect": "Trước khi tấn công, cứ mỗi 1 ô di chuyển, Tỷ Lệ Bạo Kích và ST Bạo Kích của đòn tấn công này tăng <color=#f26c1c>5%</color>, tối đa tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "ksenia": {
        "name": "Ksenia",
        "en_name": "Ksenia",
        "class": "Hỗ Trợ",
        "phase": "Thiêu Đốt",
        "rarity": "Standard",
        "weapon_type": "Súng Ngắn",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Rao Bán",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Ưu Đãi Giảm Giá",
                "en_name": "Special Discount",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Vòng Lặp Có Lợi",
                "en_name": "Favorable Cycle",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>75%</color> Tấn Công, áp dụng <color=#f26c1c>2 lớp</color> <color=#3487e0>Dễ Cháy</color> và <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>1 hiệp</color>. Nếu bản thân có từ 2 hiệu ứng Buff loại Thiêu Đốt trở lên, tiến hành thêm 1 lần tấn công lên mục tiêu ban đầu, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>75%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định."
            },
            {
                "name": "Cứu Viện Toàn Diện",
                "en_name": "Comprehensive Rescue",
                "tags": ["Chủ Động", "Trị Liệu", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, hồi phục HP bằng <color=#f26c1c>130%</color> Tấn Công, <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định và áp dụng <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>. Nếu HP của mục tiêu được hồi phục đầy sau trị liệu, áp dụng <color=#3487e0>Thế Công Rực Lửa II</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Bí Mật Kiếm Tiền",
                "en_name": "The Secret of Making Money",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Cường Hóa"],
                "description": "Bản thân nhận <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color> và <color=#3487e0>Thế Công Rực Lửa II</color> trong <color=#f26c1c>2 hiệp</color>. Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>160%</color> Tấn Công."
            },
            {
                "name": "Đam Mê Mua Sắm",
                "en_name": "Passion for Shopping",
                "tags": ["Bị Động", "Hỗ Trợ", "Cường Hóa"],
                "description": "Khi đơn vị địch trong tầm bắn chịu ST chuẩn xác từ đơn vị đồng minh, ưu tiên tiến hành 1 lần Hành Động Chi Viện, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn Định lên đơn vị địch, đồng thời áp dụng <color=#3487e0>Thế Công Rực Lửa II</color> cho đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>. Mỗi hiệp tối đa kích hoạt 1 lần.\n\nKhi có hiệu ứng <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>, ST Ổn Định gây ra tăng thêm <color=#f26c1c>1 điểm</color>. Khi kết thúc hành động, với mỗi một hiệu ứng Buff loại Thiêu Đốt, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Vòng Lặp Có Lợi",
                "effect": "Sau đòn tấn công đầu tiên, áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Đam Mê Mua Sắm",
                "effect": "Khi có hiệu ứng <color=#3487e0>Thế Công Rực Lửa I</color>, ST Ổn Định gây ra tăng thêm <color=#f26c1c>1 điểm</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Bí Mật Kiếm Tiền",
                "effect": "Nếu khai thác Điểm Yếu Thuộc Tính, ST gây ra tăng <color=#f26c1c>20%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Đam Mê Mua Sắm",
                "effect": "Số lần kích hoạt tối đa của Hành Động Chi Viện tăng thêm <color=#f26c1c>1 lần</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Cứu Viện Toàn Diện",
                "effect": "Nếu HP của mục tiêu được hồi phục đầy sau trị liệu và chưa đầy trước đó, hồi phục thêm <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho mục tiêu."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Bí Mật Kiếm Tiền",
                "effect": "Khi tấn công mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>100%</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +25\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +78\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +43\nPhòng Thủ +32", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +53\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +131\nPhòng Thủ +40", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +61\nPhòng Thủ +46", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Khi trị liệu cho đơn vị đồng minh ngoài bản thân, áp dụng ngẫu nhiên <color=#f26c1c>1</color> hiệu ứng Buff lên mục tiêu và bản thân.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Khi dùng Vòng Lặp Có Lợi, với mỗi lần tiêu diệt được mục tiêu, số lần sử dụng tối đa của Hành Động Chi Viện trong hiệp này tăng thêm <color=#f26c1c>1 lần</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Sau khi gây ST Thiêu Đốt, hồi phục HP bằng <color=#f26c1c>10%</color> ST gây ra và <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Khi dùng Cứu Viện Toàn Diện, bản thân cũng nhận các hiệu ứng Buff tương tự.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Khi áp dụng một hiệu ứng Buff loại Thiêu Đốt, giải trừ thêm <color=#f26c1c>1</color> hiệu ứng Debuff.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Nếu bản thân sở hữu <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color> khi kết thúc hành động, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Kiếm Tiền",
                "level": "20",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Bừng Bừng Rực Cháy",
                "level": "20",
                "effect": "HP +3.0% / Khi áp dụng một hiệu ứng Buff loại Thiêu Đốt, có <color=#f26c1c>50%</color> xác suất áp dụng thêm <color=#f26c1c>1</color> hiệu ứng Buff cho mục tiêu trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "20",
                "effect": "Khi kết thúc hành động, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho đồng minh có Chỉ Số Ổn Định thấp nhất.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "littara": {
        "name": "Littara",
        "en_name": "Littara",
        "class": "Hỏa Lực",
        "phase": "Vật Lý",
        "rarity": "Standard",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Nhân Chứng",
        "weakness": "Thiêu Đốt",
        "server": "global",
        "skills": [
            {
                "name": "Ghi Nhanh",
                "en_name": "Quick Writing",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Thời Cơ Hoàn Hảo",
                "en_name": "Perfect Opportunity",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color> để tấn công, gây ST Vật Lý AoE bằng <color=#f26c1c>70%</color> Tấn Công lên mục tiêu đó và tất cả kẻ địch <color=#f26c1c>trong phạm vi 2 ô xung quanh</color>, đồng thời áp dụng <color=#3487e0>Dễ Bị Thương I</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Yểm Hộ Đáng Tin",
                "en_name": "Reliable Cover",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu", "Phá Hủy Vật Cản"],
                "description": "Chọn 1 hướng xung quanh bản thân, gây ST Vật Lý AoE bằng <color=#f26c1c>65%</color> Tấn Công lên tất cả mục tiêu địch trong phạm vi 3×8 ô cách bản thân 2 ô theo hướng đã chọn và áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> trong <color=#f26c1c>2 hiệp</color>. Phá hủy mọi Vật Cản có thể phá hủy trong khu vực đó (ngoại trừ phạm vi 3×3 ô quanh bản thân). Với mỗi mục tiêu trúng đòn, giảm thời gian hồi chiêu của kỹ năng này đi <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Kế Hoạch Quân Sư",
                "en_name": "Strategist's Plan",
                "tags": ["Tuyệt Kỹ", "Phạm Vi"],
                "description": "Chọn 1 ô địa hình <color=#f26c1c>trong phạm vi 8 ô xung quanh</color> để phát động tấn công, gây ST Vật Lý AoE bằng <color=#f26c1c>85%</color> Tấn Công lên tất cả mục tiêu địch trong phạm vi 2 ô. Nếu mục tiêu có Debuff loại phòng thủ, đổi ST gây ra thành ST Vật Lý AoE bằng <color=#f26c1c>95%</color> Tấn Công và <color=#f26c1c>4 điểm</color> ST Ổn Định. Đồng thời, ST gây ra cho mục tiêu có Debuff loại phòng thủ tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "name": "Đánh Bại Từng Tên",
                "en_name": "Systematic Breakdown",
                "tags": ["Bị Động", "Phạm Vi"],
                "description": "Khi kết thúc hành động, gây ST Vật Lý AoE bằng <color=#f26c1c>30%</color> Tấn Công và <color=#f26c1c>1 điểm</color> ST Ổn Định lên mục tiêu gần nhất trong tầm bắn có Debuff loại phòng thủ, đồng thời nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Thời Cơ Hoàn Hảo",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Yểm Hộ Đáng Tin",
                "effect": "Phạm vi hiệu lực tăng thành <color=#f26c1c>3×8 ô</color> phía trước."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Đánh Bại Từng Tên",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Kế Hoạch Quân Sư",
                "effect": "ST gây ra cho mục tiêu có Debuff loại phòng thủ tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Kế Hoạch Quân Sư",
                "effect": "Tiêu hao Chỉ Số Nhiên Liệu giảm <color=#f26c1c>2 điểm</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Đánh Bại Từng Tên",
                "effect": "Gây ST lên <color=#f26c1c>2</color> mục tiêu địch gần nhất trong phạm vi có Debuff loại phòng thủ."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +31\nPhòng Thủ +20", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +70\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +53\nPhòng Thủ +33", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +65\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +119\nPhòng Thủ +40", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +76\nPhòng Thủ +48", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Cứ gây ST <color=#f26c1c>3 lần</color>, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Khi khai thác Điểm Yếu Thuộc Tính, sau khi tấn công áp dụng ngẫu nhiên <color=#f26c1c>1</color> hiệu ứng Debuff lên mục tiêu trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Nếu mục tiêu có Debuff loại phòng thủ, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>15%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Khi dùng KN chủ động Thời Cơ Hoàn Hảo, áp dụng <color=#3487e0>Tấn Công Giảm I</color> lên tất cả mục tiêu trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Trước khi dùng KN chủ động Yểm Hộ Đáng Tin, nếu bản thân chưa di chuyển, đổi loại sát thương gây ra thành <color=#e67129>ST Thiêu Đốt</color> AoE.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Ghi Chép Vụn Vặt",
                "level": "20",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Đánh Phá Nhược Điểm",
                "level": "20",
                "effect": "TL Bạo Kích +3.0% / ST gây ra cho mục tiêu có Debuff loại phòng thủ tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "20",
                "effect": "Nếu mục tiêu có Debuff loại Phòng Thủ, ST gây ra tăng <color=#f26c1c>10%</color> và bỏ qua <color=#f26c1c>15%</color> giảm thương từ Vật Cản.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "lotta": {
        "name": "Lotta",
        "en_name": "Lotta",
        "class": "Hỏa Lực",
        "phase": "Băng Kết",
        "rarity": "Standard",
        "weapon_type": "Súng Săn",
        "ammo_type": "Đạn Săn",
        "signature_weapon": "Giọt Nước Mắt Băng",
        "weakness": "Thiêu Đốt",
        "server": "global",
        "skills": [
            {
                "name": "Bộc Bạch Tiếng Lòng",
                "en_name": "Heartfelt Confession",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Đạn Băng Giá",
                "en_name": "Cryo Rounds",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu", "Phá Hủy Vật Cản"],
                "description": "Chọn 1 hướng xung quanh bản thân, gây <color=#42cce0>ST Băng Kết</color> AoE bằng <color=#f26c1c>60%</color> Tấn Công lên tất cả mục tiêu địch trong phạm vi 3×5 ô theo hướng đã chọn. Đồng thời phá hủy mọi Vật Cản có thể phá hủy ngoài phạm vi 3×3 ô quanh bản thân. Áp dụng <color=#3487e0>Rét Buốt</color> lên các mục tiêu trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Điều Chỉnh Tâm Trí",
                "en_name": "Neural Adjustment",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Nạp đầy Chỉ Số Nhiên Liệu và nhận <color=#3487e0>Tấn Công Tăng I</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Dũng Khí Tràn Đầy",
                "en_name": "Amplified Courage",
                "tags": ["Tuyệt Kỹ", "Phạm Vi"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color> để phát động tấn công, gây <color=#42cce0>ST Băng Kết</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công bỏ qua giảm thương từ Vật Cản lên mục tiêu đó và tất cả kẻ địch trong phạm vi 3 ô. Nếu đánh trúng từ 2 mục tiêu trở lên, nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "name": "Kết Nối Tình Bạn",
                "en_name": "Bonds of Friendship",
                "tags": ["Bị Động", "Hỗ Trợ"],
                "description": "Khi một mục tiêu địch trong phạm vi chịu trạng thái <color=#3487e0>Rét Buốt</color>, tiến hành 1 lần Chi Viện Thông Minh, gây ST Vật Lý AoE bằng <color=#f26c1c>50%</color> Tấn Công và <color=#f26c1c>1 điểm</color> ST Ổn Định lên mục tiêu đó. Mỗi hiệp tối đa kích hoạt 2 lần."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Dũng Khí Tràn Đầy",
                "effect": "Nếu khai thác Điểm Yếu Thuộc Tính, áp dụng <color=#3487e0>Rét Buốt</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Kết Nối Tình Bạn",
                "effect": "Tầm Di Chuyển của bản thân tăng thêm <color=#f26c1c>1 ô</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Dũng Khí Tràn Đầy",
                "effect": "Đổi \"Chọn 1 mục tiêu địch\" thành \"Chọn 1 ô địa hình\"."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Kết Nối Tình Bạn",
                "effect": "ST Ổn Định do Chi Viện Thông Minh gây ra tăng thêm <color=#f26c1c>1 điểm</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Đạn Băng Giá",
                "effect": "Thời gian duy trì của <color=#3487e0>Rét Buốt</color> tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Điều Chỉnh Tâm Trí",
                "effect": "Thay thế <color=#3487e0>Tấn Công Tăng I</color> bằng <color=#3487e0>Tấn Công Tăng II</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +32\nPhòng Thủ +21", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +67\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +55\nPhòng Thủ +35", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +67\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +115\nPhòng Thủ +43", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +78\nPhòng Thủ +50", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "ST gây ra cho mục tiêu địch có Debuff loại Băng Kết tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Nếu gây ST Băng Kết, áp dụng <color=#3487e0>Ngưng Tụ</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Khi HP lớn hơn <color=#f26c1c>50%</color>, ST AoE phải chịu giảm <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "KN chủ động Đạn Băng Giá nhận thêm hiệu ứng: Đẩy lùi mục tiêu <color=#f26c1c>3 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "KN chủ động Điều Chỉnh Tâm Trí nhận thêm hiệu ứng: Nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Lá Chắn Tốc Độ</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Mầm Non Mới Nhú",
                "level": "20",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Bẫy Săn Bắn",
                "level": "20",
                "effect": "Tấn Công +3.0% / ST gây ra với mục tiêu địch có Debuff loại di chuyển tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "20",
                "effect": "Trước khi tấn công, nếu Chỉ Số Ổn Định của mục tiêu lớn hơn <color=#f26c1c>0</color>, ST gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "nagant": {
        "name": "Nagant",
        "en_name": "Nagant",
        "class": "Phòng Ngự",
        "phase": "Ăn Mòn",
        "rarity": "Standard",
        "weapon_type": "Súng Ngắn",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Lời Thề Khắc Kỷ",
        "weakness": "Điện Từ",
        "server": "global",
        "skills": [
            {
                "name": "Bắn Thần Tốc",
                "en_name": "Point Shooting",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Lời Khuyên Tiền Bối",
                "en_name": "Senior's Admonishment",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Sau khi kích hoạt nếu mục tiêu đang chịu trạng thái Sụp Đổ Ổn Định, áp dụng <color=#3487e0>Ăn Mòn Mạnh II</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Bạn Của Chính Nghĩa",
                "en_name": "Friend of Justice",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>70%</color> Tấn Công. Nếu không có kẻ địch nào trong phạm vi 4 ô, tiến hành thêm 1 đòn tấn công lên mục tiêu ban đầu và áp dụng <color=#3487e0>Ăn Mòn Mạnh II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Tuyên Cáo Trừng Phạt",
                "en_name": "Sanction Declaration",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng <color=#f26c1c>150%</color> Tấn Công. Nếu mục tiêu có Debuff loại phòng thủ, áp dụng <color=#3487e0>Dễ Bị Thương I</color> trước khi tấn công trong <color=#f26c1c>2 hiệp</color>. ST Ổn Định do đòn đánh này gây ra tăng thêm <color=#f26c1c>2 điểm</color>."
            },
            {
                "name": "Kinh Nghiệm Cựu Binh",
                "en_name": "Veteran's Skills",
                "tags": ["Bị Động", "Suy Yếu", "Khống Chế"],
                "description": "Với mỗi lần gây ST, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Nếu một đơn vị địch di chuyển trong phạm vi của Nagant, cô gây ST Vật Lý bằng <color=#f26c1c>50%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định. Nếu mục tiêu có Debuff loại phòng thủ, áp dụng <color=#3487e0>Choáng</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>. Hiệu ứng này mỗi hiệp chỉ có thể kích hoạt 1 lần."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Bạn Của Chính Nghĩa",
                "effect": "Nếu mục tiêu có Debuff loại phòng thủ, thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tuyên Cáo Trừng Phạt",
                "effect": "Nếu mục tiêu có Debuff loại phòng thủ, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>20%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Bạn Của Chính Nghĩa",
                "effect": "Nếu không có kẻ địch nào trong phạm vi <color=#f26c1c>3 ô xung quanh</color> bản thân, tiến hành thêm 1 lần tấn công lên mục tiêu ban đầu."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tuyên Cáo Trừng Phạt",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Kinh Nghiệm Cựu Binh",
                "effect": "Hệ số ST tăng thêm <color=#f26c1c>30%</color> và gây thêm <color=#f26c1c>3 điểm</color> ST Ổn Định."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Kinh Nghiệm Cựu Binh",
                "effect": "Số lần kích hoạt mỗi hiệp tăng thêm <color=#f26c1c>1 lần</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +28\nPhòng Thủ +22", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +70\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +47\nPhòng Thủ +37", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +57\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +126\nPhòng Thủ +45", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +66\nPhòng Thủ +52", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Nếu tấn công mục tiêu địch có Debuff loại phòng thủ, giảm thời gian hồi chiêu của tất cả KN chủ động đi <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Nếu bị tấn công bởi mục tiêu địch có hiệu ứng Debuff, ST phải chịu giảm <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Khi dùng Bạn Của Chính Nghĩa, nếu đánh trúng 2 lần, đòn đánh đầu tiên gây ST Vật Lý bằng <color=#f26c1c>10%</color> Tấn Công, và đòn thứ hai gây ST bằng <color=#f26c1c>130%</color> Tấn Công.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Nếu mục tiêu có Debuff loại phòng thủ, Tỷ Lệ Bạo Kích và ST Bạo Kích tăng <color=#f26c1c>10%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Khi dùng KN chủ động Lời Khuyên Tiền Bối, nếu gây ra Sụp Đổ Ổn Định lên mục tiêu địch, gây thêm ST cố định bằng <color=#f26c1c>50%</color> Tấn Công.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Mẹo Đội Mũ",
                "level": "20",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Răn Dạy Thường Ngày",
                "level": "20",
                "effect": "Tấn Công +3.0% / Nếu Chỉ Số Ổn Định của mục tiêu thấp hơn bản thân, ST gây ra cho mục tiêu tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Chỉ Dẫn Của Tiền Bối",
                "level": "20",
                "effect": "Sau khi dùng tấn công chủ động, áp dụng <color=#3487e0>Choáng</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>. Trong trận đấu hiện tại, nếu áp dụng Choáng lên cùng 1 mục tiêu nhiều lần, thời gian duy trì Choáng đổi thành <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "nemesis": {
        "name": "Nemesis",
        "en_name": "Nemesis",
        "class": "Hỏa Lực",
        "phase": "Ăn Mòn",
        "rarity": "Standard",
        "weapon_type": "Súng Bắn Tỉa",
        "ammo_type": "Đạn Nặng",
        "signature_weapon": "Mũi Tên Dẫn Đường",
        "weakness": "Vật Lý",
        "server": "global",
        "skills": [
            {
                "name": "Điềm Báo Chiến Thắng",
                "en_name": "Victory Portent",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Sao Mai",
                "en_name": "Enlightened Star",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Khi tấn công ở gần Vật Cản, ST gây ra tăng <color=#f26c1c>20%</color> và nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Hộp Xuyên Thấu",
                "en_name": "Penetrating Casket",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> trong <color=#f26c1c>1 hiệp</color> và gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công."
            },
            {
                "name": "Truy Kích Tinh Tú",
                "en_name": "Constellation Pursuit",
                "tags": ["Tuyệt Kỹ", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng <color=#f26c1c>170%</color> Tấn Công. Cứ mỗi 1 điểm Chỉ Số Nhiên Liệu tăng thêm, ST đòn đánh này tăng <color=#f26c1c>10%</color>."
            },
            {
                "name": "Quan Sát Từ Xa",
                "en_name": "Remote Observation",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Khi bắt đầu hành động, đánh dấu <color=#3487e0>Lời Tiên Tri Tang Tóc</color> lên 2 mục tiêu địch gần nhất trong phạm vi trong <color=#f26c1c>1 hiệp</color>. Hành Động Chi Viện gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định. Bản thân nhận <color=#3487e0>Nhìn Thấu</color> trong <color=#f26c1c>1 hiệp</color> sau khi dùng Hành Động Chi Viện."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Quan Sát Từ Xa",
                "effect": "Thời gian duy trì của <color=#3487e0>Lời Tiên Tri Tang Tóc</color> tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Sao Mai",
                "effect": "Nếu mục tiêu có <color=#3487e0>Lời Tiên Tri Tang Tóc</color>, ST gây ra tăng <color=#f26c1c>10%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Hộp Xuyên Thấu",
                "effect": "Nếu mục tiêu có Debuff loại phòng thủ, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Quan Sát Từ Xa",
                "effect": "Khi bản thân có hiệu ứng <color=#3487e0>Nhìn Thấu</color>, ST gây ra tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Truy Kích Tinh Tú",
                "effect": "Khi hiệu ứng Nhìn Thấu có hiệu lực, hệ số ST tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Truy Kích Tinh Tú",
                "effect": "Với mỗi 1 Debuff trên người mục tiêu, Tỷ Lệ Bạo Kích tăng <color=#f26c1c>20%</color>, tối đa tăng <color=#f26c1c>100%</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +33\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +70\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +56\nPhòng Thủ +32", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +69\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +118\nPhòng Thủ +39", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +80\nPhòng Thủ +46", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Nếu mục tiêu địch bị đánh dấu <color=#3487e0>Lời Tiên Tri Tang Tóc</color>, trước khi phát động tấn công chủ động, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên mục tiêu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Khi bản thân có hiệu ứng <color=#3487e0>Nhìn Thấu</color>, tầm thi triển của KN chủ động Sao Mai và Hộp Xuyên Thấu tăng thêm <color=#f26c1c>1 ô</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Nếu ở gần Vật Cản trong khi có hiệu ứng <color=#3487e0>Nhìn Thấu</color>, ST AoE phải chịu giảm <color=#f26c1c>20%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Khi tiêu diệt mục tiêu bị đánh dấu <color=#3487e0>Lời Tiên Tri Tang Tóc</color>, nhận <color=#3487e0>Tấn Công Tăng I</color> và <color=#3487e0>ST tăng I</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Khi mục tiêu bị đánh dấu <color=#3487e0>Lời Tiên Tri Tang Tóc</color> bị bản thân tiêu diệt, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Khi bản thân có hiệu ứng <color=#3487e0>Nhìn Thấu</color>, nhận miễn dịch với mọi hiệu ứng di chuyển vị trí từ đơn vị địch.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Lời Thì Thầm Êm Dịu",
                "level": "20",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Chúc Phúc Sao Mai",
                "level": "20",
                "effect": "Tấn Công +3.0% / Khi bản thân có hiệu ứng Nhìn Thấu, nhận thêm <color=#f26c1c>3 ô</color> Di Chuyển Bổ Sung sau khi tiêu diệt mục tiêu địch.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng-Tiên Tri Tưởng Niệm",
                "level": "20",
                "effect": "Khi bắt đầu hiệp, áp dụng <color=#3487e0>Lời Tiên Tri Tang Tóc</color> lên kẻ địch có HP cao nhất trong Tầm Bắn.",
                "materials": "1\n\n\n3000"
            }
        ]
    },
    "sharkry": {
        "name": "Sharkry",
        "en_name": "Sharkry",
        "class": "Hỏa Lực",
        "phase": "Thiêu Đốt",
        "rarity": "Standard",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Mối Tình Nồng Cháy",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Bắn Tim",
                "en_name": "Love Shot",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Sóng Âm Rực Cháy",
                "en_name": "Boiling Soundwaves",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>1 hiệp</color> và gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>140%</color> Tấn Công. Nếu bản thân có hiệu ứng <color=#3487e0>Khóa Mục Tiêu</color>, ST Ổn Định gây ra tăng thêm <color=#f26c1c>1 điểm</color>."
            },
            {
                "name": "Lên Tông Hoàn Mỹ",
                "en_name": "Perfect Rising Tone",
                "tags": ["Chủ Động", "Chỉ Định", "Cường Hóa", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>150%</color> Tấn Công và nhận <color=#3487e0>Khóa Mục Tiêu</color>. Nếu mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, áp dụng <color=#f26c1c>2 lớp</color> <color=#3487e0>Dễ Cháy</color> trước khi tấn công và đổi loại sát thương thành <color=#e67129>ST Thiêu Đốt</color>."
            },
            {
                "name": "Thời Khắc Tỏa Sáng",
                "en_name": "Highlight Moment",
                "tags": ["Tuyệt Kỹ", "Cường Hóa"],
                "description": "Nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Khóa Mục Tiêu</color> và <color=#f26c1c>1 lần</color> <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "name": "Chỉnh Trang Diện Mạo",
                "en_name": "Makeup Organization",
                "tags": ["Bị Động"],
                "description": "Khi bắt đầu hành động, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Khi mục tiêu địch bị áp dụng <color=#3487e0>Tràn Lửa</color>, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Tỷ Lệ Bạo Kích tăng <color=#f26c1c>20%</color> khi tấn công mục tiêu chịu <color=#3487e0>Tràn Lửa</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Sóng Âm Rực Cháy",
                "effect": "Thời gian duy trì của <color=#3487e0>Tràn Lửa</color> tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Thời Khắc Tỏa Sáng",
                "effect": "Bản thân nhận <color=#3487e0>ST tăng I</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Lên Tông Hoàn Mỹ",
                "effect": "Nếu tiêu diệt được mục tiêu, nhận thêm <color=#f26c1c>1 lớp</color> <color=#3487e0>Khóa Mục Tiêu</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Chỉnh Trang Diện Mạo",
                "effect": "Tỷ Lệ Bạo Kích tăng thêm <color=#f26c1c>10%</color> khi tấn công mục tiêu chịu <color=#3487e0>Tràn Lửa</color>. Với mỗi 1 hiệu ứng Buff đang kích hoạt, ST Bạo Kích tăng <color=#f26c1c>3%</color>, tối đa tăng <color=#f26c1c>15%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Thời Khắc Tỏa Sáng",
                "effect": "Hiệu ứng của <color=#3487e0>Khóa Mục Tiêu</color> được tăng cường, ST gây ra tăng thêm <color=#f26c1c>5%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Chỉnh Trang Diện Mạo",
                "effect": "Khi bắt đầu hành động, nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Khóa Mục Tiêu</color>."
            }
        ],
        "neural_helix": [
            {"node": "Cường Hóa 1", "level": 1, "effect": "Tấn Công +32\nPhòng Thủ +19", "materials": "20\n\n\n1000"},
            {"node": "Cường Hóa 2", "level": 20, "effect": "HP +72\nTấn Công +5.0%", "materials": "20\n\n\n2000"},
            {"node": "Cường Hóa 3", "level": 30, "effect": "Tấn Công +54\nPhòng Thủ +32", "materials": "20\n\n\n3000"},
            {"node": "Cường Hóa 4", "level": 40, "effect": "Tấn Công +66\nHP +5.0%", "materials": "20\n\n\n4000"},
            {"node": "Cường Hóa 5", "level": 50, "effect": "HP +122\nPhòng Thủ +39", "materials": "20\n\n\n5000"},
            {"node": "Cường Hóa 6", "level": 60, "effect": "Tấn Công +78\nPhòng Thủ +46", "materials": "20\n\n\n6000"}
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1",
                "level": "20",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2",
                "level": "20",
                "effect": "Khi một mục tiêu địch trong tầm bắn chịu trạng thái <color=#3487e0>Tràn Lửa</color>, tiến hành <color=#f26c1c>1 lần</color> Chi Viện Thông Minh, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định lên mục tiêu đó. Mỗi hiệp tối đa kích hoạt <color=#f26c1c>3 lần</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3",
                "level": "20",
                "effect": "Khi bắt đầu hành động, nếu trên sân có kẻ địch chịu <color=#3487e0>Tràn Lửa</color>, nhận <color=#3487e0>Thế Công Rực Lửa II</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 4",
                "level": "20",
                "effect": "Khi dùng KN chủ động Lên Tông Hoàn Mỹ, nếu mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, nhận <color=#3487e0>Thế Công Rực Lửa II</color> trước khi tấn công trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 5",
                "level": "20",
                "effect": "Khi dùng KN chủ động Sóng Âm Rực Cháy, nếu tiêu diệt được mục tiêu, nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Khóa Mục Tiêu</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 6",
                "level": "20",
                "effect": "Khi tấn công mục tiêu chịu <color=#3487e0>Tràn Lửa</color>, hồi phục <color=#f26c1c>20%</color> HP tối đa.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Tương Thích-Quyết Tâm Của Thần Tượng",
                "level": "20",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Chung-Pháo Hoa Khởi Động",
                "level": "20",
                "effect": "TL Bạo Kích +3.0% / Nếu bản thân có từ <color=#f26c1c>1 hiệu ứng Buff trở lên</color>, ST gây ra tăng <color=#f26c1c>7%</color>.",
                "materials": "1\n\n\n3000"
            },
            {
                "name": "Khóa Mở Rộng",
                "level": "20",
                "effect": "ST do Chi Viện Thông Minh gây ra đổi thành <color=#e67129>ST Thiêu Đốt</color>.",
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
    
    for slug, new_data in BATCH_1_DATA.items():
        print(f"Updating {slug} in i18n_vi...")
        chars[slug] = new_data

    # Stage using atomic transaction
    tx = RepositoryTransaction(ROOT)
    stage_i18n_bundle(ROOT, tx, bundle)
    tx.commit()
    print("Successfully committed Batch 1 changes to data/i18n_vi.json and site/static/js/i18n-vi.js.")

if __name__ == "__main__":
    main()
