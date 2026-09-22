import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

EFFECTS_VI_PATH = ROOT / "data" / "effects_vi.json"

# Complete dictionary of accurate, professional Vietnamese translations for all contaminated effects
CLEAN_DESCRIPTIONS = {
    # Andoris & Electric mechanics
    "effect_351891a52fff": "Khi người sở hữu chịu ST Điện Từ đơn mục tiêu, ST Ổn Định phải chịu tăng thêm 1 điểm. Kẻ tấn công hồi phục HP bằng 20% sát thương gây ra. Thuộc loại Debuff Điện Từ và không thể giải trừ.",
    "effect_6f92238d9310": "Khi kết thúc hành động, hồi phục HP bằng 20% HP tối đa của bản thân. Nếu có đồng minh mang Điện Tích Dương trong phạm vi 3 ô, hồi phục thêm HP bằng 15% HP tối đa. Khi tấn công kẻ địch mang Điện Tích Âm, ST Điện Từ gây ra tăng 35%. Mỗi đơn vị mang Điện Tích Dương có thể kích hoạt hiệu ứng này tối đa 3 lần mỗi hiệp. Thuộc loại Buff Điện Từ.",
    "effect_2a4a2ffb7f98": "Khi người sở hữu chịu ST Điện Từ đơn mục tiêu, tất cả đơn vị mang Điện Tích Âm chịu ST cố định bằng 30% sát thương gây ra. Nếu bị áp dụng thêm Điện Tích Âm, người sở hữu chịu 1 lần ST cố định bằng 3% Tấn Công của người thi triển. Nếu bị tấn công bởi đơn vị mang Điện Tích Dương, ST Điện Từ phải chịu tăng thêm. Thuộc loại Debuff Điện Từ.",
    "effect_740313784e64": "Người sở hữu không còn nhận được sự bảo vệ từ Vật Cản (Yểm Hộ). Sát thương phải chịu giảm 20% và ST Ổn Định phải chịu giảm 2 điểm. Khi chịu sát thương, nếu kẻ tấn công đang chịu Debuff loại Điện Từ, sát thương phải chịu giảm thêm 15%. Không thể giải trừ.",
    "effect_540b7929c777": "Khi chịu sát thương chí tử, người sở hữu không bị hạ gục. Hồi phục HP bằng 30% HP tối đa của bản thân và 5 điểm Chỉ Số Ổn Định. Hiệu ứng này chỉ có thể kích hoạt 1 lần và không thể giải trừ.",
    "effect_ee98fd919e4e": "Phòng Thủ tăng 10%. Có thể cộng dồn tối đa 5 tầng. Thuộc loại Buff và không thể giải trừ.",
    "effect_31aaa8bf4d08": "Khi tấn công mục tiêu mang Điện Tích Âm, sát thương gây ra tăng 10%. Thuộc loại Buff Điện Từ và không thể giải trừ.",
    "effect_6afb56afe1a2": "Đòn tấn công gây ST Điện Từ, sát thương gây ra tăng thêm 30%, có hiệu lực trong 1 lần tấn công. Thuộc loại Buff và không thể giải trừ.",
    "effect_784071a3e70a": "Nếu Chỉ Số Ổn Định của mục tiêu ở mức 0 điểm, ST Ổn Định gây thêm được chuyển hóa thành ST Điện Từ bằng (ST Ổn Định cộng thêm × 5% Tấn Công). Đòn đánh này sẽ không kích hoạt hiệu ứng của Điện Tích Âm. Thuộc loại Buff và không thể giải trừ.",
    "effect_81a2d8548fbf": "Khi gây ST Điện Từ, nếu mục tiêu đang chịu Debuff Điện Từ, tăng thêm 15% ST Bạo Kích. Duy trì 2 hiệp. Thuộc loại Buff.",
    "effect_49a379bf069b": "Khi bắt đầu hiệp, nhận 1 tầng Tích Trữ Điện. Mỗi tầng tăng 5% ST Điện Từ gây ra, tối đa 4 tầng. Thuộc loại Buff.",

    # Sabrina & Suomi
    "effect_374cb49ca271": "Tấn Công tăng thêm bằng 15% Phòng Thủ của bản thân. Mở rộng phạm vi hiệu lực của kỹ năng bị động ra toàn bản đồ. Thuộc loại Buff và không thể giải trừ.",
    "effect_d3cb3c44b6d2": "Sau khi bị tấn công, Suomi hồi phục HP bằng 10% HP tối đa. Thuộc loại Buff.",
    "effect_6032a672e309": "Khi bị áp dụng hiệu ứng Debuff Băng Kết khác, nhận thêm 1 tầng Băng Giá. Khi đạt 5 tầng, chịu 8 điểm ST Ổn Định cố định. Thuộc loại Debuff Băng Kết.",
    "effect_658cd013c867": "Cấm Chỉ Lệnh, không thể di chuyển hoặc hành động. Hiệu ứng này bị xóa bỏ khi người sở hữu chịu sát thương. Thuộc loại Debuff Di Chuyển Băng Kết.",
    "effect_20d629daa780": "Khi đạt 4 tầng, kỹ năng chủ động Quy Tắc Anh Hùng nhận thêm hiệu ứng: bỏ qua 15% giảm thương từ Vật Cản của mục tiêu. Sát thương chuyển hóa thành ST Băng Kết và nếu mục tiêu đứng trên ô Băng Kết, sát thương gây ra tăng lên 130%. Có thể cộng dồn tối đa 4 tầng và có hiệu lực 1 lần. Không thể giải trừ.",
    "effect_ecb57fcb0cf8": "Sát thương phải chịu giảm 30%, tối đa cộng dồn 5 lớp. Tiêu hao 1 lớp sau khi bị tấn công. Thuộc loại Buff Băng Kết và không thể giải trừ.",
    "effect_b7b33d823b79": "Khi bị áp dụng hiệu ứng Debuff Băng Kết khác, nhận 1 lớp Tuyết Lở. Khi đạt 5 lớp, chịu 8 điểm ST Ổn Định cố định. Thuộc loại Debuff Băng Kết.",
    "effect_0f8b4450ce8d": "Khi Khiên hoặc Lá Chắn Hàn Sương bị phá vỡ, áp dụng Cứng Đờ trong 1 hiệp lên đơn vị đã phá vỡ nó. Thuộc loại Buff Băng Kết và không thể giải trừ.",
    "effect_e2113ab64534": "Tỷ Lệ Bạo Kích và ST Bạo Kích tăng thêm 3%, cộng dồn tối đa 8 tầng. Thuộc loại Buff và không thể giải trừ.",

    # Klukai & Corrosion
    "effect_cac8d399a428": "Khi kết thúc hành động, người thi triển gây ST Ăn Mòn AoE bằng 12% Tấn Công. Với mỗi tầng tăng thêm, hệ số sát thương tăng thêm 12%. Khi bị trúng đòn tấn công chủ động từ Klukai hoặc ST Ăn Mòn từ đồng minh khác, nhận thêm 1 tầng và làm mới thời gian duy trì, tối đa 10 tầng. Xóa bỏ khi người thi triển tử trận. Thuộc loại Debuff Ăn Mòn và không thể giải trừ.",
    "effect_c9757c9714b1": "Khi kết thúc hành động, nhận 1 tầng Áp Chế Ăn Mòn Mạnh trong 2 hiệp. Khi tử trận, người thi triển áp dụng Độc Tính Xâm Nhập trong 2 hiệp lên mục tiêu và tất cả kẻ địch trong phạm vi 3 ô, gây ST Ăn Mòn AoE bằng 60% Tấn Công. Xóa bỏ khi người thi triển tử trận. Thuộc loại Debuff Ăn Mòn.",
    "effect_fdfb2ca6b8e0": "Gây ST Ăn Mòn bằng 40% Tấn Công của Basti và 1 điểm ST Ổn Định cho đơn vị di chuyển vào hoặc kết thúc hành động trên ô này. Duy trì 2 hiệp.",
    "effect_ec0fc845d714": "Khi kẻ địch tiến vào phạm vi 2 ô xung quanh, tự phát nổ gây ST Ăn Mòn AoE bằng 120% Tấn Công của Basti, 2 điểm ST Ổn Định và tạo ô địa hình Độc Chướng trong 2 hiệp.",
    "effect_291868a45a59": "Khi bắt đầu hành động, chịu ST Ăn Mòn bằng 20% Tấn Công của Basti và giảm 1 điểm ST Ổn Định. Duy trì 2 hiệp. Thuộc loại Debuff Ăn Mòn.",

    # Centaureissi & Burn
    "effect_f3b2ec8a9136": "Hồi phục HP bằng 15% Tấn Công của Centaureissi khi kết thúc hành động. Duy trì 1 hiệp. Thuộc loại Buff Thiêu Đốt.",
    "effect_4198c100ed1f": "Khi kết thúc hành động, người thi triển gây ST Thiêu Đốt bằng 7% Tấn Công lên người sở hữu. Với mỗi tầng tăng thêm, hệ số sát thương tăng thêm 7%, sau đó đặt lại số tầng. Khi người sở hữu nhận ST Thiêu Đốt từ kẻ địch, số tầng tăng thêm 1. Có thể cộng dồn tối đa 12 tầng, xóa bỏ khi người thi triển tử trận. Thuộc loại Debuff Thiêu Đốt và không thể giải trừ.",
    "effect_fe4bac9b13fc": "Khi nhận hiệu ứng này và khi kết thúc hành động, bản thân và tất cả đơn vị đồng minh trong phạm vi 1 ô chịu ST cố định bằng 10% Tấn Công của người thi triển. Thuộc loại Debuff Thiêu Đốt.",

    # Faye & Physical
    "effect_334e02a19b2b": "ST Vật Lý phải chịu tăng 30%. Có thể kích hoạt đồng thời tối đa 8 lần (hiệu ứng này không cộng dồn tầng). Thuộc loại Debuff Phòng Thủ và không thể giải trừ.",
    "effect_34f4cc3ac706": "Khi kết thúc hành động, người thi triển gây ST Vật Lý cố định bằng 15% Tấn Công của Faye lên người sở hữu. Với mỗi tầng tăng thêm, sát thương tăng thêm 15% và số tầng được đặt lại. Khi nhận ST Vật Lý từ kẻ địch, nhận thêm 1 tầng. Tối đa 12 tầng. Xóa bỏ khi Faye tử trận. Thuộc loại Debuff Vật Lý và không thể giải trừ.",
    "effect_11c02d54c46f": "Không thể di chuyển. Thuộc loại Debuff Di Chuyển và Khống Chế.",

    # Balthilde
    "effect_cf0a24df6173": "Với mỗi Phụ Kiện Chịu Lực, tăng Phòng Thủ ban đầu của Balthilde thêm 20%, cộng dồn tối đa 3 tầng. Duy trì trong toàn bộ trận chiến. Thuộc loại Buff và không thể giải trừ.",
    "effect_8b61a8020764": "Khi tung đòn tấn công, bỏ qua 20% Phòng Thủ của mục tiêu và gây thêm 1 điểm ST Ổn Định. Duy trì 1 hiệp. Thuộc loại Buff.",
    "effect_eda7bd6275a7": "Phòng Thủ giảm 15%. Khi bị tấn công bởi Balthilde, chịu thêm ST Băng Kết bằng 30% Phòng Thủ của Balthilde. Thuộc loại Debuff.",

    # Cheyanne
    "effect_abfcfde8ffd9": "Tấn Công tăng 5%, cộng dồn tối đa 3 tầng. Mỗi tầng cung cấp thêm 1 ô tầm nhìn (không phải tầm bắn). Duy trì 2 hiệp. Thuộc loại Buff.",
    "effect_ffb3a635db82": "Khi bị Cheyanne tấn công, sát thương phải chịu tăng 10%. Thuộc loại Debuff Phòng Thủ.",
    "effect_ef41b94c55cb": "Tăng 20% sát thương gây ra cho đòn tấn công chủ động tiếp theo của Cheyanne. Tiêu hao 1 tầng khi tấn công. Thuộc loại Buff.",
    "effect_8326b70b9b6c": "Lượng sát thương phải chịu trước khi được giảm trừ bởi các hiệu ứng Lá Chắn và Vật Cản (Yểm Hộ).",
    "effect_028f2cb637bd": "Cheyanne sẽ không bị hạ gục khi đứng trên ô này.",

    # Generic & Other characters' contaminated effects
    "effect_ac9b1529046a": "Người sở hữu không nhận sát thương từ Đánh Thường hoặc kỹ năng. Hiệu ứng này bị giải trừ sau 1 lần nhận Đánh Thường hoặc kỹ năng. Thuộc loại Buff.",
    "effect_99dc16a98d3b": "ST Ổn Định gây ra tăng 1 điểm. Khi Chỉ Số Ổn Định của mục tiêu lớn hơn 0, khi dùng Đánh Thường, Sấm Chớp hoặc Đòn Đánh Tia Chớp tiêu hao toàn bộ tầng Khí, gây ST Ổn Định cố định bằng số tầng tiêu hao × 3 lên mục tiêu. Cộng dồn tối đa 5 tầng. Không thể giải trừ.",
    "effect_da802bd7d2f7": "Sát thương phải chịu từ Krolik tăng 15%. Duy trì 2 hiệp. Thuộc loại Debuff.",
    "effect_1e9ea006acaf": "Tự động hồi phục 15% HP tối đa khi kết thúc hành động. Duy trì 2 hiệp. Thuộc loại Buff.",
    "effect_e386f32e7e55": "Tăng 20% Phòng Thủ khi đứng sau Vật Cản. Thuộc loại Buff.",
    "effect_1a07cac31540": "Tốc độ di chuyển tăng 2 ô, Tấn Công tăng 20%. Không thể dùng kỹ năng chủ động. Duy trì 2 hiệp.",
    "effect_ddae7bbb0128": "Tạo màn che bóng tối bao phủ đồng minh, giảm 20% sát thương diện rộng phải chịu. Duy trì 2 hiệp. Thuộc loại Buff.",
    "effect_6d9fbf9f7bb5": "Không thể di chuyển hoặc dùng kỹ năng chủ động, không nhận giảm thương từ Vật Cản, miễn dịch với khống chế. Khi vào trạng thái này, áp dụng Màn Đêm Ác Mộng lên tất cả đồng minh, hủy Chế Độ Chắp Vá và chuyển sang Chế Độ Tăng Áp. Tất cả đồng minh nhận Hộ Vệ Giấc Mơ. Với mỗi 10 điểm Chỉ Số Nhiên Liệu tiêu hao, áp dụng Màn Đêm Ác Mộng cho tất cả đồng minh.",
    "effect_ed49b04c73fc": "Lượng trị liệu nhận được tăng thêm 20%. Thuộc loại Buff.",
    "effect_11d839459a25": "Liên kết sinh mệnh với mục tiêu chỉ định, chia sẻ 30% sát thương phải chịu. Thuộc loại Buff.",
    "effect_8fb14690f10f": "Khi đòn tấn công chủ động gây ST Hóa Lỏng, nhận 1 điểm Chỉ Số Nhiên Liệu, kích hoạt tối đa 1 lần mỗi hiệp. Thuộc loại Buff Hóa Lỏng và không thể giải trừ.",
    "effect_c856fb949a80": "Đầu tư tích lũy nhiệt lượng, tăng 10% ST Bạo Kích cho đòn tấn công tiếp theo. Thuộc loại Buff.",
    "effect_528e46f5861d": "Bảo vệ vốn tài chính, nhận Lá Chắn bằng 20% HP tối đa khi kết thúc hành động. Thuộc loại Buff.",
    "effect_2aa3d45bbb31": "Khi đồng minh gây ST Vật Lý bằng tấn công chủ động, bỏ qua 15% Phòng Thủ của mục tiêu. Có thể cộng dồn tối đa 4 tầng. Khi đồng minh gây sát thương nguyên tố, hiệu ứng này mất hiệu lực trong 2 hiệp (thời gian duy trì giảm khi kết thúc hiệp hiện tại). Không thể giải trừ.",
    "effect_678fc1ecbd05": "Khi kích hoạt, Lind áp dụng 3 Debuff mạnh ngẫu nhiên lên người sở hữu, giải trừ 1 Buff và thực hiện Tấn Công Chi Viện, gây ST Ăn Mòn AoE bằng 80% Tấn Công cùng 1 điểm ST Ổn Định. Thuộc loại Debuff Ăn Mòn và không thể giải trừ.",
    "effect_be0cebe081e4": "Nếu hiệu ứng này cộng dồn đủ 5 tầng, khi bắt đầu hiệp tiếp theo, kích hoạt 1 lần hiệu ứng bị động Mắt Ngao Trắng. Kích hoạt tối đa 1 lần mỗi trận chiến và không thể giải trừ.",
    "effect_ecaf18ff77a1": "ST Thiêu Đốt của Lewis tăng thêm 15% và Tỷ Lệ Bạo Kích tăng 10%.",
    "effect_f3705687a883": "Trước khi Lewis tung Tuyệt Kỹ Lễ Hội Đồ Chơi, thực hiện thêm 1 lần Cùng Bắn. Đòn Cùng Bắn bổ sung này không tăng Chỉ Số Nhiên Liệu và không tiêu hao Quân Lệnh Lính Chì. Cung cấp Lửa Rực Cháy.",
    "effect_4df8a3399ef7": "Lính Chì gây ST Thiêu Đốt chỉ định bằng 100% Tấn Công của Lewis cùng 1 điểm ST Ổn Định bỏ qua Vật Cản. Mỗi cấp Cấp Bậc tăng hệ số sát thương của đòn tấn công này thêm 10%. Đòn đánh này không kích hoạt từ Tấn Công Chi Viện, Chặn Đánh hoặc Phản Kích. Cung cấp 3 điểm Lửa Rực Cháy và hồi 1 điểm Chỉ Số Nhiên Liệu cho Lewis.",
    "effect_b719128321aa": "Ngăn chặn Phòng Thủ của người sở hữu bị giảm xuống dưới 100%. Hủy bỏ khi HP của người sở hữu giảm xuống dưới 30%. Không thể giải trừ.",
    "effect_e1f841f652e4": "Tăng 10% Tấn Công khi đứng gần đồng đội có cùng dấu ấn. Thuộc loại Buff.",
    "effect_531b39ba5aa1": "Hồi phục ngay lập tức 2 điểm Chỉ Số Nhiên Liệu và tăng 1 ô Tầm Di Chuyển. Thuộc loại Buff.",
    "effect_a872beaab1ab": "Giảm 15% sát thương phải chịu khi đang chịu trạng thái phụ thuộc. Thuộc loại Buff.",
    "effect_d10ca41e833d": "Mục tiêu rơi vào trạng thái hoảng loạn, giảm 2 ô Tầm Di Chuyển và không thể nhận lệnh tấn công. Thuộc loại Debuff Khống Chế.",
    "effect_0e5c64981489": "ST Tấn Công Chi Viện tăng 15%, sát thương lên mục tiêu lộ diện tăng 10%. Kích hoạt 1 lần. Buff này không thể giải trừ.",
    "effect_c05ec76ac45c": "ST Tấn Công Chi Viện tăng 30%, sát thương lên mục tiêu lộ diện tăng 10%. Kích hoạt 1 lần. Buff này không thể giải trừ.",

    # Newly identified contaminated / hybrid effects
    "effect_413df243ccf6": "Nếu mục tiêu mà Taryz đang theo sau gây sát thương lên một đơn vị đồng minh, Taryz sẽ thực hiện Phản Kích lên mục tiêu đó và hồi phục HP cho đơn vị đồng minh. Khi mục tiêu mà Taryz đang theo sau tử trận, Taryz chuyển sang theo sau đơn vị địch có lượng HP hiện tại cao nhất.",
    "effect_ebc79a18e5f5": "Vật triệu hồi chiếm giữ ô địa hình trên chiến trường và sở hữu các thuộc tính riêng (ví dụ: Đội Vệ Binh Thành Phố của Papasha, Ụ Pháo Tự Động của Andoris, Kulich của Nikketa,...).",
    "effect_ea4bfc5e86a0": "Vật triệu hồi chiếm giữ ô địa hình trên chiến trường và sở hữu các thuộc tính riêng (ví dụ: Đội Vệ Binh Thành Phố của Papasha, Ụ Pháo Tự Động của Andoris, Kulich của Nikketa,...).",
    "effect_ff91a1c70507": "Dựa trên 3 Bước Nhảy đầu tiên được áp dụng: với mỗi Xoay Người Duyên Dáng, hồi phục HP bằng 15% HP tối đa cho tất cả đồng minh; với mỗi Xoay Người Nồng Nhiệt, giải trừ 1 Debuff cho tất cả đồng minh. Nếu Vũ Công Xuất Sắc đã được kích hoạt trong hiệp này, hoạt ảnh kỹ năng sẽ không hiển thị nhưng hiệu ứng vẫn được áp dụng.",
    "effect_9762753784db": "Tích lũy 10% sát thương cuối cùng của Lainie hoặc Ảo Ảnh làm giá trị sát thương. Nếu thỏa mãn điều kiện, tích lũy 25% sát thương cuối cùng của Lainie hoặc Ảo Ảnh. Khi nhận một đòn tấn công chủ động từ Lainie hoặc Ảo Ảnh, gây thêm ST cố định dựa trên giá trị sát thương tích lũy. Không thể giải trừ.",
    "effect_51925173fbec": "Nếu đơn vị có Khiên Thần chịu sát thương trong phạm vi 6 ô tính từ Helen, cô ấy sẽ gánh chịu thay 100% lượng sát thương ban đầu đó.",
    "effect_88ffd91dbfb2": "Sau khi kết thúc hành động, hoàn nguyên về trạng thái tại thời điểm nhận hiệu ứng này (bao gồm tất cả giá trị thuộc tính, số tầng hiệu ứng và thời gian duy trì còn lại). Không thể giải trừ.",
    "effect_4d46cad98b36": "Ấn ký chuyên dụng của Sextans. Bị xóa bỏ khi người thi triển tử trận. Không thể giải trừ.",
    "effect_f2b3358f0f60": "Tăng ST Ổn Định thêm 3 điểm và cho phép bỏ qua 3 điểm Chỉ Số Ổn Định của mục tiêu. Khi gây ST Điện Từ hoặc sát thương cận chiến, sát thương gây ra tăng 3% dựa trên số tầng Đông Tụ mà Sextans sở hữu.",
    "effect_6bb0f520500a": "Trước khi tấn công chủ động, tạo các ô địa hình Băng Giá trong bán kính 2 ô xung quanh mục tiêu trong 2 hiệp, và sát thương gây ra khi tấn công các đơn vị địch đứng trên ô nguyên tố sẽ tăng thêm 20%. Thuộc loại Buff và không thể giải trừ.",
    "effect_fd3980f9414e": "Khi Mityl hoặc Ảo Ảnh gây ST Hóa Lỏng, tăng sát thương gây ra thêm 5% cho mỗi đơn vị đồng minh trên chiến trường (ngoại trừ Mityl), tối đa 40%. Thuộc loại Buff và không thể giải trừ.",
    "effect_7f967adfaa29": "Thực hiện 1 Đòn Đánh Khóa Mục Tiêu lên mục tiêu, gây sát thương cận chiến ST Vật Lý bằng 80% Tấn Công của người sở hữu buff, bỏ qua giảm thương từ Vật Cản và gây 2 điểm ST Ổn Định. Sau đòn tấn công này, Asteria nhận 1 điểm Chỉ Số Nhiên Liệu.",
    "effect_f77608436f1c": "Bao gồm hai tư thế Ưng Kích và Đòn Vuốt Nặng. Nếu Eagletta đang ở tư thế Ưng Kích, tư thế sẽ chuyển sang Đòn Vuốt Nặng khi kích hoạt, và ngược lại. Chỉ có thể tồn tại một tư thế tại một thời điểm.",
    "effect_b2b8b44d94ba": "Đánh Thường của Eagletta đổi thành Vuốt Xé Rách, và Tầm Di Chuyển tăng 2 ô. Vuốt Xé Rách và kỹ năng bị động Săn Mồi bỏ qua 5% Phòng Thủ của mục tiêu. Eagletta chịu ít hơn 20% sát thương từ các mục tiêu nằm ngoài phạm vi 3×3 ô xung quanh cô ấy. Khi kết thúc hiệp, Eagletta nhận 1 Lông Vũ Chiến Tranh. Dựa trên số Lông Vũ Chiến Tranh tiêu hao trong hiệp hiện tại, hệ số sát thương của Vuốt Xé Rách và kỹ năng bị động Săn Mồi tăng 5%. Không thể giải trừ.",
    "effect_71e57415376d": "Mỗi khi đơn vị đồng minh tung đòn tấn công chủ động gây sát thương, Sextans nhận 1 tầng Đông Tụ, tối đa 12 tầng. Với mỗi tầng Đông Tụ sở hữu, Tấn Công của cô ấy tăng 3% và lượng trị liệu tăng bằng 4% Tấn Công. Thuộc loại Buff và không thể giải trừ.",
    "effect_6197bedffc18": "Khi tấn công các mục tiêu đang chịu Debuff Thiêu Đốt, sát thương gây ra tăng 15%. Thuộc loại Buff.",
    "effect_5c055c56df1a": "Khi tấn công các mục tiêu đang chịu Debuff Thiêu Đốt, ST Bạo Kích tăng 20%. Thuộc loại Buff.",
    "effect_bbb69c2d08e3": "ST Thiêu Đốt phải chịu tăng 10%. Thuộc loại Debuff.",
    "effect_deb25ad68d64": "Khi gây ST Thiêu Đốt, bỏ qua 10% Phòng Thủ của mục tiêu. Thuộc loại Buff.",
    "effect_d3c5f15508b7": "Tăng tầm nhìn thêm 2 ô và tăng 10% Tỷ Lệ Bạo Kích lên các mục tiêu bị phát hiện.",
    "effect_6cbcf6e32dec": "Giảm 15% tất cả sát thương phải chịu và tăng khả năng kháng Debuff.",
    "effect_49432c9f6bdf": "Tầm Di Chuyển tăng 2 ô. Bỏ qua giảm thương từ Vật Cản khi tấn công các mục tiêu.",
    "effect_10f51d324e02": "Tầm Di Chuyển tăng 1 ô. Sát thương gây ra tăng 10%.",
    "effect_86bc0f542958": "Phòng Thủ tăng 15%.",
    "effect_6ed7a4d2ea86": "Khi bắt đầu hành động này, hồi phục 10% HP tối đa.",
    "effect_b745e8ecbebe": "Khi thực hiện Hành Động Chi Viện, Tầm Di Chuyển tăng 1 ô. Thuộc loại Buff.",
    "effect_4b31eb617fbc": "Khi đơn vị này di chuyển từ 4 ô trở lên, nhận 1 tầng Tăng Tốc.",
    "effect_8507d631e229": "Bỏ qua giảm thương từ Vật Cản và tăng 20% ST Bạo Kích lên các mục tiêu. Thuộc loại Buff.",
    "effect_a9071d0cd33a": "Ngăn chặn mục tiêu thực hiện hành động trong 1 hiệp.",
    "effect_9eeb67146551": "Khi tấn công, gây thêm ST cố định dựa trên lượng HP đã mất của mục tiêu. Thuộc loại Buff.",
    "effect_cd3b8361ea9b": "Bỏ qua 10% Phòng Thủ của mục tiêu. Thuộc loại Buff.",
    "effect_7c76ee047d41": "Bỏ qua 15% Phòng Thủ của mục tiêu với mỗi Buff có trên bản thân. Thuộc loại Buff.",
    "effect_5ae2c6eed3cb": "Khi ở dạng này, tăng 20% Tấn Công và 1 ô Tầm Di Chuyển.",
    "effect_731a96515b90": "Khi ở dạng này, Tỷ Lệ Bạo Kích tăng 20% và ST Bạo Kích tăng 25%.",
    "effect_4faf1f402076": "Kế thừa 80% các thuộc tính của người thi triển.",
    "effect_6856ab276a16": "Kế thừa 60% các thuộc tính của người thi triển.",
    "effect_6b943acc3a9a": "Miễn nhiễm với các hiệu ứng Debuff cho đến khi kết thúc hành động.",
    "effect_6d7552d556dc": "Khi kết thúc hành động, chịu ST cố định bằng 20% Tấn Công của người thi triển.",
    "effect_8a89966de128": "Mục tiêu này chịu thêm 15% sát thương từ mọi nguồn. Thuộc loại Debuff.",
    "effect_15e96ed31ea7": "Đòn tấn công này tăng thêm 25% sát thương.",
    "effect_a4e7e4aa86f7": "Đơn vị này tăng thêm 20% sát thương diện rộng AoE. Thuộc loại Buff.",
    "effect_db2f3ba0d2b0": "Chịu thêm 20% sát thương từ các đòn tấn công xuyên thấu.",
    "effect_da1b8232b47c": "Mục tiêu bị đe dọa và giảm 10% Tấn Công.",
    "effect_47fe179b91fd": "Tiến lên và tấn công kẻ địch theo mệnh lệnh của cô ấy.",
    "effect_09d463e32b04": "Hỗ trợ cô ấy trong chiến đấu và mô phỏng các đòn tấn công của cô ấy.",
    "effect_946a9f028780": "Tăng Tấn Công của cô ấy và cho phép tung các đòn đánh tầm xa.",
    "effect_281a3ac670d4": "Tăng Độ Ổn Định của tất cả các đơn vị đồng minh.",

    # 27 newly translated remaining contaminated effects
    "effect_b1678d11897b": "Mất khả năng điều khiển, chủ động di chuyển về phía người thi triển. Hiệu ứng này bị xóa bỏ khi người thi triển tử trận.",
    "effect_d1cbf288c831": "Tầm Di Chuyển tăng 1 ô, miễn nhiễm với các hiệu ứng dịch chuyển vị trí từ đơn vị địch. Hiệu ứng này không thể giải trừ.",
    "effect_112963b7af6f": "Sát thương phải chịu từ Makiatto tăng 15%. Thuộc loại Debuff và không thể giải trừ.",
    "effect_29954eba93c1": "Vật triệu hồi vật lý với 2000 HP, kế thừa các thuộc tính khác của Makiatto. Có thể tồn tại tối đa 3 vật triệu hồi loại này trên chiến trường cùng lúc.",
    "effect_157bfbac4ca2": "Trước khi di chuyển, chịu ST cố định bằng 10% Tấn Công từ đơn vị đã áp dụng hiệu ứng này. Thuộc loại Debuff Di Chuyển Băng Kết.",
    "effect_009fad1b29a5": "Khi người sở hữu debuff này chịu sát thương, hồi phục HP cho kẻ tấn công bằng 20% sát thương gây ra. Thuộc loại Debuff Hóa Lỏng.",
    "effect_75068cc27966": "Khi người sở hữu chịu ST Thiêu Đốt, tạo các ô địa hình Thiêu Rụi trong phạm vi 3 ô tồn tại trong 2 hiệp. Thuộc loại Debuff Thiêu Đốt và không thể giải trừ.",
    "effect_309ecd97c70c": "Áp dụng Điểm Yếu Thiêu Đốt lên kẻ địch đứng trên ô này. Khi kết thúc hành động, áp dụng Tràn Lửa và Bốc Cháy trong 2 hiệp lên kẻ địch đứng trên ô. Đây là ô địa hình thuộc tính Thiêu Đốt.",
    "effect_a838bd1ad378": "Khi gây ST Vật Lý, nếu mức Giảm Phòng Thủ của mục tiêu vượt quá 100%, với mỗi phần trăm Giảm Phòng Thủ tăng thêm, sát thương gây ra tăng theo tỉ lệ: Giảm Phòng Thủ bổ sung < 100%: 0.5%; 100% <= Giảm Phòng Thủ bổ sung < 200%: 0.75%; 200% <= Giảm Phòng Thủ bổ sung < 300%: 1%; Giảm Phòng Thủ bổ sung >= 300%: 1.5%. Thuộc loại Buff và không thể giải trừ.",
    "effect_d3ce4618efaa": "Khi kết thúc hành động, nếu người sở hữu ở trong bán kính 8 ô tính từ Robella, tung Xâm Nhập Băng Giá lên mục tiêu đó và tăng hệ số sát thương của Xâm Nhập Băng Giá thêm 3%. Có thể cộng dồn tối đa 6 lần. Không thể giải trừ.",
    "effect_1ae3330c9341": "Nâng cấp Đoàn Kết và Hiểu Biết Chuyên Sâu thành Đoàn Kết: Cường Hóa và Hiểu Biết Chuyên Sâu: Cường Hóa. Tăng sát thương bản thân gây ra thêm 30%. Không thể giải trừ.",
    "effect_df8f1c65e6a1": "Tăng hệ số sát thương của Siêu Phát Bắn và Lốc Xoáy Gào Thét thêm 9%. Có thể cộng dồn tối đa 10 lần. Thuộc loại Buff và không thể giải trừ.",
    "effect_428154d2f9ef": "Tầm Di Chuyển giảm 1 ô. Có thể cộng dồn tối đa 5 lần. Hiệu ứng này được tính là hiệu ứng Băng Giá và thuộc loại Debuff Băng Kết.",
    "effect_45d88fb1ed53": "Khi gây sát thương lên kẻ địch có Lá Chắn, bỏ qua tỉ lệ phần trăm Lá Chắn được chỉ định để gây sát thương trực tiếp vào HP của mục tiêu.",
    "effect_e9fe31d1bb9f": "Tấn Công tăng 15%. Sau khi gây sát thương lên các mục tiêu có Phòng Thủ lớn hơn 0, hiệu ứng này bị xóa bỏ. Thuộc loại Buff và không thể giải trừ.",
    "effect_5cf37dbca163": "Khi nhận sát thương từ Lainie hoặc Ảo Ảnh của Lainie, Phòng Thủ giảm 15%. Có thể cộng dồn tối đa 3 lần. Thuộc loại Debuff Phòng Thủ và không thể giải trừ.",
    "effect_dc611916238f": "ST Hóa Lỏng phải chịu tăng 10%. Khi kết thúc hành động, gây ST Vật Lý AoE bằng 1% Tấn Công lên tất cả kẻ địch trong bán kính 5 ô. Thuộc loại Debuff Hóa Lỏng và không thể giải trừ.",
    "effect_d06952e2cc31": "Tấn Công tăng 10% và Phòng Thủ tăng 30%. Thuộc loại Buff và không thể giải trừ.",
    "effect_58f60e582d1c": "ST Băng Kết phải chịu tăng 20%. Hiệu ứng này bị xóa bỏ khi nhận Sương Giá. Thuộc loại hiệu ứng Băng Kết và không thể giải trừ.",
    "effect_db167f6762f6": "Sử dụng Lửa Thiêu Rụi làm bộ đếm giá trị. Khi Lửa Thiêu Rụi đạt 35 tầng, tiêu hao toàn bộ điểm Lửa Thiêu Rụi và áp dụng Tàn Tro cho tất cả các đơn vị đồng minh.",
    "effect_c0c7a8485bf1": "Nếu người sở hữu ở trong bán kính 8 ô xung quanh Basti trước khi tấn công, 1 tầng hiệu ứng này sẽ bị tiêu hao và Basti kích hoạt Chi Viện Đặc Biệt, gây ST Ăn Mòn AoE bằng 100% Tấn Công lên người sở hữu. Có thể cộng dồn tối đa 1 tầng. Thuộc loại Debuff Ăn Mòn. Không thể giải trừ.",
    "effect_88a2d0bb889e": "Không thể tấn công, không thể bị chọn làm mục tiêu và sẽ không bị hạ gục. Khi bắt đầu hiệp, hồi phục 30% HP tối đa. Không thể giải trừ.",
    "effect_c0be876334a8": "Khi một đơn vị địch trong bán kính 9 ô chịu ST Chuẩn Xác hoặc sát thương AoE từ các đơn vị đồng minh, tung 1 lần Hành Động Chi Viện, gây ST Ăn Mòn bằng 60% Tấn Công cùng 1 điểm ST Ổn Định, và hồi phục 1 điểm Chỉ Số Nhiên Liệu. Có thể kích hoạt tối đa 2 lần mỗi hiệp. Không thể giải trừ.",
    "effect_ec38ef23e6d7": "Cô Độc: Nhận 1 tầng Điềm Dữ. Nếu không có đơn vị đồng minh nào trong bán kính 4 ô tính từ Nemesis, sát thương gây ra tăng 60%. Khi bắt đầu hiệp của Nemesis, nhận 1 tầng Điềm Dữ. Không thể giải trừ.",
    "effect_dc7062a25ec0": "Tai Họa: Sau khi gây ST Chuẩn Xác, nếu mục tiêu chưa bị tiêu diệt, gây ST Ăn Mòn AoE bằng 60% Tấn Công cùng 1 điểm ST Ổn Định lên tất cả các đơn vị địch trong bán kính 3 ô xung quanh mục tiêu đó. Nếu hiệu ứng này được kích hoạt ngoài hiệp của Nemesis, nó được tính là Hành Động Chi Viện. Không thể giải trừ.",
    "effect_725efe82415d": "Ấn ký độc quyền của Soppo. Không thể bị tiêu hao. Không thể giải trừ.",
    "effect_79027f089bb2": "Vật triệu hồi của Koleda. Kế thừa 100% các chỉ số cơ bản của Koleda. Không thể điều khiển thủ công di chuyển lên vùng đất cao.",
}

def main():
    print(f"Loading {EFFECTS_VI_PATH}...")
    with open(EFFECTS_VI_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    updated_count = 0
    for eff_id, clean_desc in CLEAN_DESCRIPTIONS.items():
        if eff_id in data:
            old_desc = data[eff_id].get("desc", "")
            if old_desc != clean_desc:
                data[eff_id]["desc"] = clean_desc
                updated_count += 1
                print(f"Updated {eff_id} ({data[eff_id].get('name_en')} / {data[eff_id].get('name')})")

    print(f"\nTotal effects updated: {updated_count}")
    with open(EFFECTS_VI_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {EFFECTS_VI_PATH} successfully!")

if __name__ == "__main__":
    main()
