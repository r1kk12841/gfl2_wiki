import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.editor_core.transaction import RepositoryTransaction
from tools.editor_core.bundle import stage_i18n_bundle

I18N_PATH = ROOT / "data" / "i18n_vi.json"

UPDATES = {
    "andoris": {
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
    "suomi": {
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ánh Sáng Tuyết Nguyên",
                "effect": "Số tầng của <color=#3487e0>Tuyết Lở</color> tăng thêm <color=#f26c1c>1 tầng</color>.\n\nHồi phục HP bằng <color=#f26c1c>30%</color> HP tối đa của Suomi và hồi phục <color=#f26c1c>4 điểm</color> Chỉ Số Ổn Định cho tất cả đơn vị đồng minh. Tất cả đồng minh (ngoại trừ bản thân) nhận thêm <color=#f26c1c>1 lớp</color> <color=#3487e0>Pháo Đài Băng Tuyết</color>.\n\nNếu đơn vị đồng minh đang đầy HP trước khi được trị liệu, họ nhận thêm <color=#f26c1c>1 lớp</color> <color=#3487e0>Yểm Hộ</color> và trạng thái <color=#3487e0>Duy Trì Chữa Lành I</color> trong <color=#f26c1c>3 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Bài Ca Chúc Phúc",
                "effect": "Khi bắt đầu chiến đấu, tự động tạo ra ô địa hình Tuyết Phủ có bán kính <color=#f26c1c>3 ô</color> quanh bản thân trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Nhịp Điệu Tuyết",
                "effect": "Khi đồng minh đứng trên ô Tuyết Phủ kết thúc hành động, hồi phục HP bằng <color=#f26c1c>15%</color> Tấn Công của Suomi."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Ánh Sáng Tuyết Nguyên",
                "effect": "Khi đồng minh nhận trị liệu từ Ánh Sáng Tuyết Nguyên, giải trừ thêm <color=#f26c1c>1</color> hiệu ứng Debuff."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Lũ Cuộn",
                "effect": "Phạm vi ảnh hưởng của Lũ Cuộn mở rộng thêm <color=#f26c1c>1 ô</color> và tăng sát thương gây ra thêm <color=#f26c1c>15%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Pháo Đài Băng Tuyết",
                "effect": "Lá Chắn nhận từ Pháo Đài Băng Tuyết tăng thêm <color=#f26c1c>20%</color> và đồng minh nhận thêm <color=#3487e0>Hỗ Trợ Phòng Thủ</color>."
            }
        ]
    },
    "tololo": {
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ánh Sáng Chói Lòa",
                "effect": "Khi bắt đầu chiến đấu, Tololo nhận thêm <color=#f26c1c>2 tầng</color> <color=#3487e0>Gai Ánh Sáng</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Va Chạm Siêu Tân Tinh",
                "effect": "Nếu đang chịu ảnh hưởng từ <color=#f26c1c>3</color> Buff trở lên, đòn tấn công này gây <color=#2caadb>ST Hóa Lỏng</color>, đồng thời nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Sao Tận Diệt",
                "effect": "Nếu đang chịu ảnh hưởng từ <color=#f26c1c>3</color> Buff trở lên, sát thương gây ra tăng <color=#f26c1c>30%</color> và giảm thời gian hồi chiêu của kỹ năng này đi <color=#f26c1c>3 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Màn Cực Quang",
                "effect": "Khi kích hoạt Tăng Hành Động, nhận thêm <color=#3487e0>Chuẩn Xác Tăng II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Va Chạm Siêu Tân Tinh",
                "effect": "Sát thương của Va Chạm Siêu Tân Tinh tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Sao Rơi",
                "effect": "Khi Sao Rơi tiêu diệt mục tiêu, hồi phục ngay lập tức <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            }
        ]
    },
    "klukai": {
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ăn Mòn Áp Đảo",
                "effect": "Sát thương gây ra lên mục tiêu đã chịu <color=#3487e0>Độc Tính Xâm Nhập</color> tăng thêm <color=#f26c1c>30%</color>.\n\nNếu mục tiêu không bị tiêu diệt bởi sát thương này, đòn đánh vẫn kích hoạt hiệu ứng khi tử trận của Độc Tính Xâm Nhập.\n\nĐộc Tính Xâm Nhập nhận thêm hiệu ứng: Khi mục tiêu mang hiệu ứng này kết thúc hành động, người thi triển sẽ áp dụng Độc Tính Xâm Nhập trong <color=#f26c1c>2 hiệp</color> lên các đơn vị địch trong phạm vi 3 ô chưa có Độc Tính Xâm Nhập."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Niềm Tự Hào Của Tinh Anh",
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 tầng</color> <color=#3487e0>Hiếu Thắng</color>. Khi đơn vị đồng minh khác gây <color=#8679e8>ST Ăn Mòn</color>, Klukai có thể nhận <color=#f26c1c>1 tầng</color> Hiếu Thắng. Giới hạn số tầng của Hiếu Thắng tăng thêm <color=#f26c1c>4 tầng</color>.\n\nMỗi khi nhận được <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu, áp dụng thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> cho kẻ địch đã có Áp Chế Ăn Mòn Mạnh, đồng thời giảm thời gian hồi chiêu Tuyệt Kỹ của Klukai đi <color=#f26c1c>1 hiệp</color>.\n\nÁp Chế Ăn Mòn Mạnh nhận thêm hiệu ứng: Khi Klukai thực hiện tấn công chủ động hoặc đồng minh khác gây ST Ăn Mòn, áp dụng thêm 1 tầng Áp Chế Ăn Mòn Mạnh cho mục tiêu đã có hiệu ứng này. Phòng Thủ giảm <color=#f26c1c>1%</color> và giới hạn số tầng tối đa tăng thêm <color=#f26c1c>5 tầng</color>."
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
                "effect": "Tầm bắn hiệu dụng tăng thêm <color=#f26c1c>2 ô</color>, sát thương tăng lên <color=#f26c1c>110%</color> Tấn Công. Phạm vi lan truyền của <color=#3487e0>Độc Tính Xâm Nhập</color> tăng thêm <color=#f26c1c>1 ô</color> và sát thương gây ra tăng lên <color=#f26c1c>80%</color> Tấn Công. Nếu mục tiêu đang chịu Debuff Ăn Mòn, áp dụng Độc Tính Xâm Nhập trong <color=#f26c1c>2 hiệp</color> trước khi tấn công.\n\nĐộc Tính Xâm Nhập nhận thêm hiệu ứng: Khi nhận đòn tấn công chủ động từ Klukai, sát thương phải chịu tăng thêm <color=#f26c1c>30%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Lướt Hủy Diệt",
                "effect": "Bỏ qua hiệu ứng giảm thương của Vật Cản (Yểm Hộ).\n\nĐộ rộng đường đi tăng thêm <color=#f26c1c>2 ô</color> và áp dụng trạng thái <color=#3487e0>Hoảng Sợ</color> trong <color=#f26c1c>2 hiệp</color>.\n\nSau khi tấn công, kích hoạt hiệu ứng của <color=#3487e0>Áp Chế Ăn Mòn Mạnh</color> trên tất cả kẻ địch và kích hoạt hiệu ứng khi tử trận của <color=#3487e0>Độc Tính Xâm Nhập</color>."
            }
        ]
    },
    "balthilde": {
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Nghi Thức Tăng Viện",
                "effect": "Thời gian tồn tại của Cấu Trúc Phòng Thủ tăng thêm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Nghi Thức Tăng Viện",
                "effect": "Tầm hiệu lực của Ý Thức An Toàn và Bảo Dưỡng Tập Trung tăng lên <color=#f26c1c>5 ô</color>.\n\nÝ Thức An Toàn nhận thêm hiệu ứng: Khi được triệu hồi, hồi phục độ bền của tất cả Vật Cản trong phạm vi 5 ô.\n\nBảo Dưỡng Tập Trung nhận thêm hiệu ứng: Hồi phục HP bằng <color=#f26c1c>100%</color> Phòng Thủ, <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định và áp dụng <color=#3487e0>Phòng Thủ Tăng I</color> cho tất cả đồng minh trong phạm vi 5 ô khi kết thúc hành động của họ."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Đập Vụn Bằng Búa",
                "effect": "Khi tấn công kẻ địch đang mang Khe Nứt Ứng Lực, ST gây ra tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Hàn Gắn Cơ Cấu",
                "effect": "Khi hồi phục cho Cấu Trúc Phòng Thủ, bản thân nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Giảm ST II</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Nghi Thức Tăng Viện",
                "effect": "Thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>1 hiệp</color>. Tấn Công và Phòng Thủ kế thừa của Cấu Trúc Phòng Thủ tăng lên <color=#f26c1c>100%</color>.\n\nCường hóa Ý Thức An Toàn: Khi được triệu hồi, hồi phục HP bằng <color=#f26c1c>200%</color> Phòng Thủ và <color=#f26c1c>4 điểm</color> Chỉ Số Ổn Định.\n\nCường hóa Bảo Dưỡng Tập Trung: Hiệu ứng giảm sát thương được áp dụng cho tất cả đồng minh."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Nghi Thức Tăng Viện",
                "effect": "Khi Cấu Trúc Phòng Thủ bị phá hủy, gây ST Băng Kết AoE bằng <color=#f26c1c>100%</color> Phòng Thủ của Balthilde lên tất cả kẻ địch xung quanh trong phạm vi 2 ô."
            }
        ]
    },
    "belka": {
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Tích Điện Trong Rừng",
                "effect": "Khi bắt đầu chiến đấu, Belka nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Điện Tích Âm</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tác Chiến Tích Cực",
                "effect": "Khi kích hoạt Tác Chiến Tích Cực, tăng thêm <color=#f26c1c>15%</color> Tỷ Lệ Bạo Kích."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Tia Chớp Rừng Sâu",
                "effect": "Tia Chớp Rừng Sâu áp dụng thêm <color=#3487e0>Dẫn Điện</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Ẩn Náu",
                "effect": "Khi ở trạng thái Ẩn Náu, ST Bạo Kích tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Nhảy Vọt Rừng Già",
                "effect": "ST Ổn Định gây ra tăng thêm <color=#f26c1c>2 điểm</color>. ST Bạo Kích của đòn tấn công này tăng <color=#f26c1c>30%</color>.\n\nSát thương của đòn tấn công này tăng thêm dựa trên <color=#f26c1c>6%</color> × số lượng <color=#3487e0>Điện Tích Âm</color> trên sân, tối đa tăng <color=#f26c1c>30%</color>. Nếu mục tiêu là đơn vị Boss và có Điện Tích Âm, sát thương tăng ngay lập tức lên <color=#f26c1c>30%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Tác Chiến Tích Cực",
                "effect": "Khi hạ gục kẻ địch có Điện Tích Âm, hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu và nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            }
        ]
    },
    "cheyanne": {
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Rút Lui Chiến Thuật",
                "effect": "Sau khi dùng Rút Lui Chiến Thuật, nhận thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Đài Hoa E Thẹn</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Quan Sát Điềm Tĩnh",
                "effect": "Tầm thi triển của Quan Sát Điềm Tĩnh mở rộng thêm <color=#f26c1c>2 ô</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Kiên Trì Truy Đuổi",
                "effect": "Hiệu ứng <color=#3487e0>Tâm Bia</color> được cường hóa: Giảm Phòng Thủ tăng lên <color=#f26c1c>100%</color>; khi bị Cheyanne tấn công, không còn tiêu hao <color=#3487e0>Giá Trị Phân Tích</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Hỏa Lực Che Phủ",
                "effect": "Tạo ô địa hình Khói trong phạm vi 2 ô quanh điểm rơi trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Đài Hoa E Thẹn",
                "effect": "Hiệu ứng tăng Tấn Công của Đài Hoa E Thẹn tăng thêm <color=#f26c1c>10%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Quan Sát Điềm Tĩnh",
                "effect": "Sau khi dùng Quan Sát Điềm Tĩnh, nhận ngay <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            }
        ]
    },
    "faye": {
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Săn Đuổi Không Ngừng",
                "effect": "Khi bắt đầu chiến đấu, Faye nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Di Hình</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Cú Bắn Tàn Nhẫn",
                "effect": "Cú Bắn Tàn Nhẫn gây thêm <color=#f26c1c>2 điểm</color> ST Ổn Định lên mục tiêu có <color=#3487e0>Liệt Thương</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Vũ Điệu Bóng Đêm",
                "effect": "Khi tiêu diệt kẻ địch, nhận thêm <color=#f26c1c>3 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Không Ai Sống Sót",
                "effect": "Hiệu ứng áp dụng Vết Thương lên tất cả kẻ địch xung quanh Faye mang Liệt Thương được đổi thành: Áp dụng <color=#f26c1c>4 tầng</color> <color=#3487e0>Vết Thương</color> cho tất cả đơn vị địch trên sân. Với kẻ địch đang mang tầng <color=#3487e0>Liệt Thương</color>, áp dụng thêm số tầng Vết Thương tương ứng với số tầng Liệt Thương của họ.\n\nKhi Faye kết thúc hành động, kích hoạt sát thương của toàn bộ các tầng Vết Thương mà không tiêu hao số tầng."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Cú Bắn Tàn Nhẫn",
                "effect": "Sát thương của Cú Bắn Tàn Nhẫn tăng thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 6,
                "level": 2,
                "skill": "Không Ai Sống Sót",
                "effect": "Không Ai Sống Sót áp dụng thêm trạng thái <color=#3487e0>Vô Hiệu Hóa Di Chuyển</color> cho mục tiêu chính trong <color=#f26c1c>1 hiệp</color>."
            }
        ]
    }
}

def main():
    print(f"Loading {I18N_PATH}...")
    with open(I18N_PATH, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    chars = bundle.setdefault("characters", {})
    for slug, updates in UPDATES.items():
        if slug in chars:
            print(f"Patching {slug}...")
            char_data = chars[slug]
            for key, val in updates.items():
                char_data[key] = val
        else:
            print(f"Warning: {slug} not found in characters!")

    tx = RepositoryTransaction(ROOT)
    try:
        stage_i18n_bundle(ROOT, tx, bundle)
        tx.commit()
        print("Successfully patched data/i18n_vi.json and site/static/js/i18n-vi.js!")
    except Exception as e:
        tx.rollback()
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
