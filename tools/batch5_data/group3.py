"""
Auto-synced batch data.
"""

GROUP_3_DATA = {'phaetusa': {'name': 'Phaetusa',
              'skills': [{'name': 'Song Trảm',
                          'tags': ['Đánh Thường', 'Chuẩn Xác', 'Cận Chiến'],
                          'description': 'Chọn 1 mục tiêu trong phạm vi 1 ô, gây cho mục tiêu ST Vật Lý cận chiến bằng '
                                         '80% Tấn Công.'},
                         {'name': 'Tỷ Dực Giáng Lâm',
                          'tags': ['Chủ Động', 'Phạm Vi', 'Dịch Chuyển'],
                          'description': 'Chọn 1 ô trong khu vực chữ thập 8 ô, đáp xuống ô đã chọn và gây ST Ăn Mòn '
                                         'cận chiến AoE bằng 90% Tấn Công cho tất cả mục tiêu địch trên đường đi.'},
                         {'name': 'Bẫy Gương',
                          'tags': ['Chủ Động', 'Suy Yếu'],
                          'description': 'Nhận 1 tầng <color=#3487e0>Cộng Hưởng Lưỡi Đao</color> và gắn '
                                         '<color=#3487e0>Xé Rách</color> lên tất cả mục tiêu địch trên sân trong 2 '
                                         'lượt. Sau khi dùng kỹ năng, Phaetusa nhận <color=#3487e0>Chỉ Lệnh Bổ '
                                         'Sung</color>.'},
                         {'name': 'Thiên Đường Song Sinh',
                          'tags': ['Tuyệt Kỹ', 'Phạm Vi', 'Cận Chiến'],
                          'description': 'Gây ST Ăn Mòn cận chiến AoE bằng 90% Tấn Công cho tất cả kẻ địch trong bán '
                                         'kính 5 ô. Tiêu hao toàn bộ tầng <color=#3487e0>Cộng Hưởng Lưỡi Đao</color>; '
                                         'mỗi tầng tiêu hao làm tăng hệ số sát thương của kỹ năng này thêm 10% rồi sau '
                                         'đó nhân đôi thêm trên cơ sở đó.'},
                         {'name': 'Đồng Hành',
                          'tags': ['Bị Động', 'Chủ Động', 'Hỗ Trợ'],
                          'description': 'Mỗi khi gây ST Cận Chiến, nhận 1 điểm Chỉ Số Nhiên Liệu. Hiệu quả này có thể '
                                         'kích hoạt 3 lần mỗi hiệp.\n'
                                         'Khi kẻ địch trong phạm vi chịu sát thương từ đòn tấn công AoE của đồng minh, '
                                         'thực hiện <color=#3487e0>Hành Động Chi Viện</color> lên mục tiêu đó, gây ST '
                                         'Ăn Mòn cận chiến AoE bằng 90% Tấn Công và 1 điểm ST Ổn Định. Hiệu quả này có '
                                         'thể kích hoạt 3 lần mỗi hiệp.\n'
                                         'Sau khi kích hoạt kỹ năng Bẫy Gương, kỹ năng chủ động Đồng Hành sẽ có thể sử '
                                         'dụng. Khi kích hoạt, nhận hiệu ứng <color=#3487e0>Chân Thân</color> và '
                                         '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Có thể sử dụng 1 lần mỗi trận.'}],
              'fortification': [{'tier': 1,
                                 'level': 2,
                                 'skill': 'Bẫy Gương',
                                 'effect': 'Khi bắt đầu trận chiến, nhận <color=#3487e0>Cộng Hưởng Lưỡi Đao</color>. '
                                           'Khi kích hoạt hiệu ứng của <color=#3487e0>Xé Rách</color>, nếu chưa dùng '
                                           'KN Tuyệt Kỹ Thiên Đường Song Sinh, nhận <color=#f26c1c>2 điểm</color> '
                                           '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.\n'
                                           'Khi bắt đầu hiệp, nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu, áp '
                                           'dụng <color=#f26c1c>2 lớp</color> <color=#3487e0>Xé Rách</color> lên '
                                           '<color=#f26c1c>5</color> mục tiêu địch ngẫu nhiên trên toàn trận. Nếu bản '
                                           'thân có <color=#3487e0>Chân Thân</color>, ST gây ra tăng '
                                           '<color=#f26c1c>50%</color>, ST Bạo Kích tăng <color=#f26c1c>25%</color>.'},
                                {'tier': 2,
                                 'level': 2,
                                 'skill': 'Tỷ Dực Giáng Lâm',
                                 'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>120%</color> Tấn Công.\n'
                                           'Độ rộng khu vực hiệu quả tăng thêm <color=#f26c1c>2 ô</color>.'},
                                {'tier': 3,
                                 'level': 2,
                                 'skill': 'Đồng Hành',
                                 'effect': 'Tấn Công và Phòng Thủ của đơn vị đồng minh toàn trận tăng '
                                           '<color=#f26c1c>50%</color>. Có thể kích hoạt 1 lần mỗi hiệp.'},
                                {'tier': 4,
                                 'level': 2,
                                 'skill': 'Thiên Đường Song Sinh',
                                 'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>120%</color> Tấn Công.\n'
                                           'Hiệu ứng <color=#3487e0>Xé Rách</color> tăng: Hệ số sát thương bồi thêm '
                                           'tăng <color=#f26c1c>30%</color>.'},
                                {'tier': 5,
                                 'level': 3,
                                 'skill': 'Đồng Hành',
                                 'effect': 'Chọn 1 hướng, áp dụng <color=#f26c1c>3 lớp</color> <color=#3487e0>Cộng '
                                           'Hưởng Lưỡi Đao</color> lên toàn bộ đồng minh trong phạm vi 3x10 ô phía '
                                           'trước.'},
                                {'tier': 6,
                                 'level': 3,
                                 'skill': 'Bẫy Gương',
                                 'effect': 'Khi thi triển Bẫy Gương, nhận thêm 1 tầng <color=#3487e0>Cộng Hưởng Lưỡi '
                                           'Đao</color> và nhận thêm 1 lượt hành động. Sát thương gây ra cho mục tiêu '
                                           'có <color=#3487e0>Xé Rách</color> tăng <color=#f26c1c>30%</color>.'}],
              'keys': [{'name': 'Khóa Cố Định 1 - Băng Mạch',
                        'level': 20,
                        'effect': 'Lần đầu tiên đạt tối đa tầng Cộng Hưởng Lưỡi Đao, tăng 20% Tỷ Lệ Bạo Kích.',
                        'materials': '3\n\n\n3000'},
                       {'name': 'Khóa Cố Định 2 - Quyết Tâm Kẻ Phiêu Bạt',
                        'level': 20,
                        'effect': 'Khi bắt đầu lượt, gắn Xé Rách lên tất cả kẻ địch trên sân trong 1 lượt. Có thể kích '
                                  'hoạt 1 lần mỗi 2 lượt.',
                        'materials': '3\n\n\n3000'},
                       {'name': 'Khóa Cố Định 3 - Lưỡi Đao Tận Diệt',
                        'level': 30,
                        'effect': 'Nếu đòn tấn công chủ động chỉ đánh trúng 1 mục tiêu địch, sát thương gây ra cho mục '
                                  'tiêu đó tăng 15%.',
                        'materials': '3\n\n\n8000'},
                       {'name': 'Khóa Cố Định 4 - Món Quà Sinh Lực',
                        'level': 30,
                        'effect': 'Mỗi tầng Cộng Hưởng Lưỡi Đao tiêu hao, hồi phục HP bằng 10% Tấn Công và 1 điểm Chỉ '
                                  'Số Ổn Định.',
                        'materials': '3\n\n\n8000'},
                       {'name': 'Khóa Cố Định 5 - Người Gác Biên Giới',
                        'level': 40,
                        'effect': 'Trước khi thực hiện Hành Động Chi Viện, hóa giải 1 buff của mục tiêu.',
                        'materials': '3\n\n\n12000'},
                       {'name': 'Khóa Cố Định 6 - Thính Giác Thợ Săn',
                        'level': 40,
                        'effect': 'Sau khi kích hoạt kỹ năng Bẫy Gương, nhận thêm 6 ô Di Chuyển.',
                        'materials': '3\n\n\n12000'},
                       {'name': 'Khóa Tương Thích - Lõi Kép Tích Hợp',
                        'level': '-',
                        'effect': 'Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%',
                        'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                       {'name': 'Khóa Chung - Khởi Nguyên Hư Không',
                        'level': 40,
                        'effect': 'TL Bạo Kích +5.0% / Nếu Chỉ Số Nhiên Liệu bằng 0 trong hiệp hiện tại, sát thương '
                                  'gây ra tăng 10%.',
                        'materials': 'None'},
                       {'name': 'Khóa Mở Rộng - Bản Sonate Cộng Hưởng Song Hồn',
                        'level': 60,
                        'effect': 'Khi sở hữu Cộng Hưởng Lưỡi Đao, sát thương gây ra tăng 30%. Sau đòn tấn công chủ '
                                  'động, gây ST Ăn Mòn cận chiến bằng 100% Tấn Công 1 lần lên mục tiêu địch gần nhất '
                                  'trong bán kính 8 ô. Sau khi gây sát thương ngoài lượt, gắn 3 tầng Ám Ảnh Mũi Nhọn '
                                  'lên mục tiêu trong 2 hiệp.',
                        'materials': '3\n\n\n15000'}]},
 'qiuhua': {'name': 'Qiuhua',
            'skills': [{'name': 'Khai Đường Mở Lối',
                        'tags': ['Đánh Thường', 'Chuẩn Xác'],
                        'description': 'Chọn 1 mục tiêu địch trong bán kính 6 ô, gây ST Vật Lý tương đương 80% Tấn '
                                       'Công.'},
                       {'name': 'Xèo Xèo Nóng Bỏng',
                        'tags': ['Chủ Động', 'Chuẩn Xác'],
                        'description': 'Chọn 1 mục tiêu địch trong bán kính 6 ô, gây ST Thiêu Đốt tương đương 120% Tấn '
                                       'Công. Nếu khoảng cách giữa Qiuhua và mục tiêu nhỏ hơn hoặc bằng 4 ô, sát '
                                       'thương gây ra tăng 5% và ST Ổn Định tăng 1 điểm.'},
                       {'name': 'Bước Nhảy Vọt',
                        'tags': ['Chủ Động', 'Chuẩn Xác'],
                        'description': 'Chọn 1 ô trong bán kính 6 ô của bản thân và đáp xuống ô đã chọn, gây ST Thiêu '
                                       'Đốt tương đương 30% Tấn Công lên mục tiêu địch gần nhất trong bán kính 6 ô. '
                                       'Sau khi tấn công, nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Giảm thời gian '
                                       'hồi chiêu của Tuyệt Kỹ đi 1 lượt.'},
                       {'name': 'Đun Sôi Cô Đặc',
                        'tags': ['Tuyệt Kỹ', 'Phạm Vi', 'Suy Yếu'],
                        'description': 'Chọn 1 ô trong bán kính 6 ô của bản thân, gây ST Thiêu Đốt AoE tương đương 90% '
                                       'Tấn Công và gắn <color=#3487e0>Vết Cháy</color> lên tất cả kẻ địch trong bán '
                                       'kính 3 ô xung quanh ô chỉ định. Kỹ năng này tiêu hao toàn bộ Chỉ Số Nhiên '
                                       'Liệu, mỗi điểm tiêu hao làm tăng hệ số sát thương thêm 5%.'},
                       {'name': 'Quy Tắc Táo Quân',
                        'tags': ['Bị Động', 'Hỗ Trợ'],
                        'description': 'Khi không có đồng minh nào trong bán kính 2 ô của bản thân, tăng 5% ST Thiêu '
                                       'Đốt gây ra.\n'
                                       '\n'
                                       'Nếu mục tiêu địch trong tầm đánh chịu <color=#3487e0>Quá Nhiệt</color>, Qiuhua '
                                       'phát động 1 lần <color=#3487e0>Chi Viện Tức Thời</color> lên mục tiêu, gây ST '
                                       'Thiêu Đốt tương đương 60% Tấn Công và 1 điểm ST Ổn Định, đồng thời tăng 1 điểm '
                                       'Chỉ Số Nhiên Liệu. Hiệu quả này có thể kích hoạt 1 lần mỗi lượt.\n'
                                       '\n'
                                       'Tăng 30% Tỷ Lệ Bạo Kích khi gây ST Thiêu Đốt lên mục tiêu có '
                                       '<color=#3487e0>Vết Cháy</color>.'}],
            'fortification': [{'tier': 1,
                               'level': 2,
                               'skill': 'Đun Sôi Cô Đặc',
                               'effect': 'Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>. Khi gây sát thương, '
                                         'lập tức kích hoạt <color=#f26c1c>1 lần</color> hiệu ứng của '
                                         '<color=#3487e0>Vết Cháy</color> vốn được kích hoạt khi kết thúc hành động '
                                         'của mục tiêu.'},
                              {'tier': 2,
                               'level': 2,
                               'skill': 'Quy Tắc Táo Quân',
                               'effect': 'Chi Viện Khẩn Cấp có thể kích hoạt từ 1 → <color=#f26c1c>2 lần</color> mỗi '
                                         'hiệp.\n'
                                         '\n'
                                         'Tăng <color=#ff4d4f>ST Thiêu Đốt</color> gây ra từ 5% → '
                                         '<color=#f26c1c>15%</color>. Loại bỏ điều kiện cần thiết để kích hoạt hiệu '
                                         'ứng này.\n'
                                         '\n'
                                         'Khi gây sát thương, nếu Tỷ Lệ Bạo Kích vượt quá <color=#f26c1c>100%</color>, '
                                         'mỗi <color=#f26c1c>1%</color> Tỷ Lệ Bạo Kích vượt mức sẽ chuyển đổi thành '
                                         '<color=#f26c1c>1%</color> ST Bạo Kích.'},
                              {'tier': 3,
                               'level': 3,
                               'skill': 'Quy Tắc Táo Quân',
                               'effect': '<color=#3487e0>Vết Cháy</color> không còn giới hạn tầng tối đa.\n'
                                         '\n'
                                         'Bổ sung hiệu ứng mới khi gây <color=#ff4d4f>ST Thiêu Đốt</color> lên mục '
                                         'tiêu có <color=#3487e0>Vết Cháy</color> - nếu số tầng <color=#3487e0>Vết '
                                         'Cháy</color> nhiều hơn <color=#f26c1c>10 tầng</color>, với mỗi tầng vượt '
                                         'mức, Tấn Công tăng thêm <color=#f26c1c>1%</color>.'},
                              {'tier': 4,
                               'level': 2,
                               'skill': 'Bước Nhảy Vọt',
                               'effect': 'Hệ số sát thương tăng thêm <color=#f26c1c>50%</color>.\n'
                                         '\n'
                                         'Nếu mục tiêu có <color=#3487e0>Vết Cháy</color>, gây thêm 1 lần sát thương '
                                         'cố định tương đương <color=#f26c1c>50%</color> Tấn Công.\n'
                                         '\n'
                                         'Sau khi tấn công, nhận <color=#3487e0>Dị Vị Tăng II</color> và '
                                         '<color=#3487e0>Thế Tấn Công Ổn Định II</color> trong <color=#f26c1c>1 '
                                         'hiệp</color>.'},
                              {'tier': 5,
                               'level': 2,
                               'skill': 'Xèo Xèo Nóng Bỏng',
                               'effect': 'Sau khi tấn công, nhận thêm <color=#f26c1c>6 ô</color> Di Chuyển Bổ Sung.\n'
                                         '\n'
                                         'Nếu mục tiêu có <color=#3487e0>Vết Cháy</color>, sát thương gây ra tăng thêm '
                                         '<color=#f26c1c>30%</color>.\n'
                                         '\n'
                                         'Nếu khoảng cách giữa Qiuhua và mục tiêu nhỏ hơn hoặc bằng <color=#f26c1c>4 '
                                         'ô</color>, sát thương gây ra tăng từ 5% → <color=#f26c1c>15%</color> và ST '
                                         'Ổn Định gây ra tăng từ 1 → <color=#f26c1c>2 điểm</color>.'},
                              {'tier': 6,
                               'level': 3,
                               'skill': 'Đun Sôi Cô Đặc',
                               'effect': 'Nếu kỹ năng này chỉ đánh trúng 1 mục tiêu, sát thương gây ra tăng thêm '
                                         '<color=#f26c1c>15%</color>.\n'
                                         '\n'
                                         'Cường hóa hiệu ứng <color=#3487e0>Vết Cháy</color> - tăng sát thương gây ra '
                                         'mỗi tầng lên <color=#f26c1c>10%</color> Tấn Công của người thi triển, và số '
                                         'tầng nhận được khi chịu <color=#ff4d4f>ST Thiêu Đốt</color> tăng lên '
                                         '<color=#f26c1c>2 tầng</color>.'}],
            'keys': [{'name': 'Khóa Cố Định 1 - Chuẩn Bị Nguyên Liệu',
                      'level': 20,
                      'effect': 'Khi bắt đầu trận chiến, tăng 3 điểm Chỉ Số Nhiên Liệu.',
                      'materials': '3\n\n\n3000'},
                     {'name': 'Khóa Cố Định 2 - Bếp Lửa Bập Bùng',
                      'level': 20,
                      'effect': 'Khi bắt đầu lượt, gắn Vết Cháy lên kẻ địch có HP cao nhất. Hiệu quả này có thời gian '
                                'hồi chiêu 2 lượt.',
                      'materials': '3\n\n\n3000'},
                     {'name': 'Khóa Cố Định 3 - Dao Thớt Mau Lẹ',
                      'level': 30,
                      'effect': 'Miễn nhiễm với tất cả debuff từ ô địa hình Thiêu Đốt và tất cả debuff thuộc tính '
                                'Thiêu Đốt. Khi kết thúc hành động, nếu Qiuhua đứng trên ô địa hình Thiêu Đốt, hồi '
                                'phục 2 điểm Ổn Định và lượng HP tương đương 10% HP tối đa.',
                      'materials': '3\n\n\n8000'},
                     {'name': 'Khóa Cố Định 4 - Xào Nấu Thơm Lừng',
                      'level': 30,
                      'effect': 'Trước khi sử dụng đòn tấn công chủ động, gắn Quá Nhiệt lên mục tiêu trong 1 lượt.',
                      'materials': '3\n\n\n8000'},
                     {'name': 'Khóa Cố Định 5 - Khói Bếp Vấn Vương',
                      'level': 40,
                      'effect': 'Sau khi di chuyển, nhận 1 tầng Lá Chắn Tốc Độ.',
                      'materials': '3\n\n\n12000'},
                     {'name': 'Khóa Cố Định 6 - Bụng No Tròn Trịa',
                      'level': 40,
                      'effect': 'Trước khi thực hiện Chi Viện Tức Thời, hóa giải 1 buff của mục tiêu.',
                      'materials': '3\n\n\n12000'},
                     {'name': 'Khóa Tương Thích',
                      'level': '-',
                      'effect': 'Tấn Công +3%, HP +3%, ST Bạo Kích +3%',
                      'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                     {'name': 'Khóa Chung',
                      'level': 40,
                      'effect': 'TL Bạo Kích +5.0% / Khi đòn đánh ngoài lượt gây ST Thiêu Đốt, sát thương gây ra tăng '
                                '10%.',
                      'materials': 'None'},
                     {'name': 'Khóa Mở Rộng',
                      'level': 60,
                      'effect': 'Hệ số sát thương của Chi Viện Tức Thời tăng 30% và khi gây sát thương sẽ bỏ qua 15% '
                                'phòng thủ của mục tiêu; mỗi lần thực hiện Chi Viện Tức Thời, nhận 1 tầng Hào Quang '
                                'Chảo Nóng trong 2 hiệp.\n'
                                '\n'
                                'Hào Quang Chảo Nóng: ST Thiêu Đốt gây ra tăng 7%, sát thương phải chịu giảm 7%, cộng '
                                'dồn tối đa 4 tầng. Thuộc loại Buff Thiêu Đốt, không thể hóa giải.\n'
                                '\n'
                                'Khi đơn vị có Vết Cháy tử trận, gây ST Thiêu Đốt AoE tương đương 130% Tấn Công của '
                                'Qiuhua lên tất cả đơn vị xung quanh trong bán kính 3 ô.\n'
                                '\n'
                                'Khi kỹ năng chủ động Bước Nhảy Vọt gây sát thương, tạo ô địa hình Thiêu Rụi trong bán '
                                'kính 1 ô xung quanh mục tiêu, duy trì trong 2 lượt.',
                      'materials': '3\n\n\n12000'}]},
 'sakura': {'name': 'Sakura',
            'skills': [{'name': 'Tiếng Chuông Anh Đào',
                        'tags': ['Đánh Thường', 'Chuẩn Xác'],
                        'description': 'Chọn 1 mục tiêu địch trong bán kính 7 ô, gây ST Vật Lý tương đương 80% Tấn '
                                       'Công.'},
                       {'name': 'Hoa Rơi Tung Bay',
                        'tags': ['Chủ Động', 'Chuẩn Xác'],
                        'description': 'Chọn 1 ô trống trong bán kính 2 ô của một Doll đồng minh hoặc kẻ địch chịu '
                                       '<color=#3487e0>Dấu Anh Đào</color>, sau đó nhảy tới ô đã chọn, gây ST Thiêu '
                                       'Đốt AoE tương đương 60% Tấn Công lên tất cả kẻ địch trong bán kính 2 ô. Nhận '
                                       '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                       {'name': 'Chuyển Phát Vận Rủi',
                        'tags': ['Chủ Động', 'Chuẩn Xác', 'Suy Yếu'],
                        'description': 'Chọn 1 mục tiêu địch trong bán kính 7 ô, gây ST Thiêu Đốt tương đương 130% Tấn '
                                       'Công, đồng thời gắn 2 tầng <color=#3487e0>Dấu Anh Đào</color>.\n'
                                       'Trước khi tấn công, gắn thêm <color=#3487e0>Vận Rủi</color> lên mục tiêu trong '
                                       '3 lượt.'},
                       {'name': 'Đại Mạo Hiểm Dị Giới',
                        'tags': ['Tuyệt Kỹ', 'Phạm Vi'],
                        'description': 'Chọn 1 hướng và gắn 3 tầng <color=#3487e0>Dấu Anh Đào</color> lên tất cả kẻ '
                                       'địch trong phạm vi 3x10 ô phía trước, gây ST Thiêu Đốt AoE tương đương 90% Tấn '
                                       'Công.\n'
                                       'Sau khi sử dụng kỹ năng này, kích hoạt hiệu ứng của <color=#3487e0>Dấu Anh '
                                       'Đào</color>, đồng thời nhận <color=#3487e0>Vận May</color> trong 2 lượt và 2 '
                                       'điểm Chỉ Số Nhiên Liệu.'},
                       {'name': 'Cầu Nguyện Phúc Lành',
                        'tags': ['Bị Động'],
                        'description': 'Khi bắt đầu trận chiến, nhận <color=#3487e0>Dẫn Nhiệt</color>. Khi kích hoạt '
                                       'hiệu ứng của <color=#3487e0>Dấu Anh Đào</color>, nếu chưa sử dụng Tuyệt Kỹ Đại '
                                       'Mạo Hiểm Dị Giới, nhận 2 tầng <color=#3487e0>Lửa Thiêu Đốt</color>. Khi bắt '
                                       'đầu mỗi lượt, nhận 2 điểm Chỉ Số Nhiên Liệu và gắn 2 tầng <color=#3487e0>Dấu '
                                       'Anh Đào</color> lên 3 kẻ địch ngẫu nhiên trên sân. Nếu Sakura sở hữu '
                                       '<color=#3487e0>Vận May</color>, sát thương của cô tăng 20%.'}],
            'fortification': [{'tier': 1,
                               'level': 2,
                               'skill': 'Cầu Nguyện Phúc Lành',
                               'effect': 'Áp dụng ngẫu nhiên <color=#3487e0>Dấu Anh Đào</color> lên tối đa '
                                         '<color=#f26c1c>5</color> kẻ địch; hệ số sát thương của <color=#3487e0>Dấu '
                                         'Anh Đào</color> tăng lên <color=#f26c1c>90%</color>, và bán kính hiệu lực '
                                         'tăng thêm <color=#f26c1c>1 ô</color>.\n'
                                         'Nếu một đơn vị địch đang đứng trên ô địa hình loại Thiêu Đốt, sát thương gây '
                                         'ra bởi <color=#3487e0>Dấu Anh Đào</color> tăng thêm '
                                         '<color=#f26c1c>30%</color>.'},
                              {'tier': 2,
                               'level': 2,
                               'skill': 'Hoa Rơi Tung Bay',
                               'effect': 'Tầm bắn tăng thêm <color=#f26c1c>1 ô</color>; phạm vi hiệu lực tăng thêm '
                                         '<color=#f26c1c>1 ô</color>; hệ số sát thương tăng thêm '
                                         '<color=#f26c1c>15%</color>; giảm tiêu hao Chỉ Số Nhiên Liệu đi '
                                         '<color=#f26c1c>1 điểm</color>.'},
                              {'tier': 3,
                               'level': 2,
                               'skill': 'Cầu Nguyện Phúc Lành',
                               'effect': 'Nếu bản thân sở hữu <color=#3487e0>Vận May</color>, sát thương gây ra tăng '
                                         'thêm <color=#f26c1c>50%</color> và ST Bạo Kích tăng thêm '
                                         '<color=#f26c1c>25%</color>.\n'
                                         'Khi một kẻ địch nhận <color=#3487e0>Dấu Anh Đào</color>, tạo ô địa hình '
                                         '<color=#3487e0>Thiêu Rụi</color> trong phạm vi bán kính <color=#f26c1c>1 '
                                         'ô</color> xung quanh mục tiêu trong <color=#f26c1c>3 hiệp</color>; khi '
                                         '<color=#3487e0>Dấu Anh Đào</color> gây sát thương, bỏ qua '
                                         '<color=#f26c1c>15%</color> Phòng Thủ của mục tiêu.'},
                              {'tier': 4,
                               'level': 2,
                               'skill': 'Chuyển Phát Vận Rủi',
                               'effect': 'Tăng số tầng <color=#3487e0>Dấu Anh Đào</color> được áp dụng lên '
                                         '<color=#f26c1c>3 tầng</color>; mức tăng sát thương từ <color=#3487e0>Vận '
                                         'Rủi</color> nâng lên <color=#f26c1c>30%</color>.'},
                              {'tier': 5,
                               'level': 3,
                               'skill': 'Đại Mạo Hiểm Dị Giới',
                               'effect': 'Hệ số sát thương tăng thêm <color=#f26c1c>30%</color>; mở rộng phạm vi hiệu '
                                         'lực thành khu vực <color=#f26c1c>5×10 ô</color> phía trước; cộng dồn hiệu '
                                         'ứng này tới giới hạn tối đa trên tất cả đơn vị địch trên toàn sân đang bị '
                                         'ảnh hưởng bởi <color=#3487e0>Dấu Anh Đào</color>.'},
                              {'tier': 6,
                               'level': 3,
                               'skill': 'Đại Mạo Hiểm Dị Giới',
                               'effect': '<color=#3487e0>Vận May</color> nhận thêm hiệu ứng:\n'
                                         'Trước khi một đơn vị đồng minh thực hiện đòn tấn công chủ động hoặc đòn tấn '
                                         'công ngoài lượt (ngoại trừ bản thân), Sakura áp dụng <color=#f26c1c>1 '
                                         'tầng</color> <color=#3487e0>Dấu Anh Đào</color> lên mục tiêu đó.\n'
                                         'Có thể kích hoạt tối đa <color=#f26c1c>3 lần</color> mỗi hiệp.'}],
            'keys': [{'name': 'Khóa Cố Định 1 - Chăm Chỉ Và Quả Cảm',
                      'level': 20,
                      'effect': 'Khi bắt đầu trận chiến, gắn 1 tầng Dấu Anh Đào lên 3 đơn vị địch bất kỳ trên sân.',
                      'materials': '3\n\n\n3000'},
                     {'name': 'Khóa Cố Định 2 - Hậu Cần Kịp Thời',
                      'level': 20,
                      'effect': 'Khi gắn Dấu Anh Đào bằng kỹ năng không phải Tuyệt Kỹ, đồng thời gắn Quá Nhiệt trong 1 '
                                'lượt.',
                      'materials': '3\n\n\n3000'},
                     {'name': 'Khóa Cố Định 3 - Chân Thành Tạ Lỗi',
                      'level': 30,
                      'effect': 'Khi gắn Vận Rủi, hóa giải 1 buff của mục tiêu.',
                      'materials': '3\n\n\n8000'},
                     {'name': 'Khóa Cố Định 4 - Số Phận Trớ Trêu',
                      'level': 30,
                      'effect': 'Khi bắt đầu trận chiến, gắn Vận Rủi lên đơn vị địch có HP cao nhất trên sân trong 3 '
                                'lượt.',
                      'materials': '3\n\n\n8000'},
                     {'name': 'Khóa Cố Định 5 - Đơn Thương Độc Mã',
                      'level': 40,
                      'effect': 'Khi kết thúc hành động, nếu có đơn vị địch trong bán kính 3 ô, nhận 1 tầng Lá Chắn '
                                'Tốc Độ.',
                      'materials': '3\n\n\n12000'},
                     {'name': 'Khóa Cố Định 6 - Tiến Bộ Mỗi Ngày',
                      'level': 40,
                      'effect': 'Khi kẻ địch chịu Dấu Anh Đào tử trận, tăng 4% Tấn Công của bản thân, tối đa tăng 20%.',
                      'materials': '3\n\n\n12000'},
                     {'name': 'Khóa Tương Thích - Nhiệm Vụ Hoàn Thành',
                      'level': '-',
                      'effect': 'Tấn Công +3%, HP +3%, ST Bạo Kích +3%',
                      'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                     {'name': 'Khóa Chung - Người Vận Chuyển Xuất Sắc',
                      'level': 40,
                      'effect': 'TL Bạo Kích +5.0% / Tăng 10% sát thương AoE gây ra cho mục tiêu địch chịu debuff.',
                      'materials': 'None'},
                     {'name': 'Khóa Mở Rộng - Vũ Điệu Hỏa Anh Đào',
                      'level': 60,
                      'effect': 'Khi nhận Chỉ Lệnh Bổ Sung bằng kỹ năng chủ động Hoa Rơi Tung Bay, có thể di chuyển 6 '
                                'ô.\n'
                                'Hệ số sát thương của Dấu Anh Đào tăng 15%. Cứ mỗi 3 lần hiệu ứng Dấu Anh Đào được '
                                'kích hoạt (không tính lần kích hoạt bởi Tuyệt Kỹ), nhận 1 điểm Chỉ Số Nhiên Liệu, tối '
                                'đa 4 điểm mỗi lượt.\n'
                                'Mỗi khi hiệu ứng Dẫn Nhiệt được kích hoạt, sát thương bản thân gây ra tăng vĩnh viễn '
                                '15% và Sát Thương Bạo Kích tăng vĩnh viễn 15%, cộng dồn tối đa 75%.',
                      'materials': '3\n\n\n15000'}]},
 'sextans': {'name': 'Sextans',
             'skills': [{'name': 'Mộng Cảnh Giảo Sát',
                         'tags': ['Đánh Thường', 'Chuẩn Xác', 'Cận Chiến'],
                         'description': 'Chọn 1 mục tiêu trong phạm vi 1 ô, gây cho mục tiêu ST Vật Lý cận chiến bằng '
                                        '80% Tấn Công.'},
                        {'name': 'Cầu Nguyện Thánh Địa',
                         'tags': ['Chủ Động', 'Phạm Vi', 'Cận Chiến'],
                         'description': 'Chọn 1 hướng, gây ST Dẫn Điện cận chiến AoE tương đương 90% Tấn Công cho tất '
                                        'cả kẻ địch trong khu vực 3x9 phía trước theo hướng đã chọn và gắn '
                                        '<color=#3487e0>Huyết Hôn</color>. Hệ số sát thương của kỹ năng này tăng 10% '
                                        'dựa theo số tầng <color=#3487e0>Đông Tụ</color> mà Sextans sở hữu. Hồi phục '
                                        'HP tương đương 90% Tấn Công cho tất cả đồng minh trong khu vực. Sau khi dùng '
                                        'kỹ năng, Sextans nhận 6 ô Di Chuyển Thêm và có thể sử dụng kỹ năng chủ động '
                                        'Chuông Tang Vong Hồn.'},
                        {'name': 'Chuông Tang Vong Hồn',
                         'tags': ['Chủ Động', 'Phạm Vi', 'Cận Chiến'],
                         'description': 'Chọn 1 hướng, gây ST Dẫn Điện cận chiến AoE tương đương 90% Tấn Công cho tất '
                                        'cả kẻ địch trong khu vực 3x9 phía trước theo hướng đã chọn và tạo các ô địa '
                                        'hình <color=#3487e0>Điện Áp</color> trong 3 lượt. Hệ số sát thương của kỹ '
                                        'năng này tăng 10% dựa theo số tầng <color=#3487e0>Đông Tụ</color> mà Sextans '
                                        'sở hữu. Hồi phục HP tương đương 90% Tấn Công cho tất cả đồng minh trong khu '
                                        'vực và hóa giải 1 debuff của họ. Nếu mục tiêu địch đang chịu '
                                        '<color=#3487e0>Huyết Hôn</color>, kỹ năng này gây thêm 1 lần ST Dẫn Điện cận '
                                        'chiến với hệ số tương đương sau khi thi triển. Sextans nhận '
                                        '<color=#3487e0>Đông Tụ</color> và xóa <color=#3487e0>Huyết Hôn</color> của '
                                        'mục tiêu. Nhận thêm số tầng <color=#3487e0>Đông Tụ</color> dựa theo cấp bậc '
                                        'của mục tiêu (Thường, Tinh Anh, Boss).'},
                        {'name': 'Khúc Vịnh Đêm Tối',
                         'tags': ['Tuyệt Kỹ', 'Phạm Vi', 'Cận Chiến', 'Ô Địa Hình', 'Suy Yếu', 'Cường Hóa'],
                         'description': 'Chọn 1 ô trong khu vực hình chữ thập 4-8 ô, đáp xuống ô đã chọn và gây ST Dẫn '
                                        'Điện cận chiến AoE bằng 120% Tấn Công cho tất cả mục tiêu địch trên đường đi, '
                                        'đồng thời gắn <color=#3487e0>Huyết Hôn</color> lên chúng. Tạo các ô địa hình '
                                        '<color=#3487e0>Điện Áp</color> trong 3 lượt. Hệ số sát thương của kỹ năng này '
                                        'tăng 10% dựa theo số tầng <color=#3487e0>Đông Tụ</color> mà Sextans sở hữu. '
                                        'Trước khi kỹ năng có hiệu lực, gắn <color=#3487e0>Xé Rách</color> lên các mục '
                                        'tiêu địch trong khu vực hiệu lực trong 2 lượt; gắn <color=#3487e0>Dấu Ấn '
                                        'Thánh Huyết</color> lên tất cả đồng minh trong khu vực trong 2 lượt. Sau kỹ '
                                        'năng, nhận 6 ô Di Chuyển Thêm và có thể sử dụng kỹ năng chủ động Chuông Tang '
                                        'Vong Hồn.'},
                        {'name': 'Khúc An Hồn',
                         'tags': ['Bị Động', 'Cường Hóa'],
                         'description': 'Sát thương gây ra tăng 10% cho tất cả các Doll sử dụng Kiếm. Tầm Di Chuyển '
                                        'tăng 1 ô cho tất cả Doll thuộc tính Dẫn Điện và tất cả Doll sử dụng Kiếm (chỉ '
                                        'tính 1 lần khi thỏa mãn đồng thời nhiều điều kiện). Khi 1 đơn vị địch tử trận '
                                        'hoặc rơi vào trạng thái Sụp Đổ Ổn Định, Sextans nhận 1 tầng '
                                        '<color=#3487e0>Đông Tụ</color>. Dựa theo cấp bậc của đơn vị địch, Sextans '
                                        'nhận thêm các tầng <color=#3487e0>Đông Tụ</color>. Khi đồng minh (không bao '
                                        'gồm Sextans) tấn công bằng Kiếm, tiêu hao 1 điểm Chỉ Số Nhiên Liệu để phát '
                                        'động <color=#3487e0>Huyết Huy Hiệu</color>. Khi bắt đầu lượt của Sextans, nếu '
                                        'Chỉ Số Nhiên Liệu chưa đầy, hồi phục đầy đủ. Gắn <color=#3487e0>Huy Hiệu Đỏ '
                                        'Thẫm</color> lên kẻ địch kết thúc hành động trên ô địa hình thuộc tính Dẫn '
                                        'Điện.'}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Chuông Tang Vong Hồn',
                                'effect': 'Nếu kỹ năng đánh trúng mục tiêu địch, bản thân thi triển '
                                          '<color=#3487e0>Huyết Huy Hiệu</color> lên mục tiêu đó <color=#f26c1c>1 '
                                          'lần</color> và nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Sau '
                                          'khi dùng kỹ năng, bản thân nhận <color=#f26c1c>2 tầng</color> '
                                          '<color=#3487e0>Đông Tụ</color>.'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Khúc Vịnh Đêm Tối',
                                'effect': 'Độ rộng khu vực kỹ năng tăng thêm <color=#f26c1c>2 ô</color>. Cường hóa '
                                          'hiệu ứng <color=#3487e0>Dấu Ấn Thánh Huyết</color>, ST Ổn Định và lượng Chỉ '
                                          'Số Ổn Định bị bỏ qua tăng thêm <color=#f26c1c>5 điểm</color>; khi gây '
                                          '<color=#b359f2>ST Dẫn Điện</color> hoặc ST Cận Chiến, sát thương tăng thêm '
                                          '<color=#f26c1c>5%</color> cho mỗi tầng <color=#3487e0>Đông Tụ</color> (chỉ '
                                          'áp dụng 1 lần khi thỏa mãn nhiều điều kiện).'},
                               {'tier': 3,
                                'level': 2,
                                'skill': 'Khúc An Hồn',
                                'effect': 'Tất cả Doll thuộc tính <color=#b359f2>Dẫn Điện</color> và tất cả Doll sử '
                                          'dụng Kiếm được tăng <color=#f26c1c>2 ô</color> di chuyển (chỉ áp dụng 1 lần '
                                          'khi thỏa mãn nhiều điều kiện), đồng thời bỏ qua cản trở của kẻ địch. Cường '
                                          'hóa hiệu ứng <color=#3487e0>Đông Tụ</color>: Giới hạn tối đa chuyển đổi Tỷ '
                                          'Lệ Bạo Kích dư thừa thành Tấn Công, lượng trị liệu và ST Bạo Kích nâng lên '
                                          '<color=#f26c1c>45%</color>. Cường hóa hiệu ứng <color=#3487e0>Huyết Huy '
                                          'Hiệu</color>: Với mỗi tầng <color=#3487e0>Đông Tụ</color>, hệ số sát thương '
                                          'tăng lên <color=#f26c1c>4%</color>. Cường hóa hiệu ứng <color=#3487e0>Huy '
                                          'Hiệu Đỏ Thẫm</color>: Sát thương cận chiến phải gánh chịu tăng lên '
                                          '<color=#f26c1c>10%</color>.'},
                               {'tier': 4,
                                'level': 3,
                                'skill': 'Khúc Vịnh Đêm Tối',
                                'effect': 'Trước khi dùng kỹ năng, áp dụng <color=#3487e0>Dẫn Điện Tăng II</color> cho '
                                          'tất cả đơn vị đồng minh trong <color=#f26c1c>2 hiệp</color>. Sau khi dùng '
                                          'kỹ năng, nhận <color=#3487e0>Ngụy Trang</color> trong <color=#f26c1c>2 '
                                          'hiệp</color>.'},
                               {'tier': 5,
                                'level': 3,
                                'skill': 'Chuông Tang Vong Hồn',
                                'effect': 'Hệ số sát thương và hồi máu tăng thêm <color=#f26c1c>30%</color>; giải trừ '
                                          'thêm <color=#f26c1c>1</color> Debuff; <color=#3487e0>Huyết Hôn</color> '
                                          'không còn bị xóa bỏ.'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Khúc An Hồn',
                                'effect': 'Khi bắt đầu chiến đấu, nhận <color=#f26c1c>5 tầng</color> '
                                          '<color=#3487e0>Đông Tụ</color>, và giới hạn Tỷ Lệ Bạo Kích cho '
                                          '<color=#3487e0>Đông Tụ</color> tăng lên <color=#f26c1c>75%</color>. Hệ số '
                                          'sát thương của <color=#3487e0>Huyết Huy Hiệu</color> tăng lên '
                                          '<color=#f26c1c>90%</color>, bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của '
                                          'mục tiêu khi gây sát thương. Không còn tiêu hao Chỉ Số Nhiên Liệu. Khi đầy '
                                          'Chỉ Số Nhiên Liệu, tất cả đơn vị đồng minh tăng <color=#f26c1c>15%</color> '
                                          'sát thương cận chiến gây ra.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Duyên Phận Giao Ước',
                       'level': 20,
                       'effect': 'Khi bắt đầu trận chiến, Sextans nhận 1 tầng Đông Tụ dựa theo số lượng Doll thuộc '
                                 'tính Dẫn Điện hoặc Doll dùng Kiếm trên sân (chỉ tính 1 lần khi thỏa mãn nhiều điều '
                                 'kiện).',
                       'materials': '3\n\n\n3000'},
                      {'name': 'Khóa Cố Định 2 - Bia Văn Câm Lặng',
                       'level': 20,
                       'effect': 'Trước khi đồng minh có Dấu Ấn Thánh Huyết sử dụng đòn tấn công chủ động, gắn Phòng '
                                 'Thủ Giảm II lên mục tiêu trong 2 lượt.',
                       'materials': '3\n\n\n3000'},
                      {'name': 'Khóa Cố Định 3 - Hiệu Chỉnh Đồng Hồ',
                       'level': 30,
                       'effect': 'Trước khi Huyết Huy Hiệu gây sát thương, hóa giải 1 buff của mục tiêu.',
                       'materials': '3\n\n\n8000'},
                      {'name': 'Khóa Cố Định 4 - Lời Thề Tàn Phai',
                       'level': 30,
                       'effect': 'Kẻ địch trong trạng thái Sụp Đổ Ổn Định chịu thêm 7% sát thương.',
                       'materials': '3\n\n\n8000'},
                      {'name': 'Khóa Cố Định 5 - Màn Chắn Nhung Đỏ',
                       'level': 40,
                       'effect': 'Sau khi một đơn vị đồng minh (ngoại trừ Sextans) tấn công bằng Kiếm, tạo ô địa hình '
                                 'Điện Áp trong bán kính 1 ô xung quanh mục tiêu.',
                       'materials': '3\n\n\n12000'},
                      {'name': 'Khóa Cố Định 6 - Lông Vũ Thiên Nga',
                       'level': 40,
                       'effect': 'Tăng 1 điểm ST Ổn Định gây ra bởi tất cả đơn vị đồng minh.',
                       'materials': '3\n\n\n12000'},
                      {'name': 'Khóa Tương Thích - Tiếng Vang Tĩnh Lặng',
                       'level': '-',
                       'effect': 'Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%',
                       'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                      {'name': 'Khóa Chung - Thánh Ấn Trong Tay',
                       'level': 40,
                       'effect': 'ST Bạo Kích +5.0% / Sát thương cận chiến gây ra tăng 10%.',
                       'materials': 'None'}]},
 'zhaohui': {'name': 'Zhaohui',
             'skills': [{'name': 'Gió Xuyên Rừng',
                         'tags': ['Đánh Thường', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch trong phạm vi 6 ô, gây ST Vật Lý tương đương 80% Tấn '
                                        'Công.'},
                        {'name': 'Dây Đoạt Ảnh',
                         'tags': ['Chủ Động', 'Phạm Vi', 'Khống Chế'],
                         'description': 'Chọn 1 hướng, gây ST Vật Lý AoE tương đương 110% Tấn Công cho tất cả mục tiêu '
                                        'địch trong phạm vi 4 ô theo hướng đã chọn. Nếu mục tiêu sở hữu bất kỳ debuff '
                                        'loại Hóa Lỏng nào, gắn <color=#3487e0>Choáng</color> lên mục tiêu trong 1 '
                                        'lượt. Zhaohui nhận 1 điểm Chỉ Số Nhiên Liệu cho mỗi mục tiêu đánh trúng, đồng '
                                        'thời tăng 10% Tỷ Lệ Bạo Kích cho đòn tấn công chủ động tiếp theo.'},
                        {'name': 'Định Phong Ba',
                         'tags': ['Chủ Động', 'Phạm Vi', 'Triệu Hồi', 'Suy Yếu'],
                         'description': 'Chọn 1 ô trống trong phạm vi 6 ô và triệu hồi 1 Mũi Tên Tĩnh Lặng, gây ST Hóa '
                                        'Lỏng AoE tương đương 90% Tấn Công cho tất cả kẻ địch trong phạm vi 2 ô xung '
                                        'quanh Mũi Tên Tĩnh Lặng, đồng thời gắn <color=#3487e0>Định Tức</color> trong '
                                        '2 lượt.'},
                        {'name': 'Bước Nhảy Thanh Minh',
                         'tags': ['Tuyệt Kỹ', 'Chuẩn Xác', 'Suy Yếu'],
                         'description': 'Chọn Mũi Tên Tĩnh Lặng bất kỳ trong phạm vi 9 ô và đáp xuống một ô trong phạm '
                                        'vi 2 ô xung quanh mũi tên đó. Gây ST Hóa Lỏng tương đương 160% Tấn Công lên '
                                        'mục tiêu địch gần nhất trong phạm vi 6 ô và gắn <color=#3487e0>Đình '
                                        'Trệ</color> trong 2 lượt.'},
                        {'name': 'Thập Diện Mai Phục',
                         'tags': ['Bị Động', 'Hỗ Trợ', 'Suy Yếu'],
                         'description': 'Khi kết thúc hành động, Zhaohui có thể chọn Mũi Tên Tĩnh Lặng bất kỳ trong '
                                        'phạm vi 9 ô và đáp xuống một ô trong phạm vi 2 ô xung quanh mũi tên đó, nhận '
                                        '1 điểm Chỉ Số Nhiên Liệu.\n'
                                        '\n'
                                        'Khi kẻ địch trong tầm đánh chịu sát thương chuẩn xác từ một đơn vị đồng minh, '
                                        'Zhaohui phát động <color=#3487e0>Hành Động Chi Viện</color> 1 lần, gây ST Hóa '
                                        'Lỏng tương đương 80% Tấn Công, 2 điểm ST Ổn Định và gắn <color=#3487e0>Ẩm '
                                        'Ướt</color> trong 2 lượt lên đơn vị địch. Hiệu quả này có thể kích hoạt tối '
                                        'đa 1 lần mỗi lượt.'}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Thập Diện Mai Phục',
                                'effect': 'Khi bắt đầu trận chiến, Zhaohui triệu hồi <color=#f26c1c>1</color> Mũi Tên '
                                          'Tĩnh Lặng trên ô xung quanh. Số lần kích hoạt tối đa của Hành Động Chi Viện '
                                          'tăng thêm <color=#f26c1c>1 lần</color>. Khi có bất kỳ Mũi Tên Tĩnh Lặng nào '
                                          'trên sân, sát thương gây ra của Zhaohui tăng thêm '
                                          '<color=#f26c1c>10%</color>.\n'
                                          '\n'
                                          '(Mặc định được triệu hồi ở ô bên phải Zhaohui. Nếu ô đó không hợp lệ, sẽ '
                                          'được triệu hồi ở ô bên trái. Nếu vẫn không hợp lệ, sẽ được triệu hồi ở ô '
                                          'phía sau)'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Định Phong Ba',
                                'effect': 'Cự ly thi triển tăng thêm <color=#f26c1c>3 ô</color>, và phạm vi hiệu lực '
                                          'tăng thêm <color=#f26c1c>1 ô</color>. ST Ổn Định tăng thêm <color=#f26c1c>2 '
                                          'điểm</color>, và sát thương gây ra tăng lên <color=#f26c1c>110%</color> Tấn '
                                          'Công.'},
                               {'tier': 3,
                                'level': 2,
                                'skill': 'Bước Nhảy Thanh Minh',
                                'effect': 'ST Ổn Định gây ra tăng thêm <color=#f26c1c>2 điểm</color>. Áp dụng '
                                          '<color=#3487e0>Định Tức</color> lên mục tiêu trong <color=#f26c1c>2 '
                                          'hiệp</color>. Di dời vị trí cùng với tất cả đơn vị đồng minh trong phạm vi '
                                          '<color=#f26c1c>2 ô</color> quanh bản thân.'},
                               {'tier': 4,
                                'level': 2,
                                'skill': 'Dây Đoạt Ảnh',
                                'effect': 'Khi áp dụng <color=#3487e0>Choáng</color>, không còn yêu cầu mục tiêu phải '
                                          'có bất kỳ Debuff thuộc tính Hóa Lỏng nào. Cứ mỗi mục tiêu đánh trúng, '
                                          'Zhaohui hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số Ổn Định. Tỷ lệ bạo '
                                          'kích của đòn tấn công chủ động tiếp theo tăng thêm '
                                          '<color=#f26c1c>20%</color>. Ngoài ra, cứ mỗi mục tiêu đánh trúng, tỷ lệ bạo '
                                          'kích tăng thêm <color=#f26c1c>5%</color>.'},
                               {'tier': 5,
                                'level': 3,
                                'skill': 'Thập Diện Mai Phục',
                                'effect': 'Khi kết thúc hành động, Mũi Tên Tĩnh Lặng giờ đây có thể được chọn từ bất '
                                          'kỳ vị trí nào trên toàn sân. Số lần kích hoạt tối đa của Hành Động Chi Viện '
                                          'tăng thêm <color=#f26c1c>1 lần</color>. Trước khi tấn công, nếu mục tiêu có '
                                          'từ <color=#f26c1c>2</color> Debuff trở lên, sát thương gây ra cho mục tiêu '
                                          'đó tăng thêm <color=#f26c1c>20%</color>.'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Bước Nhảy Thanh Minh',
                                'effect': 'ST Bạo Kích của đòn tấn công này tăng thêm <color=#f26c1c>30%</color>, và '
                                          'sát thương gây ra tăng lên <color=#f26c1c>180%</color> Tấn Công. Sau khi sử '
                                          'dụng kỹ năng này, Tấn Công của Zhaohui tăng thêm '
                                          '<color=#f26c1c>10%</color>, tối đa cộng dồn <color=#f26c1c>3 '
                                          'tầng</color>.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Điểm Yếu Lộ Rõ',
                       'level': 20,
                       'effect': 'Tăng 10% sát thương gây ra đối với các mục tiêu đang chịu debuff thuộc tính Hóa '
                                 'Lỏng.',
                       'materials': '3\n\n\n3000'},
                      {'name': 'Khóa Cố Định 2 - Căm Ghét Tội Ác',
                       'level': 20,
                       'effect': 'Khi kỹ năng chủ động Dây Đoạt Ảnh chỉ đánh trúng 1 mục tiêu, gây thêm 1 lần sát '
                                 'thương cố định bằng 10% Tấn Công và gắn Ẩm Ướt trong 2 lượt.',
                       'materials': '3\n\n\n3000'},
                      {'name': 'Khóa Cố Định 3 - Thời Gian Đệm',
                       'level': 30,
                       'effect': 'Nếu có bất kỳ Mũi Tên Tĩnh Lặng nào trên sân, hồi phục 10% HP của Zhaohui khi kết '
                                 'thúc hành động.',
                       'materials': '3\n\n\n8000'},
                      {'name': 'Khóa Cố Định 4 - Ánh Sáng Công Lý',
                       'level': 30,
                       'effect': 'Khi sử dụng kỹ năng chủ động Định Phong Ba, Zhaohui nhận 1 tầng Lá Chắn Tốc Độ và '
                                 'đẩy lùi mục tiêu 2 ô.',
                       'materials': '3\n\n\n8000'},
                      {'name': 'Khóa Cố Định 5 - Tiết Tấu Ngưng Đọng',
                       'level': 40,
                       'effect': 'Nếu Zhaohui ở trong phạm vi 2 ô của bất kỳ Mũi Tên Tĩnh Lặng nào, giảm 1 điểm ST Ổn '
                                 'Định phải chịu và giảm 30% ST AoE phải chịu.',
                       'materials': '3\n\n\n12000'},
                      {'name': 'Khóa Cố Định 6 - Hài Hước Khô Khan',
                       'level': 40,
                       'effect': 'Trước khi thực hiện Hành Động Chi Viện, hóa giải 2 buff của mục tiêu.',
                       'materials': '3\n\n\n12000'},
                      {'name': 'Khóa Tương Thích',
                       'level': 40,
                       'effect': 'Tấn Công +3%, HP +3%, ST Bạo Kích +3%',
                       'materials': 'Mở khóa khi Độ Tương Thích đạt Lv.5'},
                      {'name': 'Khóa Chung - Âm Vực Kèn Suona',
                       'level': 40,
                       'effect': 'TL Bạo Kích +5.0% / Khi bắt đầu lượt, tăng 10% Sát Thương Bạo Kích của đòn tấn công '
                                 'chủ động tiếp theo.',
                       'materials': 'None'},
                      {'name': 'Khóa Mở Rộng - Hình Thái Hoàn Mỹ',
                       'level': 60,
                       'effect': 'Tăng 45% ST Hóa Lỏng gây ra cho mục tiêu trong trạng thái Sụp Đổ Ổn Định.\n'
                                 '\n'
                                 'Sau khi dịch chuyển bằng Thập Diện Mai Phục, gây ST Hóa Lỏng bằng 80% Tấn Công và 2 '
                                 'điểm ST Ổn Định lên mục tiêu địch gần nhất trong tầm đánh, gắn Ẩm Ướt trong 2 lượt '
                                 'và tăng 1 điểm Chỉ Số Nhiên Liệu.',
                       'materials': '3\n\n\n15000'}]}}
