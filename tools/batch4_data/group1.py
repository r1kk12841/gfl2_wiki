"""
Auto-synced batch data.
"""

GROUP_1_DATA = {'florence': {'name': 'Florence',
              'en_name': 'Florence',
              'class': 'Hỗ Trợ',
              'phase': 'Hóa Lỏng',
              'rarity': 'Tinh Nhuệ',
              'weapon_type': 'Súng Lục',
              'ammo_type': 'Đạn Nhẹ',
              'signature_weapon': 'Giác Quan Nở Rộ',
              'weakness': 'Dẫn Điện',
              'server': 'global',
              'skills': [{'name': 'Tiêm Cưỡng Chế',
                          'tags': ['Đánh Thường', 'Chuẩn Xác'],
                          'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, '
                                         'gây ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                         {'name': 'Chăm Sóc Đặc Biệt',
                          'tags': ['Chủ Động', 'Trị Liệu'],
                          'description': 'Chọn 1 đơn vị đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>. '
                                         'Hồi phục lượng HP bằng <color=#f26c1c>100%</color> Tấn Công và '
                                         '<color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định, đồng thời giải trừ '
                                         '<color=#f26c1c>1</color> Debuff. Florence nhận <color=#f26c1c>1 điểm</color> '
                                         'Chỉ Số Nhiên Liệu.'},
                         {'name': 'Kích Hoạt Khoái Cảm',
                          'tags': ['Chủ Động', 'Cường Hóa'],
                          'description': 'Chọn 1 đồng minh <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, áp '
                                         'dụng <color=#3487e0>Thuốc Phấn Khởi</color> trong <color=#f26c1c>2 '
                                         'hiệp</color>. Florence nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên '
                                         'Liệu.'},
                         {'name': 'Ảo Giác Khổ Dâm',
                          'tags': ['Tuyệt Kỹ', 'AoE', 'Triệu Hồi', 'Khống Chế'],
                          'description': 'Triệu hồi Arios tại 1 ô chỉ định trong phạm vi 6 ô, đồng thời gây ST Hóa '
                                         'Lỏng AoE bằng <color=#f26c1c>100%</color> Tấn Công lên toàn bộ kẻ địch trong '
                                         'phạm vi 3×3 ô quanh ô đó và áp dụng <color=#3487e0>Chất Nhiễu Loạn</color> '
                                         'trong <color=#f26c1c>2 hiệp</color>.'},
                         {'name': 'Chuẩn Bị Phẫu Thuật',
                          'tags': ['Bị Động', 'Hỗ Trợ'],
                          'description': 'Khi kết thúc hành động, hồi phục HP bằng <color=#f26c1c>30%</color> Tấn Công '
                                         'cho đồng minh có lượng HP thấp nhất trong phạm vi 6 ô. Khi đồng minh nhận '
                                         'trị liệu từ Florence, họ nhận thêm <color=#3487e0>Adrenaline</color> trong '
                                         '<color=#f26c1c>1 hiệp</color>.'}],
              'summons': [{'name': 'Arios',
                           'type': 'Vật Triệu Hồi Vật Lý',
                           'description': 'Trợ thủ hộ vệ có khả năng khiêu khích đối phương, chịu sát thương thay cho '
                                          'Florence và thực hiện Phản Kích khi bản thân hoặc Florence bị tấn công.',
                           'stats': {'hp': '120% HP ban đầu của Florence',
                                     'atk': '100% Tấn Công ban đầu của Florence',
                                     'def': '120% Phòng Thủ ban đầu của Florence'},
                           'skills': [{'name': 'Gây Mê Chuẩn Xác',
                                       'tags': ['Chủ Động', 'Chuẩn Xác', 'Khống Chế', 'Suy Yếu'],
                                       'description': 'Áp dụng Chất Nhiễu Loạn lên kẻ địch gần Florence nhất trong 2 '
                                                      'hiệp, gây ST Hóa Lỏng bằng 80% Tấn Công và áp dụng Khiêu Khích '
                                                      'trong 1 hiệp.'},
                                      {'name': 'Trợ Thủ Đắc Lực',
                                       'tags': ['Bị Động', 'Phản Kích'],
                                       'description': 'Khi Florence nhận sát thương, Arios sẽ gánh chịu toàn bộ sát '
                                                      'thương thay cho cô. Khi Arios hoặc Florence nhận sát thương, '
                                                      'Arios thực hiện Phản Kích gây ST Hóa Lỏng bằng 80% Tấn Công '
                                                      '(tối đa 2 lần mỗi hiệp).'}]}],
              'fortification': [{'tier': 1,
                                 'level': 2,
                                 'skill': 'Chuẩn Bị Phẫu Thuật',
                                 'effect': 'Giảm tiêu hao Chỉ Số Nhiên Liệu đi <color=#f26c1c>1 điểm</color>.\n'
                                           '\n'
                                           'Tăng số lần Phản Kích thông qua kỹ năng nội tại của Arios thêm '
                                           '<color=#f26c1c>2 lần</color>.'},
                                {'tier': 2,
                                 'level': 2,
                                 'skill': 'Ảo Giác Khổ Dâm',
                                 'effect': 'Cường hóa hiệu ứng <color=#3487e0>Chất Nhiễu Loạn</color>: Tăng '
                                           '<color=#f26c1c>15%</color> <color=#2caadb>ST Hóa Lỏng</color> phải chịu.\n'
                                           '\n'
                                           'Bổ sung hiệu ứng mới - Gây <color=#e08834>ST Vật Lý</color> lên toàn bộ '
                                           'đơn vị khi bắt đầu hiệp.'},
                                {'tier': 3,
                                 'level': 2,
                                 'skill': 'Kích Hoạt Khoái Cảm',
                                 'effect': 'Tăng thời gian duy trì của <color=#3487e0>Thuốc Phấn Khởi</color> thêm '
                                           '<color=#f26c1c>1 hiệp</color> (Thời lượng giảm vào cuối hiệp hiện tại).\n'
                                           '\n'
                                           'Bổ sung hiệu ứng mới - Khi kết thúc hành động, nếu HP dưới '
                                           '<color=#f26c1c>30%</color>, hồi phục lượng HP bằng '
                                           '<color=#f26c1c>100%</color> Tấn Công của Florence. Hiệu ứng này chỉ có thể '
                                           'kích hoạt 1 lần trong suốt thời gian duy trì của Thuốc Phấn Khởi.'},
                                {'tier': 4,
                                 'level': 3,
                                 'skill': 'Ảo Giác Khổ Dâm',
                                 'effect': 'Tăng hệ số sát thương thêm <color=#f26c1c>20%</color>. Nếu Arios đang có '
                                           'mặt trên sân, hồi phục cho Florence lượng HP bằng '
                                           '<color=#f26c1c>100%</color> Tấn Công và áp dụng '
                                           '<color=#3487e0>Adrenaline</color> trong <color=#f26c1c>1 hiệp</color> '
                                           '(Thời lượng giảm vào cuối hiệp hiện tại).'},
                                {'tier': 5,
                                 'level': 3,
                                 'skill': 'Kích Hoạt Khoái Cảm',
                                 'effect': 'Giải trừ thêm <color=#3487e0>Dẫn Dụ</color> và '
                                           '<color=#3487e0>Choáng</color>. Kỹ năng này cũng được áp dụng cho Arios.'},
                                {'tier': 6,
                                 'level': 3,
                                 'skill': 'Chuẩn Bị Phẫu Thuật',
                                 'effect': 'Arios giảm <color=#f26c1c>30%</color> sát thương phải gánh chịu.\n'
                                           '\n'
                                           'Cường hóa hiệu ứng Rung Chuyển Tuyệt Vọng: Tăng Tấn Công thêm '
                                           '<color=#f26c1c>35%</color>, tăng gấp đôi hệ số sát thương của Phản Kích, '
                                           'và hồi phục lượng HP bằng <color=#f26c1c>30%</color> sát thương gây ra sau '
                                           'khi gây sát thương.'}],
              'keys': [{'name': 'Khóa Cố Định 1 - Kích Thích Chí Mạng',
                        'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                       {'name': 'Khóa Cố Định 2 - Tự Tận Hưởng',
                        'effect': 'Khi trị liệu cho đồng minh, bản thân cũng hồi phục lượng HP bằng '
                                  '<color=#f26c1c>30%</color> lượng trị liệu đó.'},
                       {'name': 'Khóa Cố Định 3 - Tăng Cường Độ Nhạy',
                        'effect': 'Trước khi tấn công chủ động, áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên '
                                  'mục tiêu trong <color=#f26c1c>2 hiệp</color>.'},
                       {'name': 'Khóa Cố Định 4 - Phần Thưởng Phản Kích',
                        'effect': 'Khi Arios thực hiện Phản Kích, hồi phục <color=#f26c1c>1 điểm</color> Chỉ Số Ổn '
                                  'Định cho Florence.'},
                       {'name': 'Khóa Cố Định 5 - Ham Muốn Trói Buộc',
                        'effect': 'Mục tiêu mang Chất Nhiễu Loạn bị giảm thêm <color=#f26c1c>15%</color> Tấn Công.'},
                       {'name': 'Khóa Cố Định 6 - Cám Dỗ Ngọt Ngào',
                        'effect': 'Khi dùng Ảo Giác Khổ Dâm, giải trừ <color=#f26c1c>2</color> Buff trên toàn bộ kẻ '
                                  'địch trúng đòn.'},
                       {'name': 'Khóa Tương Thích - Giác Quan Nhạy Bén',
                        'effect': 'Tấn Công +3%, HP +3%, Phòng Thủ +3%'},
                       {'name': 'Khóa Chung - Mệnh Lệnh Của Chủ Nhân',
                        'effect': 'HP +5.0% / Khi trị liệu cho mục tiêu có HP dưới 50%, lượng trị liệu tăng '
                                  '<color=#f26c1c>15%</color>.'},
                       {'name': 'Khóa Mở Rộng - Kẻ Tìm Kiếm Kích Thích',
                        'effect': 'Khi Arios có mặt trên sân, sát thương Florence gánh chịu giảm '
                                  '<color=#f26c1c>30%</color>. Arios tăng thêm <color=#f26c1c>50%</color> sát thương '
                                  'Phản Kích.'}]},
 'helen': {'name': 'Helen',
           'en_name': 'Helen',
           'class': 'Hộ Vệ',
           'phase': 'Băng Kết',
           'rarity': 'Tinh Nhuệ',
           'weapon_type': 'Súng Shotgun',
           'ammo_type': 'Đạn Shotgun',
           'signature_weapon': 'Trọng Khiên Băng Giá',
           'weakness': 'Đốt Cháy',
           'server': 'global',
           'skills': [{'name': 'Lính Canh',
                       'tags': ['Đánh Thường', 'Chuẩn Xác'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 5 ô xung quanh</color>, gây '
                                      'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                      {'name': 'Chỉ Lệnh Khiên Chắn',
                       'tags': ['Chủ Động', 'Cường Hóa'],
                       'description': 'Chọn 1 đồng minh trong phạm vi 5 ô, bản thân và mục tiêu nhận '
                                      '<color=#3487e0>Yểm Hộ</color> và chia sẻ sát thương trong <color=#f26c1c>2 '
                                      'hiệp</color>. Helen nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                      {'name': 'Đột Kích Khiên Chắn',
                       'tags': ['Chủ Động', 'Cường Hóa', 'Ô Địa Hình', 'Phòng Ngự'],
                       'description': 'Lao về phía trước tới 4 ô, gây ST Băng Kết AoE bằng <color=#f26c1c>90%</color> '
                                      'Tấn Công lên toàn bộ kẻ địch trên đường đi và tạo ô địa hình '
                                      '<color=#3487e0>Băng Giá</color> trong <color=#f26c1c>2 hiệp</color>. Bản thân '
                                      'nhận <color=#3487e0>Khiên</color> hấp thu sát thương bằng '
                                      '<color=#f26c1c>30%</color> HP tối đa.'},
                      {'name': 'Chiến Kỳ Lính Canh',
                       'tags': ['Tuyệt Kỹ', 'Cường Hóa'],
                       'description': 'Cắm cờ hiệu chiến trận, áp dụng <color=#3487e0>Phòng Ngự Ban Đầu</color> và '
                                      '<color=#3487e0>Vinh Quang Cho Mẹ</color> lên toàn bộ đồng minh trong bán kính 6 '
                                      'ô trong <color=#f26c1c>2 hiệp</color>. Helen nhận <color=#3487e0>Chỉ Lệnh Bổ '
                                      'Sung</color>.'},
                      {'name': 'Valkyrie Bất Khuất',
                       'tags': ['Bị Động', 'Phòng Ngự'],
                       'description': 'Helen giảm <color=#f26c1c>20%</color> sát thương phải gánh chịu. Khi đồng minh '
                                      'liền kề bị tấn công, Helen kích hoạt <color=#3487e0>Yểm Hộ</color> để gánh chịu '
                                      'sát thương thay họ.'}],
           'fortification': [{'tier': 1,
                              'level': 2,
                              'skill': 'Đột Kích Khiên Chắn',
                              'effect': 'Độ rộng phạm vi tăng thêm <color=#f26c1c>2 ô</color>, giải trừ thêm '
                                        '<color=#f26c1c>2</color> Debuff, và áp dụng <color=#3487e0>ST Bạo Kích Tăng '
                                        'II</color> trong <color=#f26c1c>2 hiệp</color>.'},
                             {'tier': 2,
                              'level': 2,
                              'skill': 'Valkyrie Bất Khuất',
                              'effect': 'Tăng Chỉ Số Ổn Định lên <color=#f26c1c>16 điểm</color>, giảm '
                                        '<color=#f26c1c>50%</color> sát thương phải gánh chịu. Mỗi khi chịu sát '
                                        'thương, nhận thêm <color=#f26c1c>1 tầng</color> <color=#3487e0>Lưỡi Đao Vượt '
                                        'Mức</color>. Trước khi thực hiện đòn đánh thường, tăng Tấn Công bằng '
                                        '<color=#f26c1c>30%</color> Phòng Thủ của bản thân.'},
                             {'tier': 3,
                              'level': 2,
                              'skill': 'Chiến Kỳ Lính Canh',
                              'effect': 'Thời gian hồi chiêu giảm <color=#f26c1c>2 hiệp</color>. Nhận '
                                        '<color=#3487e0>Tấn Công Tăng III</color> và <color=#3487e0>Phòng Thủ Tăng '
                                        'III</color> trong <color=#f26c1c>2 hiệp</color>. Nhận <color=#f26c1c>10 '
                                        'tầng</color> <color=#3487e0>Lưỡi Đao Vượt Mức</color>. Giảm thời gian hồi '
                                        'chiêu Tuyệt kỹ của các Doll thuộc tính <color=#42cce0>Băng Kết</color> đi '
                                        '<color=#f26c1c>2 hiệp</color>.'},
                             {'tier': 4,
                              'level': 2,
                              'skill': 'Chỉ Lệnh Khiên Chắn',
                              'effect': 'Giải trừ thêm <color=#3487e0>Dẫn Dụ</color> và <color=#3487e0>Choáng</color>. '
                                        'Nếu chịu sát thương chí tử trong khi chia sẻ sát thương, Helen sẽ không tử '
                                        'trận và hồi phục lượng HP bằng <color=#f26c1c>150%</color> Phòng Thủ của bản '
                                        'thân. Hiệu ứng này có thể kích hoạt tối đa 1 lần mỗi hiệp. Các đơn vị đồng '
                                        'minh có Khiên Chắn gây thêm <color=#f26c1c>30%</color> <color=#42cce0>ST Băng '
                                        'Kết</color>.'},
                             {'tier': 5,
                              'level': 3,
                              'skill': 'Đột Kích Khiên Chắn',
                              'effect': 'Với mỗi đơn vị đồng minh (ngoại trừ bản thân) trên đường di chuyển, hồi phục '
                                        'thêm <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định, đồng thời nhận số tầng '
                                        '<color=#3487e0>Lực Đẩy Băng Giá</color> tương ứng.'},
                             {'tier': 6,
                              'level': 3,
                              'skill': 'Valkyrie Bất Khuất',
                              'effect': 'Trước khi thực hiện đòn đánh thường, tăng Tấn Công của Helen bằng '
                                        '<color=#f26c1c>70%</color> Phòng Thủ của bản thân.\n'
                                        'Khi một đơn vị đồng minh chịu sát thương, nhận <color=#f26c1c>2 tầng</color> '
                                        '<color=#3487e0>Lưỡi Đao Vượt Mức</color>. Khi đang có <color=#3487e0>Lưỡi Đao '
                                        'Vượt Mức</color>, hệ số sát thương của đòn đánh thường tăng lên '
                                        '<color=#f26c1c>300%</color>.'}],
           'keys': [{'name': 'Khóa Cố Định 1 - Điệp Viên Hai Đầu',
                     'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                    {'name': 'Khóa Cố Định 2 - Hoa Nở Trong Băng',
                     'effect': 'Khi đứng trên ô địa hình Băng Giá, Phòng Thủ tăng thêm <color=#f26c1c>20%</color>.'},
                    {'name': 'Khóa Cố Định 3 - Ký Ức Chôn Giấu',
                     'effect': 'Khi Khiên bị phá hủy, gây ST Băng Kết AoE bằng <color=#f26c1c>50%</color> Tấn Công lên '
                               'toàn bộ kẻ địch xung quanh 2 ô.'},
                    {'name': 'Khóa Cố Định 4 - Quyết Tâm Người Hộ Vệ', 'effect': 'Miễn nhiễm với Choáng và Chạy Trốn.'},
                    {'name': 'Khóa Cố Định 5 - Vinh Quang Cho Mẹ',
                     'effect': 'Khi sở hữu Khiên, sát thương nhận vào giảm thêm <color=#f26c1c>15%</color>.'},
                    {'name': 'Khóa Cố Định 6 - Người Thực Thi Trật Tự',
                     'effect': 'Sau khi dùng Đột Kích Khiên Chắn, nhận <color=#f26c1c>3 ô</color> <color=#3487e0>Di '
                               'Chuyển Bổ Sung</color>.'},
                    {'name': 'Khóa Tương Thích - Chồi Non Mới Nhú', 'effect': 'Tấn Công +3%, HP +3%, Phòng Thủ +3%'},
                    {'name': 'Khóa Chung - Phòng Ngự Bất Động',
                     'effect': 'HP +5.0% / Khi bị tấn công, nếu còn Chỉ Số Ổn Định, sát thương nhận vào giảm '
                               '<color=#f26c1c>10%</color>.'}]},
 'lenna': {'name': 'Lenna',
           'en_name': 'Lenna',
           'class': 'Hỗ Trợ',
           'phase': 'Dẫn Điện',
           'rarity': 'Tinh Nhuệ',
           'weapon_type': 'Súng Tiểu Liên',
           'ammo_type': 'Đạn Nhẹ',
           'signature_weapon': 'Tiếng Gầm Sấm Sét',
           'weakness': 'Hóa Lỏng',
           'server': 'global',
           'skills': [{'name': 'Móng Vuốt Kích',
                       'tags': ['Đánh Thường', 'Chuẩn Xác'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                      'ST Dẫn Điện bằng <color=#f26c1c>80%</color> Tấn Công.'},
                      {'name': 'Nhảy Vọt Truy Kích',
                       'tags': ['Chủ Động', 'Chuẩn Xác'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                      'ST Dẫn Điện bằng <color=#f26c1c>120%</color> Tấn Công. Nếu mục tiêu có Dẫn '
                                      'Điện, gây thêm <color=#f26c1c>2 điểm</color> ST Ổn Định. Lenna nhận '
                                      '<color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                      {'name': 'Chiến Lược Săn Mồi',
                       'tags': ['Chủ Động', 'Cường Hóa'],
                       'description': 'Lenna nhận trạng thái <color=#3487e0>Ẩn Nấp</color> trong <color=#f26c1c>2 '
                                      'hiệp</color> và nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Đòn đánh kế tiếp '
                                      'tăng thêm <color=#f26c1c>30%</color> sát thương. Lenna nhận <color=#f26c1c>1 '
                                      'điểm</color> Chỉ Số Nhiên Liệu.'},
                      {'name': 'Tuyệt Diệt Hoang Dã',
                       'tags': ['Tuyệt Kỹ', 'Chuẩn Xác', 'Suy Yếu'],
                       'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                      'ST Dẫn Điện bằng <color=#f26c1c>180%</color> Tấn Công. Áp dụng '
                                      '<color=#3487e0>Tê Liệt</color> lên mục tiêu trong <color=#f26c1c>1 hiệp</color> '
                                      'và áp dụng <color=#3487e0>Dẫn Điện</color> trong <color=#f26c1c>2 '
                                      'hiệp</color>.'},
                      {'name': 'Uy Quyền Của Vua',
                       'tags': ['Bị Động', 'Suy Yếu'],
                       'description': 'Lenna miễn nhiễm với các hiệu ứng bất lợi từ ô địa hình Dẫn Điện. Khi kẻ địch '
                                      'nhận Dẫn Điện, Lenna nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu. Khi '
                                      'gây sát thương đơn mục tiêu, tạo ô địa hình <color=#3487e0>Điện Áp</color> '
                                      'trong bán kính 1 ô quanh mục tiêu trong <color=#f26c1c>2 hiệp</color>.'}],
           'fortification': [{'tier': 1,
                              'level': 2,
                              'skill': 'Uy Quyền Của Vua',
                              'effect': 'Cứ mỗi 3 điểm Chỉ Số Nhiên Liệu tiêu hao, giảm thời gian hồi chiêu của tất cả '
                                        'kỹ năng đi <color=#f26c1c>1 hiệp</color>.'},
                             {'tier': 2,
                              'level': 2,
                              'skill': 'Tuyệt Diệt Hoang Dã',
                              'effect': 'Nếu có từ 3 điểm Chỉ Số Nhiên Liệu trở lên trước khi kích hoạt, sát thương '
                                        'gây ra tăng từ 30% lên <color=#f26c1c>50%</color>. Nếu mục tiêu có Dẫn Điện, '
                                        'nhận thêm <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                             {'tier': 3,
                              'level': 2,
                              'skill': 'Nhảy Vọt Truy Kích',
                              'effect': 'Tầm thi triển hiệu lực tăng thêm <color=#f26c1c>2 ô</color>.'},
                             {'tier': 4,
                              'level': 2,
                              'skill': 'Chiến Lược Săn Mồi',
                              'effect': 'Tầm thi triển tăng thêm <color=#f26c1c>2 ô</color>, và áp dụng ngẫu nhiên 2 '
                                        'Debuff lên mục tiêu trong <color=#f26c1c>1 hiệp</color>.'},
                             {'tier': 5,
                              'level': 3,
                              'skill': 'Uy Quyền Của Vua',
                              'effect': 'Tăng thời lượng của Ẩn Nấp thêm <color=#f26c1c>1 hiệp</color>.'},
                             {'tier': 6,
                              'level': 3,
                              'skill': 'Chiến Lược Săn Mồi',
                              'effect': 'Hồ Quang Điện: Khi kết thúc hành động của Lenna, hồi phục đầy Chỉ Số Nhiên '
                                        'Liệu. Kỹ năng không còn cần tiêu hao Chỉ Số Nhiên Liệu để được cường hóa; khi '
                                        'tiêu hao, sát thương gây ra tăng thêm <color=#f26c1c>20%</color>.'}],
           'keys': [{'name': 'Khóa Cố Định 1 - Mưu Kế Khéo Léo',
                     'effect': 'Khi tấn công kẻ địch có Dẫn Điện và miễn nhiễm Tê Liệt, bỏ qua '
                               '<color=#f26c1c>15%</color> Phòng Thủ của mục tiêu.'},
                    {'name': 'Khóa Cố Định 2 - Hành Động Đẳng Cấp',
                     'effect': 'Tuyệt Diệt Hoang Dã: Khi kỹ năng này tiêu diệt mục tiêu, nhận thêm <color=#f26c1c>2 '
                               'điểm</color> Chỉ Số Nhiên Liệu.'},
                    {'name': 'Khóa Cố Định 3 - Phương Thức Hoàn Hảo',
                     'effect': 'Khi áp dụng Dẫn Điện, chuyển hóa 1 Buff ngẫu nhiên của mục tiêu thành 1 Debuff ngẫu '
                               'nhiên.'},
                    {'name': 'Khóa Cố Định 4 - Khát Khao Sức Mạnh',
                     'effect': 'Nhảy Vọt Truy Kích: Sau khi dùng kỹ năng, áp dụng Dẫn Điện lên 2 kẻ địch gần nhất '
                               'trong bán kính 5 ô trong <color=#f26c1c>1 hiệp</color>.'},
                    {'name': 'Khóa Cố Định 5 - Động Lực Thúc Đẩy',
                     'effect': 'Khi kẻ địch mang Debuff hệ Dẫn Điện bị tiêu diệt, nhận <color=#f26c1c>1 điểm</color> '
                               'Chỉ Số Nhiên Liệu.'},
                    {'name': 'Khóa Cố Định 6 - Phản Ứng Đỉnh Cao',
                     'effect': 'Khi Lenna rơi vào trạng thái Sụp Đổ Ổn Định do bị tấn công, áp dụng Tê Liệt lên toàn '
                               'bộ kẻ địch trong bán kính 5 ô trong <color=#f26c1c>1 hiệp</color> (kích hoạt 1 lần mỗi '
                               'trận).'},
                    {'name': 'Khóa Tương Thích - Nanh Vuốt Sắc Bén', 'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                    {'name': 'Khóa Chung - Vuốt Sắc Săn Mồi',
                     'effect': 'TL Bạo Kích +5.0% / Khi gây sát thương đơn mục tiêu, áp dụng Dẫn Điện lên mục tiêu '
                               'trong <color=#f26c1c>1 hiệp</color> (tối đa 2 lần mỗi hiệp).'},
                    {'name': 'Khóa Mở Rộng - Ý Chí Sư Tử',
                     'effect': 'Chiến Lược Săn Mồi: Sau khi dùng kỹ năng, Lenna nhận <color=#3487e0>Huy Hoàng Tối '
                               'Thượng</color> trong <color=#f26c1c>3 hiệp</color>.\n'
                               '\n'
                               'Nhảy Vọt Truy Kích: Tăng hệ số sát thương của đòn tấn công trong Chỉ Lệnh Bổ Sung thêm '
                               '<color=#f26c1c>100%</color>.\n'
                               '\n'
                               'Với mỗi điểm Chỉ Số Nhiên Liệu tiêu hao trong hiệp, tăng Tấn Công của Lenna thêm '
                               '<color=#f26c1c>5%</color> ở hiệp tiếp theo, tối đa tăng <color=#f26c1c>30%</color>.'}]},
 'leva': {'name': 'Leva',
          'en_name': 'Leva',
          'class': 'Vệ Binh',
          'phase': 'Dẫn Điện',
          'rarity': 'Tinh Nhuệ',
          'weapon_type': 'Súng Tiểu Liên',
          'ammo_type': 'Đạn Nhẹ',
          'signature_weapon': 'Đuôi Cáo Điện Từ',
          'weakness': 'Hóa Lỏng',
          'server': 'global',
          'skills': [{'name': 'Nụ Cười Nguy Hiểm',
                      'tags': ['Đánh Thường', 'Chuẩn Xác'],
                      'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST '
                                     'Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                     {'name': 'Áp Chế Lý Tính',
                      'tags': ['Chủ Động', 'AoE', 'Ô Địa Hình'],
                      'description': 'Chọn 1 hướng, gây ST Dẫn Điện AoE bằng <color=#f26c1c>120%</color> Tấn Công lên '
                                     'toàn bộ mục tiêu trong phạm vi 7×3 ô theo hướng chỉ định, áp dụng '
                                     '<color=#3487e0>Điện Tích Âm</color> trong <color=#f26c1c>2 hiệp</color> và tạo ô '
                                     'địa hình <color=#3487e0>Điện Áp</color> trong <color=#f26c1c>3 hiệp</color>.'},
                     {'name': 'Phá Rối Trật Tự',
                      'tags': ['Chủ Động', 'AoE'],
                      'description': 'Chọn 1 ô địa hình trong phạm vi 7 ô, gây ST Dẫn Điện AoE bằng '
                                     '<color=#f26c1c>100%</color> Tấn Công lên toàn bộ mục tiêu trong bán kính 3 ô '
                                     'quanh ô đó. Sát thương tăng thêm <color=#f26c1c>30%</color> và ST Ổn Định tăng '
                                     'thêm <color=#f26c1c>1 điểm</color> lên kẻ địch mang Điện Tích Âm.'},
                     {'name': 'Tính Toán Lượng Tử',
                      'tags': ['Tuyệt Kỹ', 'AoE', 'Ô Địa Hình', 'Cường Hóa'],
                      'description': 'Gây ST Dẫn Điện AoE bằng <color=#f26c1c>60%</color> Tấn Công lên toàn bộ mục '
                                     'tiêu trong bán kính 7 ô và tạo ô địa hình Điện Áp duy trì trong <color=#f26c1c>3 '
                                     'hiệp</color>. Leva nhận <color=#3487e0>Đòn Đánh Ép Xung</color> trong '
                                     '<color=#f26c1c>3 hiệp</color>. Sau khi tấn công, có thể dùng Đòn Đánh Siêu Dẫn 1 '
                                     'lần.'},
                     {'name': 'Mưu Kế Hồ Ly',
                      'tags': ['Bị Động', 'Hỗ Trợ'],
                      'description': 'Khi bắt đầu hiệp hoặc khi kích hoạt phản ứng địa hình Điện Áp, nhận '
                                     '<color=#f26c1c>1 tầng</color> <color=#3487e0>Mã Siêu Dẫn</color>. Nếu Leva có '
                                     '<color=#3487e0>Điện Tích Dương</color>, ST Dẫn Điện gây ra tăng thêm '
                                     '<color=#f26c1c>10%</color>. Nếu kẻ địch trong tầm bắn bị áp dụng Điện Tích Âm, '
                                     'Leva thực hiện 1 lần <color=#3487e0>Chi Viện Tức Thời</color>, gây ST Dẫn Điện '
                                     'cận chiến bằng <color=#f26c1c>60%</color> Tấn Công và 1 điểm ST Ổn Định, đồng '
                                     'thời nhận 1 điểm Chỉ Số Nhiên Liệu (tối đa 2 lần mỗi hiệp).'},
                     {'name': 'Đòn Đánh Siêu Dẫn',
                      'tags': ['Chủ Động', 'Cận Chiến', 'Ô Địa Hình'],
                      'description': 'Chọn 1 mục tiêu địch trong bán kính 7 ô, tạo ô địa hình Điện Áp trong bán kính 1 '
                                     'ô quanh mục tiêu trong 3 hiệp, sau đó gây ST Dẫn Điện cận chiến bằng '
                                     '<color=#f26c1c>50%</color> Tấn Công lên mục tiêu.\n'
                                     '\n'
                                     'Tiêu hao toàn bộ tầng Mã Siêu Dẫn để gia tăng hệ số sát thương và ST Ổn Định '
                                     'tương ứng:\n'
                                     '- 1 tầng: 60% Tấn Công + 1 ST Ổn Định\n'
                                     '- 2 tầng: 70% Tấn Công + 2 ST Ổn Định\n'
                                     '- 3 tầng: 85% Tấn Công + 3 ST Ổn Định\n'
                                     '- 4 tầng: 120% Tấn Công + 6 ST Ổn Định.'}],
          'fortification': [{'tier': 1,
                             'level': 2,
                             'skill': 'Mưu Kế Hồ Ly',
                             'effect': 'Số lần Chi Viện Tức Thời tối đa tăng thêm 1 lần. Nếu kẻ địch mang Điện Tích Âm '
                                       'trong tầm bắn tử trận, nhận 1 tầng Mã Siêu Dẫn. Nếu Leva có Điện Tích Dương, '
                                       'ST Dẫn Điện gây ra tăng thêm 25%.'},
                            {'tier': 2,
                             'level': 2,
                             'skill': 'Phá Rối Trật Tự',
                             'effect': 'Hệ số sát thương tăng lên 130% Tấn Công. Khi kết thúc hành động, nhận 1 tầng '
                                       'Mã Siêu Dẫn.'},
                            {'tier': 3,
                             'level': 2,
                             'skill': 'Tính Toán Lượng Tử',
                             'effect': 'Đòn Đánh Siêu Dẫn bỏ qua 15% Phòng Thủ của mục tiêu, và nhận 1 tầng Mã Siêu '
                                       'Dẫn sau khi dùng. Hệ số sát thương các mốc tầng tăng lên 75%/90%/120%/180% Tấn '
                                       'Công và 1/2/4/8 ST Ổn Định.'},
                            {'tier': 4,
                             'level': 2,
                             'skill': 'Áp Chế Lý Tính',
                             'effect': 'Áp dụng Tê Liệt lên toàn bộ mục tiêu trong phạm vi trong 2 hiệp. ST Bạo Kích '
                                       'của kỹ năng này tăng thêm 25%.'},
                            {'tier': 5,
                             'level': 3,
                             'skill': 'Tính Toán Lượng Tử',
                             'effect': 'Hệ số sát thương tăng lên 90% Tấn Công, giải trừ toàn bộ Debuff trên bản thân '
                                       'trước khi tấn công.'},
                            {'tier': 6,
                             'level': 3,
                             'skill': 'Mưu Kế Hồ Ly',
                             'effect': 'Sau khi dùng Áp Chế Lý Tính hoặc Phá Rối Trật Tự, có thể dùng Đòn Đánh Siêu '
                                       'Dẫn 1 lần. Khi Leva đạt 4 tầng Mã Siêu Dẫn, Tấn Công tăng thêm 15%.'}],
          'keys': [{'name': 'Khóa Cố Định 1 - Điềm Tĩnh Trưởng Thành',
                    'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Mã Siêu '
                              'Dẫn</color> và <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                   {'name': 'Khóa Cố Định 2 - Nụ Cười Hồ Ly',
                    'effect': 'Sát thương gây ra lên kẻ địch đang trong trạng thái Sụp Đổ Ổn Định tăng '
                              '<color=#f26c1c>7%</color>.'},
                   {'name': 'Khóa Cố Định 3 - Ứng Biến Linh Hoạt',
                    'effect': 'Trước khi thực hiện Chi Viện Tức Thời, giải trừ <color=#f26c1c>1</color> Buff của mục '
                              'tiêu.'},
                   {'name': 'Khóa Cố Định 4 - Kế Hoạch Ẩn Náu',
                    'effect': 'Sau khi dùng Đòn Đánh Siêu Dẫn, nhận trạng thái <color=#3487e0>Ẩn Nấp</color> trong '
                              '<color=#f26c1c>1 hiệp</color>.'},
                   {'name': 'Khóa Cố Định 5 - Phản Ứng Lý Tính',
                    'effect': 'Trước khi đồng minh tấn công chủ động, áp dụng Điện Tích Âm lên kẻ địch trong tầm bắn '
                              'trong <color=#f26c1c>1 hiệp</color>.'},
                   {'name': 'Khóa Cố Định 6 - Luôn Luôn Sẵn Sàng',
                    'effect': 'Khi bắt đầu chiến đấu, nhận <color=#3487e0>Đòn Đánh Ép Xung</color> trong '
                              '<color=#f26c1c>3 hiệp</color>.'},
                   {'name': 'Khóa Tương Thích - Nét Duyên Hồ Ly',
                    'effect': 'Tấn Công +3%, TL Bạo Kích +3%, ST Bạo Kích +3%'},
                   {'name': 'Khóa Chung - Đặc Điệp Tinh Nhuệ',
                    'effect': 'Tấn Công +5.0% / Tăng sát thương gây ra lên kẻ địch mang Debuff hệ Dẫn Điện thêm '
                              '<color=#f26c1c>7%</color>.'},
                   {'name': 'Khóa Mở Rộng - Gián Điệp Điện Từ',
                    'effect': 'Tầm tấn công của các đòn chi viện và Đòn Đánh Siêu Dẫn tăng lên 9 ô. Số lần tấn công '
                              'chi viện tăng thêm 1 lần. ST Bạo Kích gây ra lên kẻ địch có Điện Tích Âm tăng 7% (tăng '
                              'thêm 7% nếu mục tiêu Sụp Đổ Ổn Định). Khi bắt đầu trận chiến, với mỗi đồng minh hệ Dẫn '
                              'Điện, ST Dẫn Điện của Leva tăng 2% và ST Ổn Định tăng 1 điểm.'}]}}
