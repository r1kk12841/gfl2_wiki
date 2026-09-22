"""
Auto-synced batch data.
"""

GROUP_2_DATA = {'jiangyu': {'name': 'Jiangyu',
             'en_name': 'Jiangyu',
             'class': 'Hỗ Trợ',
             'phase': 'Dẫn Điện',
             'rarity': 'Tinh Nhuệ',
             'weapon_type': 'Súng Trường Tấn Công',
             'ammo_type': 'Đạn Vừa',
             'signature_weapon': 'Hổ Vồ',
             'weakness': 'Hóa Lỏng',
             'server': 'global',
             'skills': [{'name': 'Hình Ý Quyền',
                         'tags': ['Đánh Thường', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây '
                                        'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                        {'name': 'Sấm Sét Rền Vang',
                         'tags': ['Chủ Động', 'Cận Chiến', 'AoE'],
                         'description': 'Chọn 1 mục tiêu địch trong phạm vi 3×3 ô quanh bản thân, gây ST Dẫn Điện Cận '
                                        'Chiến AoE bằng <color=#f26c1c>90%</color> Tấn Công lên mục tiêu và tất cả kẻ '
                                        'địch trong phạm vi 3×3 ô. Tạo ô địa hình <color=#3487e0>Điện Áp</color> trong '
                                        '<color=#f26c1c>3 hiệp</color>. Nếu khai thác được Điểm Yếu Thuộc Tính, gây '
                                        'thêm <color=#f26c1c>5 điểm</color> ST Ổn Định. Sau đòn đánh, nhận '
                                        '<color=#f26c1c>6 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color> và '
                                        '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                        {'name': 'Kích Điện Mãnh Liệt',
                         'tags': ['Chủ Động', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>, gây '
                                        'ST Dẫn Điện bằng <color=#f26c1c>110%</color> Tấn Công. Jiangyu nhận '
                                        '<color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu. Nếu mục tiêu đang trong '
                                        'trạng thái Sụp Đổ Ổn Định, nhận <color=#f26c1c>1 tầng</color> '
                                        '<color=#3487e0>Khí</color> trước khi tấn công.'},
                        {'name': 'Sấm Rền Vạn Lý',
                         'tags': ['Tuyệt Kỹ', 'Chuẩn Xác', 'Cường Hóa'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 8 ô xung quanh</color>. '
                                        'Jiangyu nhận <color=#f26c1c>2 tầng</color> <color=#3487e0>Khí</color> và gây '
                                        'ST Dẫn Điện bỏ qua Vật Cản bằng <color=#f26c1c>130%</color> Tấn Công. Áp dụng '
                                        '<color=#3487e0>Điện Tích Dương</color> lên toàn bộ đồng minh trong '
                                        '<color=#f26c1c>3 hiệp</color>, giải trừ <color=#f26c1c>1</color> Debuff, đồng '
                                        'thời xóa bỏ trạng thái <color=#3487e0>Choáng</color> và <color=#3487e0>Khiêu '
                                        'Khích</color>. Jiangyu nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                        {'name': 'Hạo Nhiên Chính Khí',
                         'tags': ['Bị Động', 'Hỗ Trợ'],
                         'description': 'Khi bắt đầu hiệp đấu, Jiangyu nhận <color=#f26c1c>1 điểm</color> Chỉ Số Nhiên '
                                        'Liệu.\n'
                                        'Khi kết thúc hành động, nếu Chỉ Số Nhiên Liệu đầy, tiêu hao toàn bộ điểm để '
                                        'giảm thời gian hồi chiêu của Sấm Rền Vạn Lý đi <color=#f26c1c>1 hiệp</color>. '
                                        'Khi kẻ địch liên tục nhận <color=#3487e0>Điện Tích Âm</color>, áp dụng '
                                        '<color=#f26c1c>1 tầng</color> <color=#3487e0>Sóng Điện Sai Tầng</color> trong '
                                        '<color=#f26c1c>2 hiệp</color>. Khi đồng minh liên tục nhận Điện Tích Dương, '
                                        'áp dụng <color=#f26c1c>1 tầng</color> <color=#3487e0>Bổ Sung Điện '
                                        'Mạnh</color> trong <color=#f26c1c>3 hiệp</color>.\n'
                                        '\n'
                                        'Khi kẻ địch trong tầm bắn (8 ô) nhận sát thương đơn mục tiêu từ đồng minh, '
                                        'Jiangyu ưu tiên thực hiện 1 lần Hành Động Chi Viện và nhận <color=#f26c1c>1 '
                                        'tầng</color> Khí.\n'
                                        '\n'
                                        'Hành Động Chi Viện: Nếu mục tiêu có Ổn Định > 0, gây ST Dẫn Điện bằng '
                                        '<color=#f26c1c>45%</color> Tấn Công và <color=#f26c1c>3 điểm</color> ST Ổn '
                                        'Định. Nếu mục tiêu Sụp Đổ Ổn Định, gây ST Dẫn Điện bằng '
                                        '<color=#f26c1c>75%</color> Tấn Công. Kích hoạt tối đa <color=#f26c1c>2 '
                                        'lần</color> mỗi hiệp.'}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Hạo Nhiên Chính Khí',
                                'effect': 'Số lần Hành Động Chi Viện tăng thêm <color=#f26c1c>1 lần</color>.\n'
                                          'Khi bắt đầu chiến đấu, gây <color=#f26c1c>4 điểm</color> ST Ổn Định cố định '
                                          'lên toàn bộ đơn vị địch trong phạm vi bán kính <color=#f26c1c>8 ô</color>.\n'
                                          '<color=#3487e0>Sóng Điện Sai Tầng</color> nhận hiệu ứng mới: Khi nhận được, '
                                          'gây sát thương cố định bằng số tầng hiện tại × <color=#f26c1c>10%</color> '
                                          'Tấn Công của người thi triển.\n'
                                          '<color=#3487e0>Bổ Sung Điện Mạnh</color> nhận hiệu ứng mới: Khi nhận hiệu '
                                          'ứng này, hồi phục lượng HP bằng <color=#f26c1c>10%</color> HP tối đa.'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Sấm Rền Vạn Lý',
                                'effect': 'Thời gian hồi chiêu giảm <color=#f26c1c>1 hiệp</color>, và Chỉ Số Nhiên '
                                          'Liệu nhận được tăng thêm <color=#f26c1c>1 điểm</color>.\n'
                                          'Hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho toàn bộ đồng '
                                          'minh, tăng số lượng Debuff được giải trừ thêm <color=#f26c1c>1</color>, và '
                                          'xóa bỏ <color=#3487e0>Chạy Trốn</color> cùng <color=#3487e0>Dẫn '
                                          'Dụ</color>.'},
                               {'tier': 3,
                                'level': 2,
                                'skill': 'Kích Điện Mãnh Liệt',
                                'effect': 'Hệ số sát thương tăng lên <color=#f26c1c>140%</color>.\n'
                                          'Sát thương gây ra cho mục tiêu có <color=#3487e0>Sóng Điện Sai Tầng</color> '
                                          'tăng thêm <color=#f26c1c>30%</color>.\n'
                                          'Trước khi gây sát thương, hóa giải <color=#f26c1c>1</color> Buff của mục '
                                          'tiêu.'},
                               {'tier': 4,
                                'level': 2,
                                'skill': 'Sấm Sét Rền Vang',
                                'effect': 'Trước khi tấn công, nhận <color=#3487e0>Tấn Công Tăng II</color> trong '
                                          '<color=#f26c1c>3 hiệp</color>. Khi gây ST Ổn Định, gây thêm '
                                          '<color=#f26c1c>5 điểm</color> ST Ổn Định cố định lên toàn bộ đơn vị địch '
                                          'mang <color=#3487e0>Điện Tích Âm</color>.'},
                               {'tier': 5,
                                'level': 3,
                                'skill': 'Kích Điện Mãnh Liệt',
                                'effect': 'Số lượng Buff hóa giải tăng thêm <color=#f26c1c>1</color>. Nếu mục tiêu có '
                                          '<color=#f26c1c>0 điểm</color> Ổn Định, thực hiện thêm 1 đòn tấn công bổ '
                                          'sung.'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Hạo Nhiên Chính Khí',
                                'effect': 'ST Ổn Định cố định gây ra khi bắt đầu chiến đấu tăng thêm <color=#f26c1c>4 '
                                          'điểm</color>.\n'
                                          'Khi Jiangyu sở hữu <color=#3487e0>Khí</color>, <color=#b359f2>ST Dẫn '
                                          'Điện</color> gây ra tăng thêm <color=#f26c1c>15%</color>.\n'
                                          'Giới hạn tầng tối đa của <color=#3487e0>Sóng Điện Sai Tầng</color> tăng '
                                          'thêm <color=#f26c1c>3 tầng</color>.\n'
                                          'Thay đổi hiệu ứng <color=#3487e0>Bổ Sung Điện Mạnh</color>: Khi gây '
                                          '<color=#b359f2>ST Dẫn Điện</color>, tỷ lệ bỏ qua Phòng Thủ tăng lên '
                                          '<color=#f26c1c>10%</color>, và lượng hồi máu nhận được tăng lên '
                                          '<color=#f26c1c>10%</color>.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Khởi Động Nội Lực',
                       'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>4 tầng</color> '
                                 '<color=#3487e0>Khí</color>.'},
                      {'name': 'Khóa Cố Định 2 - Quy Tắc Quan Sát',
                       'effect': 'Trước khi kẻ địch trong phạm vi 8 ô tấn công chủ động, Jiangyu thực hiện 1 lần '
                                 '<color=#3487e0>Chặn Đánh</color>, gây ST Dẫn Điện bằng <color=#f26c1c>60%</color> '
                                 'Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn Định. Trước đòn đánh, áp dụng '
                                 '<color=#3487e0>Dẫn Điện</color> trong <color=#f26c1c>1 hiệp</color>. Kích hoạt tối '
                                 'đa <color=#f26c1c>2 lần</color> mỗi hiệp.'},
                      {'name': 'Khóa Cố Định 3 - Tâm Định Như Bàn Thạch',
                       'effect': 'Khi bị áp dụng Khiêu Khích, Chạy Trốn, Dẫn Dụ hoặc Choáng, lập tức giải trừ hiệu '
                                 'ứng. Hồi chiêu: 1 hiệp.'},
                      {'name': 'Khóa Cố Định 4 - Chuyển Hướng Kình Lực',
                       'effect': 'Khi sở hữu Khí, sát thương nhận vào giảm <color=#f26c1c>15%</color>.'},
                      {'name': 'Khóa Cố Định 5 - Phản Chấn Uy Dũng',
                       'effect': 'Khi Chặn Đánh mục tiêu trong trạng thái Sụp Đổ Ổn Định, sát thương gây ra tăng thêm '
                                 '<color=#f26c1c>30%</color>.'},
                      {'name': 'Khóa Cố Định 6 - Điện Áp Cực Đại',
                       'effect': 'Khi đứng trên ô địa hình Điện Áp, Tấn Công tăng <color=#f26c1c>10%</color> và tầm di '
                                 'chuyển tăng thêm <color=#f26c1c>1 ô</color>.'},
                      {'name': 'Khóa Tương Thích - Khí Phách Hào Kiệt',
                       'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                      {'name': 'Khóa Chung - Hổ Gầm Núi Rừng',
                       'effect': 'Tấn Công +5.0% / Khi tấn công mục tiêu có Debuff hệ Dẫn Điện, sát thương tăng '
                                 '<color=#f26c1c>7%</color>.'},
                      {'name': 'Khóa Mở Rộng - Mãnh Hổ Xuất Sơn',
                       'effect': 'Tấn công bỏ qua <color=#f26c1c>20%</color> Phòng Thủ của mục tiêu. Khi Chặn Đánh '
                                 'thành công, lập tức hồi phục <color=#f26c1c>2 điểm</color> Chỉ Số Ổn Định cho toàn '
                                 'đội.'}]},
 'vector': {'name': 'Vector',
            'en_name': 'Vector',
            'class': 'Hỗ Trợ',
            'phase': 'Đốt Cháy',
            'rarity': 'Tinh Nhuệ',
            'weapon_type': 'Súng Tiểu Liên',
            'ammo_type': 'Đạn Nhẹ',
            'signature_weapon': 'Tiếng Thì Thầm Banshee',
            'weakness': 'Hóa Lỏng',
            'server': 'global',
            'skills': [{'name': 'Tâm Lý Trầm Uất',
                        'tags': ['Đánh Thường', 'Chuẩn Xác'],
                        'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây '
                                       'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                       {'name': 'Tan Chảy Ngõ Cụt',
                        'tags': ['Chủ Động', 'Chuẩn Xác', 'Suy Yếu'],
                        'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây '
                                       'ST Đốt Cháy bằng <color=#f26c1c>120%</color> Tấn Công. Nếu mục tiêu mang '
                                       'Debuff hệ Đốt Cháy, gây ST cố định bằng <color=#f26c1c>50%</color> Tấn Công '
                                       'lên mục tiêu và tất cả kẻ địch trong bán kính 3 ô, đồng thời áp dụng '
                                       '<color=#3487e0>Tràn Lửa</color> trong <color=#f26c1c>2 hiệp</color>. Vector '
                                       'nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.'},
                       {'name': 'Điềm Báo Tận Diệt',
                        'tags': ['Chủ Động', 'Chuẩn Xác', 'Suy Yếu'],
                        'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây '
                                       'ST Đốt Cháy bằng <color=#f26c1c>100%</color> Tấn Công và áp dụng '
                                       '<color=#3487e0>Lòng Như Lửa Đốt</color> trong <color=#f26c1c>2 hiệp</color>. '
                                       'Vector nhận <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.'},
                       {'name': 'Khúc Vĩ Bỏng Rát',
                        'tags': ['Tuyệt Kỹ', 'AoE', 'Ô Địa Hình', 'Cường Hóa'],
                        'description': 'Chọn 1 ô địa hình <color=#f26c1c>trong phạm vi 7 ô xung quanh</color>, gây ST '
                                       'Đốt Cháy AoE bằng <color=#f26c1c>60%</color> Tấn Công lên toàn bộ kẻ địch và '
                                       'tạo ô địa hình <color=#3487e0>Thiêu Rụi</color> duy trì <color=#f26c1c>2 '
                                       'hiệp</color> trong phạm vi 7 ô quanh ô chỉ định. Áp dụng <color=#3487e0>Thêm '
                                       'Dầu Vào Lửa</color> lên toàn bộ đồng minh trong <color=#f26c1c>2 hiệp</color>. '
                                       'Vector nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>.'},
                       {'name': 'Chặn Đứng Nhận Thức',
                        'tags': ['Bị Động', 'Suy Yếu'],
                        'description': 'Vector miễn nhiễm với các hiệu ứng bất lợi từ ô địa hình Đốt Cháy.\n'
                                       '\n'
                                       'Trước khi gây ST Đốt Cháy, nếu mục tiêu mang Tràn Lửa, áp dụng '
                                       '<color=#3487e0>Cháy Quá Nhiệt</color> lên mục tiêu trong <color=#f26c1c>2 '
                                       'hiệp</color>.\n'
                                       '\n'
                                       'Khi bắt đầu trận chiến, số lần Tấn Công Chi Viện gây ST Đốt Cháy tăng thêm '
                                       '<color=#f26c1c>1 lần</color>.\n'
                                       '\n'
                                       'Khi bắt đầu mỗi hiệp, nếu Chỉ Số Nhiên Liệu đầy, Vector tiêu hao toàn bộ điểm '
                                       'và tăng Tấn Công thêm <color=#f26c1c>10%</color> cho đến cuối hiệp đấu.'}],
            'fortification': [{'tier': 1,
                               'level': 2,
                               'skill': 'Chặn Đứng Nhận Thức',
                               'effect': 'Bổ sung hiệu ứng cho Cháy Quá Nhiệt: Tăng ST Đốt Cháy phải gánh chịu thêm '
                                         '<color=#f26c1c>30%</color>, gây sát thương cố định lên toàn bộ kẻ địch trong '
                                         'phạm vi 3×3 ô quanh mục tiêu, và số lần Tấn Công Chi Viện gây ST Đốt Cháy '
                                         'tăng lên <color=#f26c1c>2 lần</color>.'},
                              {'tier': 2,
                               'level': 2,
                               'skill': 'Khúc Vĩ Bỏng Rát',
                               'effect': 'Cường hóa Thêm Dầu Vào Lửa: Khi gây ST Đốt Cháy, sát thương tăng thêm '
                                         '<color=#f26c1c>20%</color> (từ 10% lên 30%).\n'
                                         '\n'
                                         'Áp dụng <color=#3487e0>Thế Công Rực Lửa II</color> lên toàn bộ đồng minh '
                                         'trong <color=#f26c1c>2 hiệp</color> và giải trừ <color=#f26c1c>2</color> '
                                         'Debuff cho cả đội.'},
                              {'tier': 3,
                               'level': 2,
                               'skill': 'Tan Chảy Ngõ Cụt',
                               'effect': 'Hệ số ST Đốt Cháy và sát thương cố định tăng thêm '
                                         '<color=#f26c1c>30%</color>.\n'
                                         '\n'
                                         'Mục tiêu không bắt buộc phải có Debuff hệ Đốt Cháy để kích hoạt sát thương '
                                         'cố định. Áp dụng thêm Cháy Quá Nhiệt lên mục tiêu trong <color=#f26c1c>2 '
                                         'hiệp</color>.\n'
                                         '\n'
                                         'Vector nhận thêm <color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.'},
                              {'tier': 4,
                               'level': 2,
                               'skill': 'Điềm Báo Tận Diệt',
                               'effect': 'Hệ số sát thương tăng thêm <color=#f26c1c>30%</color>.\n'
                                         '\n'
                                         'Bổ sung hiệu ứng cho Lòng Như Lửa Đốt: Với mỗi Debuff hệ Đốt Cháy đang có, '
                                         'tăng sát thương phải gánh chịu thêm <color=#f26c1c>3%</color>.\n'
                                         '\n'
                                         'Áp dụng Quá Nhiệt trong <color=#f26c1c>1 hiệp</color>. Vector nhận thêm '
                                         '<color=#f26c1c>2 điểm</color> Chỉ Số Nhiên Liệu.'},
                              {'tier': 5,
                               'level': 3,
                               'skill': 'Chặn Đứng Nhận Thức',
                               'effect': 'Bổ sung hiệu ứng cho Cháy Quá Nhiệt: Khi kết thúc hành động, tạo ô địa hình '
                                         'Thiêu Rụi trong phạm vi 1 ô quanh bản thân. Hệ số sát thương cố định tăng '
                                         'thêm <color=#f26c1c>10%</color>.\n'
                                         '\n'
                                         'Khi bắt đầu hiệp, với mỗi điểm Chỉ Số Nhiên Liệu vượt quá giới hạn tối đa, '
                                         'tăng Tấn Công thêm <color=#f26c1c>10%</color>, tối đa tăng '
                                         '<color=#f26c1c>20%</color>.'},
                              {'tier': 6,
                               'level': 3,
                               'skill': 'Khúc Vĩ Bỏng Rát',
                               'effect': 'Bổ sung hiệu ứng cho Thêm Dầu Vào Lửa: Khi gây ST Đốt Cháy, tăng ST Bạo Kích '
                                         'thêm <color=#f26c1c>15%</color>. Với mỗi Buff hệ Đốt Cháy đang có, tăng sát '
                                         'thương thêm <color=#f26c1c>5%</color>.'}],
            'keys': [{'name': 'Khóa Cố Định 1 - Điểm Hỏa Tận Diệt',
                      'effect': 'Tan Chảy Ngõ Cụt: Nếu tiêu diệt được mục tiêu, tạo ô địa hình <color=#3487e0>Thiêu '
                                'Rụi</color> trong bán kính 3 ô quanh mục tiêu duy trì <color=#f26c1c>2 hiệp</color>.'},
                     {'name': 'Khóa Cố Định 2 - Tiếp Lửa Chiến Trường',
                      'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                     {'name': 'Khóa Cố Định 3 - Xóa Sạch Chướng Ngại',
                      'effect': 'Trước khi tấn công chủ động, giải trừ <color=#f26c1c>2</color> Buff của mục tiêu.'},
                     {'name': 'Khóa Cố Định 4 - Nhiệt Lượng Vĩnh Cửu',
                      'effect': 'Khi đứng trên ô địa hình Thiêu Rụi, sát thương gây ra tăng thêm '
                                '<color=#f26c1c>15%</color>.'},
                     {'name': 'Khóa Cố Định 5 - Kháng Hỏa Tuyệt Đối',
                      'effect': 'Giảm sát thương phải gánh chịu từ các đòn đánh hệ Đốt Cháy đi '
                                '<color=#f26c1c>20%</color>.'},
                     {'name': 'Khóa Cố Định 6 - Ngọn Lửa Cuồng Nhiệt',
                      'effect': 'Khi mục tiêu mang Cháy Quá Nhiệt tử trận, gây ST Đốt Cháy AoE bằng '
                                '<color=#f26c1c>40%</color> Tấn Công lên toàn bộ kẻ địch xung quanh 2 ô.'},
                     {'name': 'Khóa Tương Thích - Tàn Tro Rực Đỏ', 'effect': 'Tấn Công +3%, HP +3%, TL Bạo Kích +3%'},
                     {'name': 'Khóa Chung - Bão Lửa Tàn Phá',
                      'effect': 'Tấn Công +5.0% / Khi gây sát thương lên kẻ địch mang Debuff hệ Đốt Cháy, sát thương '
                                'tăng <color=#f26c1c>7%</color>.'},
                     {'name': 'Khóa Mở Rộng - Hỏa Diễm Bùng Nổ',
                      'effect': 'Tấn công bỏ qua <color=#f26c1c>25%</color> Phòng Thủ của mục tiêu đang mang Tràn Lửa '
                                'hoặc Cháy Quá Nhiệt. Sau khi dùng Khúc Vĩ Bỏng Rát, nhận thêm 1 lần '
                                '<color=#3487e0>Chi Viện Tức Thời</color>.'}]},
 'makiatto': {'name': 'Makiatto',
              'en_name': 'Makiatto',
              'class': 'Vệ Binh',
              'phase': 'Băng Kết',
              'rarity': 'Tinh Nhuệ',
              'weapon_type': 'Súng Bắn Tỉa',
              'ammo_type': 'Đạn Nặng',
              'signature_weapon': 'Sát Ý Băng Giá',
              'weakness': 'Đốt Cháy',
              'server': 'global',
              'skills': [{'name': 'Phát Bắn Chuẩn Xác Băng Giá',
                          'tags': ['Đánh Thường', 'Chuẩn Xác'],
                          'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 9 ô xung quanh</color>, '
                                         'gây ST Băng Kết bằng <color=#f26c1c>100%</color> Tấn Công. Tỷ lệ bạo kích '
                                         'của đòn đánh này tăng thêm <color=#f26c1c>100%</color>, và ST Bạo Kích tăng '
                                         'thêm <color=#f26c1c>50%</color>.'},
                         {'name': 'Lãnh Địa Sói Cô Độc',
                          'tags': ['Chủ Động', 'Cường Hóa'],
                          'description': 'Makiatto nhận <color=#f26c1c>1 tầng</color> <color=#3487e0>Sói Cô '
                                         'Độc</color> và nhận <color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Khi có Sói Cô '
                                         'Độc, sau khi đồng minh tấn công mục tiêu địch trong tầm bắn, Makiatto thực '
                                         'hiện 1 lần <color=#3487e0>Chặn Đánh</color>, gây ST Băng Kết bằng '
                                         '<color=#f26c1c>80%</color> Tấn Công và <color=#f26c1c>2 điểm</color> ST Ổn '
                                         'Định.'},
                         {'name': 'Chiến Thuật Chuyên Nghiệp',
                          'tags': ['Chủ Động', 'Cường Hóa'],
                          'description': 'Nhận <color=#3487e0>Chiến Lược Thường</color> và nhận <color=#3487e0>Chỉ '
                                         'Lệnh Bổ Sung</color>. Makiatto nhận <color=#f26c1c>1 điểm</color> Chỉ Số '
                                         'Nhiên Liệu.'},
                         {'name': 'Phòng Ngự Tâm Trí Tuyệt Đối',
                          'tags': ['Tuyệt Kỹ', 'Cường Hóa', 'Phòng Ngự'],
                          'description': 'Nhận <color=#3487e0>Lá Chắn Hàn Sương</color> và <color=#3487e0>Cảnh '
                                         'Giác</color> trong <color=#f26c1c>2 hiệp</color>. Lượng hấp thu của Lá Chắn '
                                         'Hàn Sương bằng <color=#f26c1c>65%</color> Tấn Công ban đầu, nhưng không vượt '
                                         'quá <color=#f26c1c>60%</color> HP tối đa.'},
                         {'name': 'Cái Nhìn Chiến Trường',
                          'tags': ['Bị Động', 'Cường Hóa'],
                          'description': 'Tăng tỷ lệ bạo kích thêm <color=#f26c1c>40%</color> và giảm sát thương bạo '
                                         'kích đi <color=#f26c1c>10%</color>.\n'
                                         '\n'
                                         'Khi bắt đầu hiệp, nếu HP của bản thân trên 80%, nhận <color=#3487e0>Nhìn '
                                         'Thấu</color> và <color=#3487e0>Hành Động Vững Bước</color> cho đến hiệp sau. '
                                         'Khi tấn công mục tiêu có <color=#3487e0>Ngưng Tụ</color>, bỏ qua '
                                         '<color=#f26c1c>4 điểm</color> Chỉ Số Ổn Định và tăng sát thương gây ra thêm '
                                         '<color=#f26c1c>20%</color>. Khi tấn công mục tiêu có <color=#3487e0>Cứng '
                                         'Đờ</color>, bỏ qua <color=#f26c1c>6 điểm</color> Chỉ Số Ổn Định và tăng sát '
                                         'thương thêm <color=#f26c1c>30%</color>. Các hiệu ứng này không cộng dồn.'}],
              'fortification': [{'tier': 1,
                                 'level': 2,
                                 'skill': 'Phát Bắn Chuẩn Xác Băng Giá',
                                 'effect': 'Tấn công 2 lần, sát thương bạo kích không còn tăng thêm và sát thương gây '
                                           'ra giảm xuống 100% Tấn Công. Nếu đòn thứ nhất bạo kích, tỷ lệ bạo kích đòn '
                                           'thứ hai tăng 100% và ST Bạo Kích tăng 80%.'},
                                {'tier': 2,
                                 'level': 2,
                                 'skill': 'Phòng Ngự Tâm Trí Tuyệt Đối',
                                 'effect': 'Lượng hấp thu của Lá Chắn Hàn Sương tăng lên <color=#f26c1c>80%</color> '
                                           'Tấn Công ban đầu, mức trần tăng lên 80% HP tối đa. Số lần Chặn Đánh tăng '
                                           'thêm 1 lần mỗi hiệp.'},
                                {'tier': 3,
                                 'level': 2,
                                 'skill': 'Cái Nhìn Chiến Trường',
                                 'effect': 'Khi gây ST Băng Kết lên mục tiêu có Ngưng Tụ, Chỉ Số Ổn Định bị bỏ qua '
                                           'tăng lên 6 điểm. Với mục tiêu có Cứng Đờ, Chỉ Số Ổn Định bị bỏ qua tăng '
                                           'lên 10 điểm.'},
                                {'tier': 4,
                                 'level': 2,
                                 'skill': 'Chiến Thuật Chuyên Nghiệp',
                                 'effect': 'Chuyển Chiến Lược Thường thành <color=#3487e0>Chiến Lược Khẩn '
                                           'Cấp</color>.'},
                                {'tier': 5,
                                 'level': 3,
                                 'skill': 'Cái Nhìn Chiến Trường',
                                 'effect': 'Khi gây ST Băng Kết lên mục tiêu có Ngưng Tụ hoặc Cứng Đờ, Chỉ Số Ổn Định '
                                           'bị bỏ qua tăng lên 10 điểm và sát thương gây ra tăng 30%.'},
                                {'tier': 6,
                                 'level': 3,
                                 'skill': 'Phòng Ngự Tâm Trí Tuyệt Đối',
                                 'effect': 'Sau khi dùng Phòng Ngự Tâm Trí Tuyệt Đối, nhận 2 điểm Chỉ Số Nhiên Liệu '
                                           'khi kết thúc hành động. Chặn Đánh kích hoạt thêm 1 lần mỗi hiệp; nếu Chặn '
                                           'Đánh bạo kích, nhận <color=#3487e0>Tập Trung Gấp Đôi</color> trong 1 '
                                           'hiệp.'}],
              'keys': [{'name': 'Khóa Cố Định 1 - Tình Báo Bổ Sung',
                        'effect': 'Khi kỹ năng Phát Bắn Chuẩn Xác Băng Giá tiêu diệt được mục tiêu, nhận '
                                  '<color=#f26c1c>1 điểm</color> Chỉ Số Nhiên Liệu.'},
                       {'name': 'Khóa Cố Định 2 - Kem Bọt Băng Tuyết',
                        'effect': 'Khi bắt đầu trận chiến, nhận <color=#f26c1c>3 điểm</color> Chỉ Số Nhiên Liệu.'},
                       {'name': 'Khóa Cố Định 3 - Sói Đơn Độc Kiên Cường',
                        'effect': 'Sau khi dùng Chiến Thuật Chuyên Nghiệp, nếu không có đồng minh nào trong phạm vi 3 '
                                  'ô, nhận 1 tầng Sói Cô Độc.'},
                       {'name': 'Khóa Cố Định 4 - Giờ Nghỉ Giải Lao',
                        'effect': 'Khi dùng kỹ năng trên ô địa hình Băng Kết, giải trừ mọi Debuff hệ Băng Kết trên bản '
                                  'thân và nhận <color=#f26c1c>3 ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color>.'},
                       {'name': 'Khóa Cố Định 5 - Caramel Nóng Bỏng',
                        'effect': 'Khi bắt đầu chiến đấu, áp dụng <color=#3487e0>Sát Ý Run Rẩy</color> lên kẻ địch có '
                                  'lượng HP cao nhất.'},
                       {'name': 'Khóa Cố Định 6 - Tập Trung Tuyệt Đối',
                        'effect': 'Tăng Tấn Công thêm <color=#f26c1c>10%</color> khi bắt đầu chiến đấu. Hiệu ứng duy '
                                  'trì cho đến khi HP lần đầu tiên giảm xuống dưới 100%.'},
                       {'name': 'Khóa Tương Thích - Tình Yêu Ngọt Ngào',
                        'effect': 'Tấn Công +3%, HP +3%, ST Bạo Kích +3%'},
                       {'name': 'Khóa Chung - Bản Năng Sinh Tồn',
                        'effect': 'Tấn Công +5.0% / Khi bắt đầu hành động, nếu HP bản thân trên 80%, giảm ST Ổn Định '
                                  'phải nhận đi 2 điểm.'},
                       {'name': 'Khóa Mở Rộng 1 - Ống Ngắm Bắn Tỉa',
                        'effect': 'ST Bạo Kích của các đòn Chặn Đánh tăng <color=#f26c1c>30%</color>. Khi Phòng Ngự '
                                  'Tâm Trí Tuyệt Đối đang kích hoạt, nhận Chỉ Lệnh Bổ Sung. Nếu mục tiêu là Boss, áp '
                                  'dụng <color=#3487e0>Đường Quá Liều</color> trong <color=#f26c1c>2 hiệp</color>.'},
                       {'name': 'Khóa Mở Rộng 2 - Lãnh Địa Tuyệt Đối',
                        'effect': 'Khi bắt đầu trận chiến, tăng Tấn Công của bản thân thêm <color=#f26c1c>30%</color> '
                                  'và bỏ qua <color=#f26c1c>30%</color> Phòng Thủ của mục tiêu khi tấn công; đồng thời '
                                  'tạo 1 điểm Cao Điểm tại ô trống gần nhất. Khi đứng trên Cao Điểm, sát thương gây ra '
                                  'tăng <color=#f26c1c>80%</color> và ST Bạo Kích tăng <color=#f26c1c>30%</color>.\n'
                                  'Khi Phục Kích đánh trúng mục tiêu, triệu hồi 1 <color=#3487e0>Vật Tạo Băng</color> '
                                  'bên cạnh. Khi Vật Tạo Băng xuất hiện và khi kết thúc hành động, áp dụng Khiêu Khích '
                                  'lên toàn bộ kẻ địch trong bán kính 3 ô duy trì 2 hiệp.'}]},
 'robella': {'name': 'Robella',
             'en_name': 'Robella',
             'class': 'Vệ Binh',
             'phase': 'Băng Kết',
             'rarity': 'Tinh Nhuệ',
             'weapon_type': 'Súng Bắn Tỉa',
             'ammo_type': 'Đạn Nặng',
             'signature_weapon': 'Ánh Sáng Công Lý',
             'weakness': 'Đốt Cháy',
             'server': 'global',
             'skills': [{'name': 'Phát Bắn Siêu Cấp',
                         'tags': ['Đánh Thường', 'Chuẩn Xác'],
                         'description': 'Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi 6 ô xung quanh</color>, gây '
                                        'ST Vật Lý bằng <color=#f26c1c>80%</color> Tấn Công.'},
                        {'name': 'Ánh Sáng Khế Ước',
                         'tags': ['Chủ Động', 'Cường Hóa'],
                         'description': 'Chọn 1 đồng minh (ngoại trừ bản thân) <color=#f26c1c>trong phạm vi 8 ô xung '
                                        'quanh</color> và áp dụng <color=#3487e0>Đồng Tâm Liên Kết</color>. Chỉ có thể '
                                        'tồn tại 1 Đồng Tâm Liên Kết cùng thời điểm. Sau khi dùng, Robella nhận '
                                        '<color=#3487e0>Chỉ Lệnh Bổ Sung</color>. Kỹ năng chỉ dùng 1 lần mỗi hiệp.'},
                        {'name': 'Ký Ức Rực Rỡ',
                         'tags': ['Chủ Động', 'Cường Hóa'],
                         'description': 'Robella nhận <color=#3487e0>Thăng Hoa Ánh Sáng</color> trong <color=#f26c1c>2 '
                                        'hiệp</color> (thời lượng giảm vào cuối hiệp hiện tại). Sau khi dùng kỹ năng, '
                                        'nhận <color=#3487e0>Lá Chắn Hàn Sương</color> trong <color=#f26c1c>2 '
                                        'hiệp</color>, hấp thu sát thương bằng <color=#f26c1c>65%</color> Tấn Công ban '
                                        'đầu, tối đa bằng <color=#f26c1c>60%</color> HP tối đa.'},
                        {'name': 'Cuồng Phong Gầm Thét',
                         'tags': ['Tuyệt Kỹ', 'AoE'],
                         'description': 'Chọn 1 hướng, gây ST Băng Kết AoE bằng <color=#f26c1c>120%</color> Tấn Công '
                                        'lên toàn bộ kẻ địch trong khu vực hình quạt 4 ô.'},
                        {'name': 'Hiểu Thấu Điểm Yếu',
                         'tags': ['Bị Động', 'Cường Hóa'],
                         'description': 'Khi kết thúc hành động, tăng Chỉ Số Nhiên Liệu thêm <color=#f26c1c>1 '
                                        'điểm</color>.\n'
                                        '\n'
                                        'Sau khi dùng <color=#3487e0>Thâm Nhập Băng Giá</color>, tiêu hao toàn bộ tầng '
                                        '<color=#3487e0>Hiểu Biết Chuyên Sâu</color> trên mục tiêu và nhận lượng tầng '
                                        'tương ứng của <color=#3487e0>Xác Định Điểm Yếu</color>. Khi số tầng Xác Định '
                                        'Điểm Yếu trên 2, đòn đánh thường chuyển thành ST Băng Kết và tăng tỷ lệ bạo '
                                        'kích thêm <color=#f26c1c>20%</color>.'}],
             'fortification': [{'tier': 1,
                                'level': 2,
                                'skill': 'Ánh Sáng Khế Ước',
                                'effect': 'Tăng Tấn Công của bản thân thêm 20% lượng Tấn Công ban đầu của đồng minh '
                                          'được chọn.'},
                               {'tier': 2,
                                'level': 2,
                                'skill': 'Ký Ức Rực Rỡ',
                                'effect': 'Thăng Hoa Ánh Sáng tăng sát thương gây ra lên <color=#f26c1c>50%</color>. '
                                          'Cường hóa hiệu ứng Thăng Hoa Ánh Sáng: Khi dùng Thâm Nhập Băng Giá, áp dụng '
                                          '1 tầng <color=#3487e0>Cú Sốc Ký Ức</color> lên mục tiêu trong 2 hiệp.'},
                               {'tier': 3,
                                'level': 2,
                                'skill': 'Hiểu Thấu Điểm Yếu',
                                'effect': 'Khi số tầng Xác Định Điểm Yếu trên 5, tăng ST Bạo Kích thêm 30% và tăng sát '
                                          'thương gây ra từ Thâm Nhập Băng Giá thêm 30%.'},
                               {'tier': 4,
                                'level': 2,
                                'skill': 'Cuồng Phong Gầm Thét',
                                'effect': 'Hệ số sát thương tăng lên 150% Tấn Công. Với mỗi tầng Xác Định Điểm Yếu, '
                                          'tăng hệ số sát thương thêm 9%.'},
                               {'tier': 5,
                                'level': 3,
                                'skill': 'Ký Ức Rực Rỡ',
                                'effect': 'Tăng thời lượng của Thăng Hoa Ánh Sáng thêm 2 hiệp (thời lượng giảm vào '
                                          'cuối hiệp hiện tại).'},
                               {'tier': 6,
                                'level': 3,
                                'skill': 'Hiểu Thấu Điểm Yếu',
                                'effect': 'Xác Định Điểm Yếu không còn giới hạn số tầng tối đa.'}],
             'keys': [{'name': 'Khóa Cố Định 1 - Lỗ Thông Phòng Vệ',
                       'effect': 'Trước khi đồng minh có Đồng Tâm Liên Kết thực hiện tấn công chủ động hoặc Chặn Đánh, '
                                 'áp dụng <color=#3487e0>Phòng Thủ Giảm II</color> lên mục tiêu trong <color=#f26c1c>2 '
                                 'hiệp</color>.'},
                      {'name': 'Khóa Cố Định 2 - Đám Mây Tâm Trí Đời Ba',
                       'effect': 'Khi kết thúc hành động, nếu Robella có Thăng Hoa Ánh Sáng, nhận <color=#3487e0>Tấn '
                                 'Công Tăng II</color> trong <color=#f26c1c>1 hiệp</color>.'},
                      {'name': 'Khóa Cố Định 3 - Chú Ý Đặc Biệt',
                       'effect': 'Phát Bắn Siêu Cấp: Sau khi dùng kỹ năng, nhận <color=#f26c1c>2 tầng</color> '
                                 '<color=#3487e0>Xác Định Điểm Yếu</color>.'},
                      {'name': 'Khóa Cố Định 4 - Nhỏ Hơn Cẩu Binh',
                       'effect': 'Nếu Robella hoặc đồng minh có Đồng Tâm Liên Kết gây ST Băng Kết lên kẻ địch có '
                                 'Khiên, tăng <color=#3487e0>Tỷ Lệ Xuyên Khiên</color> thêm <color=#f26c1c>30%</color> '
                                 'và sát thương tăng <color=#f26c1c>20%</color>.'},
                      {'name': 'Khóa Cố Định 5 - Bảo Hộ Mát Lạnh',
                       'effect': 'Nếu Robella đứng trên ô địa hình Băng Giá của đồng minh, nhận <color=#f26c1c>5 '
                                 'ô</color> <color=#3487e0>Di Chuyển Bổ Sung</color> sau khi dùng Phát Bắn Siêu Cấp '
                                 'hoặc Cuồng Phong Gầm Thét.'},
                      {'name': 'Khóa Cố Định 6 - Tâm Lặng Như Nước',
                       'effect': 'Trước khi dùng Thâm Nhập Băng Giá, giải trừ <color=#f26c1c>2</color> Buff của mục '
                                 'tiêu.'},
                      {'name': 'Khóa Tương Thích - Khế Ước Băng Giá',
                       'effect': 'Tấn Công +3%, HP +3%, ST Bạo Kích +3%'},
                      {'name': 'Khóa Chung - Công Lý Là Sức Mạnh',
                       'effect': 'Tấn Công +5% / Nếu người sở hữu có Khiên, tăng sát thương thuộc tính gây ra thêm '
                                 '<color=#f26c1c>10%</color>.'},
                      {'name': 'Khóa Mở Rộng - Thi Hành Công Lý',
                       'effect': 'Nếu sở hữu Thăng Hoa Ánh Sáng, dùng đòn đánh thường Phát Bắn Siêu Cấp sẽ nhận Chỉ '
                                 'Lệnh Bổ Sung. Kích hoạt tối đa 1 lần mỗi hiệp.\n'
                                 'Khi dùng Ký Ức Rực Rỡ hoặc khi kẻ địch mang Hiểu Biết Chuyên Sâu bị tiêu diệt bởi '
                                 'đồng minh, nhận 3 tầng Xác Định Điểm Yếu.\n'
                                 'Trước khi tấn công chủ động, tạo ô địa hình Băng Giá trong phạm vi 2 ô quanh bản '
                                 'thân trong 2 hiệp.'}]}}
