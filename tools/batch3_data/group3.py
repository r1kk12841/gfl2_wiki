"""
Auto-synced batch data.
"""

GROUP_3_DATA = {'eagletta': {'name': 'Eagletta',
              'en_name': 'Eagletta',
              'class': 'Vệ Binh',
              'phase': 'Băng Kết',
              'rarity': 'Tinh Nhuệ',
              'weapon_type': 'Súng Lục',
              'ammo_type': 'Đạn Nhẹ',
              'signature_weapon': 'Vuốt Ưng Bạc',
              'weakness': 'Ăn Mòn',
              'server': 'cn',
              'skills': [{'name': 'Truy Kích Nhanh',
                          'tags': ['Đánh Thường'],
                          'description': 'Tùy thuộc vào <color=#3487e0>Tư Thế Tác Chiến</color>, Eagletta sử dụng đòn '
                                         'đánh thường Ưng Kích Chớp Nhoáng hoặc Móng Vuốt Xé Rách.'},
                         {'name': 'Ưng Kích Chớp Nhoáng',
                          'tags': ['Đánh Thường', 'Chuẩn Xác'],
                          'description': 'Tiêu hao 2 Lông Vũ Chiến Trận để chọn 1 mục tiêu địch <color=#f26c1c>trong '
                                         'phạm vi 6 ô xung quanh</color>, gây ST Băng Kết bằng '
                                         '<color=#f26c1c>100%</color> Tấn Công. Sát thương gây ra tăng thêm '
                                         '<color=#f26c1c>15%</color> và ST Bạo Kích tăng thêm '
                                         '<color=#f26c1c>5%</color>.\n'
                                         'Sau khi kỹ năng kết thúc, nhận <color=#f26c1c>6 ô</color> <color=#3487e0>Di '
                                         'Chuyển Bổ Sung</color> và có thể sử dụng 1 chỉ lệnh.\n'
                                         'Nếu mục tiêu bị tiêu diệt, vô hiệu hóa các kỹ năng và hiệu ứng kích hoạt khi '
                                         'tử trận của mục tiêu.\n'
                                         'Chỉ có thể dùng khi có từ 2 tầng Lông Vũ Chiến Trận trở lên.'},
                         {'name': 'Móng Vuốt Xé Rách',
                          'tags': ['Đánh Thường', 'Chuẩn Xác', 'Cận Chiến'],
                          'description': 'Chọn 1 mục tiêu địch trong phạm vi 3×3 ô, gây ST Băng Kết bằng '
                                         '<color=#f26c1c>60%</color> Tấn Công và hồi phục HP bằng '
                                         '<color=#f26c1c>20%</color> lượng sát thương gây ra.\n'
                                         'Nếu mục tiêu bị tiêu diệt, vô hiệu hóa các hiệu ứng kích hoạt khi tử trận '
                                         'của mục tiêu, Eagletta nhận <color=#f26c1c>8 ô</color> <color=#3487e0>Di '
                                         'Chuyển Bổ Sung</color> và có thể dùng 1 chỉ lệnh. Phạm vi của kỹ năng này '
                                         'không thể bị sửa đổi.'},
                         {'name': 'Chiến Thuật Uy Nhiếp',
                          'tags': ['Chủ Động'],
                          'description': 'Chuyển đổi <color=#3487e0>Tư Thế Tác Chiến</color>. Sau khi dùng, Eagletta '
                                         'nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Kỹ năng chỉ có thể dùng tối đa '
                                         '1 lần mỗi hiệp.\n'
                                         '\n'
                                         'Bị động: Khi bắt đầu hiệp, Eagletta chuyển sang thế <color=#3487e0>Ưng '
                                         'Kích</color>.'},
                         {'name': 'Cú Bổ Nhào Băng Giá',
                          'tags': ['Chủ Động', 'Chuẩn Xác', 'Suy Yếu', 'Khống Chế'],
                          'description': 'Chọn 1 ô địa hình trong bán kính 6 ô quanh bản thân và đáp xuống, gây ST '
                                         'Băng Kết bằng <color=#f26c1c>100%</color> Tấn Công lên mục tiêu địch gần '
                                         'nhất trong bán kính 4 ô và áp dụng <color=#3487e0>Dễ Bị Thương II</color> '
                                         'trong <color=#f26c1c>2 hiệp</color>.\n'
                                         'Sau đó, áp dụng <color=#3487e0>Khiêu Khích</color> và <color=#3487e0>Nữ '
                                         'Hoàng Bầu Trời</color> lên toàn bộ kẻ địch không phải Boss trong bán kính 4 '
                                         'ô quanh bản thân trong <color=#f26c1c>2 hiệp</color>. Eagletta nhận thêm '
                                         '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                         {'name': 'Vũ Điệu Bão Lông Vũ',
                          'tags': ['Tuyệt Kỹ', 'Chuẩn Xác'],
                          'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, '
                                         'gây ST Băng Kết bằng <color=#f26c1c>120%</color> Tấn Công và tiêu hao toàn '
                                         'bộ <color=#3487e0>Lông Vũ Chiến Trận</color>.\n'
                                         '\n'
                                         'Tiêu hao 1 lông vũ: Sát thương tăng thêm <color=#f26c1c>20%</color>.\n'
                                         'Tiêu hao 2 lông vũ: ST Bạo Kích tăng thêm <color=#f26c1c>35%</color> và ST '
                                         'Ổn Định tăng thêm <color=#f26c1c>4 điểm</color>.\n'
                                         'Tiêu hao 3 lông vũ: Hệ số sát thương tăng thêm <color=#f26c1c>50%</color> và '
                                         'Tấn Công tăng thêm <color=#f26c1c>10%</color>.\n'
                                         '\n'
                                         'Nếu mục tiêu bị tiêu diệt, vô hiệu hóa các hiệu ứng kích hoạt khi tử trận. '
                                         'Sau khi dùng xong, Eagletta chuyển sang thế <color=#3487e0>Đòn Vuốt '
                                         'Nặng</color>. Khi kết thúc hiệp đấu, nhận 7 Lông Vũ Chiến Trận.'},
                         {'name': 'Bản Năng Hoang Dã',
                          'tags': ['Bị Động', 'Cường Hóa'],
                          'description': 'Eagletta không nhận Chỉ Số Nhiên Liệu.\n'
                                         'Khi bắt đầu chiến đấu, Eagletta nhận 7 tầng <color=#3487e0>Lông Vũ Chiến '
                                         'Trận</color>.\n'
                                         'Khi kết thúc giai đoạn đồng minh, tạo ô địa hình <color=#3487e0>Băng '
                                         'Giá</color> trong bán kính 3 ô xung quanh Eagletta trong 2 hiệp. Sát thương '
                                         'gây ra tăng <color=#f26c1c>20%</color> và ST Bạo Kích tăng '
                                         '<color=#f26c1c>12%</color>.\n'
                                         '\n'
                                         'Nếu mục tiêu không nằm trong phạm vi 3×3 ô quanh Eagletta, mỗi 1 ô khoảng '
                                         'cách sẽ làm giảm sát thương 5% và ST Bạo Kích 3% (tối đa giảm 20% và 12%). '
                                         'Nếu mục tiêu dính hiệu ứng khống chế, Ngưng Tụ, Tê Liệt hoặc là đơn vị cỡ '
                                         'lớn, hiệu ứng giảm sát thương sẽ bị vô hiệu hóa.\n'
                                         '\n'
                                         'Khi ở thế Đòn Vuốt Nặng, nếu kẻ địch chuẩn bị di chuyển, tấn công hoặc kết '
                                         'thúc hành động trong phạm vi 3×3 ô và không có Sốc Điện, kích hoạt kỹ năng '
                                         'bị động <color=#3487e0>Săn Mồi</color> để thực hiện <color=#3487e0>Khóa Tấn '
                                         'Công</color>, tối đa 2 lần mỗi hiệp.\n'
                                         'Cứ mỗi 7 tầng Lông Vũ Chiến Trận tiêu hao, nhận 1 tầng <color=#3487e0>Đe Dọa '
                                         'Xâm Lấn</color>.\n'
                                         'Khi có Đe Dọa Xâm Lấn, tỷ lệ bạo kích tăng 25%; dùng đòn đánh thường Móng '
                                         'Vuốt Xé Rách và bị động Săn Mồi sẽ nhận 1 tầng Lông Vũ Chiến Trận.\n'
                                         '\n'
                                         'Khi có từ 4 tầng Đe Dọa Xâm Lấn trở lên và dùng Ưng Kích Chớp Nhoáng, tiêu '
                                         'hao 2 Lông Vũ Chiến Trận để tạo hiệu quả của Tuyệt kỹ Vũ Điệu Bão Lông Vũ '
                                         '(nhận toàn bộ hiệu ứng theo số lông vũ tiêu hao). Đòn đánh này được tính là '
                                         'đòn đánh thường, tối đa 1 lần mỗi hiệp.'}],
              'fortification': [{'tier': 1,
                                 'level': 2,
                                 'skill': 'Bản Năng Hoang Dã',
                                 'effect': 'Khi bắt đầu chiến đấu, nhận <color=#f26c1c>1 tầng</color> '
                                           '<color=#3487e0>Đe Dọa Xâm Lấn</color>. Khi sở hữu <color=#f26c1c>1 '
                                           'tầng</color> <color=#3487e0>Đe Dọa Xâm Lấn</color>, sử dụng đòn đánh '
                                           'thường Móng Vuốt Xé Rách và kỹ năng nội tại Săn Mồi nhận thêm '
                                           '<color=#f26c1c>1</color> Lông Vũ Chiến Trận. Khi sở hữu từ '
                                           '<color=#f26c1c>2 tầng</color> <color=#3487e0>Đe Dọa Xâm Lấn</color> trở '
                                           'lên, vào cuối hiệp, thời gian hồi chiêu của tuyệt kỹ Vũ Điệu Bão Lông Vũ '
                                           'giảm <color=#f26c1c>1 hiệp</color>. Nếu đòn đánh thường Ưng Kích Chớp '
                                           'Nhoáng hạ gục mục tiêu, nhận <color=#f26c1c>2</color> Lông Vũ Chiến Trận.'},
                                {'tier': 2,
                                 'level': 2,
                                 'skill': 'Chiến Thuật Uy Nhiếp',
                                 'effect': 'Bổ sung hiệu ứng nội tại: Vào cuối hiệp, nếu số lần Khóa Tấn Công của kỹ '
                                           'năng nội tại Bản Năng Hoang Dã chưa đạt giới hạn, nhận '
                                           '<color=#f26c1c>2</color> Lông Vũ Chiến Trận cho mỗi lần dùng còn lại. Hệ '
                                           'số sát thương của đòn đánh thường Ưng Kích Chớp Nhoáng tăng lên '
                                           '<color=#f26c1c>120%</color>, mức tăng sát thương gây ra nâng lên '
                                           '<color=#f26c1c>25%</color> và sát thương bạo kích tăng thêm nâng lên '
                                           '<color=#f26c1c>10%</color>. Hệ số sát thương của đòn đánh thường Móng Vuốt '
                                           'Xé Rách và kỹ năng nội tại Săn Mồi tăng lên <color=#f26c1c>80%</color>.'},
                                {'tier': 3,
                                 'level': 2,
                                 'skill': 'Cú Bổ Nhào Băng Giá',
                                 'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>120%</color>. Phạm vi áp dụng '
                                           '<color=#3487e0>Nữ Hoàng Bầu Trời</color> mở rộng thành phạm vi '
                                           '<color=#f26c1c>5 ô</color> quanh bản thân. Cường hóa hiệu ứng '
                                           '<color=#3487e0>Nữ Hoàng Bầu Trời</color>: Mức giảm sát thương của đòn tấn '
                                           'công đầu tiên nhắm vào Eagletta tăng lên <color=#f26c1c>40%</color>.'},
                                {'tier': 4,
                                 'level': 2,
                                 'skill': 'Vũ Điệu Bão Lông Vũ',
                                 'effect': 'Khi tiêu hao <color=#f26c1c>1</color> Lông Vũ Chiến Trận, mức tăng sát '
                                           'thương gây ra nâng lên <color=#f26c1c>30%</color>.\n'
                                           'Khi tiêu hao <color=#f26c1c>2</color> Lông Vũ Chiến Trận, mức tăng sát '
                                           'thương bạo kích nâng lên <color=#f26c1c>45%</color>.\n'
                                           'Khi tiêu hao <color=#f26c1c>3</color> Lông Vũ Chiến Trận, mức tăng hệ số '
                                           'sát thương nâng lên <color=#f26c1c>80%</color> và mức tăng Tấn Công nâng '
                                           'lên <color=#f26c1c>20%</color>.'},
                                {'tier': 5,
                                 'level': 3,
                                 'skill': 'Bản Năng Hoang Dã',
                                 'effect': 'Số lượng Lông Vũ Chiến Trận cần thiết để nhận <color=#3487e0>Đe Dọa Xâm '
                                           'Lấn</color> giảm xuống còn <color=#f26c1c>3</color>.'},
                                {'tier': 6,
                                 'level': 3,
                                 'skill': 'Chiến Thuật Uy Nhiếp',
                                 'effect': 'Bổ sung hiệu ứng nội tại: Khi tuyệt kỹ Vũ Điệu Bão Lông Vũ tiêu hao '
                                           '<color=#f26c1c>3</color> Lông Vũ Chiến Trận, hệ số sát thương tăng thêm '
                                           '<color=#f26c1c>30%</color>. Hiệu ứng này cũng áp dụng cho hiệu ứng kỹ năng '
                                           'Vũ Điệu Bão Lông Vũ được kích hoạt khi dùng đòn đánh thường Ưng Kích Chớp '
                                           'Nhoáng lúc đang có <color=#f26c1c>4 tầng</color> <color=#3487e0>Đe Dọa Xâm '
                                           'Lấn</color>. Với mỗi tầng <color=#3487e0>Đe Dọa Xâm Lấn</color>, sát '
                                           'thương bản thân gây ra tăng thêm <color=#f26c1c>10%</color>; khi một đơn '
                                           'vị địch chịu sát thương từ đơn vị đồng minh, nếu đứng trên ô địa hình '
                                           '<color=#42cce0>Băng Kết</color>, sát thương phải chịu tăng thêm '
                                           '<color=#f26c1c>10%</color> cho mỗi tầng <color=#3487e0>Đe Dọa Xâm '
                                           'Lấn</color>.\n'
                                           'Mức tăng Tấn Công từ tư thế Ưng Kích tăng thêm '
                                           '<color=#f26c1c>20%</color>.\n'
                                           'Hệ số sát thương của đòn đánh thường Ưng Kích Chớp Nhoáng tăng lên '
                                           '<color=#f26c1c>150%</color>, mức tăng sát thương gây ra nâng lên '
                                           '<color=#f26c1c>40%</color> và mức tăng sát thương bạo kích nâng lên '
                                           '<color=#f26c1c>15%</color>.\n'
                                           'Tỷ lệ bỏ qua Phòng Thủ của đòn đánh thường Móng Vuốt Xé Rách và kỹ năng '
                                           'nội tại Săn Mồi tăng lên <color=#f26c1c>10%</color>. Khi Lông Vũ Chiến '
                                           'Trận được tiêu hao bởi tư thế Trọng Trảo, mức tăng hệ số sát thương cho '
                                           'đòn đánh thường Móng Vuốt Xé Rách và kỹ năng nội tại Săn Mồi nâng lên '
                                           '<color=#f26c1c>10%</color>.'}],
              'keys': [{'name': 'Khóa Cố Định 1 - Uy Hiếp Của Kẻ Săn Mồi',
                        'effect': 'Sau khi dùng đòn đánh thường Móng Vuốt Xé Rách hoặc bị động Săn Mồi, nhận 1 tầng '
                                  'Lông Vũ Chiến Trận.'},
                       {'name': 'Khóa Cố Định 2 - Chúa Tể Bầu Trời',
                        'effect': 'Trước khi tấn công chủ động, giải trừ <color=#f26c1c>1</color> Buff của mục tiêu.'},
                       {'name': 'Khóa Cố Định 3 - Quan Sát Từ Trên Cao',
                        'effect': 'Khi kết thúc hiệp đồng minh, Eagletta hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số '
                                  'Ổn Định.'},
                       {'name': 'Khóa Cố Định 4 - Thống Trị Vòm Trời',
                        'effect': 'Khi tấn công kẻ địch mang Debuff hệ Dẫn Điện, sát thương gây ra tăng thêm '
                                  '<color=#f26c1c>15%</color>.'},
                       {'name': 'Khóa Cố Định 5 - Đôi Cánh Ngược Gió',
                        'effect': 'Trước khi dùng Ưng Kích Chớp Nhoáng, áp dụng <color=#3487e0>Phòng Thủ Giảm '
                                  'II</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>.'},
                       {'name': 'Khóa Cố Định 6 - Vùng Đất Chưa Khai Phá',
                        'effect': 'Khi chủ động tấn công, nếu Chỉ Số Ổn Định của mục tiêu thấp hơn 50%, sát thương gây '
                                  'ra tăng thêm <color=#f26c1c>20%</color>.'},
                       {'name': 'Khóa Tương Thích - Sự Chân Thành Giản Dị',
                        'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                       {'name': 'Khóa Chung - Nghệ Thuật Tự Hoàn Thiện',
                        'effect': 'Tấn Công tăng <color=#f26c1c>10%</color>. Khi mang trạng thái Buff, tăng thêm '
                                  '<color=#f26c1c>5%</color> ST Bạo Kích.'}]},
 'asteria': {'name': 'Asteria',
             'en_name': 'Asteria',
             'class': 'Hỗ Trợ',
             'phase': 'Vật Lý',
             'rarity': 'Tinh Nhuệ',
             'weapon_type': 'Súng Trường Tấn Công',
             'ammo_type': 'Đạn Vừa',
             'signature_weapon': 'Lời Hứa Xa Xăm',
             'weakness': 'Ăn Mòn',
             'server': 'cn',
             'skills': [{'name': 'Cò Súng Lặng Lẽ',
                         'tags': ['Đánh Thường', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây '
                                        'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                        {'name': 'Trận Hình Đột Kích',
                         'tags': ['Chủ Động', 'Cường Hóa'],
                         'description': 'Chọn 1 đồng minh trong bán kính 6 ô, áp dụng <color=#3487e0>Đồng Bộ</color> '
                                        'lên mục tiêu. Bản thân và mục tiêu nhận <color=#3487e0>Điềm Tĩnh</color> và '
                                        '<color=#3487e0>Hội Tâm</color> trong <color=#f26c1c>2 hiệp</color>. Asteria '
                                        'nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                        {'name': 'Phá Hủy Trừng Phạt',
                         'tags': ['Chủ Động', 'AoE', 'Phá Hủy Vật Cản'],
                         'description': 'Chọn 1 ô địa hình trong bán kính 7 ô, gây ST Vật Lý AoE bằng '
                                        '<color=#f26c1c>90%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 3×3 ô '
                                        'quanh ô chỉ định và phá hủy toàn bộ Vật Cản trong khu vực. Áp dụng '
                                        '<color=#3487e0>Ấn Kẻ Trừng Phạt</color> lên tất cả mục tiêu trúng đòn trong '
                                        '<color=#f26c1c>2 hiệp</color>.'},
                        {'name': 'Phán Quyết Pháo Điện Từ',
                         'tags': ['Tuyệt Kỹ', 'Chuẩn Xác', 'Cường Hóa'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây '
                                        'ST Vật Lý bằng <color=#f26c1c>180%</color> Tấn Công bỏ qua '
                                        '<color=#f26c1c>30%</color> Phòng Thủ của mục tiêu. Áp dụng '
                                        '<color=#3487e0>Khiên Trừng Phạt</color> và <color=#3487e0>Tội Và Phạt</color> '
                                        'lên toàn đội trong <color=#f26c1c>2 hiệp</color>.'},
                        {'name': 'Khế Ước Đồng Tâm',
                         'tags': ['Bị Động', 'Hỗ Trợ', 'Cường Hóa'],
                         'description': 'Khi đơn vị có Đồng Bộ tấn công mục tiêu mang Ấn Kẻ Trừng Phạt, Asteria thực '
                                        'hiện <color=#3487e0>Hành Động Chi Viện</color>, gây ST Vật Lý bằng '
                                        '<color=#f26c1c>60%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn '
                                        'Định. Kích hoạt tối đa <color=#f26c1c>3 lần</color> mỗi hiệp.\n'
                                        '\n'
                                        'Đồng minh mang Đồng Bộ được chia sẻ <color=#f26c1c>20%</color> Tấn Công và '
                                        'Phòng Thủ của Asteria.'}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Trận Hình Đột Kích',
                                'effect': 'Lượng chia sẻ Tấn Công và Phòng Thủ tăng lên 30%. Nhận thêm 1 điểm Chỉ Số '
                                          'Nhiên Liệu.'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Phá Hủy Trừng Phạt',
                                'effect': 'Phạm vi hiệu lực mở rộng lên 5×5 ô. Sát thương gây ra tăng thêm 20%.'},
                               {'tier': 3,
                                'level': 2,
                                'skill': 'Phán Quyết Pháo Điện Từ',
                                'effect': 'Lượng Phòng Thủ bỏ qua tăng lên 50%. Khiên Trừng Phạt hấp thu thêm 20% sát '
                                          'thương.'},
                               {'tier': 4,
                                'level': 2,
                                'skill': 'Khế Ước Đồng Tâm',
                                'effect': 'Hành Động Chi Viện có thể kích hoạt thêm 2 lần mỗi hiệp. Sát thương chi '
                                          'viện tăng 30%.'},
                               {'tier': 5,
                                'level': 3,
                                'skill': 'Phán Quyết Pháo Điện Từ',
                                'effect': 'Thời gian hồi chiêu giảm 1 hiệp. Áp dụng thêm <color=#3487e0>Xá Tội</color> '
                                          'cho toàn đội trong 2 hiệp.'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Khế Ước Đồng Tâm',
                                'effect': 'Đơn vị có Đồng Bộ nhận thêm hiệu ứng: Khi bị tấn công, Asteria kích hoạt '
                                          '<color=#3487e0>Công Kích Nghịch Đảo</color> phản đòn kẻ tấn công.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Người Bảo Vệ Vô Hình',
                       'effect': 'Tấn Công tăng <color=#f26c1c>10%</color>. Khi mang trạng thái Buff, Phòng Thủ tăng '
                                 'thêm <color=#f26c1c>15%</color>.'},
                      {'name': 'Khóa Cố Định 2 - Kẻ Trừng Phạt',
                       'effect': 'Khi áp dụng Đồng Bộ, làm mới thời lượng của tất cả hiệu ứng Ấn Kẻ Trừng Phạt trên '
                                 'sân.'},
                      {'name': 'Khóa Cố Định 3 - Lãnh Địa Khổng Lồ',
                       'effect': 'Trước khi đồng minh tấn công mục tiêu có Ấn Kẻ Trừng Phạt, áp dụng '
                                 '<color=#3487e0>Phòng Thủ Giảm III</color> trong <color=#f26c1c>1 hiệp</color>.'},
                      {'name': 'Khóa Cố Định 4 - Lời Hứa Tái Ngộ',
                       'effect': 'Khi đơn vị mang Ấn Kẻ Trừng Phạt tử trận, áp dụng Ấn Kẻ Trừng Phạt lên kẻ địch gần '
                                 'nhất.'},
                      {'name': 'Khóa Cố Định 5 - Hướng Đến Kết Quả',
                       'effect': 'Đồng minh có Đồng Bộ nhận hiệu ứng giảm <color=#f26c1c>15%</color> sát thương phải '
                                 'gánh chịu.'},
                      {'name': 'Khóa Cố Định 6 - Con Đường Truy Cầu',
                       'effect': 'Chọn 1 mục tiêu địch gần nhất, gây ST Vật Lý bằng <color=#f26c1c>50%</color> Tấn '
                                 'Công và kéo mục tiêu <color=#f26c1c>1 ô</color>.'},
                      {'name': 'Khóa Tương Thích - Khế Ước Lặng Lẽ', 'effect': 'Tấn Công +3%, TL Bạo Kích +3%, HP +3%'},
                      {'name': 'Khóa Chung - Hướng Về Bầu Trời',
                       'effect': 'Trước khi đồng minh tấn công, nếu mục tiêu sở hữu Debuff, tăng sát thương gây ra '
                                 'thêm <color=#f26c1c>7%</color>.'}]},
 'soppo': {'name': 'Soppo',
           'en_name': 'Soppo',
           'class': 'Vệ Binh',
           'phase': 'Băng Kết',
           'rarity': 'Tinh Nhuệ',
           'weapon_type': 'Súng Trường Tấn Công',
           'ammo_type': 'Đạn Vừa',
           'signature_weapon': 'Tiếng Gầm Xé Trời',
           'weakness': 'Ăn Mòn',
           'server': 'cn',
           'skills': [{'name': 'Truy Lùng Con Mồi',
                       'tags': ['Đánh Thường', 'Chuẩn Xác'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô</color>, gây ST Băng Kết '
                                      'bằng <color=#f26c1c>80%</color> Tấn Công. Soppo nhận <color=#f26c1c>1 '
                                      'điểm</color> Chỉ Số Nhiên Liệu và <color=#f26c1c>2 tầng</color> '
                                      '<color=#3487e0>Dấu Ấn Thợ Săn</color>. Nếu Soppo đang ở <color=#3487e0>Dạng Dã '
                                      'Thú</color>, đòn đánh này sẽ chuyển sang gây ST Thiêu Đốt.'},
                      {'name': 'Cắn Xé Hung Bạo',
                       'tags': ['Chủ Động', 'Phạm Vi', 'Ô Địa Hình'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô</color>, gây ST Băng Kết '
                                      'phạm vi bằng <color=#f26c1c>80%</color> Tấn Công lên mục tiêu và tất cả mục '
                                      'tiêu địch trong bán kính <color=#f26c1c>3 ô</color> xung quanh, đồng thời tạo '
                                      'các ô địa hình <color=#3487e0>Băng Giá</color> duy trì <color=#f26c1c>2 '
                                      'hiệp</color>. Sau khi dùng kỹ năng, lập tức dùng đòn đánh thường Truy Lùng Con '
                                      'Mồi lên mục tiêu địch gần nhất <color=#f26c1c>trong phạm vi 8 ô</color> và nhận '
                                      '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.\n'
                                      'Nếu đang ở <color=#3487e0>Dạng Dã Thú</color>, chuyển sang gây ST Thiêu Đốt '
                                      'phạm vi, tạo các ô địa hình <color=#3487e0>Thiêu Rụi</color> và không còn nhận '
                                      '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                      {'name': 'Tiếng Hú Nửa Đêm',
                       'tags': ['Chủ Động', 'Chuẩn Xác'],
                       'description': 'Chọn 1 ô trống bất kỳ mang thuộc tính Băng Kết hoặc Thiêu Đốt trên toàn bộ '
                                      'chiến trường, di chuyển đến ô đó và áp dụng <color=#3487e0>Dấu Vết Tàn '
                                      'Sát</color> cho tất cả Búp Bê đồng minh trong bán kính <color=#f26c1c>8 '
                                      'ô</color> xung quanh bản thân (không bao gồm bản thân) duy trì <color=#f26c1c>3 '
                                      'hiệp</color>. Sau khi dùng kỹ năng, chuyển sang <color=#3487e0>Dạng Dã '
                                      'Thú</color>.\n'
                                      '\n'
                                      'Nếu đang ở <color=#3487e0>Dạng Dã Thú</color>, chuyển sang gây ST Thiêu Đốt '
                                      'phạm vi bằng <color=#f26c1c>120%</color> Tấn Công lên tất cả mục tiêu địch '
                                      'trong bán kính <color=#f26c1c>4 ô</color>. Sát thương này được chia đều cho mọi '
                                      'mục tiêu trong phạm vi. Sau khi dùng kỹ năng, Soppo dùng đòn đánh thường Truy '
                                      'Lùng Con Mồi lên mục tiêu địch gần nhất <color=#f26c1c>trong phạm vi 8 '
                                      'ô</color> và nhận <color=#3487e0>Tăng Hành Động</color>.'},
                      {'name': 'Vồ Mồi Chí Mạng',
                       'tags': ['Tuyệt Kỹ', 'Phạm Vi', 'Chặn Đánh'],
                       'description': 'Chọn tất cả mục tiêu địch trong bán kính <color=#f26c1c>6 ô</color>, tiêu hao '
                                      'toàn bộ số tầng <color=#3487e0>Dấu Ấn Thợ Săn</color> và gây ST Băng Kết phạm '
                                      'vi bằng số tầng Dấu Ấn Thợ Săn × <color=#f26c1c>30%</color> Tấn Công. Nếu đòn '
                                      'đánh này trúng mục tiêu địch đang đứng trên ô địa hình Dị Vị, gây thêm '
                                      '<color=#f26c1c>1 lần</color> ST Băng Kết bằng <color=#f26c1c>50%</color> Tấn '
                                      'Công lên mục tiêu đó. Sau khi dùng kỹ năng, chuyển sang <color=#3487e0>Dạng Thợ '
                                      'Săn</color>.\n'
                                      '\n'
                                      'Bị động: Trước khi một đơn vị địch <color=#f26c1c>trong phạm vi 8 ô</color> '
                                      'thực hiện tấn công chủ động, kích hoạt <color=#3487e0>Chặn Đánh</color> lên mục '
                                      'tiêu, gây ST Băng Kết bằng <color=#f26c1c>30%</color> Tấn Công và '
                                      '<color=#f26c1c>4 điểm</color> ST Ổn Định. Chỉ có thể kích hoạt tối đa '
                                      '<color=#f26c1c>1 lần</color> mỗi hiệp.'},
                      {'name': 'Hội Chứng Chó Điên',
                       'tags': ['Bị Động'],
                       'description': 'Khi bắt đầu trận chiến, chuyển sang <color=#3487e0>Dạng Thợ Săn</color>; tiêu '
                                      'hao <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu của bản thân và nhận '
                                      '<color=#3487e0>Lá Chắn Hàn Sương</color> duy trì <color=#f26c1c>3 hiệp</color>. '
                                      'Lá Chắn Hàn Sương hấp thụ lượng sát thương bằng <color=#f26c1c>65%</color> Tấn '
                                      'Công ban đầu, tối đa không quá <color=#f26c1c>60%</color> HP tối đa.\n'
                                      '\n'
                                      'Khi bắt đầu trận chiến, nếu đội hình có từ <color=#f26c1c>3</color> Búp Bê đồng '
                                      'minh hệ Thiêu Đốt trở lên (không bao gồm bản thân), thì khi ở Dạng Thợ Săn, sát '
                                      'thương từ đòn đánh thường Truy Lùng Con Mồi và kỹ năng chủ động Cắn Xé Hung Bạo '
                                      'gây ra cho kẻ địch đang chịu Debuff loại Thiêu Đốt tăng '
                                      '<color=#f26c1c>100%</color>; nếu có từ 3 Búp Bê đồng minh hệ Băng Kết trở lên '
                                      '(không bao gồm bản thân), thì khi ở Dạng Dã Thú, sát thương gây ra từ các kỹ '
                                      'năng trên cùng kỹ năng chủ động Tiếng Hú Nửa Đêm lên kẻ địch đang chịu Debuff '
                                      'loại Băng Kết tăng <color=#f26c1c>100%</color>.\n'
                                      'Nếu không thỏa mãn điều kiện nào ở trên, nhận <color=#f26c1c>2 tầng</color> '
                                      '<color=#3487e0>Dấu Ấn Thợ Săn Vĩnh Viễn</color>.\n'
                                      '\n'
                                      'Sau khi sử dụng kỹ năng chủ động, nhận <color=#f26c1c>1 tầng</color> '
                                      '<color=#3487e0>Nhân Tố Cuồng Bạo</color>, tối đa <color=#f26c1c>10 '
                                      'tầng</color>. Khi đạt <color=#f26c1c>4 tầng</color> Nhân Tố Cuồng Bạo, nhận '
                                      '<color=#3487e0>Nhân Tố Cuồng Bạo I</color>; khi đạt <color=#f26c1c>6 '
                                      'tầng</color> Nhân Tố Cuồng Bạo, nhận <color=#3487e0>Nhân Tố Cuồng Bạo '
                                      'II</color>; khi đạt từ <color=#f26c1c>8 tầng</color> Nhân Tố Cuồng Bạo trở lên, '
                                      'nhận <color=#3487e0>Nhân Tố Cuồng Bạo III</color>.'}],
           'fortification': [{'tier': 1,
                              'level': 2,
                              'skill': 'Cắn Xé Hung Bạo',
                              'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>130%</color>.\n'
                                        'Nếu đang ở <color=#3487e0>Dạng Thợ Săn</color>, nhận <color=#f26c1c>2 '
                                        'tầng</color> <color=#3487e0>Dấu Ấn Thợ Săn</color> sau khi tấn công, và nhận '
                                        '<color=#3487e0>Tăng Hành Động</color> thay vì <color=#3487e0>Chỉ Lệnh Bổ '
                                        'Sung</color>.'},
                             {'tier': 2,
                              'level': 2,
                              'skill': 'Tiếng Hú Nửa Đêm',
                              'effect': 'Sau khi di chuyển đến ô chỉ định, nếu ô đó là ô loại <color=#3487e0>Băng '
                                        'Giá</color> hoặc <color=#3487e0>Thiêu Đốt</color>, gây ST Băng Kết hoặc ST '
                                        'Thiêu Đốt bằng <color=#f26c1c>80%</color> Tấn Công lên <color=#f26c1c>3 mục '
                                        'tiêu</color> địch gần nhất <color=#f26c1c>trong phạm vi 8 ô</color>.\n'
                                        'Nếu ô đó là ô Tro Tàn (Băng-Nhiệt), sẽ gây đồng thời <color=#f26c1c>1 '
                                        'lần</color> ST Băng Kết và <color=#f26c1c>1 lần</color> ST Thiêu Đốt, mỗi lần '
                                        'bằng <color=#f26c1c>80%</color> Tấn Công lên 3 mục tiêu địch gần nhất trong '
                                        'phạm vi 8 ô.\n'
                                        'Nếu đang ở <color=#3487e0>Dạng Dã Thú</color>, nhận <color=#f26c1c>1 '
                                        'tầng</color> <color=#3487e0>Dấu Ấn Thợ Săn</color> sau khi dùng kỹ năng.'},
                             {'tier': 3,
                              'level': 2,
                              'skill': 'Tiếng Hú Nửa Đêm',
                              'effect': 'Hiệu ứng của <color=#3487e0>Dấu Vết Tàn Sát</color> được cường hóa: phạm vi '
                                        'tạo ô <color=#3487e0>Băng Giá</color> tăng thêm <color=#f26c1c>2 ô</color>; '
                                        'trước khi chủ động tấn công, Soppo nhận <color=#f26c1c>1 tầng</color> '
                                        '<color=#3487e0>Nhân Tố Cuồng Bạo</color>.\n'
                                        'Nếu đang ở <color=#3487e0>Dạng Dã Thú</color>, hệ số sát thương tăng lên '
                                        '<color=#f26c1c>150%</color>. Nếu mục tiêu địch đang đứng trên ô địa hình Cấp '
                                        '1, sát thương tăng thêm <color=#f26c1c>10%</color>; mỗi cấp ô địa hình tăng '
                                        'thêm, sát thương tăng thêm <color=#f26c1c>10%</color>.'},
                             {'tier': 4,
                              'level': 2,
                              'skill': 'Hội Chứng Chó Điên',
                              'effect': 'Lượng sát thương tăng theo điều kiện đội hình lên mục tiêu địch tăng lên '
                                        '<color=#f26c1c>150%</color> và không còn yêu cầu mục tiêu phải chịu bất kỳ '
                                        'Debuff nào. Số tầng <color=#3487e0>Dấu Ấn Thợ Săn Vĩnh Viễn</color> nhận được '
                                        'tăng thêm <color=#f26c1c>2 tầng</color>.'},
                             {'tier': 5,
                              'level': 2,
                              'skill': 'Vồ Mồi Chí Mạng',
                              'effect': 'Hệ số sát thương tăng lên số tầng Dấu Ấn Thợ Săn × <color=#f26c1c>50%</color> '
                                        'Tấn Công. Khi sử dụng kỹ năng này, tiêu hao toàn bộ Chỉ Số Nhiên Liệu; với '
                                        'mỗi <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu tiêu hao thêm, hệ số cơ '
                                        'bản tăng thêm <color=#f26c1c>5%</color>. Sau khi dùng kỹ năng, hồi phục '
                                        '<color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.\n'
                                        'Sau khi kích hoạt <color=#3487e0>Chặn Đánh</color>, nhận <color=#f26c1c>2 '
                                        'tầng</color> <color=#3487e0>Dấu Ấn Thợ Săn</color>. Hệ số sát thương của Chặn '
                                        'Đánh tăng lên <color=#f26c1c>60%</color>.'},
                             {'tier': 6,
                              'level': 3,
                              'skill': 'Hội Chứng Chó Điên',
                              'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 tầng</color> '
                                        '<color=#3487e0>Nhân Tố Cuồng Bạo</color>.\n'
                                        'Số tầng tối đa của Nhân Tố Cuồng Bạo tăng lên <color=#f26c1c>20 tầng</color>, '
                                        'và sau khi chủ động tấn công, số tầng Nhân Tố Cuồng Bạo nhận được tăng thêm '
                                        '<color=#f26c1c>1 tầng</color>.\n'
                                        'Ngoài ra, khi Nhân Tố Cuồng Bạo đạt 20 tầng, các hiệu ứng được cường hóa:\n'
                                        '<color=#3487e0>Nhân Tố Cuồng Bạo I</color> — khi chủ động tấn công mục tiêu '
                                        'địch đang đứng trên ô địa hình Dị Vị, bỏ qua Phòng Thủ tăng lên '
                                        '<color=#f26c1c>20%</color>;\n'
                                        '<color=#3487e0>Nhân Tố Cuồng Bạo II</color> — lượng tăng ST Băng Kết và ST '
                                        'Thiêu Đốt nâng lên <color=#f26c1c>10%</color>;\n'
                                        '<color=#3487e0>Nhân Tố Cuồng Bạo III</color> — khi tấn công mục tiêu địch '
                                        'đang đứng trên ô địa hình Dị Vị, lượng sát thương tăng lên '
                                        '<color=#f26c1c>30%</color>.'}],
           'keys': [{'name': 'Khóa Cố Định 1 - Lãnh Địa Của Ta',
                     'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Nhân Tố '
                               'Cuồng Bạo</color>.'},
                    {'name': 'Khóa Cố Định 2 - Muốn Thêm Miếng Nữa Không?',
                     'effect': 'Sau khi tấn công mục tiêu địch đang đứng trên ô địa hình Dị Vị, giải trừ '
                               '<color=#f26c1c>1</color> Buff của mục tiêu.'},
                    {'name': 'Khóa Cố Định 3 - Địa Ngục Băng Giá',
                     'effect': 'Khi bắt đầu hiệp, tạo các ô địa hình <color=#3487e0>Băng Giá</color> trong bán kính '
                               '<color=#f26c1c>4 ô</color> xung quanh bản thân duy trì <color=#f26c1c>2 hiệp</color>.'},
                    {'name': 'Khóa Cố Định 4 - Khôi Phục Lãnh Thổ',
                     'effect': 'Khi chịu sát thương lúc đang đứng trên ô địa hình Dị Vị, sát thương phải chịu giảm '
                               '<color=#f26c1c>10%</color> và ST Ổn Định phải chịu giảm <color=#f26c1c>1 '
                               'điểm</color>.'},
                    {'name': 'Khóa Cố Định 5 - Cơn Say Sát Nhân',
                     'effect': 'Khi Soppo sở hữu Khiên, ST Thiêu Đốt và ST Băng Kết gây ra tăng '
                               '<color=#f26c1c>10%</color>.'},
                    {'name': 'Khóa Cố Định 6 - Sức Mạnh Bầy Đàn',
                     'effect': 'Sau khi một đơn vị đồng minh (ngoại trừ Soppo) thực hiện <color=#3487e0>Đòn Đánh Ngoài '
                               'Lượt</color>, nếu bản thân chưa sở hữu <color=#3487e0>Thế Công Rực Lửa I</color> hoặc '
                               '<color=#3487e0>Xung Kích Băng Kết</color>, nhận hiệu ứng tương ứng duy trì '
                               '<color=#f26c1c>2 hiệp</color>.'},
                    {'name': 'Khóa Tương Thích - Giai Điệu Vui Vẻ', 'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                    {'name': 'Khóa Chung - Tiếng Gọi Hoang Dã',
                     'effect': 'TL Bạo Kích +5.0% / Khi tấn công mục tiêu địch đang đứng trên ô địa hình loại '
                               '<color=#3487e0>Băng Giá</color> hoặc <color=#3487e0>Thiêu Đốt</color>, sát thương Dị '
                               'Vị gây ra tăng <color=#f26c1c>10%</color>.'}]},
 'welrod': {'name': 'Welrod',
            'en_name': 'Welrod',
            'class': 'Hộ Vệ',
            'phase': 'Ăn Mòn',
            'rarity': 'Tinh Nhuệ',
            'weapon_type': 'Súng Lục',
            'ammo_type': 'Đạn Nhẹ',
            'signature_weapon': 'Bóng Ma London',
            'weakness': 'Hóa Lỏng',
            'server': 'cn',
            'skills': [{'name': 'Hạ Gục Thầm Lặng',
                        'tags': ['Đánh Thường', 'Chuẩn Xác'],
                        'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                       'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                       {'name': 'Phối Hợp Điều Tra',
                        'tags': ['Chủ Động', 'AoE', 'Cường Hóa', 'Phòng Ngự'],
                        'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                       'ST Ăn Mòn bằng <color=#f26c1c>100%</color> Tấn Công và nhận <color=#3487e0>Ám '
                                       'Ảnh Suy Luận</color> trong <color=#f26c1c>3 hiệp</color>. Bản thân nhận '
                                       '<color=#f26c1c>2 tầng</color> <color=#3487e0>Yểm Hộ</color> và '
                                       '<color=#f26c1c>4 điểm</color> Chỉ Số Nhiên Liệu.'},
                       {'name': 'Luận Tội Và Trừng Phạt',
                        'tags': ['Chủ Động', 'Chuẩn Xác', 'Dịch Chuyển'],
                        'description': 'Chọn 1 ô địa hình trong bán kính 6 ô, gây ST Ăn Mòn AoE bằng '
                                       '<color=#f26c1c>120%</color> Tấn Công lên toàn bộ kẻ địch trong bán kính 5 ô và '
                                       'tạo ô địa hình <color=#3487e0>Độc Chướng</color> trong 2 hiệp. Cứ mỗi 1% HP '
                                       'tối đa tăng thêm so với HP ban đầu, hệ số sát thương tăng thêm 1% (tối đa '
                                       '60%). Cứ mỗi kẻ địch trúng đòn, lượng sát thương tích lũy của '
                                       '<color=#3487e0>Miễn Trừ Trinh Thám</color> giảm 10% (với Boss giảm 30%, tối đa '
                                       'giảm 50%).'},
                       {'name': 'Giờ Khắc Định Tội',
                        'tags': ['Tuyệt Kỹ', 'Suy Yếu', 'Dịch Chuyển', 'Trị Liệu'],
                        'description': 'Chọn 1 hướng, gây ST Ăn Mòn AoE bằng <color=#f26c1c>120%</color> Tấn Công lên '
                                       'tất cả kẻ địch trong khu vực 3×9 ô phía trước, kéo chúng <color=#f26c1c>3 '
                                       'ô</color> về phía bản thân và áp dụng <color=#3487e0>Phản Phệ Tội Ác</color> '
                                       'trong <color=#f26c1c>1 hiệp</color> cùng <color=#3487e0>Nghi Phạm</color> '
                                       'trong <color=#f26c1c>2 hiệp</color>. Welrod hồi phục lượng HP bằng '
                                       '<color=#f26c1c>20%</color> lượng sát thương tích lũy của Miễn Trừ Trinh Thám '
                                       'và nhận <color=#3487e0>V3 Viện Hộ</color> trong <color=#f26c1c>1 hiệp</color>. '
                                       'Sau khi dùng, Welrod có thể dùng đánh thường hoặc kỹ năng chủ động.'},
                       {'name': 'Thám Tử Hiện Trường',
                        'tags': ['Bị Động', 'Khống Chế'],
                        'description': 'Welrod không nhận sự bảo vệ từ Vật Cản và tỷ lệ bạo kích giảm 100%, nhưng HP '
                                       'tối đa tăng <color=#f26c1c>50%</color> và sát thương nhận vào giảm '
                                       '<color=#f26c1c>20%</color>.\n'
                                       'Nhận <color=#3487e0>Miễn Trừ Trinh Thám</color> khi bắt đầu trận chiến. Khi '
                                       'kết thúc hành động của Welrod, gây 1 lần ST Ăn Mòn AoE bằng '
                                       '<color=#f26c1c>30%</color> lượng sát thương tích lũy của Miễn Trừ Trinh Thám '
                                       'lên toàn bộ kẻ địch trong bán kính 6 ô và áp dụng Nghi Phạm trong 2 hiệp. Đồng '
                                       'thời áp dụng <color=#3487e0>Khiêu Khích</color> lên toàn bộ kẻ địch trong bán '
                                       'kính 6 ô trong <color=#f26c1c>1 hiệp</color>.'}],
            'fortification': [{'tier': 1,
                               'level': 2,
                               'skill': 'Phối Hợp Điều Tra',
                               'effect': 'Hiệu quả tăng trị liệu của Ám Ảnh Suy Luận tăng lên 30%, mức giảm sát thương '
                                         'tăng lên 30%, và bổ sung hiệu ứng: ST Ăn Mòn gây ra tăng 30%.\n'
                                         'Sau khi dùng kỹ năng, hồi phục HP bằng 100% Tấn Công cho đồng minh có lượng '
                                         'HP thấp nhất trong bán kính 5 ô và áp dụng 2 tầng Yểm Hộ.'},
                              {'tier': 2,
                               'level': 2,
                               'skill': 'Thám Tử Hiện Trường',
                               'effect': 'Khi kết thúc hành động của búp bê đồng minh khác, Welrod cũng kích hoạt 1 '
                                         'lần ST Ăn Mòn AoE bằng 30% lượng sát thương tích lũy của Miễn Trừ Trinh '
                                         'Thám.\n'
                                         'Cường hóa Miễn Trừ Trinh Thám: Giới hạn hấp thu tăng lên tổng của 250% HP '
                                         'tối đa và 150% Tấn Công lúc bắt đầu trận chiến.'},
                              {'tier': 3,
                               'level': 2,
                               'skill': 'Giờ Khắc Định Tội',
                               'effect': 'Hệ số sát thương tăng lên 120%. Cường hóa Phản Phệ Tội Ác: Sát thương phải '
                                         'chịu tăng lên tổng của 50% sát thương tích lũy và 30% HP tối đa của Welrod. '
                                         'Hồi chiêu của V3 Viện Hộ giảm 1 hiệp.'},
                              {'tier': 4,
                               'level': 2,
                               'skill': 'Luận Tội Và Trừng Phạt',
                               'effect': 'Hệ số sát thương tăng lên 120%. Cứ mỗi 1% HP tối đa tăng thêm, hệ số sát '
                                         'thương tăng 1.5% (tối đa 150%).'},
                              {'tier': 5,
                               'level': 3,
                               'skill': 'Giờ Khắc Định Tội',
                               'effect': 'Với mỗi lần chịu sát thương, sát thương gây ra tăng 40% (tối đa 80%). Cứ mỗi '
                                         'kẻ địch trúng đòn, sát thương tăng 20% (tối đa 100%). Cường hóa Nghi Phạm: '
                                         'Sát thương cố định cuối hiệp tăng lên 16% HP tối đa (với Boss tăng lên 360% '
                                         'Tấn Công của Welrod). Hồi chiêu giảm 1 hiệp.'},
                              {'tier': 6,
                               'level': 3,
                               'skill': 'Thám Tử Hiện Trường',
                               'effect': 'Khi bắt đầu trận chiến, mức tăng HP tối đa được nâng lên 150%. Với mỗi lần '
                                         'chịu sát thương (bao gồm cả sát thương từ Miễn Trừ Trinh Thám), Tấn Công của '
                                         'bản thân tăng 1% (tối đa tăng 50%).'}],
            'keys': [{'name': 'Khóa Cố Định 1 - Khí Chất Đại Thám Tử',
                      'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                     {'name': 'Khóa Cố Định 2 - Thu Thập Chứng Cứ Sơ Bộ',
                      'effect': 'Trước khi tấn công chủ động, giải trừ <color=#f26c1c>1</color> Buff của mục tiêu.'},
                     {'name': 'Khóa Cố Định 3 - Suy Luận Đích Thực',
                      'effect': 'Giới hạn hấp thu của Miễn Trừ Trinh Thám tăng lên <color=#f26c1c>90%</color>.'},
                     {'name': 'Khóa Cố Định 4 - Săn Chó Địa Ngục',
                      'effect': 'Khi tấn công đơn vị Boss, ST Ăn Mòn gây ra tăng thêm <color=#f26c1c>20%</color>.'},
                     {'name': 'Khóa Cố Định 5 - Vấn Đề Cuối Cùng',
                      'effect': 'Miễn nhiễm với Choáng và Chạy Trốn. Hiệu quả trị liệu nhận được tăng thêm '
                                '<color=#f26c1c>30%</color>.'},
                     {'name': 'Khóa Cố Định 6 - Cặp Đôi Thám Tử',
                      'effect': 'Sát thương cố định từ Miễn Trừ Trinh Thám mà Welrod phải chịu khi kết thúc hành động '
                                'đổi thành 2 lần, và lượng sát thương cố định nhận vào giảm '
                                '<color=#f26c1c>15%</color>.'},
                     {'name': 'Khóa Tương Thích - Lời Thề Truy Vết', 'effect': 'Tấn Công +3%, HP +3%, Phòng Thủ +3%'},
                     {'name': 'Khóa Chung - Quy Tắc Của Van Dine',
                      'effect': 'HP +5.0% / Khi tấn công, nếu tỷ lệ HP của bản thân bằng hoặc cao hơn mục tiêu, sát '
                                'thương thuộc tính tăng <color=#f26c1c>10%</color>.'}]}}
