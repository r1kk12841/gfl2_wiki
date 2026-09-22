"""
tools/batch3_data/group1.py
Batch 3 - Group 1: Springfield, Peritya, Vepley, Mosin-Nagant.
"""

GROUP_1_DATA = {
    "springfield": {
        "name": "Springfield",
        "en_name": "Springfield",
        "class": "Hỗ Trợ",
        "phase": "Hóa Lỏng",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Bắn Tỉa",
        "ammo_type": "Đạn Nặng",
        "signature_weapon": "Hào Quang",
        "weakness": "Dẫn Điện",
        "server": "global",
        "skills": [
            {
                "name": "Tiếp Cận Dịu Dàng",
                "tags": ["Đánh Thường", "Chuẩn Xác"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Thao Túng Tình Báo",
                "tags": ["Chủ Động", "Chuẩn Xác", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, áp dụng <color=#3487e0>Tình Báo Giả</color> trong <color=#f26c1c>2 hiệp</color>. Gây ST Hóa Lỏng bằng <color=#f26c1c>130%</color> Tấn Công và áp dụng <color=#3487e0>Đình Trệ</color> trong <color=#f26c1c>1 hiệp</color>. Springfield nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Trợ Giúp Kịp Thời",
                "tags": ["Chủ Động", "Trị Liệu", "Cường Hóa"],
                "description": "Chọn 1 đơn vị đồng minh <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>. Hồi phục lượng HP bằng <color=#f26c1c>100%</color> Tấn Công và <color=#f26c1c>3 điểm</color> Chỉ Số Ổn Định, đồng thời áp dụng <color=#3487e0>Vô Cùng Quan Tâm</color> trong <color=#f26c1c>2 hiệp</color> (thời lượng giảm vào cuối hiệp hiện tại). Springfield nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Hành Trình Bảo Vệ",
                "tags": ["Tuyệt Kỹ", "AoE", "Triệu Hồi"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color> và triệu hồi <color=#3487e0>Tayz</color> đi theo mục tiêu đó trong <color=#f26c1c>2 hiệp</color> (thời lượng giảm vào cuối hiệp hiện tại). Áp dụng <color=#3487e0>Ẩm Ướt</color> và <color=#3487e0>Tình Báo Giả</color> lên mục tiêu chỉ định và tất cả đơn vị địch <color=#f26c1c>trong phạm vi 3 ô xung quanh mục tiêu</color> trong <color=#f26c1c>2 hiệp</color>, đồng thời gây ST Hóa Lỏng AoE bằng <color=#f26c1c>80%</color> Tấn Công.\n\nÁp dụng <color=#3487e0>Tình Cảm Sâu Sắc</color> và <color=#3487e0>Vô Cùng Quan Tâm</color> lên toàn bộ đồng minh trong <color=#f26c1c>2 hiệp</color> (thời lượng giảm vào cuối hiệp hiện tại). Hồi phục cho tất cả đồng minh lượng HP bằng <color=#f26c1c>100%</color> Tấn Công và <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định, giải trừ <color=#f26c1c>1</color> Debuff, đồng thời xóa bỏ trạng thái <color=#3487e0>Khiêu Khích</color> và <color=#3487e0>Chạy Trốn</color> trên toàn phe ta.\n\nKhi mục tiêu mà Tayz bám theo tử trận, Tayz sẽ chuyển sang bám theo đơn vị địch có lượng HP hiện tại cao nhất. Springfield nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Đại Bàng Cảnh Giác",
                "tags": ["Bị Động", "Cường Hóa", "Phản Kích"],
                "description": "Khi kết thúc hành động của Springfield, nếu Chỉ Số Nhiên Liệu đạt tối đa, tiêu hao toàn bộ điểm để nhận <color=#3487e0>Tăng Hành Động</color>.\n\nKhi bắt đầu hiệp, nếu HP của Springfield cao hơn <color=#f26c1c>80%</color>, nhận <color=#3487e0>Nhìn Thấu</color> trong <color=#f26c1c>2 hiệp</color>. Nếu mục tiêu bị Tayz bám theo gây sát thương lên đồng minh, Tayz thực hiện <color=#3487e0>Phản Kích</color> lên kẻ đó, gây ST Hóa Lỏng bằng <color=#f26c1c>20%</color> HP tối đa của Springfield cùng <color=#f26c1c>1 điểm</color> ST Ổn Định, đồng thời trị liệu cho đồng minh lượng HP bằng <color=#f26c1c>20%</color> HP tối đa của Springfield. Kích hoạt tối đa <color=#f26c1c>2 lần</color> mỗi hiệp.\n\nKhi Tayz có mặt trên sân, Springfield hồi phục lượng HP bằng <color=#f26c1c>20%</color> HP tối đa khi kết thúc hành động."
            }
        ],
        "summons": [
            {
                "name": "Tayz",
                "type": "Vật Triệu Hồi Vật Lý",
                "description": "Thiết bị bay hộ vệ đi theo mục tiêu đồng minh hoặc đối phương, thực hiện Phản Kích và Hành Động Chi Viện đồng thời hỗ trợ hồi phục sinh lực cho đồng đội.",
                "stats": {
                    "hp": "200% HP ban đầu của Springfield",
                    "atk": "100% Tấn Công ban đầu của Springfield",
                    "def": "100% Phòng Thủ ban đầu của Springfield"
                },
                "skills": []
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Trợ Giúp Kịp Thời",
                "effect": "Lượng HP hồi phục tăng lên <color=#f26c1c>130%</color> Tấn Công. Hiệu ứng của Vô Cùng Quan Tâm được cường hóa: lượng HP hồi phục tăng lên <color=#f26c1c>15%</color> Tấn Công. Mức chuyển hóa tăng cường ST Hóa Lỏng tối đa tăng lên <color=#f26c1c>70%</color>. Ngoài ra, áp dụng <color=#f26c1c>6 tầng</color> <color=#3487e0>Cảm Ứng Đồng Tâm</color> lên đơn vị được chọn."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Hành Trình Bảo Vệ",
                "effect": "Lượng Chỉ Số Nhiên Liệu nhận được tăng thêm <color=#f26c1c>1 điểm</color>. HP hồi phục tăng lên <color=#f26c1c>120%</color> Tấn Công, Chỉ Số Ổn Định hồi phục tăng thêm <color=#f26c1c>4 điểm</color>, giải trừ thêm <color=#f26c1c>1</color> Debuff. Đồng thời xóa bỏ trạng thái <color=#3487e0>Choáng</color> và <color=#3487e0>Dẫn Dụ</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Đại Bàng Cảnh Giác",
                "effect": "Bổ sung hiệu ứng cho Tayz: Tăng ST Hóa Lỏng mà mục tiêu bị bám theo và tất cả kẻ địch trong phạm vi 3 ô xung quanh phải gánh chịu thêm <color=#f26c1c>10%</color>.\n\nKhi Tayz trên sân, ST Hóa Lỏng từ các đòn tấn công ngoài hiệp của phe ta tăng thêm <color=#f26c1c>40%</color>.\n\nBổ sung hiệu ứng chi viện: Khi đồng minh tấn công chủ động gây ST Hóa Lỏng lên mục tiêu bị Tayz bám theo, Tayz thực hiện <color=#3487e0>Hành Động Chi Viện</color>, gây ST Hóa Lỏng bằng <color=#f26c1c>20%</color> HP tối đa của Springfield cùng <color=#f26c1c>1 điểm</color> ST Ổn Định và hồi máu cho đồng minh bằng <color=#f26c1c>20%</color> HP tối đa của Springfield. Kích hoạt tối đa <color=#f26c1c>2 lần</color> mỗi hiệp."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Thao Túng Tình Báo",
                "effect": "Sát thương gây ra tăng lên <color=#f26c1c>150%</color> Tấn Công. Khi kẻ địch mang Tình Báo Giả rơi vào Sụp Đổ Ổn Định, ST Hóa Lỏng phải chịu tăng lên <color=#f26c1c>20%</color>. Đình Trệ chuyển hóa thành <color=#3487e0>Rét Buốt</color> duy trì <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Hành Trình Bảo Vệ",
                "effect": "Phạm vi hiệu lực tăng thêm <color=#f26c1c>1 ô</color>. Tình Cảm Sâu Sắc nhận hiệu ứng mới: Giảm sát thương nhận vào <color=#f26c1c>15%</color> và thời lượng tăng thêm <color=#f26c1c>1 hiệp</color>.\n\nTăng thời lượng của Tayz thêm <color=#f26c1c>1 hiệp</color>. Khi mục tiêu bị Tayz bám theo tử trận, gây ST cố định bằng <color=#f26c1c>40%</color> Tấn Công của Springfield lên toàn bộ kẻ địch trong bán kính 4 ô."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Đại Bàng Cảnh Giác",
                "effect": "Tayz được nâng cấp thành Tayz Đột Kích. Tất cả hệ số đòn đánh của Tayz Đột Kích tăng gấp đôi: Hệ số ST Hóa Lỏng tăng thêm <color=#f26c1c>20%</color>, ST Ổn Định tăng thêm <color=#f26c1c>1 điểm</color>, hệ số hồi phục HP tăng thêm <color=#f26c1c>20%</color> và số lần kích hoạt tăng thêm <color=#f26c1c>2 lần</color> mỗi hiệp. Trước khi tấn công, áp dụng <color=#3487e0>Phân Tích Lỗ Hổng</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Lõi Tụ Hợp",
                "effect": "Khi dùng Tuyệt kỹ Hành Trình Bảo Vệ, kéo tất cả mục tiêu trúng đòn <color=#f26c1c>3 ô</color> về tâm điểm hiệu ứng."
            },
            {
                "name": "Khóa Cố Định 2 - Thu Thập Tin Tức",
                "effect": "Trước khi tấn công chủ động, Springfield giải trừ <color=#f26c1c>1</color> Buff của mục tiêu."
            },
            {
                "name": "Khóa Cố Định 3 - Liên Kết Không Gian",
                "effect": "Khi Tayz có mặt trên sân, Phòng Thủ của toàn bộ đồng minh tăng <color=#f26c1c>10%</color>."
            },
            {
                "name": "Khóa Cố Định 4 - Đọc Vị Tâm Trí",
                "effect": "Nếu HP mục tiêu thấp hơn <color=#f26c1c>80%</color>, hiệu quả trị liệu tăng thêm <color=#f26c1c>15%</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Sau Lưng Nụ Cười",
                "effect": "Trước khi tấn công chủ động, Springfield áp dụng nhược điểm Hóa Lỏng lên mục tiêu trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 6 - Chăm Sóc Dịu Êm",
                "effect": "Khi trị liệu cho mục tiêu đang trong trạng thái Sụp Đổ Ổn Định, hồi phục thêm <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho mục tiêu."
            },
            {
                "name": "Khóa Tương Thích - Trái Tim Ấm Áp",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%"
            },
            {
                "name": "Khóa Chung - Chu Đáo Tỉ Mỉ",
                "effect": "HP +5.0% / Khi bắt đầu hiệp, nếu Chỉ Số Ổn Định chưa đầy, nhận <color=#3487e0>Hồi Phục Ổn Định Liên Tục II</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Mở Rộng - Khế Ước Cảnh Giác",
                "effect": "Hiệu quả của Trợ Giúp Kịp Thời áp dụng lên toàn bộ đồng minh. Sau khi dùng Hành Trình Bảo Vệ, triệu hồi Elsin xung quanh mục tiêu. Nếu Elsin đã có mặt, sát thương gây ra bởi Vật Triệu Hồi của phe ta tăng <color=#f26c1c>50%</color>. Mỗi khi Vật Triệu Hồi khác của đồng minh hoặc Tayz gây ST Hóa Lỏng, áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Bão Hòa</color> lên mục tiêu. Khi kích hoạt kỹ năng bị động Mổ Bắt của Elsin, tiêu hao Bão Hòa; với mỗi tầng tiêu hao, hệ số sát thương của Mổ Bắt tăng <color=#f26c1c>5%</color>."
            }
        ]
    },
    "peritya": {
        "name": "Peritya",
        "en_name": "Peritya",
        "class": "Vệ Binh",
        "phase": "Ăn Mòn",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Máy",
        "ammo_type": "Đạn Nặng",
        "signature_weapon": "Ảo Giác Quang Học",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Ghi Đè Thần Tốc",
                "tags": ["Đánh Thường", "Chuẩn Xác"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Ăn Mòn Cố Định",
                "tags": ["Chủ Động", "AoE", "Giải Trừ"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Ăn Mòn AoE bằng <color=#f26c1c>85%</color> Tấn Công lên mục tiêu và tất cả kẻ địch <color=#f26c1c>trong phạm vi 3×3 ô</color>, đồng thời giải trừ <color=#f26c1c>1</color> Buff."
            },
            {
                "name": "Áp Chế Lãnh Địa",
                "tags": ["Chủ Động", "AoE", "Dịch Chuyển"],
                "description": "Chọn 1 ô địa hình <color=#f26c1c>trong phạm vi 8 ô xung quanh</color> làm tâm điểm. Gây ST Vật Lý AoE bằng <color=#f26c1c>90%</color> Tấn Công lên tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 1 ô</color> quanh tâm và kéo chúng <color=#f26c1c>1 ô</color> về phía tâm. Cứ đánh trúng 1 mục tiêu, giảm thời gian hồi chiêu của kỹ năng này đi <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Đa Đoạn Biên Soạn",
                "tags": ["Tuyệt Kỹ", "AoE"],
                "description": "Gây ST Ăn Mòn AoE bằng <color=#f26c1c>100%</color> Tấn Công lên tất cả kẻ địch <color=#f26c1c>trong phạm vi 9×9 ô</color> lấy bản thân làm tâm, ngoại trừ phạm vi 5×5 ô bên trong. Cứ đánh trúng 1 mục tiêu, sát thương gây ra tăng thêm <color=#f26c1c>5%</color>, tối đa tăng <color=#f26c1c>15%</color>."
            },
            {
                "name": "Phản Ứng Dây Chuyền",
                "tags": ["Bị Động", "Hỗ Trợ"],
                "description": "Khi kẻ địch trong tầm bắn nhận ST AoE từ đồng minh, thực hiện <color=#3487e0>Hành Động Chi Viện</color>, gây ST Vật Lý AoE bằng <color=#f26c1c>50%</color> Tấn Công và <color=#f26c1c>1 điểm</color> ST Ổn Định, đồng thời nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Kích hoạt tối đa <color=#f26c1c>6 lần</color> mỗi hiệp.\n\nTrước khi tấn công, mỗi điểm di chuyển còn lại gia tăng sát thương thêm <color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>30%</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Ăn Mòn Cố Định",
                "effect": "Số lượng Buff bị giải trừ tăng thêm <color=#f26c1c>2</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Áp Chế Lãnh Địa",
                "effect": "Phạm vi hiệu lực tăng thêm <color=#f26c1c>1 ô</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Đa Đoạn Biên Soạn",
                "effect": "Mỗi kẻ địch trúng đòn giúp tăng thêm <color=#f26c1c>5%</color> sát thương, tối đa tăng lên <color=#f26c1c>25%</color>."
            },
            {
                "tier": 4,
                "level": 3,
                "skill": "Đa Đoạn Biên Soạn",
                "effect": "Khu vực loại trừ thu hẹp lại thành phạm vi 3×3 ô bên trong vùng 9×9 ô lấy bản thân làm tâm."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Phản Ứng Dây Chuyền",
                "effect": "Nếu không di chuyển trước khi tấn công chủ động, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu sau khi kết thúc đòn đánh."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Phản Ứng Dây Chuyền",
                "effect": "Số lần kích hoạt Hành Động Chi Viện tăng thêm <color=#f26c1c>4 lần</color> mỗi hiệp."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Bảo Trì Tạm Thời",
                "effect": "Cứ gây mỗi <color=#f26c1c>10 điểm</color> ST Ổn Định, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 2 - Mèo Vờn Chuột",
                "effect": "Nếu còn điểm di chuyển trước khi tấn công, nhận <color=#3487e0>Di Chuyển Tăng II</color> khi kết thúc hành động trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Khóa Cố Định 3 - Tự Động Phục Hồi",
                "effect": "Nếu không di chuyển trước khi tấn công, giải trừ <color=#f26c1c>2</color> Debuff trên bản thân."
            },
            {
                "name": "Khóa Cố Định 4 - Chống Cự Lười Biếng",
                "effect": "Tăng sát thương từ kỹ năng chủ động Áp Chế Lãnh Địa lên mục tiêu miễn dịch hiệu ứng dịch chuyển thêm <color=#f26c1c>15%</color>."
            },
            {
                "name": "Khóa Cố Định 5 - Nghỉ Ngơi Chốc Lát",
                "effect": "Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "name": "Khóa Cố Định 6 - Tiếp Xúc Thân Mật",
                "effect": "Tăng ST Ổn Định gây ra lên mục tiêu chính bởi kỹ năng Ăn Mòn Cố Định thêm <color=#f26c1c>4 điểm</color>."
            },
            {
                "name": "Khóa Tương Thích - Mèo Lười Thư Thái",
                "effect": "Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Toàn Lực Công Kích",
                "effect": "TL Bạo Kích +5.0% / Nếu kỹ năng chủ động đánh trúng từ 2 mục tiêu địch trở lên, sát thương gây ra tăng <color=#f26c1c>7%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Dịch Mã Tận Thế",
                "effect": "Khi gây ST Ăn Mòn, với mỗi Debuff trên mục tiêu, tăng sát thương gây ra thêm <color=#f26c1c>5%</color>, tối đa tăng <color=#f26c1c>25%</color>.\n\nĐa Đoạn Biên Soạn kéo tất cả kẻ địch trúng đòn về phía bản thân <color=#f26c1c>2 ô</color>.\n\nTrong cùng 1 hiệp, cứ mỗi <color=#f26c1c>2 lần</color> thực hiện Hành Động Chi Viện, đòn Hành Động Chi Viện kế tiếp sẽ gây ST Ăn Mòn AoE bằng <color=#f26c1c>50%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định lên mục tiêu và tất cả kẻ địch trong phạm vi 3×3 ô xung quanh."
            }
        ]
    },
    "vepley": {
        "name": "Vepley",
        "en_name": "Vepley",
        "class": "Tiên Phong",
        "phase": "Vật Lý",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Shotgun",
        "ammo_type": "Đạn Shotgun",
        "signature_weapon": "Thợ Săn Trái Tim",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Tương Tác Trực Tiếp",
                "tags": ["Đánh Thường", "Chuẩn Xác"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 5 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Biểu Diễn Hết Mình",
                "tags": ["Chủ Động", "AoE", "Phá Hủy Vật Cản", "Dịch Chuyển"],
                "description": "Chọn 1 hướng, gây ST Vật Lý bằng <color=#f26c1c>75%</color> Tấn Công lên mục tiêu địch đầu tiên trên mỗi hàng trong phạm vi 3×5 ô theo hướng đã chọn và đẩy lùi mục tiêu <color=#f26c1c>4 ô</color>. Đồng thời phá hủy toàn bộ Vật Cản có thể phá hủy nằm ngoài phạm vi 3×3 ô quanh bản thân."
            },
            {
                "name": "Sân Khấu Độc Quyền",
                "tags": ["Chủ Động", "Chuẩn Xác", "Giải Trừ"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 5 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>150%</color> Tấn Công. Nếu mục tiêu mang Debuff di chuyển, bỏ qua <color=#f26c1c>10%</color> giảm thương từ Vật Cản. Nếu mục tiêu không được Vật Cản che chở, giải trừ <color=#f26c1c>2</color> Buff của kẻ đó trước khi tấn công."
            },
            {
                "name": "Nhiệt Huyết Lan Tỏa",
                "tags": ["Chủ Động", "AoE", "Suy Yếu"],
                "description": "Chọn 1 ô địa hình <color=#f26c1c>trong phạm vi 5 ô xung quanh</color> để tấn công, gây ST Vật Lý AoE bằng <color=#f26c1c>100%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 2 ô. Đồng thời áp dụng <color=#3487e0>Quá Khích</color> và <color=#3487e0>Dễ Bị Thương II</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Tài Năng Thần Tượng",
                "tags": ["Bị Động", "Suy Yếu"],
                "description": "Khi bắt đầu hành động, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Với mỗi lần gây sát thương, nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Sát thương gây ra lên mục tiêu mang Debuff di chuyển tăng <color=#f26c1c>20%</color>. Nếu đã di chuyển từ 5 ô trở lên, áp dụng <color=#3487e0>Di Chuyển Giảm II</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color> trước khi tấn công."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Biểu Diễn Hết Mình",
                "effect": "Nếu đánh trúng từ 2 mục tiêu trở lên, nhận <color=#f26c1c>3 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Sân Khấu Độc Quyền",
                "effect": "Nếu mục tiêu mang Debuff di chuyển, tỷ lệ bạo kích tăng thêm <color=#f26c1c>100%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Nhiệt Huyết Lan Tỏa",
                "effect": "Trạng thái Quá Khích được áp dụng trước khi tấn công thay vì sau đòn đánh."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Tài Năng Thần Tượng",
                "effect": "Chỉ cần di chuyển từ 3 ô trở lên, áp dụng Di Chuyển Giảm II lên mục tiêu trước khi tấn công."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Tài Năng Thần Tượng",
                "effect": "Nếu mục tiêu mang Debuff di chuyển, áp dụng <color=#3487e0>Cấm Di Chuyển</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Nhiệt Huyết Lan Tỏa",
                "effect": "Nếu chỉ đánh trúng 1 mục tiêu duy nhất, áp dụng <color=#3487e0>Choáng</color> trong <color=#f26c1c>1 hiệp</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Khoảng Cách An Toàn",
                "effect": "Tăng ST Ổn Định gây ra lên kẻ địch mang Debuff di chuyển thêm <color=#f26c1c>2 điểm</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Tuần Diễn Vùng Ô Nhiễm",
                "effect": "Phạm vi của Biểu Diễn Hết Mình đổi thành 5×3 ô, cự ly đẩy lùi đổi thành 1 ô."
            },
            {
                "name": "Khóa Cố Định 3 - May Mắn Của Thần Tượng",
                "effect": "Nếu không có đồng minh nào trong phạm vi 6 ô xung quanh, nhận 1 tầng <color=#3487e0>Lá Chắn Tốc Độ</color> khi kết thúc hành động."
            },
            {
                "name": "Khóa Cố Định 4 - Khủng Long Lướt Sóng",
                "effect": "Khi dùng Sân Khấu Độc Quyền, bỏ qua <color=#f26c1c>10%</color> giảm thương từ Vật Cản lên mục tiêu mang Debuff di chuyển."
            },
            {
                "name": "Khóa Cố Định 5 - Rèn Luyện Chống Căng Thẳng",
                "effect": "Nếu ở gần Vật Cản, giảm sát thương AoE phải gánh chịu đi <color=#f26c1c>20%</color>."
            },
            {
                "name": "Khóa Cố Định 6 - Cống Hiến Cho Sân Khấu",
                "effect": "Khi áp dụng Debuff di chuyển lên mục tiêu thể hình lớn, gây thêm 1 lần sát thương cố định bằng <color=#f26c1c>15%</color> Tấn Công."
            },
            {
                "name": "Khóa Tương Thích - Màn Ra Mắt Hoành Tráng",
                "effect": "Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Đòn Đánh Tan Chảy",
                "effect": "Tấn Công +5.0% / Nếu Điểm Di Chuyển của bản thân bằng hoặc cao hơn mục tiêu, sát thương gây ra tăng <color=#f26c1c>7%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Sân Khấu Rực Sáng",
                "effect": "Đòn đánh bỏ qua <color=#f26c1c>15%</color> Phòng Thủ của mục tiêu; nếu mục tiêu mang Debuff di chuyển, bỏ qua thêm <color=#f26c1c>15%</color> Phòng Thủ.\n\nBiểu Diễn Hết Mình: Áp dụng Choáng và Dễ Bị Thương II lên mục tiêu trong <color=#f26c1c>2 hiệp</color>."
            }
        ]
    },
    "mosin-nagant": {
        "name": "Mosin-Nagant",
        "en_name": "Mosin-Nagant",
        "class": "Vệ Binh",
        "phase": "Dẫn Điện",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Bắn Tỉa",
        "ammo_type": "Đạn Nặng",
        "signature_weapon": "Samosek",
        "weakness": "Ăn Mòn",
        "server": "global",
        "skills": [
            {
                "name": "Giờ Tuần Tra",
                "tags": ["Đánh Thường", "Chuẩn Xác"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Hồng Tâm Thắng Lợi",
                "tags": ["Chủ Động", "Chuẩn Xác", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Sau đòn đánh, áp dụng <color=#3487e0>Dẫn Điện</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Tâm Thái Tích Cực",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Tác Chiến Tích Cực</color> và 1 lần <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Cứ mỗi 3 lần sử dụng kỹ năng này, nhận trạng thái <color=#3487e0>Sốc Điện</color>. Chỉ có thể kích hoạt 1 lần mỗi hiệp."
            },
            {
                "name": "Tuyên Ngôn Thắng Lợi",
                "tags": ["Tuyệt Kỹ", "Chuẩn Xác", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>180%</color> Tấn Công. Nếu khai thác được Điểm Yếu Thuộc Tính, áp dụng <color=#3487e0>Tê Liệt</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color> sau khi tấn công."
            },
            {
                "name": "Sẵn Lòng Giúp Đỡ",
                "tags": ["Bị Động", "Hỗ Trợ", "Cường Hóa"],
                "description": "Khi đồng minh tấn công mục tiêu địch ngoài hiệp trong tầm bắn của Mosin-Nagant, nếu mục tiêu đang trong trạng thái Sụp Đổ Ổn Định, Mosin-Nagant thực hiện <color=#3487e0>Hành Động Chi Viện</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định. Kích hoạt tối đa <color=#f26c1c>2 lần</color> mỗi hiệp.\n\nSau đòn tấn công chi viện, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu và nhận <color=#3487e0>Nhìn Thấu</color> trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Hồng Tâm Thắng Lợi",
                "effect": "Nếu khai thác Điểm Yếu Thuộc Tính, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tuyên Ngôn Thắng Lợi",
                "effect": "Sau mỗi lần Hành Động Chi Viện, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Tự Tin Chiến Thắng</color>."
            },
            {
                "tier": 3,
                "level": 3,
                "skill": "Tuyên Ngôn Thắng Lợi",
                "effect": "Sau khi dùng Tuyệt kỹ, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu với mỗi tầng Tự Tin Chiến Thắng sở hữu."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Sẵn Lòng Giúp Đỡ",
                "effect": "Trước khi thực hiện Tấn Công Chi Viện, nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Tác Chiến Tích Cực</color>."
            },
            {
                "tier": 5,
                "level": 2,
                "skill": "Tâm Thái Tích Cực",
                "effect": "Tăng sát thương gây ra khi mang Tác Chiến Tích Cực thêm <color=#f26c1c>10%</color>. Cứ mỗi 2 lần dùng kỹ năng này, nhận Sốc Điện."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Sẵn Lòng Giúp Đỡ",
                "effect": "Khi một Debuff hệ Dẫn Điện được áp dụng lên mục tiêu ngoài hiệp, nhận <color=#3487e0>Chi Viện Tinh Anh</color>. Số lần Tấn Công Chi Viện tối đa tăng thêm <color=#f26c1c>1 lần</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Đội Tuần Tra An Ninh",
                "effect": "Nếu mục tiêu mang trạng thái Tê Liệt, tăng ST Ổn Định mục tiêu phải chịu thêm <color=#f26c1c>2 điểm</color>."
            },
            {
                "name": "Khóa Cố Định 2 - Phòng Tuyến Chuẩn Bị Trước",
                "effect": "Khi Hồng Tâm Thắng Lợi gây ST Dẫn Điện, áp dụng <color=#3487e0>Tê Liệt</color> trong <color=#f26c1c>1 hiệp</color> thay vì Dẫn Điện."
            },
            {
                "name": "Khóa Cố Định 3 - Di Chuyển Ngăn Nắp",
                "effect": "Nếu mục tiêu mang trạng thái Tê Liệt, áp dụng <color=#f26c1c>2</color> Debuff lên mục tiêu trước khi tấn công."
            },
            {
                "name": "Khóa Cố Định 4 - Tinh Thần Lạc Quan",
                "effect": "Khi dùng kỹ năng chủ động Tâm Thái Tích Cực, nếu bản thân có Sốc Điện, đòn đánh bỏ qua <color=#f26c1c>15%</color> giảm thương từ Vật Cản."
            },
            {
                "name": "Khóa Cố Định 5 - Chăm Chỉ Làm Việc",
                "effect": "Khi sở hữu Nhìn Thấu, giảm ST Ổn Định phải gánh chịu đi <color=#f26c1c>1 điểm</color>."
            },
            {
                "name": "Khóa Cố Định 6 - Tuần Tra Cơ Động",
                "effect": "Nếu đòn tấn công chủ động áp dụng Tê Liệt lên mục tiêu, nhận <color=#f26c1c>3 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color>."
            },
            {
                "name": "Khóa Tương Thích - Trái Tim Vàng",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%"
            },
            {
                "name": "Khóa Chung - Mắt Thần Tinh Tường",
                "effect": "Tấn Công +5.0% / Khi chịu hiệu ứng Nhìn Thấu, sát thương gây ra tăng <color=#f26c1c>7%</color>."
            },
            {
                "name": "Khóa Mở Rộng - Tử Thần Trắng",
                "effect": "Khi đồng minh kích hoạt Tê Liệt lên mục tiêu, Mosin-Nagant chuyển hóa thành áp dụng Tia Lửa Điện lên mục tiêu trong <color=#f26c1c>1 hiệp</color>. Kích hoạt tối đa 1 lần mỗi hiệp."
            }
        ]
    }
}
