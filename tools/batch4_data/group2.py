"""
Auto-synced batch data.
"""

GROUP_2_DATA = {'lewis': {'name': 'Lewis',
           'en_name': 'Lewis',
           'class': 'Vệ Binh',
           'phase': 'Đốt Cháy',
           'rarity': 'Tinh Nhuệ',
           'weapon_type': 'Súng Máy',
           'ammo_type': 'Đạn Nặng',
           'signature_weapon': 'Lời Chúc Ấm Áp',
           'weakness': 'Hóa Lỏng',
           'server': 'global',
           'skills': [{'name': 'Giờ Chơi Đùa',
                       'tags': ['Đánh Thường', 'Chuẩn Xác'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây '
                                      'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                      {'name': 'Dọn Dẹp Kẻ Xấu',
                       'tags': ['Chủ Động', 'AoE', 'Suy Yếu'],
                       'description': 'Chọn 1 ô địa hình trong phạm vi 8 ô, gây ST Đốt Cháy AoE bằng '
                                      '<color=#f26c1c>100%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 3×3 ô và '
                                      'áp dụng <color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>2 hiệp</color>. '
                                      'Lewis nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                      {'name': 'Quả Cầu Bất Ngờ',
                       'tags': ['Chủ Động', 'Chuẩn Xác', 'Cường Hóa'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây '
                                      'ST Đốt Cháy bằng <color=#f26c1c>120%</color> Tấn Công. Áp dụng '
                                      '<color=#3487e0>Lửa Thiêu Đốt</color> lên mục tiêu trong <color=#f26c1c>2 '
                                      'hiệp</color>. Nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Công '
                                      'Huân</color>.'},
                      {'name': 'Lễ Hội Đồ Chơi',
                       'tags': ['Tuyệt Kỹ', 'Chuẩn Xác'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây '
                                      'ST Đốt Cháy bằng <color=#f26c1c>180%</color> Tấn Công. Nếu mục tiêu mang Debuff '
                                      'hệ Đốt Cháy, kích hoạt hiệu lệnh <color=#3487e0>Lính Chì</color> bắn hỗ trợ gây '
                                      'thêm ST Đốt Cháy bằng <color=#f26c1c>60%</color> Tấn Công.'},
                      {'name': 'Lính Chì Diễu Hành',
                       'tags': ['Bị Động', 'Cường Hóa'],
                       'description': 'Khi bắt đầu trận chiến, Lewis nhận <color=#3487e0>Hiệu Lệnh Lính Chì</color>. '
                                      'Khi gây ST Đốt Cháy, Lewis tích lũy điểm Công Huân để thăng cấp Lính Chì (tối '
                                      'đa cấp 3). Mỗi cấp tăng Tấn Công thêm <color=#f26c1c>5%</color> và tăng sát '
                                      'thương các đòn phối hợp <color=#3487e0>Cùng Bắn</color>.'}],
           'fortification': [{'tier': 1,
                              'level': 2,
                              'skill': 'Lính Chì Diễu Hành',
                              'effect': 'Hệ số sát thương cơ bản của Bắn Đồng Loạt tăng lên '
                                        '<color=#f26c1c>120%</color> Tấn Công của Lewis.\n'
                                        'Khi Lính Chì thi triển Bắn Đồng Loạt, nếu mục tiêu địch có '
                                        '<color=#3487e0>Tràn Lửa</color>, hiệu ứng <color=#3487e0>Tràn Lửa</color> sẽ '
                                        'được kích hoạt số lần tương ứng với Cấp Bậc của chúng.'},
                             {'tier': 2,
                              'level': 2,
                              'skill': 'Lễ Hội Đồ Chơi',
                              'effect': 'Giảm tiêu hao Chỉ Số Nhiên Liệu đi <color=#f26c1c>2 điểm</color>.\n'
                                        'Bổ sung thêm hiệu ứng dựa trên Cấp Bậc hiện tại cao nhất của bạn. Hiệu ứng '
                                        'cấp cao hơn bao gồm cả hiệu ứng cấp thấp hơn:\n'
                                        'Cấp 1: Nhận <color=#3487e0>ST Tăng II</color> trước khi tấn công, duy trì '
                                        'trong <color=#f26c1c>2 hiệp</color>.\n'
                                        'Cấp 2: Đòn tấn công này bỏ qua vật chắn (Yểm Hộ).\n'
                                        'Cấp 3: Tăng hệ số sát thương lên <color=#f26c1c>200%</color> Tấn Công của '
                                        'bạn.'},
                             {'tier': 3,
                              'level': 2,
                              'skill': 'Quả Cầu Bất Ngờ',
                              'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>160%</color>, hệ số sát thương cố '
                                        'định tăng lên <color=#f26c1c>50%</color>.\n'
                                        '\n'
                                        'Sửa đổi hiệu ứng <color=#3487e0>Hiệu Lệnh Lính Chì</color>: Không còn số tầng '
                                        'và không còn bị tiêu hao bởi Bắn Đồng Loạt. Thay vào đó duy trì trong '
                                        '<color=#f26c1c>3 hiệp</color> và tăng sát thương Bắn Đồng Loạt thêm '
                                        '<color=#f26c1c>50%</color>.'},
                             {'tier': 4,
                              'level': 2,
                              'skill': 'Dọn Dẹp Kẻ Xấu',
                              'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>120%</color>. Với mỗi Debuff thuộc '
                                        'tính Thiêu Đốt trên mục tiêu, đòn tấn công này gây thêm '
                                        '<color=#f26c1c>10%</color> sát thương, tối đa tăng '
                                        '<color=#f26c1c>30%</color>.'},
                             {'tier': 5,
                              'level': 3,
                              'skill': 'Lễ Hội Đồ Chơi',
                              'effect': 'Mỗi Lính Chì tăng thêm hệ số sát thương cho đòn tấn công này thêm '
                                        '<color=#f26c1c>10%</color> theo mỗi Cấp Bậc; sát thương bạo kích tăng thêm '
                                        '<color=#f26c1c>5%</color> theo mỗi Cấp Bậc.'},
                             {'tier': 6,
                              'level': 3,
                              'skill': 'Lính Chì Diễu Hành',
                              'effect': 'Lính Chì được chỉ định khi bắt đầu trận chiến có Cấp 2.\n'
                                        'Cường hóa hiệu ứng Cấp Bậc:\n'
                                        'Cấp 2: Tăng thêm <color=#f26c1c>15%</color> ST Bạo Kích.\n'
                                        'Cấp 3: Vào cuối hành động của Doll được chỉ định, tung ra 1 lần Bắn Đồng Loạt '
                                        'nhắm vào mục tiêu địch gần nhất. Đợt Bắn Đồng Loạt này cung cấp '
                                        '<color=#3487e0>Lửa Thiêu Đốt</color> nhưng không hồi phục Chỉ Số Nhiên '
                                        'Liệu.'}],
           'keys': [{'name': 'Khóa Cố Định 1 - Nhà Thiết Kế Mộng Mơ',
                     'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                    {'name': 'Khóa Cố Định 2 - Bí Mật Nụ Cười',
                     'effect': 'Khi tiêu diệt kẻ địch mang Debuff hệ Đốt Cháy, nhận thêm 1 tầng Công Huân.'},
                    {'name': 'Khóa Cố Định 3 - Người Bảo Vệ Ngây Thơ',
                     'effect': 'Trước khi tấn công chủ động, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên mục '
                               'tiêu trong <color=#f26c1c>2 hiệp</color>.'},
                    {'name': 'Khóa Cố Định 4 - Trí Tưởng Tượng Tươi Sáng',
                     'effect': 'Sát thương gây ra lên mục tiêu mang Tràn Lửa tăng thêm <color=#f26c1c>15%</color>.'},
                    {'name': 'Khóa Cố Định 5 - Đáng Yêu Là Công Lý',
                     'effect': 'Khi sở hữu Lính Chì, sát thương nhận vào giảm <color=#f26c1c>15%</color>.'},
                    {'name': 'Khóa Cố Định 6 - Hộ Vệ Từ Tầng Mây',
                     'effect': 'Sau khi dùng Lễ Hội Đồ Chơi, nhận <color=#f26c1c>3 ô</color> <color=#3487e0>Di Chuyển '
                               'Bổ Sung</color>.'},
                    {'name': 'Khóa Tương Thích - Trái Tim Trẻ Thơ', 'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                    {'name': 'Khóa Chung - Phép Màu Vĩ Đại',
                     'effect': 'Tấn Công +5.0% / Khi gây ST Đốt Cháy lên kẻ địch, sát thương tăng thêm '
                               '<color=#f26c1c>7%</color>.'},
                    {'name': 'Khóa Mở Rộng - Lính Chì Tập Hợp',
                     'effect': 'Đòn đánh bỏ qua <color=#f26c1c>20%</color> Phòng Thủ của mục tiêu. Khi Lính Chì thực '
                               'hiện Cùng Bắn, áp dụng Tràn Lửa lên mục tiêu trong 2 hiệp.'}]},
 'lind': {'name': 'Lind',
          'en_name': 'Lind',
          'class': 'Vệ Binh',
          'phase': 'Ăn Mòn',
          'rarity': 'Tinh Nhuệ',
          'weapon_type': 'Súng Tiểu Liên',
          'ammo_type': 'Đạn Nhẹ',
          'signature_weapon': 'Kẹo Ngọt Độc Dược',
          'weakness': 'Hóa Lỏng',
          'server': 'global',
          'skills': [{'name': 'Bắn Đẩy Lùi',
                      'tags': ['Đánh Thường', 'Chuẩn Xác'],
                      'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây ST '
                                     'Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                     {'name': 'Bình Xịt Đột Kích',
                      'tags': ['Chủ Động', 'AoE', 'Suy Yếu'],
                      'description': 'Chọn 1 ô địa hình trong phạm vi 6 ô, gây ST Ăn Mòn AoE bằng '
                                     '<color=#f26c1c>100%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 3×3 ô và '
                                     'áp dụng <color=#3487e0>Kẹo Đường</color> trong <color=#f26c1c>2 hiệp</color>. '
                                     'Lind nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                     {'name': 'Bộc Phá Áp Đảo',
                      'tags': ['Chủ Động', 'AoE'],
                      'description': 'Gây ST Ăn Mòn AoE bằng <color=#f26c1c>120%</color> Tấn Công lên tất cả kẻ địch '
                                     'trong phạm vi 3 ô quanh bản thân. Kẻ địch mang Kẹo Đường phải chịu thêm '
                                     '<color=#f26c1c>30%</color> sát thương.'},
                     {'name': 'Quá Tải Đường Huyết',
                      'tags': ['Tuyệt Kỹ', 'AoE'],
                      'description': 'Gây ST Ăn Mòn AoE bằng <color=#f26c1c>160%</color> Tấn Công lên toàn bộ kẻ địch '
                                     'trong phạm vi 5 ô quanh bản thân và kích nổ toàn bộ tầng Kẹo Đường, gây thêm sát '
                                     'thương tương ứng với số tầng tiêu hao. Lind nhận <color=#3487e0>Tăng Hành '
                                     'Động</color>.'},
                     {'name': 'Kho Dự Trữ Kẹo',
                      'tags': ['Bị Động', 'Suy Yếu'],
                      'description': 'Khi gây ST Ăn Mòn, Lind tích lũy các tầng Kẹo Đường trên mục tiêu. Kẻ địch mang '
                                     'Kẹo Đường bị giảm <color=#f26c1c>10%</color> Phòng Thủ và giảm <color=#f26c1c>1 '
                                     'ô</color> Di Chuyển. Khi mục tiêu tử trận, Lind nhận <color=#3487e0>Lá Chắn Tốc '
                                     'Độ</color> trong <color=#f26c1c>1 hiệp</color>.'}],
          'fortification': [{'tier': 1,
                             'level': 2,
                             'skill': 'Kho Dự Trữ Kẹo',
                             'effect': 'Khi bắt đầu trận chiến, với mỗi đồng minh hiện diện, Lind nhận '
                                       '<color=#f26c1c>1 tầng</color> <color=#3487e0>Kẹo Đường</color>. Tăng số tầng '
                                       'tối đa của <color=#3487e0>Kẹo Đường</color> lên <color=#f26c1c>30 '
                                       'tầng</color>.\n'
                                       '\n'
                                       'Cường hóa hiệu ứng <color=#3487e0>Kẹo Đường</color> - Tăng '
                                       '<color=#f26c1c>2%</color> <color=#5bcc3b>ST Ăn Mòn</color> gây ra.'},
                            {'tier': 2,
                             'level': 2,
                             'skill': 'Quá Tải Đường Huyết',
                             'effect': 'Tăng sát thương gây ra bởi kỹ năng chủ động tiếp theo thêm '
                                       '<color=#f26c1c>15%</color>.\n'
                                       '\n'
                                       'Cường hóa hiệu ứng <color=#3487e0>Chứng Nhiễm Ceton</color> - Mục tiêu nhận '
                                       'thêm <color=#f26c1c>12%</color> <color=#5bcc3b>ST Ăn Mòn</color> từ Lind, tối '
                                       'đa lên tới <color=#f26c1c>72%</color>.'},
                            {'tier': 3,
                             'level': 3,
                             'skill': 'Kho Dự Trữ Kẹo',
                             'effect': 'Loại bỏ thời gian hồi chiêu để áp dụng <color=#3487e0>Cạm Bẫy Ngọt '
                                       'Ngào</color> khi bắt đầu hiệp.\n'
                                       '\n'
                                       'Khi <color=#3487e0>Cạm Bẫy Ngọt Ngào</color> được kích hoạt, tăng số lượng '
                                       'Debuff mạnh ngẫu nhiên được áp dụng thêm <color=#f26c1c>3</color>, tăng hệ số '
                                       'sát thương lên <color=#f26c1c>120%</color> Tấn Công, và tăng ST Bạo Kích thêm '
                                       '<color=#f26c1c>15%</color>.'},
                            {'tier': 4,
                             'level': 2,
                             'skill': 'Bình Xịt Đột Kích',
                             'effect': 'Áp dụng <color=#f26c1c>2 tầng</color> <color=#3487e0>Giải Phóng Phụ '
                                       'Thuộc</color>.\n'
                                       '\n'
                                       'Mở rộng phạm vi hiệu lực của kỹ năng từ khu vực hình quạt nhỏ thành khu vực '
                                       'hình quạt (mở rộng 2×6 ô sang trái và phải của khu vực ban đầu).\n'
                                       '\n'
                                       'Với mỗi Debuff trên kẻ địch, tăng sát thương gây ra thêm '
                                       '<color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>60%</color>.'},
                            {'tier': 5,
                             'level': 2,
                             'skill': 'Bộc Phá Áp Đảo',
                             'effect': 'Tăng hệ số sát thương lên <color=#f26c1c>120%</color> Tấn Công và tăng ST Ổn '
                                       'Định gây ra thêm <color=#f26c1c>1 điểm</color>.\n'
                                       '\n'
                                       'Trước khi dùng kỹ năng, nếu Chỉ Số Nhiên Liệu đạt tối đa, tăng ST Bạo Kích '
                                       'thêm <color=#f26c1c>20%</color>; với mỗi tầng <color=#3487e0>Kẹo '
                                       'Đường</color>, tăng hệ số sát thương thêm <color=#f26c1c>10%</color>.'},
                            {'tier': 6,
                             'level': 3,
                             'skill': 'Quá Tải Đường Huyết',
                             'effect': 'Sau khi dùng kỹ năng, tăng Chỉ Số Nhiên Liệu thêm <color=#f26c1c>3 '
                                       'điểm</color>. Nếu Lind có <color=#f26c1c>10 tầng</color> <color=#3487e0>Kẹo '
                                       'Đường</color>, giảm thời gian hồi chiêu của kỹ năng này đi <color=#f26c1c>1 '
                                       'hiệp</color>.'}],
          'keys': [{'name': 'Khóa Cố Định 1 - Cảm Giác Đau Đớn',
                    'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                   {'name': 'Khóa Cố Định 2 - Sự Nhạy Bén Của Cú Đêm',
                    'effect': 'Khi tấn công mục tiêu có Kẹo Đường, tỷ lệ bạo kích tăng thêm '
                              '<color=#f26c1c>15%</color>.'},
                   {'name': 'Khóa Cố Định 3 - Lời Mời Phát Thanh',
                    'effect': 'Trước khi tấn công chủ động, giải trừ <color=#f26c1c>1</color> Buff của mục tiêu.'},
                   {'name': 'Khóa Cố Định 4 - Phán Xét Văn Minh',
                    'effect': 'Kẻ địch mang Kẹo Đường bị giảm thêm <color=#f26c1c>1 điểm</color> ST Ổn Định khi chịu '
                              'đòn.'},
                   {'name': 'Khóa Cố Định 5 - Trị Liệu Bằng Điểm Tâm',
                    'effect': 'Khi tiêu diệt kẻ địch có Kẹo Đường, Lind hồi phục lượng HP bằng '
                              '<color=#f26c1c>25%</color> HP tối đa.'},
                   {'name': 'Khóa Cố Định 6 - Phản Ứng Cai Nghiện',
                    'effect': 'Sau khi kích nổ Quá Tải Đường Huyết, nhận <color=#f26c1c>3 ô</color> <color=#3487e0>Di '
                              'Chuyển Bổ Sung</color>.'},
                   {'name': 'Khóa Tương Thích - Vị Ngọt Chết Người', 'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                   {'name': 'Khóa Chung - Đêm Dài Vô Tận',
                    'effect': 'Tấn Công +5.0% / Tăng sát thương gây ra lên mục tiêu mang Debuff hệ Ăn Mòn thêm '
                              '<color=#f26c1c>7%</color>.'},
                   {'name': 'Khóa Mở Rộng - Viên Đạn Bọc Đường',
                    'effect': 'Đòn đánh bỏ qua <color=#f26c1c>25%</color> Phòng Thủ của mục tiêu có Kẹo Đường. Sau khi '
                              'dùng Quá Tải Đường Huyết, nhận hiệu ứng <color=#3487e0>Cạm Bẫy Ngọt Ngào</color> trong '
                              '2 hiệp.'}]},
 'liushih': {'name': 'Liushih',
             'en_name': 'Liushih',
             'class': 'Vệ Binh',
             'phase': 'Hóa Lỏng',
             'rarity': 'Tinh Nhuệ',
             'weapon_type': 'Súng Bắn Tỉa',
             'ammo_type': 'Đạn Nặng',
             'signature_weapon': 'Thủy Triều Sóng Dữ',
             'weakness': 'Dẫn Điện',
             'server': 'global',
             'skills': [{'name': 'Phá Vỡ Trận Tuyến',
                         'tags': ['Đánh Thường', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây '
                                        'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                        {'name': 'Được Ăn Cả',
                         'tags': ['Chủ Động', 'Chuẩn Xác', 'Cường Hóa'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây '
                                        'ST Hóa Lỏng bằng <color=#f26c1c>130%</color> Tấn Công. Áp dụng '
                                        '<color=#3487e0>Phong Tỏa</color> lên mục tiêu trong <color=#f26c1c>2 '
                                        'hiệp</color>. Liushih nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                        {'name': 'Nước Cờ Chiến Lược',
                         'tags': ['Chủ Động', 'Cường Hóa'],
                         'description': 'Liushih ra lệnh kích hoạt chế độ nạp đạn đặc biệt, đòn đánh kế tiếp được tính '
                                        'là <color=#3487e0>Đòn Tấn Công Đã Nạp</color> và nhận <color=#3487e0>Chỉ Lệnh '
                                        'Bổ Sung</color>. Liushih nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên '
                                        'Liệu.'},
                        {'name': 'Dẫn Đầu Xung Phong',
                         'tags': ['Tuyệt Kỹ', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây '
                                        'ST Hóa Lỏng bằng <color=#f26c1c>180%</color> Tấn Công. Nếu mục tiêu mang '
                                        'Phong Tỏa, đòn đánh bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu '
                                        'và Liushih nhận <color=#3487e0>Tăng Hành Động</color>.'},
                        {'name': 'Đồng Tâm Tác Chiến',
                         'tags': ['Bị Động', 'Triệu Hồi', 'Suy Yếu'],
                         'description': 'Khi bắt đầu trận chiến, triệu hồi Pegasus tại vị trí chỉ định. Khi Liushih '
                                        'hoặc Pegasus tấn công mục tiêu mang Phong Tỏa, kích hoạt <color=#3487e0>Tác '
                                        'Chiến Phối Hợp</color> gây thêm ST Hóa Lỏng bằng <color=#f26c1c>50%</color> '
                                        'Tấn Công.'}],
             'summons': [{'name': 'Pegasus',
                          'type': 'Vật Triệu Hồi Vật Lý',
                          'description': 'Tháp pháo phòng thủ điểm tự động. Không thể di chuyển. Khi chịu sát thương '
                                         'chí tử, Pegasus chuyển sang trạng thái Chờ Lệnh.',
                          'stats': {'hp': '100% HP ban đầu của Liushih',
                                    'atk': '100% Tấn Công ban đầu của Liushih',
                                    'def': '100% Phòng Thủ ban đầu của Liushih'},
                          'skills': [{'name': 'Pháo Tự Động Phòng Thủ Điểm',
                                      'tags': ['Bị Động', 'Chuẩn Xác'],
                                      'description': 'Gây ST Hóa Lỏng bằng 110% Tấn Công lên mục tiêu trong tầm bắn. '
                                                     'Được tính là Đòn Tấn Công Đã Nạp và đòn đánh thường.'},
                                     {'name': 'Giao Thức An Toàn',
                                      'tags': ['Bị Động'],
                                      'description': 'Không thể di chuyển. Khi nhận sát thương chí tử, chuyển sang '
                                                     'trạng thái Chờ Lệnh và hủy bỏ trạng thái Tác Chiến Phối Hợp.'}]}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Đồng Tâm Tác Chiến',
                                'effect': 'Khi kết thúc hành động của Liushih, Pegasus bắn <color=#f26c1c>1 '
                                          'lần</color> Pháo Tự Động Phòng Thủ Điểm vào mục tiêu địch gần nhất trong '
                                          'phạm vi.'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Nước Cờ Chiến Lược',
                                'effect': 'Tạo các ô địa hình <color=#3487e0>Dòng Ngầm</color> trên đường di chuyển '
                                          'trong <color=#f26c1c>2 hiệp</color>. Pegasus không còn bị rút khỏi trạng '
                                          'thái <color=#3487e0>Tác Chiến Phối Hợp</color>.'},
                               {'tier': 3,
                                'level': 2,
                                'skill': 'Được Ăn Cả',
                                'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>120%</color>.\n'
                                          'Cải thiện hiệu ứng <color=#3487e0>Độ chính xác</color>: Tăng hệ số sát '
                                          'thương của đòn đánh thường thêm <color=#f26c1c>20%</color> cho mỗi tầng.'},
                               {'tier': 4,
                                'level': 2,
                                'skill': 'Dẫn Đầu Xung Phong',
                                'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>120%</color>.\n'
                                          '<color=#3487e0>Tác Chiến Phối Hợp</color> nhận hiệu ứng mới: ST Bạo Kích '
                                          'của Liushih và Pegasus tăng thêm <color=#f26c1c>30%</color>.'},
                               {'tier': 5,
                                'level': 3,
                                'skill': 'Đồng Tâm Tác Chiến',
                                'effect': 'Với mỗi <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu nhận được trong '
                                          'hiệp hiện tại, trước khi sử dụng kỹ năng chủ động Được Ăn Cả ở hiệp tiếp '
                                          'theo, bản thân và tất cả vật triệu hồi thực thể phe đồng minh nhận '
                                          '<color=#f26c1c>1 tầng</color> <color=#3487e0>Sắc bén</color>, duy trì trong '
                                          '<color=#f26c1c>1 hiệp</color>.'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Được Ăn Cả',
                                'effect': 'Gấp đôi số tầng <color=#3487e0>Độ chính xác</color> nhận được.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Phối Hợp Hoàn Hảo',
                       'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                      {'name': 'Khóa Cố Định 2 - Thiện Xạ',
                       'effect': 'Khi dùng Đòn Tấn Công Đã Nạp, tỷ lệ bạo kích tăng thêm <color=#f26c1c>20%</color>.'},
                      {'name': 'Khóa Cố Định 3 - Không Tiếc Công Sức',
                       'effect': 'Trước khi tấn công chủ động, giải trừ <color=#f26c1c>1</color> Buff của mục tiêu.'},
                      {'name': 'Khóa Cố Định 4 - Ý Chí Bất Khuất',
                       'effect': 'Khi Pegasus có mặt trên sân, Liushih giảm <color=#f26c1c>15%</color> sát thương phải '
                                 'gánh chịu.'},
                      {'name': 'Khóa Cố Định 5 - Đầu Tư Trọng Điểm',
                       'effect': 'Sát thương gây ra lên mục tiêu mang Phong Tỏa tăng thêm <color=#f26c1c>15%</color>.'},
                      {'name': 'Khóa Cố Định 6 - Tiếng Gọi Xuất Trận',
                       'effect': 'Sau khi dùng Dẫn Đầu Xung Phong, nhận <color=#f26c1c>3 ô</color> <color=#3487e0>Di '
                                 'Chuyển Bổ Sung</color>.'},
                      {'name': 'Khóa Tương Thích - Điện Ngọc Huy Hoàng',
                       'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                      {'name': 'Khóa Chung - Tiềm Lực Tài Chính',
                       'effect': 'Tấn Công +5.0% / Khi gây sát thương lên mục tiêu mang Debuff hệ Hóa Lỏng, sát thương '
                                 'tăng <color=#f26c1c>7%</color>.'}]},
 'loreley': {'name': 'Loreley',
             'en_name': 'Loreley',
             'class': 'Hỗ Trợ',
             'phase': 'Đốt Cháy',
             'rarity': 'Tinh Nhuệ',
             'weapon_type': 'Súng Trường Tấn Công',
             'ammo_type': 'Đạn Vừa',
             'signature_weapon': 'Khúc Ca Bỏng Rát',
             'weakness': 'Hóa Lỏng',
             'server': 'global',
             'skills': [{'name': 'Khúc Dạo Đầu Trừng Phạt',
                         'tags': ['Đánh Thường', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây '
                                        'ST Đốt Cháy bằng <color=#f26c1c>80%</color> Tấn Công.'},
                        {'name': 'Dấu Ấn Thiêu Đốt',
                         'tags': ['Chủ Động', 'Chuẩn Xác', 'Cường Hóa'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây '
                                        'ST Đốt Cháy bằng <color=#f26c1c>120%</color> Tấn Công và áp dụng '
                                        '<color=#3487e0>Lửa Thiêu Đốt</color> trong <color=#f26c1c>2 hiệp</color>. '
                                        'Loreley nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                        {'name': 'Tuyên Ngôn Đỏ Thắm',
                         'tags': ['Chủ Động', 'AoE', 'Ô Địa Hình'],
                         'description': 'Chọn 1 ô địa hình trong phạm vi 7 ô, gây ST Đốt Cháy AoE bằng '
                                        '<color=#f26c1c>100%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 3×3 ô '
                                        'và tạo ô địa hình <color=#3487e0>Thiêu Rụi</color> trong <color=#f26c1c>2 '
                                        'hiệp</color>. Kẻ địch đứng trên ô địa hình phải chịu thêm trạng thái '
                                        '<color=#3487e0>Tràn Lửa</color>.'},
                        {'name': 'Ân Sủng Đau Đớn',
                         'tags': ['Tuyệt Kỹ', 'AoE', 'Cường Hóa', 'Ô Địa Hình', 'Triệu Hồi'],
                         'description': 'Triệu hồi Thợ Săn - Loại II tại ô chỉ định và tạo ô địa hình Thiêu Rụi trong '
                                        'bán kính 4 ô trong <color=#f26c1c>2 hiệp</color>. Toàn bộ đồng minh nhận '
                                        '<color=#3487e0>Vũ Điệu Cộng Sinh</color> trong <color=#f26c1c>2 hiệp</color>. '
                                        'Loreley nhận <color=#3487e0>Tăng Hành Động</color>.'},
                        {'name': 'Sự Hào Phóng Của Nữ Hoàng',
                         'tags': ['Bị Động', 'Cường Hóa'],
                         'description': 'Trước khi đồng minh nhận sát thương, Loreley ban tặng <color=#3487e0>Lửa Cháy '
                                        'Hoàn Hảo</color>, giúp vô hiệu hóa lần sát thương đó (kích hoạt tối đa 3 lần '
                                        'mỗi hiệp). Khi đồng minh gây ST Đốt Cháy, Loreley tích lũy thêm điểm Lửa '
                                        'Thiêu Đốt.'}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Ân Sủng Đau Đớn',
                                'effect': 'Hiệu ứng <color=#3487e0>Vũ Điệu Cộng Sinh</color> mới: Khi chịu sát thương '
                                          'chí tử, hồi phục <color=#f26c1c>25%</color> HP tối đa và <color=#f26c1c>5 '
                                          'điểm</color> Chỉ Số Ổn Định, giải trừ tất cả Debuff và giảm '
                                          '<color=#f26c1c>60%</color> sát thương phải chịu trong vòng <color=#f26c1c>1 '
                                          'hiệp</color>.\n'
                                          'Sau khi sử dụng đòn đánh thường hoặc kỹ năng chủ động, Thợ Săn - Loại II '
                                          'phát phóng thêm 1 lần Xung Hỏa Lực.\n'
                                          'Đồng thời giải trừ <color=#3487e0>Choáng</color> cho toàn bộ đơn vị đồng '
                                          'minh.'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Sự Hào Phóng Của Nữ Hoàng',
                                'effect': 'Số lần có thể áp dụng <color=#3487e0>Lửa Cháy Hoàn Hảo</color> tăng lên '
                                          '<color=#f26c1c>5 lần</color>.\n'
                                          'Chỉ Lệnh Bổ Sung được thay thế bằng Hành Động Thêm.\n'
                                          '<color=#3487e0>Tàn Tro Lửa Rực</color> không còn tăng sát thương Thiêu Đốt, '
                                          'thay vào đó tăng tất cả sát thương gây ra thêm <color=#f26c1c>45%</color>.'},
                               {'tier': 3,
                                'level': 3,
                                'skill': 'Ân Sủng Đau Đớn',
                                'effect': 'Thợ Săn - Loại II tạo thêm <color=#f26c1c>4 điểm</color> <color=#3487e0>Lửa '
                                          'Thiêu Đốt</color> khi được triệu hồi.\n'
                                          'Hệ số sát thương của Xung Hỏa Lực tăng gấp đôi; với mỗi đợt Xung Hỏa Lực '
                                          'được phóng ra, sát thương gây ra bởi Loreley tăng thêm '
                                          '<color=#f26c1c>10%</color>, tối đa <color=#f26c1c>60%</color>; ST Bạo Kích '
                                          'tăng thêm <color=#f26c1c>2%</color>, tối đa <color=#f26c1c>12%</color>.\n'
                                          'Áp dụng <color=#3487e0>Lửa Cháy Hoàn Hảo</color> cho toàn bộ đơn vị đồng '
                                          'minh.'},
                               {'tier': 4,
                                'level': 2,
                                'skill': 'Tuyên Ngôn Đỏ Thắm',
                                'effect': 'Tăng hệ số sát thương thêm <color=#f26c1c>30%</color> và tăng phạm vi hiệu '
                                          'lực thêm <color=#f26c1c>1 ô</color>.\n'
                                          'Với mỗi Buff thuộc tính Thiêu Đốt mà Loreley sở hữu, sát thương gây ra tăng '
                                          'thêm <color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>40%</color>.'},
                               {'tier': 5,
                                'level': 2,
                                'skill': 'Dấu Ấn Thiêu Đốt',
                                'effect': 'Kỹ năng bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu. Nếu mục '
                                          'tiêu đang đứng trên ô địa hình <color=#3487e0>Thiêu Rụi</color>, sát thương '
                                          'gây ra tăng thêm <color=#f26c1c>60%</color>.'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Sự Hào Phóng Của Nữ Hoàng',
                                'effect': '<color=#3487e0>Lửa Thiêu Đốt</color> nhận được bởi tất cả đơn vị đồng minh '
                                          'khi Loreley có mặt trên sân tăng thêm <color=#f26c1c>1 điểm</color>. Với '
                                          'mỗi Doll thuộc tính Thiêu Đốt trên sân, Tấn Công của Loreley tăng thêm '
                                          '<color=#f26c1c>6%</color>.\n'
                                          'Tấn Công từ <color=#3487e0>Dâng Trào Địa Ngục</color> được áp dụng bởi Thợ '
                                          'Săn - Loại II tăng lên <color=#f26c1c>12%</color>.\n'
                                          'Tăng cường hiệu ứng <color=#3487e0>Tàn Tro Lửa Rực</color>: Mức giảm sát '
                                          'thương tăng lên <color=#f26c1c>30%</color>.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Nhiệt Huyết Ẩn Giấu',
                       'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu và 10 '
                                 'điểm Lửa Thiêu Đốt.'},
                      {'name': 'Khóa Cố Định 2 - Ngưỡng Chịu Đựng',
                       'effect': 'Khi Xung Hỏa Lực của Thợ Săn gây sát thương, áp dụng <color=#3487e0>Tràn Lửa</color> '
                                 'lên mục tiêu trong <color=#f26c1c>1 hiệp</color>.'},
                      {'name': 'Khóa Cố Định 3 - Giấc Mộng Giao Thoa',
                       'effect': 'Khi Thợ Săn có mặt trên sân, ST Đốt Cháy của toàn bộ đồng minh tăng '
                                 '<color=#f26c1c>7%</color>.'},
                      {'name': 'Khóa Cố Định 4 - Sự Dịu Dàng Của Thiên Thần',
                       'effect': 'Trước khi tấn công chủ động, giải trừ <color=#f26c1c>1</color> Buff của mục tiêu.'},
                      {'name': 'Khóa Cố Định 5 - Bước Chân Của Ác Quỷ',
                       'effect': 'Khi bắt đầu trận chiến, Loreley nhận <color=#3487e0>Di Chuyển Tăng III</color> trong '
                                 '<color=#f26c1c>2 hiệp</color>.'},
                      {'name': 'Khóa Cố Định 6 - Kẻ Chinh Phục Tuyệt Đối',
                       'effect': 'Khi kẻ địch ELID thông thường kết thúc hành động trong bán kính 3 ô quanh Thợ Săn, '
                                 'lập tức bị hành quyết.'},
                      {'name': 'Khóa Tương Thích - Ngọn Lửa Tình Si',
                       'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                      {'name': 'Khóa Chung - Hơi Thở Âm Ỉ',
                       'effect': 'Tấn Công +5.0% / Khi mang Buff hệ Đốt Cháy, tỷ lệ bạo kích tăng '
                                 '<color=#f26c1c>10%</color>.'}]},
 'mechty': {'name': 'Mechty',
            'en_name': 'Mechty',
            'class': 'Hỗ Trợ',
            'phase': 'Ăn Mòn',
            'rarity': 'Tinh Nhuệ',
            'weapon_type': 'Súng Trường Tấn Công',
            'ammo_type': 'Đạn Vừa',
            'signature_weapon': 'Gối Ngủ Giấc Mơ',
            'weakness': 'Hóa Lỏng',
            'server': 'global',
            'skills': [{'name': 'Khởi Động Giờ Ngủ',
                        'tags': ['Đánh Thường', 'Chuẩn Xác'],
                        'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây '
                                       'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công. Ở Chế Độ Quyết Đấu, chuyển '
                                       'thành ST Ăn Mòn, tăng thêm <color=#f26c1c>2 điểm</color> ST Ổn Định và nhận '
                                       '<color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                       {'name': 'Chấn Động Giấc Mơ',
                        'tags': ['Chủ Động', 'AoE', 'Ô Địa Hình'],
                        'description': 'Chọn 1 mục tiêu trong phạm vi 8 ô, gây ST Ăn Mòn AoE bằng '
                                       '<color=#f26c1c>130%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 1 ô '
                                       'quanh mục tiêu. Ở Chế Độ Quyết Đấu, nhận <color=#3487e0>Di Chuyển Tăng '
                                       'II</color> trong <color=#f26c1c>1 hiệp</color> và tạo ô địa hình '
                                       '<color=#3487e0>Độc Chướng</color> trong <color=#f26c1c>2 hiệp</color>.'},
                       {'name': 'Đêm Không Mộng Mị',
                        'tags': ['Chủ Động', 'Cường Hóa', 'Trị Liệu'],
                        'description': 'Hồi phục <color=#f26c1c>6 điểm</color> Chỉ Số Ổn Định, giải trừ toàn bộ Debuff '
                                       'trên bản thân và áp dụng <color=#3487e0>Người Bảo Vệ Giấc Mơ</color> lên toàn '
                                       'bộ đồng minh trong phạm vi 8 ô trong <color=#f26c1c>2 hiệp</color>. Ở Chế Độ '
                                       'Quyết Đấu, có thể dùng tiếp kỹ năng chủ động hoặc đánh thường, đồng thời nhận '
                                       '1 tầng Bộ Trợ Ngủ.'},
                       {'name': 'Xứ Sở Thần Tiên Trong Mơ',
                        'tags': ['Tuyệt Kỹ', 'Cường Hóa'],
                        'description': 'Chuyển từ Chế Độ Bản Vá sang <color=#3487e0>Chế Độ Quyết Đấu</color> trong '
                                       '<color=#f26c1c>3 hiệp</color>. Áp dụng <color=#3487e0>Lá Chắn Ác Mộng</color> '
                                       'lên toàn đội và áp dụng <color=#3487e0>Ngập Tràn Độc Tố</color> lên kẻ địch '
                                       'gần nhất trong <color=#f26c1c>1 hiệp</color>.'},
                       {'name': 'Giấc Ngủ Ngắn Kỳ Bí',
                        'tags': ['Bị Động', 'Cường Hóa'],
                        'description': 'Khi bắt đầu trận chiến, Mechty kích hoạt <color=#3487e0>Chế Độ Bản Vá</color> '
                                       'và áp dụng <color=#3487e0>Ác Mộng Hóa</color> lên toàn bộ đồng minh.'}],
            'fortification': [{'tier': 1,
                               'level': 2,
                               'skill': 'Xứ Sở Thần Tiên Trong Mơ',
                               'effect': 'Không còn tắt <color=#3487e0>Chế Độ Bản Vá</color> khi vào '
                                         '<color=#3487e0>Chế Độ Quyết Đấu</color>.\n'
                                         '\n'
                                         '<color=#3487e0>Lá Chắn Ác Mộng</color> giảm Tấn Công của kẻ tấn công đi '
                                         '<color=#f26c1c>10%</color> và tăng số lượng Debuff được giải trừ thêm '
                                         '<color=#f26c1c>1</color>.\n'
                                         '\n'
                                         '<color=#3487e0>Chế Độ Quyết Đấu</color> nhận hiệu ứng mới: Tỷ lệ bạo kích '
                                         'của đòn đánh thường tăng thêm <color=#f26c1c>30%</color>.'},
                              {'tier': 2,
                               'level': 2,
                               'skill': 'Giấc Ngủ Ngắn Kỳ Bí',
                               'effect': '<color=#3487e0>Chế Độ Bản Vá</color> nhận hiệu ứng mới: Đòn đánh thường gây '
                                         'thêm <color=#f26c1c>50%</color> sát thương. Khi bắt đầu hiệp, giải trừ '
                                         '<color=#f26c1c>2</color> Debuff trên bản thân.'},
                              {'tier': 3,
                               'level': 2,
                               'skill': 'Đêm Không Mộng Mị',
                               'effect': 'Số tầng tối đa của <color=#3487e0>Bộ Trợ Ngủ</color> tăng thêm '
                                         '<color=#f26c1c>1 tầng</color>. Mechty hồi phục lượng HP bằng '
                                         '<color=#f26c1c>30%</color> HP tối đa, và đơn vị đồng minh có tỷ lệ HP thấp '
                                         'nhất hồi phục lượng HP bằng <color=#f26c1c>15%</color> HP tối đa của Mechty '
                                         'cùng <color=#f26c1c>3 điểm</color> Chỉ Số Ổn Định.\n'
                                         '\n'
                                         'Khi ở <color=#3487e0>Chế Độ Quyết Đấu</color>, số tầng <color=#3487e0>Bộ Trợ '
                                         'Ngủ</color> nhận được tăng thêm <color=#f26c1c>1 tầng</color>.'},
                              {'tier': 4,
                               'level': 2,
                               'skill': 'Chấn Động Giấc Mơ',
                               'effect': 'ST Ổn Định tăng thêm <color=#f26c1c>2 điểm</color>.\n'
                                         '\n'
                                         'Khi <color=#3487e0>Chế Độ Quyết Đấu</color> đang kích hoạt, tăng sát thương '
                                         'của đòn đánh thường tiếp theo thêm <color=#f26c1c>100%</color>. Gây sát '
                                         'thương cố định bằng <color=#f26c1c>50%</color> Tấn Công lên toàn bộ đơn vị '
                                         'địch trong phạm vi.'},
                              {'tier': 5,
                               'level': 3,
                               'skill': 'Xứ Sở Thần Tiên Trong Mơ',
                               'effect': '<color=#3487e0>Chế Độ Quyết Đấu</color> nhận hiệu ứng mới: Khả năng di '
                                         'chuyển tăng thêm <color=#f26c1c>2 ô</color>, áp dụng <color=#3487e0>Lá Chắn '
                                         'Ác Mộng</color> cho các đơn vị đồng minh chưa có Lá Chắn Ác Mộng vào cuối '
                                         'hành động. Nhận thêm <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                              {'tier': 6,
                               'level': 3,
                               'skill': 'Giấc Ngủ Ngắn Kỳ Bí',
                               'effect': '<color=#3487e0>Chế Độ Bản Vá</color> nhận hiệu ứng mới: <color=#5bcc3b>ST Ăn '
                                         'Mòn</color> gây ra bởi tất cả đơn vị đồng minh tăng thêm '
                                         '<color=#f26c1c>25%</color>, tăng ST Bạo Kích gây ra bởi đòn đánh thường của '
                                         'Mechty thêm <color=#f26c1c>80%</color>.\n'
                                         '\n'
                                         '<color=#3487e0>Ác Mộng Hóa</color> nhận hiệu ứng mới: Sát thương diện rộng '
                                         'gây ra bởi Đòn Đánh Chi Viện tăng lên <color=#f26c1c>80%</color>, ST Ổn Định '
                                         'gây ra tăng thêm <color=#f26c1c>1 điểm</color>, và sát thương diện rộng gây '
                                         'ra tăng lên <color=#f26c1c>20%</color>.'}],
            'keys': [{'name': 'Khóa Cố Định 1 - Mảnh Ghép Giấc Mơ',
                      'effect': 'Sau khi dùng đòn đánh thường Khởi Động Giờ Ngủ, nhận 1 Buff ngẫu nhiên trong '
                                '<color=#f26c1c>1 hiệp</color>.'},
                     {'name': 'Khóa Cố Định 2 - Ngủ Đi Ngủ Đi',
                      'effect': 'Nếu khai thác Điểm Yếu Thuộc Tính, áp dụng <color=#3487e0>Ngập Tràn Độc Tố</color> '
                                'lên mục tiêu sau đòn đánh.'},
                     {'name': 'Khóa Cố Định 3 - Đêm Phim Kinh Dị',
                      'effect': 'Khi dùng Chấn Động Giấc Mơ lên mục tiêu thể hình lớn, áp dụng <color=#3487e0>Ăn Mòn '
                                'Mạnh II</color> trong <color=#f26c1c>2 hiệp</color>.'},
                     {'name': 'Khóa Cố Định 4 - Nhanh Lên Còn Ngủ',
                      'effect': 'Khi dùng Đêm Không Mộng Mị, tạo ô địa hình Độc Chướng trong phạm vi 2 ô quanh kẻ địch '
                                'gần nhất trong <color=#f26c1c>2 hiệp</color>.'},
                     {'name': 'Khóa Cố Định 5 - Tinh Thần Kẻ Thua Cuộc',
                      'effect': 'Trước khi dùng đòn đánh thường Khởi Động Giờ Ngủ, giải trừ <color=#f26c1c>2</color> '
                                'Buff của mục tiêu.'},
                     {'name': 'Khóa Cố Định 6 - Hào Quang Sofa',
                      'effect': 'Khi có từ 2 Buff trở lên, sát thương đơn mục tiêu phải gánh chịu giảm '
                                '<color=#f26c1c>20%</color>.'},
                     {'name': 'Khóa Tương Thích - Giấc Ngủ Bình Yên', 'effect': 'Tấn Công +3%, Phòng Thủ +3%, HP +3%'},
                     {'name': 'Khóa Chung - Giờ Chơi Game',
                      'effect': 'Tấn Công +5.0% / Sát thương đòn đánh thường tăng thêm <color=#f26c1c>20%</color>.'},
                     {'name': 'Khóa Mở Rộng - Hội Chứng Mộng Du Cuồng Bạo',
                      'effect': 'Khi bắt đầu trận chiến, vào trạng thái Mộng Du và nhận kỹ năng: Chỉ Lệnh Thức Tỉnh.\n'
                                'Khi bắt đầu hiệp ở trạng thái Mộng Du, tiêu hao toàn bộ Chỉ Số Nhiên Liệu để nhận số '
                                'tầng tối đa Bộ Trợ Ngủ; với mỗi điểm tiêu hao, giải trừ 1 Debuff và nhận 1 tầng Giấc '
                                'Mơ Phấn Khởi.\n'
                                'Khi kết thúc hành động ở trạng thái Mộng Du, kích hoạt Mộng Tàn Đạn Lạc lên kẻ địch '
                                'gần nhất theo số tầng Bộ Trợ Ngủ và hồi phục 10% Tấn Công cùng 1 điểm Ổn Định cho '
                                'toàn đội.'}]}}
