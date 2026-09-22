#!/usr/bin/env python3
"""
tools/patch_15_fortifications.py
Accurately updates the Vietnamese fortification (Cường Hóa Tâm Trí) data for 15 dolls:
  eagletta, florence, helen, jiangyu, lewis, lind, liushih, loreley, mechty,
  mityl, ots-14, qiuhua, sakura, sextans, zhaohui.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_core.bundle import stage_i18n_bundle
from tools.effects_catalog import canonicalize_effects, browser_catalog

I18N_PATH = ROOT / "data" / "i18n_vi.json"

FORTIFICATIONS_DATA = {
    "eagletta": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Bản Năng Hoang Dã",
            "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Đe Dọa Xâm Lấn</color>. Khi sở hữu <color=#f26c1c>1 tầng</color> <color=#3487e0>Đe Dọa Xâm Lấn</color>, sử dụng đòn đánh thường Móng Vuốt Xé Rách và kỹ năng nội tại Săn Mồi nhận thêm <color=#f26c1c>1</color> Lông Vũ Chiến Trận. Khi sở hữu từ <color=#f26c1c>2 tầng</color> <color=#3487e0>Đe Dọa Xâm Lấn</color> trở lên, vào cuối hiệp, thời gian hồi chiêu của tuyệt kỹ Vũ Điệu Bão Lông Vũ giảm <color=#f26c1c>1 hiệp</color>. Nếu đòn đánh thường Ưng Kích Chớp Nhoáng hạ gục mục tiêu, nhận <color=#f26c1c>2</color> Lông Vũ Chiến Trận."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Chiến Thuật Uy Nhiếp",
            "effect": "Bổ sung hiệu ứng nội tại: Vào cuối hiệp, nếu số lần Khóa Tấn Công của kỹ năng nội tại Bản Năng Hoang Dã chưa đạt giới hạn, nhận <color=#f26c1c>2</color> Lông Vũ Chiến Trận cho mỗi lần dùng còn lại. Hệ số sát thương của đòn đánh thường Ưng Kích Chớp Nhoáng tăng lên <color=#f26c1c>120%</color>, mức tăng sát thương gây ra nâng lên <color=#f26c1c>25%</color> và sát thương bạo kích tăng thêm nâng lên <color=#f26c1c>10%</color>. Hệ số sát thương của đòn đánh thường Móng Vuốt Xé Rách và kỹ năng nội tại Săn Mồi tăng lên <color=#f26c1c>80%</color>."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Cú Bổ Nhào Băng Giá",
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>120%</color>. Phạm vi áp dụng <color=#3487e0>Nữ Hoàng Bầu Trời</color> mở rộng thành phạm vi <color=#f26c1c>5 ô</color> quanh bản thân. Cường hóa hiệu ứng <color=#3487e0>Nữ Hoàng Bầu Trời</color>: Mức giảm sát thương của đòn tấn công đầu tiên nhắm vào Eagletta tăng lên <color=#f26c1c>40%</color>."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Vũ Điệu Bão Lông Vũ",
            "effect": "Khi tiêu hao <color=#f26c1c>1</color> Lông Vũ Chiến Trận, mức tăng sát thương gây ra nâng lên <color=#f26c1c>30%</color>.\nKhi tiêu hao <color=#f26c1c>2</color> Lông Vũ Chiến Trận, mức tăng sát thương bạo kích nâng lên <color=#f26c1c>45%</color>.\nKhi tiêu hao <color=#f26c1c>3</color> Lông Vũ Chiến Trận, mức tăng hệ số sát thương nâng lên <color=#f26c1c>80%</color> và mức tăng Tấn Công nâng lên <color=#f26c1c>20%</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Bản Năng Hoang Dã",
            "effect": "Số lượng Lông Vũ Chiến Trận cần thiết để nhận <color=#3487e0>Đe Dọa Xâm Lấn</color> giảm xuống còn <color=#f26c1c>3</color>."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Chiến Thuật Uy Nhiếp",
            "effect": "Bổ sung hiệu ứng nội tại: Khi tuyệt kỹ Vũ Điệu Bão Lông Vũ tiêu hao <color=#f26c1c>3</color> Lông Vũ Chiến Trận, hệ số sát thương tăng thêm <color=#f26c1c>30%</color>. Hiệu ứng này cũng áp dụng cho hiệu ứng kỹ năng Vũ Điệu Bão Lông Vũ được kích hoạt khi dùng đòn đánh thường Ưng Kích Chớp Nhoáng lúc đang có <color=#f26c1c>4 tầng</color> <color=#3487e0>Đe Dọa Xâm Lấn</color>. Với mỗi tầng <color=#3487e0>Đe Dọa Xâm Lấn</color>, sát thương bản thân gây ra tăng thêm <color=#f26c1c>10%</color>; khi một đơn vị địch chịu sát thương từ đơn vị đồng minh, nếu đứng trên ô địa hình <color=#42cce0>Băng Kết</color>, sát thương phải chịu tăng thêm <color=#f26c1c>10%</color> cho mỗi tầng <color=#3487e0>Đe Dọa Xâm Lấn</color>.\nMức tăng Tấn Công từ tư thế Ưng Kích tăng thêm <color=#f26c1c>20%</color>.\nHệ số sát thương của đòn đánh thường Ưng Kích Chớp Nhoáng tăng lên <color=#f26c1c>150%</color>, mức tăng sát thương gây ra nâng lên <color=#f26c1c>40%</color> và mức tăng sát thương bạo kích nâng lên <color=#f26c1c>15%</color>.\nTỷ lệ bỏ qua Phòng Thủ của đòn đánh thường Móng Vuốt Xé Rách và kỹ năng nội tại Săn Mồi tăng lên <color=#f26c1c>10%</color>. Khi Lông Vũ Chiến Trận được tiêu hao bởi tư thế Trọng Trảo, mức tăng hệ số sát thương cho đòn đánh thường Móng Vuốt Xé Rách và kỹ năng nội tại Săn Mồi nâng lên <color=#f26c1c>10%</color>."
        }
    ],
    "florence": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Chuẩn Bị Phẫu Thuật",
            "effect": "Giảm tiêu hao Chỉ Số Nhiên Liệu đi <color=#f26c1c>1 điểm</color>.\n\nTăng số lần Phản Kích thông qua kỹ năng nội tại của Arios thêm <color=#f26c1c>2 lần</color>."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Ảo Giác Khổ Dâm",
            "effect": "Cường hóa hiệu ứng <color=#3487e0>Chất Nhiễu Loạn</color>: Tăng <color=#f26c1c>15%</color> <color=#2caadb>ST Hóa Lỏng</color> phải chịu.\n\nBổ sung hiệu ứng mới - Gây <color=#e08834>ST Vật Lý</color> lên toàn bộ đơn vị khi bắt đầu hiệp."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Kích Hoạt Khoái Cảm",
            "effect": "Tăng thời gian duy trì của <color=#3487e0>Thuốc Phấn Khởi</color> thêm <color=#f26c1c>1 hiệp</color> (Thời lượng giảm vào cuối hiệp hiện tại).\n\nBổ sung hiệu ứng mới - Khi kết thúc hành động, nếu HP dưới <color=#f26c1c>30%</color>, hồi phục lượng HP bằng <color=#f26c1c>100%</color> Tấn Công của Florence. Hiệu ứng này chỉ có thể kích hoạt 1 lần trong suốt thời gian duy trì của Thuốc Phấn Khởi."
        },
        {
            "tier": 4,
            "level": 3,
            "skill": "Ảo Giác Khổ Dâm",
            "effect": "Tăng hệ số sát thương thêm <color=#f26c1c>20%</color>. Nếu Arios đang có mặt trên sân, hồi phục cho Florence lượng HP bằng <color=#f26c1c>100%</color> Tấn Công và áp dụng <color=#3487e0>Adrenaline</color> trong <color=#f26c1c>1 hiệp</color> (Thời lượng giảm vào cuối hiệp hiện tại)."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Kích Hoạt Khoái Cảm",
            "effect": "Giải trừ thêm <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Choáng</color>. Kỹ năng này cũng được áp dụng cho Arios."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Chuẩn Bị Phẫu Thuật",
            "effect": "Arios giảm <color=#f26c1c>30%</color> sát thương phải gánh chịu.\n\nCường hóa hiệu ứng Rung Chuyển Tuyệt Vọng: Tăng Tấn Công thêm <color=#f26c1c>35%</color>, tăng gấp đôi hệ số sát thương của Phản Kích, và hồi phục lượng HP bằng <color=#f26c1c>30%</color> sát thương gây ra sau khi gây sát thương."
        }
    ],
    "helen": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Đột Kích Khiên Chắn",
            "effect": "Độ rộng phạm vi tăng thêm <color=#f26c1c>2 ô</color>, giải trừ thêm <color=#f26c1c>2</color> Debuff, và áp dụng <color=#3487e0>ST Bạo Kích Tăng II</color> trong <color=#f26c1c>2 hiệp</color>."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Valkyrie Bất Khuất",
            "effect": "Tăng Chỉ Số Ổn Định lên <color=#f26c1c>16 điểm</color>, giảm <color=#f26c1c>50%</color> sát thương phải gánh chịu. Mỗi khi chịu sát thương, nhận thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Lưỡi Đao Vượt Mức</color>. Trước khi thực hiện đòn đánh thường, tăng Tấn Công bằng <color=#f26c1c>30%</color> Phòng Thủ của bản thân."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Chiến Kỳ Lính Canh",
            "effect": "Thời gian hồi chiêu giảm <color=#f26c1c>2 hiệp</color>. Nhận <color=#3487e0>Tấn Công Tăng III</color> và <color=#3487e0>Phòng Thủ Tăng III</color> trong <color=#f26c1c>2 hiệp</color>. Nhận <color=#f26c1c>10 tầng</color> <color=#3487e0>Lưỡi Đao Vượt Mức</color>. Giảm thời gian hồi chiêu Tuyệt kỹ của các Doll thuộc tính <color=#42cce0>Băng Kết</color> đi <color=#f26c1c>2 hiệp</color>."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Chỉ Lệnh Khiên Chắn",
            "effect": "Giải trừ thêm <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Choáng</color>. Nếu chịu sát thương chí tử trong khi chia sẻ sát thương, Helen sẽ không tử trận và hồi phục lượng HP bằng <color=#f26c1c>150%</color> Phòng Thủ của bản thân. Hiệu ứng này có thể kích hoạt tối đa 1 lần mỗi hiệp. Các đơn vị đồng minh có Khiên Chắn gây thêm <color=#f26c1c>30%</color> <color=#42cce0>ST Băng Kết</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Đột Kích Khiên Chắn",
            "effect": "Với mỗi đơn vị đồng minh (ngoại trừ bản thân) trên đường di chuyển, hồi phục thêm <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định, đồng thời nhận số tầng <color=#3487e0>Lực Đẩy Băng Giá</color> tương ứng."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Valkyrie Bất Khuất",
            "effect": "Trước khi thực hiện đòn đánh thường, tăng Tấn Công của Helen bằng <color=#f26c1c>70%</color> Phòng Thủ của bản thân.\nKhi một đơn vị đồng minh chịu sát thương, nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Lưỡi Đao Vượt Mức</color>. Khi đang có <color=#3487e0>Lưỡi Đao Vượt Mức</color>, hệ số sát thương của đòn đánh thường tăng lên <color=#f26c1c>300%</color>."
        }
    ],
    "jiangyu": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Hạo Nhiên Chính Khí",
            "effect": "Số lần Hành Động Chi Viện tăng thêm <color=#f26c1c>1 lần</color>.\nKhi bắt đầu chiến đấu, gây <color=#f26c1c>4 điểm</color> ST Ổn Định cố định lên toàn bộ đơn vị địch trong phạm vi bán kính <color=#f26c1c>8 ô</color>.\n<color=#3487e0>Sóng Điện Sai Tầng</color> nhận hiệu ứng mới: Khi nhận được, gây sát thương cố định bằng số tầng hiện tại × <color=#f26c1c>10%</color> Tấn Công của người thi triển.\n<color=#3487e0>Bổ Sung Điện Mạnh</color> nhận hiệu ứng mới: Khi nhận hiệu ứng này, hồi phục lượng HP bằng <color=#f26c1c>10%</color> HP tối đa."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Sấm Rền Vạn Lý",
            "effect": "Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>, và Chỉ Số Nhiên Liệu nhận được tăng thêm <color=#f26c1c>1 điểm</color>.\nHồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho toàn bộ đồng minh, tăng số lượng Debuff được giải trừ thêm <color=#f26c1c>1</color>, và xóa bỏ <color=#3487e0>Chạy Trốn</color> cùng <color=#3487e0>Dẫn Dụ</color>."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Kích Điện Mãnh Liệt",
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>140%</color>.\nSát thương gây ra cho mục tiêu có <color=#3487e0>Sóng Điện Sai Tầng</color> tăng thêm <color=#f26c1c>30%</color>.\nTrước khi gây sát thương, hóa giải <color=#f26c1c>1</color> Buff của mục tiêu."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Sấm Sét Rền Vang",
            "effect": "Trước khi tấn công, nhận <color=#3487e0>Tấn Công Tăng II</color> trong <color=#f26c1c>3 hiệp</color>. Khi gây ST Ổn Định, gây thêm <color=#f26c1c>5 điểm</color> ST Ổn Định cố định lên toàn bộ đơn vị địch mang <color=#3487e0>Điện Tích Âm</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Kích Điện Mãnh Liệt",
            "effect": "Số lượng Buff hóa giải tăng thêm <color=#f26c1c>1</color>. Nếu mục tiêu có <color=#f26c1c>0 điểm</color> Ổn Định, thực hiện thêm 1 đòn tấn công bổ sung."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Hạo Nhiên Chính Khí",
            "effect": "ST Ổn Định cố định gây ra khi bắt đầu chiến đấu tăng thêm <color=#f26c1c>4 điểm</color>.\nKhi Jiangyu sở hữu <color=#3487e0>Khí</color>, <color=#b359f2>ST Dẫn Điện</color> gây ra tăng thêm <color=#f26c1c>15%</color>.\nGiới hạn tầng tối đa của <color=#3487e0>Sóng Điện Sai Tầng</color> tăng thêm <color=#f26c1c>3 tầng</color>.\nThay đổi hiệu ứng <color=#3487e0>Bổ Sung Điện Mạnh</color>: Khi gây <color=#b359f2>ST Dẫn Điện</color>, tỷ lệ bỏ qua Phòng Thủ tăng lên <color=#f26c1c>10%</color>, và lượng hồi máu nhận được tăng lên <color=#f26c1c>10%</color>."
        }
    ],
    "lewis": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Lính Chì Diễu Hành",
            "effect": "Hệ số sát thương cơ bản của Bắn Đồng Loạt tăng lên <color=#f26c1c>120%</color> Tấn Công của Lewis.\nKhi Lính Chì thi triển Bắn Đồng Loạt, nếu mục tiêu địch có <color=#3487e0>Tràn Lửa</color>, hiệu ứng <color=#3487e0>Tràn Lửa</color> sẽ được kích hoạt số lần tương ứng với Cấp Bậc của chúng."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Lễ Hội Đồ Chơi",
            "effect": "Giảm tiêu hao Chỉ Số Nhiên Liệu đi <color=#f26c1c>2 điểm</color>.\nBổ sung thêm hiệu ứng dựa trên Cấp Bậc hiện tại cao nhất của bạn. Hiệu ứng cấp cao hơn bao gồm cả hiệu ứng cấp thấp hơn:\nCấp 1: Nhận <color=#3487e0>ST Tăng II</color> trước khi tấn công, duy trì trong <color=#f26c1c>2 hiệp</color>.\nCấp 2: Đòn tấn công này bỏ qua vật chắn (Yểm Hộ).\nCấp 3: Tăng hệ số sát thương lên <color=#f26c1c>200%</color> Tấn Công của bạn."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Quả Cầu Bất Ngờ",
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>160%</color>, hệ số sát thương cố định tăng lên <color=#f26c1c>50%</color>.\n\nSửa đổi hiệu ứng <color=#3487e0>Hiệu Lệnh Lính Chì</color>: Không còn số tầng và không còn bị tiêu hao bởi Bắn Đồng Loạt. Thay vào đó duy trì trong <color=#f26c1c>3 hiệp</color> và tăng sát thương Bắn Đồng Loạt thêm <color=#f26c1c>50%</color>."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Dọn Dẹp Kẻ Xấu",
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>120%</color>. Với mỗi Debuff thuộc tính Thiêu Đốt trên mục tiêu, đòn tấn công này gây thêm <color=#f26c1c>10%</color> sát thương, tối đa tăng <color=#f26c1c>30%</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Lễ Hội Đồ Chơi",
            "effect": "Mỗi Lính Chì tăng thêm hệ số sát thương cho đòn tấn công này thêm <color=#f26c1c>10%</color> theo mỗi Cấp Bậc; sát thương bạo kích tăng thêm <color=#f26c1c>5%</color> theo mỗi Cấp Bậc."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Lính Chì Diễu Hành",
            "effect": "Lính Chì được chỉ định khi bắt đầu trận chiến có Cấp 2.\nCường hóa hiệu ứng Cấp Bậc:\nCấp 2: Tăng thêm <color=#f26c1c>15%</color> ST Bạo Kích.\nCấp 3: Vào cuối hành động của Doll được chỉ định, tung ra 1 lần Bắn Đồng Loạt nhắm vào mục tiêu địch gần nhất. Đợt Bắn Đồng Loạt này cung cấp <color=#3487e0>Lửa Thiêu Đốt</color> nhưng không hồi phục Chỉ Số Nhiên Liệu."
        }
    ],
    "lind": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Kho Dự Trữ Kẹo",
            "effect": "Khi bắt đầu trận chiến, với mỗi đồng minh hiện diện, Lind nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Kẹo Đường</color>. Tăng số tầng tối đa của <color=#3487e0>Kẹo Đường</color> lên <color=#f26c1c>30 tầng</color>.\n\nCường hóa hiệu ứng <color=#3487e0>Kẹo Đường</color> - Tăng <color=#f26c1c>2%</color> <color=#5bcc3b>ST Ăn Mòn</color> gây ra."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Quá Tải Đường Huyết",
            "effect": "Tăng sát thương gây ra bởi kỹ năng chủ động tiếp theo thêm <color=#f26c1c>15%</color>.\n\nCường hóa hiệu ứng <color=#3487e0>Chứng Nhiễm Ceton</color> - Mục tiêu nhận thêm <color=#f26c1c>12%</color> <color=#5bcc3b>ST Ăn Mòn</color> từ Lind, tối đa lên tới <color=#f26c1c>72%</color>."
        },
        {
            "tier": 3,
            "level": 3,
            "skill": "Kho Dự Trữ Kẹo",
            "effect": "Loại bỏ thời gian hồi chiêu để áp dụng <color=#3487e0>Cạm Bẫy Ngọt Ngào</color> khi bắt đầu hiệp.\n\nKhi <color=#3487e0>Cạm Bẫy Ngọt Ngào</color> được kích hoạt, tăng số lượng Debuff mạnh ngẫu nhiên được áp dụng thêm <color=#f26c1c>3</color>, tăng hệ số sát thương lên <color=#f26c1c>120%</color> Tấn Công, và tăng ST Bạo Kích thêm <color=#f26c1c>15%</color>."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Bình Xịt Đột Kích",
            "effect": "Áp dụng <color=#f26c1c>2 tầng</color> <color=#3487e0>Giải Phóng Phụ Thuộc</color>.\n\nMở rộng phạm vi hiệu lực của kỹ năng từ khu vực hình quạt nhỏ thành khu vực hình quạt (mở rộng 2×6 ô sang trái và phải của khu vực ban đầu).\n\nVới mỗi Debuff trên kẻ địch, tăng sát thương gây ra thêm <color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>60%</color>."
        },
        {
            "tier": 5,
            "level": 2,
            "skill": "Bộc Phá Áp Đảo",
            "effect": "Tăng hệ số sát thương lên <color=#f26c1c>120%</color> Tấn Công và tăng ST Ổn Định gây ra thêm <color=#f26c1c>1 điểm</color>.\n\nTrước khi dùng kỹ năng, nếu Chỉ Số Nhiên Liệu đạt tối đa, tăng ST Bạo Kích thêm <color=#f26c1c>20%</color>; với mỗi tầng <color=#3487e0>Kẹo Đường</color>, tăng hệ số sát thương thêm <color=#f26c1c>10%</color>."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Quá Tải Đường Huyết",
            "effect": "Sau khi dùng kỹ năng, tăng Chỉ Số Nhiên Liệu thêm <color=#f26c1c>3 điểm</color>. Nếu Lind có <color=#f26c1c>10 tầng</color> <color=#3487e0>Kẹo Đường</color>, giảm thời gian hồi chiêu của kỹ năng này đi <color=#f26c1c>1 hiệp</color>."
        }
    ],
    "liushih": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Đồng Tâm Tác Chiến",
            "effect": "Khi kết thúc hành động của Liushih, Pegasus bắn <color=#f26c1c>1 lần</color> Pháo Tự Động Phòng Thủ Điểm vào mục tiêu địch gần nhất trong phạm vi."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Nước Cờ Chiến Lược",
            "effect": "Tạo các ô địa hình <color=#3487e0>Dòng Ngầm</color> trên đường di chuyển trong <color=#f26c1c>2 hiệp</color>. Pegasus không còn bị rút khỏi trạng thái <color=#3487e0>Tác Chiến Phối Hợp</color>."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Được Ăn Cả",
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>120%</color>.\nCải thiện hiệu ứng <color=#3487e0>Độ chính xác</color>: Tăng hệ số sát thương của đòn đánh thường thêm <color=#f26c1c>20%</color> cho mỗi tầng."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Dẫn Đầu Xung Phong",
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>120%</color>.\n<color=#3487e0>Tác Chiến Phối Hợp</color> nhận hiệu ứng mới: ST Bạo Kích của Liushih và Pegasus tăng thêm <color=#f26c1c>30%</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Đồng Tâm Tác Chiến",
            "effect": "Với mỗi <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu nhận được trong hiệp hiện tại, trước khi sử dụng kỹ năng chủ động Được Ăn Cả ở hiệp tiếp theo, bản thân và tất cả vật triệu hồi thực thể phe đồng minh nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Sắc bén</color>, duy trì trong <color=#f26c1c>1 hiệp</color>."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Được Ăn Cả",
            "effect": "Gấp đôi số tầng <color=#3487e0>Độ chính xác</color> nhận được."
        }
    ],
    "loreley": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Ân Sủng Đau Đớn",
            "effect": "Hiệu ứng <color=#3487e0>Vũ Điệu Cộng Sinh</color> mới: Khi chịu sát thương chí tử, hồi phục <color=#f26c1c>25%</color> HP tối đa và <color=#f26c1c>5 điểm</color> Chỉ Số Ổn Định, giải trừ tất cả Debuff và giảm <color=#f26c1c>60%</color> sát thương phải chịu trong vòng <color=#f26c1c>1 hiệp</color>.\nSau khi sử dụng đòn đánh thường hoặc kỹ năng chủ động, Thợ Săn - Loại II phát phóng thêm 1 lần Xung Hỏa Lực.\nĐồng thời giải trừ <color=#3487e0>Choáng</color> cho toàn bộ đơn vị đồng minh."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Sự Hào Phóng Của Nữ Hoàng",
            "effect": "Số lần có thể áp dụng <color=#3487e0>Lửa Cháy Hoàn Hảo</color> tăng lên <color=#f26c1c>5 lần</color>.\nChỉ Lệnh Bổ Sung được thay thế bằng Hành Động Thêm.\n<color=#3487e0>Tàn Tro Lửa Rực</color> không còn tăng sát thương Thiêu Đốt, thay vào đó tăng tất cả sát thương gây ra thêm <color=#f26c1c>45%</color>."
        },
        {
            "tier": 3,
            "level": 3,
            "skill": "Ân Sủng Đau Đớn",
            "effect": "Thợ Săn - Loại II tạo thêm <color=#f26c1c>4 điểm</color> <color=#3487e0>Lửa Thiêu Đốt</color> khi được triệu hồi.\nHệ số sát thương của Xung Hỏa Lực tăng gấp đôi; với mỗi đợt Xung Hỏa Lực được phóng ra, sát thương gây ra bởi Loreley tăng thêm <color=#f26c1c>10%</color>, tối đa <color=#f26c1c>60%</color>; ST Bạo Kích tăng thêm <color=#f26c1c>2%</color>, tối đa <color=#f26c1c>12%</color>.\nÁp dụng <color=#3487e0>Lửa Cháy Hoàn Hảo</color> cho toàn bộ đơn vị đồng minh."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Tuyên Ngôn Đỏ Thắm",
            "effect": "Tăng hệ số sát thương thêm <color=#f26c1c>30%</color> và tăng phạm vi hiệu lực thêm <color=#f26c1c>1 ô</color>.\nVới mỗi Buff thuộc tính Thiêu Đốt mà Loreley sở hữu, sát thương gây ra tăng thêm <color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>40%</color>."
        },
        {
            "tier": 5,
            "level": 2,
            "skill": "Dấu Ấn Thiêu Đốt",
            "effect": "Kỹ năng bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu. Nếu mục tiêu đang đứng trên ô địa hình <color=#3487e0>Thiêu Rụi</color>, sát thương gây ra tăng thêm <color=#f26c1c>60%</color>."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Sự Hào Phóng Của Nữ Hoàng",
            "effect": "<color=#3487e0>Lửa Thiêu Đốt</color> nhận được bởi tất cả đơn vị đồng minh khi Loreley có mặt trên sân tăng thêm <color=#f26c1c>1 điểm</color>. Với mỗi Doll thuộc tính Thiêu Đốt trên sân, Tấn Công của Loreley tăng thêm <color=#f26c1c>6%</color>.\nTấn Công từ <color=#3487e0>Dâng Trào Địa Ngục</color> được áp dụng bởi Thợ Săn - Loại II tăng lên <color=#f26c1c>12%</color>.\nTăng cường hiệu ứng <color=#3487e0>Tàn Tro Lửa Rực</color>: Mức giảm sát thương tăng lên <color=#f26c1c>30%</color>."
        }
    ],
    "mechty": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Xứ Sở Thần Tiên Trong Mơ",
            "effect": "Không còn tắt <color=#3487e0>Chế Độ Bản Vá</color> khi vào <color=#3487e0>Chế Độ Quyết Đấu</color>.\n\n<color=#3487e0>Lá Chắn Ác Mộng</color> giảm Tấn Công của kẻ tấn công đi <color=#f26c1c>10%</color> và tăng số lượng Debuff được giải trừ thêm <color=#f26c1c>1</color>.\n\n<color=#3487e0>Chế Độ Quyết Đấu</color> nhận hiệu ứng mới: Tỷ lệ bạo kích của đòn đánh thường tăng thêm <color=#f26c1c>30%</color>."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Giấc Ngủ Ngắn Kỳ Bí",
            "effect": "<color=#3487e0>Chế Độ Bản Vá</color> nhận hiệu ứng mới: Đòn đánh thường gây thêm <color=#f26c1c>50%</color> sát thương. Khi bắt đầu hiệp, giải trừ <color=#f26c1c>2</color> Debuff trên bản thân."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Đêm Không Mộng Mị",
            "effect": "Số tầng tối đa của <color=#3487e0>Bộ Trợ Ngủ</color> tăng thêm <color=#f26c1c>1 tầng</color>. Mechty hồi phục lượng HP bằng <color=#f26c1c>30%</color> HP tối đa, và đơn vị đồng minh có tỷ lệ HP thấp nhất hồi phục lượng HP bằng <color=#f26c1c>15%</color> HP tối đa của Mechty cùng <color=#f26c1c>3 điểm</color> Chỉ Số Ổn Định.\n\nKhi ở <color=#3487e0>Chế Độ Quyết Đấu</color>, số tầng <color=#3487e0>Bộ Trợ Ngủ</color> nhận được tăng thêm <color=#f26c1c>1 tầng</color>."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Chấn Động Giấc Mơ",
            "effect": "ST Ổn Định tăng thêm <color=#f26c1c>2 điểm</color>.\n\nKhi <color=#3487e0>Chế Độ Quyết Đấu</color> đang kích hoạt, tăng sát thương của đòn đánh thường tiếp theo thêm <color=#f26c1c>100%</color>. Gây sát thương cố định bằng <color=#f26c1c>50%</color> Tấn Công lên toàn bộ đơn vị địch trong phạm vi."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Xứ Sở Thần Tiên Trong Mơ",
            "effect": "<color=#3487e0>Chế Độ Quyết Đấu</color> nhận hiệu ứng mới: Khả năng di chuyển tăng thêm <color=#f26c1c>2 ô</color>, áp dụng <color=#3487e0>Lá Chắn Ác Mộng</color> cho các đơn vị đồng minh chưa có Lá Chắn Ác Mộng vào cuối hành động. Nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Giấc Ngủ Ngắn Kỳ Bí",
            "effect": "<color=#3487e0>Chế Độ Bản Vá</color> nhận hiệu ứng mới: <color=#5bcc3b>ST Ăn Mòn</color> gây ra bởi tất cả đơn vị đồng minh tăng thêm <color=#f26c1c>25%</color>, tăng ST Bạo Kích gây ra bởi đòn đánh thường của Mechty thêm <color=#f26c1c>80%</color>.\n\n<color=#3487e0>Ác Mộng Hóa</color> nhận hiệu ứng mới: Sát thương diện rộng gây ra bởi Đòn Đánh Chi Viện tăng lên <color=#f26c1c>80%</color>, ST Ổn Định gây ra tăng thêm <color=#f26c1c>1 điểm</color>, và sát thương diện rộng gây ra tăng lên <color=#f26c1c>20%</color>."
        }
    ],
    "mityl": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Kỹ Xảo Điện Ảnh",
            "effect": "Sát thương của <color=#3487e0>Cộng Hưởng Tương Thích</color> tăng lên <color=#f26c1c>60%</color> Tấn Công. Khi <color=#3487e0>Danh Hiệu Điện Ảnh</color> được nâng cấp, Hình Chiếu thi triển <color=#3487e0>Cộng Hưởng Tương Thích</color> <color=#f26c1c>1 lần</color>. Chỉ Số Nhiên Liệu cần thiết để nâng cấp Danh Hiệu giảm xuống còn <color=#f26c1c>4 điểm</color>. <color=#3487e0>Cộng Hưởng Tương Thích</color> áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Hình Chiếu Sóc Con",
            "effect": "Mỗi khi thi triển <color=#3487e0>Cộng Hưởng Tương Thích</color>, Hình Chiếu nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Bất Khả Xâm Phạm</color>. Hệ số sát thương của đòn đánh thường Tấn Công Bóng Vòng của Hình Chiếu Cá Nhân tăng lên <color=#f26c1c>120%</color> Tấn Công."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Hội Tụ Hư Không",
            "effect": "Phạm vi của ô địa hình <color=#3487e0>Dòng Ngầm</color> được tạo ra mở rộng thành bán kính <color=#f26c1c>7 ô</color>. Mức tăng Tấn Công từ <color=#3487e0>Tràn Bão Hòa</color> tăng lên <color=#f26c1c>40%</color> và cũng áp dụng cho Hình Chiếu. Nếu <color=#3487e0>Cộng Hưởng Tương Thích</color> kích hoạt tổng cộng từ <color=#f26c1c>4 lần</color> trở lên trong hiệp hiện tại, <color=#3487e0>Tràn Bão Hòa</color> sẽ không bị tiêu hao thời lượng."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Phi Thân Nhào Lộn",
            "effect": "Điều kiện để tái sử dụng kỹ năng chủ động được thay đổi: Mityl chỉ cần đứng trên ô địa hình loại Hóa Lỏng trước khi dùng kỹ năng hoặc khi gây sát thương. Sát thương tăng lên <color=#f26c1c>160%</color> Tấn Công. Sát thương gây ra bởi kỹ năng chủ động được tái sử dụng tăng thêm <color=#f26c1c>50%</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Phi Thân Nhào Lộn",
            "effect": "Sau khi thi triển kỹ năng, Hình Chiếu Cá Nhân thực hiện <color=#f26c1c>1 lần</color> Hành Động Chi Viện nhắm vào mục tiêu, gây <color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>60%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định. Có thể kích hoạt tối đa 1 lần mỗi hiệp. Sát thương gây ra bởi Hình Chiếu Bắt Chước trong hiệp hiện tại tăng thêm <color=#f26c1c>100%</color>. Hiệu ứng này không thể cộng dồn."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Kỹ Xảo Điện Ảnh",
            "effect": "Ngôi Sao Huyền Thoại nhận hiệu ứng mới: Cứ mỗi <color=#f26c1c>4 điểm</color> Chỉ Số Nhiên Liệu nhận được, tất cả Hình Chiếu thi triển <color=#3487e0>Cộng Hưởng Tương Thích</color> <color=#f26c1c>1 lần</color>.\n\nKhi một Hình Chiếu thi triển <color=#3487e0>Cộng Hưởng Tương Thích</color>, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Khuếch Đại Tương Thích</color>."
        }
    ],
    "ots-14": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Lệnh Tác Chiến",
            "effect": "Cường hóa hiệu ứng <color=#3487e0>Chỉ Lệnh Yểm Hộ</color>: Mức tăng ST Bạo Kích của tất cả đơn vị đồng minh ngoại trừ bản thân được nâng lên <color=#f26c1c>15%</color> ST Bạo Kích ban đầu của bản thân.\nCường hóa hiệu ứng <color=#3487e0>Chỉ Lệnh Bạo Phá</color>: Mức tăng Tấn Công của bản thân được nâng lên <color=#f26c1c>15%</color> Tấn Công ban đầu của tất cả Doll đồng minh ngoại trừ bản thân."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Áp Chế Toàn Diện",
            "effect": "Hệ số sát thương tăng lên <color=#f26c1c>150%</color>.\nPhạm vi hiệu lực mở rộng lên phạm vi <color=#f26c1c>5×5 ô</color>.\nThời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Càn Quét Tầm Xa",
            "effect": "Cường hóa hiệu ứng <color=#3487e0>Đồng Hóa Nghịch Đảo</color>: Sát thương của Bộc Phá Chí Mạng tăng lên <color=#f26c1c>200%</color>, và tầm bắn hiệu lực tăng thêm <color=#f26c1c>2 ô</color>."
        },
        {
            "tier": 4,
            "level": 3,
            "skill": "Càn Quét Tầm Xa",
            "effect": "Cường hóa hiệu ứng <color=#3487e0>Đồng Hóa Nghịch Đảo</color>: Mỗi khi sử dụng Bộc Phá Chí Mạng trong hiệp hiện tại, hệ số sát thương của Bộc Phá Chí Mạng tăng thêm <color=#f26c1c>50%</color>, và hệ số sát thương cố định gây ra khi tiêu hao <color=#3487e0>Mạch Xung Quá Tải</color> tăng thêm <color=#f26c1c>10%</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Áp Chế Toàn Diện",
            "effect": "Nếu bản thân đang có <color=#3487e0>Chỉ Lệnh Yểm Hộ</color>, mức tăng sát thương tích lũy bởi Chế Độ Chỉ Huy sau khi dùng kỹ năng được nâng lên <color=#f26c1c>33%</color>.\nNếu bản thân đang có <color=#3487e0>Chỉ Lệnh Bạo Phá</color>, cứ mỗi <color=#f26c1c>15%</color> ST Bạo Kích ban đầu, hệ số sát thương tăng thêm <color=#f26c1c>15%</color>."
        },
        {
            "tier": 6,
            "level": 2,
            "skill": "Chiến Thuật Bậc Thầy",
            "effect": "Kỹ năng chủ động Áp Chế Toàn Diện tạo các ô địa hình Giai Đoạn cấp 1 trong <color=#f26c1c>2 hiệp</color> trong phạm vi hiệu lực nếu có bất kỳ Tái Cấu Trúc Giai Đoạn nào đang kích hoạt. <color=#3487e0>Tái Tạo - 0</color> không tạo ô địa hình.\nCường hóa các hiệu ứng của <color=#3487e0>Tái Tạo Tế Bào</color>:\n<color=#3487e0>Tái Tạo - Thiêu Đốt</color> - Hóa giải <color=#f26c1c>1</color> Debuff khi đồng đội nhận Tàn Tro;\n<color=#3487e0>Tái Tạo - Dẫn Điện</color> - Khi một đơn vị địch rơi vào trạng thái Sụp Đổ Ổn Định, toàn bộ đồng minh hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định;\n<color=#3487e0>Tái Tạo - Băng Kết</color> - Khi một đồng minh gây sát thương, tăng Tấn Công của họ bằng <color=#f26c1c>10%</color> giá trị lá chắn;\n<color=#3487e0>Tái Tạo - Ăn Mòn</color> - Kỹ năng chủ động Áp Chế Toàn Diện kích hoạt toàn bộ Debuff thuộc tính Ăn Mòn của các đơn vị địch trong phạm vi hiệu lực;\n<color=#3487e0>Tái Tạo - Hóa Lỏng</color> - Với mỗi đơn vị đồng minh, tất cả Vật Triệu Hồi Thực Thể tăng <color=#f26c1c>1%</color> Tấn Công và <color=#f26c1c>1%</color> HP tối đa;\n<color=#3487e0>Tái Tạo - 0</color> - Chỉ Lệnh Bạo Phá tăng Tấn Công thêm <color=#f26c1c>50%</color> thay vì 30%, bỏ qua <color=#f26c1c>5%</color> Phòng Thủ cho mỗi <color=#f26c1c>15%</color> ST Bạo Kích ban đầu."
        }
    ],
    "qiuhua": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Đun Sôi Cô Đặc",
            "effect": "Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>. Khi gây sát thương, lập tức kích hoạt <color=#f26c1c>1 lần</color> hiệu ứng của <color=#3487e0>Vết Cháy</color> vốn được kích hoạt khi kết thúc hành động của mục tiêu."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Quy Tắc Táo Quân",
            "effect": "Chi Viện Khẩn Cấp có thể kích hoạt từ 1 → <color=#f26c1c>2 lần</color> mỗi hiệp.\n\nTăng <color=#ff4d4f>ST Thiêu Đốt</color> gây ra từ 5% → <color=#f26c1c>15%</color>. Loại bỏ điều kiện cần thiết để kích hoạt hiệu ứng này.\n\nKhi gây sát thương, nếu Tỷ Lệ Bạo Kích vượt quá <color=#f26c1c>100%</color>, mỗi <color=#f26c1c>1%</color> Tỷ Lệ Bạo Kích vượt mức sẽ chuyển đổi thành <color=#f26c1c>1%</color> ST Bạo Kích."
        },
        {
            "tier": 3,
            "level": 3,
            "skill": "Quy Tắc Táo Quân",
            "effect": "<color=#3487e0>Vết Cháy</color> không còn giới hạn tầng tối đa.\n\nBổ sung hiệu ứng mới khi gây <color=#ff4d4f>ST Thiêu Đốt</color> lên mục tiêu có <color=#3487e0>Vết Cháy</color> - nếu số tầng <color=#3487e0>Vết Cháy</color> nhiều hơn <color=#f26c1c>10 tầng</color>, với mỗi tầng vượt mức, Tấn Công tăng thêm <color=#f26c1c>1%</color>."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Bước Nhảy Vọt",
            "effect": "Hệ số sát thương tăng thêm <color=#f26c1c>50%</color>.\n\nNếu mục tiêu có <color=#3487e0>Vết Cháy</color>, gây thêm 1 lần sát thương cố định tương đương <color=#f26c1c>50%</color> Tấn Công.\n\nSau khi tấn công, nhận <color=#3487e0>Dị Vị Tăng II</color> và <color=#3487e0>Thế Tấn Công Ổn Định II</color> trong <color=#f26c1c>1 hiệp</color>."
        },
        {
            "tier": 5,
            "level": 2,
            "skill": "Xèo Xèo Nóng Bỏng",
            "effect": "Sau khi tấn công, nhận thêm <color=#f26c1c>6 ô</color> Di Chuyển Bổ Sung.\n\nNếu mục tiêu có <color=#3487e0>Vết Cháy</color>, sát thương gây ra tăng thêm <color=#f26c1c>30%</color>.\n\nNếu khoảng cách giữa Qiuhua và mục tiêu nhỏ hơn hoặc bằng <color=#f26c1c>4 ô</color>, sát thương gây ra tăng từ 5% → <color=#f26c1c>15%</color> và ST Ổn Định gây ra tăng từ 1 → <color=#f26c1c>2 điểm</color>."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Đun Sôi Cô Đặc",
            "effect": "Nếu kỹ năng này chỉ đánh trúng 1 mục tiêu, sát thương gây ra tăng thêm <color=#f26c1c>15%</color>.\n\nCường hóa hiệu ứng <color=#3487e0>Vết Cháy</color> - tăng sát thương gây ra mỗi tầng lên <color=#f26c1c>10%</color> Tấn Công của người thi triển, và số tầng nhận được khi chịu <color=#ff4d4f>ST Thiêu Đốt</color> tăng lên <color=#f26c1c>2 tầng</color>."
        }
    ],
    "sakura": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Cầu Nguyện Phúc Lành",
            "effect": "Áp dụng ngẫu nhiên <color=#3487e0>Dấu Anh Đào</color> lên tối đa <color=#f26c1c>5</color> kẻ địch; hệ số sát thương của <color=#3487e0>Dấu Anh Đào</color> tăng lên <color=#f26c1c>90%</color>, và bán kính hiệu lực tăng thêm <color=#f26c1c>1 ô</color>.\nNếu một đơn vị địch đang đứng trên ô địa hình loại Thiêu Đốt, sát thương gây ra bởi <color=#3487e0>Dấu Anh Đào</color> tăng thêm <color=#f26c1c>30%</color>."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Hoa Rơi Tung Bay",
            "effect": "Tầm bắn tăng thêm <color=#f26c1c>1 ô</color>; phạm vi hiệu lực tăng thêm <color=#f26c1c>1 ô</color>; hệ số sát thương tăng thêm <color=#f26c1c>15%</color>; giảm tiêu hao Chỉ Số Nhiên Liệu đi <color=#f26c1c>1 điểm</color>."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Cầu Nguyện Phúc Lành",
            "effect": "Nếu bản thân sở hữu <color=#3487e0>Vận May</color>, sát thương gây ra tăng thêm <color=#f26c1c>50%</color> và ST Bạo Kích tăng thêm <color=#f26c1c>25%</color>.\nKhi một kẻ địch nhận <color=#3487e0>Dấu Anh Đào</color>, tạo ô địa hình <color=#3487e0>Thiêu Rụi</color> trong phạm vi bán kính <color=#f26c1c>1 ô</color> xung quanh mục tiêu trong <color=#f26c1c>3 hiệp</color>; khi <color=#3487e0>Dấu Anh Đào</color> gây sát thương, bỏ qua <color=#f26c1c>15%</color> Phòng Thủ của mục tiêu."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Chuyển Phát Vận Rủi",
            "effect": "Tăng số tầng <color=#3487e0>Dấu Anh Đào</color> được áp dụng lên <color=#f26c1c>3 tầng</color>; mức tăng sát thương từ <color=#3487e0>Vận Rủi</color> nâng lên <color=#f26c1c>30%</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Đại Mạo Hiểm Dị Giới",
            "effect": "Hệ số sát thương tăng thêm <color=#f26c1c>30%</color>; mở rộng phạm vi hiệu lực thành khu vực <color=#f26c1c>5×10 ô</color> phía trước; cộng dồn hiệu ứng này tới giới hạn tối đa trên tất cả đơn vị địch trên toàn sân đang bị ảnh hưởng bởi <color=#3487e0>Dấu Anh Đào</color>."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Đại Mạo Hiểm Dị Giới",
            "effect": "<color=#3487e0>Vận May</color> nhận thêm hiệu ứng:\nTrước khi một đơn vị đồng minh thực hiện đòn tấn công chủ động hoặc đòn tấn công ngoài lượt (ngoại trừ bản thân), Sakura áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Dấu Anh Đào</color> lên mục tiêu đó.\nCó thể kích hoạt tối đa <color=#f26c1c>3 lần</color> mỗi hiệp."
        }
    ],
    "sextans": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Chuông Tang Vong Hồn",
            "effect": "Nếu kỹ năng đánh trúng mục tiêu địch, bản thân thi triển <color=#3487e0>Huyết Huy Hiệu</color> lên mục tiêu đó <color=#f26c1c>1 lần</color> và nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Sau khi dùng kỹ năng, bản thân nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Đông Tụ</color>."
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Khúc Vịnh Đêm Tối",
            "effect": "Độ rộng khu vực kỹ năng tăng thêm <color=#f26c1c>2 ô</color>. Cường hóa hiệu ứng <color=#3487e0>Dấu Ấn Thánh Huyết</color>, ST Ổn Định và lượng Chỉ Số Ổn Định bị bỏ qua tăng thêm <color=#f26c1c>5 điểm</color>; khi gây <color=#b359f2>ST Dẫn Điện</color> hoặc ST Cận Chiến, sát thương tăng thêm <color=#f26c1c>5%</color> cho mỗi tầng <color=#3487e0>Đông Tụ</color> (chỉ áp dụng 1 lần khi thỏa mãn nhiều điều kiện)."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Khúc An Hồn",
            "effect": "Tất cả Doll thuộc tính <color=#b359f2>Dẫn Điện</color> và tất cả Doll sử dụng Kiếm được tăng <color=#f26c1c>2 ô</color> di chuyển (chỉ áp dụng 1 lần khi thỏa mãn nhiều điều kiện), đồng thời bỏ qua cản trở của kẻ địch. Cường hóa hiệu ứng <color=#3487e0>Đông Tụ</color>: Giới hạn tối đa chuyển đổi Tỷ Lệ Bạo Kích dư thừa thành Tấn Công, lượng trị liệu và ST Bạo Kích nâng lên <color=#f26c1c>45%</color>. Cường hóa hiệu ứng <color=#3487e0>Huyết Huy Hiệu</color>: Với mỗi tầng <color=#3487e0>Đông Tụ</color>, hệ số sát thương tăng lên <color=#f26c1c>4%</color>. Cường hóa hiệu ứng <color=#3487e0>Huy Hiệu Đỏ Thẫm</color>: Sát thương cận chiến phải gánh chịu tăng lên <color=#f26c1c>10%</color>."
        },
        {
            "tier": 4,
            "level": 3,
            "skill": "Khúc Vịnh Đêm Tối",
            "effect": "Trước khi dùng kỹ năng, áp dụng <color=#3487e0>Dẫn Điện Tăng II</color> cho tất cả đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>. Sau khi dùng kỹ năng, nhận <color=#3487e0>Ngụy Trang</color> trong <color=#f26c1c>2 hiệp</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Chuông Tang Vong Hồn",
            "effect": "Hệ số sát thương và hồi máu tăng thêm <color=#f26c1c>30%</color>; giải trừ thêm <color=#f26c1c>1</color> Debuff; <color=#3487e0>Huyết Hôn</color> không còn bị xóa bỏ."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Khúc An Hồn",
            "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>5 tầng</color> <color=#3487e0>Đông Tụ</color>, và giới hạn Tỷ Lệ Bạo Kích cho <color=#3487e0>Đông Tụ</color> tăng lên <color=#f26c1c>75%</color>. Hệ số sát thương của <color=#3487e0>Huyết Huy Hiệu</color> tăng lên <color=#f26c1c>90%</color>, bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu khi gây sát thương. Không còn tiêu hao Chỉ Số Nhiên Liệu. Khi đầy Chỉ Số Nhiên Liệu, tất cả đơn vị đồng minh tăng <color=#f26c1c>15%</color> sát thương cận chiến gây ra."
        }
    ],
    "zhaohui": [
        {
            "tier": 1,
            "level": 2,
            "skill": "Thập Diện Mai Phục",
            "effect": "Khi bắt đầu trận chiến, Zhaohui triệu hồi <color=#f26c1c>1</color> Mũi Tên Tĩnh Lặng trên ô xung quanh. Số lần kích hoạt tối đa của Hành Động Chi Viện tăng thêm <color=#f26c1c>1 lần</color>. Khi có bất kỳ Mũi Tên Tĩnh Lặng nào trên sân, sát thương gây ra của Zhaohui tăng thêm <color=#f26c1c>10%</color>.\n\n(Mặc định được triệu hồi ở ô bên phải Zhaohui. Nếu ô đó không hợp lệ, sẽ được triệu hồi ở ô bên trái. Nếu vẫn không hợp lệ, sẽ được triệu hồi ở ô phía sau)"
        },
        {
            "tier": 2,
            "level": 2,
            "skill": "Định Phong Ba",
            "effect": "Cự ly thi triển tăng thêm <color=#f26c1c>3 ô</color>, và phạm vi hiệu lực tăng thêm <color=#f26c1c>1 ô</color>. ST Ổn Định tăng thêm <color=#f26c1c>2 điểm</color>, và sát thương gây ra tăng lên <color=#f26c1c>110%</color> Tấn Công."
        },
        {
            "tier": 3,
            "level": 2,
            "skill": "Bước Nhảy Thanh Minh",
            "effect": "ST Ổn Định gây ra tăng thêm <color=#f26c1c>2 điểm</color>. Áp dụng <color=#3487e0>Định Tức</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>. Di dời vị trí cùng với tất cả đơn vị đồng minh trong phạm vi <color=#f26c1c>2 ô</color> quanh bản thân."
        },
        {
            "tier": 4,
            "level": 2,
            "skill": "Dây Đoạt Ảnh",
            "effect": "Khi áp dụng <color=#3487e0>Choáng</color>, không còn yêu cầu mục tiêu phải có bất kỳ Debuff thuộc tính Hóa Lỏng nào. Cứ mỗi mục tiêu đánh trúng, Zhaohui hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định. Tỷ lệ bạo kích của đòn tấn công chủ động tiếp theo tăng thêm <color=#f26c1c>20%</color>. Ngoài ra, cứ mỗi mục tiêu đánh trúng, tỷ lệ bạo kích tăng thêm <color=#f26c1c>5%</color>."
        },
        {
            "tier": 5,
            "level": 3,
            "skill": "Thập Diện Mai Phục",
            "effect": "Khi kết thúc hành động, Mũi Tên Tĩnh Lặng giờ đây có thể được chọn từ bất kỳ vị trí nào trên toàn sân. Số lần kích hoạt tối đa của Hành Động Chi Viện tăng thêm <color=#f26c1c>1 lần</color>. Trước khi tấn công, nếu mục tiêu có từ <color=#f26c1c>2</color> Debuff trở lên, sát thương gây ra cho mục tiêu đó tăng thêm <color=#f26c1c>20%</color>."
        },
        {
            "tier": 6,
            "level": 3,
            "skill": "Bước Nhảy Thanh Minh",
            "effect": "ST Bạo Kích của đòn tấn công này tăng thêm <color=#f26c1c>30%</color>, và sát thương gây ra tăng lên <color=#f26c1c>180%</color> Tấn Công. Sau khi sử dụng kỹ năng này, Tấn Công của Zhaohui tăng thêm <color=#f26c1c>10%</color>, tối đa cộng dồn <color=#f26c1c>3 tầng</color>."
        }
    ]
}


def validate_effects_resolve(data):
    """Validate that every <color=#3487e0>...</color> resolves against browser_catalog."""
    with open(ROOT / "assets" / "effects.json", "r", encoding="utf-8") as f:
        catalog = browser_catalog(canonicalize_effects(json.load(f)))
    name_index = catalog["nameIndex"]

    color_re = re.compile(r"<color=#3487e0>(.*?)</color>")
    unresolved = {}

    for slug, forts in data.items():
        for f in forts:
            matches = color_re.findall(f["effect"])
            for m in matches:
                cleaned = m.strip().casefold()
                if cleaned not in name_index:
                    unresolved.setdefault(slug, []).append(m)

    return unresolved


def main():
    print("Validating effects resolve...")
    unresolved = validate_effects_resolve(FORTIFICATIONS_DATA)
    if unresolved:
        print("ERROR: Found unresolved status effects:")
        for slug, effs in unresolved.items():
            print(f"  [{slug}]: {effs}")
        sys.exit(1)
    print("All status effects resolve cleanly in nameIndex!")

    print(f"Loading {I18N_PATH}...")
    with open(I18N_PATH, "r", encoding="utf-8-sig") as f:
        i18n_bundle = json.load(f)

    chars = i18n_bundle.setdefault("characters", {})

    for slug, forts in FORTIFICATIONS_DATA.items():
        if slug not in chars:
            print(f"WARNING: {slug} not found in i18n_bundle!")
            continue
        chars[slug]["fortification"] = forts
        print(f"Updated fortification for {slug} (6 tiers)")

    # Atomic write to data/i18n_vi.json and site/static/js/i18n-vi.js
    tx = RepositoryTransaction(ROOT)
    stage_i18n_bundle(ROOT, tx, i18n_bundle)
    tx.commit()
    print("Committed updated fortifications to data/i18n_vi.json and site/static/js/i18n-vi.js!")


if __name__ == "__main__":
    main()
