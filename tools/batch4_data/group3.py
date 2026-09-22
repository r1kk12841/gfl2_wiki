"""
tools/batch4_data/group3.py
Batch 4 - Group 3: Papasha, Peri, Ullrid, Yoohee.
"""

GROUP_3_DATA = {
    "papasha": {
        "name": "Papasha",
        "en_name": "Papasha",
        "class": "Vệ Binh",
        "phase": "Vật Lý",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Svarog",
        "weakness": "Ăn Mòn",
        "server": "global",
        "skills": [
            {
                "name": "Phát Súng Cảnh Cáo",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>60%</color> Tấn Công."
            },
            {
                "name": "Bảo Vệ Vinh Dự",
                "tags": ["Chủ Động", "AoE", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý AoE bằng <color=#f26c1c>80%</color> Tấn Công lên mục tiêu và tất cả mục tiêu địch <color=#f26c1c>trong phạm vi 1 ô xung quanh</color>. Nếu sau đòn tấn công Chỉ Số Ổn Định của mục tiêu được chọn vẫn lớn hơn 0, Vệ Sĩ Hộ Thành nhận <color=#3487e0>Dũng Khí Kháng Cự</color> trong <color=#f26c1c>3 hiệp</color>."
            },
            {
                "name": "Đột Phá Hiệp Lực",
                "tags": ["Chủ Động", "Chỉ Định", "Giải Trừ"],
                "description": "Chọn 1 ô <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, giải trừ <color=#f26c1c>2</color> Debuff cho bản thân, đồng thời giải trừ toàn bộ hiệu ứng khống chế, Cấm Chỉ Lệnh và hiệu ứng <color=#3487e0>Cứng Đờ</color> khỏi Vệ Sĩ Hộ Thành. Vệ Sĩ Hộ Thành di chuyển đến ô đã chọn và tấn công kẻ địch gần Papasha nhất, gây ST Vật Lý bằng <color=#f26c1c>150%</color> Tấn Công. Đòn tấn công này tăng thêm <color=#f26c1c>50%</color> ST lên Mục Tiêu Cỡ Lớn.\n\nSau khi dùng kỹ năng này, Vệ Sĩ Hộ Thành sẽ không di chuyển độc lập trong phần còn lại của hiệp. Kỹ năng này không thể sử dụng nếu Vệ Sĩ Hộ Thành đang tiến hành <color=#3487e0>Tự Sửa Chữa</color>."
            },
            {
                "name": "Trái Tim Bảo Vệ",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Cường Hóa"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>150%</color> Tấn Công. Vệ Sĩ Hộ Thành nhận <color=#3487e0>Nghị Lực Kiên Trì</color> trong <color=#f26c1c>2 hiệp</color>.\n\nTrước khi tấn công, cứ mỗi Buff bản thân sở hữu, Vệ Sĩ Hộ Thành nhận <color=#f26c1c>1</color> Buff tấn công ngẫu nhiên, tối đa nhận <color=#f26c1c>2</color> Buff, duy trì <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Vệ Binh Đoàn Kết",
                "tags": ["Bị Động", "Triệu Hồi"],
                "description": "Khi bắt đầu chiến đấu, triệu hồi 1 Vệ Sĩ Hộ Thành ở gần bản thân.\n\nSau khi bản thân hoặc Vệ Sĩ Hộ Thành tấn công, bản thân nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\n\nKhi bản thân đánh trúng đòn chí mạng, lần tấn công tiếp theo của Vệ Sĩ Hộ Thành tăng <color=#f26c1c>20%</color> Tỷ Lệ Bạo Kích. Tương tự, khi Vệ Sĩ Hộ Thành đánh trúng đòn chí mạng, lần tấn công tiếp theo của bản thân tăng <color=#f26c1c>20%</color> Tỷ Lệ Bạo Kích."

            }
        ],
        "summons": [
            {
                "name": "Vệ Sĩ Hộ Thành",
                "type": "Vật Triệu Hồi Vật Lý",
                "description": "Vật triệu hồi phòng ngự kiên cố do Papasha chế tạo. Cung cấp hỏa lực yểm trợ và khả năng chống chịu bền bỉ trên chiến trường.",
                "stats": {
                    "hp": "120% HP ban đầu của Papasha",
                    "atk": "60% Tấn Công ban đầu của Papasha",
                    "def": "120% Phòng Thủ ban đầu của Papasha"
                },
                "skills": [
                    {
                        "name": "Chi Viện Chống Khủng Bố",
                        "tags": ["Bị Động", "Hỗ Trợ"],
                        "description": "Sau khi Papasha tấn công mục tiêu địch, Vệ Sĩ Hộ Thành sẽ bồi thêm 1 lần Tấn Công Chi Viện lên cùng mục tiêu đó, gây ST Vật Lý bằng 80% Tấn Công."
                    },
                    {
                        "name": "Biện Pháp Phòng Chống Cháy Nổ",
                        "tags": ["Bị Động", "Trị Liệu"],
                        "description": "Khi kết thúc hiệp, Vệ Sĩ Hộ Thành tự động di chuyển độc lập để tìm Nơi Ẩn Nấp.\n\nLượng trị liệu Vệ Sĩ Hộ Thành nhận vào giảm 100% và không thể nhận lá chắn. Khi Papasha nhận trị liệu, Vệ Sĩ Hộ Thành hồi phục 10% HP tối đa của bản thân.\n\nKhi Vệ Sĩ Hộ Thành chịu sát thương chí mạng, nó tiến vào trạng thái Tự Sửa Chữa trong 1 hiệp."
                    },
                    {
                        "name": "Giám Sát An Ninh",
                        "tags": ["Bị Động"],
                        "description": "Khi kết thúc hành động của đơn vị này, tiến hành Cảnh Giới toàn bản đồ. Khi một đơn vị địch dùng đánh thường hoặc kỹ năng chủ động, gây sát thương bằng 40% Tấn Công của bản thân lên kẻ đó. Hiệu ứng này có thể kích hoạt 1 lần mỗi hiệp.\n\nKỹ năng bị động này chỉ mở khóa sau khi mở Đốt Sống 5."
                    }
                ]
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Bảo Vệ Vinh Dự",
                "effect": "Thời gian duy trì <color=#3487e0>Tự Sửa Chữa</color> của Vệ Sĩ Hộ Thành giảm <color=#f26c1c>1 hiệp</color>. Sau khi bản thân được trị liệu, Vệ Sĩ Hộ Thành hồi phục HP bằng <color=#f26c1c>20%</color> HP tối đa của nó.\n\nHủy bỏ yêu cầu Chỉ Số Ổn Định của mục tiêu. Hiệu ứng của <color=#3487e0>Dũng Khí Kháng Cự</color> được cường hóa: Bỏ qua <color=#f26c1c>30%</color> Phòng Thủ khi tấn công Mục Tiêu Cỡ Lớn."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Đột Phá Trong Im Lặng",
                "effect": "Phạm vi chọn ô được mở rộng ra toàn bộ chiến trường, và đòn tấn công này chắc chắn gây bạo kích. Khi kết thúc hiệp, Vệ Sĩ Hộ Thành tung thêm <color=#f26c1c>1 lần</color> Chi Viện Chống Khủng Bố lên mục tiêu địch gần nhất."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Vệ Binh Đoàn Kết",
                "effect": "Khi Vệ Sĩ Hộ Thành được triệu hồi, Tỷ Lệ Bạo Kích của nó tăng <color=#f26c1c>30%</color> và ST Bạo Kích tăng <color=#f26c1c>20%</color>. Khi bắt đầu chiến đấu, bản thân nhận <color=#f26c1c>3 lớp</color> <color=#3487e0>Sức Mạnh Đoàn Kết</color>. Khi kết thúc hành động, bản thân nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Sức Mạnh Đoàn Kết</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Trái Tim Bảo Vệ",
                "effect": "Hiệu ứng của <color=#3487e0>Nghị Lực Kiên Trì</color> được cường hóa: Khiến sát thương mục tiêu phải chịu tăng lên đến <color=#f26c1c>80%</color>. Hiệu lực của các Buff tấn công ngẫu nhiên được khuếch đại, và số lượng Buff tấn công tối đa nhận được tăng lên <color=#f26c1c>3</color> Buff. Cứ mỗi lớp <color=#3487e0>Sức Mạnh Đoàn Kết</color> vượt quá 1 sẽ được tính là 1 Buff độc lập."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Vệ Binh Đoàn Kết",
                "effect": "Vệ Sĩ Hộ Thành nhận kỹ năng Giám Sát An Ninh."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Trái Tim Bảo Vệ",
                "effect": "Khi bắt đầu chiến đấu, Vệ Sĩ Hộ Thành nhận <color=#3487e0>Nghị Lực Kiên Trì</color> vĩnh viễn. Trái Tim Bảo Vệ đổi thành áp dụng <color=#3487e0>Quyết Tâm Bảo Vệ</color> trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Vinh Quang Cùng Ta",
                "level": 20,
                "effect": "Khi dùng KN chủ động Bảo Vệ Vinh Dự tấn công Mục Tiêu Cỡ Lớn, ST gây ra tăng <color=#f26c1c>20%</color>. ST Ổn Định của KN chủ động Chi Viện Chống Khủng Bố của Vệ Sĩ Hộ Thành tăng <color=#f26c1c>2 điểm</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Lời Thề Phòng Thủ",
                "level": 20,
                "effect": "Khi Vệ Sĩ Hộ Thành đang trong trạng thái <color=#3487e0>Tự Sửa Chữa</color>, ST gây ra của Papasha tăng <color=#f26c1c>20%</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Niềm Tin Kiên Định",
                "level": 30,
                "effect": "Vệ Sĩ Hộ Thành không thể di chuyển độc lập, nhưng Tấn Công của nó tăng <color=#f26c1c>10%</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Đòn Tấn Công Cuối Cùng",
                "level": 30,
                "effect": "Khi KN chủ động Đột Phá Hiệp Lực gây sát thương, nếu không có kẻ địch nào trong phạm vi 3 ô quanh Vệ Sĩ Hộ Thành, ST gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Tôi Sẽ Học Được",
                "level": 40,
                "effect": "Khi bắt đầu hiệp, nếu Papasha có tối đa 1 Buff có thể giải trừ, bản thân nhận 1 Buff ngẫu nhiên có thể giải trừ trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Sức Mạnh Đoàn Kết",
                "level": 40,
                "effect": "Khi bắt đầu hiệp, đơn vị có Tấn Công thấp hơn giữa bản thân và Vệ Sĩ Hộ Thành sẽ nhận <color=#3487e0>Hào Quang Huân Chương</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Niềm Tin Bất Diệt",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Huân Chương Rực Rỡ",
                "level": 40,
                "effect": "Tấn Công +5.0% / Tăng <color=#f26c1c>10%</color> ST gây ra bởi kỹ năng chi viện của đơn vị đồng minh (không bao gồm bản thân). Mỗi hiệp kích hoạt tối đa 1 lần.",
                "materials": "None"
            },
            {
                "name": "Khóa Mở Rộng - Thành Trì Bất Bại",
                "level": 60,
                "effect": "ST gây ra của Vệ Sĩ Hộ Thành tăng <color=#f26c1c>50%</color>. Khi Vệ Sĩ Hộ Thành có mặt trên sân, toàn bộ vật triệu hồi phe ta tăng <color=#f26c1c>30%</color> ST gây ra, và khi kết thúc hiệp sẽ nhận <color=#3487e0>Giảm ST III</color> trong <color=#f26c1c>1 hiệp</color>. Tiêu hao Chỉ Số Nhiên Liệu của KN chủ động Đột Phá Trong Im Lặng giảm <color=#f26c1c>3 điểm</color>. Khi kích hoạt, Vệ Sĩ Hộ Thành nhận <color=#f26c1c>2 lớp</color> <color=#3487e0>Rèn Thép</color>.",
                "materials": "3\n\n\n15000"
            }
        ]
    },
    "peri": {
        "name": "Peri",
        "en_name": "Peri",
        "class": "Hộ Vệ",
        "phase": "Thiêu Đốt",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Tiểu Liên",
        "ammo_type": "Đạn Nhẹ",
        "signature_weapon": "Amanita",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Món Quà Nhiệt Tình",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Đầu Tư Mạo Hiểm",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Tiêu hao HP bằng <color=#f26c1c>30%</color> HP tối đa, và nhận <color=#f26c1c>2 lớp</color> <color=#3487e0>Đầu Tư Khuyến Mãi</color> (hiệu ứng này không làm HP giảm xuống dưới 10%). Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>120%</color> Tấn Công."
            },
            {
                "name": "Đơn Đặt Hàng Vượt Mức",
                "tags": ["Chủ Động", "AoE", "Suy Yếu"],
                "description": "Tiêu hao HP bằng <color=#f26c1c>40%</color> HP tối đa, và nhận <color=#f26c1c>3 lớp</color> <color=#3487e0>Đầu Tư Khuyến Mãi</color> (hiệu ứng này không làm HP giảm xuống dưới 10%). Chọn 1 ô <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây <color=#e67129>ST Thiêu Đốt</color> AoE bằng <color=#f26c1c>100%</color> Tấn Công lên tất cả kẻ địch <color=#f26c1c>trong phạm vi 2 ô xung quanh</color> ô chỉ định, và áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Giá Đấu Cuối Cùng",
                "tags": ["Tuyệt Kỹ", "Cường Hóa"],
                "description": "Nhận <color=#f26c1c>6 lớp</color> <color=#3487e0>Đầu Tư Khuyến Mãi</color>, đồng thời nhận <color=#3487e0>Mặc Cả</color> và <color=#3487e0>Phòng Hộ Bản Kim</color> trong <color=#f26c1c>3 hiệp</color> (Thời gian duy trì giảm khi kết thúc hiệp hiện tại). <color=#3487e0>Phòng Hộ Bản Kim</color> có thể hấp thụ lượng sát thương tương đương <color=#f26c1c>50%</color> HP tối đa của Peri."
            },
            {
                "name": "Tối Đa Hóa Lợi Nhuận",
                "tags": ["Bị Động"],
                "description": "Khi kết thúc hành động, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Khi đồng minh (không bao gồm bản thân) kích hoạt Đòn Tấn Công Chi Viện gây <color=#e67129>ST Thiêu Đốt</color>, nếu Chỉ Số Nhiên Liệu của Peri dưới 6 điểm, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Hiệu ứng này có thể kích hoạt 1 lần mỗi hiệp.\n\nSau khi dùng kỹ năng chủ động, cứ có <color=#f26c1c>3 lớp</color> <color=#3487e0>Đầu Tư Khuyến Mãi</color>, Peri có thể tung <color=#f26c1c>1 lần</color> đánh thường. Hiệu ứng của đòn đánh thường này đổi thành: Cứ mỗi lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color> sở hữu, gây <color=#e67129>ST Thiêu Đốt</color> bằng <color=#f26c1c>12%</color> HP tối đa ban đầu của Peri."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Tối Đa Hóa Lợi Nhuận",
                "effect": "Số lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color> cần thiết để tung 1 đòn đánh thường giảm <color=#f26c1c>1 lớp</color>."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Giá Đấu Cuối Cùng",
                "effect": "Cường hóa hiệu ứng của <color=#3487e0>Mặc Cả</color>: Tăng ST gây ra thêm <color=#f26c1c>30%</color> (Từ 30% → <color=#f26c1c>60%</color>). Khi <color=#3487e0>Mặc Cả</color> kết thúc, hồi phục Chỉ Số Ổn Định về mức tối đa."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Tối Đa Hóa Lợi Nhuận",
                "effect": "Khi bắt đầu chiến đấu, Chỉ Số Ổn Định tăng <color=#f26c1c>6 điểm</color>. Cứ mỗi lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color> sở hữu, <color=#e67129>ST Thiêu Đốt</color> bản thân gây ra tăng <color=#f26c1c>8%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Đơn Đặt Hàng Vượt Mức",
                "effect": "Lượng HP tiêu hao giảm <color=#f26c1c>10%</color>. Phạm vi hiệu ứng AoE tăng <color=#f26c1c>1 ô</color>. Cứ mỗi lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color> sở hữu, hệ số sát thương tăng <color=#f26c1c>5%</color>."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Đầu Tư Mạo Hiểm",
                "effect": "Lượng HP tiêu hao giảm <color=#f26c1c>10%</color>. Cứ mỗi lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color> sở hữu, hệ số sát thương tăng <color=#f26c1c>10%</color>. Trước khi tấn công, giải trừ <color=#f26c1c>1</color> Buff của mục tiêu."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Giá Đấu Cuối Cùng",
                "effect": "Thêm hiệu ứng mới cho <color=#3487e0>Mặc Cả</color>: Tăng <color=#f26c1c>50%</color> ST Bạo Kích do đòn đánh thường gây ra.\n\nThêm hiệu ứng mới cho <color=#3487e0>Phòng Hộ Bản Kim</color>: Trước khi bị tấn công, giảm <color=#f26c1c>30%</color> Tấn Công của kẻ tấn công."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Nền Tảng Giao Dịch",
                "level": 20,
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Điềm Tĩnh Đáng Tin",
                "level": 20,
                "effect": "Cứ mỗi lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color> sở hữu, Phòng Thủ tăng <color=#f26c1c>5%</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Tin Tức Nội Bộ",
                "level": 30,
                "effect": "Khi bắt đầu hiệp, nếu số lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color> sở hữu từ 2 lớp trở lên, nhận <color=#f26c1c>2 lớp</color> <color=#3487e0>Yểm Hộ</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Người Phụ Nữ Tự Lập",
                "level": 30,
                "effect": "Giá Đấu Cuối Cùng: Sau khi sử dụng, giải trừ toàn bộ Debuff trên người bản thân.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Người Lớn Trưởng Thành",
                "level": 40,
                "effect": "Khi Peri bị áp dụng Choáng, Khiêu Khích hoặc Tê Liệt, lập tức giải trừ hiệu ứng đó, đồng thời miễn nhiễm với Choáng, Khiêu Khích và Tê Liệt trong <color=#f26c1c>1 hiệp</color> và hồi phục HP bằng <color=#f26c1c>20%</color> HP tối đa của bản thân. Hiệu ứng này có thời gian hồi <color=#f26c1c>3 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Thao Túng Tâm Lý",
                "level": 40,
                "effect": "Tăng <color=#f26c1c>10%</color> ST gây ra lên các mục tiêu có Debuff loại Thiêu Đốt.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Trưởng Thành Vững Vàng",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Vẫn Đang Lớn Lên",
                "level": 40,
                "effect": "HP +5.0% / Khi tấn công cùng một mục tiêu nhiều lần, tăng <color=#f26c1c>10%</color> ST nguyên tố gây ra lên mục tiêu đó.",
                "materials": "None"
            },
            {
                "name": "Khóa Mở Rộng - Kế Hoạch Của Nhà Môi Giới",
                "level": 60,
                "effect": "Đòn đánh thường giờ tấn công 2 lần.\n<color=#3487e0>Đầu Tư Khuyến Mãi</color> giờ không còn làm giảm hiệu quả trị liệu nhận vào.\nCứ mỗi lớp <color=#3487e0>Đầu Tư Khuyến Mãi</color>, giảm <color=#f26c1c>5%</color> sát thương phải chịu cho tất cả đơn vị đồng minh (không bao gồm Peri).\nHiệu ứng bị động của Tối Đa Hóa Lợi Nhuận được thay đổi: Khi các đơn vị đồng minh (không bao gồm Peri) gây ST Thiêu Đốt, sẽ kích hoạt hiệu ứng nhận Chỉ Số Nhiên Liệu của Peri.",
                "materials": "3\n\n\n15000"
            }
        ]
    },
    "ullrid": {
        "name": "Ullrid",
        "en_name": "Ullrid",
        "class": "Tiên Phong",
        "phase": "Vật Lý",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Lưỡi Đao",
        "ammo_type": "Cận Chiến",
        "signature_weapon": "Rectrix",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Phát Súng Cảnh Cáo",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 5 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Tầm Nhìn Của Thợ Săn",
                "tags": ["Chủ Động", "Chỉ Định", "Cận Chiến", "Suy Yếu"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 1 ô xung quanh</color>, gây ST Vật Lý cận chiến bằng <color=#f26c1c>120%</color> Tấn Công và nhận <color=#f26c1c>6 ô</color> Di Chuyển Thêm. Nếu mục tiêu chưa bị tiêu diệt, áp dụng <color=#3487e0>Đánh Dấu Con Mồi</color> trong <color=#f26c1c>2 hiệp</color>."
            },
            {
                "name": "Lưỡi Đao Xoay",
                "tags": ["Chủ Động", "Chỉ Định", "Cận Chiến"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 1 ô xung quanh</color>, gây ST Vật Lý cận chiến bằng <color=#f26c1c>90%</color> Tấn Công. Nhận <color=#3487e0>Xoay Liên Hoàn</color> sau khi tấn công."
            },
            {
                "name": "Truy Lùng Ẩn Tích",
                "tags": ["Tuyệt Kỹ", "Chỉ Định", "Cận Chiến"],
                "description": "Chọn 1 ô <color=#f26c1c>trong phạm vi chữ thập 5 ô</color>, di chuyển đến ô đó và gây ST Vật Lý cận chiến bằng <color=#f26c1c>180%</color> Tấn Công lên mục tiêu địch có lượng HP cao nhất <color=#f26c1c>trong phạm vi 1 ô xung quanh</color>.\n\nTiêu hao toàn bộ lớp <color=#3487e0>Thiên Phú Thợ Săn</color>, cứ mỗi lớp tiêu hao giúp tăng <color=#f26c1c>10%</color> ST đòn đánh này gây ra, tối đa tăng <color=#f26c1c>30%</color>. Nếu có từ 2 lớp <color=#3487e0>Thiên Phú Thợ Săn</color> trở lên, nhận <color=#f26c1c>2 lớp</color> <color=#3487e0>Ngụy Trang</color> trong <color=#f26c1c>1 hiệp</color>."
            },
            {
                "name": "Ngụy Trang Quang Học",
                "tags": ["Bị Động"],
                "description": "Nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Thiên Phú Thợ Săn</color> và <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu sau khi thực hiện tấn công chủ động.\n\nKhi kết thúc hành động của một đơn vị địch, nếu HP của Ullrid dưới 30%, nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Ngụy Trang</color> trong <color=#f26c1c>1 hiệp</color>. Thời gian hồi: 3 hiệp."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Lưỡi Đao Xoay",
                "effect": "Nếu tấn công cùng một mục tiêu trong một lượt hành động, ST gây ra tăng <color=#f26c1c>30%</color>. Hiệu ứng của <color=#3487e0>Xoay Liên Hoàn</color> được cường hóa: Bỏ qua giảm sát thương từ vật chắn khi tấn công."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Ngụy Trang Quang Học",
                "effect": "Khi bắt đầu chiến đấu, cứ mỗi đơn vị đồng minh trên sân (không bao gồm bản thân), nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Thiên Phú Thợ Săn</color> và <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Tầm Nhìn Của Thợ Săn",
                "effect": "Nếu mục tiêu chưa bị tiêu diệt, áp dụng <color=#3487e0>Di Chuyển Giảm II</color> lên mục tiêu địch trong <color=#f26c1c>2 hiệp</color>. Khi Ullrid bị tấn công bởi mục tiêu có <color=#3487e0>Đánh Dấu Con Mồi</color>, sát thương phải chịu giảm <color=#f26c1c>20%</color>."
            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Truy Lùng Ẩn Tích",
                "effect": "Tầm thi triển tăng <color=#f26c1c>2 ô</color>. Giới hạn tăng sát thương khi tiêu hao <color=#3487e0>Thiên Phú Thợ Săn</color> nâng lên <color=#f26c1c>60%</color>."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Ngụy Trang Quang Học",
                "effect": "Trước khi tấn công, nếu bản thân đã di chuyển từ <color=#f26c1c>2 ô trở lên</color>, Tấn Công tăng <color=#f26c1c>20%</color>. Nếu HP của Ullrid dưới <color=#f26c1c>50%</color>, nhận <color=#3487e0>Ngụy Trang</color> và thời gian hồi chiêu của hiệu ứng này giảm <color=#f26c1c>1 hiệp</color>."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Truy Lùng Ẩn Tích",
                "effect": "Cứ mỗi 2% HP mục tiêu địch bị tổn thất, tăng <color=#f26c1c>1%</color> Tấn Công của bản thân cho kỹ năng này. Nếu tiêu diệt mục tiêu, ST gây ra bởi đòn tấn công chủ động tiếp theo tăng <color=#f26c1c>30%</color>.\n\nNếu có từ 2 lớp <color=#3487e0>Thiên Phú Thợ Săn</color> trở lên, chỉ nhận 1 lớp <color=#3487e0>Ngụy Trang</color>, nhưng <color=#3487e0>Ngụy Trang</color> sẽ không còn bị mất đi sau khi chịu sát thương."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Hành Động Thần Tốc",
                "level": 20,
                "effect": "Khi bản thân sở hữu <color=#3487e0>Xoay Liên Hoàn</color>, có thể sử dụng đòn đánh thường và các kỹ năng chủ động khác, nhưng sẽ tiêu hao thêm <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Săn Mồi",
                "level": 20,
                "effect": "Bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu địch khi không có kẻ địch nào khác trong phạm vi 3 ô quanh mục tiêu.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Cẩn Trọng Thích Đáng",
                "level": 30,
                "effect": "Khi bắt đầu chiến đấu, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Trạng Thái Lý Tưởng",
                "level": 30,
                "effect": "Khi không có đơn vị đồng minh nào trong phạm vi 3 ô quanh bản thân (không bao gồm vật triệu hồi), Tỷ Lệ Bạo Kích của bản thân tăng <color=#f26c1c>20%</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Áp Chế",
                "level": 40,
                "effect": "Khi đầy HP, ST gây ra tăng <color=#f26c1c>15%</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Nhạy Bén Của Thợ Săn",
                "level": 40,
                "effect": "Khi khai thác Điểm Yếu Thuộc Tính, nhận <color=#3487e0>Tấn Công Tăng I</color> trong <color=#f26c1c>2 hiệp</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Kẻ Hủy Diệt Căng Thẳng",
                "level": "-",
                "effect": "Tấn Công +3%, HP +3%, ST Bạo Kích +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Xé Toạc",
                "level": 40,
                "effect": "TL Bạo Kích +5.0% / Trước khi tấn công, nếu mục tiêu địch không đầy HP, tăng <color=#f26c1c>7%</color> ST gây ra lên mục tiêu đó.",
                "materials": "None"
            },
            {
                "name": "Khóa Mở Rộng - Cuồng Phong Trảm",
                "level": 60,
                "effect": "Sau khi dùng Lưỡi Đao Xoay, nếu mục tiêu vẫn còn sống, bồi thêm <color=#f26c1c>1 lần</color> ST Vật Lý bằng <color=#f26c1c>90%</color> Tấn Công và gây <color=#f26c1c>1 điểm</color> ST Ổn Định. Sát thương của đòn tấn công này tăng <color=#f26c1c>30%</color>. Hiệu ứng này có thể kích hoạt tối đa 3 lần mỗi hiệp.",
                "materials": "3\n\n\n15000"
            },
            {
                "name": "Khóa Mở Rộng Cấp 2 - Vết Thương Xé Rách",
                "level": 60,
                "effect": "Áp dụng <color=#3487e0>Đánh Dấu Con Mồi</color> trước mỗi lần dùng KN chủ động Lưỡi Đao Xoay. Sau khi dùng kỹ năng nói trên, thời gian hồi của KN Tuyệt Kỹ Truy Lùng Ẩn Tích giảm <color=#f26c1c>1 hiệp</color>. Nếu Ullrid liên tục đánh trúng cùng một mục tiêu, bản thân nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Hiệu ứng này chỉ có thể kích hoạt 1 lần mỗi hiệp.\n\nTrước khi dùng KN Tuyệt Kỹ Truy Lùng Ẩn Tích, Ullrid nhận tối đa số lớp <color=#3487e0>Thiên Phú Thợ Săn</color>.\n\nHiệu ứng của <color=#3487e0>Thiên Phú Thợ Săn</color> được cường hóa: Nếu Tỷ Lệ Bạo Kích của Ullrid cao hơn 100%, cứ mỗi 1% Tỷ Lệ Bạo Kích vượt mức sẽ tăng <color=#f26c1c>0.3%</color> ST Bạo Kích. Tăng <color=#f26c1c>10%</color> ST gây ra bởi tất cả đơn vị đồng minh gây sát thương cận chiến. Cứ mỗi lớp <color=#3487e0>Thiên Phú Thợ Săn</color> tiêu hao, Ullrid nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\n\n<color=#3487e0>Đánh Dấu Con Mồi</color> nhận hiệu ứng mới: <color=#3487e0>Xé Rách</color> - Khi chịu sát thương, nếu kẻ tấn công sử dụng vũ khí đao kiếm, mỗi lần gây sát thương sẽ gây thêm sát thương bằng 40% sát thương gốc. Debuff, không thể giải trừ.",
                "materials": "3\n\n\n15000"
            }
        ]
    },
    "yoohee": {
        "name": "Yoohee",
        "en_name": "Yoohee",
        "class": "Hỗ Trợ",
        "phase": "Vật Lý",
        "rarity": "Tinh Nhuệ",
        "weapon_type": "Súng Trường",
        "ammo_type": "Đạn Vừa",
        "signature_weapon": "Sparkling Centerstage",
        "weakness": "Băng Kết",
        "server": "global",
        "skills": [
            {
                "name": "Nhịp Điệu Sôi Động",
                "tags": ["Đánh Thường", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công."
            },
            {
                "name": "Bước Nhảy Ngẫu Hứng",
                "tags": ["Chủ Động", "Chỉ Định"],
                "description": "Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>120%</color> Tấn Công. Nếu Yoohee có từ 3 điểm Chỉ Số Nhiên Liệu trở lên, tiêu hao thêm <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu để bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu trong lần tấn công này."
            },
            {
                "name": "Linh Hồn Vũ Đạo",
                "tags": ["Tuyệt Kỹ", "AoE", "Cường Hóa", "Khống Chế"],
                "description": "Chọn 1 đồng minh <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, áp dụng <color=#3487e0>Phòng Thủ Chuẩn Xác I</color> lên đồng minh đó và tất cả đồng minh <color=#f26c1c>trong phạm vi 2 ô xung quanh</color> trong <color=#f26c1c>2 hiệp</color>.\n\nGây ST Vật Lý AoE bằng <color=#f26c1c>80%</color> Tấn Công lên tất cả kẻ địch trong phạm vi và áp dụng <color=#3487e0>Choáng</color> trong <color=#f26c1c>1 hiệp</color>. Sau đòn tấn công, Yoohee nhận 1 lần sử dụng KN chủ động <color=#3487e0>Bước Nhảy Nhẹ Nhàng</color> hoặc <color=#3487e0>Bước Nhảy Nhiệt Tình</color>."
            },
            {
                "name": "Hạ Màn Lộng Lẫy",
                "tags": ["Tuyệt Kỹ", "Cường Hóa"],
                "description": "Yoohee nhận <color=#3487e0>Nòng Cốt Vũ Đoàn</color> trong <color=#f26c1c>3 hiệp</color>. Áp dụng <color=#3487e0>Thế Tấn Công Ổn Định I</color> cho toàn bộ đồng minh trong <color=#f26c1c>2 hiệp</color>. Sau khi dùng kỹ năng, nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>."
            },
            {
                "name": "Khí Chất Vũ Công Chính",
                "tags": ["Bị Động", "Cường Hóa"],
                "description": "Khi đồng minh gây ST Vật Lý, Yoohee nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.\n\nSau khi dùng đánh thường hoặc kỹ năng chủ động, có thể dùng <color=#3487e0>Bước Nhảy Nhẹ Nhàng</color> hoặc <color=#3487e0>Bước Nhảy Nhiệt Tình</color> (hiệu ứng này không thể kích hoạt lặp lại).\n\nKhi áp dụng từ 3 <color=#3487e0>Bước Nhảy</color> trở lên, kích hoạt 1 lần <color=#3487e0>Vũ Công Xuất Sắc</color>, đồng thời nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Quyết Không Nhận Thua</color> và làm mới thời gian duy trì của toàn bộ các lớp <color=#3487e0>Bước Nhảy</color> và <color=#3487e0>Công Kích Nghịch Đảo</color> trên toàn chiến trường."
            },
            {
                "name": "Bước Nhảy Nhẹ Nhàng",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Chọn 1 đồng minh (không bao gồm bản thân) <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, áp dụng <color=#3487e0>Bước Nhảy Nhẹ Nhàng</color> và <color=#3487e0>Công Kích Nghịch Đảo</color> trong <color=#f26c1c>3 hiệp</color>."
            },
            {
                "name": "Bước Nhảy Nhiệt Tình",
                "tags": ["Chủ Động", "Cường Hóa"],
                "description": "Chọn 1 đồng minh (không bao gồm bản thân) <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, áp dụng <color=#3487e0>Bước Nhảy Nhiệt Tình</color> và <color=#3487e0>Công Kích Nghịch Đảo</color> trong <color=#f26c1c>3 hiệp</color>."
            }
        ],
        "fortification": [
            {
                "tier": 1,
                "level": 2,
                "skill": "Hạ Màn Lộng Lẫy",
                "effect": "Áp dụng <color=#3487e0>Thế Tấn Công Ổn Định II</color> thay cho <color=#3487e0>Thế Tấn Công Ổn Định I</color>. Đồng thời áp dụng <color=#3487e0>Tấn Công Tăng II</color> cho toàn bộ đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>.\n\nSau khi dùng kỹ năng, nếu dùng <color=#3487e0>Bước Nhảy Nhẹ Nhàng</color> hoặc <color=#3487e0>Bước Nhảy Nhiệt Tình</color> trong hiệp này, hiệu ứng sẽ được áp dụng lên toàn bộ đồng minh."
            },
            {
                "tier": 2,
                "level": 2,
                "skill": "Khí Chất Vũ Công Chính",
                "effect": "Phạm vi chọn mục tiêu của <color=#3487e0>Bước Nhảy Nhẹ Nhàng</color> và <color=#3487e0>Bước Nhảy Nhiệt Tình</color> được mở rộng ra toàn bộ chiến trường.\n\nThêm hiệu ứng mới cho <color=#3487e0>Bước Nhảy Nhẹ Nhàng</color>: Hồi phục HP tương đương <color=#f26c1c>15%</color> HP tối đa.\n\nThêm hiệu ứng mới cho <color=#3487e0>Bước Nhảy Nhiệt Tình</color>: Giải trừ <color=#f26c1c>1</color> Debuff trên người mục tiêu.\n\nKhi <color=#3487e0>Vũ Công Xuất Sắc</color> kích hoạt, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên kẻ địch có Phòng Thủ ban đầu cao nhất trong <color=#f26c1c>3 hiệp</color>. Nếu Yoohee có <color=#3487e0>Nòng Cốt Vũ Đoàn</color>, <color=#3487e0>Quyết Không Nhận Thua</color> giúp giảm <color=#f26c1c>30%</color> sát thương đồng minh phải chịu."
            },
            {
                "tier": 3,
                "level": 2,
                "skill": "Hạ Màn Lộng Lẫy",
                "effect": "Yoohee nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Quyết Không Nhận Thua</color>.\n\nThêm hiệu ứng mới cho <color=#3487e0>Nòng Cốt Vũ Đoàn</color>: Khi tấn công, bỏ qua <color=#f26c1c>50%</color> Phòng Thủ của kẻ địch. Sau khi kích hoạt hiệu ứng của <color=#3487e0>Vũ Công Xuất Sắc</color>, lập tức kích hoạt Bước Nhảy Ngẫu Hứng lên kẻ địch có HP hiện tại cao nhất trong tầm bắn. Hiệu ứng này chỉ có thể kích hoạt 1 lần mỗi hiệp, và không thể sử dụng <color=#3487e0>Bước Nhảy Nhẹ Nhàng</color> hay <color=#3487e0>Bước Nhảy Nhiệt Tình</color> sau lần thi triển đó.\n\nCứ mỗi 2 lần kích hoạt <color=#3487e0>Vũ Công Xuất Sắc</color>, thời gian hồi chiêu của kỹ năng này giảm <color=#f26c1c>1 hiệp</color>."

            },
            {
                "tier": 4,
                "level": 2,
                "skill": "Bước Nhảy Ngẫu Hứng",
                "effect": "Hệ số sát thương tăng <color=#f26c1c>60%</color>. Cứ mỗi <color=#3487e0>Bước Nhảy</color> được áp dụng, nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Ý Tưởng Kỳ Diệu</color>."
            },
            {
                "tier": 5,
                "level": 3,
                "skill": "Linh Hồn Vũ Đạo",
                "effect": "Hệ số sát thương tăng <color=#f26c1c>50%</color>, và phạm vi hiệu ứng tăng <color=#f26c1c>1 ô</color>.\n\nÁp dụng <color=#3487e0>Phòng Thủ Chuẩn Xác II</color> thay cho <color=#3487e0>Phòng Thủ Chuẩn Xác I</color>. Giải trừ Khiêu Khích, Sợ Hãi, Choáng và Mê Mẩn cho toàn bộ đồng minh."
            },
            {
                "tier": 6,
                "level": 3,
                "skill": "Khí Chất Vũ Công Chính",
                "effect": "Nhân đôi hiệu ứng của <color=#3487e0>Bước Nhảy</color> cho bản thân (Tăng <color=#f26c1c>20%</color> ST Bạo Kích, hồi phục HP tương đương <color=#f26c1c>40%</color> Tấn Công, nhận <color=#f26c1c>3 lớp</color> <color=#3487e0>Yểm Hộ</color>).\n\nCứ mỗi Buff áp dụng lên các đồng minh khác, Tấn Công của bản thân tăng <color=#f26c1c>1.5%</color>, tối đa tăng đến <color=#f26c1c>45%</color>. Khi kích hoạt <color=#3487e0>Vũ Công Xuất Sắc</color>, áp dụng <color=#3487e0>Khởi Động Trước</color> cho toàn bộ đồng minh trong <color=#f26c1c>2 hiệp</color>."
            }
        ],
        "keys": [
            {
                "name": "Khóa Cố Định 1 - Công Sức Và Thành Quả",
                "level": 20,
                "effect": "Bước Nhảy Ngẫu Hứng: Khi tiêu hao thêm điểm Chỉ Số Nhiên Liệu, ST Bạo Kích gây ra tăng <color=#f26c1c>5%</color>.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 2 - Đắm Chìm Trong Ánh Đèn",
                "level": 20,
                "effect": "Vũ Công Xuất Sắc: Khi hiệu ứng này được kích hoạt, hồi phục HP tương đương <color=#f26c1c>20%</color> HP tối đa.",
                "materials": "3\n\n\n3000"
            },
            {
                "name": "Khóa Cố Định 3 - Nhịp Điệu Cộng Hưởng",
                "level": 30,
                "effect": "Bước Nhảy Ngẫu Hứng: Trước khi sử dụng kỹ năng, giải trừ <color=#f26c1c>1</color> Buff ngẫu nhiên từ mục tiêu.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 4 - Cảm Xúc Lan Tỏa",
                "level": 30,
                "effect": "Linh Hồn Vũ Đạo: Sau khi kỹ năng này áp dụng Choáng lên kẻ địch, khi trạng thái Choáng kết thúc, áp dụng <color=#3487e0>Vô Hiệu Hóa Di Chuyển</color> trong <color=#f26c1c>1 hiệp</color>.",
                "materials": "3\n\n\n8000"
            },
            {
                "name": "Khóa Cố Định 5 - Bước Chuyển Kỳ Diệu",
                "level": 40,
                "effect": "Nếu hiệp này Yoohee không di chuyển, tầm bắn của đòn đánh thường và các kỹ năng tăng <color=#f26c1c>3 ô</color> ở hiệp tiếp theo.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Cố Định 6 - Vũ Đạo Tinh Tế",
                "level": 40,
                "effect": "Quyết Không Nhận Thua: Khi hiệu ứng này đang kích hoạt, Tấn Công tăng <color=#f26c1c>10%</color>.",
                "materials": "3\n\n\n12000"
            },
            {
                "name": "Khóa Tương Thích - Vũ Điệu Đam Mê",
                "level": "-",
                "effect": "Tấn Công +3%, Phòng Thủ +3%, HP +3%",
                "materials": "Mở khóa khi Độ Tương Thích đạt Lv.5"
            },
            {
                "name": "Khóa Chung - Uy Lực Của Vũ Công Chính",
                "level": 40,
                "effect": "Tấn Công +5% / Khi gây sát thương loại Đạn Dược, ST gây ra tăng <color=#f26c1c>10%</color>.",
                "materials": "None"
            },
            {
                "name": "Khóa Mở Rộng - Vũ Điệu Hoàn Hảo",
                "level": 60,
                "effect": "Sau khi sử dụng Hạ Màn Lộng Lẫy, khi dùng Bước Nhảy Nhẹ Nhàng hoặc Bước Nhảy Nhiệt Tình, kỹ năng cũng sẽ kích hoạt lên 2 đồng minh có Tấn Công cao nhất chưa được chọn bởi kỹ năng (không bao gồm bản thân). 2 kỹ năng này sẽ không thể tiếp tục sử dụng trong hiệp hiện tại.\n\nKhi gây ST Vật Lý từ kỹ năng bị động, sẽ kích hoạt hiệu ứng của <color=#3487e0>Quyết Không Nhận Thua</color>. Hiệu ứng của nó sẽ không còn bị vô hiệu hóa nếu đồng minh gây sát thương thuộc tính.\n\nTăng <color=#f26c1c>50%</color> lượng trị liệu nhận vào cho đồng minh. Khi bắt đầu chiến đấu, cứ mỗi đồng minh thuộc tính Vật Lý trên sân, tăng <color=#f26c1c>3%</color> ST Vật Lý gây ra bởi đồng minh, tối đa tăng <color=#f26c1c>15%</color>.",
                "materials": "3\n\n\n15000"
            }
        ]
    }
}
