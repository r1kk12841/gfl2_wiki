from __future__ import annotations

import copy
import hashlib
from typing import Any


def effect_id(name_en: str) -> str:
    """Return a stable, name-independent-at-runtime identifier for an English effect."""
    digest = hashlib.sha1(name_en.strip().encode("utf-8")).hexdigest()[:12]
    return f"effect_{digest}"


def canonicalize_effects(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Read legacy name-keyed or v2 ID-keyed data and return the v2 ID map."""
    unique_by_en: dict[str, dict[str, Any]] = {}
    for key, raw in data.items():
        if not isinstance(raw, dict):
            continue
        name_en = raw.get("name_en")
        if not isinstance(name_en, str) or not name_en.strip():
            continue
        entry = copy.deepcopy(raw)
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id.startswith("effect_"):
            entry_id = key if key.startswith("effect_") else effect_id(name_en)
        entry["id"] = entry_id
        unique_by_en.setdefault(name_en, entry)

    id_by_en = {name_en: entry["id"] for name_en, entry in unique_by_en.items()}
    result: dict[str, dict[str, Any]] = {}
    for name_en, entry in unique_by_en.items():
        sub_ids = entry.get("sub_effect_ids")
        if not isinstance(sub_ids, list):
            sub_ids = [id_by_en[name] for name in entry.get("sub_effects", []) if name in id_by_en]
        normalized = {
            "id": entry["id"],
            "name": str(entry.get("name", name_en)),
            "name_en": name_en,
            "desc": str(entry.get("desc", entry.get("desc_en", ""))),
            "desc_en": str(entry.get("desc_en", entry.get("desc", ""))),
            "type": str(entry.get("type", "effect")),
            "sub_effect_ids": [item for item in sub_ids if item in {e["id"] for e in unique_by_en.values()}],
        }
        result[normalized["id"]] = normalized
    return result


EFFECT_ALIASES: dict[str, str] = {
    # Synonyms / Alternative Translations -> Canonical Effect ID or Name
    "nơi trú ẩn": "effect_a8fbb45be7f6",  # Yểm Hộ / Shelter
    "yểm hộ": "effect_a8fbb45be7f6",
    "tăng công i": "effect_fd27624b3d3e",  # Tấn Công Tăng I / Attack Up I
    "tăng công ii": "effect_247c609026e5",  # Tấn Công Tăng II / Attack Up II
    "tấn công tăng i": "effect_fd27624b3d3e",
    "tấn công tăng ii": "effect_247c609026e5",
    "giảm công i": "effect_6f5e94a06fd6",  # Tấn Công Giảm I / Attack Down I
    "tấn công giảm i": "effect_6f5e94a06fd6",
    "tăng thủ i": "effect_5e00d2315910",  # Phòng Thủ Tăng I / Defense Up I
    "tăng thủ ii": "effect_de1a5d2ad86f",  # Phòng Thủ Tăng II / Defense Up II
    "phòng thủ tăng i": "effect_5e00d2315910",
    "phòng thủ tăng ii": "effect_de1a5d2ad86f",
    "giảm thủ i": "effect_44846e36a8e2",  # Phòng Thủ Giảm I / Defense Down I
    "giảm thủ ii": "effect_5d454095ff39",  # Phòng Thủ Giảm II / Defense Down II
    "phòng thủ giảm i": "effect_44846e36a8e2",
    "phòng thủ giảm ii": "effect_5d454095ff39",
    "tăng di chuyển i": "effect_87b35208250c",  # Di Chuyển Tăng I / Movement Up I
    "tăng di chuyển ii": "effect_40ab16ddd687",  # Di Chuyển Tăng II / Movement Up II
    "di chuyển tăng i": "effect_87b35208250c",
    "di chuyển tăng ii": "effect_40ab16ddd687",
    "giảm di chuyển i": "effect_86e780aa86a9",  # Di Chuyển Giảm I / Movement Down I
    "giảm di chuyển ii": "effect_937a51c7ee7f",  # Di Chuyển Giảm II / Movement Down II
    "di chuyển giảm i": "effect_86e780aa86a9",
    "di chuyển giảm ii": "effect_937a51c7ee7f",
    "tăng tỷ lệ bạo kích i": "effect_61582b05fd89",  # TL Bạo Kích Tăng I / Critical Rate Boost I
    "tăng tỷ lệ bạo kích ii": "effect_9b6e378b1399",  # TL Bạo Kích Tăng II / Critical Rate Boost II
    "tl bạo kích tăng i": "effect_61582b05fd89",
    "tl bạo kích tăng ii": "effect_9b6e378b1399",
    "tỷ lệ bạo kích tăng i": "effect_61582b05fd89",
    "tỷ lệ bạo kích tăng ii": "effect_9b6e378b1399",
    "tăng sát thương i": "effect_5946130d4f87",  # ST tăng I / Damage Up I
    "tăng st i": "effect_5946130d4f87",
    "st tăng i": "effect_5946130d4f87",
    "dễ tổn thương i": "effect_3f848b4f2f07",  # Dễ Bị Thương I / Vulnerable I
    "dễ tổn thương ii": "effect_9bc4df85f23c",  # Dễ Bị Thương II / Vulnerable II
    "dễ bị thương i": "effect_3f848b4f2f07",
    "dễ bị thương ii": "effect_9bc4df85f23c",
    "thế công rực lửa": "effect_914c68a15887",  # Thế Công Rực Lửa I / Blazing Assault I
    "thế công rực lửa i": "effect_914c68a15887",
    "thế công rực lửa ii": "effect_7b125762331b",  # Thế Công Rực Lửa II / Blazing Assault II
    "xung kích thiêu đốt": "effect_914c68a15887",
    "xung kích thiêu đốt i": "effect_914c68a15887",
    "xung kích thiêu đốt ii": "effect_7b125762331b",
    "phục hồi nhiệt lượng": "effect_f3b2ec8a9136",  # Hồi Phục Trạng Thái Nhiệt / Heat Recovery
    "hồi phục trạng thái nhiệt": "effect_f3b2ec8a9136",
    "đóng băng": "effect_939f868537a1",  # Ngưng Tụ / Frozen
    "ngưng tụ": "effect_939f868537a1",
    "hàn ý": "effect_157bfbac4ca2",  # Rét Buốt / Cold Snap
    "rét buốt": "effect_157bfbac4ca2",
    "quá nhiệt": "effect_fe4bac9b13fc",  # Tràn Lửa / Overburn
    "tràn lửa": "effect_fe4bac9b13fc",
    "thấu suốt": "effect_1ed1264f96b2",  # Nhìn Thấu / Insight
    "nhìn thấu": "effect_1ed1264f96b2",
    "cận cảnh": "effect_e59ac86a75de",  # Khóa Mục Tiêu / Zoom In
    "khóa mục tiêu": "effect_e59ac86a75de",
    "lá chắn nhanh": "effect_b54a2b06722c",  # Lá Chắn Tốc Độ / Quick Barrier
    "lá chắn tốc độ": "effect_b54a2b06722c",
    "hỗ trợ hành động": "effect_49d5675f8edb",  # Hành Động Chi Viện / Action Support
    "hành động chi viện": "effect_49d5675f8edb",
    "sợ hãi": "effect_689e027c2657",  # Chạy Trốn / Fear
    "chạy trốn": "effect_689e027c2657",
    "trị liệu liên tục ii": "effect_67cce02e9b4e",  # Duy Trì Chữa Lành II / Continuous Healing II
    "duy trì chữa lành ii": "effect_67cce02e9b4e",
    "ăn mòn axit ii": "effect_d3d71700dbd7",  # Ăn Mòn Mạnh II / Acid Corrosion II
    "ăn mòn mạnh ii": "effect_d3d71700dbd7",
    "quy tắc săn mồi": "effect_6eb9e144a2c9",
    "hệ thống mắt sói": "effect_20379010bbdf",
    "chỉ lệnh bổ sung": "effect_66241cc2ad8d",
    "di chuyển bổ sung": "effect_16f39fae7c94",
    # Batch 2 additions
    "tăng sát thương ii": "effect_a251940c4ac7",  # ST Tăng II / Damage Up II
    "st tăng ii": "effect_a251940c4ac7",
    "tăng st ii": "effect_a251940c4ac7",
    "tăng st bạo kích i": "effect_3bfb0932b179",  # ST Bạo Kích Tăng I / Critical Damage Up I
    "tăng st bạo kích ii": "effect_ef43b0e2237a",  # ST Bạo Kích Tăng II / Critical Damage Up II
    "trị liệu liên tục i": "effect_7576b592a976",  # Duy Trì Chữa Lành I / Continuous Healing I
    "duy trì chữa lành i": "effect_7576b592a976",
    "hành động bổ sung": "effect_22ef658d9460",  # Tăng Hành Động / Extra Action
    "gai sáng": "effect_e2113ab64534",  # Gai Ánh Sáng / Lightspike
    "tăng tấn công chuẩn xác ii": "effect_99ae68bb3090",  # Chuẩn Xác Tăng II / Targeted Attack Boost II
    "tấn công chuẩn xác tăng ii": "effect_99ae68bb3090",
    "chuẩn xác tăng ii": "effect_99ae68bb3090",
    "thuộc tính tăng ii": "effect_6b682a52a725",  # Dị Vị Tăng II / Phase Boost II
    "tăng thuộc tính ii": "effect_6b682a52a725",
    "dị vị tăng ii": "effect_6b682a52a725",
    "no nê": "effect_374cb49ca271",  # No Bụng / Feeling Full
    "no bụng": "effect_374cb49ca271",
    "cường hóa chi viện i": "effect_0e5c64981489",  # Tăng Chi Viện I / Support Boost I
    "cường hóa chi viện ii": "effect_c05ec76ac45c",  # Tăng Chi Viện II / Support Boost II
    "tăng chi viện i": "effect_0e5c64981489",
    "tăng chi viện ii": "effect_c05ec76ac45c",
    "điều âm": "effect_221b75185057",  # Chỉnh Âm / Tuning
    "chỉnh âm": "effect_221b75185057",
    "chuẩn cao độ": "effect_1c4b0835d885",  # Định Âm / Pitch Perfect
    "chính âm": "effect_1c4b0835d885",
    "định âm": "effect_1c4b0835d885",
    "chặn đánh": "effect_e1db8d557124",  # Chặn Đánh / Interception
    "đánh chặn": "effect_e1db8d557124",
    "phục kích": "effect_e1db8d557124",
    "vô hiệu hóa": "effect_a9071d0cd33a",
    "áp chế ăn mòn": "effect_cac8d399a428",  # Áp Chế Ăn Mòn Mạnh / Corrosive Infusion
    "ăn mòn thấm sâu": "effect_cac8d399a428",
    "áp chế ăn mòn mạnh": "effect_cac8d399a428",
    "độc tố xâm lấn": "effect_c9757c9714b1",  # Độc Tính Xâm Nhập / Toxic Infiltration
    "độc tính xâm nhập": "effect_c9757c9714b1",
    "di chuyển thêm": "effect_c3e1a90d5f79",  # Di Chuyển Bổ Sung / Additional Movement
    "tinh thần quyết thắng": "effect_6ec5a16770d4",  # Hiếu Thắng / Competitive Spirit
    "hiếu thắng": "effect_6ec5a16770d4",
    "mê muội": "effect_b1678d11897b",  # Dẫn Dụ / Infatuated
    "dẫn dụ": "effect_b1678d11897b",
    "nạp điện": "effect_351891a52fff",  # Tụ Điện / Electro-Charge
    "tụ điện": "effect_351891a52fff",
    "tư thế kiên cố": "effect_740313784e64",  # Tư Thế Mạnh Mẽ / Fortified Stance
    "tư thế phòng ngự": "effect_740313784e64",
    "tư thế mạnh mẽ": "effect_740313784e64",
    "tự chẩn đoán": "effect_540b7929c777",  # Tự Sửa Chữa / Self-Diagnosis
    "tự sửa chữa": "effect_540b7929c777",
    "thần kinh tê liệt": "effect_ee98fd919e4e",  # Sức Ì / Blunted Nerves
    "thần kinh trơ lì": "effect_ee98fd919e4e",
    "sức ì": "effect_ee98fd919e4e",
    "đột phá hiệu suất": "effect_8b61a8020764",  # Đột Phá Tính Năng / Performance Breakthrough
    "đột phá tính năng": "effect_8b61a8020764",
    "vết nứt ứng suất": "effect_eda7bd6275a7",  # Khe Nứt Ứng Lực / Stress Fracture
    "vết rạn áp lực": "effect_eda7bd6275a7",
    "khe nứt ứng lực": "effect_eda7bd6275a7",
    "bộ phận chịu lực": "effect_cf0a24df6173",  # Phụ Kiện Chịu Lực / Load-Bearing Parts
    "phụ kiện chịu lực": "effect_cf0a24df6173",
    "sương độc": "effect_fdfb2ca6b8e0",  # Độc Chướng / Toxic Mist
    "sương mù độc": "effect_fdfb2ca6b8e0",
    "độc chướng": "effect_fdfb2ca6b8e0",
    "độc tố tràn ngập": "effect_291868a45a59",  # Ngập Tràn Độc Tố / Toxic Inundation
    "ngập tràn độc tố": "effect_291868a45a59",
    "cục cưng": "effect_ec0fc845d714",
    "oán hận": "effect_c0c7a8485bf1",  # Ghi Hận / Grudge
    "ghi hận": "effect_c0c7a8485bf1",
    "mặt quỷ vụng về": "effect_da1b8232b47c",  # Mặt Quỷ Nhăn Nhó / Sloppy Grimace
    "mặt quỷ nhăn nhó": "effect_da1b8232b47c",
    "dấu ấn đồng đội": "effect_e1f841f652e4",
    "nước tăng lực": "effect_531b39ba5aa1",
    "phụ thuộc xoa dịu": "effect_a872beaab1ab",  # Giải Phóng Phụ Thuộc / Alleviation Dependence
    "giải phóng phụ thuộc": "effect_a872beaab1ab",
    "tác chiến tích cực": "effect_6afb56afe1a2",  # Active Engagement
    "tích cực giao chiến": "effect_6afb56afe1a2",
    "giao tranh tích cực": "effect_6afb56afe1a2",
    "duy trì phóng điện": "effect_31aaa8bf4d08",  # Continual Release
    "phóng điện liên tục": "effect_31aaa8bf4d08",
    "ẩn náu": "effect_9481254c3284",  # Concealment
    "điện tử tràn ra": "effect_81a2d8548fbf",  # Overflowing Electrons
    "electron tràn trề": "effect_81a2d8548fbf",
    "lưu trữ điện năng": "effect_49a379bf069b",  # Stored Charge
    "tích trữ điện": "effect_49a379bf069b",
    "đài hoa e thẹn": "effect_abfcfde8ffd9",  # Sepal of Shyness
    "hồng tâm": "effect_ffb3a635db82",  # Tâm Bia / Bullseye
    "tâm bia": "effect_ffb3a635db82",
    "giá trị phân tích": "effect_ef41b94c55cb",
    "cảm giác an toàn": "effect_d72174b51365",
    "tích lũy làm nóng": "effect_3ddc2767ed65",
    "làm nóng tích lũy": "effect_3ddc2767ed65",
    "chúc phúc hàn băng": "effect_20d629daa780",  # Ice's Grace
    "ân huệ của băng": "effect_20d629daa780",
    "ân huệ băng": "effect_20d629daa780",
    "cứng đờ": "effect_237b67268b41",  # Frigid
    "giá lạnh": "effect_237b67268b41",
    "lời chúc cực hàn": "effect_1381bcd41b08",  # Arctic Benediction
    "chúc phúc bắc cực": "effect_1381bcd41b08",
    "lĩnh vực cực hàn": "effect_30afb08a5259",  # Glacial Domain
    "lãnh địa băng hà": "effect_30afb08a5259",
    "vô hiệu hóa di chuyển": "effect_11c02d54c46f",  # Movement Denied
    "cấm di chuyển": "effect_11c02d54c46f",
    "liệt thương": "effect_334e02a19b2b",  # Rend
    "xé rách": "effect_334e02a19b2b",
    "di hình": "effect_497852e2576f",  # Bypass
    "vết thương": "effect_34f4cc3ac706",  # Gash
    "vết thương sâu": "effect_34f4cc3ac706",
    "lá chắn hàn sương": "effect_0f8b4450ce8d",
    "hỗ trợ phòng thủ": "effect_e95b58944db1",
    "băng giá": "effect_6032a672e309",
    "sương giá": "effect_6032a672e309",
    "tuyết lở": "effect_b7b33d823b79",
    "pháo đài băng tuyết": "effect_ecb57fcb0cf8",
    "pháo đài mùa đông": "effect_ecb57fcb0cf8",
    "ánh sáng bảo vệ": "effect_1b391e77add2",
    "ánh sáng hộ vệ": "effect_1b391e77add2",
    "hồi phục khi bị đánh i": "effect_d3cb3c44b6d2",
    "phản ứng va chạm i": "effect_d3cb3c44b6d2",
    "tuần hoàn nhiệt": "effect_46910b897665",
    "phi tuyết tật bộ": "effect_c9a885a61333",
    "sleetdrift sprint": "effect_c9a885a61333",
    "phong ấn băng": "effect_658cd013c867",
    "đình trệ": "effect_76c40ad22b5e",
    "hoảng sợ": "effect_d10ca41e833d",
    "che chở hoàn hảo": "effect_ac9b1529046a",
    # Batch 5 additions
    "lệnh bổ sung": "effect_66241cc2ad8d",  # Chỉ Lệnh Bổ Sung / Extra Command
    "dấu ấn sakura": "effect_f4304acc4581",  # Dấu Anh Đào / Sakura Mark
    "viện hộ khẩn cấp": "effect_221576430ed3",  # Chi Viện Tức Thời / Emergency Support
    # CN Server standardization aliases
    "lửa thiêu": "effect_8066815f5668",  # Lửa Thiêu Đốt / Searing Flame
    "khiên chắn": "effect_08271419319f",  # Khiên / Shield
    "hành động hỗ trợ": "effect_a08aa26dd750",  # Hành Động Hỗ Trợ / Support Action
    "tấn công ngoài lượt": "effect_fd655633896a",  # Tấn Công Ngoài Lượt / Out-of-Turn Attack
    "đòn đánh ngoài lượt": "effect_fd655633896a",  # Đòn Đánh Ngoài Lượt
    "dấu ấn con mồi": "effect_da802bd7d2f7",  # Đánh Dấu Con Mồi / Mark of Prey
    "lối nước": "effect_5db88e1b8ea0",  # Dòng Ngầm / Tideway
    "cháy bỏng": "effect_fe4bac9b13fc",  # Tràn Lửa / Overburn
    "thiêu đốt": "effect_309ecd97c70c",  # Thiêu Rụi / Incineration
    "tăng sát thương lan ii": "effect_be04e120617f",  # Lan Tỏa Tăng II / Coverage Boost II
    "tăng sát thương chuẩn xác ii": "effect_99ae68bb3090",  # Chuẩn Xác Tăng II / Targeted Attack Boost II
    "dạng thợ săn": "effect_731a96515b90",  # Hình Thái Thợ Săn / Hunter Form
    "nhân tố cuồng bạo": "effect_fb8802d4262c",  # Nhân Tố Cuồng Bạo / Berserk Factor
    "yếu tố cuồng nộ": "effect_fb8802d4262c",
    # Soppo official terminology aliases
    "mad dog mode": "effect_5ae2c6eed3cb",
    "chế độ chó điên": "effect_5ae2c6eed3cb",
    "dạng chó điên": "effect_5ae2c6eed3cb",
    "dạng dã thú": "effect_5ae2c6eed3cb",
    "hunting hound mode": "effect_731a96515b90",
    "chế độ chó săn": "effect_731a96515b90",
    "dạng chó săn": "effect_731a96515b90",
    "hình thái thợ săn": "effect_731a96515b90",
    "hunting mark": "effect_fa8f59c100ac",
    "dấu ấn săn mồi": "effect_fa8f59c100ac",
    "permanent hunting mark": "effect_725efe82415d",
    "dấu ấn săn mồi vĩnh viễn": "effect_725efe82415d",
    "slaughtertrail": "effect_6bb0f520500a",
    "rabid factor": "effect_fb8802d4262c",
    "rabid factor i": "effect_85349ba10dfa",
    "rabid factor ii": "effect_d7b3752f7c62",
    "rabid factor iii": "effect_020d65de45b5",
    "boreal assault": "effect_a3b66642114a",
    # Additional skill and effect aliases
    "dẫn nhiệt": "effect_db167f6762f6",  # Truyền Nhiệt Năng / Thermal Conduction
    "khói": "effect_028f2cb637bd",  # Ô địa hình Khói Mù / Smoke
    "mưu tính định sẵn": "effect_ef41b94c55cb",  # Điểm Khảo Sát / Analytical Value
    "dấu ấn tận diệt": "effect_c0be876334a8",  # Dấu Ấn Vận Rủi / Doom Mark
    "vũ điệu cộng sinh": "effect_53309dbd52e6",  # Điệp Vũ Cộng Sinh / Symbiotic Dance
    "xung lân hỏa": "effect_bbb69c2d08e3",  # Xung Hỏa Lân Hỏa / Pyro Pulse
    "phòng ngự ban đầu": "effect_e102b22dc944",  # Phòng Thủ Tăng III / Defense Up III
    "súng bắn tỉa": "effect_02a8c2402c1a",  # Thợ Săn-II / Hunter Type - II
    "tiếng vàng điệu ngọc": "effect_221b75185057",  # Chỉnh Âm / Tuning
    "âm vang mê hoặc": "effect_1c4b0835d885",  # Định Âm / Pitch Perfect
    "giao thức gia cố": "effect_cf0a24df6173",  # Phụ Kiện Chịu Lực / Load-Bearing Parts
    "giao thức phá dỡ": "effect_eda7bd6275a7",  # Khe Nứt Ứng Lực / Stress Fracture
    "giao thức phá hủy": "effect_eda7bd6275a7",  # Khe Nứt Ứng Lực / Stress Fracture
    "truy kích nanh thú": "effect_fa8f59c100ac",  # Ấn Săn / Hunting Mark
    "cắn xé ác tính": "effect_fa8f59c100ac",  # Ấn Săn / Hunting Mark
    "tiếng hú đêm trăng": "effect_725efe82415d",  # Dấu Ấn Săn Mồi Vĩnh Viễn / Permanent Hunting Mark
}



def build_name_index(effects: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    """Build a collision-safe secondary index; duplicate names keep every matching ID."""
    index: dict[str, list[str]] = {}
    for effect_key, entry in effects.items():
        for field in ("name_en", "name"):
            name = str(entry.get(field, "")).strip()
            if not name:
                continue
            bucket = index.setdefault(name.casefold(), [])
            if effect_key not in bucket:
                bucket.append(effect_key)
        # Also index any aliases in the entry
        for alias in entry.get("aliases", []):
            alias_str = str(alias).strip()
            if not alias_str:
                continue
            bucket = index.setdefault(alias_str.casefold(), [])
            if effect_key not in bucket:
                bucket.append(effect_key)

    # Populate global aliases
    for alias, target in EFFECT_ALIASES.items():
        resolved_id = target if target in effects else None
        if not resolved_id:
            for eid, entry in effects.items():
                if entry.get("name_en", "").strip().casefold() == target.casefold() or entry.get("name", "").strip().casefold() == target.casefold():
                    resolved_id = eid
                    break
        if resolved_id:
            bucket = index.setdefault(alias.casefold(), [])
            if resolved_id in bucket:
                bucket.remove(resolved_id)
            bucket.insert(0, resolved_id)

    return index


def browser_catalog(effects: dict[str, dict[str, Any]]) -> dict[str, Any]:
    canonical = canonicalize_effects(effects)
    return {"schemaVersion": 2, "byId": canonical, "nameIndex": build_name_index(canonical)}

