"""
tools/batch5_data/group1.py
Batch 5 - Group 1: Faelynn, Harpsy, Koleda, Lainie.
"""

GROUP_1_DATA = {
    "faelynn": {
        "name": "Faelynn",
        "en_name": "Faelynn",
        "class": "Vệ Binh",
        "phase": "Ăn Mòn",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Bristlefang Beast",
        "weakness": "Dẫn Điện",
        "server": "global",
        "skills": [
            {
                "name": "Liên Kích Răng Nanh",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Tam Trảo Phân Thân",
                "tags": ["Chủ Động", "AoE", "Ô Địa Hình", "Suy Yếu", "Khống Chế"],
                "description": "Chọn 1 đơn vị địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>60%</color> Tấn Công lên toàn bộ kẻ địch <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> mục tiêu, giải trừ <color=#f26c1c>1</color> Buff, áp dụng <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Đánh Dấu Hơi Thở</color>, đồng thời tạo ô địa hình <color=#3487e0>Độc Chướng</color> trong <color=#f26c1c>2 hiệp</color>. Cứ mỗi lớp <color=#3487e0>Theo Vết Thợ Săn</color> mục tiêu sở hữu, hệ số sát thương kỹ năng này tăng thêm <color=#f26c1c>5%</color>. Sau kỹ năng, Faelynn nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu và 1 Buff ngẫu nhiên trong <color=#f26c1c>2 hiệp lớn</color>."
            },
            {
                "name": "Thính Giác Nhạy Bén",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Faelynn nhận <color=#3487e0>Khát Máu Lang Thang</color> trong <color=#f26c1c>3 hiệp</color> và <color=#3487e0>Radar Tai Chó</color> trong <color=#f26c1c>2 hiệp</color>. Sau khi kỹ năng kết thúc, nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "name": "Săn Lùng Tận Trung",
                "tags": ["Tuyệt Kỹ", "AoE", "Ô Địa Hình"],
                "description": "Chọn một hướng và gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>120%</color> Tấn Công lên toàn bộ kẻ địch trong khu vực hình chữ nhật 3×9 ô phía trước theo hướng đã chọn, đồng thời tạo ra <color=#3487e0>Độc Chướng</color> trong <color=#f26c1c>2 hiệp</color>. Cứ mỗi lớp <color=#3487e0>Theo Vết Thợ Săn</color> mục tiêu sở hữu, hệ số sát thương tăng <color=#f26c1c>5%</color>. Sau khi kỹ năng kết thúc, nếu Faelynn có <color=#3487e0>Vồ Liên Tiếp</color>, tiêu hao 1 lớp để kích hoạt kỹ năng chủ động bổ sung Bản Năng Săn Bắn I và nhận Di Chuyển Thêm."
            },
            {
                "name": "Phản Kích Không Ngừng",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Khi bắt đầu trận chiến, Faelynn nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Vồ Liên Tiếp</color>, tối đa cộng dồn 3 lớp. Faelynn nhận thêm 1 lớp <color=#3487e0>Vồ Liên Tiếp</color> dựa trên số lượng kỹ năng chủ động đã sử dụng (không bao gồm Bản Năng Săn Bắn).\n\nKhi bắt đầu hiệp, nếu Faelynn ở trên ô địa hình Dị Vị, nhận 1 Tầm Di Chuyển và 1 lớp <color=#3487e0>Theo Vết Thợ Săn</color> dựa trên cấp độ của ô địa hình, duy trì 1 hiệp.\n\nNếu Faelynn chịu sát thương trên ô địa hình thuộc tính Ăn Mòn, chuyển 50% sát thương ban đầu phải chịu cho đơn vị đồng minh có HP hiện tại cao nhất (không bao gồm Faelynn).\n\nFaelynn miễn nhiễm với dịch chuyển, debuff di chuyển và các hiệu ứng cấm hành động."
            },
            {
                "name": "Bản Năng Săn Bắn I",
                "tags": ["Chủ Động", "AoE"],
                "description": "Chọn 1 đơn vị địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>60%</color> Tấn Công bỏ qua vật chắn lên toàn bộ kẻ địch trong phạm vi 3 ô quanh mục tiêu, và áp dụng <color=#3487e0>Ấn Ký Vòng Cổ</color>. Cứ mỗi lớp <color=#3487e0>Theo Vết Thợ Săn</color> sở hữu, hệ số sát thương tăng <color=#f26c1c>5%</color>.\nNếu chỉ đánh trúng 1 mục tiêu, hệ số sát thương tăng thêm <color=#f26c1c>30%</color>.\nSau khi dùng kỹ năng, nếu sở hữu <color=#3487e0>Vồ Liên Tiếp</color>, tiêu hao 1 lớp để kích hoạt kỹ năng chủ động bổ sung Bản Năng Săn Bắn II và nhận Di Chuyển Thêm."
            },
            {
                "name": "Bản Năng Săn Bắn II",
                "tags": ["Chủ Động", "AoE"],
                "description": "Chọn 1 đơn vị địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>120%</color> Tấn Công bỏ qua vật chắn lên toàn bộ kẻ địch trong phạm vi 3 ô quanh mục tiêu. Sát thương gây ra cho mục tiêu có <color=#3487e0>Ấn Ký Vòng Cổ</color> tăng <color=#f26c1c>50%</color>. Cứ mỗi lớp <color=#3487e0>Theo Vết Thợ Săn</color> sở hữu, hệ số sát thương tăng <color=#f26c1c>5%</color>.\nNếu chỉ đánh trúng 1 mục tiêu, hệ số sát thương tăng thêm <color=#f26c1c>30%</color>.\nSau khi dùng kỹ năng, nếu sở hữu <color=#3487e0>Vồ Liên Tiếp</color>, tiêu hao 1 lớp để kích hoạt kỹ năng chủ động bổ sung Bản Năng Săn Bắn III và nhận Di Chuyển Thêm."
            },
            {
                "name": "Bản Năng Săn Bắn III",
                "tags": ["Chủ Động", "AoE"],
                "description": "Chọn 1 đơn vị địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>240%</color> Tấn Công bỏ qua vật chắn lên toàn bộ kẻ địch trong phạm vi 3 ô quanh mục tiêu. Sát thương gây cho mục tiêu có <color=#3487e0>Ấn Ký Vòng Cổ</color> tăng <color=#f26c1c>100%</color>. Trước khi tấn công, nếu mục tiêu ở trên ô địa hình Dị Vị, cứ mỗi cấp của ô địa hình, Phòng Thủ của mục tiêu giảm <color=#f26c1c>14%</color> và ST Bạo Kích của Faelynn tăng <color=#f26c1c>5%</color>. Cứ mỗi lớp <color=#3487e0>Theo Vết Thợ Săn</color> sở hữu, hệ số sát thương tăng <color=#f26c1c>5%</color>.\nNếu chỉ đánh trúng 1 mục tiêu, hệ số sát thương tăng thêm <color=#f26c1c>30%</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Thính Giác Nhạy Bén",
                "effect": "Thời gian áp dụng <color=#3487e0>Radar Tai Chó</color> tăng thêm <color=#f26c1c>1 hiệp</color>. Cường hóa hiệu ứng của <color=#3487e0>Khát Máu Lang Thang</color>, tăng Tấn Công thêm <color=#f26c1c>30%</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Tam Trảo Phân Thân",
                "effect": "Phạm vi hiệu quả mở rộng lên <color=#f26c1c>5 ô xung quanh</color> mục tiêu, và cứ mỗi lớp <color=#3487e0>Theo Vết Thợ Săn</color>, hệ số sát thương tăng thêm <color=#f26c1c>10%</color>. Hệ số sát thương của <color=#3487e0>Đánh Dấu Hơi Thở</color> tăng lên <color=#f26c1c>100%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Săn Lùng Tận Trung",
                "effect": "Cứ mỗi lớp <color=#3487e0>Theo Vết Thợ Săn</color>, hệ số sát thương của KN Tuyệt Kỹ và KN chủ động Bản Năng Săn Bắn tăng <color=#f26c1c>10%</color>. Nếu Bản Năng Săn Bắn II tiêu diệt một mục tiêu mang <color=#3487e0>Ấn Ký Vòng Cổ</color>, lần sử dụng Bản Năng Săn Bắn tiếp theo trong hiệp này sẽ áp dụng <color=#3487e0>Ấn Ký Vòng Cổ</color>. Cường hóa hiệu ứng <color=#3487e0>Ấn Ký Vòng Cổ</color>: Sát thương Ăn Mòn phải chịu tăng <color=#f26c1c>30%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Phản Kích Không Ngừng",
                "effect": "Khi bắt đầu hiệp, nhận <color=#f26c1c>4 lớp</color> <color=#3487e0>Theo Vết Thợ Săn</color>. Số lớp cộng dồn tối đa của <color=#3487e0>Theo Vết Thợ Săn</color> tăng lên <color=#f26c1c>6 lớp</color>. Cường hóa hiệu ứng <color=#3487e0>Theo Vết Thợ Săn</color>: Sát thương Ăn Mòn gây ra tăng thêm <color=#f26c1c>5%</color>."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Tam Trảo Phân Thân",
                "effect": "Hệ số sát thương tăng lên <color=#f26c1c>120%</color>. Nếu đánh trúng từ 3 mục tiêu trở lên hoặc đánh trúng đơn vị Thủ Lĩnh, bồi thêm 1 lần ST Ăn Mòn AoE bằng <color=#f26c1c>120%</color> Tấn Công và <color=#f26c1c>1 điểm</color> ST Ổn Định lên mục tiêu. Cường hóa <color=#3487e0>Đánh Dấu Hơi Thở</color>, tăng <color=#f26c1c>30%</color> sát thương phải chịu từ Faelynn."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Săn Lùng Tận Trung",
                "effect": "Hệ số sát thương tăng lên <color=#f26c1c>150%</color>; Hệ số sát thương của 3 lần kích hoạt kỹ năng chủ động bổ sung Bản Năng Săn Bắn lần lượt tăng lên <color=#f26c1c>90%</color>, <color=#f26c1c>170%</color> và <color=#f26c1c>480%</color>. Mỗi lần dùng Bản Năng Săn Bắn sẽ gây sát thương 2 lần. Nếu Bản Năng Săn Bắn III tiêu diệt mục tiêu, nhận thêm <color=#f26c1c>1 lớp</color> <color=#3487e0>Vồ Liên Tiếp</color>, tối đa cộng dồn 2 lớp."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Đòn Kết Liễu Dango",
                "level": 20,
                "effect": "Tăng <color=#f26c1c>7%</color> ST gây ra lên các đơn vị địch không đầy HP.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Dựng Lông Đe Dọa",
                "level": 20,
                "effect": "Trước khi dùng kỹ năng chủ động bổ sung Bản Năng Săn Bắn, giải trừ <color=#f26c1c>1</color> Buff từ mục tiêu.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Tiếng Grừ Cuối Cùng",
                "level": 30,
                "effect": "Khi bản thân tử vong, gây ST Cố Định bằng <color=#f26c1c>500%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn Định lên toàn bộ kẻ địch trong phạm vi 6 ô quanh bản thân, tạo ô địa hình <color=#3487e0>Độc Chướng</color> và áp dụng <color=#3487e0>Đánh Dấu Hơi Thở</color> trong <color=#f26c1c>2 hiệp</color>. Nếu đơn vị địch không phải Thủ Lĩnh, bồi thêm ST Cố Định bằng <color=#f26c1c>300%</color> HP tối đa.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Bộ Pháp Kẻ Săn Mồi",
                "level": 30,
                "effect": "Khi bắt đầu hiệp, tạo ô địa hình <color=#3487e0>Độc Chướng</color> trong phạm vi 1 ô quanh bản thân, duy trì <color=#f26c1c>2 hiệp</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Giáp Lông Mềm",
                "level": 40,
                "effect": "Khi bản thân ở trên ô địa hình thuộc tính Ăn Mòn, sát thương phải chịu giảm <color=#f26c1c>15%</color> và ST Ổn Định phải chịu giảm <color=#f26c1c>1 điểm</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Đánh Hơi Con Mồi",
                "level": 40,
                "effect": "Khi bắt đầu trận chiến, áp dụng <color=#3487e0>Đánh Dấu Hơi Thở</color> lên đơn vị địch có HP cao nhất trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Hành Trình Lãng Mạn",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, TL Bạo Kích +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Uy Lực Loài Chó",
                "level": 40,
                "effect": "TL Bạo Kích +5.0% / Khi bắt đầu hiệp, nếu bản thân ở trên ô địa hình Dị Vị Cấp 3, ST AoE gây ra tăng <color=#f26c1c>10%</color> trong 1 hiệp lớn.",
                "materials": "None"
            }
        ]
    },
    "harpsy": {
        "name": "Harpsy",
        "en_name": "Harpsy",
        "class": "Tiên Phong",
        "phase": "Ăn Mòn",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Antinomy",
        "weakness": "Thiêu Đốt",
        "server": "global",
        "skills": [
            {
                "name": "Ngắm Bắn Thống Trị",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Khuếch Đại Cơ Bắp",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Chọn 1 đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color> và áp dụng <color=#3487e0>Tiến Trình Alpha</color> trong <color=#f26c1c>2 hiệp lớn</color>, đồng thời kéo dài <color=#3487e0>Tiến Trình Alpha</color> trên toàn bộ đồng minh thêm <color=#f26c1c>1 hiệp lớn</color>. Sau khi dùng kỹ năng, Harpsy nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Nếu mục tiêu đã có sẵn <color=#3487e0>Tiến Trình Alpha</color>, Harpsy hồi phục <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu. Kỹ năng này có thể dùng tối đa 1 lần mỗi hiệp."
            },
            {
                "name": "Lấy Độc Trị Độc",
                "tags": ["Chủ Động", "AoE", "Suy Yếu", "Dịch Chuyển"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>90%</color> Tấn Công, đẩy lùi mục tiêu <color=#f26c1c>3 ô</color> và áp dụng <color=#f26c1c>2 lớp</color> <color=#3487e0>Tiến Trình Tiêu Diệt</color>."
            },
            {
                "name": "Cú Đấm Bạch Kim",
                "tags": ["Tuyệt Kỹ", "AoE"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>90%</color> Tấn Công. Nếu số lượng Doll đồng minh có <color=#3487e0>Tiến Trình Alpha</color> trên sân từ 2 trở lên, sát thương do <color=#3487e0>Tiến Trình Tiêu Diệt</color> gây ra tăng <color=#f26c1c>30%</color> trong <color=#f26c1c>1 hiệp lớn</color>."
            },
            {
                "name": "Bậc Thầy Mã Độc",
                "tags": ["Bị Động"],
                "description": "Sau đòn tấn công chủ động, Harpsy hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.\n\nCứ mỗi 1 điểm Chỉ Số Nhiên Liệu tiêu hao bởi KN Tuyệt Kỹ, hiệu ứng của 1 <color=#3487e0>Tiến Trình Alpha</color> sẽ được kích hoạt."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Khuếch Đại Cơ Bắp",
                "effect": "Tiêu hao Chỉ Số Nhiên Liệu giảm <color=#f26c1c>1 điểm</color>, và số lần sử dụng tăng thêm <color=#f26c1c>1 lần</color> mỗi hiệp."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Cú Đấm Bạch Kim",
                "effect": "Nếu Harpsy có nhiều hơn 3 điểm Chỉ Số Nhiên Liệu, tiêu hao toàn bộ Chỉ Số Nhiên Liệu, và cứ mỗi điểm Chỉ Số Nhiên Liệu tiêu hao thêm sẽ tăng <color=#f26c1c>20%</color> hệ số sát thương."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Bậc Thầy Mã Độc",
                "effect": "Cứ mỗi lần kích hoạt <color=#3487e0>Tiến Trình Alpha</color>, tăng <color=#f26c1c>3%</color> Tấn Công và ST Bạo Kích của bản thân, tối đa tăng <color=#f26c1c>15%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Lấy Độc Trị Độc",
                "effect": "Hệ số sát thương tăng lên <color=#f26c1c>120%</color>.\nHiệu ứng <color=#3487e0>Tiến Trình Tiêu Diệt</color> được nâng cấp: Sau khi người sở hữu tử vong, toàn bộ số lớp hiệu ứng sẽ chuyển giao cho một đơn vị đồng minh ngẫu nhiên."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Cú Đấm Bạch Kim",
                "effect": "Hệ số sát thương tăng lên <color=#f26c1c>120%</color>.\nThêm hiệu ứng mới: Khi có Doll đồng minh mang <color=#3487e0>Tiến Trình Alpha</color> trên sân, hệ số sát thương của kỹ năng này được nhân đôi."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Lấy Độc Trị Độc",
                "effect": "Hiệu ứng <color=#3487e0>Tiến Trình Tiêu Diệt</color> được nâng cấp: Tiêu hao 70% số lớp (làm tròn lên) khi kích hoạt hiệu ứng, và hệ số sát thương của mỗi lớp tăng lên <color=#f26c1c>30%</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Bộ Chuyển Tiếp Di Động",
                "level": 20,
                "effect": "Sau khi dùng KN chủ động Khuếch Đại Cơ Bắp, Harpsy nhận <color=#f26c1c>6 ô</color> Di Chuyển Thêm.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Đại Tu Triệt Để",
                "level": 20,
                "effect": "Khi áp dụng <color=#3487e0>Tiến Trình Tiêu Diệt</color>, bồi thêm <color=#3487e0>Thoái Lui</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Chiến Lược Dự Phòng",
                "level": 30,
                "effect": "Sau khi kết thúc hành động của mình, đồng minh sở hữu <color=#3487e0>Tiến Trình Alpha</color> nhận <color=#3487e0>Di Chuyển Tăng II</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Sức Mạnh Đồng Minh",
                "level": 30,
                "effect": "Cứ mỗi đồng minh mang <color=#3487e0>Tiến Trình Alpha</color> trên sân, hệ số sát thương mỗi lớp của <color=#3487e0>Tiến Trình Tiêu Diệt</color> khi kích hoạt tăng <color=#f26c1c>2%</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Dũng Khí Bộc Phát",
                "level": 40,
                "effect": "Sau khi dùng KN chủ động Khuếch Đại Cơ Bắp lên đồng minh có <color=#3487e0>Tiến Trình Alpha</color>, Tỷ Lệ Bạo Kích của Harpsy tăng <color=#f26c1c>20%</color> trong 1 hiệp.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Thu Âm Từ Xa",
                "level": 40,
                "effect": "Tầm bắn của đòn đánh thường và các kỹ năng chủ động tăng thêm <color=#f26c1c>2 ô</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Nỗi Khổ Kẻ Nhút Nhát",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Mẹo Công Nghệ Đáng Tin",
                "level": 40,
                "effect": "TL Bạo Kích +5.0% / Sau khi áp dụng Debuff, sát thương gây ra tăng <color=#f26c1c>10%</color> trong 1 hiệp lớn.",
                "materials": "None"
            },
            {
                "name": "Khóa Mở Rộng - Xâm Lược Phân Giải",
                "level": 60,
                "effect": "Sau khi dùng KN Tuyệt Kỹ Cú Đấm Bạch Kim, áp dụng <color=#3487e0>Thoái Lui</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color>. Sau đòn tấn công bằng kỹ năng chủ động, nếu mục tiêu có <color=#3487e0>Thoái Lui</color>, áp dụng <color=#3487e0>Di Chuyển Giảm III</color> trong <color=#f26c1c>1 hiệp</color>.\nSau khi tấn công chủ động, áp dụng 3 lớp Chương Trình Diệt Virus.\nKhi bản thân gây sát thương, cứ mỗi đơn vị đồng minh có Tiến Trình Ưu Tiên, ST Ăn Mòn bản thân gây ra tăng <color=#f26c1c>5%</color>.",
                "materials": "3\n\n\n15000"
            }
        ]
    },
    "koleda": {
        "name": "Koleda",
        "en_name": "Koleda",
        "class": "Tiên Phong",
        "phase": "Hóa Lỏng",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Trường",
        "ammo_type": "Đạn Vừa",
        "signature_weapon": "Chernobog",
        "weakness": "Dẫn Điện",
        "server": "global",
        "skills": [
            {
                "name": "Đòn Đánh Mắt Lạnh",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Sách Chiến Thuật",
                "tags": ["Chủ Động", "AoE", "Dịch Chuyển"],
                "description": "Chọn 1 ô <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, di chuyển đến ô đó và gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công lên toàn bộ kẻ địch <color=#f26c1c>trong phạm vi 2 ô xung quanh</color> ô chỉ định. Nếu Xe Đua Sinner có mặt trên sân, Xe Đua Sinner sẽ được dịch chuyển đến 1 ô gần Koleda và tung đòn tấn công tương tự lên kẻ địch xung quanh ô đó. Kỹ năng này cho phép Koleda nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "name": "Mắt Sói Tuyết",
                "tags": ["Tuyệt Kỹ", "AoE", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#2caadb>ST Hóa Lỏng</color> AoE bằng <color=#f26c1c>150%</color> Tấn Công lên mục tiêu và kẻ địch trong phạm vi 2 ô. Sau đòn đánh, Koleda và Xe Đua Sinner nhận <color=#3487e0>Tăng Áp Turbo</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Ảo Cảnh Xe Đua",
                "tags": ["Chủ Động", "Triệu Hồi"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> bản thân và triệu hồi <color=#3487e0>Kẻ Tội Lỗi</color>. Koleda nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>, và kỹ năng này được thay thế bằng kỹ năng chủ động Người Chiến Thắng!."
            },
            {
                "name": "Kẻ Tội Lỗi",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Khi bắt đầu hiệp, Koleda nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. <color=#f26c1c>50%</color> sát thương ban đầu Koleda phải chịu sẽ do Xe Đua Sinner gánh chịu thay. Koleda không bị ảnh hưởng bởi các hiệu ứng chia sẻ sát thương khác.\n\nKhi kết thúc hành động của Xe Đua Sinner, Koleda nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Nâng cấp</color> trong <color=#f26c1c>3 hiệp</color>. Nếu Xe Đua Sinner đang ở <color=#3487e0>S+Mốc</color>, Koleda nhận thêm 1 lớp <color=#3487e0>Nâng cấp</color>. Khi cả Koleda và Xe Đua Sinner đều có mặt trên sân, cả hai nhận <color=#3487e0>Chi Viện Cơ Động</color>.\n\nSau khi Koleda dùng KN chủ động Sách Chiến Thuật và khi kết thúc hành động của cô, kích hoạt <color=#3487e0>Kích Hoạt Động Năng</color> 1 lần."
            },
            {
                "name": "Người Chiến Thắng!",
                "tags": ["Chủ Động", "Trị Liệu"],
                "description": "Hồi phục <color=#f26c1c>50%</color> HP tối đa và <color=#f26c1c>5 điểm</color> Chỉ Số Ổn Định cho Xe Đua Sinner."
            }
        ],
        "summons": [
            {
                "name": "The Sinner",
                "type": "Vật Triệu Hồi Hóa Lỏng",
                "description": "Cỗ xe đua tốc độ cao hỗ trợ chiến thuật của Koleda. Có khả năng di chuyển linh hoạt, thu hút hỏa lực và càn quét kẻ địch trên đường chạy.",
                "stats": {
                    "hp": "150% HP ban đầu của Koleda",
                    "atk": "80% Tấn Công ban đầu của Koleda",
                    "def": "120% Phòng Thủ ban đầu của Koleda"
                },
                "skills": [
                    {
                        "name": "Đi Hóng Gió Nào!",
                        "tags": ["Chủ Động", "Hỗ Trợ"],
                        "description": "Chọn 1 Doll đồng minh (không bao gồm Koleda) và áp dụng Đi Hóng Gió Nào!. Sau kỹ năng, Xe Đua Sinner nhận 9 ô Di Chuyển Thêm và có thể thực hiện thêm 1 mệnh lệnh."
                    },
                    {
                        "name": "Cú Trôi Quán Tính?!",
                        "tags": ["Chủ Động", "AoE"],
                        "description": "Gây ST Hóa Lỏng AoE bằng 90% Tấn Công lên toàn bộ kẻ địch trong phạm vi 5 ô xung quanh và kéo chúng 5 ô về phía tâm vị trí của Xe Đua Sinner. Sau kỹ năng, nhận 9 ô Di Chuyển Thêm và có thể dùng KN chủ động Doll Siêu Tốc!."
                    },
                    {
                        "name": "Doll Siêu Tốc!",
                        "tags": ["Chủ Động", "AoE"],
                        "description": "Chọn 1 ô trong phạm vi chữ thập từ 4 đến 8 ô, lao tới ô đó và gây ST Hóa Lỏng AoE bằng 90% Tấn Công lên toàn bộ kẻ địch trong phạm vi rộng 3 ô dọc theo đường đi. Nếu ở Mốc S hoặc S+Mốc, gây thêm ST Hóa Lỏng AoE bằng 60% và 90% Tấn Công."
                    },
                    {
                        "name": "Chuyển Số",
                        "tags": ["Bị Động"],
                        "description": "Khi bắt đầu hiệp, Xe Đua Sinner chuyển sang Mốc D. Khi kết thúc hành động cuối cùng, loại bỏ toàn bộ Mốc ngoại trừ Mốc N và chuyển sang Mốc P. Xe Đua Sinner không thể bị chặn đường, miễn nhiễm với Choáng, Khiêu Khích, Mất Khả Năng Hành Động, dịch chuyển và debuff di chuyển. Sát thương phải chịu giảm 35% và hồi 15% HP tối đa khi chịu đòn."
                    }
                ]
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Mắt Sói Tuyết",
                "effect": "Hệ số sát thương tăng lên <color=#f26c1c>180%</color>, và cứ mỗi cấp độ <color=#3487e0>Nâng cấp</color>, hệ số sát thương tăng thêm <color=#f26c1c>15%</color>. Cường hóa hiệu ứng <color=#3487e0>Nâng cấp</color>: Sát thương Hóa Lỏng tăng lên <color=#f26c1c>15%</color>. Khi có đủ 5 lớp <color=#3487e0>Nâng cấp</color>, ST Bạo Kích tăng <color=#f26c1c>30%</color> và sát thương phải chịu giảm <color=#f26c1c>30%</color>. Trước khi thi triển, Koleda và Xe Đua Sinner nhận <color=#3487e0>Tăng Áp Turbo</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Kẻ Tội Lỗi",
                "effect": "Số điểm Chỉ Số Nhiên Liệu nhận được khi bắt đầu hiệp tăng thêm <color=#f26c1c>1 điểm</color>. Sau khi dùng KN chủ động Sách Chiến Thuật và khi kết thúc hành động, kích hoạt <color=#3487e0>Kích Hoạt Động Năng+</color> thay thế. Hệ số sát thương của <color=#3487e0>Kích Hoạt Động Năng</color> và <color=#3487e0>Kích Hoạt Động Năng+</color> tăng thêm <color=#f26c1c>30%</color>."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Kẻ Tội Lỗi",
                "effect": "Tỷ lệ sát thương Xe Đua Sinner gánh chịu thay cho Koleda tăng lên <color=#f26c1c>80%</color>, và lượng HP hồi phục trước khi nhận sát thương tăng lên <color=#f26c1c>25%</color> HP tối đa. Tăng cường hiệu lực của các Mốc số: Mốc P giảm <color=#f26c1c>30%</color> sát thương đơn thể và AoE; Mốc N tăng giảm thương, Phòng Thủ và trị liệu nhận vào lên <color=#f26c1c>150%</color>; Mốc D, S, S+ tăng ST Hóa Lỏng lên <color=#f26c1c>30%</color>; Mốc S, S+ tăng ST Bạo Kích lên <color=#f26c1c>30%</color>; S+Mốc bỏ qua <color=#f26c1c>30%</color> Phòng Thủ và tăng <color=#f26c1c>30%</color> hệ số sát thương."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Sách Chiến Thuật",
                "effect": "Cường hóa hiệu ứng <color=#3487e0>Thu Hồi Động Năng</color>: Tăng Tấn Công, ST Bạo Kích và lượng trị liệu nhận vào lên <color=#f26c1c>25%</color>. KN chủ động Cú Trôi Quán Tính?! của Xe Đua Sinner tăng hệ số sát thương lên <color=#f26c1c>120%</color>, phạm vi hiệu quả và phạm vi kéo tăng lên <color=#f26c1c>7 ô</color>, đồng thời áp dụng <color=#3487e0>Cấm Túc</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Ảo Cảnh Xe Đua",
                "effect": "Cường hóa Người Chiến Thắng!: Hồi phục <color=#f26c1c>100%</color> HP tối đa và toàn bộ Chỉ Số Ổn Định của Xe Đua Sinner, đồng thời giải trừ toàn bộ Debuff trên Xe Đua Sinner. KN chủ động Doll Siêu Tốc! tăng hệ số sát thương lên <color=#f26c1c>120%</color>, chiều rộng đường đi tăng thêm <color=#f26c1c>2 ô</color>. Hệ số sát thương bổ sung ở Mốc S và S+Mốc tăng lên <color=#f26c1c>90%</color> và <color=#f26c1c>120%</color>."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Mắt Sói Tuyết",
                "effect": "Cường hóa <color=#3487e0>Tăng Áp Turbo</color>: Tấn Công tăng lên <color=#f26c1c>45%</color>. KN chủ động Đi Hóng Gió Nào! tăng thuộc tính bổ sung nhận được lên <color=#f26c1c>70%</color>. Khi Xe Đua Sinner thi triển Doll Siêu Tốc!, tạo ra ô địa hình Dị Vị tương ứng với thuộc tính của Doll được chọn bởi Đi Hóng Gió Nào! trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Tín Điều",
                "level": 20,
                "effect": "Khi bắt đầu trận chiến, Koleda nhận <color=#f26c1c>2 lớp</color> <color=#3487e0>Nâng cấp</color> và <color=#3487e0>Thu Hồi Động Năng</color> trong <color=#f26c1c>3 hiệp</color>. Khi Xe Đua Sinner được triệu hồi lúc mở màn, cả Koleda và Xe Đua Sinner đều nhận <color=#3487e0>Thu Hồi Động Năng</color> trong <color=#f26c1c>3 hiệp</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Chưa Đến Lúc Chết",
                "level": 20,
                "effect": "Khi Xe Đua Sinner chịu sát thương chí mạng, HP của nó sẽ không giảm xuống dưới 1 và hiệu ứng này duy trì cho đến hết hiệp. Thời gian hồi: <color=#f26c1c>2 hiệp</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Giấc Mơ Tàn Phá",
                "level": 30,
                "effect": "Trước khi Xe Đua Sinner sử dụng kỹ năng chủ động, giải trừ <color=#f26c1c>1</color> Buff từ mục tiêu.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Biện Pháp Tuyệt Vọng",
                "level": 30,
                "effect": "Khi bắt đầu hiệp, nếu Koleda có 5 lớp <color=#3487e0>Nâng cấp</color>, giải trừ toàn bộ debuff di chuyển và hiệu ứng cấm chỉ lệnh.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Khắc Ghi Danh Tính",
                "level": 40,
                "effect": "Trước khi Koleda và Xe Đua Sinner dùng đánh thường hoặc kỹ năng chủ động, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên mục tiêu địch trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Kẻ Bám Víu Phải Chết",
                "level": 40,
                "effect": "Khi Xe Đua Sinner ở Mốc S hoặc S+Mốc, cứ mỗi đơn vị địch tử vong, Tấn Công của Xe Đua Sinner tăng <color=#f26c1c>4%</color>, tối đa tăng <color=#f26c1c>20%</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Vũ Điệu Bầy Sói",
                "level": "-",
                "effect": "Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Tầm Nhìn Đoạt Mạng",
                "level": 40,
                "effect": "TL Bạo Kích +5.0% / Nếu bản thân hoặc vật triệu hồi có Tầm Di Chuyển lớn hơn hoặc bằng mục tiêu, sát thương gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "None"
            }
        ]
    },
    "lainie": {
        "name": "Lainie",
        "en_name": "Lainie",
        "class": "Vệ Binh",
        "phase": "Vật Lý",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Trường",
        "ammo_type": "Đạn Vừa",
        "signature_weapon": "Perihelion",
        "weakness": "Hóa Lỏng",
        "server": "global",
        "skills": [
            {
                "name": "Giao Thức Thắng Lợi",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Thuật Toán Chiến Đấu",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>130%</color> Tấn Công. Nếu Phòng Thủ của mục tiêu nhỏ hơn hoặc bằng 0, đòn tấn công này bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu."
            },
            {
                "name": "Nghiền Nát Tính Toán",
                "tags": ["Chủ Động", "AoE"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST Vật Lý AoE bằng <color=#f26c1c>100%</color> Tấn Công lên toàn bộ kẻ địch <color=#f26c1c>trong phạm vi 3 ô xung quanh</color> ô chỉ định. Cứ mỗi kẻ địch trúng đòn vượt quá 1, ST Ổn Định gây ra giảm 1 điểm (tối thiểu giảm còn 1 điểm)."
            },
            {
                "name": "Đồng Hành Ảo",
                "tags": ["Tuyệt Kỹ", "Triệu Hồi"],
                "description": "Chọn 1 ô trống <color=#f26c1c>trong phạm vi 7 ô xung quanh</color> và triệu hồi 1 Thực Thể Ảo. Áp dụng <color=#3487e0>Khả Năng Duyên Phận</color> lên bản thân và Thực Thể Ảo trong <color=#f26c1c>1 hiệp</color>.\n\nKhi kết thúc hiệp, tiêu hao <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu. Nếu không đủ Chỉ Số Nhiên Liệu, Thực Thể Ảo sẽ biến mất. Kỹ năng này không thể sử dụng khi Thực Thể Ảo đang có mặt trên sân."
            },
            {
                "name": "Thăm Dò Tiên Cơ",
                "tags": ["Bị Động", "Suy Yếu"],
                "description": "Cứ mỗi 12 điểm HP tối đa ban đầu, tăng <color=#f26c1c>0.1%</color> TL Bạo Kích, tối đa tăng <color=#f26c1c>30%</color>. Áp dụng Thăm Dò Tiên Cơ lên toàn bộ kẻ địch trong phạm vi 7 ô quanh bản thân.\n\nTrước khi tấn công chủ động, áp dụng <color=#f26c1c>1 lớp</color> <color=#3487e0>Quan Tâm Dưới Ô</color> lên mục tiêu và nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu sau đòn đánh. Nếu Phòng Thủ của mục tiêu nhỏ hơn hoặc bằng 0, tăng hệ số sát thương tương đương <color=#f26c1c>10%</color> HP tối đa ban đầu và nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            }
        ],
        "summons": [
            {
                "name": "Thực Thể Ảo",
                "type": "Vật Triệu Hồi Vật Lý",
                "description": "Bản sao mô phỏng tính toán chiến thuật do Lainie triệu hồi. Phản chiếu hỏa lực và phối hợp tác chiến nhịp nhàng với Lainie trên chiến trường.",
                "stats": {
                    "hp": "100% HP ban đầu của Lainie",
                    "atk": "100% Tấn Công ban đầu của Lainie",
                    "def": "100% Phòng Thủ ban đầu của Lainie"
                },
                "skills": [
                    {
                        "name": "Phản Xạ Bối Rối",
                        "tags": ["Đánh Thường", "Chỉ Định"],
                        "description": "Chọn 1 mục tiêu địch trong phạm vi 7 ô xung quanh và gây ST Vật Lý tương đương 80% Tấn Công lên mục tiêu. Sau khi dùng kỹ năng, Lainie sẽ thi triển Giao Thức Thắng Lợi lên cùng mục tiêu đó."
                    },
                    {
                        "name": "Nhận Thức Điềm Báo",
                        "tags": ["Bị Động", "Suy Yếu"],
                        "description": "Cứ mỗi 12 điểm HP tối đa ban đầu, tăng 0.1% TL Bạo Kích, tối đa tăng 30%. Áp dụng Nhận Thức Điềm Báo lên toàn bộ kẻ địch trong phạm vi 7 ô. Trước khi tấn công chủ động, áp dụng 1 lớp Quan Tâm Dưới Ô lên mục tiêu."
                    }
                ]
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Đồng Hành Ảo",
                "effect": "Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color> và lượng Chỉ Số Nhiên Liệu Thực Thể Ảo tiêu hao giảm <color=#f26c1c>1 điểm</color>.\n\nSố lớp cộng dồn tối đa của <color=#3487e0>Quan Tâm Dưới Ô</color> tăng lên <color=#f26c1c>6 lớp</color>. Áp dụng <color=#f26c1c>2 lớp</color> <color=#3487e0>Quan Tâm Dưới Ô</color> lên toàn bộ mục tiêu trong phạm vi 3 ô quanh ô đã chọn, và nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Thuật Toán Chiến Đấu",
                "effect": "Cường hóa hiệu ứng của Thuật Toán Chiến Đấu và Mô Phỏng Tấn Công: Tăng tỷ lệ Phòng Thủ bỏ qua lên <color=#f26c1c>50%</color>, và tăng <color=#f26c1c>10%</color> ST Bạo Kích gây ra lên kẻ địch có Phòng Thủ nhỏ hơn hoặc bằng 0. Trước khi tấn công, áp dụng <color=#f26c1c>1 lớp</color> <color=#3487e0>Quan Tâm Dưới Ô</color> lên mục tiêu."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Thăm Dò Tiên Cơ",
                "effect": "Cường hóa Thăm Dò Tiên Cơ và Nhận Thức Điềm Báo: Cứ mỗi 6 điểm HP tối đa ban đầu, tăng <color=#f26c1c>0.1%</color> TL Bạo Kích, tối đa tăng <color=#f26c1c>60%</color>. Khi tấn công kẻ địch có Phòng Thủ nhỏ hơn hoặc bằng 0, tăng hệ số sát thương tương đương <color=#f26c1c>20%</color> HP tối đa ban đầu.\n\nThăm Dò Tiên Cơ và Nhận Thức Điềm Báo giảm Phòng Thủ của địch thêm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Đồng Hành Ảo",
                "effect": "Khi Lainie hoặc Thực Thể Ảo gây sát thương lên kẻ địch có Phòng Thủ nhỏ hơn hoặc bằng 0, nửa còn lại nhận <color=#3487e0>Sức Mạnh Duyên Phận</color>.\n\nCường hóa hiệu ứng của <color=#3487e0>Khả Năng Duyên Phận</color>: Tăng thêm <color=#f26c1c>6 điểm</color> ST Ổn Định gây ra."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Thăm Dò Tiên Cơ",
                "effect": "Cường hóa Thăm Dò Tiên Cơ và Nhận Thức Điềm Báo: Khi tấn công kẻ địch có Phòng Thủ nhỏ hơn hoặc bằng 0, tăng hệ số sát thương tương đương <color=#f26c1c>30%</color> HP tối đa ban đầu.\n\nKhi Thực Thể Ảo có mặt trên sân, nếu Lainie phải chịu sát thương chí mạng, hồi phục HP tương đương <color=#f26c1c>100%</color> HP tối đa. Hiệu ứng này kích hoạt 1 lần mỗi trận chiến. Thực Thể Ảo sẽ biến mất sau khi hiệu ứng kích hoạt."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Thuật Toán Chiến Đấu",
                "effect": "Cường hóa Thuật Toán Chiến Đấu và Mô Phỏng Tấn Công: Tăng hệ số sát thương lên <color=#f26c1c>160%</color> Tấn Công, tăng hệ số sát thương tối thiểu của Mô Phỏng Tấn Công lên <color=#f26c1c>100%</color>, và xóa bỏ hạn chế không thể sử dụng kỹ năng sau khi thi triển."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Liên Kết Thần Kinh",
                "level": 20,
                "effect": "Khi Lainie hoặc Thực Thể Ảo nhận trị liệu, hồi phục lượng HP bằng <color=#f26c1c>20%</color> HP tối đa cho nửa còn lại. Hiệu ứng này không thể kích hoạt lặp lại liên tục.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Đi Xa Ra Nào!",
                "level": 20,
                "effect": "Sau khi Lainie dùng Nghiền Nát Tính Toán hoặc Thực Thể Ảo dùng Ép Xung Tính Toán, hành động của nửa còn lại sẽ đẩy lùi mục tiêu <color=#f26c1c>2 ô</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Sự Che Chở Của Ô",
                "level": 30,
                "effect": "Khi kết thúc hành động, nếu khoảng cách giữa Lainie và Thực Thể Ảo từ <color=#f26c1c>3 ô trở lên</color>, cả hai nhận <color=#3487e0>Phòng Thủ Phạm Vi II</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Người Bạn Trở Lại",
                "level": 30,
                "effect": "Đồng Hành Ảo: Khi Thực Thể Ảo biến mất, làm mới thời gian hồi chiêu của kỹ năng này. Có thể kích hoạt 1 lần mỗi trận chiến.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Ánh Nắng Ấm Áp",
                "level": 40,
                "effect": "Khi Lainie dùng Thuật Toán Chiến Đấu hoặc Thực Thể Ảo dùng Mô Phỏng Tấn Công, nếu Phòng Thủ của mục tiêu nhỏ hơn hoặc bằng 0, giải trừ <color=#f26c1c>1</color> Buff ngẫu nhiên.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Uy Lực Của OGAS",
                "level": 40,
                "effect": "Tăng <color=#f26c1c>5%</color> ST Bạo Kích gây ra lên kẻ địch có Phòng Thủ nhỏ hơn hoặc bằng 0.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Hồi Ức Trong Ô",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Giải Phóng Hoàn Toàn",
                "level": 40,
                "effect": "Tấn Công +5% / Tăng <color=#f26c1c>10%</color> ST gây ra lên kẻ địch có Phòng Thủ nhỏ hơn hoặc bằng 0.",
                "materials": "None"
            },
            {
                "name": "Khóa Mở Rộng - Xếp Chồng Thuật Toán",
                "level": 60,
                "effect": "Hiệu ứng của <color=#3487e0>Quan Tâm Dưới Ô</color> được cải thiện: Giảm thêm <color=#f26c1c>6%</color> Phòng Thủ mỗi lớp.\nKhi Lainie dùng các kỹ năng Thuật Toán Chiến Đấu, Nghiền Nát Tính Toán hoặc Đồng Hành Ảo, hoặc khi Thực Thể Ảo dùng Mô Phỏng Tấn Công, Ép Xung Tính Toán hoặc Nhập Thành Cánh Hậu, cứ mỗi điểm Chỉ Số Nhiên Liệu Lainie sở hữu, ST Bạo Kích của Lainie và Thực Thể Ảo tăng <color=#f26c1c>15%</color>.\nKhi Thực Thể Ảo còn sống trên sân, Tầm Di Chuyển của Lainie và Thực Thể Ảo tăng thêm <color=#f26c1c>2 ô</color>.",
                "materials": "3\n\n\n15000"
            },
            {
                "name": "Khóa Mở Rộng Cấp 2 - Vòng Lặp Phản Chiếu",
                "level": 60,
                "effect": "Khi kết thúc lượt của Thực Thể Ảo, kéo toàn bộ kẻ địch trên sân về phía bản thân nó <color=#f26c1c>1 ô</color> và gây <color=#f26c1c>2 điểm</color> ST Ổn Định.\nSau khi Lainie hoặc Thực Thể Ảo tấn công chủ động, nếu mục tiêu có 3 lớp <color=#3487e0>Quan Tâm Dưới Ô</color>, áp dụng <color=#3487e0>Bộ Nhớ Đệm Gương</color> lên mục tiêu. Nếu mục tiêu có 6 lớp <color=#3487e0>Quan Tâm Dưới Ô</color>, sát thương cuối cùng tích lũy bởi <color=#3487e0>Bộ Nhớ Đệm Gương</color> tăng lên <color=#f26c1c>25%</color>, đồng thời sát thương gây ra bởi đòn tấn công chủ động tiếp theo của Lainie hoặc Thực Thể Ảo trong hiệp này tăng <color=#f26c1c>30%</color> và ST Bạo Kích tăng <color=#f26c1c>30%</color>.\nTrước khi Lainie hoặc Thực Thể Ảo tấn công chủ động, nếu mục tiêu có <color=#3487e0>Bộ Nhớ Đệm Gương</color>, kích hoạt hiệu ứng đó và hệ số sát thương của đòn tấn công chủ động tăng vĩnh viễn <color=#f26c1c>15%</color>, tối đa tăng <color=#f26c1c>90%</color>.",
                "materials": "3\n\n\n15000"
            }
        ]
    }
}
