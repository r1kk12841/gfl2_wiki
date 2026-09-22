"""
Auto-synced batch data.
"""

GROUP_2_DATA = {'mityl': {'name': 'Mityl',
           'en_name': 'Mityl',
           'class': 'Chiến Binh',
           'phase': 'Hóa Lỏng',
           'rarity': 'Tinh Nhuệ',
           'weapon_type': 'Súng Ngắn',
           'ammo_type': 'Đạn Nhẹ',
           'signature_weapon': 'Chinchilla Nova',
           'weakness': 'Băng Kết',
           'server': 'global',
           'skills': [{'name': 'Bắn Đột Kích',
                       'tags': ['Đánh Thường', 'Chỉ Định'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                      'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                      {'name': 'Bóng Chuột Xám',
                       'tags': ['Chủ Động', 'Ô Địa Hình', 'Triệu Hồi', 'Dịch Chuyển'],
                       'description': 'Chọn 1 mục tiêu địch trong phạm vi 6 ô (không bao gồm vật triệu hồi), sau đó '
                                      'chọn 1 ô trống trong phạm vi 3 ô quanh mục tiêu đó, triệu hồi 1 Ảo Ảnh Mô Phỏng '
                                      'của mục tiêu trên ô đó, và tạo ra các ô địa hình <color=#3487e0>Dòng '
                                      'Ngầm</color> trong phạm vi 5 ô quanh Ảo Ảnh trong <color=#f26c1c>2 '
                                      'hiệp</color>. Tối đa tồn tại đồng thời 2 Ảo Ảnh. Nếu mục tiêu là Doll, Thủ Lĩnh '
                                      'hoặc đơn vị Cỡ Lớn, sẽ triệu hồi 1 Ảo Ảnh Cá Nhân thay thế.\n'
                                      '\n'
                                      'Cũng có thể chọn 1 Ảo Ảnh trong phạm vi 6 ô và dịch chuyển nó đến 1 ô trống '
                                      'trong phạm vi 5 ô.\n'
                                      '\n'
                                      'Sau khi dùng kỹ năng, nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Mỗi hiệp '
                                      'kích hoạt tối đa 1 lần.'},
                      {'name': 'Lướt Trên Không',
                       'tags': ['Chủ Động', 'Chỉ Định', 'Dịch Chuyển'],
                       'description': 'Chọn 1 ô trong phạm vi chữ thập từ 3 đến 6 ô và hạ xuống ô đó, gây '
                                      '<color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>130%</color> Tấn Công '
                                      'lên mục tiêu địch gần nhất trong phạm vi 6 ô.\n'
                                      '\n'
                                      'Nếu cả trước khi dùng kỹ năng và khi gây sát thương, Mityl đều ở trên ô địa '
                                      'hình loại Hóa Lỏng, cô có thể dùng thêm 1 lần KN chủ động Lướt Trên Không, và '
                                      'sát thương gây ra tăng thêm <color=#f26c1c>30%</color>. Mỗi hiệp kích hoạt 1 '
                                      'lần.'},
                      {'name': 'Hư Không Thích Ứng',
                       'tags': ['Tuyệt Kỹ', 'Ô Địa Hình', 'Cường Hóa'],
                       'description': 'Nhận <color=#3487e0>Tràn Bão Hòa</color> trong <color=#f26c1c>2 hiệp</color>. '
                                      'Tạo ô địa hình <color=#3487e0>Dòng Ngầm</color> trong phạm vi 5 ô quanh bản '
                                      'thân trong <color=#f26c1c>2 hiệp</color>. Sau khi dùng kỹ năng, nhận '
                                      '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                      {'name': 'Kỹ Xảo Điện Ảnh',
                       'tags': ['Bị Động', 'Cường Hóa'],
                       'description': 'Khi kết thúc lượt của phe ta, toàn bộ Ảo Ảnh sẽ thi triển <color=#3487e0>Cộng '
                                      'Hưởng Tương Thích</color> 1 lần. Sau khi Mityl hoặc Ảo Ảnh gây ST Hóa Lỏng, '
                                      'nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Nếu người tấn công hoặc '
                                      'mục tiêu ở trên ô địa hình loại Hóa Lỏng, nhận thêm <color=#f26c1c>1 '
                                      'điểm</color> Chỉ Số Nhiên Liệu. Mỗi hiệp có thể nhận tối đa 6 điểm Chỉ Số Nhiên '
                                      'Liệu.\n'
                                      '\n'
                                      'Khi bắt đầu trận chiến, nhận <color=#3487e0>Tân Tú Mô Phỏng</color>. Cứ mỗi 6 '
                                      'điểm Chỉ Số Nhiên Liệu tích lũy được (bao gồm cả điểm vượt mức), sẽ nâng cấp '
                                      '<color=#3487e0>Danh Hiệu Điện Ảnh</color> lên cấp cao hơn.'}],
           'summons': [{'name': 'Ảo Ảnh Cá Nhân',
                        'type': 'Vật Triệu Hồi Hóa Lỏng',
                        'description': 'Bản sao toàn ảnh chiến thuật được tạo ra từ công nghệ của Mityl. Có khả năng '
                                       'cộng hưởng hỏa lực và tấn công yểm trợ đồng đội.',
                        'stats': {'hp': '100% HP ban đầu của Mityl',
                                  'atk': '100% Tấn Công ban đầu của Mityl',
                                  'def': '100% Phòng Thủ ban đầu của Mityl'},
                        'skills': [{'name': 'Tập Kích Bóng Cung',
                                    'tags': ['Bị Động', 'Chỉ Định'],
                                    'description': 'Chọn 1 mục tiêu địch trong phạm vi 6 ô và gây ST Hóa Lỏng bằng '
                                                   '100% Tấn Công lên mục tiêu đó.'},
                                   {'name': 'Hào Quang Toàn Ảnh',
                                    'tags': ['Bị Động', 'Cường Hóa'],
                                    'description': 'Toàn bộ đồng minh đứng trong phạm vi 2 ô xung quanh Ảo Ảnh Cá Nhân '
                                                   'nhận tăng 15% Tấn Công và 10% Tỷ Lệ Bạo Kích.'}]}],
           'fortification': [{'tier': 1,
                              'level': 2,
                              'skill': 'Kỹ Xảo Điện Ảnh',
                              'effect': 'Sát thương của <color=#3487e0>Cộng Hưởng Tương Thích</color> tăng lên '
                                        '<color=#f26c1c>60%</color> Tấn Công. Khi <color=#3487e0>Danh Hiệu Điện '
                                        'Ảnh</color> được nâng cấp, Hình Chiếu thi triển <color=#3487e0>Cộng Hưởng '
                                        'Tương Thích</color> <color=#f26c1c>1 lần</color>. Chỉ Số Nhiên Liệu cần thiết '
                                        'để nâng cấp Danh Hiệu giảm xuống còn <color=#f26c1c>4 điểm</color>. '
                                        '<color=#3487e0>Cộng Hưởng Tương Thích</color> áp dụng <color=#3487e0>Phòng '
                                        'Thủ Giảm II</color> lên mục tiêu trong <color=#f26c1c>2 hiệp</color>.'},
                             {'tier': 2,
                              'level': 2,
                              'skill': 'Hình Chiếu Sóc Con',
                              'effect': 'Mỗi khi thi triển <color=#3487e0>Cộng Hưởng Tương Thích</color>, Hình Chiếu '
                                        'nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Bất Khả Xâm Phạm</color>. '
                                        'Hệ số sát thương của đòn đánh thường Tấn Công Bóng Vòng của Hình Chiếu Cá '
                                        'Nhân tăng lên <color=#f26c1c>120%</color> Tấn Công.'},
                             {'tier': 3,
                              'level': 2,
                              'skill': 'Hội Tụ Hư Không',
                              'effect': 'Phạm vi của ô địa hình <color=#3487e0>Dòng Ngầm</color> được tạo ra mở rộng '
                                        'thành bán kính <color=#f26c1c>7 ô</color>. Mức tăng Tấn Công từ '
                                        '<color=#3487e0>Tràn Bão Hòa</color> tăng lên <color=#f26c1c>40%</color> và '
                                        'cũng áp dụng cho Hình Chiếu. Nếu <color=#3487e0>Cộng Hưởng Tương '
                                        'Thích</color> kích hoạt tổng cộng từ <color=#f26c1c>4 lần</color> trở lên '
                                        'trong hiệp hiện tại, <color=#3487e0>Tràn Bão Hòa</color> sẽ không bị tiêu hao '
                                        'thời lượng.'},
                             {'tier': 4,
                              'level': 2,
                              'skill': 'Phi Thân Nhào Lộn',
                              'effect': 'Điều kiện để tái sử dụng kỹ năng chủ động được thay đổi: Mityl chỉ cần đứng '
                                        'trên ô địa hình loại Hóa Lỏng trước khi dùng kỹ năng hoặc khi gây sát thương. '
                                        'Sát thương tăng lên <color=#f26c1c>160%</color> Tấn Công. Sát thương gây ra '
                                        'bởi kỹ năng chủ động được tái sử dụng tăng thêm <color=#f26c1c>50%</color>.'},
                             {'tier': 5,
                              'level': 3,
                              'skill': 'Phi Thân Nhào Lộn',
                              'effect': 'Sau khi thi triển kỹ năng, Hình Chiếu Cá Nhân thực hiện <color=#f26c1c>1 '
                                        'lần</color> Hành Động Chi Viện nhắm vào mục tiêu, gây <color=#2caadb>ST Hóa '
                                        'Lỏng</color> bằng <color=#f26c1c>60%</color> Tấn Công và <color=#f26c1c>2 '
                                        'điểm</color> ST Ổn Định. Có thể kích hoạt tối đa 1 lần mỗi hiệp. Sát thương '
                                        'gây ra bởi Hình Chiếu Bắt Chước trong hiệp hiện tại tăng thêm '
                                        '<color=#f26c1c>100%</color>. Hiệu ứng này không thể cộng dồn.'},
                             {'tier': 6,
                              'level': 3,
                              'skill': 'Kỹ Xảo Điện Ảnh',
                              'effect': 'Ngôi Sao Huyền Thoại nhận hiệu ứng mới: Cứ mỗi <color=#f26c1c>4 điểm</color> '
                                        'Chỉ Số Nhiên Liệu nhận được, tất cả Hình Chiếu thi triển <color=#3487e0>Cộng '
                                        'Hưởng Tương Thích</color> <color=#f26c1c>1 lần</color>.\n'
                                        '\n'
                                        'Khi một Hình Chiếu thi triển <color=#3487e0>Cộng Hưởng Tương Thích</color>, '
                                        'nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Khuếch Đại Tương '
                                        'Thích</color>.'}],
           'keys': [{'name': 'Khóa Cố Định 1 - Đạo Cụ Chuyên Nghiệp',
                     'level': 20,
                     'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.',
                     'materials': '3\n\n\n3000'},
                    {'name': 'Khóa Cố Định 2 - Ống Kính Toàn Cảnh',
                     'level': 20,
                     'effect': 'Khi Mityl đứng trên ô địa hình Hóa Lỏng, tầm bắn của kỹ năng tấn công đơn thể tăng '
                               'thêm <color=#f26c1c>1 ô</color>.',
                     'materials': '3\n\n\n3000'},
                    {'name': 'Khóa Cố Định 3 - Góc Quay Nghệ Thuật',
                     'level': 30,
                     'effect': 'Khi Ảo Ảnh thi triển Cộng Hưởng Tương Thích trúng kẻ địch, giảm '
                               '<color=#f26c1c>15%</color> Phòng Thủ của mục tiêu trong 2 hiệp.',
                     'materials': '3\n\n\n8000'},
                    {'name': 'Khóa Cố Định 4 - Kỹ Thuật Đóng Thế',
                     'level': 30,
                     'effect': 'Khi Mityl chịu sát thương đe dọa tính mạng, nếu có Ảo Ảnh trên sân, tiêu hao 1 Ảo Ảnh '
                               'để chặn toàn bộ sát thương đó và hồi phục <color=#f26c1c>30%</color> HP tối đa. Kích '
                               'hoạt 1 lần mỗi trận.',
                     'materials': '3\n\n\n8000'},
                    {'name': 'Khóa Cố Định 5 - Bắt Kịp Xu Hướng',
                     'level': 40,
                     'effect': 'Khi bắt đầu trận chiến, Mityl triệu hồi 1 Ảo Ảnh. Cả Mityl và Ảo Ảnh này đều được coi '
                               'là Doll và vật triệu hồi. Ảo Ảnh này không có kỹ năng và không thể hành động.',
                     'materials': '3\n\n\n12000'},
                    {'name': 'Khóa Cố Định 6 - Thật Hay Giả?',
                     'level': 40,
                     'effect': 'Khi Mityl hoặc Ảo Ảnh gây sát thương, nếu người tấn công ở trên ô Hóa Lỏng, tăng '
                               '<color=#f26c1c>10%</color> ST gây ra. Cứ mỗi cấp độ tăng của ô địa hình Hóa Lỏng đó, '
                               'tăng thêm <color=#f26c1c>5%</color> ST gây ra.',
                     'materials': '3\n\n\n12000'},
                    {'name': 'Khóa Tương Thích - Góc Máy Hoàn Hảo',
                     'level': '-',
                     'effect': 'Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%',
                     'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                    {'name': 'Khóa Chung - Mitty Thông Minh',
                     'level': 40,
                     'effect': 'TL Bạo Kích +5.0% / Khi gây sát thương, nếu bản thân ở trên ô địa hình Hóa Lỏng, sát '
                               'thương gây ra tăng <color=#f26c1c>10%</color>.',
                     'materials': 'None'}]},
 'nemesis-gnosis': {'name': 'Nemesis - Gnosis',
                    'en_name': 'Nemesis - Gnosis',
                    'class': 'Vệ Binh',
                    'phase': 'Ăn Mòn',
                    'rarity': 'Tinh Nhuệ',
                    'weapon_type': 'Súng Bắn Tỉa',
                    'ammo_type': 'Đạn Nặng',
                    'signature_weapon': 'Antithesis',
                    'weakness': 'Băng Kết',
                    'server': 'global',
                    'skills': [{'name': 'Sao Băng Sa Lưới',
                                'tags': ['Đánh Thường', 'Chỉ Định'],
                                'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung '
                                               'quanh</color>, gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn '
                                               'Công.'},
                               {'name': 'Cộng Hưởng Tai Ương',
                                'tags': ['Chủ Động', 'Chỉ Định', 'Suy Yếu'],
                                'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung '
                                               'quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng '
                                               '<color=#f26c1c>100%</color> Tấn Công và áp dụng <color=#3487e0>Dấu Ấn '
                                               'Tận Diệt</color> trong <color=#f26c1c>2 hiệp</color>. Nhận '
                                               '<color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu và <color=#3487e0>Chỉ '
                                               'Lệnh Bổ Sung</color>.'},
                               {'name': 'Khúc Xạ Lăng Kính',
                                'tags': ['Chủ Động', 'Chỉ Định'],
                                'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung '
                                               'quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> bằng '
                                               '<color=#f26c1c>120%</color> Tấn Công.\n'
                                               '\n'
                                               'Nếu sở hữu <color=#3487e0>Lời Tiên Tri Thứ Nhất</color>, hệ số sát '
                                               'thương tăng <color=#f26c1c>20%</color>, nhận 1 lớp <color=#3487e0>Hội '
                                               'Tâm</color> trước khi dùng kỹ năng.\n'
                                               '\n'
                                               'Nếu sở hữu <color=#3487e0>Lời Tiên Tri Thứ Hai</color> và không có '
                                               'đồng minh nào trong phạm vi 4 ô quanh bản thân, sát thương gây ra tăng '
                                               '<color=#f26c1c>20%</color>. Sau khi dùng kỹ năng, hồi phục '
                                               '<color=#f26c1c>15%</color> HP tối đa cho bản thân.'},
                               {'name': 'Nghịch Chuyển Vận Mệnh',
                                'tags': ['Tuyệt Kỹ', 'AoE'],
                                'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung '
                                               'quanh</color>, gây <color=#8679e8>ST Ăn Mòn</color> AoE bằng '
                                               '<color=#f26c1c>140%</color> Tấn Công lên mục tiêu và kẻ địch trong '
                                               'phạm vi 1 ô, đồng thời tiêu hao toàn bộ Chỉ Số Nhiên Liệu. Cứ mỗi 1 '
                                               'điểm Chỉ Số Nhiên Liệu tiêu hao, sát thương tăng thêm '
                                               '<color=#f26c1c>10%</color> và gây <color=#f26c1c>1 điểm</color> ST Ổn '
                                               'Định.\n'
                                               '\n'
                                               'Nếu sở hữu <color=#3487e0>Lời Tiên Tri Thứ Sáu</color>, cứ mỗi điểm '
                                               'Chỉ Số Nhiên Liệu tiêu hao sẽ tăng thêm <color=#f26c1c>10%</color> sát '
                                               'thương, và toàn bộ kẻ địch trong phạm vi 3 ô quanh mục tiêu chịu thêm '
                                               '<color=#8679e8>ST Ăn Mòn</color> AoE bằng <color=#f26c1c>100%</color> '
                                               'Tấn Công và 1 điểm ST Ổn Định.'},
                               {'name': 'Thì Thầm Bờ Hy Vọng',
                                'tags': ['Bị Động'],
                                'description': 'Sát thương gây ra lên kẻ địch Paradeus tăng '
                                               '<color=#f26c1c>20%</color>.\n'
                                               '\n'
                                               'Khi lần đầu dùng KN chủ động Cộng Hưởng Tai Ương, nếu có đồng minh '
                                               'trong phạm vi 4 ô, nhận <color=#3487e0>Lời Tiên Tri Thứ Nhất</color>; '
                                               'nếu không có đồng minh trong phạm vi 4 ô, nhận <color=#3487e0>Lời Tiên '
                                               'Tri Thứ Hai</color>.\n'
                                               '\n'
                                               'Khi bắt đầu chiến đấu, nếu có kẻ địch thường trên sân, nhận '
                                               '<color=#3487e0>Lời Tiên Tri Thứ Ba</color>; nếu không có kẻ địch '
                                               'thường, nhận <color=#3487e0>Lời Tiên Tri Thứ 4: Phán Quyết</color>.\n'
                                               '\n'
                                               'Nếu có 2 Doll dùng Súng Bắn Tỉa hoặc 2 Doll thuộc tính Ăn Mòn trên '
                                               'sân, Nemesis nhận <color=#3487e0>Lời Tiên Tri Thứ 5: Tinh Quỹ</color>. '
                                               'Nếu có 4 Doll dùng Súng Bắn Tỉa trên sân, toàn bộ Doll dùng Súng Bắn '
                                               'Tỉa nhận <color=#3487e0>Lời Tiên Tri Thứ Sáu</color>.'}],
                    'fortification': [{'tier': 1,
                                       'level': 2,
                                       'skill': 'Cộng Hưởng Tai Ương',
                                       'effect': 'Cường hóa hiệu ứng <color=#3487e0>Dấu Ấn Tận Diệt</color>: Hệ số sát '
                                                 'thương tăng lên <color=#f26c1c>110%</color>, số lần kích hoạt Tấn '
                                                 'Công Chi Viện tăng thêm 1, và hồi phục thêm <color=#f26c1c>1 '
                                                 'điểm</color> Chỉ Số Nhiên Liệu.'},
                                      {'tier': 2,
                                       'level': 2,
                                       'skill': 'Nghịch Chuyển Vận Mệnh',
                                       'effect': 'Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>, và hệ số sát '
                                                 'thương tăng lên <color=#f26c1c>200%</color>. Nếu Nemesis có '
                                                 '<color=#3487e0>Lời Tiên Tri Thứ 5: Tinh Quỹ</color>, sát thương gây '
                                                 'ra tăng <color=#f26c1c>50%</color>.'},
                                      {'tier': 3,
                                       'level': 2,
                                       'skill': 'Thì Thầm Bờ Hy Vọng',
                                       'effect': 'Cường hóa <color=#3487e0>Lời Tiên Tri Thứ Nhất</color>: '
                                                 '<color=#3487e0>Hội Tâm</color> có thể cộng dồn không giới hạn và '
                                                 'không bị xóa khi tiêu hao điểm di chuyển.\n'
                                                 'Cường hóa <color=#3487e0>Lời Tiên Tri Thứ Hai</color>: Hiệu ứng Điềm '
                                                 'Báo được thay thế bằng Nhà Tiên Tri.'},
                                      {'tier': 4,
                                       'level': 2,
                                       'skill': 'Khúc Xạ Lăng Kính',
                                       'effect': 'Nếu Nemesis có <color=#3487e0>Lời Tiên Tri Thứ Nhất</color>, mức '
                                                 'tăng hệ số sát thương nâng từ 20% lên <color=#f26c1c>40%</color>.\n'
                                                 'Nếu Nemesis có <color=#3487e0>Lời Tiên Tri Thứ Hai</color> và không '
                                                 'có đồng minh nào trong phạm vi 4 ô, mức tăng sát thương nâng từ 20% '
                                                 'lên <color=#f26c1c>40%</color>, và lượng HP hồi phục sau kỹ năng '
                                                 'nâng từ 15% lên <color=#f26c1c>30%</color>.'},
                                      {'tier': 5,
                                       'level': 3,
                                       'skill': 'Thì Thầm Bờ Hy Vọng',
                                       'effect': 'Cường hóa <color=#3487e0>Lời Tiên Tri Thứ Ba</color>: Hệ số sát '
                                                 'thương tăng lên <color=#f26c1c>80%</color>, và phạm vi hiệu quả mở '
                                                 'rộng thêm <color=#f26c1c>1 ô</color>.\n'
                                                 'Cường hóa <color=#3487e0>Lời Tiên Tri Thứ 4: Phán Quyết</color>: Mức '
                                                 'tăng hệ số sát thương của Tấn Công Chi Viện nâng lên '
                                                 '<color=#f26c1c>40%</color>. Khi tấn công Tinh Nhuệ hoặc Thủ Lĩnh, tỷ '
                                                 'lệ bỏ qua Phòng Thủ tăng lên <color=#f26c1c>35%</color>, ST Bạo Kích '
                                                 'tăng lên <color=#f26c1c>40%</color>, và sát thương gây ra tăng '
                                                 '<color=#f26c1c>20%</color>.'},
                                      {'tier': 6,
                                       'level': 3,
                                       'skill': 'Thì Thầm Bờ Hy Vọng',
                                       'effect': 'Cường hóa <color=#3487e0>Lời Tiên Tri Thứ 5: Tinh Quỹ</color>: Xóa '
                                                 'bỏ yêu cầu cự ly để bỏ qua Vật Cản khi gây sát thương chuẩn xác. Mức '
                                                 'tăng sát thương cho mỗi 1 ô khoảng cách từ mục tiêu tăng lên '
                                                 '<color=#f26c1c>10%</color>, tối đa tăng <color=#f26c1c>60%</color>.\n'
                                                 'Cường hóa <color=#3487e0>Lời Tiên Tri Thứ Sáu</color>: Đòn Tấn Công '
                                                 'Chi Viện đầu tiên kích hoạt bởi <color=#3487e0>Dấu Ấn Tận '
                                                 'Diệt</color> mỗi hiệp được thay thế bằng KN Tuyệt Kỹ Nghịch Chuyển '
                                                 'Vận Mệnh, và được tính như tiêu hao tối đa Chỉ Số Nhiên Liệu.'}],
                    'keys': [{'name': 'Khóa Cố Định 1 - Điểm Ngắm Tinh Tế',
                              'level': 20,
                              'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.',
                              'materials': '3\n\n\n3000'},
                             {'name': 'Khóa Cố Định 2 - Tiếng Chuông Báo Tử',
                              'level': 20,
                              'effect': 'Khi kẻ địch mang <color=#3487e0>Dấu Ấn Tận Diệt</color> tử trận, hồi phục '
                                        '<color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu cho Nemesis.',
                              'materials': '3\n\n\n3000'},
                             {'name': 'Khóa Cố Định 3 - Đạn Ăn Mòn Xuyên Thấu',
                              'level': 30,
                              'effect': 'Khi gây ST Ăn Mòn lên mục tiêu có Phòng Thủ giảm, sát thương gây ra tăng '
                                        '<color=#f26c1c>15%</color>.',
                              'materials': '3\n\n\n8000'},
                             {'name': 'Khóa Cố Định 4 - Tương Tác Quang Học',
                              'level': 30,
                              'effect': 'Sau khi thi triển Khúc Xạ Lăng Kính, nhận <color=#3487e0>Chỉ Lệnh Bổ '
                                        'Sung</color>. Kích hoạt 1 lần mỗi 2 hiệp.',
                              'materials': '3\n\n\n8000'},
                             {'name': 'Khóa Cố Định 5 - Khải Huyền Hắc Ám',
                              'level': 40,
                              'effect': 'Khi ở trạng thái <color=#3487e0>Hội Tâm</color>, Tỷ Lệ Bạo Kích tăng '
                                        '<color=#f26c1c>15%</color> và ST Bạo Kích tăng <color=#f26c1c>20%</color>.',
                              'materials': '3\n\n\n12000'},
                             {'name': 'Khóa Cố Định 6 - Thiên Hà Vỡ Vụn',
                              'level': 40,
                              'effect': 'Cứ mỗi 1 kẻ địch tử trận trong hiệp, tăng <color=#f26c1c>5%</color> Tấn Công '
                                        'của Nemesis, tối đa cộng dồn 4 lớp.',
                              'materials': '3\n\n\n12000'},
                             {'name': 'Khóa Tương Thích - Ánh Sao Bất Diệt',
                              'level': '-',
                              'effect': 'Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%',
                              'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                             {'name': 'Khóa Chung - Lời Sấm Truyền',
                              'level': 40,
                              'effect': 'Tấn Công +5.0% / Khi gây sát thương lên mục tiêu mang debuff, sát thương tăng '
                                        '<color=#f26c1c>10%</color>.',
                              'materials': 'None'}]},
 'nikketa': {'name': 'Nikketa',
             'en_name': 'Nikketa',
             'class': 'Chiến Binh',
             'phase': 'Hóa Lỏng',
             'rarity': 'Tinh Nhuệ',
             'weapon_type': 'Súng Bắn Tỉa',
             'ammo_type': 'Đạn Nặng',
             'signature_weapon': 'Border Patrol',
             'weakness': 'Ăn Mòn',
             'server': 'global',
             'skills': [{'name': 'Răn Đe Chủ Động',
                         'tags': ['Đánh Thường', 'Chỉ Định'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây '
                                        'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                        {'name': 'Triển Khai Cảnh Khuyển',
                         'tags': ['Chủ Động', 'AoE', 'Triệu Hồi', 'Suy Yếu'],
                         'description': 'Chọn 1 ô trống <color=#f26c1c>trong phạm vi 9 ô xung quanh</color> và triệu '
                                        'hồi Kulich, sau đó gây ST Vật Lý AoE bằng <color=#f26c1c>80%</color> Tấn Công '
                                        'lên toàn bộ kẻ địch <color=#f26c1c>trong phạm vi 2 ô xung quanh</color> ô chỉ '
                                        'định, đồng thời áp dụng <color=#3487e0>Sợ Tội</color> trong <color=#f26c1c>2 '
                                        'hiệp</color>. Nếu Kulich đã có mặt trên sân, dịch chuyển Kulich đến ô đã '
                                        'chọn. Nikketa nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                        {'name': 'Đòn Đánh Phán Xét',
                         'tags': ['Chủ Động', 'Chỉ Định', 'Suy Yếu'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây '
                                        '<color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>80%</color> Tấn Công '
                                        'và áp dụng <color=#3487e0>Sợ Tội</color> trong <color=#f26c1c>2 hiệp</color>. '
                                        'Nikketa nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu và '
                                        '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                        {'name': 'Phán Quyết Chính Nghĩa',
                         'tags': ['Tuyệt Kỹ', 'Chỉ Định'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, gây '
                                        '<color=#2caadb>ST Hóa Lỏng</color> bằng <color=#f26c1c>130%</color> Tấn Công. '
                                        'Nếu mục tiêu mang <color=#3487e0>Sợ Tội</color>, tung thêm 1 đòn tấn công bồi '
                                        'thêm và giải trừ <color=#3487e0>Sợ Tội</color>.\n'
                                        '\n'
                                        'Tiêu hao toàn bộ Chỉ Số Nhiên Liệu, cứ mỗi 1 điểm Chỉ Số Nhiên Liệu tiêu hao '
                                        'thêm sẽ tăng <color=#f26c1c>5%</color> sát thương của kỹ năng này.'},
                        {'name': 'Chấp Pháp Hiện Trường',
                         'tags': ['Bị Động', 'Cường Hóa'],
                         'description': 'Khi Kulich có mặt trên sân, Nikketa nhận <color=#3487e0>Nhìn Thấu</color>. '
                                        'Trước khi Nikketa và Kulich kích hoạt kỹ năng, cả hai nhận <color=#f26c1c>1 '
                                        'lớp</color> <color=#3487e0>Manh Mối</color>, nếu khai thác Điểm Yếu Thuộc '
                                        'Tính, nhận thêm 1 lớp <color=#3487e0>Manh Mối</color>.\n'
                                        '\n'
                                        'Kulich chỉ có thể Phản Kích 1 lần mỗi hiệp. Sau khi Kulich Phản Kích, Nikketa '
                                        'sẽ bồi tiếp bằng KN Tuyệt Kỹ Phán Quyết Chính Nghĩa lên mục tiêu (lần thi '
                                        'triển này không tiêu hao Chỉ Số Nhiên Liệu).'}],
             'summons': [{'name': 'Kulich',
                          'type': 'Vật Triệu Hồi Hóa Lỏng',
                          'description': 'Chú cảnh khuyển trung thành và quả cảm của Nikketa. Luôn sẵn sàng lao vào '
                                         'bảo vệ đồng đội và thực hiện đòn phản công chớp nhoáng.',
                          'stats': {'hp': '100% HP ban đầu của Nikketa',
                                    'atk': '80% Tấn Công ban đầu của Nikketa',
                                    'def': '100% Phòng Thủ ban đầu của Nikketa'},
                          'skills': [{'name': 'Sự Trung Thành Của Kulich',
                                      'tags': ['Bị Động', 'Phản Kích'],
                                      'description': 'Kẻ địch sẽ không chọn Kulich làm mục tiêu tấn công. Nếu kẻ địch '
                                                     'trong phạm vi 3 ô gây sát thương, Kulich thực hiện Phản Kích, '
                                                     'gây ST Hóa Lỏng bằng 80% Tấn Công và 2 điểm ST Ổn Định.'},
                                     {'name': 'Uy Hiếp Của Kulich',
                                      'tags': ['Bị Động'],
                                      'description': 'Giảm 10% Tấn Công của toàn bộ kẻ địch trong phạm vi 5 ô xung '
                                                     'quanh. Kỹ năng bị động này mở khóa sau khi mở Đốt Sống 5.'}]}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Đòn Đánh Phán Xét',
                                'effect': 'Hệ số sát thương tăng thêm <color=#f26c1c>20%</color>.\n'
                                          'Chỉ Lệnh Bổ Sung được thay thế bằng Hành Động Thêm.'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Phán Quyết Chính Nghĩa',
                                'effect': 'Hệ số sát thương tăng thêm <color=#f26c1c>20%</color>. Lượng Chỉ Số Nhiên '
                                          'Liệu tiêu hao giảm <color=#f26c1c>1 điểm</color>.\n'
                                          'Nếu mục tiêu mang <color=#3487e0>Sợ Tội</color>, áp dụng '
                                          '<color=#3487e0>Giám Sát</color> lên mục tiêu trong <color=#f26c1c>1 '
                                          'hiệp</color> sau khi thi triển kỹ năng.'},
                               {'tier': 3,
                                'level': 2,
                                'skill': 'Chấp Pháp Hiện Trường',
                                'effect': 'Giới hạn cộng dồn tối đa của <color=#3487e0>Manh Mối</color> được nhân đôi '
                                          'lên <color=#f26c1c>10 lớp</color>. Kulich có thể thực hiện thêm 1 lần Phản '
                                          'Kích mỗi hiệp.'},
                               {'tier': 4,
                                'level': 2,
                                'skill': 'Triển Khai Cảnh Khuyển',
                                'effect': 'ST Ổn Định tăng thêm <color=#f26c1c>2 điểm</color>.\n'
                                          'Cường hóa hiệu ứng <color=#3487e0>Sợ Tội</color>: Chịu thêm '
                                          '<color=#f26c1c>10%</color> ST Hóa Lỏng, và hồi phục '
                                          '<color=#f26c1c>30%</color> HP tối đa cho Kulich sau khi dịch chuyển vị '
                                          'trí.'},
                               {'tier': 5,
                                'level': 3,
                                'skill': 'Triển Khai Cảnh Khuyển',
                                'effect': 'Tầm phản công của Sự Trung Thành Của Kulich tăng thêm <color=#f26c1c>2 '
                                          'ô</color>. Lượng HP kế thừa của Kulich tăng lên '
                                          '<color=#f26c1c>100%</color>.\n'
                                          'Kulich nhận kỹ năng Uy Hiếp Của Kulich.'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Phán Quyết Chính Nghĩa',
                                'effect': 'Cứ mỗi 1 điểm Chỉ Số Nhiên Liệu tiêu hao thêm, sát thương tăng lên '
                                          '<color=#f26c1c>10%</color>. <color=#3487e0>Sợ Tội</color> sẽ không còn bị '
                                          'giải trừ sau đòn đánh.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Doll Chính Trực',
                       'level': 20,
                       'effect': 'Sau khi dùng đánh thường hoặc kỹ năng đơn thể, nhận <color=#f26c1c>1 điểm</color> '
                                 'Chỉ Số Nhiên Liệu.',
                       'materials': '3\n\n\n3000'},
                      {'name': 'Khóa Cố Định 2 - Sứ Giả Công Lý',
                       'level': 20,
                       'effect': 'Nếu mục tiêu mang <color=#3487e0>Sợ Tội</color>, gây thêm <color=#f26c1c>2 '
                                 'điểm</color> ST Ổn Định lên mục tiêu đó.',
                       'materials': '3\n\n\n3000'},
                      {'name': 'Khóa Cố Định 3 - Khí Phách Quả Cảm',
                       'level': 30,
                       'effect': 'Đòn Đánh Phán Xét: Kỹ năng này đổi thành gây <color=#2caadb>ST Hóa Lỏng</color> AoE '
                                 'bằng <color=#f26c1c>80%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 2 ô quanh '
                                 'mục tiêu.',
                       'materials': '3\n\n\n8000'},
                      {'name': 'Khóa Cố Định 4 - Báo Ứng Xứng Đáng',
                       'level': 30,
                       'effect': 'Triển Khai Cảnh Khuyển: Sau khi dùng kỹ năng, tạo ô địa hình <color=#3487e0>Dòng '
                                 'Ngầm</color> trong phạm vi hiệu lực trong <color=#f26c1c>2 hiệp</color>.',
                       'materials': '3\n\n\n8000'},
                      {'name': 'Khóa Cố Định 5 - Ánh Nhìn Nghiêm Nghị',
                       'level': 40,
                       'effect': 'Sau khi tấn công, nếu mục tiêu đang trong trạng thái Phá Vỡ Ổn Định, áp dụng '
                                 '<color=#3487e0>Chạy Trốn</color> trong <color=#f26c1c>1 hiệp</color>.',
                       'materials': '3\n\n\n12000'},
                      {'name': 'Khóa Cố Định 6 - Không Khí Áp Đảo',
                       'level': 40,
                       'effect': 'Khi nhận <color=#3487e0>Manh Mối</color>, nhận thêm <color=#3487e0>Tấn Công Tăng '
                                 'II</color> trong <color=#f26c1c>1 hiệp</color>.',
                       'materials': '3\n\n\n12000'},
                      {'name': 'Khóa Tương Thích - Bạn Đồng Hành Can Trường',
                       'level': '-',
                       'effect': 'Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%',
                       'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                      {'name': 'Khóa Chung - Người Che Chở',
                       'level': 40,
                       'effect': 'Tấn Công +5.0% / Nếu bản thân sở hữu Buff thuộc tính Hóa Lỏng, Tỷ Lệ Bạo Kích tăng '
                                 '<color=#f26c1c>10%</color>.',
                       'materials': 'None'},
                      {'name': 'Khóa Mở Rộng - Công Lý Tuyệt Đối',
                       'level': 60,
                       'effect': 'Sau khi kết thúc hành động, nhận <color=#f26c1c>1 lớp</color> <color=#3487e0>Chính '
                                 'Nghĩa</color>.\n'
                                 'Mỗi khi Kulich thực hiện 1 lần Phản Kích, hồi phục <color=#f26c1c>1 điểm</color> Chỉ '
                                 'Số Nhiên Liệu cho Nikketa. Tầm phản kích của Sự Trung Thành Của Kulich tăng thêm '
                                 '<color=#f26c1c>2 ô</color>.\n'
                                 '<color=#3487e0>Chính Nghĩa</color>: Tăng <color=#f26c1c>30%</color> TL Bạo Kích và '
                                 '<color=#f26c1c>30%</color> ST Bạo Kích của bản thân. Khi chủ động dùng KN Tuyệt Kỹ '
                                 'Phán Quyết Chính Nghĩa, tiêu hao 5 lớp hiệu ứng này để thi triển KN Tuyệt Kỹ thêm 1 '
                                 'lần. Tối đa cộng dồn 5 lớp, không thể giải trừ.',
                       'materials': '3\n\n\n15000'}]},
 'ots-14': {'name': 'OTs-14',
            'en_name': 'OTs-14',
            'class': 'Vệ Binh',
            'phase': 'Cộng Hưởng',
            'rarity': 'Tinh Nhuệ',
            'weapon_type': 'Súng Trường Tấn Công',
            'ammo_type': 'Đạn Vừa',
            'signature_weapon': 'Grozny',
            'weakness': 'Thiêu Đốt',
            'server': 'global',
            'skills': [{'name': 'Cú Bắn Tích Lũy',
                        'tags': ['Đánh Thường', 'Chỉ Định'],
                        'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                       'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                       {'name': 'Áp Chế Toàn Diện',
                        'tags': ['Chủ Động', 'AoE'],
                        'description': 'Chọn 1 ô <color=#f26c1c>trong phạm vi 8 ô xung quanh</color> và gây '
                                       '<color=#e52955FF>ST Cộng Hưởng</color> AoE bằng <color=#f26c1c>120%</color> '
                                       'Tấn Công lên toàn bộ kẻ địch trong phạm vi 3×3 ô. Nếu OTs-14 đang ở trạng thái '
                                       '<color=#3487e0>Chỉ Lệnh Yểm Hộ</color>, lượng sát thương tích lũy bởi '
                                       '<color=#3487e0>Chế Độ Chỉ Huy</color> tăng <color=#f26c1c>25%</color> sau khi '
                                       'dùng kỹ năng. Nếu đang ở <color=#3487e0>Chỉ Lệnh Bạo Phá</color>, cứ mỗi 15% '
                                       'ST Bạo Kích ban đầu, sát thương gây ra tăng <color=#f26c1c>15%</color> và hệ '
                                       'số sát thương được nhân đôi.'},
                       {'name': 'Lệnh Tác Chiến',
                        'tags': ['Chủ Động', 'Cường Hóa'],
                        'description': 'Chọn chuyển đổi giữa <color=#3487e0>Chỉ Lệnh Yểm Hộ</color> và '
                                       '<color=#3487e0>Chỉ Lệnh Bạo Phá</color>. Nhận <color=#3487e0>Chỉ Lệnh Bổ '
                                       'Sung</color>. Kỹ năng này không tiêu hao lượt hành động và có thể thi triển 1 '
                                       'lần mỗi hiệp.'},
                       {'name': 'Càn Quét Tầm Xa',
                        'tags': ['Tuyệt Kỹ', 'AoE'],
                        'description': 'Chọn một hướng và gây <color=#e52955FF>ST Cộng Hưởng</color> AoE bằng '
                                       '<color=#f26c1c>150%</color> Tấn Công lên toàn bộ kẻ địch trong khu vực hình '
                                       'chữ nhật 3×10 ô phía trước theo hướng đã chọn. Tiêu hao toàn bộ Chỉ Số Nhiên '
                                       'Liệu, cứ mỗi 1 điểm tiêu hao thêm sẽ tăng <color=#f26c1c>10%</color> sát '
                                       'thương gây ra và tăng <color=#f26c1c>1 điểm</color> ST Ổn Định.'},
                       {'name': 'Chiến Thuật Bậc Thầy',
                        'tags': ['Bị Động', 'Cường Hóa'],
                        'description': 'Khi bắt đầu trận chiến, OTs-14 tự động vào trạng thái <color=#3487e0>Chỉ Lệnh '
                                       'Yểm Hộ</color>. Khi đồng minh trong phạm vi 6 ô bị tấn công, OTs-14 thực hiện '
                                       '<color=#3487e0>Yểm Hộ</color>, giảm <color=#f26c1c>30%</color> sát thương phải '
                                       'chịu cho đồng minh đó. Mỗi hiệp kích hoạt tối đa 2 lần.\n'
                                       '\n'
                                       'Khi ở trạng thái <color=#3487e0>Chỉ Lệnh Bạo Phá</color>, sát thương gây ra '
                                       'tăng <color=#f26c1c>25%</color> và tỷ lệ bạo kích tăng '
                                       '<color=#f26c1c>20%</color>.'},
                       {'name': 'Bộc Phá Chí Mạng',
                        'tags': ['Đánh Thường', 'Chủ Động'],
                        'description': 'Chọn 1 ô trong phạm vi 3-10 ô phía trước bản thân, gây ST Cộng Hưởng AoE bằng '
                                       '<color=#f26c1c>150%</color> Tấn Công lên toàn bộ kẻ địch trong phạm vi 3 ô '
                                       'quanh ô đã chọn. Tiêu hao 1 <color=#3487e0>Mạch Xung Quá Tải</color> để gây '
                                       'thêm sát thương cố định bằng <color=#f26c1c>10%</color> lượng sát thương tích '
                                       'lũy của <color=#3487e0>Mạch Xung Quá Tải</color> đã tiêu hao.'}],
            'fortification': [{'tier': 1,
                               'level': 2,
                               'skill': 'Lệnh Tác Chiến',
                               'effect': 'Cường hóa hiệu ứng <color=#3487e0>Chỉ Lệnh Yểm Hộ</color>: Mức tăng ST Bạo '
                                         'Kích của tất cả đơn vị đồng minh ngoại trừ bản thân được nâng lên '
                                         '<color=#f26c1c>15%</color> ST Bạo Kích ban đầu của bản thân.\n'
                                         'Cường hóa hiệu ứng <color=#3487e0>Chỉ Lệnh Bạo Phá</color>: Mức tăng Tấn '
                                         'Công của bản thân được nâng lên <color=#f26c1c>15%</color> Tấn Công ban đầu '
                                         'của tất cả Doll đồng minh ngoại trừ bản thân.'},
                              {'tier': 2,
                               'level': 2,
                               'skill': 'Áp Chế Toàn Diện',
                               'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>150%</color>.\n'
                                         'Phạm vi hiệu lực mở rộng lên phạm vi <color=#f26c1c>5×5 ô</color>.\n'
                                         'Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>.'},
                              {'tier': 3,
                               'level': 2,
                               'skill': 'Càn Quét Tầm Xa',
                               'effect': 'Cường hóa hiệu ứng <color=#3487e0>Đồng Hóa Nghịch Đảo</color>: Sát thương '
                                         'của Bộc Phá Chí Mạng tăng lên <color=#f26c1c>200%</color>, và tầm bắn hiệu '
                                         'lực tăng thêm <color=#f26c1c>2 ô</color>.'},
                              {'tier': 4,
                               'level': 3,
                               'skill': 'Càn Quét Tầm Xa',
                               'effect': 'Cường hóa hiệu ứng <color=#3487e0>Đồng Hóa Nghịch Đảo</color>: Mỗi khi sử '
                                         'dụng Bộc Phá Chí Mạng trong hiệp hiện tại, hệ số sát thương của Bộc Phá Chí '
                                         'Mạng tăng thêm <color=#f26c1c>50%</color>, và hệ số sát thương cố định gây '
                                         'ra khi tiêu hao <color=#3487e0>Mạch Xung Quá Tải</color> tăng thêm '
                                         '<color=#f26c1c>10%</color>.'},
                              {'tier': 5,
                               'level': 3,
                               'skill': 'Áp Chế Toàn Diện',
                               'effect': 'Nếu bản thân đang có <color=#3487e0>Chỉ Lệnh Yểm Hộ</color>, mức tăng sát '
                                         'thương tích lũy bởi Chế Độ Chỉ Huy sau khi dùng kỹ năng được nâng lên '
                                         '<color=#f26c1c>33%</color>.\n'
                                         'Nếu bản thân đang có <color=#3487e0>Chỉ Lệnh Bạo Phá</color>, cứ mỗi '
                                         '<color=#f26c1c>15%</color> ST Bạo Kích ban đầu, hệ số sát thương tăng thêm '
                                         '<color=#f26c1c>15%</color>.'},
                              {'tier': 6,
                               'level': 2,
                               'skill': 'Chiến Thuật Bậc Thầy',
                               'effect': 'Kỹ năng chủ động Áp Chế Toàn Diện tạo các ô địa hình Giai Đoạn cấp 1 trong '
                                         '<color=#f26c1c>2 hiệp</color> trong phạm vi hiệu lực nếu có bất kỳ Tái Cấu '
                                         'Trúc Giai Đoạn nào đang kích hoạt. <color=#3487e0>Tái Tạo - 0</color> không '
                                         'tạo ô địa hình.\n'
                                         'Cường hóa các hiệu ứng của <color=#3487e0>Tái Tạo Tế Bào</color>:\n'
                                         '<color=#3487e0>Tái Tạo - Thiêu Đốt</color> - Hóa giải '
                                         '<color=#f26c1c>1</color> Debuff khi đồng đội nhận Tàn Tro;\n'
                                         '<color=#3487e0>Tái Tạo - Dẫn Điện</color> - Khi một đơn vị địch rơi vào '
                                         'trạng thái Sụp Đổ Ổn Định, toàn bộ đồng minh hồi phục <color=#f26c1c>1 '
                                         'điểm</color> Chỉ Số Ổn Định;\n'
                                         '<color=#3487e0>Tái Tạo - Băng Kết</color> - Khi một đồng minh gây sát '
                                         'thương, tăng Tấn Công của họ bằng <color=#f26c1c>10%</color> giá trị lá '
                                         'chắn;\n'
                                         '<color=#3487e0>Tái Tạo - Ăn Mòn</color> - Kỹ năng chủ động Áp Chế Toàn Diện '
                                         'kích hoạt toàn bộ Debuff thuộc tính Ăn Mòn của các đơn vị địch trong phạm vi '
                                         'hiệu lực;\n'
                                         '<color=#3487e0>Tái Tạo - Hóa Lỏng</color> - Với mỗi đơn vị đồng minh, tất cả '
                                         'Vật Triệu Hồi Thực Thể tăng <color=#f26c1c>1%</color> Tấn Công và '
                                         '<color=#f26c1c>1%</color> HP tối đa;\n'
                                         '<color=#3487e0>Tái Tạo - 0</color> - Chỉ Lệnh Bạo Phá tăng Tấn Công thêm '
                                         '<color=#f26c1c>50%</color> thay vì 30%, bỏ qua <color=#f26c1c>5%</color> '
                                         'Phòng Thủ cho mỗi <color=#f26c1c>15%</color> ST Bạo Kích ban đầu.'}],
            'keys': [{'name': 'Khóa Cố Định 1 - Kỷ Luật Quân Đội',
                      'level': 20,
                      'effect': 'Khi bắt đầu trận chiến, tăng <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.',
                      'materials': '3\n\n\n3000'},
                     {'name': 'Khóa Cố Định 2 - Tiên Phong Chắn Đạn',
                      'level': 20,
                      'effect': 'Khi thực hiện Yểm Hộ, hồi phục HP bằng <color=#f26c1c>15%</color> Tấn Công cho mục '
                                'tiêu được bảo vệ.',
                      'materials': '3\n\n\n3000'},
                     {'name': 'Khóa Cố Định 3 - Hỏa Lực Đồng Loạt',
                      'level': 30,
                      'effect': 'Khi ở trạng thái Chỉ Lệnh Bạo Phá, ST AoE gây ra tăng thêm '
                                '<color=#f26c1c>15%</color>.',
                      'materials': '3\n\n\n8000'},
                     {'name': 'Khóa Cố Định 4 - Chuyển Trạng Thái Nhanh',
                      'level': 30,
                      'effect': 'Sau khi thi triển Lệnh Tác Chiến, nhận thêm 3 ô Di Chuyển Thêm trong hiệp đó.',
                      'materials': '3\n\n\n8000'},
                     {'name': 'Khóa Cố Định 5 - Bản Lĩnh Chỉ Huy',
                      'level': 40,
                      'effect': 'Tất cả đồng minh trong phạm vi 3 ô quanh OTs-14 nhận tăng <color=#f26c1c>10%</color> '
                                'Tấn Công và <color=#f26c1c>10%</color> Phòng Thủ.',
                      'materials': '3\n\n\n12000'},
                     {'name': 'Khóa Cố Định 6 - Chiến Lược Áp Đảo',
                      'level': 40,
                      'effect': 'Khi tấn công kẻ địch đang chịu debuff, sát thương gây ra tăng '
                                '<color=#f26c1c>15%</color>.',
                      'materials': '3\n\n\n12000'},
                     {'name': 'Khóa Tương Thích - Niềm Tin Sắt Đá',
                      'level': '-',
                      'effect': 'Tấn Công +3%, HP +3%, ST Bạo Kích +3%',
                      'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                     {'name': 'Khóa Chung - Tác Chiến Phối Hợp',
                      'level': 40,
                      'effect': 'Tấn Công +5.0% / Khi ở gần đồng minh trong phạm vi 2 ô, sát thương tăng '
                                '<color=#f26c1c>10%</color>.',
                      'materials': 'None'}]}}
