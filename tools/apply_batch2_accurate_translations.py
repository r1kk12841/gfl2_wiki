#!/usr/bin/env python3
"""
tools/apply_batch2_accurate_translations.py
Applies 100% faithful, accurate Vietnamese translations for Batch 2 (13 dolls):
  suomi, tololo, sabrina, qiongjiu, daiyan, klukai, centaureissi,
  balthilde, basti, belka, cheyanne, dushevnaya, faye.
(andoris, alva, voymastina are strictly preserved).
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
        "class": "Hỗ Trợ",
        "phase": "Băng Kết",
        "rarity": "Elite",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Lời Gọi Thầm Kín",
        "weakness": "Ăn Mòn",
        "server": "global",
        "skills": [
            {
                "name": "Bông Tuyết Rơi",
                "en_name": "Pelting Snowflake",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Cơn Thịnh Nộ Mùa Đông",
                "en_name": "Winter's Wrath",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây <color=#42cce0>ST Băng Kết</color> bằng <color=#f26c1c>100%</color> Tấn Công lên mục tiêu đó. Tỷ lệ bạo kích của kỹ năng này giảm <color=#f26c1c>100%</color>, nhưng gây thêm ST cố định bằng <color=#f26c1c>50%</color> Phòng Thủ. Với mỗi đơn vị đồng minh <color=#f26c1c>trong phạm vi 6 ô</color>, ST Ổn Định gây ra tăng thêm <color=#f26c1c>1 điểm</color>."
            },
            {
                "name": "Ân Huệ Của Tuyết",
                "en_name": "Snow's Grace",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu đồng minh (ngoại trừ bản thân) <color=#f26c1c>trong phạm vi 6 ô</color>, áp dụng <color=#3487e0>Lá Chắn Hàn Sương</color> trong <color=#f26c1c>2 hiệp</color>. Lượng sát thương hấp thụ của Lá Chắn Hàn Sương bằng <color=#f26c1c>130%</color> Tấn Công ban đầu của Suomi, tối đa không quá <color=#f26c1c>100%</color> HP tối đa của mục tiêu. Hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định. Với mỗi đơn vị địch <color=#f26c1c>trong phạm vi 5 ô</color> quanh mục tiêu được chọn, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Hỗ Trợ Phòng Thủ</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Ánh Sáng Tuyết Nguyên",
                "en_name": "Snowfield's Radiance",
                "tags": ["Tuyệt Kỹ", "Ô Địa Hình"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST cố định bằng <color=#f26c1c>50%</color> Phòng Thủ lên tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 3 ô</color>, đồng thời áp dụng <color=#f26c1c>2 tầng</color> <color=#3487e0>Tuyết Lở</color>.\n\nHồi phục <color=#f26c1c>2 điểm</color> Độ Ổn Định, giải trừ <color=#f26c1c>1</color> Debuff, và giải trừ hiệu ứng <color=#3487e0>Khiêu Khích</color> cho tất cả đơn vị đồng minh. Đồng thời áp dụng <color=#3487e0>Lá Chắn Hàn Sương</color> và <color=#f26c1c>1 tầng</color> <color=#3487e0>Pháo Đài Băng Tuyết</color> trong <color=#f26c1c>3 hiệp</color>. Lá Chắn Hàn Sương hấp thụ sát thương bằng <color=#f26c1c>100%</color> Tấn Công ban đầu của Suomi, tối đa không quá <color=#f26c1c>100%</color> HP tối đa của mục tiêu.\n\nSau khi sử dụng kỹ năng này, tạo ra các ô địa hình <color=#3487e0>Băng Giá</color> hình bông tuyết trong bán kính <color=#f26c1c>3 ô</color> xung quanh ô được chọn trong <color=#f26c1c>3 hiệp</color>."
            },
            {
                "name": "Nguồn Ấm Áp",
                "en_name": "Source of Warmth",
                "tags": ["Bị Động", "Trị Liệu", "Hỗ Trợ"],
                "description": "Khi kết thúc hành động, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu, hồi phục HP bằng <color=#f26c1c>5%</color> HP tối đa của Suomi cho các đơn vị đồng minh khác <color=#f26c1c>trong phạm vi 6 ô</color>. Nếu HP của mục tiêu dưới <color=#f26c1c>50%</color>, lượng hồi phục tăng lên thành <color=#f26c1c>10%</color>.\n\nKhi đơn vị đồng minh (ngoại trừ Suomi) dùng Đánh Thường hoặc kỹ năng, Suomi áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Tuyết Lở</color> lên 1 mục tiêu địch ngẫu nhiên <color=#f26c1c>trong phạm vi 6 ô</color> quanh bản thân.\n\nKhi đơn vị địch trong tầm bắn chịu sát thương chuẩn xác từ đồng minh, ưu tiên dùng Hành Động Chi Viện 1 lần, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn Định. Áp dụng <color=#3487e0>ST Bạo Kích Tăng I</color> cho đơn vị đồng minh đó trong <color=#f26c1c>2 hiệp</color>. Hiệu ứng này có thể kích hoạt 2 lần mỗi hiệp. Khi HP trên <color=#f26c1c>80%</color>, nhận <color=#3487e0>Phi Tuyết Tật Bộ</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ánh Sáng Tuyết Nguyên",
                "effect": "Số tầng <color=#3487e0>Tuyết Lở</color> tăng thêm <color=#f26c1c>1 tầng</color>.\n\nHồi phục HP bằng <color=#f26c1c>30%</color> HP tối đa của Suomi và hồi <color=#f26c1c>4 điểm</color> Chỉ Số Ổn Định cho tất cả đơn vị đồng minh. Tất cả đơn vị đồng minh (ngoại trừ bản thân) nhận thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Pháo Đài Băng Tuyết</color>.\n\nNếu đơn vị đồng minh đang đầy HP trước khi được trị liệu, họ nhận thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Yểm Hộ</color> và <color=#3487e0>Duy Trì Chữa Lành I</color> trong <color=#f26c1c>3 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Nguồn Ấm Áp",
                "effect": "Nếu đơn vị đồng minh có <color=#3487e0>Lá Chắn Hàn Sương</color>, áp dụng <color=#3487e0>Ánh Sáng Bảo Vệ</color> cho họ.\n\nCường hóa hiệu ứng Phi Tuyết Tật Bộ, phạm vi chi viện tăng thêm <color=#f26c1c>2 ô</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Ân Huệ Của Tuyết",
                "effect": "Áp dụng <color=#3487e0>Phản Ứng Va Chạm I</color> cho mục tiêu trong <color=#f26c1c>2 hiệp</color>. Với mỗi đơn vị địch cỡ lớn xung quanh, áp dụng thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Hỗ Trợ Phòng Thủ</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Cơn Thịnh Nộ Mùa Đông",
                "effect": "Nếu đòn đánh gây Sụp Đổ Ổn Định, tăng ST cố định lên thành <color=#f26c1c>125%</color> Phòng Thủ."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Nguồn Ấm Áp",
                "effect": "Bổ sung thêm hiệu ứng cho Ánh Sáng Bảo Vệ: khi bị tấn công, nếu Lá Chắn Hàn Sương không bị phá vỡ, gây <color=#f26c1c>1 điểm</color> ST Ổn Định lên kẻ tấn công.\n\nHành Động Chi Viện có thể kích hoạt thêm <color=#f26c1c>1 lần</color> mỗi hiệp, và hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định cho các đơn vị đồng minh khác <color=#f26c1c>trong phạm vi 4 ô</color> quanh người dùng."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Ánh Sáng Tuyết Nguyên",
                "effect": "Áp dụng <color=#3487e0>Phòng Thủ Tăng II</color> cho tất cả đơn vị đồng minh trong <color=#f26c1c>3 hiệp</color>. Số lượng Debuff được giải trừ tăng thêm <color=#f26c1c>2</color>, đồng thời giải trừ thêm các hiệu ứng <color=#3487e0>Khiếp Đảm</color>, <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Choáng</color>. Lượng HP hồi phục tăng thêm bằng <color=#f26c1c>50%</color> HP tối đa của Suomi. Bán kính ô Băng Giá mở rộng thêm <color=#f26c1c>1 ô</color>.\n\nHiệu quả của Khiên được tăng thêm <color=#f26c1c>30%</color>, tối đa lên đến <color=#f26c1c>150%</color> HP tối đa của mục tiêu."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Khí Thế Bất Khuất",
                "effect": "Sau khi sử dụng kỹ năng chủ động Cơn Thịnh Nộ Mùa Đông, nếu mục tiêu tiến vào hoặc đang trong trạng thái Sụp Đổ Ổn Định, hồi phục <color=#f26c1c>2 điểm</color> Độ Ổn Định của Suomi."
            },
            {
                "name": "Khóa Cố Định 2 - Người Bảo Vệ Nhỏ",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 3 - Phản Hồi Tích Cực",
                "effect": "Khi sử dụng kỹ năng chủ động Ân Huệ Của Tuyết, nếu HP của mục tiêu dưới <color=#f26c1c>80%</color>, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 4 - Di Chuyển Mau Lẹ",
                "effect": "Khi bắt đầu hiệp của bản thân, với mỗi đơn vị đồng minh (ngoại trừ bản thân) có HP dưới <color=#f26c1c>80%</color>, tăng Tầm Di Chuyển của đơn vị này thêm <color=#f26c1c>1 ô</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Bất Động",
                "effect": "Khi bị trúng trạng thái Choáng, Khiêu Khích hoặc Tê Liệt, ngay lập tức giải trừ hiệu ứng đó và miễn nhiễm với Choáng, Khiêu Khích, Tê Liệt trong 1 hiệp. Đồng thời nhận Lá Chắn Hàn Sương trong <color=#f26c1c>3 hiệp</color>. Lá Chắn Hàn Sương hấp thụ sát thương bằng <color=#f26c1c>60%</color> Tấn Công cơ bản, tối đa không quá <color=#f26c1c>100%</color> HP tối đa của Suomi. Chỉ kích hoạt 1 lần mỗi trận chiến."
            },
            {
                "name": "Khóa Cố Định 6 - Tiếp Vận Đang Tiến Hành",
                "effect": "Khi kết thúc hành động của đơn vị này, nếu Độ Ổn Định lớn hơn 0, hồi phục <color=#f26c1c>10%</color> HP tối đa và <color=#f26c1c>1 điểm</color> Độ Ổn Định."
            },
            {
                "name": "Khóa Tương Thích - Rock and Roll",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%"
            },
            {
                "name": "Khóa Chung - Phước Lành Nhiệm Vụ",
                "effect": "Phòng Thủ +5.0% / Khi HP giảm xuống dưới 80%, hồi phục <color=#f26c1c>15%</color> HP tối đa của đơn vị này và nhận <color=#3487e0>Phòng Thủ Tăng III</color> trong <color=#f26c1c>2 hiệp</color>. Chỉ kích hoạt 1 lần mỗi trận chiến."
            },
            {
                "name": "Khóa Mở Rộng - Khúc Ca Băng Giá",
                "effect": "Hành Động Chi Viện chuyển thành gây <color=#42cce0>ST Băng Kết</color>.\n\nKhi đồng minh có <color=#3487e0>Lá Chắn Hàn Sương</color>, tăng <color=#f26c1c>15%</color> <color=#42cce0>ST Băng Kết</color> gây ra và hồi phục <color=#f26c1c>4 điểm</color> Độ Ổn Định khi bắt đầu hiệp. Trước khi đồng minh tấn công, nếu chưa có Lá Chắn Hàn Sương, Suomi ngay lập tức áp dụng Lá Chắn Hàn Sương cho họ trong <color=#f26c1c>2 hiệp</color>. Lá Chắn Hàn Sương hấp thụ sát thương bằng <color=#f26c1c>60%</color> Tấn Công ban đầu của Suomi, tối đa không quá <color=#f26c1c>100%</color> HP tối đa của mục tiêu.\n\nÁnh Sáng Tuyết Nguyên: Kỹ năng này áp dụng <color=#3487e0>Phong Ấn Băng</color> trong <color=#f26c1c>2 hiệp</color>."
            }
        ]
    },
    "tololo": {
        "name": "Tololo",
        "en_name": "Tololo",
        "class": "Tiên Phong",
        "phase": "Hóa Lỏng",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Ngôi Sao Đôi",
        "weakness": "Điện Từ",
        "server": "global",
        "skills": [
            {
                "name": "Sao Băng",
                "en_name": "Meteor",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Tái Hiện Hố Đen",
                "en_name": "Black Hole Inversion",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>130%</color> Tấn Công. Nếu khai thác Điểm Yếu Thuộc Tính, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Xung Kích Siêu Tân Tinh",
                "en_name": "Supernova Impact",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Nếu bản thân có từ <color=#f26c1c>2 hiệu ứng Buff trở lên</color>, sát thương gây ra tăng <color=#f26c1c>20%</color> và nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Ánh Sáng Hủy Diệt",
                "en_name": "Morte Lumina",
                "tags": ["Tuyệt Kỹ", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>180%</color> Tấn Công. Nếu bản thân có từ <color=#f26c1c>3 hiệu ứng Buff trở lên</color>, sát thương gây ra tăng <color=#f26c1c>15%</color> và thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Màn Cực Quang",
                "en_name": "Aurora Curtain",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Khi bắt đầu trận chiến, nạp đầy Chỉ Số Nhiên Liệu lên mức tối đa. Sau khi tấn công, nếu Chỉ Số Nhiên Liệu đạt tối đa, tiêu hao tất cả và nhận <color=#f26c1c>1 lần</color> <color=#3487e0>Tăng Hành Động</color>.\n\nKhi bắt đầu mỗi hành động, cứ mỗi <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu, nhận <color=#f26c1c>1</color> Buff ngẫu nhiên duy trì cho đến khi kết thúc hành động. Mỗi khi một đơn vị đồng minh gây ST Hóa Lỏng, bản thân nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Gai Ánh Sáng</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Tái Hiện Hố Đen",
                "effect": "Nếu khai thác Điểm Yếu Thuộc Tính, đòn tấn công này bỏ qua <color=#f26c1c>15%</color> giảm thương từ Vật Cản (Yểm Hộ)."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Xung Kích Siêu Tân Tinh",
                "effect": "Nếu bản thân có từ <color=#f26c1c>3</color> Buff trở lên, đòn tấn công này chuyển thành gây <color=#2caadb>ST Hóa Lỏng</color>, đồng thời nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Ánh Sáng Hủy Diệt",
                "effect": "Nếu bản thân có từ <color=#f26c1c>3</color> Buff trở lên, sát thương gây ra tăng <color=#f26c1c>30%</color> và giảm thời gian hồi chiêu của kỹ năng này đi <color=#f26c1c>3 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Màn Cực Quang",
                "effect": "Trong thời gian Tăng Hành Động, đơn vị này nhận <color=#3487e0>Tăng Tấn Công Chuẩn Xác II</color>, <color=#3487e0>Tăng Tỷ Lệ Bạo Kích II</color>, <color=#3487e0>Dị Vị Tăng II</color>, và <color=#3487e0>Xuyên Thấu II</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Màn Cực Quang",
                "effect": "Hiệu ứng của Gai Ánh Sáng được cường hóa, tăng thêm <color=#f26c1c>2%</color> Tỷ Lệ Bạo Kích và <color=#f26c1c>2%</color> ST Bạo Kích."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Ánh Sáng Hủy Diệt",
                "effect": "Nếu đòn đánh này tiêu diệt mục tiêu, nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Quá Cảnh Đuôi Sao Chổi",
                "effect": "Tăng Hành Động giúp tăng Tầm Di Chuyển thêm <color=#f26c1c>1 ô</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Nguyên Lý Thiên Văn Quan Sát",
                "effect": "Khi sử dụng Tái Hiện Hố Đen, áp dụng <color=#3487e0>Đình Trệ</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 3 - Ánh Sáng Vô Hình",
                "effect": "Khi kích hoạt Tăng Hành Động, nhận <color=#3487e0>Tấn Công Tăng II</color> và <color=#3487e0>ST Tăng II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 4 - Nghịch Hành",
                "effect": "Khi sử dụng Xung Kích Siêu Tân Tinh, nếu đơn vị đồng minh thực hiện Tấn Công Chi Viện trước khi kích hoạt kỹ năng, áp dụng <color=#3487e0>Choáng</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Tuần Du Ngân Hà",
                "effect": "Khi khai thác Điểm Yếu Thuộc Tính, giải trừ <color=#f26c1c>2</color> Buff của mục tiêu trước khi tấn công."
            },
            {
                "name": "Khóa Cố Định 6 - Tinh Tú Che Khuất",
                "effect": "Khi ở mức HP và Chỉ Số Ổn Định tối đa, bỏ qua <color=#f26c1c>10%</color> giảm thương từ Vật Cản của mục tiêu."
            },
            {
                "name": "Khóa Tương Thích - Lời Thì Thầm Của Bụi Sao",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Ánh Hoàng Hôn",
                "effect": "Tấn Công +5.0% / Khi Chỉ Số Nhiên Liệu chưa đầy, sát thương gây ra tăng <color=#f26c1c>7%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Quỹ Đạo Vệ Tinh",
                "effect": "Sau khi dùng kỹ năng chủ động, Tololo nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu. Nếu đơn vị đồng minh (ngoại trừ Tololo) gây ST Hóa Lỏng, thời gian hồi chiêu của kỹ năng Tái Hiện Hố Đen giảm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Mở Rộng Cấp 2 - Mạng Lưới Vệ Tinh Vũ Trụ",
                "effect": "Khi bắt đầu trận chiến, Tololo nhận <color=#f26c1c>3 tầng</color> Dự Trữ Năng Lượng Tinh Tú.\nKhi kết thúc hành động của Tololo, cô nhận <color=#f26c1c>1 tầng</color> Lợi Thế Quan Sát trong <color=#f26c1c>1 hiệp</color>. Nếu số lượng Vệ Tinh Địa Tĩnh trên sân chưa đạt tối đa, tiêu hao <color=#f26c1c>1 tầng</color> Dự Trữ Năng Lượng Tinh Tú để triệu hồi <color=#f26c1c>1</color> Vệ Tinh Địa Tĩnh bên cạnh Tololo trong <color=#f26c1c>2 hiệp</color>.\nKhi bắt đầu mỗi hiệp cách quãng, Tololo nhận <color=#f26c1c>3 tầng</color> Dự Trữ Năng Lượng Tinh Tú.\nSau khi Tololo thực hiện tấn công chủ động, áp dụng Ấn Trọng Lực lên mục tiêu. Sau khi Vệ Tinh Địa Tĩnh gây sát thương, áp dụng <color=#f26c1c>1 tầng</color> Khúc Xạ Ánh Sao lên mục tiêu. Tololo sau đó nhận <color=#f26c1c>1 tầng</color> Cộng Hưởng Quỹ Đạo."
            }
        ],
        "summons": [
            {
                "name": "Vệ Tinh Cố Định",
                "type": "Vật Triệu Hồi Vật Lý",
                "description": "Thiết bị vệ tinh dẫn đường quỹ đạo, cung cấp tầm nhìn chiến thuật và kích hoạt các đòn đánh chi viện năng lượng.",
                "stats": {
                    "hp": "80% HP ban đầu của Tololo",
                    "atk": "100% Tấn Công ban đầu của Tololo",
                    "def": "80% Phòng Thủ ban đầu của Tololo"
                },
                "skills": [
                    {
                        "name": "Triệu Hồi Vì Sao",
                        "tags": ["Bị Động", "Chuẩn Xác"],
                        "description": "Khi kết thúc hiệp phe ta, gây ST Chuẩn Xác Hóa Lỏng bằng 130% Tấn Công lên đơn vị địch trong bán kính 7 ô xung quanh sở hữu Dấu Ấn Trọng Lực. Nếu không có đơn vị nào có Dấu Ấn Trọng Lực, chỉ định đơn vị địch gần nhất."
                    },
                    {
                        "name": "Đồng Bộ Tĩnh Lặng",
                        "tags": ["Bị Động"],
                        "description": "Miễn dịch với các hiệu ứng khống chế như Choáng, Khiêu Khích và Cấm Lệnh."
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
        "weapon_type": "Súng Shotgun",
        "ammo_type": "Đạn Shotgun",
        "signature_weapon": "Vị Ngọt Tự Nhiên",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Tôi Mời Khách",
                "en_name": "My Treat",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Bữa Tiệc Thịnh Soạn",
                "en_name": "Delicious Feast",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu", "Trị Liệu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color> để tấn công, gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>80%</color> Tấn Công lên mục tiêu đó và tất cả kẻ địch <color=#f26c1c>trong phạm vi 2 ô</color>, đồng thời áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>2 hiệp</color>. Hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho mỗi mục tiêu trúng đòn."
            },
            {
                "name": "Chuẩn Bị Bữa Ăn",
                "en_name": "Meal Preparation",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu", "Phá Hủy Vật Cản"],
                "description": "Chọn 1 hướng, gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>70%</color> Tấn Công lên tất cả mục tiêu địch trong phạm vi 3×6 ô theo hướng đã chọn, đồng thời áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>2 hiệp</color>. Phá hủy mọi Vật Cản có thể phá hủy nằm ngoài phạm vi 3×3 ô xung quanh bản thân."
            },
            {
                "name": "Tinh Thần Ẩm Thực",
                "en_name": "Gourmet Spirit",
                "tags": ["Tuyệt Kỹ", "Cường Hóa", "Phòng Ngự", "Phản Kích"],
                "description": "Áp dụng <color=#f26c1c>2 tầng</color> <color=#3487e0>Yểm Hộ</color> cho tất cả đơn vị đồng minh và bản thân nhận trạng thái <color=#3487e0>No Bụng</color> trong <color=#f26c1c>3 hiệp</color>. Khi có trạng thái No Bụng, nếu kẻ địch trong tầm bắn gây sát thương chuẩn xác lên một đơn vị đồng minh, Sabrina dùng Phản Kích lên kẻ đó, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>4 điểm</color> ST Ổn Định. Có thể kích hoạt tối đa 3 lần mỗi hiệp."
            },
            {
                "name": "Cải Tiến Linh Hoạt",
                "en_name": "Flexible Modification",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Trước khi một đơn vị đồng minh bị tấn công, nếu họ ở <color=#f26c1c>trong phạm vi 7 ô</color> quanh Sabrina, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Yểm Hộ</color> cho đồng minh đó. Có thể kích hoạt tối đa 4 lần mỗi hiệp. Sabrina nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu cho mỗi lần gây sát thương.\n\nSau khi dùng kỹ năng để tấn công, tạo ô địa hình Thủy Triều trong phạm vi ảnh hưởng. Nếu đã có ô địa hình Hóa Lỏng trong khu vực, kích hoạt phản ứng địa hình, xóa bỏ ô địa hình và gây ST cố định bằng <color=#f26c1c>20%</color> Tấn Công lên kẻ địch đứng trên ô đó."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Cải Tiến Linh Hoạt",
                "effect": "Số lần có thể áp dụng <color=#3487e0>Yểm Hộ</color> tăng thêm <color=#f26c1c>2 lần</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Chuẩn Bị Bữa Ăn",
                "effect": "Hệ số sát thương tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Bữa Tiệc Thịnh Soạn",
                "effect": "Nếu chỉ đánh trúng 1 mục tiêu, hồi phục <color=#f26c1c>6 điểm</color> Chỉ Số Ổn Định."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tinh Thần Ẩm Thực",
                "effect": "Tăng thêm <color=#f26c1c>10%</color> Tấn Công khi ở trạng thái <color=#3487e0>No Bụng</color>. Tăng thêm <color=#f26c1c>2 điểm</color> ST Ổn Định cho đòn Phản Kích."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Tinh Thần Ẩm Thực",
                "effect": "Không còn tiêu hao Chỉ Số Nhiên Liệu, nhận thêm <color=#f26c1c>1 lần</color> <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Cải Tiến Linh Hoạt",
                "effect": "Khi Chỉ Số Nhiên Liệu đầy, tiêu hao thêm <color=#f26c1c>4 điểm</color> Chỉ Số Nhiên Liệu để tăng sát thương kỹ năng thêm <color=#f26c1c>30%</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Ăn Là Hạnh Phúc",
                "effect": "Khi bị tấn công, Phòng Thủ tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Chia Sẻ Mỹ Vị",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 3 - Ninh Nhừ Mọi Thứ",
                "effect": "Khi đứng trên ô địa hình Hóa Lỏng, Phòng Thủ tăng thêm <color=#f26c1c>30%</color>, miễn nhiễm với các hiệu ứng dịch chuyển từ kẻ địch và mọi hiệu ứng địa hình Hóa Lỏng bất lợi."
            },
            {
                "name": "Khóa Cố Định 4 - Ăn No Ngủ Kỹ",
                "effect": "Khi Chỉ Số Nhiên Liệu chưa đầy, hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho mỗi điểm Chỉ Số Nhiên Liệu nhận được."
            },
            {
                "name": "Khóa Cố Định 5 - Quá Tải Calo",
                "effect": "Phạm vi hiệu lực của Bữa Tiệc Thịnh Soạn đổi thành 1 ô, kỹ năng nhắm vào ô địa hình thay vì đơn vị và kéo tất cả kẻ địch lại gần tâm <color=#f26c1c>1 ô</color>. Sát thương gây ra tăng lên thành <color=#f26c1c>100%</color> Tấn Công."
            },
            {
                "name": "Khóa Cố Định 6 - Thực Đơn Dưỡng Sinh Kì Lạ",
                "effect": "Kỹ năng chủ động Chuẩn Bị Bữa Ăn đổi thành ảnh hưởng 5 ô xung quanh bản thân, và không còn áp dụng Di Chuyển Giảm II. Thay vào đó áp dụng <color=#3487e0>Khiêu Khích</color> lên tối đa 2 mục tiêu trong <color=#f26c1c>1 hiệp</color>. Thời gian hồi chiêu tăng lên thành 3 hiệp."
            },
            {
                "name": "Khóa Tương Thích - Giờ Tráng Miệng",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%"
            },
            {
                "name": "Khóa Chung - Bảo Hộ Dầu Nóng",
                "effect": "Phòng Thủ +5.0% / Khi gây sát thương chuẩn xác, áp dụng <color=#3487e0>Di Chuyển Giảm II</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Mở Rộng - Công Thức Huyền Thoại",
                "effect": "Đòn Phản Kích chuyển sang gây <color=#2caadb>ST Hóa Lỏng</color>. Nếu đòn đánh này kích hoạt bất kỳ hiệu ứng ô địa hình Hóa Lỏng nào, hiệu ứng của ô địa hình sẽ không bị xóa bỏ. Mỗi lần thực hiện Phản Kích, sát thương Sabrina phải chịu giảm <color=#f26c1c>5%</color>, cộng dồn tối đa <color=#f26c1c>30%</color>, duy trì trong <color=#f26c1c>2 hiệp</color>."
            }
        ]
    },
    "qiongjiu": {
        "name": "Qiongjiu",
        "en_name": "Qiongjiu",
        "class": "Tiên Phong",
        "phase": "Thiêu Đốt",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Ngọn Lửa Dẫn Đường",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Mồi Lửa",
                "en_name": "Fuse",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Đường Đạn Chung",
                "en_name": "Common Rail",
                "tags": ["Chủ Động", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>150%</color> Tấn Công. Đồng thời bản thân nhận <color=#3487e0>Tăng Chi Viện I</color>."
            },
            {
                "name": "Chỉ Dẫn Thắng Lợi",
                "en_name": "Guide to Victory",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 hướng, gây <color=#e67129>ST Thiêu Đốt</color> AoE bằng <color=#f26c1c>110%</color> Tấn Công lên mục tiêu địch đầu tiên trúng đòn <color=#f26c1c>trong phạm vi 8 ô</color> theo hướng đã chọn. Áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Truy Kích Đoạt Thế",
                "en_name": "Pressing the Momentum",
                "tags": ["Tuyệt Kỹ", "Cường Hóa"],
                "description": "Nhận <color=#f26c1c>3 tầng</color> <color=#3487e0>Tăng Chi Viện II</color>. Khi Chỉ Số Nhiên Liệu đạt tối đa, nhận thêm <color=#f26c1c>1 tầng</color> và tăng số lần Hành Động Chi Viện tối đa trong hiệp này thêm <color=#f26c1c>1 lần</color>."
            },
            {
                "name": "Mưu Lược Ổn Định",
                "en_name": "Steady Plan",
                "tags": ["Bị Động", "Hỗ Trợ", "Cường Hóa"],
                "description": "Nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu mỗi lần sau khi gây sát thương. Tăng sát thương gây ra lên các mục tiêu không được Vật Cản (Yểm Hộ) bảo vệ thêm <color=#f26c1c>10%</color>.\n\nKhi một đơn vị địch trong tầm bắn nhận sát thương chuẩn xác từ đồng minh, Qiongjiu thực hiện 1 lần Hành Động Chi Viện, gây ST Vật Lý bằng <color=#f26c1c>90%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định. Hiệu ứng này có thể kích hoạt tối đa 3 lần mỗi hiệp."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Đường Đạn Chung",
                "effect": "Nếu tiêu diệt được mục tiêu, mức tăng sát thương của <color=#3487e0>Tăng Chi Viện I</color> tăng lên thành <color=#f26c1c>30%</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Chỉ Dẫn Thắng Lợi",
                "effect": "Nếu mục tiêu đang chịu trạng thái <color=#3487e0>Tràn Lửa</color>, đòn tấn công này tăng <color=#f26c1c>100%</color> Tỷ Lệ Bạo Kích."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Mưu Lược Ổn Định",
                "effect": "Sau khi thực hiện Hành Động Chi Viện, áp dụng <color=#3487e0>Tràn Lửa</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>. Sát thương của Hành Động Chi Viện tăng thêm <color=#f26c1c>10%</color>."
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
                "effect": "Khi thực hiện Hành Động Chi Viện, áp dụng <color=#3487e0>ST Tăng II</color> cho bản thân và đơn vị đồng minh trong <color=#f26c1c>1 hiệp</color> trước khi đồng minh đó tung đòn tấn công."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Mưu Lược Ổn Định",
                "effect": "Sát thương gây ra lên mục tiêu không được Vật Cản bảo vệ tăng thêm <color=#f26c1c>10%</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Sự Tập Trung",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 2 - Hoạch Định Hiệu Quả",
                "effect": "Trước khi thực hiện Hành Động Chi Viện, giải trừ <color=#f26c1c>1</color> Buff của mục tiêu."
            },
            {
                "name": "Khóa Cố Định 3 - Huấn Luyện Mục Tiêu",
                "effect": "Khi đang ở Chế Độ Chi Viện, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color> trước đòn đánh của đồng minh."
            },
            {
                "name": "Khóa Cố Định 4 - Điểm Yếu",
                "effect": "Điều chỉnh hiệu ứng kỹ năng Chỉ Dẫn Thắng Lợi để gây sát thương lên tất cả mục tiêu địch trong phạm vi 8 ô theo hướng đã chọn. Tất cả các mục tiêu ngoại trừ mục tiêu đầu tiên chịu ít hơn 30% sát thương."
            },
            {
                "name": "Khóa Cố Định 5 - Điều Chỉnh Cần Thiết",
                "effect": "Khi khai thác Điểm Yếu Thuộc Tính bằng kỹ năng Đường Đạn Chung, nhận <color=#3487e0>Thế Công Rực Lửa II</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 6 - Sự Kiên Định",
                "effect": "Khi đang chịu ảnh hưởng của Tăng Chi Viện, miễn nhiễm với các hiệu ứng dịch chuyển vị trí do kẻ địch gây ra."
            },
            {
                "name": "Khóa Tương Thích - Ấm Áp Như Ngọc",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Đàm Phán Chiến Lược",
                "effect": "Bạo Kích +5.0% / Tăng <color=#f26c1c>7%</color> sát thương gây ra ngoài lượt đi của bản thân."
            },
            {
                "name": "Khóa Mở Rộng - Ngọc Vỡ",
                "effect": "Sát thương gây ra bởi Hành Động Chi Viện chuyển thành <color=#e67129>ST Thiêu Đốt</color>, và sát thương lên mục tiêu có Debuff Thiêu Đốt tăng thêm <color=#f26c1c>15%</color>."
            }
        ]
    },
    "daiyan": {
        "name": "Daiyan",
        "en_name": "Daiyan",
        "class": "Tiên Phong",
        "phase": "Vật Lý",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Ngọc Khúc",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Gảy Đàn",
                "en_name": "Plucking Strings",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Tiếng Vàng Điệu Ngọc",
                "en_name": "Absolute Tuning",
                "tags": ["Chủ Động", "Chỉ Định", "Giải Trừ"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, giải trừ <color=#f26c1c>1</color> Buff trên mục tiêu, và gây ST Vật Lý bằng <color=#f26c1c>150%</color> Tấn Công."
            },
            {
                "name": "Hòa Điệu Thanh Thương",
                "en_name": "Qing Shang Harmony",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Nhận <color=#f26c1c>3 tầng</color> <color=#3487e0>Chỉnh Âm</color>, nhận <color=#3487e0>Định Âm</color> trong <color=#f26c1c>1 hiệp</color>, và nhận <color=#f26c1c>1 lần</color> <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "name": "Âm Vang Mê Hoặc",
                "en_name": "Ethereal Resonance",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>190%</color> Tấn Công. Cứ mỗi <color=#f26c1c>1 tầng</color> <color=#3487e0>Chỉnh Âm</color>, giảm thời gian hồi chiêu của kỹ năng này đi <color=#f26c1c>1 hiệp</color>.\n\nSau khi tấn công, tiêu hao toàn bộ số tầng <color=#3487e0>Chỉnh Âm</color> và nhận vĩnh viễn <color=#f26c1c>1 tầng</color> <color=#3487e0>Chỉnh Âm</color>, tối đa cộng dồn 3 tầng vĩnh viễn."
            },
            {
                "name": "Tiếng Đàn Tiếp Viện",
                "en_name": "Swift Harmony",
                "tags": ["Bị Động", "Phục Kích"],
                "description": "Khi bắt đầu hành động, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu và <color=#f26c1c>1 tầng</color> <color=#3487e0>Chỉnh Âm</color>. Khi thực hiện tấn công chủ động lên mục tiêu không được Vật Cản bảo vệ, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\n\nTrước khi nhận sát thương chuẩn xác, nếu số tầng Chỉnh Âm lớn hơn 2, tung <color=#3487e0>Chặn Đánh</color>, gây ST Vật Lý loại đạn nhẹ bằng <color=#f26c1c>150%</color> Tấn Công và <color=#f26c1c>4 điểm</color> ST Ổn Định, đồng thời nhận vĩnh viễn <color=#f26c1c>1 tầng</color> <color=#3487e0>Chỉnh Âm</color>. Hiệu ứng này có thể kích hoạt 1 lần mỗi hiệp.\n\nNếu số tầng Chỉnh Âm lớn hơn 3, sát thương gây ra tăng thêm <color=#f26c1c>20%</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Tiếng Vàng Điệu Ngọc",
                "effect": "Nếu mục tiêu không có Buff nào để giải trừ trong đòn tấn công, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Chỉnh Âm</color> sau đòn đánh."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Hòa Điệu Thanh Thương",
                "effect": "Số tầng <color=#3487e0>Chỉnh Âm</color> nhận được tăng thêm <color=#f26c1c>3 tầng</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Âm Vang Mê Hoặc",
                "effect": "Giới hạn cộng dồn Chỉnh Âm vĩnh viễn tăng thêm <color=#f26c1c>3 tầng</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tiếng Đàn Tiếp Viện",
                "effect": "Nếu số tầng Chỉnh Âm lớn hơn 5, sát thương gây ra tăng lên thành <color=#f26c1c>40%</color>. Đồng thời ST Ổn Định gây ra bởi <color=#3487e0>Chặn Đánh</color> tăng thêm <color=#f26c1c>2 điểm</color>, và hệ số sát thương ban đầu tăng thêm <color=#f26c1c>30%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Tiếng Đàn Tiếp Viện",
                "effect": "Khi số tầng Chỉnh Âm vĩnh viễn đạt tối đa, bỏ qua <color=#f26c1c>15%</color> giảm thương từ Vật Cản khi tấn công kẻ địch bị Lộ Diện."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Âm Vang Mê Hoặc",
                "effect": "Với mỗi đơn vị địch tử trận trên chiến trường, nhận vĩnh viễn <color=#f26c1c>1 tầng</color> <color=#3487e0>Chỉnh Âm</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Giai Điệu Vang Vọng",
                "effect": "Khi Daiyan có Chỉnh Âm, tăng Tầm Di Chuyển thêm <color=#f26c1c>1 ô</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Giấc Mơ Dang Dở",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 3 - Khúc Ca Người Hành Hương",
                "effect": "Với mỗi điểm di chuyển bổ sung trước đòn tấn công, Tỷ Lệ Bạo Kích tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "name": "Khóa Cố Định 4 - Khúc Hát Thanh Bình",
                "effect": "Nếu Tầm Di Chuyển của Daiyan cao hơn mục tiêu, nhận <color=#f26c1c>1 tầng</color> Chỉnh Âm trước khi tung đòn tấn công chủ động."
            },
            {
                "name": "Khóa Cố Định 5 - Phá Vỡ Đội Hình",
                "effect": "Cứ mỗi 3 tầng Chỉnh Âm, giải trừ thêm <color=#f26c1c>1</color> Buff khi dùng kỹ năng chủ động Tiếng Vàng Điệu Ngọc."
            },
            {
                "name": "Khóa Cố Định 6 - Di Sản Vĩnh Cửu",
                "effect": "Sau khi dùng Hòa Điệu Thanh Thương, nếu có kẻ địch bị tiêu diệt trong hiệp này, hồi phục <color=#f26c1c>20%</color> HP tối đa và <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định."
            },
            {
                "name": "Khóa Tương Thích - Khúc Hát Ngọt Ngào",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Đá Vỡ Lụa Tàn",
                "effect": "Bạo Kích +5.0% / Khi bắt đầu hành động, nhận <color=#3487e0>Di Chuyển Tăng I</color> trong <color=#f26c1c>1 hiệp</color> (hồi chiêu 1 hiệp)."
            },
            {
                "name": "Khóa Mở Rộng - Khúc Biến Tấu",
                "effect": "Với mỗi tầng Chỉnh Âm vĩnh viễn đang giữ, bỏ qua <color=#f26c1c>10%</color> Phòng Thủ của mục tiêu khi tấn công. Khi kết thúc hành động, nhận <color=#f26c1c>2 tầng</color> Chỉnh Âm, và với mỗi tầng Chỉnh Âm vĩnh viễn, tăng thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Mở Rộng Cấp 2 - Khúc Biến Tấu Thần Tốc",
                "effect": "Khi dùng Tuyệt Kỹ Âm Vang Mê Hoặc và kích hoạt <color=#3487e0>Chặn Đánh</color>, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Chỉnh Âm</color> vĩnh viễn.\n\nKhi kết thúc hiệp, nếu không kích hoạt <color=#3487e0>Chặn Đánh</color>, nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Chỉnh Âm</color> vĩnh viễn và tăng hệ số sát thương của đòn tấn công chủ động kế tiếp thêm <color=#f26c1c>150%</color> cùng <color=#f26c1c>4 điểm</color> ST Ổn Định.\n\nSau khi dùng Tuyệt Kỹ Âm Vang Mê Hoặc, thực hiện thêm <color=#f26c1c>1 đòn tấn công bổ sung</color> lên mục tiêu. Cứ mỗi tầng Chỉnh Âm vĩnh viễn đang có, đòn tấn công này gây ST Vật Lý bằng <color=#f26c1c>100%</color> Tấn Công và <color=#f26c1c>1 điểm</color> ST Ổn Định."
            }
        ]
    },
    "klukai": {
        "name": "Klukai",
        "en_name": "Klukai",
        "class": "Tiên Phong",
        "phase": "Ăn Mòn",
        "rarity": "Elite",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Vết Tích Xâm Thực",
        "weakness": "Thiêu Đốt",
        "server": "global",
        "skills": [
            {
                "name": "Đòn Đánh Nhanh",
                "en_name": "Swift Strike",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Điểm Nổ Chuẩn Xác",
                "en_name": "Pinpoint Detonation",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng <color=#f26c1c>80%</color> Tấn Công. Thực hiện thêm 1 đòn tấn công bổ sung, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>60%</color> Tấn Công lên mục tiêu đó và tất cả kẻ địch <color=#f26c1c>trong phạm vi 3 ô</color>, kéo tất cả kẻ địch chịu ảnh hưởng lại gần tâm <color=#f26c1c>1 ô</color>.\n\nNếu có bất kỳ kẻ địch nào bị tiêu diệt, giảm thời gian hồi chiêu của Tuyệt Kỹ Đột Phá Hủy Diệt đi <color=#f26c1c>1 hiệp</color>, và nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.\n\nNếu không có kẻ địch nào bị tiêu diệt, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Ăn Mòn Áp Đảo",
                "en_name": "Overpowering Corrosion",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Chọn 1 ô <color=#f26c1c>trong phạm vi 8 ô</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>90%</color> Tấn Công lên tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 3 ô</color>, và áp dụng <color=#3487e0>Độc Tính Xâm Nhập</color> trong <color=#f26c1c>2 hiệp</color>. Tăng <color=#f26c1c>15%</color> sát thương lên các mục tiêu đã chịu Độc Tính Xâm Nhập."
            },
            {
                "name": "Đột Phá Hủy Diệt",
                "en_name": "Devastating Drift",
                "tags": ["Tuyệt Kỹ", "Phạm Vi"],
                "description": "Chọn 1 ô trong phạm vi hình chữ thập từ <color=#f26c1c>4 đến 8 ô</color>, đáp xuống ô đã chọn và gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công lên tất cả mục tiêu địch trên đường đi rộng <color=#f26c1c>5 ô</color>. Nhận <color=#f26c1c>6 ô</color> Di Chuyển Bổ Sung. Nếu tiêu diệt từ <color=#f26c1c>2 mục tiêu trở lên</color>, kỹ năng này có thể được dùng lại thêm 1 lần (tối đa dùng lại 1 lần)."
            },
            {
                "name": "Kiêu Hãnh Tinh Anh",
                "en_name": "Elite's Pride",
                "tags": ["Bị Động", "Suy Yếu", "Cường Hóa"],
                "description": "Miễn nhiễm với tất cả các hiệu ứng ô địa hình loại Khống Chế bất lợi. Khi gây sát thương bằng tấn công chủ động, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>, và nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Hiếu Thắng</color> sau khi dùng kỹ năng.\n\nMỗi khi Klukai tung đòn tấn công chủ động hoặc đơn vị đồng minh khác gây ST Ăn Mòn, Klukai nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Cứ mỗi <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu nhận được, giảm thời gian hồi chiêu Tuyệt Kỹ của cô ấy đi <color=#f26c1c>1 hiệp</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ăn Mòn Áp Đảo",
                "effect": "Sát thương gây ra lên mục tiêu đã chịu <color=#3487e0>Độc Tính Xâm Nhập</color> tăng thêm <color=#f26c1c>30%</color>.\n\nNếu mục tiêu không bị tiêu diệt bởi sát thương này, vẫn kích hoạt hiệu ứng khi tử trận của Độc Tính Xâm Nhập.\n\nĐộc Tính Xâm Nhập nhận thêm hiệu ứng: Khi mục tiêu mang hiệu ứng này kết thúc hành động, người thi triển áp dụng Độc Tính Xâm Nhập trong <color=#f26c1c>2 hiệp</color> lên các đơn vị địch trong phạm vi 3 ô chưa có Độc Tính Xâm Nhập."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Kiêu Hãnh Tinh Anh",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 tầng</color> <color=#3487e0>Hiếu Thắng</color>. Khi đồng minh khác gây ST Ăn Mòn, Klukai có thể nhận 1 tầng Hiếu Thắng. Tăng giới hạn số tầng Hiếu Thắng thêm <color=#f26c1c>4 tầng</color>.\n\nCứ mỗi 3 điểm Chỉ Số Nhiên Liệu nhận được, áp dụng thêm 1 tầng Áp Chế Ăn Mòn Mạnh lên các đơn vị địch đã có Áp Chế Ăn Mòn Mạnh, và giảm hồi chiêu Tuyệt Kỹ của Klukai đi 1 hiệp.\n\nÁp Chế Ăn Mòn Mạnh nhận thêm hiệu ứng: Khi Klukai tung tấn công chủ động hoặc đồng minh khác gây ST Ăn Mòn, áp dụng thêm 1 tầng Áp Chế Ăn Mòn Mạnh lên các mục tiêu đã có hiệu ứng này. Phòng Thủ giảm thêm 1%, và giới hạn cộng dồn tăng thêm 5 tầng."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Đột Phá Hủy Diệt",
                "effect": "Với mỗi kẻ địch trúng đòn, tăng sát thương gây ra thêm <color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>50%</color>. Nếu đánh trúng Boss, mức tăng này ngay lập tức đạt mức tối đa 50%.\n\nNếu đánh trúng từ 2 mục tiêu trở lên hoặc đánh trúng Boss, kỹ năng này có thể được dùng lại 1 lần nữa. Trước khi tấn công, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> và <color=#3487e0>Độc Tính Xâm Nhập</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Điểm Nổ Chuẩn Xác",
                "effect": "Sát thương gây ra ở lần sát thương đầu tiên tăng lên thành <color=#f26c1c>100%</color> Tấn Công. Với mỗi tầng Áp Chế Ăn Mòn Mạnh trên mục tiêu, hệ số sát thương của đòn tấn công bổ sung tăng thêm <color=#f26c1c>5%</color>. Nếu khai thác Điểm Yếu Thuộc Tính, đòn đánh bỏ qua <color=#f26c1c>15%</color> giảm thương từ Vật Cản của mục tiêu."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Ăn Mòn Áp Đảo",
                "effect": "Tầm hiệu lực tăng thêm <color=#f26c1c>2 ô</color>, sát thương tăng lên thành <color=#f26c1c>110%</color> Tấn Công. Bán kính lan truyền của Độc Tính Xâm Nhập tăng thêm <color=#f26c1c>1 ô</color>, và sát thương gây ra tăng lên thành <color=#f26c1c>80%</color> Tấn Công. Nếu mục tiêu đang chịu Debuff Ăn Mòn, áp dụng Độc Tính Xâm Nhập trong 2 hiệp trước khi tấn công.\n\nĐộc Tính Xâm Nhập nhận thêm hiệu ứng: Khi nhận đòn tấn công chủ động từ Klukai, sát thương phải chịu tăng thêm <color=#f26c1c>30%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Đột Phá Hủy Diệt",
                "effect": "Bỏ qua giảm thương từ Vật Cản.\n\nTăng độ rộng thêm <color=#f26c1c>2 ô</color> và áp dụng <color=#3487e0>Hoảng Sợ</color> trong <color=#f26c1c>2 hiệp</color>.\n\nSau đòn tấn công, kích hoạt toàn bộ hiệu ứng Áp Chế Ăn Mòn Mạnh và hiệu ứng khi tử trận của Độc Tính Xâm Nhập trên tất cả kẻ địch."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Cuốn Dây Chết Người",
                "effect": "Khi bắt đầu hiệp, nếu chỉ có 1 mục tiêu duy nhất, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> lên kẻ đó trong <color=#f26c1c>2 hiệp</color>. Đồng thời nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 2 - Một Nhát Đoạt Mạng",
                "effect": "Nếu Tuyệt Kỹ Đột Phá Hủy Diệt chỉ đánh trúng 1 mục tiêu, tăng <color=#f26c1c>30%</color> sát thương gây ra."
            },
            {
                "name": "Khóa Cố Định 3 - Không Thương Tiếc",
                "effect": "Áp Chế Ăn Mòn Mạnh nhận thêm hiệu ứng: tăng <color=#f26c1c>15%</color> sát thương lên các mục tiêu đang trong trạng thái Sụp Đổ Ổn Định."
            },
            {
                "name": "Khóa Cố Định 4 - Chi Viện Đắc Lực",
                "effect": "Với mỗi đòn Tấn Công Chi Viện do các đơn vị đồng minh khác thực hiện, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 5 - Phá Vỡ Giới Hạn",
                "effect": "Giảm độ rộng phạm vi hiệu lực của Tuyệt Kỹ Đột Phá Hủy Diệt xuống còn 3 ô. Với mỗi ô giảm bớt, tăng <color=#f26c1c>10%</color> sát thương gây ra."
            },
            {
                "name": "Khóa Cố Định 6 - Khoảnh Khắc Diệt Vong",
                "effect": "Sau khi đơn vị chịu Độc Tính Xâm Nhập nhận sát thương từ hiệu ứng của nó và sống sót, chúng bị áp dụng thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Khóa Tương Thích",
                "effect": "Tấn Công +3%, Bạo Kích +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Sát Khí Trở Lại",
                "effect": "Tấn Công +5.0% / Khi bắt đầu hiệp, nếu Chỉ Số Nhiên Liệu của người dùng đầy, sát thương diện rộng AoE tiếp theo gây ra bởi tấn công chủ động tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Kiêu Hãnh Của Búp Bê Tinh Anh",
                "effect": "Khi bắt đầu chiến đấu, triệu hồi Drone Nanh Vuốt đi theo Klukai (không thể bị chọn làm mục tiêu và không tính là vật triệu hồi độc lập).\n\nSau đòn tấn công chủ động của Klukai, Drone Nanh Vuốt tấn công 3 kẻ địch gần nhất, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công của Klukai bỏ qua Vật Cản, và áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Độc Tính Xâm Nhập</color>. Hệ số sát thương tăng thêm 10% mỗi lần kích hoạt hiệu ứng Áp Chế Ăn Mòn Mạnh hoặc hiệu ứng khi tử trận của Độc Tính Xâm Nhập.\n\nKhi hiệu ứng Áp Chế Ăn Mòn Mạnh được kích hoạt, hệ số sát thương tăng thêm 1% cho mỗi tầng Hiếu Thắng."
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
        "signature_weapon": "Lời Hứa Hầu Gái",
        "weakness": "Ăn Mòn",
        "server": "global",
        "skills": [
            {
                "name": "Giờ Dọn Dẹp",
                "en_name": "Cleaning Time",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu <color=#f26c1c>trong phạm vi 7 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Đón Tiếp Chu Đáo",
                "en_name": "Careful Hospitality",
                "tags": ["Chủ Động", "Chỉ Định", "Trị Liệu", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô</color>, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>130%</color> Tấn Công lên mục tiêu đó. Sau khi tấn công, hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công cho mục tiêu đồng minh gần nhất (ngoại trừ bản thân) và nhận <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>. Nếu mục tiêu địch đang chịu <color=#3487e0>Tràn Lửa</color>, hồi phục thêm cho 1 mục tiêu đồng minh nữa."
            },
            {
                "name": "Thức Uống Đặc Biệt Của Zucchero",
                "en_name": "Zucchero's Special Drink",
                "tags": ["Chủ Động", "Phạm Vi", "Trị Liệu", "Giải Trừ"],
                "description": "Chọn 1 mục tiêu đồng minh <color=#f26c1c>trong phạm vi 7 ô</color>, hồi phục HP bằng <color=#f26c1c>150%</color> Tấn Công phân bổ đều cho mục tiêu đó và tất cả đơn vị đồng minh <color=#f26c1c>trong phạm vi 3 ô</color>. Đồng thời gây ST Vật Lý AoE bằng <color=#f26c1c>50%</color> Tấn Công lên tất cả kẻ địch trong phạm vi. Nếu mục tiêu địch có <color=#3487e0>Tràn Lửa</color>, giải trừ <color=#f26c1c>2</color> Buff trên kẻ đó."
            },
            {
                "name": "Giờ Nghỉ Trà Chiều",
                "en_name": "Afternoon Tea Break",
                "tags": ["Tuyệt Kỹ", "Trị Liệu", "Hỗ Trợ", "Giải Trừ", "Cường Hóa"],
                "description": "Hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công cho tất cả đồng minh trên toàn bản đồ, giải trừ <color=#f26c1c>2</color> Debuff, xóa bỏ trạng thái <color=#3487e0>Khiếp Đảm</color> và <color=#3487e0>Choáng</color>, đồng thời hồi phục tối đa <color=#f26c1c>7 điểm</color> Chỉ Số Ổn Định cho đồng minh có Chỉ Số Ổn Định thấp nhất. Sau khi trị liệu, áp dụng <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>."
            },
            {
                "name": "Bổn Phận Hầu Gái",
                "en_name": "Maid's Duty",
                "tags": ["Bị Động", "Cường Hóa", "Suy Yếu", "Hỗ Trợ"],
                "description": "Khi bắt đầu chiến đấu, nhận <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color>.\n\nKhi ở trong trạng thái Hồi Phục Trạng Thái Nhiệt: Sát thương gây ra tăng <color=#f26c1c>20%</color>. Khi trị liệu, hồi phục thêm <color=#f26c1c>10%</color> HP tối đa của người dùng. Sau các đòn tấn công chủ động, áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>2 hiệp</color>.\n\nKhi đơn vị địch trong tầm bắn nhận sát thương chuẩn xác từ đồng minh, ưu tiên thực hiện 1 lần Hành Động Chi Viện, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn Định lên kẻ đó, đồng thời áp dụng <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color> cho đơn vị đồng minh. Nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Kỹ năng có thể kích hoạt tối đa 2 lần mỗi hiệp."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Bổn Phận Hầu Gái",
                "effect": "Khi Hành Động Chi Viện được kích hoạt, áp dụng thêm <color=#3487e0>Thế Công Rực Lửa II</color> và <color=#3487e0>ST Tăng II</color> cho đơn vị đồng minh trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Bổn Phận Hầu Gái",
                "effect": "Khi trạng thái Hồi Phục Trạng Thái Nhiệt có hiệu lực: lượng trị liệu tăng <color=#f26c1c>20%</color> và sát thương gây ra tăng <color=#f26c1c>40%</color>. Nếu mục tiêu được trị liệu có Hồi Phục Trạng Thái Nhiệt, mức tăng trị liệu nâng lên thành <color=#f26c1c>50%</color>; nếu mục tiêu địch có Tràn Lửa, sát thương gây ra tăng lên thành <color=#f26c1c>50%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Đón Tiếp Chu Đáo",
                "effect": "Nếu bản thân có Hồi Phục Trạng Thái Nhiệt, nhận thêm <color=#3487e0>Tuần Hoàn Nhiệt</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Giờ Nghỉ Trà Chiều",
                "effect": "Số lượng Debuff được giải trừ tăng thêm 1, đồng thời xóa bỏ thêm các hiệu ứng <color=#3487e0>Khiêu Khích</color>, <color=#3487e0>Khiếp Đảm</color>, <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Choáng</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Thức Uống Đặc Biệt Của Zucchero",
                "effect": "Mỗi mục tiêu đồng minh được hồi phục ít nhất <color=#f26c1c>75%</color> Tấn Công của Centaureissi dưới dạng HP."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Giờ Nghỉ Trà Chiều",
                "effect": "Hồi phục Chỉ Số Ổn Định cho 2 đồng minh có Độ Ổn Định thấp nhất, sau đó tăng thêm <color=#f26c1c>1 điểm</color> nữa."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Tráng Miệng Trước Bữa Ăn",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 2 - Quyết Tâm Của Hầu Gái",
                "effect": "Nếu đơn vị đồng minh trong phạm vi 7 ô rơi vào trạng thái Sụp Đổ Ổn Định sau khi nhận sát thương, xóa bỏ Hồi Phục Trạng Thái Nhiệt trên bản thân và áp dụng Hồi Phục Trạng Thái Nhiệt cho đồng minh đó."
            },
            {
                "name": "Khóa Cố Định 3 - Xử Lý Hiệu Quả",
                "effect": "Khi Hồi Phục Trạng Thái Nhiệt được kích hoạt, ngẫu nhiên giải trừ <color=#f26c1c>1</color> Buff của kẻ tấn công. Trước khi Hồi Phục Trạng Thái Nhiệt kích hoạt, giải trừ 2 Debuff trên các đồng minh đang có Hồi Phục Trạng Thái Nhiệt."
            },
            {
                "name": "Khóa Cố Định 4 - Công Thức Dễ Chịu",
                "effect": "Tăng hệ số trị liệu của kỹ năng chủ động Thức Uống Đặc Biệt Của Zucchero thêm <color=#f26c1c>75%</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Chuẩn Bị Kỹ Lưỡng",
                "effect": "Khi trị liệu cho mục tiêu đồng minh bằng kỹ năng chủ động, giải trừ 1 Debuff. Với các mục tiêu có Hồi Phục Trạng Thái Nhiệt, giải trừ thêm 1 Debuff nữa."
            },
            {
                "name": "Khóa Cố Định 6 - Thực Đơn May Mắn",
                "effect": "Khi trị liệu cho mục tiêu đồng minh bằng kỹ năng chủ động, nếu mục tiêu có Hồi Phục Trạng Thái Nhiệt, ngẫu nhiên áp dụng 1 Buff mạnh cho họ trong 1 hiệp."
            },
            {
                "name": "Khóa Tương Thích",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%"
            },
            {
                "name": "Khóa Chung - Đồ Uống Nóng Thiết Yếu",
                "effect": "HP +5.0% / Khi kết thúc hành động, áp dụng <color=#3487e0>Hồi Phục Trạng Thái Nhiệt</color> cho đồng minh gần nhất chưa có hiệu ứng này (hồi chiêu 2 hiệp)."
            },
            {
                "name": "Khóa Mở Rộng - Ý Chí Bảo Vệ",
                "effect": "Khi bắt đầu trận chiến và sau khi kích hoạt Giờ Nghỉ Trà Chiều, áp dụng <color=#3487e0>Trà Nóng Tỉnh Táo</color> lên bản thân trong <color=#f26c1c>2 hiệp lớn</color> (thời gian duy trì giảm khi kết thúc hiệp hiện tại).\n\nSau khi kích hoạt Thức Uống Đặc Biệt Của Zucchero, áp dụng <color=#3487e0>Che Chở Hoàn Hảo</color> cho tất cả đồng minh trong <color=#f26c1c>2 hiệp</color>. Khi đồng minh gây ST Thiêu Đốt hoặc khi Centaureissi kích hoạt Hành Động Chi Viện, tăng 1 điểm Chỉ Số Nhiên Liệu (kích hoạt 1 lần mỗi hiệp)."
            }
        ]
    },
    "balthilde": {
        "name": "Balthilde",
        "en_name": "Balthilde",
        "class": "Hỗ Trợ",
        "phase": "Vật Lý",
        "rarity": "Standard",
        "weapon_type": "Súng Shotgun",
        "ammo_type": "Đạn Shotgun",
        "signature_weapon": "Búa Rèn Bền Bỉ",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Đòn Đập Băng Vụn",
                "en_name": "Cryoshatter Strike",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Giao Thức Gia Cố",
                "en_name": "Reinforcement Protocol",
                "tags": ["Chủ Động", "Triệu Hồi", "Phòng Ngự"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 8 ô</color> và triệu hồi Vật Tạo Phòng Ngự trên ô đó. Nếu Vật Tạo Phòng Ngự đã được triệu hồi, nó sẽ dịch chuyển tới ô đã chọn.\n\nNếu Giao Thức Phá Hủy chưa được dùng trong hiệp này, Balthilde có thể dùng Giao Thức Phá Hủy 1 lần.\n\nKhi Vật Tạo Phòng Ngự bị phá hủy, kỹ năng này bước vào thời gian hồi chiêu <color=#f26c1c>3 hiệp</color>."
            },
            {
                "name": "Giao Thức Phá Hủy",
                "en_name": "Demolition Protocol",
                "tags": ["Chủ Động", "Triệu Hồi"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 8 ô</color> và triệu hồi Vật Tạo Tấn Công trên ô đó. Nếu Vật Tạo Tấn Công đã được triệu hồi, nó sẽ dịch chuyển tới ô đã chọn.\n\nNếu Giao Thức Gia Cố chưa được dùng trong hiệp này, Balthilde có thể dùng Giao Thức Gia Cố 1 lần.\n\nKhi Vật Tạo Tấn Công bị phá hủy, kỹ năng này bước vào thời gian hồi chiêu <color=#f26c1c>3 hiệp</color>."
            },
            {
                "name": "Nổ Chuỗi Cuồng Nộ",
                "en_name": "Raging Chainblast",
                "tags": ["Tuyệt Kỹ", "Phạm Vi"],
                "description": "Chọn 1 hướng, gây ST Vật Lý AoE bằng <color=#f26c1c>100%</color> Tấn Công lên tất cả kẻ địch trong khu vực hình quạt <color=#f26c1c>6 ô</color> theo hướng đã chọn.\n\nGiảm thời gian hồi chiêu của Giao Thức Gia Cố và Giao Thức Phá Hủy đi <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Hiệu Chuẩn Cờ Lê",
                "en_name": "Wrench Calibration",
                "tags": ["Bị Động"],
                "description": "Sau khi thực hiện Đánh Thường, tăng <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Khi đồng minh (ngoại trừ bản thân) gây ST Vật Lý bằng tấn công chủ động, tăng <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu cho bản thân (kích hoạt tối đa 2 lần mỗi hiệp).\n\nVới mỗi điểm Chỉ Số Nhiên Liệu nhận được, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Đột Phá Tính Năng</color> cho tất cả Vật Tạo. Khi một Vật Tạo có 10 tầng Đột Phá Tính Năng bị phá hủy, gây ST Vật Lý bằng <color=#f26c1c>100%</color> Phòng Thủ của Vật Tạo lên tất cả kẻ địch <color=#f26c1c>trong phạm vi 3 ô</color>. Đòn đánh này không kích hoạt Chặn Đánh, Phản Kích hoặc Hành Động Chi Viện."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Giao Thức Phá Hủy",
                "effect": "Tăng tầm bắn của Kỹ Năng Tháo Dỡ lên <color=#f26c1c>5 ô</color>, và áp dụng <color=#3487e0>Khe Nứt Ứng Lực</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Giao Thức Gia Cố",
                "effect": "Tăng phạm vi của Ý Thức An Toàn và Bảo Trì Tập Trung lên <color=#f26c1c>5 ô</color>.\n\nÝ Thức An Toàn nhận thêm hiệu ứng: Khi được triệu hồi, phục hồi độ bền của tất cả Vật Cản trong phạm vi 5 ô.\n\nBảo Trì Tập Trung nhận thêm hiệu ứng: Hồi phục HP bằng <color=#f26c1c>100%</color> Phòng Thủ và <color=#f26c1c>2 điểm</color> Độ Ổn Định, đồng thời áp dụng <color=#3487e0>Phòng Thủ Tăng I</color> cho tất cả đồng minh trong phạm vi 5 ô khi họ kết thúc hành động."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Nổ Chuỗi Cuồng Nộ",
                "effect": "Đặt lại hồi chiêu của Giao Thức Gia Cố và Giao Thức Phá Hủy.\n\nHồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công cho tất cả đồng minh, và áp dụng <color=#3487e0>Phụ Kiện Chịu Lực</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Giao Thức Phá Hủy",
                "effect": "Giảm hồi chiêu kỹ năng này đi <color=#f26c1c>1 hiệp</color>. Tăng Tấn Công và Phòng Thủ kế thừa của Vật Tạo Tấn Công lên thành <color=#f26c1c>100%</color>.\n\nSố lần sử dụng Kỹ Năng Tháo Dỡ mỗi hiệp tăng thêm <color=#f26c1c>1 lần</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Giao Thức Gia Cố",
                "effect": "Giảm hồi chiêu kỹ năng này đi <color=#f26c1c>1 hiệp</color>. Tăng Tấn Công và Phòng Thủ kế thừa của Vật Tạo Phòng Ngự lên thành <color=#f26c1c>100%</color>.\n\nCường hóa Ý Thức An Toàn: Khi được triệu hồi, hồi phục HP bằng <color=#f26c1c>200%</color> Phòng Thủ và <color=#f26c1c>4 điểm</color> Độ Ổn Định.\n\nCường hóa Bảo Trì Tập Trung: Hiệu ứng giảm thương được áp dụng cho tất cả đồng minh."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Hiệu Chuẩn Cờ Lê",
                "effect": "Với mỗi điểm Chỉ Số Nhiên Liệu đang giữ, tăng hệ số sát thương của Đòn Đập Băng Vụn thêm <color=#f26c1c>5%</color>.\n\nCường hóa Đột Phá Tính Năng: Tăng Tấn Công và Phòng Thủ thêm <color=#f26c1c>5%</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Không Thể Nói Ra",
                "effect": "Trước khi tung đòn tấn công chủ động, áp dụng <color=#3487e0>Khe Nứt Ứng Lực</color> lên kẻ địch trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Nôn Nóng",
                "effect": "Khi bắt đầu trận chiến, tăng <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 3 - Ý Định Bị Hiểu Lầm",
                "effect": "Khi kết thúc hành động, áp dụng <color=#3487e0>Giảm ST II</color> cho tất cả đồng minh không đứng gần Vật Cản trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 4 - Mô-đun Khắc Phục Sự Cố",
                "effect": "Khi kết thúc hành động, hồi phục <color=#f26c1c>3 điểm</color> Độ Ổn Định cho đồng minh có Độ Ổn Định thấp nhất."
            },
            {
                "name": "Khóa Cố Định 5 - Sửa Đổi Thực Tế",
                "effect": "Trước khi đồng minh bị tấn công, Vật Tạo Phòng Ngự hồi phục <color=#f26c1c>1 điểm</color> Độ Ổn Định cho họ."
            },
            {
                "name": "Khóa Cố Định 6 - Điều Khiển Cơ Khí",
                "effect": "Khi có một Vật Tạo trên sân, tăng ST Ổn Định do bản thân gây ra thêm <color=#f26c1c>3 điểm</color>."
            },
            {
                "name": "Khóa Tương Thích",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%"
            },
            {
                "name": "Khóa Chung - Thợ Rèn Thành Thạo",
                "effect": "HP +5% / Tăng Phòng Thủ cho Vật Triệu Hồi Vật Lý của người sở hữu thêm <color=#f26c1c>7%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Thép Thức Tỉnh",
                "effect": "Sau khi dùng Tuyệt Kỹ Nổ Chuỗi Cuồng Nộ, nếu kỹ năng Giao Thức Gia Cố hoặc Giao Thức Phá Hủy không trong thời gian hồi chiêu, Balthilde có thể sử dụng kỹ năng đó. Tiêu hao Chỉ Số Nhiên Liệu của Tuyệt Kỹ Nổ Chuỗi Cuồng Nộ giảm xuống còn <color=#f26c1c>4 điểm</color>.\nVật Tạo nhận thêm hiệu ứng dựa trên số tầng Đột Phá Tính Năng:\n0 tầng: Balthilde nhận 4 điểm Chỉ Số Nhiên Liệu và Vật Tạo giải trừ 1 Debuff cho các đơn vị đồng minh trong phạm vi 5 ô.\n2 tầng: Phòng Thủ của mọi đơn vị đồng minh trong phạm vi 5 ô từ Vật Tạo tăng 20% (không cộng dồn).\n5 tầng: Khi dùng Tuyệt Kỹ Nổ Chuỗi Cuồng Nộ mà có Vật Tạo trong vùng ảnh hưởng, kích hoạt hiệu ứng tử trận gây sát thương của kỹ năng bị động Hiệu Chuẩn Cờ Lê cho chúng. Mỗi tầng Đột Phá Tính Năng tăng hệ số sát thương của hiệu ứng tử trận thêm 20%."
            }
        ],
        "summons": [
            {
                "name": "Vật Tạo Phòng Ngự",
                "type": "Vật Triệu Hồi Vật Lý",
                "description": "Kế thừa các thuộc tính của Balthilde, bảo vệ đồng minh và Vật Cản trong bán kính 3 ô.",
                "stats": {
                    "hp": "100% HP ban đầu của Balthilde",
                    "atk": "80% Tấn Công ban đầu của Balthilde",
                    "def": "80% Phòng Thủ ban đầu của Balthilde"
                },
                "skills": [
                    {
                        "name": "Ý Thức An Toàn",
                        "tags": ["Bị Động", "Cường Hóa"],
                        "description": "Khi được triệu hồi, áp dụng <color=#3487e0>Phòng Thủ Tăng I</color> trong <color=#f26c1c>2 hiệp</color> và hồi phục lượng HP tương đương <color=#f26c1c>100%</color> Phòng Thủ cho tất cả đồng minh trong phạm vi 3 ô."
                    },
                    {
                        "name": "Bảo Dưỡng Tập Trung",
                        "tags": ["Bị Động", "Cường Hóa"],
                        "description": "Vật Cản trong phạm vi 3 ô sẽ không bị giảm độ bền. Giảm <color=#f26c1c>30%</color> sát thương phải chịu cho các đồng minh trong phạm vi không nhận được giảm sát thương từ Vật Cản."
                    }
                ]
            },
            {
                "name": "Vật Tạo Tấn Công",
                "type": "Vật Triệu Hồi Vật Lý",
                "description": "Kế thừa các thuộc tính của Balthilde, tấn công kẻ địch gần nhất trong bán kính 3 ô.",
                "stats": {
                    "hp": "100% HP ban đầu của Balthilde",
                    "atk": "80% Tấn Công ban đầu của Balthilde",
                    "def": "80% Phòng Thủ ban đầu của Balthilde"
                },
                "skills": [
                    {
                        "name": "Bí Quyết Tháo Dỡ",
                        "tags": ["Đánh Thường", "Chỉ Định"],
                        "description": "Chọn mục tiêu địch gần nhất trong bán kính 3 ô, gây ST Vật Lý bằng <color=#f26c1c>100%</color> Phòng Thủ. Có thể dùng 2 lần mỗi hiệp."
                    }
                ]
            }
        ]
    },
    "basti": {
        "name": "Basti",
        "en_name": "Basti",
        "class": "Hỗ Trợ",
        "phase": "Ăn Mòn",
        "rarity": "Standard",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Lon Sơn Nổi Loạn",
        "weakness": "Điện Từ",
        "server": "global",
        "skills": [
            {
                "name": "Khiêu Khích Liều Lĩnh",
                "en_name": "Reckless Provocation",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Tác Động Xấu",
                "en_name": "Bad Influence",
                "tags": ["Chủ Động", "Dịch Chuyển"],
                "description": "Chọn 1 đồng minh <color=#f26c1c>trong phạm vi 6 ô</color> sau đó chọn 1 ô địa hình Độc Chướng thân thiện, dịch chuyển đồng minh được chọn tới ô đó, hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công và <color=#f26c1c>5 điểm</color> Chỉ Số Ổn Định cho đồng minh đó, giải trừ <color=#f26c1c>2</color> Debuff và áp dụng <color=#3487e0>Duy Trì Chữa Lành II</color> trong <color=#f26c1c>2 hiệp</color>. Dịch chuyển Basti tới ô trống <color=#f26c1c>trong phạm vi 1 ô</color> quanh vị trí mới của đồng minh. Sau khi dùng kỹ năng, Basti nhận <color=#f26c1c>6 ô</color> Di Chuyển Bổ Sung."
            },
            {
                "name": "Cô Nàng Đặt Mìn",
                "en_name": "Landmine Gal",
                "tags": ["Chủ Động", "Triệu Hồi"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 6 ô</color> và triệu hồi <color=#3487e0>Cục Cưng</color> trên ô đó. Sau khi dùng kỹ năng, Basti có thể dùng tiếp kỹ năng Cô Nàng Đặt Mìn, Tác Động Xấu hoặc Tuyệt Kỹ Cạm Bẫy Bọc Đường. Kỹ năng này có thể dùng tối đa 2 lần mỗi hiệp.\n\nCục Cưng: Vật triệu hồi kế thừa các thuộc tính cơ bản của Basti. Nếu có kẻ địch trong phạm vi 3 ô khi được triệu hồi, hoặc nếu kẻ địch xuất hiện, kết thúc hành động, hoặc bị dịch chuyển vào phạm vi, Cục Cưng sẽ tự phát nổ, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định, đồng thời tạo các ô địa hình Độc Chướng trong <color=#f26c1c>2 hiệp</color>. Áp dụng Ngập Tràn Độc Tính và <color=#3487e0>Choáng</color> trong <color=#f26c1c>2 hiệp</color> cho tất cả kẻ địch trong vùng, đồng thời hồi phục HP bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định cho Basti. Tối đa tồn tại 2 Cục Cưng trên sân cùng lúc."
            },
            {
                "name": "Cạm Bẫy Bọc Đường",
                "en_name": "Sugar-Coated Trap",
                "tags": ["Tuyệt Kỹ", "Phạm Vi", "Ô Địa Hình", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>150%</color> Tấn Công lên mục tiêu đó và tất cả kẻ địch <color=#f26c1c>trong phạm vi 8 ô</color> quanh nó, tạo các ô địa hình Độc Chướng trong <color=#f26c1c>2 hiệp</color>, và áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Ghi Hận</color>."
            },
            {
                "name": "Thế Giới Graffiti",
                "en_name": "The World of Graffiti",
                "tags": ["Bị Động", "Ô Địa Hình", "Suy Yếu"],
                "description": "Khi bắt đầu hiệp, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\nKhi bắt đầu trận chiến, tạo các ô địa hình Độc Chướng trong <color=#f26c1c>2 hiệp</color> tại vị trí của tất cả búp bê đồng minh. Sau khi di chuyển, để lại các ô Độc Chướng trong bán kính <color=#f26c1c>1 ô</color> quanh bản thân trong <color=#f26c1c>2 hiệp</color>.\nNếu kẻ địch đứng trên ô Độc Chướng của đồng minh, kẻ đó nhận <color=#3487e0>Mặt Quỷ Nhăn Nhó</color>.\nKhi Cục Cưng được triệu hồi và khi bắt đầu hiệp, nếu đồng minh đứng trên ô Độc Chướng, họ nhận <color=#3487e0>Dấu Ấn Đồng Đội</color> và <color=#3487e0>Tấn Công Tăng II</color> trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Cô Nàng Đặt Mìn",
                "effect": "Tầm xa tăng thêm <color=#f26c1c>2 ô</color>. Kỹ năng này có thể dùng tối đa <color=#f26c1c>3 lần</color> mỗi hiệp.\nCường hóa Cục Cưng: Phạm vi hiệu lực tăng lên thành 5 ô, số lượng vật triệu hồi tối đa trên sân tăng lên 3."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Thế Giới Graffiti",
                "effect": "ST Ổn Định Basti phải chịu giảm đi <color=#f26c1c>1 điểm</color>.\nKhi bắt đầu trận chiến, tạo các ô Độc Chướng trong 2 hiệp tại vị trí của tất cả búp bê đồng minh và trong khu vực 3×3 xung quanh họ. Sau khi di chuyển, để lại các ô Độc Chướng trong bán kính 3 ô quanh bản thân trong 2 hiệp.\nTrước khi gây sát thương, người thi triển và Cục Cưng nhận 1 tầng <color=#3487e0>Nước Tăng Lực</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Thế Giới Graffiti",
                "effect": "Cường hóa Nước Tăng Lực: mức tăng sát thương mỗi tầng tăng lên thành <color=#f26c1c>24%</color>, và lượng trị liệu tăng lên thành <color=#f26c1c>6%</color>.\nCường hóa Dấu Ấn Đồng Đội: mức tăng sát thương gây ra tăng lên thành <color=#f26c1c>30%</color>.\nCường hóa Mặt Quỷ Nhăn Nhó: mức tăng ST Ăn Mòn phải chịu nâng lên thành <color=#f26c1c>30%</color>, và lượng HP hồi phục cho kẻ tấn công khi nhận ST Ăn Mòn tăng lên thành <color=#f26c1c>30%</color> sát thương gây ra."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Cạm Bẫy Bọc Đường",
                "effect": "Hệ số sát thương tăng lên thành <color=#f26c1c>200%</color>.\nÁp dụng thêm <color=#f26c1c>2 tầng</color> <color=#3487e0>Giải Phóng Phụ Thuộc</color>.\nSau khi dùng kỹ năng, hồi phục HP bằng <color=#f26c1c>50%</color> Tấn Công của Basti cho tất cả đồng minh, giải trừ 2 Debuff."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Cạm Bẫy Bọc Đường",
                "effect": "Số tầng Ghi Hận áp dụng tăng lên thành <color=#f26c1c>3 tầng</color>, và hệ số sát thương của nó tăng lên thành <color=#f26c1c>200%</color>.\nVới mỗi mục tiêu trúng đòn, sát thương gây ra tăng thêm <color=#f26c1c>20%</color>, tối đa tăng <color=#f26c1c>100%</color>.\nSau khi dùng kỹ năng, giải trừ thêm trạng thái <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Choáng</color> cho tất cả đồng minh."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Cô Nàng Đặt Mìn",
                "effect": "Sau khi mỗi Cục Cưng tự phát nổ, Tấn Công của Basti và Cục Cưng tăng thêm <color=#f26c1c>3%</color>.\nCường hóa Cục Cưng: Hệ số sát thương tăng lên thành <color=#f26c1c>130%</color>, và áp dụng 1 Debuff mạnh ngẫu nhiên khi gây sát thương."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Khoảnh Khắc Cảm Hứng",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 2 - Nghệ Thuật Đường Phố",
                "effect": "Khi có các ô Độc Chướng thân thiện trên sân, tất cả đơn vị đồng minh gây thêm <color=#f26c1c>7%</color> ST Ăn Mòn."
            },
            {
                "name": "Khóa Cố Định 3 - Phụ Thuộc Nỗi Đau",
                "effect": "Khi bị áp dụng Khiếp Đảm, Khiêu Khích, Dẫn Dụ, Choáng hoặc Bất Động, hiệu ứng đó ngay lập tức bị xóa bỏ (kích hoạt tối đa 1 lần mỗi trận chiến).\nKhi bắt đầu trận chiến, nhận <color=#3487e0>Phòng Thủ Tăng III</color> trong <color=#f26c1c>3 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 4 - Thiên Tài Thảm Họa",
                "effect": "Khi Cục Cưng được triệu hồi, hồi phục HP bằng <color=#f26c1c>100%</color> Tấn Công và <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho mục tiêu đồng minh có HP hiện tại thấp nhất trên sân (kích hoạt tối đa 1 lần mỗi hiệp)."
            },
            {
                "name": "Khóa Cố Định 5 - Món Quà Đáng Sợ",
                "effect": "Trước khi tấn công, Cục Cưng giải trừ <color=#f26c1c>1</color> Buff của mục tiêu."
            },
            {
                "name": "Khóa Cố Định 6 - Vệt Sơn Tình Yêu",
                "effect": "Khi Cục Cưng được triệu hồi, tạo 1 ô địa hình Độc Chướng tại ô hiện tại của nó."
            },
            {
                "name": "Khóa Tương Thích - Hat Trick",
                "effect": "Tấn Công +3%, HP +3%, Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Chiếm Hữu Chết Người",
                "effect": "Bạo Kích +5.0% / Nếu mục tiêu địch đang đứng trên ô địa hình thuộc tính Ăn Mòn, sát thương nguyên tố gây ra cho chúng tăng <color=#f26c1c>10%</color>."
            }
        ],
        "summons": [
            {
                "name": "Cục Cưng",
                "description": "Vật triệu hồi kế thừa các thuộc tính cơ bản của Basti. Nếu có kẻ địch trong phạm vi 3 ô khi được triệu hồi, Cục Cưng sẽ tự phát nổ trong khu vực."
            }
        ]
    },
    "belka": {
        "name": "Belka",
        "en_name": "Belka",
        "class": "Tiên Phong",
        "phase": "Điện Từ",
        "rarity": "Standard",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Hạt Dẻ Rực Lửa",
        "weakness": "Vật Lý",
        "server": "global",
        "skills": [
            {
                "name": "Vỏ Kẹp Hạt Dẻ",
                "en_name": "Nutcracker Shell",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Cú Nhảy Rừng Xanh",
                "en_name": "Sylvan Vault",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Tăng sát thương của đòn đánh này dựa trên (<color=#f26c1c>3%</color> × số lượng <color=#3487e0>Điện Tích Âm</color> trên sân), tối đa tăng <color=#f26c1c>15%</color>. Nếu mục tiêu là Boss và có Điện Tích Âm, sát thương tăng ngay lập tức lên mức <color=#f26c1c>15%</color>.\n\nNếu đòn đánh này Bạo Kích, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Sau khi dùng kỹ năng, chọn 1 ô trống trong phạm vi 6 ô và đáp xuống ô đó."
            },
            {
                "name": "Lõi Năng Lượng Nổ Lách Tách",
                "en_name": "Crackling Core",
                "tags": ["Chủ Động", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>130%</color> Tấn Công. Với mỗi điểm di chuyển tiêu hao, hệ số sát thương tăng thêm <color=#f26c1c>5%</color>.\n\nBelka nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Tác Chiến Tích Cực</color>. Sau khi dùng kỹ năng này, Belka có thể dùng Cú Nhảy Rừng Xanh hoặc Vỏ Kẹp Hạt Dẻ."
            },
            {
                "name": "Hồ Quang Nhảy Vọt",
                "en_name": "Leaping Arc",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây <color=#d4a017>ST Điện Từ</color> bằng <color=#f26c1c>160%</color> Tấn Công, và áp dụng <color=#3487e0>Dẫn Điện</color> trong <color=#f26c1c>1 hiệp</color>. Với mỗi điểm di chuyển tiêu hao, hệ số sát thương tăng thêm <color=#f26c1c>5%</color>. Belka nhận <color=#3487e0>Duy Trì Phóng Điện</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Bí Mật Của Rừng",
                "en_name": "Forest's Secrets",
                "tags": ["Bị Động", "Suy Yếu", "Cường Hóa"],
                "description": "Khi bắt đầu hiệp, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\n\nTrước khi tấn công, áp dụng <color=#3487e0>Điện Tích Âm</color> lên mục tiêu và kẻ địch gần nhất trong <color=#f26c1c>1 hiệp</color>. Nếu mục tiêu bị tiêu diệt, nhận <color=#3487e0>Ngụy Trang</color>.\n\nVới mỗi Điện Tích Âm do đồng minh áp dụng, tăng <color=#f26c1c>5%</color> Tỷ Lệ Bạo Kích, tối đa tăng <color=#f26c1c>30%</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Lõi Năng Lượng Nổ Lách Tách",
                "effect": "Với mỗi điểm di chuyển tiêu hao, hệ số sát thương tăng thêm <color=#f26c1c>8%</color>. Tăng <color=#f26c1c>15%</color> sát thương lên mục tiêu địch có <color=#3487e0>Điện Tích Âm</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Hồ Quang Nhảy Vọt",
                "effect": "Nhận 1 tầng <color=#3487e0>Tác Chiến Tích Cực</color>.\n\nBổ sung hiệu ứng cho Duy Trì Phóng Điện: Nếu mục tiêu của kỹ năng này trùng với mục tiêu của Duy Trì Phóng Điện trong hiệp này, áp dụng Điện Tử Tràn Đầy trong 2 hiệp trước khi tấn công."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Bí Mật Của Rừng",
                "effect": "Trước khi tấn công, áp dụng <color=#3487e0>Dẫn Điện</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>. Khi tấn công mục tiêu có <color=#3487e0>Điện Tích Âm</color>, bỏ qua <color=#f26c1c>10%</color> Phòng Thủ.\n\nKhi Belka gây ST Điện Từ đơn mục tiêu lên kẻ địch có Điện Tích Âm, tăng hệ số ST cố định gây ra bởi Điện Tích Âm lên thành <color=#f26c1c>40%</color>. Với mỗi đòn ST Điện Từ do đồng minh gây ra, Belka nhận 1 tầng Tích Điện."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Bí Mật Của Rừng",
                "effect": "Khi bắt đầu trận chiến, tăng Tốc Độ Di Chuyển và Tầm Bắn thêm <color=#f26c1c>1 ô</color>.\n\nTăng giới hạn số tầng Tích Điện thêm 4 tầng. Với mỗi đòn ST Điện Từ do bản thân gây ra, nhận thêm 1 tầng Tích Điện."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Cú Nhảy Rừng Xanh",
                "effect": "ST Ổn Định gây ra tăng thêm <color=#f26c1c>2 điểm</color>. Tăng <color=#f26c1c>30%</color> ST Bạo Kích cho đòn tấn công này.\n\nTăng sát thương của đòn đánh này dựa trên (<color=#f26c1c>6%</color> × số lượng Điện Tích Âm trên sân), tối đa tăng <color=#f26c1c>30%</color>. Nếu mục tiêu là Boss có Điện Tích Âm, sát thương tăng ngay lập tức lên mức <color=#f26c1c>30%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Hồ Quang Nhảy Vọt",
                "effect": "Với mỗi điểm di chuyển tiêu hao, hệ số sát thương tăng thêm <color=#f26c1c>10%</color>. Tăng hệ số sát thương của Duy Trì Phóng Điện thêm <color=#f26c1c>30%</color>.\n\nNếu mục tiêu có từ 2 Debuff loại Điện Từ trở lên, tăng thêm <color=#f26c1c>30%</color> ST Bạo Kích."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Năng Lượng Tràn Đầy",
                "effect": "Khi Ngụy Trang kết thúc, Belka hồi phục HP bằng <color=#f26c1c>30%</color> HP tối đa và <color=#f26c1c>4 điểm</color> Độ Ổn Định."
            },
            {
                "name": "Khóa Cố Định 2 - Nước Mắt Công Kích",
                "effect": "Nếu Belka có Duy Trì Phóng Điện, cô ấy miễn nhiễm với các hiệu ứng dịch chuyển vị trí."
            },
            {
                "name": "Khóa Cố Định 3 - Khuấy Động Không Khí",
                "effect": "Khi bắt đầu hiệp, nếu có kẻ địch trong bán kính 5 ô xung quanh, nhận <color=#3487e0>Di Chuyển Tăng I</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 4 - Chiếc Đuôi Dựng Đứng",
                "effect": "Lõi Năng Lượng Nổ Lách Tách: Khi dùng kỹ năng này tấn công mục tiêu có Điện Tích Âm, Tấn Công tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Lời Khen Mong Muốn",
                "effect": "Khi kết thúc hành động, nếu có Boss mang Điện Tích Âm, nhận <color=#3487e0>Tăng Tỷ Lệ Bạo Kích I</color> và <color=#3487e0>ST Tăng I</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 6 - Động Lực Quyết Định",
                "effect": "Hồ Quang Nhảy Vọt: Trước khi sử dụng kỹ năng này, giải trừ <color=#f26c1c>2</color> Buff của mục tiêu."
            },
            {
                "name": "Khóa Tương Thích",
                "effect": "Tấn Công +3%, HP +3%, Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Tranh Đoạt Ân Huệ",
                "effect": "Tấn Công +5% / Nếu có tiêu hao điểm di chuyển, sát thương gây ra tăng <color=#f26c1c>10%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Quyết Tâm Của Sóc Nhỏ",
                "effect": "Cú Nhảy Rừng Xanh chuyển sang gây <color=#d4a017>ST Điện Từ</color>. Tăng ST Bạo Kích của đòn đánh này thêm <color=#f26c1c>5%</color> cho mỗi đồng minh mang Điện Tích Dương, tối đa tăng <color=#f26c1c>25%</color>.\n\nKhi dùng Lõi Năng Lượng Nổ Lách Tách hoặc Hồ Quang Nhảy Vọt, nếu Belka di chuyển ít hơn 10 ô, khoảng cách di chuyển được tính là 10 ô."
            }
        ]
    },
    "cheyanne": {
        "name": "Cheyanne",
        "en_name": "Cheyanne",
        "class": "Tiên Phong",
        "phase": "Vật Lý",
        "rarity": "Standard",
        "weapon_type": "Súng Bắn Tỉa",
        "ammo_type": "Đạn Nặng",
        "signature_weapon": "Bông Hoa Đẽo Gọt",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Khai Mở Tiềm Năng",
                "en_name": "Playing to Potential",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trên toàn bản đồ</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Bức Tường Nội Tâm",
                "en_name": "Wall of One's Self",
                "tags": ["Chủ Động", "Ô Địa Hình"],
                "description": "Cheyanne nhận <color=#3487e0>Đài Hoa E Thẹn</color> và <color=#f26c1c>1 lần</color> <color=#3487e0>Chỉ Lệnh Bổ Sung</color>.\n\nKhi nhận sát thương chí tử trong lúc có Đài Hoa E Thẹn, Cheyanne sẽ không bị hạ gục, thay vào đó rải các ô địa hình <color=#3487e0>Khói</color> trong bán kính <color=#f26c1c>1 ô</color> quanh vị trí của cô ấy trong <color=#f26c1c>1 hiệp</color>. Khi đứng trên các ô Khói này, Cheyanne trở nên bất tử. Kích hoạt 1 lần mỗi trận chiến."
            },
            {
                "name": "Kiên Trì Truy Kích",
                "en_name": "Steadfast Pursuit",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trên toàn bản đồ</color>, áp dụng <color=#3487e0>Tâm Bia</color> lên kẻ đó và gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Xuyên Mây Hướng Dương",
                "en_name": "Piercing the Clouds, Into the Sun",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trên toàn bản đồ</color>, gây ST Vật Lý bằng <color=#f26c1c>200%</color> Tấn Công và đặt lại <color=#3487e0>Giá Trị Phân Tích</color> của nó. Nếu mục tiêu mang <color=#3487e0>Tâm Bia</color>, ST Bạo Kích tăng thêm <color=#f26c1c>30%</color>."
            },
            {
                "name": "Tính Toán Chu Toàn",
                "en_name": "Meticulous Planning",
                "tags": ["Bị Động", "Chỉ Định"],
                "description": "Khi một đơn vị địch kết thúc lượt đi, Cheyanne kích hoạt Cân Nhắc Kỹ Lưỡng, gây ST Vật Lý bằng <color=#f26c1c>120%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định lên kẻ địch đó, đồng thời tăng <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Nếu <color=#3487e0>Giá Trị Phân Tích</color> của mục tiêu vượt quá <color=#f26c1c>50%</color>, hệ số sát thương của đòn đánh này tăng lên thành <color=#f26c1c>180%</color>. Có thể kích hoạt tối đa 2 lần mỗi hiệp.\n\nÁp dụng <color=#f26c1c>100%</color> Giá Trị Phân Tích cho tất cả đơn vị địch khi bắt đầu trận chiến.\n\nSát thương gây ra lên các đơn vị bay tăng thêm <color=#f26c1c>20%</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Tính Toán Chu Toàn",
                "effect": "Với mỗi <color=#f26c1c>10%</color> Giá Trị Phân Tích mà mục tiêu nắm giữ khi gây sát thương, ST Bạo Kích tăng thêm <color=#f26c1c>5%</color>.\nCải thiện hiệu ứng của Giá Trị Phân Tích: Hiệu ứng bỏ qua Chỉ Số Ổn Định của mục tiêu được tăng lên tương ứng thành <color=#f26c1c>10 điểm</color> và <color=#f26c1c>5 điểm</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Xuyên Mây Hướng Dương",
                "effect": "Hệ số sát thương tăng lên thành <color=#f26c1c>280%</color>. Nếu mục tiêu mang <color=#3487e0>Tâm Bia</color>, bỏ qua <color=#f26c1c>50%</color> Phòng Thủ của nó."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Kiên Trì Truy Kích",
                "effect": "Cải thiện hiệu ứng Tâm Bia: Mức giảm Phòng Thủ tăng lên thành <color=#f26c1c>100%</color>; khi bị Cheyanne tấn công, không còn tiêu hao Giá Trị Phân Tích."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Bức Tường Nội Tâm",
                "effect": "Với mỗi 1 hiệp ở trạng thái Đài Hoa E Thẹn, Cheyanne nhận 1 tầng <color=#3487e0>Cảm Giác An Toàn</color> khi kết thúc hiệp.\nThời gian tồn tại của các ô Khói tăng lên thành <color=#f26c1c>2 hiệp</color>, và phạm vi mở rộng thêm <color=#f26c1c>1 ô</color>.\nThời gian hồi chiêu giảm đi <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Xuyên Mây Hướng Dương",
                "effect": "Hệ số sát thương tăng lên thành <color=#f26c1c>330%</color>. Khi gây sát thương, nếu trên sân có từ 3 đơn vị địch trở xuống có Giá Trị Phân Tích dưới 50%, hệ số sát thương tăng lên thành <color=#f26c1c>380%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Tính Toán Chu Toàn",
                "effect": "Hệ số sát thương của Cân Nhắc Kỹ Lưỡng tăng lên thành <color=#f26c1c>160%</color>. Nếu gây sát thương lên đơn vị địch có Giá Trị Phân Tích từ 50% trở lên trong hiệp này, hệ số sát thương tăng lên thành <color=#f26c1c>220%</color>.\nKhi Cân Nhắc Kỹ Lưỡng gây sát thương, nhận 1 tầng <color=#3487e0>Tích Lũy Làm Nóng</color>, tối đa 1 lần mỗi hiệp."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Đừng Lại Gần, Tôi Ngại Lắm",
                "effect": "Khi gây sát thương chuẩn xác, đẩy lùi mục tiêu <color=#f26c1c>2 ô</color> và áp dụng <color=#3487e0>Di Chuyển Giảm II</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Bản Thân Tự Do",
                "effect": "Cheyanne miễn nhiễm với các hiệu ứng Khiêu Khích, Dẫn Dụ và Khiếp Đảm.\nCứ mỗi 3 hiệp, nhận miễn nhiễm với sát thương diện rộng AoE 1 lần."
            },
            {
                "name": "Khóa Cố Định 3 - Bước Tiến Dũng Cảm",
                "effect": "Khi bắt đầu trận chiến, Tầm Di Chuyển tăng thêm <color=#f26c1c>2 ô</color> trong 1 hiệp. Tạo 1 Điểm Cao tại ô trống gần nhất quanh bản thân."
            },
            {
                "name": "Khóa Cố Định 4 - Khép Kín",
                "effect": "Khi một đơn vị địch mang Tâm Bia tử trận, áp dụng Tâm Bia lên 1 kẻ địch có lượng HP hiện tại cao nhất trên sân."
            },
            {
                "name": "Khóa Cố Định 5 - Ý Chí Kiên Định",
                "effect": "Sát thương gây ra lên mục tiêu mang Tâm Bia tăng <color=#f26c1c>10%</color>, và được tính là điểm yếu Đạn Nặng."
            },
            {
                "name": "Khóa Cố Định 6 - Toàn Tâm Toàn Ý",
                "effect": "Mỗi hiệp, chỉ khi mục tiêu mang Tâm Bia kết thúc hành động, tung Cân Nhắc Kỹ Lưỡng 1 lần lên kẻ đó. Hệ số sát thương và ST Ổn Định được cộng dồn theo tổng số lần thi triển Cân Nhắc Kỹ Lưỡng khả dụng trong hiệp (mặc định là 2 lần). Hồi phục 2 điểm Chỉ Số Nhiên Liệu. Kích hoạt tối đa 1 lần mỗi hiệp."
            },
            {
                "name": "Khóa Tương Thích - Hồi Hộp Mong Đợi",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Cuộc Tái Ngộ Đợi Chờ",
                "effect": "Tấn Công +5.0% / Sát thương gây ra lên các mục tiêu có HP hiện tại cao hơn bản thân tăng <color=#f26c1c>10%</color>."
            }
        ]
    },
    "dushevnaya": {
        "name": "Dushevnaya",
        "en_name": "Dushevnaya",
        "class": "Hỗ Trợ",
        "phase": "Băng Kết",
        "rarity": "Standard",
        "weapon_type": "Súng Trường Tấn Công",
        "ammo_type": "Đạn Trung",
        "signature_weapon": "Thơ Ca Mùa Đông",
        "weakness": "Vật Lý",
        "server": "global",
        "skills": [
            {
                "name": "Bình Minh",
                "en_name": "Daybreak",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Quy Tắc Anh Hùng",
                "en_name": "Hero's Code",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>110%</color> Tấn Công lên mục tiêu. Nếu đòn đánh này tiêu diệt một đơn vị địch đang chịu Debuff Băng Kết, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Chúc Phúc Hàn Băng</color>."
            },
            {
                "name": "Trừng Phạt Của Marzanna",
                "en_name": "Marzanna's Sanction",
                "tags": ["Chủ Động", "Suy Yếu", "Ô Địa Hình"],
                "description": "Chọn 1 ô <color=#f26c1c>trong phạm vi 6 ô</color>, gây <color=#42cce0>ST Băng Kết</color> AoE bằng <color=#f26c1c>50%</color> Tấn Công lên tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 2 ô</color> quanh ô được chọn, và tạo ra các ô địa hình Băng Giá trong <color=#f26c1c>2 hiệp</color>.\n\nLần sử dụng tiếp theo của kỹ năng này sẽ được cường hóa, tăng hệ số sát thương lên <color=#f26c1c>70%</color>, đồng thời áp dụng <color=#3487e0>Hàn Ý</color> trong <color=#f26c1c>1 hiệp</color>. Cường hóa này không thể cộng dồn nếu kỹ năng đã được cường hóa.\n\nNếu Chỉ Số Nhiên Liệu đạt tối đa, Trừng Phạt Của Marzanna có thể được dùng lại ngay lập tức."
            },
            {
                "name": "Sách Tiên Tri",
                "en_name": "Book of Prophecy",
                "tags": ["Tuyệt Kỹ", "Cường Hóa", "Hỗ Trợ"],
                "description": "Áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Lời Chúc Cực Hàn</color> cho tất cả đơn vị đồng minh <color=#f26c1c>trong phạm vi 7 ô</color>. Nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu, đồng thời nhận <color=#3487e0>Lĩnh Vực Cực Hàn</color> trong <color=#f26c1c>2 hiệp</color>. Khi Lĩnh Vực Cực Hàn đang kích hoạt, nếu Chỉ Số Nhiên Liệu ở mức 0 khi kết thúc hành động, nhận lại <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Tác Phẩm Được Ban Phước",
                "en_name": "Blessed Artwork",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Tăng sát thương cho tất cả đơn vị đồng minh thêm <color=#f26c1c>10%</color>, với mức tăng riêng biệt thêm <color=#f26c1c>10%</color> cho <color=#42cce0>ST Băng Kết</color>. Khi kết thúc hành động, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.\n\nKhi HP của bản thân trên <color=#f26c1c>80%</color>, giảm ST Ổn Định phải chịu đi <color=#f26c1c>1 điểm</color> và nhận <color=#3487e0>Thấu Suốt</color>. Trong thời gian có hiệu ứng Thấu Suốt, tầm hiệu lực của các kỹ năng chủ động và Tấn Công Chi Viện (ngoại trừ Tuyệt Kỹ) tăng thêm <color=#f26c1c>1 ô</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Sách Tiên Tri",
                "effect": "Tăng tầm hiệu lực thêm <color=#f26c1c>2 ô</color>, đồng thời áp dụng 1 Buff mạnh ngẫu nhiên và <color=#3487e0>Di Chuyển Tăng II</color> cho tất cả đơn vị đồng minh trong phạm vi trong <color=#f26c1c>2 hiệp</color>. Lời Chúc Cực Hàn tăng sát thương gây ra thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tác Phẩm Được Ban Phước",
                "effect": "Các đòn tấn công bỏ qua <color=#f26c1c>15%</color> giảm thương từ Vật Cản của mục tiêu. Khi bắt đầu hành động, tạo các ô địa hình Băng Giá trong bán kính <color=#f26c1c>1 ô</color> quanh bản thân trong <color=#f26c1c>2 hiệp</color>. Nếu bản thân đứng trên ô Băng Giá của đồng minh, ST Ổn Định gây ra tăng thêm <color=#f26c1c>1 điểm</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Trừng Phạt Của Marzanna",
                "effect": "Tầm hiệu lực tăng thêm <color=#f26c1c>1 ô</color>. Hệ số sát thương ban đầu tăng lên thành <color=#f26c1c>70%</color>. Mức này tăng lên thành <color=#f26c1c>90%</color> đối với kỹ năng được cường hóa."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Quy Tắc Anh Hùng",
                "effect": "Số tầng Chúc Phúc Hàn Băng nhận được tăng thêm 1. Khi số tầng đạt 4, hiệu ứng kỹ năng được cường hóa, tăng sát thương gây ra lên <color=#f26c1c>140%</color>. Nếu mục tiêu đứng trên ô Băng Giá của đồng minh, sát thương tăng lên thành <color=#f26c1c>160%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Sách Tiên Tri",
                "effect": "Giải trừ 1 Buff từ 4 kẻ địch ngẫu nhiên trong phạm vi. Số tầng Lời Chúc Cực Hàn áp dụng tăng thêm 1 tầng. Khi Lĩnh Vực Cực Hàn đang kích hoạt, bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu, số lần Tấn Công Chi Viện tối đa tăng thêm 1 lần."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Tác Phẩm Được Ban Phước",
                "effect": "Tăng sát thương của các đòn tấn công chủ động thêm <color=#f26c1c>20%</color>, kèm theo mức tăng thêm <color=#f26c1c>40%</color> riêng cho ST Băng Kết. Sau đòn tấn công chủ động, giải trừ 1 Buff loại phòng ngự trên mục tiêu. Nếu người dùng đứng trên ô Băng Giá của đồng minh, áp dụng <color=#3487e0>Dễ Bị Thương II</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Ngọn Giáo Longinus",
                "effect": "Mỗi tầng Chúc Phúc Hàn Băng vượt quá giới hạn tối đa sẽ tăng Tỷ Lệ Bạo Kích của Quy Tắc Anh Hùng thêm <color=#f26c1c>5%</color>, tối đa tăng <color=#f26c1c>30%</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Ý Chí Nhà Thám Hiểm",
                "effect": "Khi đòn tấn công chủ động chỉ đánh trúng 1 mục tiêu, tăng <color=#f26c1c>20%</color> ST Băng Kết gây ra và tăng <color=#f26c1c>2 điểm</color> ST Ổn Định."
            },
            {
                "name": "Khóa Cố Định 3 - Hỗ Trợ Ma Pháp",
                "effect": "Khi kỹ năng chủ động tạo ô địa hình Băng Giá, nếu đã có ô Băng Giá trong phạm vi, kích hoạt phản ứng địa hình, xóa các ô dưới chân kẻ địch và giải trừ 1 Buff của chúng. Với mỗi ô bị xóa, nhận 1 tầng Chúc Phúc Hàn Băng (tối đa 3 tầng)."
            },
            {
                "name": "Khóa Cố Định 4 - Đại Đao Dũng Cảm",
                "effect": "Khi dùng Trừng Phạt Của Marzanna, nếu làm mục tiêu rơi vào trạng thái Sụp Đổ Ổn Định, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên chúng trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Trái Tim Hiền Triết",
                "effect": "Khi đang có hiệu ứng Lĩnh Vực Cực Hàn, miễn nhiễm với các Debuff loại Di Chuyển."
            },
            {
                "name": "Khóa Cố Định 6 - Ánh Sáng Thánh",
                "effect": "Khi bắt đầu hiệp, nếu đơn vị này đang đứng trên ô Băng Giá của đồng minh, giải trừ 2 Debuff."
            },
            {
                "name": "Khóa Tương Thích - Ký Ức Lấp Lánh",
                "effect": "Tấn Công +3%, HP +3%, Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Cảm Hứng Nghệ Thuật",
                "effect": "Tấn Công +5.0% / Với các mục tiêu có Tầm Di Chuyển nhỏ hơn hoặc bằng người dùng hoặc không thể di chuyển, tăng <color=#f26c1c>10%</color> sát thương nguyên tố gây ra."
            },
            {
                "name": "Khóa Mở Rộng - Khúc Hát Mùa Đông Của Anh Hùng",
                "effect": "Khi đồng minh gây ST Băng Kết, nhận 1 tầng Chúc Phúc Hàn Băng, và tăng <color=#f26c1c>5%</color> ST Băng Kết cho tất cả đồng minh (tối đa 15%).\n\nCác đòn tấn công đơn mục tiêu của Dushevnaya chuyển thành gây <color=#42cce0>ST Băng Kết</color>, bỏ qua 30% Phòng Thủ của kẻ địch, và tăng 30% ST Băng Kết gây ra cho kẻ địch.\n\nKhi bắt đầu trận chiến, tăng 10% sát thương và tăng 10% ST Băng Kết cho 2 đồng minh có Tấn Công cao nhất (ngoại trừ bản thân)."
            }
        ]
    },
    "faye": {
        "name": "Faye",
        "en_name": "Faye",
        "class": "Tiên Phong",
        "phase": "Vật Lý",
        "rarity": "Standard",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Chiếc Rìu Lấp Lánh",
        "weakness": "Thiêu Đốt",
        "server": "global",
        "skills": [
            {
                "name": "Bắn Tập",
                "en_name": "Practice Shot",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Xoáy Rìu Tàn Phá",
                "en_name": "Ruinous Whirl",
                "tags": ["Chủ Động", "Phạm Vi", "Suy Yếu"],
                "description": "Tiêu hao toàn bộ Chỉ Số Nhiên Liệu. Với mỗi điểm Chỉ Số Nhiên Liệu tiêu hao, Faye áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Vết Thương</color> lên tất cả đơn vị địch <color=#f26c1c>trong phạm vi 3 ô</color>, kéo chúng lại gần bản thân <color=#f26c1c>2 ô</color>, và gây ST Vật Lý AoE bằng <color=#f26c1c>80%</color> Tấn Công, đồng thời áp dụng <color=#3487e0>Cấm Di Chuyển</color> trong <color=#f26c1c>1 hiệp</color>.\n\nFaye nhận <color=#f26c1c>8 ô</color> Di Chuyển Bổ Sung và trạng thái <color=#3487e0>Di Hình</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Ánh Lửa Phân Tách",
                "en_name": "Fissioned Firelight",
                "tags": ["Chủ Động", "Chỉ Định", "Suy Yếu"],
                "description": "Faye nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu. Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, áp dụng <color=#f26c1c>2 tầng</color> <color=#3487e0>Vết Thương</color> lên kẻ đó, và gây ST Vật Lý bằng <color=#f26c1c>120%</color> Tấn Công."
            },
            {
                "name": "Tuyệt Diệt",
                "en_name": "No Survivors",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>. Áp dụng số tầng <color=#3487e0>Liệt Thương</color> bằng đúng số tầng Vết Thương lên tất cả kẻ địch có mang Vết Thương <color=#f26c1c>trong phạm vi 6 ô</color>, và gây ST Vật Lý bằng <color=#f26c1c>160%</color> Tấn Công.\n\nNếu mục tiêu địch mang từ <color=#f26c1c>6 tầng Vết Thương trở lên</color>, tiêu hao 6 tầng Vết Thương trên mục tiêu để tăng sát thương mục tiêu phải chịu từ đòn đánh này thêm <color=#f26c1c>120%</color>."
            },
            {
                "name": "Liên Hoàn Rìu Chiến",
                "en_name": "Tomahawk Combo",
                "tags": ["Bị Động", "Suy Yếu"],
                "description": "Khi tấn công, Faye bỏ qua một lượng Phòng Thủ của mục tiêu bằng (<color=#f26c1c>2%</color> × số tầng Vết Thương) và hồi phục HP bằng <color=#f26c1c>10%</color> HP tối đa + (<color=#f26c1c>2%</color> × số tầng Vết Thương).\n\nKhi kết thúc hành động của một đơn vị địch, nếu nó ở <color=#f26c1c>trong phạm vi 6 ô</color>, Faye ném rìu vào nó, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Vết Thương</color> lên nó, và gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công cùng <color=#f26c1c>2 điểm</color> ST Ổn Định. Nếu kẻ địch ở <color=#f26c1c>trong phạm vi 3 ô</color>, Faye chuyển sang xoay rìu chém; nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu, áp dụng <color=#f26c1c>2 tầng</color> Vết Thương lên tất cả kẻ địch trong phạm vi 3 ô, và gây ST Vật Lý AoE bằng <color=#f26c1c>60%</color> Tấn Công cùng <color=#f26c1c>1 điểm</color> ST Ổn Định. Hiệu ứng này có thể kích hoạt tối đa 2 lần mỗi hiệp."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Liên Hoàn Rìu Chiến",
                "effect": "Lượng Phòng Thủ bỏ qua trên mỗi tầng Vết Thương tăng thêm <color=#f26c1c>2%</color>.\n\nKhi kết thúc hành động của một đơn vị địch, nếu nó mang từ 2 tầng Vết Thương trở lên, Faye áp dụng 2 tầng Vết Thương lên đơn vị địch gần nhất."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Ánh Lửa Phân Tách",
                "effect": "Hệ số sát thương tăng thêm <color=#f26c1c>20%</color>. Nếu mục tiêu địch mang từ 4 tầng Vết Thương trở lên sau khi Faye dùng kỹ năng này, Faye áp dụng thêm số tầng Liệt Thương bằng đúng số tầng Vết Thương lên nó."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Liên Hoàn Rìu Chiến",
                "effect": "Khi kết thúc hành động của Faye, thực hiện 1 lần xoay rìu và áp dụng <color=#3487e0>Cấm Di Chuyển</color> cho tất cả kẻ địch trong khu vực trong <color=#f26c1c>1 hiệp</color>. Sát thương gây ra bởi đòn tấn công này tăng thêm <color=#f26c1c>30%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tuyệt Diệt",
                "effect": "Hiệu ứng áp dụng Liệt Thương cho tất cả kẻ địch có Vết Thương quanh Faye đổi thành: Áp dụng <color=#f26c1c>4 tầng</color> Liệt Thương cho tất cả kẻ địch trên chiến trường. Với những kẻ địch đã có Vết Thương, áp dụng thêm số tầng Liệt Thương bằng đúng số tầng Vết Thương.\n\nKhi kết thúc hành động của Faye, kích hoạt toàn bộ số tầng Liệt Thương nhưng không tiêu hao số tầng Liệt Thương đó."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Xoáy Rìu Tàn Phá",
                "effect": "Hệ số sát thương tăng thêm <color=#f26c1c>20%</color>. Thời gian duy trì của Cấm Di Chuyển và Di Hình tăng thêm <color=#f26c1c>1 hiệp</color>.\n\nSau khi dùng kỹ năng này, Faye giải trừ toàn bộ các Debuff loại Phòng Thủ và Di Chuyển trên bản thân."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Tuyệt Diệt",
                "effect": "Hiệu ứng khi mục tiêu mang từ 6 tầng Vết Thương trở lên đổi thành: Tiêu hao 6 tầng Vết Thương. Với mỗi tầng Vết Thương mục tiêu đang giữ, sát thương phải chịu từ đòn đánh này tăng thêm <color=#f26c1c>20%</color>, tối đa tăng <color=#f26c1c>160%</color>. Mỗi tầng Vết Thương tăng Tỷ Lệ Bạo Kích cho đòn đánh này thêm <color=#f26c1c>5%</color> và ST Bạo Kích thêm <color=#f26c1c>2%</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Theo Dấu Mùi Hương",
                "effect": "Với mỗi đơn vị mang Vết Thương trên sân, tăng Tầm Di Chuyển của Faye thêm <color=#f26c1c>1 ô</color>, tối đa tăng <color=#f26c1c>3 ô</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Nhát Chém Tất Tay",
                "effect": "Khi kỹ năng chủ động Xoáy Rìu Tàn Phá chỉ đánh trúng 1 đơn vị địch, sát thương gây ra tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "name": "Khóa Cố Định 3 - Vật Phẩm Cứu Trợ Khẩn Cấp",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 4 - Kế Hoạch Khẩn Cấp",
                "effect": "Khi HP của Faye thấp hơn 50%, hiệu quả trị liệu nhận được tăng thêm <color=#f26c1c>30%</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Bảo Vệ Lúc Nguy Cấp",
                "effect": "Khi kết thúc hành động của Faye, nếu có đơn vị địch mang Vết Thương trong phạm vi 2 ô, Faye nhận Phòng Thủ AoE I trong 1 hiệp."
            },
            {
                "name": "Khóa Cố Định 6 - Trong Cuộc Hỗn Chiến",
                "effect": "Khi một đơn vị địch có Liệt Thương tử trận, Tấn Công của Faye tăng thêm <color=#f26c1c>4%</color>, tối đa tăng <color=#f26c1c>20%</color>."
            },
            {
                "name": "Khóa Tương Thích",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Quyết Đấu Sinh Tử",
                "effect": "Bạo Kích +5.0% / Sát thương Vật Lý mà các đơn vị địch trong phạm vi 3 ô phải chịu tăng <color=#f26c1c>5%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Cuồng Bạo Tột Cùng",
                "effect": "Khi gây sát thương lên kẻ địch có <color=#3487e0>Liệt Thương</color>, bỏ qua <color=#f26c1c>50%</color> Phòng Thủ của mục tiêu và tăng Tấn Công thêm <color=#f26c1c>15%</color>.\n\nTuyệt Diệt: Sau khi sử dụng kỹ năng, áp dụng <color=#f26c1c>2 tầng</color> <color=#3487e0>Vết Thương</color> lên mục tiêu.\n\nSau khi dùng Phi Rìu hoặc Xoay Rìu, áp dụng <color=#3487e0>Cấm Di Chuyển</color> trong <color=#f26c1c>1 hiệp</color>."
            }
        ]
    }
}

def main():
    print(f"Loading {I18N_PATH}...")
    with open(I18N_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    chars = data.setdefault("characters", {})

    updated_count = 0
    for slug, payload in BATCH_2_DATA.items():
        if slug in chars:
            # Preserve existing avatar/portrait or other keys if present
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

    # Use stage_i18n_bundle inside RepositoryTransaction with effects_data
    print(f"\nStaging i18n bundle across repository...")
    effects_path = ROOT / "data" / "effects_vi.json"
    effects_data = json.loads(effects_path.read_text(encoding="utf-8"))
    with RepositoryTransaction(ROOT) as tx:
        stage_i18n_bundle(ROOT, tx, data, effects_data=effects_data)
        tx.commit()

    print(f"Successfully applied accurate Batch 2 translations for {updated_count} characters!")

if __name__ == "__main__":
    main()
