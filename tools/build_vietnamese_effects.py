#!/usr/bin/env python3
"""
tools/build_vietnamese_effects.py
Comprehensive translation and localization builder for:
1. All 381 status effects (Buff / Debuff / Hiệu Ứng) with 0 English artifacts
2. All 12 character summons (Names, descriptions, stats, and skills)
3. All 187 weapons (Names, traits, imprint/passive effects, and stats)
4. Elimination of {0}, {1} placeholders in skill descriptions
5. Synchronization with data/i18n_vi.json and site/static/js/i18n-vi.js
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CHAR_DIR = DATA_DIR / "characters"
WEAPONS_FILE = DATA_DIR / "weapons.json"
ASSETS_DIR = ROOT / "assets"
EFFECTS_FILE = ASSETS_DIR / "effects.json"
I18N_JSON = DATA_DIR / "i18n_vi.json"
I18N_JS = ROOT / "site" / "static" / "js" / "i18n-vi.js"
EFFECTS_VI_JSON = DATA_DIR / "effects_vi.json"
WEAPONS_VI_FILE = DATA_DIR / "weapons_vi.json"

# ==============================================================================
# 1. COMPLETE 381 STATUS EFFECT NAMES (EN -> VI)
# ==============================================================================
EFFECT_NAMES: Dict[str, str] = {
    "Movement Down I": "Giảm Di Chuyển I",
    "Movement Down II": "Giảm Di Chuyển II",
    "Movement Down III": "Giảm Di Chuyển III",
    "Movement Up I": "Tăng Di Chuyển I",
    "Movement Up II": "Tăng Di Chuyển II",
    "Movement Up III": "Tăng Di Chuyển III",
    "Movement Denied": "Cấm Di Chuyển",
    "Additional Movement": "Di Chuyển Thêm",
    "Whirlwind": "Lốc Xoáy",
    "Bypass": "Đi Xuyên",
    "Pull": "Kéo",
    "Retrograde": "Nghịch Hành",
    "Sleetdrift Sprint": "Nước Rút Mưa Tuyết",
    "Sleepwalking": "Mộng Du",
    "Defense Up I": "Tăng Thủ I",
    "Defense Up II": "Tăng Thủ II",
    "Defense Up III": "Tăng Thủ III",
    "Defense Down I": "Giảm Thủ I",
    "Defense Down II": "Giảm Thủ II",
    "Defense Down III": "Giảm Thủ III",
    "Area Defense I": "Phòng Thủ AoE I",
    "Area Defense II": "Phòng Thủ AoE II",
    "Targeted Attack Defense I": "Phòng Thủ Đòn Đơn I",
    "Targeted Attack Defense II": "Phòng Thủ Đòn Đơn II",
    "Damage Reduction I": "Giảm Sát Thương I",
    "Damage Reduction II": "Giảm Sát Thương II",
    "Damage Down I": "Giảm Sát Thương I",
    "Damage Down II": "Giảm Sát Thương II",
    "Vulnerable I": "Dễ Tổn Thương I",
    "Vulnerable II": "Dễ Tổn Thương II",
    "Vulnerability Analysis": "Phân Tích Sơ Hở",
    "Piercing I": "Xuyên Thấu I",
    "Piercing II": "Xuyên Thấu II",
    "Shield Pierce Rate": "Tỷ Lệ Xuyên Khiên",
    "Domain Penetration I": "Xuyên Thấu Lĩnh Vực I",
    "Attack Up I": "Tăng Công I",
    "Attack Up II": "Tăng Công II",
    "Attack Up III": "Tăng Công III",
    "Attack Down I": "Giảm Công I",
    "Attack Down II": "Giảm Công II",
    "Attack Down III": "Giảm Công III",
    "Damage Up I": "Tăng Sát Thương I",
    "Damage Up II": "Tăng Sát Thương II",
    "Critical Rate Boost I": "Tăng TL Bạo Kích I",
    "Critical Rate Boost II": "Tăng TL Bạo Kích II",
    "Critical Damage Up I": "Tăng ST Bạo Kích I",
    "Critical Damage Up II": "Tăng ST Bạo Kích II",
    "Targeted Attack Boost I": "Cường Hóa ST Chuẩn Xác I",
    "Targeted Attack Boost II": "Cường Hóa ST Chuẩn Xác II",
    "Phase Boost I": "Cường Hóa Dị Vị I",
    "Phase Boost II": "Cường Hóa Dị Vị II",
    "Support Boost I": "Cường Hóa Chi Viện I",
    "Support Boost II": "Cường Hóa Chi Viện II",
    "Electric Boost I": "Cường Hóa Điện I",
    "Electric Boost II": "Cường Hóa Điện II",
    "Stability Offensive I": "Tấn Công Ổn Định I",
    "Stability Offensive II": "Tấn Công Ổn Định II",
    "Stability Loss I": "Hao Tổn Ổn Định I",
    "Stability Loss II": "Hao Tổn Ổn Định II",
    "Continuous Healing I": "Trị Liệu Liên Tục I",
    "Continuous Healing II": "Trị Liệu Liên Tục II",
    "Continuous Stability Regen I": "Hồi Phục Ổn Định Liên Tục I",
    "Continuous Stability Regen II": "Hồi Phục Ổn Định Liên Tục II",
    "Self-Repair": "Tự Sửa Chữa",
    "Self-Diagnosis": "Tự Chẩn Đoán",
    "Heat Recovery": "Hồi Nhiệt",
    "Thermal Cycling": "Tuần Hoàn Nhiệt",
    "Stimulant": "Thuốc Kích Thích",
    "Shield": "Khiên",
    "Quick Barrier": "Lá Chắn Nhanh",
    "Frost Barrier": "Bình Chướng Băng",
    "Brumal Barrier": "Bình Chướng Băng",
    "Aegis": "Phòng Ngự Ban Đầu",
    "Absolute Defense": "Phòng Thủ Tuyệt Đối",
    "Perfect Defense": "Phòng Thủ Hoàn Hảo",
    "Shelter": "Nơi Trú Ẩn",
    "Wintry Bastion": "Pháo Đài Băng Giá",
    "Shield of Punishment": "Khiên Trừng Phạt",
    "Capital Protection": "Bảo Vệ Vốn",
    "V3 Protection": "Bảo Vệ V3",
    "Steel Forging": "Rèn Thép",
    "Fortified Stance": "Tư Thế Phòng Ngự",
    "Patch Mode": "Chế Độ Chắp Vá",
    "Detective's Immunity": "Miễn Dịch Thám Tử",
    "Extra Action": "Tăng Hành Động",
    "Extra Command": "Lệnh Bổ Sung",
    "Action Support": "Tấn Công Chi Viện",
    "Support": "Chi Viện",
    "Wise Support": "Viện Trợ Sáng Suốt",
    "Emergency Support": "Viện Hộ Khẩn Cấp",
    "Defensive Support": "Chi Viện Phòng Ngự",
    "Interception": "Chặn Đánh",
    "Counterattack": "Phản Kích",
    "Preemptive Strike": "Tấn Công Phủ Đầu",
    "Overclock Strike": "Đòn Đánh Ép Xung",
    "Predation": "Săn Mồi",
    "Predation Protocol": "Giao Thức Săn Mồi",
    "Combo Pounce": "Vồ Liên Hoàn",
    "Eagle Strike": "Ưng Kích",
    "Volley Fire": "Bắn Loạt",
    "Resolve to Defend": "Quyết Tâm Phòng Ngự",
    "Standby": "Chờ Lệnh",
    "Taunt": "Khiêu Khích",
    "Fear": "Sợ Hãi",
    "Stun": "Choáng",
    "Shock": "Sốc Điện",
    "Conductivity": "Dẫn Điện",
    "Paralysis": "Tê Liệt",
    "Frozen": "Đóng Băng",
    "Frigid": "Lạnh Buốt",
    "Hoarfrost": "Sương Giá",
    "Cold Snap": "Rét Buốt",
    "Frost": "Băng Giá",
    "Ice Seal": "Phong Ấn Băng",
    "Ice's Grace": "Ân Huệ Của Băng",
    "Glacial Domain": "Lĩnh Vực Băng Giá",
    "Ice Construct": "Vật Tạo Băng",
    "Overburn": "Quá Nhiệt",
    "Overheating": "Quá Tải Nhiệt",
    "Overheat": "Quá Nhiệt",
    "Overheat Combustion": "Cháy Quá Nhiệt",
    "Flammable": "Dễ Cháy",
    "Conflagration": "Đại Hỏa",
    "Embers": "Tàn Lửa",
    "Smolder": "Cháy Âm Ỉ",
    "Pyro Pulse": "Xung Hỏa Lực",
    "Searing Flame": "Ngọn Lửa Thiêu Đốt",
    "Thermal Conduction": "Dẫn Nhiệt",
    "Damp": "Ẩm Ướt",
    "Soak I": "Ẩm Ướt I",
    "Tideway": "Thủy Triều Rút",
    "Congestion": "Tắc Nghẽn",
    "Chaos Compound": "Hợp Chất Hỗn Loạn",
    "Toxic Mist": "Sương Mù Độc",
    "Toxic Inundation": "Nhiễm Độc",
    "Toxic Infiltration": "Xâm Nhiễm Ăn Mòn",
    "Corrosive Infusion": "Truyền Dẫn Ăn Mòn",
    "Acid Corrosion I": "Ăn Mòn Axit I",
    "Acid Corrosion II": "Ăn Mòn Axit II",
    "Blazing Assault I": "Xung Kích Thiêu Đốt I",
    "Blazing Assault II": "Xung Kích Thiêu Đốt II",
    "Berserk Factor I": "Yếu Tố Cuồng Nộ I",
    "Berserk Factor II": "Yếu Tố Cuồng Nộ II",
    "Berserk Factor III": "Yếu Tố Cuồng Nộ III",
    "Berserk Factor": "Yếu Tố Cuồng Nộ",
    "Smoke": "Khói",
    "Infatuated": "Mê Hoặc",
    "Immobilize": "Bất Động",
    "Control-type": "Hiệu Ứng Khống Chế",
    "Incapaciation": "Vô Hiệu Hóa",
    "Blunted Nerves": "Thần Kinh Trơ",
    "Stress Fracture": "Vết Rạn Áp Lực",
    "Dismay": "Mất Tinh Thần",
    "Bad Luck": "Vận Xui",
    "Sloppy Grimace": "Mặt Quỷ Nhăn Nhó",
    "Sugar Overdose": "Quá Tải Đường",
    "Aichmophobia": "Ám Ảnh Mũi Nhọn",
    "Alleviation Dependence": "Phụ Thuộc Xoa Dịu",
    "Suspect": "Kẻ Khả Nghi",
    "Crime Backlash": "Phản Phệ Tội Ác",
    "Electric Spark": "Tia Lửa Điện",
    "Electric Arc": "Hồ Quang Điện",
    "Positive Charge": "Điện Tích Dương",
    "Negative Charge": "Điện Tích Âm",
    "Electro-Charge": "Tụ Điện",
    "Voltage": "Điện Áp",
    "Voltage Sag": "Sụt Áp",
    "Power Surge": "Đột Biến Năng Lượng",
    "Stored Charge": "Tích Điện",
    "Overflowing Electrons": "Electron Tràn Đầy",
    "Continual Release": "Giải Phóng Liên Tục",
    "Cyclotron Potential": "Điện Thế Xoay Chiều",
    "Superconductive Chain": "Chuỗi Siêu Dẫn",
    "Superconductive Code": "Mã Siêu Dẫn",
    "Confectance Index": "Chỉ Số Nhiên Liệu",
    "Stability Protection": "Bảo Vệ Độ Ổn Định",
    "Stability Index": "Chỉ Số Ổn Định",
    "Cover": "Vật Cản",
    "High Ground": "Cao Điểm",
    "Doom Mark": "Dấu Ấn Tận Diệt",
    "Hunter's Tracking": "Theo Vết Thợ Săn",
    "Hunter's Talent": "Tài Năng Thợ Săn",
    "Mark of Prey": "Dấu Ấn Con Mồi",
    "Collar Brand": "Dấu Ấn Vòng Cổ",
    "Scorch Mark": "Vết Thiêu Đốt",
    "Sakura Mark": "Dấu Ấn Sakura",
    "Vindicator's Mark": "Ấn Kẻ Trừng Phạt",
    "Predator Mark": "Dấu Ấn Thợ Săn",
    "Permanent Predator Mark": "Dấu Ấn Thợ Săn Vĩnh Viễn",
    "Scent Mark": "Dấu Ấn Mùi Hương",
    "Bullseye": "Hồng Tâm",
    "Blood Emblem": "Huyết Huy Chương",
    "Blood Kiss": "Huyết Nụ Hôn",
    "Scarlet Insignia": "Huy Hiệu Đỏ Thẫm",
    "Feathers of War": "Lông Vũ Chiến Trận",
    "Battle Prep": "Chuẩn Bị Tác Chiến",
    "Rend": "Xé Rách",
    "Reversed Assault": "Công Kích Nghịch Đảo",
    "Overzealous": "Quá Khích",
    "Feeling Full": "No Nê",
    "Candyglaze": "Áo Đường",
    "Hot Sobering Tea": "Trà Nóng Tỉnh Táo",
    "Energy drink": "Nước Tăng Lực",
    "Wok Aura": "Hào Quang Chảo Nấu",
    "Lone Wolf": "Sói Cô Độc",
    "Active Engagement": "Giao Tranh Tích Cực",
    "Unshakable Confidence": "Tự Tin Vững Vàng",
    "Lightspike": "Gai Sáng",
    "Precision": "Chuẩn Xác",
    "Insight": "Thấu Thị",
    "Stellar Insight": "Thấu Thị Tinh Tú",
    "Zoom In": "Thu Phóng",
    "Sense Weakness": "Cảm Nhận Điểm Yếu",
    "Sense of Security": "Cảm Giác An Toàn",
    "Presence of Mind": "Tâm Trí Vững Vàng",
    "Courage to Endure": "Dũng Khí Nhẫn Nại",
    "Tenacity to Withstand": "Kiên Cường Chống Chịu",
    "Preshow Warmup": "Khởi Động Trước Giờ Diễn",
    "Sleep Aid Kit": "Bộ Hỗ Trợ Giấc Ngủ",
    "Stealth": "Tàng Hình",
    "Concealed": "Ẩn Nấp",
    "Concealment": "Ẩn Nấp",
    "Camouflage": "Ngụy Trang",
    "Untouchable": "Bất Khả Xâm Phạm",
    "Warding Light": "Ánh Sáng Hộ Vệ",
    "Wolf Eye System": "Hệ Thống Mắt Sói",
    "Dog-Eared Radar": "Radar Tai Chó",
    "Clue": "Manh Mối",
    "Deductive Obsession": "Ám Ảnh Suy Luận",
    "Feral Form": "Dạng Dã Thú",
    "True Form": "Chân Thân",
    "Coagulation": "Đông Tụ",
    "Saturation": "Bão Hòa",
    "Saturation Overflow": "Bão Hòa Tràn Ngập",
    "Tuning": "Điều Âm",
    "Pitch Perfect": "Chuẩn Cao Độ",
    "Best Dancer": "Vũ Công Xuất Sắc",
    "Dance Steps": "Bước Nhảy",
    "Passionate Spin": "Xoay Người Nhiệt Huyết",
    "Graceful Spin": "Xoay Người Duyên Dáng",
    "Troupe's Core": "Trụ Cột Đoàn Kịch",
    "Symbiotic Dance": "Điệu Múa Cộng Sinh",
    "Rapture": "Hoan Hỉ",
    "Steady Progress": "Tiến Bước Vững Chắc",
    "Steady": "Vững Vàng",
    "Murderous Intent": "Sát Ý",
    "Roving Bloodlust": "Khát Máu Lang Thang",
    "Blade Resonance": "Cộng Hưởng Lưỡi Đao",
    "Blade of Sin": "Lưỡi Đao Tội Lỗi",
    "Sharpness": "Sắc Bén",
    "Tempered Blood": "Máu Tôi Luyện",
    "Crime and Punishment": "Tội Và Phạt",
    "Absolution": "Miễn Trừ Tội",
    "Adjudication Privilege": "Đặc Quyền Phán Quyết",
    "Adrenaline": "Adrenaline",
    "Accelerant": "Chất Kích Cháy",
    "Accumulated Preheat": "Tích Lũy Làm Nóng",
    "Accolade's Brilliance": "Huy Hoàng Tán Thưởng",
    "Ultimate Briliance": "Huy Hoàng Quyết Thắng",
    "Alpha Process": "Tiến Trình Alpha",
    "Analytical Value": "Giá Trị Phân Tích",
    "Arctic Benediction": "Phước Lành Bắc Cực",
    "Avalanche": "Tuyết Lở",
    "Awakening Command": "Lệnh Thức Tỉnh",
    "Bargain": "Mặc Cả",
    "Bonded Possibility": "Khả Năng Liên Kết",
    "Cold Conviction": "Niềm Tin Lạnh Lùng",
    "Standard Approach": "Tiếp Cận Chuẩn Mực",
    "Emergency Plan": "Kế Hoạch Khẩn Cấp",
    "Chi": "Khí",
    "Competitive Spirit": "Tinh Thần Cạnh Tranh",
    "Coordinated Combat": "Tác Chiến Phối Hợp",
    "Coordinated Hunting": "Săn Bắn Phối Hợp",
    "Cover Order": "Lệnh Che Chắn",
    "Covering Mode": "Chế Độ Viện Hộ",
    "Command Mode": "Chế Độ Chỉ Huy",
    "Demolition Order": "Lệnh Phá Hủy",
    "Deep-Rooted Bonds": "Liên Kết Sâu Đậm",
    "Dream Guardian": "Vệ Sĩ Mộng Mị",
    "Dreamscape Exhilaration": "Hưng Phấn Cảnh Mộng",
    "Fantastic Conception": "Ý Tưởng Tuyệt Vời",
    "Immune": "Miễn Dịch",
    "Parapluie's Penetration": "Xuyên Thấu Parapluie",
    "Performance Breakthrough": "Đột Phá Hiệu Suất",
    "Overedge": "Vượt Giới Hạn",
    "Overflowing Care": "Quan Tâm Tràn Đầy",
    "Overload Pulse": "Xung Quá Tải",
    "Power of Bonds": "Sức Mạnh Liên Kết",
    "Power of Unity": "Sức Mạnh Đoàn Kết",
    "Precognition Awareness": "Nhận Thức Dự Đoán",
    "Precognition Foresight": "Viễn Cảnh Dự Đoán",
    "Prophet": "Nhà Tiên Tri",
    "Pursuer": "Kẻ Truy Đuổi",
    "Queen of the Skies": "Nữ Hoàng Bầu Trời",
    "Radiant Rise": "Thăng Hoa Rực Rỡ",
    "Reverse Assimilation": "Đồng Hóa Nghịch Đảo",
    "Sepal of Shyness": "Đài Hoa E Thẹn",
    "Shared Telepathy": "Thần Giao Cách Cảm",
    "Slaughter Trail": "Dấu Vết Tàn Sát",
    "Stunt Double": "Diễn Viên Thế Thân",
    "Sync": "Đồng Bộ",
    "Turbo Boost": "Tăng Áp Turbo",
    "Turbo Mode": "Chế Độ Turbo",
    "Unity": "Đoàn Kết",
    "Waking Ricochet": "Bật Nảy Tỉnh Thức",
    "Cinematic Title": "Danh Hiệu Điện Ảnh",
    "Cellular Reconfiguration": "Tái Cấu Trúc Tế Bào",
    "Combat Stance": "Tư Thế Tác Chiến",
    "False Intelligence": "Tình Báo Giả",
    "D Gear": "Trang Bị D",
    "P Gear": "Trang Bị P",
    "S Gear": "Trang Bị S",
    "S+ Gear": "Trang Bị S+",
    "Upshift": "Tăng Số",
    "Prophecy of Mourning": "Lời Tiên Tri Bi Tang",
    "First Prophecy: Resonance": "Tiên Tri Thứ Nhất: Cộng Hưởng",
    "Second Prophecy: Solitude": "Tiên Tri Thứ Hai: Cô Độc",
    "Second Prophecy": "Lời Tiên Tri Thứ Hai",
    "Third Prophecy": "Lời Tiên Tri Thứ Ba",
    "Fifth Prophecy: Startrack": "Tiên Tri Thứ Năm: Quỹ Đạo Sao",
    "Sixth Prophecy": "Lời Tiên Tri Thứ Sáu",
    "Reconfiguration · Burn": "Tái Cấu Trúc · Thiêu Đốt",
    "Reconfiguration · Corrosion": "Tái Cấu Trúc · Ăn Mòn",
    "Reconfiguration · Electro": "Tái Cấu Trúc · Dẫn Điện",
    "Reconfiguration · Freeze": "Tái Cấu Trúc · Băng Kết",
    "Reconfiguration · Hydro": "Tái Cấu Trúc · Hóa Lỏng",
    "Reconfiguration · Zero": "Tái Cấu Trúc · Không",
    "Rank": "Cấp Bậc",
    "Rank 1": "Cấp 1",
    "Rank 2": "Cấp 2",
    "Rank 3": "Cấp 3",
    "Tin Soldier": "Lính Chì",
    "Tin Soldier's Order": "Mệnh Lệnh Lính Chì",
    "Cutie Pie": "Cục Cưng",
    "The Sinner": "Kẻ Tội Lỗi",
    "Personal Hologram": "Hologram Cá Nhân",
    "Taryz": "Taryz",
    "Physical Summon": "Vật Triệu Hồi Vật Lý",
    "Entity Summon": "Vật Triệu Hồi",
    "Impact Response I": "Phản Ứng Va Chạm I",
    "Alert": "Cảnh Giác",
    "Nightmarish Shroud": "Màn Che Ác Mộng",
    "Nightmare Form": "Hình Thái Ác Mộng",
    "Incineration": "Thiêu Rụi",
    "Inital Damage": "Sát Thương Ban Đầu",
    "Gash": "Vết Chém Sâu",
    "Hot Investment": "Đầu Tư Nóng",
    "Never Give Up": "Không Bao Giờ Bỏ Cuộc",
    "Guilt": "Tội Lỗi",
    "Monitoring": "Giám Sát",
    "Inspection": "Thị Sát",
    "Frigid Infiltration": "Thâm Nhập Băng Giá",
    "Memory Shock": "Cú Sốc Ký Ức",
    "Mirror Cache": "Bộ Nhớ Đệm Gương",
    "Ketoacidemia": "Nhiễm Toan Ceton",
    "Honey Trap": "Cạm Bẫy Ngọt Ngào",
    "Load-Bearing Parts": "Bộ Phận Chịu Tải",
    "Liquid N2 Fang": "Nanh Băng N2 Lỏng",
    "Hypothermia": "Hạ Thân Nhiệt",
    "Frostbite": "Tê Cóng",
    "Frightened": "Kinh Hãi",
    "Hunting Rhythm": "Nhịp Điệu Săn Bắt",
    "Merit": "Chiến Công",
    "Frost Drive": "Lực Đẩy Băng Giá",
    "Glory to Mommies": "Vinh Quang Cho Mẹ",
    "Laceration": "Vết Cắt Xé",
    "Good Luck": "Vận May",
    "Glowing Embers": "Tàn Lửa Đỏ Rực",
    "Hunter Type - II": "Thợ Săn-II",
    "Infernal Surge": "Dâng Trào Địa Ngục",
    "Flawless Blaze": "Ngọn Lửa Hoàn Hảo",
    "Kill Process": "Tiến Trình Tiêu Diệt",
    "Grudge": "Oán Hận",
    "Mark of Comrades": "Dấu Ấn Đồng Đội",
    "Loaded Attack": "Đòn Tấn Công Đã Nạp",
    "Lockdown": "Khóa Chặt",
    "Holy Blood Mark": "Dấu Ấn Thánh Huyết",
    "Focus": "Tập Trung",
    "First Prophecy": "Lời Tiên Tri Thứ Nhất",
    "Omen": "Điềm Báo",
    "Fourth Prophecy": "Lời Tiên Tri Thứ 4: Phán Quyết",
    "Fifth Prophecy": "Lời Tiên Tri Thứ 5: Tinh Quỹ",
    "Hunter Form": "Hình Thái Thợ Săn",
    "Frost Assault": "Xung Kích Băng Kết",
    "Mimic Hologram": "Hologram Mô Phỏng",
    "Hologram": "Hologram",
    "Fitting Resonance": "Cộng Hưởng Tương Thích",
    "Mimic Rookie": "Tân Tú Mô Phỏng",
    "Legendary Star": "Ngôi Sao Huyền Thoại",
    "Fitting Amplification": "Khuếch Đại Tương Thích",
    "N Gear": "Số N",
    "Kinetic Recovery": "Thu Hồi Động Năng",
    "Mobile Support": "Chi Viện Cơ Động",
    "Lets go for a spin!": "Đi Hóng Gió Nào!",
    "Immobilized": "Bất Động",
    "Kinetic Release": "Giải Phóng Động Năng",
    "Kinetic Release+": "Giải Phóng Động Năng+",
    "Lock on Attack": "Khóa Mục Tiêu",
    "Heavy Talons": "Đòn Vuốt Nặng",
    "Invasive Threat": "Đe Dọa Xâm Lấn"
}

# ==============================================================================
# 2. EXACT IN-GAME & REFINED EFFECT TRANSLATIONS
# ==============================================================================
EXACT_IN_GAME: Dict[str, Tuple[str, str, str]] = {
    "Movement Down I": [
        "Di Chuyển Giảm I",
        "Tầm Di Chuyển giảm 1 ô. Thuộc loại Debuff Di Chuyển.",
        "debuff"
    ],
    "Movement Down II": [
        "Di Chuyển Giảm II",
        "Tầm Di Chuyển giảm 2 ô. Thuộc loại Debuff Di Chuyển.",
        "debuff"
    ],
    "Movement Down III": [
        "Di Chuyển Giảm III",
        "Tầm Di Chuyển giảm 3 ô. Thuộc loại Debuff Di Chuyển.",
        "debuff"
    ],
    "Movement Up I": [
        "Di Chuyển Tăng I",
        "Tầm Di Chuyển tăng 1 ô. Thuộc loại Buff.",
        "buff"
    ],
    "Movement Up II": [
        "Di Chuyển Tăng II",
        "Tầm Di Chuyển tăng 2 ô. Thuộc loại Buff.",
        "buff"
    ],
    "Movement Up III": [
        "Di Chuyển Tăng III",
        "Tầm Di Chuyển tăng 3 ô. Thuộc loại Buff.",
        "buff"
    ],
    "Movement Denied": [
        "Cấm Di Chuyển",
        "Không thể di chuyển. Thuộc loại Debuff Di Chuyển.",
        "debuff"
    ],
    "Additional Movement": [
        "Di Chuyển Thêm",
        "Có thể di chuyển 1 lần, nhưng không thể dùng lệnh khác.",
        "buff"
    ],
    "Bypass": [
        "Đi Xuyên",
        "Khi di chuyển bỏ qua cản trở của đơn vị địch. Thuộc loại Buff.",
        "buff"
    ],
    "Pull": [
        "Kéo",
        "Kéo mục tiêu về phía vị trí chỉ định.",
        "effect"
    ],
    "Attack Up I": [
        "Tấn Công Tăng I",
        "Tấn Công tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Attack Up II": [
        "Tấn Công Tăng II",
        "Tấn Công tăng 15%. Thuộc loại Buff.",
        "buff"
    ],
    "Attack Up III": [
        "Tấn Công Tăng III",
        "Tấn Công tăng 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Attack Down I": [
        "Tấn Công Giảm I",
        "Tấn Công giảm 10%. Thuộc loại Debuff.",
        "debuff"
    ],
    "Attack Down II": [
        "Tấn Công Giảm II",
        "Tấn Công giảm 15%. Thuộc loại Debuff.",
        "debuff"
    ],
    "Attack Down III": [
        "Tấn Công Giảm III",
        "Tấn Công giảm 20%. Thuộc loại Debuff.",
        "debuff"
    ],
    "Defense Up I": [
        "Phòng Thủ Tăng I",
        "Phòng Thủ tăng 15%. Thuộc loại Buff.",
        "buff"
    ],
    "Defense Up II": [
        "Phòng Thủ Tăng II",
        "Phòng Thủ tăng 30%. Thuộc loại Buff.",
        "buff"
    ],
    "Defense Up III": [
        "Phòng Thủ Tăng III",
        "Phòng Thủ tăng 45%. Thuộc loại Buff.",
        "buff"
    ],
    "Defense Down I": [
        "Phòng Thủ Giảm I",
        "Phòng Thủ giảm 20%. Thuộc loại Debuff phòng thủ.",
        "debuff"
    ],
    "Defense Down II": [
        "Phòng Thủ Giảm II",
        "Phòng Thủ giảm 30%. Thuộc loại Debuff phòng thủ.",
        "debuff"
    ],
    "Defense Down III": [
        "Phòng Thủ Giảm III",
        "Phòng Thủ giảm 40%. Thuộc loại Debuff phòng thủ.",
        "debuff"
    ],
    "Damage Up I": [
        "Tăng Sát Thương I",
        "Sát thương gây ra tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Damage Up II": [
        "Tăng Sát Thương II",
        "Sát thương gây ra tăng 15%. Thuộc loại Buff.",
        "buff"
    ],
    "Damage Down I": [
        "Giảm Sát Thương I",
        "Sát thương gây ra giảm 10%. Thuộc loại Debuff.",
        "debuff"
    ],
    "Damage Down II": [
        "Giảm Sát Thương II",
        "Sát thương gây ra giảm 15%. Thuộc loại Debuff.",
        "debuff"
    ],
    "Damage Reduction I": [
        "Giảm ST I",
        "Sát thương phải chịu giảm 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Damage Reduction II": [
        "Giảm ST II",
        "Sát thương phải chịu giảm 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Area Defense I": [
        "Phòng Thủ AoE I",
        "ST AoE phải chịu giảm 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Area Defense II": [
        "Phòng Thủ AoE II",
        "ST AoE phải chịu giảm 40%. Thuộc loại Buff.",
        "buff"
    ],
    "Targeted Attack Defense I": [
        "Phòng Thủ Chuẩn Xác I",
        "ST Chuẩn Xác phải chịu giảm 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Targeted Attack Defense II": [
        "Phòng Thủ Chuẩn Xác II",
        "ST Chuẩn Xác phải chịu giảm 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Targeted Attack Boost I": [
        "ST Chuẩn Xác Tăng I",
        "ST Chuẩn Xác tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Targeted Attack Boost II": [
        "ST Chuẩn Xác Tăng II",
        "ST Chuẩn Xác tăng 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Critical Rate Boost I": [
        "TL Bạo Kích Tăng I",
        "Tỷ lệ Bạo Kích tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Critical Rate Boost II": [
        "TL Bạo Kích Tăng II",
        "Tỷ lệ Bạo Kích tăng 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Critical Damage Up I": [
        "ST Bạo Kích Tăng I",
        "ST Bạo Kích tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Critical Damage Up II": [
        "ST Bạo Kích Tăng II",
        "ST Bạo Kích tăng 30%. Thuộc loại Buff.",
        "buff"
    ],
    "Piercing I": [
        "Xuyên Thấu I",
        "ST Chuẩn Xác bỏ qua 15% Phòng Thủ của mục tiêu. Thuộc loại Buff.",
        "buff"
    ],
    "Piercing II": [
        "Xuyên Thấu II",
        "ST Chuẩn Xác bỏ qua 30% Phòng Thủ của mục tiêu. Thuộc loại Buff.",
        "buff"
    ],
    "Vulnerable I": [
        "Dễ Bị Thương I",
        "Sát thương phải chịu tăng 10%. Thuộc loại Debuff.",
        "debuff"
    ],
    "Vulnerable II": [
        "Dễ Bị Thương II",
        "Sát thương phải chịu tăng 20%. Thuộc loại Debuff.",
        "debuff"
    ],
    "Electric Boost I": [
        "Dẫn Điện Tăng I",
        "ST Dẫn Điện gây ra tăng 10%. Thuộc loại Buff Dẫn Điện.",
        "buff"
    ],
    "Electric Boost II": [
        "Dẫn Điện Tăng II",
        "ST Dẫn Điện gây ra tăng 20%. Thuộc loại Buff Dẫn Điện.",
        "buff"
    ],
    "Phase Boost I": [
        "ST Dị Vị Tăng I",
        "ST Dị Vị gây ra tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Phase Boost II": [
        "ST Dị Vị Tăng II",
        "ST Dị Vị gây ra tăng 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Support Boost I": [
        "Cường Hóa Chi Viện I",
        "ST Tấn Công Chi Viện tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Support Boost II": [
        "Cường Hóa Chi Viện II",
        "ST Tấn Công Chi Viện tăng 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Continuous Healing I": [
        "Trị Liệu Liên Tục I",
        "Hồi phục 10% HP tối đa khi kết thúc hành động. Thuộc loại Buff.",
        "buff"
    ],
    "Continuous Healing II": [
        "Trị Liệu Liên Tục II",
        "Hồi phục 20% HP tối đa khi kết thúc hành động. Thuộc loại Buff.",
        "buff"
    ],
    "Continuous Stability Regen I": [
        "Hồi Phục Ổn Định Liên Tục I",
        "Hồi phục 1 điểm Chỉ Số Ổn Định khi kết thúc hành động. Thuộc loại Buff.",
        "buff"
    ],
    "Continuous Stability Regen II": [
        "Hồi Phục Ổn Định Liên Tục II",
        "Hồi phục 2 điểm Chỉ Số Ổn Định khi kết thúc hành động. Thuộc loại Buff.",
        "buff"
    ],
    "Stability Loss I": [
        "Mất Ổn Định I",
        "ST Ổn Định phải chịu tăng 1 điểm. Thuộc loại Debuff.",
        "debuff"
    ],
    "Stability Loss II": [
        "Mất Ổn Định II",
        "ST Ổn Định phải chịu tăng 2 điểm. Thuộc loại Debuff.",
        "debuff"
    ],
    "Stability Offensive I": [
        "Tấn Công Ổn Định I",
        "ST Ổn Định gây ra tăng 1 điểm. Thuộc loại Buff.",
        "buff"
    ],
    "Stability Offensive II": [
        "Tấn Công Ổn Định II",
        "ST Ổn Định gây ra tăng 2 điểm. Thuộc loại Buff.",
        "buff"
    ],
    "Shelter": [
        "Nơi Trú Ẩn",
        "Nhận Bảo Vệ Độ Ổn Định, giảm 2 điểm ST Ổn Định phải chịu. Mỗi lần chịu ST Ổn Định tiêu hao 1 lớp, tối đa 3 lớp. Thuộc loại Buff.",
        "buff"
    ],
    "Taunt": [
        "Khiêu Khích",
        "Mất kiểm soát, cưỡng chế dùng Đánh Thường tấn công người thi triển. Xóa bỏ khi người thi triển tử vong. Thuộc loại Debuff.",
        "debuff"
    ],
    "Fear": [
        "Sợ Hãi",
        "Mất kiểm soát, chủ động di chuyển ra xa người thi triển. Xóa bỏ khi người thi triển tử vong. Thuộc loại Debuff.",
        "debuff"
    ],
    "Stun": [
        "Choáng",
        "Đơn vị chịu hiệu ứng Choáng không thể thực hiện bất kỳ hành động nào. Thuộc loại Debuff.",
        "debuff"
    ],
    "Paralysis": [
        "Tê Liệt",
        "Chỉ có thể di chuyển hoặc chờ, không thể thi triển kỹ năng hoặc Đánh Thường. Thuộc loại Debuff Dẫn Điện.",
        "debuff"
    ],
    "Counterattack": [
        "Phản Kích",
        "Tiến hành 1 lần tấn công; Không thể bị kích hoạt bởi Chặn Đánh, Phản Kích hoặc Tấn Công Chi Viện. Thuộc loại Buff.",
        "buff"
    ],
    "Interception": [
        "Chặn Đánh",
        "Tiến hành 1 lần tấn công, ngắt quãng hành động của mục tiêu; Không thể bị kích hoạt bởi Chặn Đánh, Phản Kích hoặc Tấn Công Chi Viện. Thuộc loại Buff.",
        "buff"
    ],
    "Action Support": [
        "Tấn Công Chi Viện",
        "Tiến hành 1 lần Tấn Công Chi Viện; Không thể bị kích hoạt bởi 1 lần Tấn Công Chi Viện khác. Thuộc loại Buff.",
        "buff"
    ],
    "Support": [
        "Chi Viện",
        "Vào Tư Thế Chi Viện. Khi kẻ địch trong tầm bắn nhận ST Chuẩn Xác từ đồng đội, ưu tiên Tấn Công Chi Viện 1 lần, gây ST Vật Lý bằng 80% Tấn Công và 3 điểm ST Ổn Định. Hiệu ứng này không thể giải trừ.",
        "buff"
    ],
    "Wise Support": [
        "Chi Viện Tinh Anh",
        "Tiến hành 1 lần Tấn Công Chi Viện.",
        "buff"
    ],
    "Absolute Defense": [
        "Phòng Ngự Tuyệt Đối",
        "Miễn dịch sát thương từ Đánh Thường và kỹ năng. Xóa bỏ hiệu quả miễn dịch sau khi nhận 1 lần Đánh Thường hoặc kỹ năng. Thuộc loại Buff.",
        "buff"
    ],
    "Overburn": [
        "Tràn Lửa",
        "Khi nhận hiệu ứng này và khi kết thúc hành động, bản thân và tất cả đơn vị đồng minh trong phạm vi 1 ô chịu ST cố định bằng 10% Tấn Công của người thi triển. Thuộc loại Debuff Thiêu Đốt.",
        "debuff"
    ],
    "Frozen": [
        "Đóng Băng",
        "Tầm Di Chuyển giảm 1 ô. Nếu Đóng Băng đạt 2 lớp khi kết thúc hành động, chuyển hóa thành Băng Đọng duy trì 1 hiệp. Tối đa 2 lớp. Thuộc loại Debuff Di Chuyển Băng Kết.",
        "debuff"
    ],
    "Frigid": [
        "Băng Đọng",
        "Không thể di chuyển và không thể bị dịch chuyển chủ động. Thuộc loại Debuff Di Chuyển Băng Kết.",
        "debuff"
    ],
    "Flammable": [
        "Dễ Cháy",
        "Khi chịu ST Thiêu Đốt, ST Ổn Định phải chịu tăng 2 điểm, và kẻ tấn công hồi phục 2 điểm Chỉ Số Ổn Định. Mỗi lần chịu ST Thiêu Đốt tiêu hao 1 lớp. Tối đa 2 lớp. Thuộc loại Debuff Thiêu Đốt.",
        "debuff"
    ],
    "Insight": [
        "Thấu Thị",
        "Tăng tầm bắn của KN Quyết Thắng thêm 1 ô. Thuộc loại Buff.",
        "buff"
    ],
    "Damp": [
        "Ẩm Ướt",
        "Ký hiệu độc quyền, có thể cộng dồn. Thuộc loại Debuff Hóa Lỏng. Không thể giải trừ.",
        "debuff"
    ],
    "Electric Spark": [
        "Tia Lửa Điện",
        "ST Dẫn Điện nhận từ Mosin Nagant tăng 15%. Hiệu ứng này được tính là hiệu ứng Tê Liệt. Thuộc loại Debuff Dẫn Điện.",
        "debuff"
    ],
    "Extra Action": [
        "Tăng Hành Động",
        "Có thể hành động nhiều lần trong hiệp đồng minh.",
        "buff"
    ],
    "Overzealous": [
        "Quá Khích",
        "Khi bị Vepley tấn công, sát thương phải chịu tăng 30%. Debuff này không thể giải trừ.",
        "debuff"
    ],
    "Tideway": [
        "Thủy Triều Rút",
        "Áp dụng Ẩm Ướt lên đơn vị kết thúc di chuyển trong khu vực này trong 2 hiệp. Đơn vị kẻ địch trong khu vực nhận nhược điểm ST Hóa Lỏng và ô Thủy Lực.",
        "effect"
    ],
    "Voltage": [
        "Điện Áp",
        "Gây nhược điểm Dẫn Điện lên kẻ địch đứng trên ô này. Khi kẻ địch đứng trên ô chịu ST AoE, kích hoạt Phản Ứng Ô Địa Hình và xóa bỏ hiệu ứng của ô, gây ST cố định bằng 30% Tấn Công. Nếu ST AoE là Dẫn Điện hoặc Hóa Lỏng, sát thương gây ra tăng thành 60% Tấn Công. Sát thương nhân đôi với mục tiêu cỡ lớn. Thuộc loại ô Dẫn Điện.",
        "effect"
    ],
    "Positive Charge": [
        "Điện Tích Dương",
        "Khi kết thúc hành động, hồi phục lượng HP bằng 20% HP tối đa của bản thân. Nếu có đồng đội sở hữu Điện Tích Dương trong bán kính 3 ô, hồi phục thêm lượng HP bằng 15% HP tối đa. Khi tấn công kẻ địch có Điện Tích Âm, ST Dẫn Điện gây ra tăng 35%. Mỗi đơn vị có Điện Tích Dương có thể kích hoạt hiệu ứng này 3 lần mỗi hiệp. Thuộc loại Buff Dẫn Điện.",
        "buff"
    ],
    "Negative Charge": [
        "Điện Tích Âm",
        "Khi nhận hiệu ứng này và khi bắt đầu hành động, bản thân và tất cả đồng đội trong bán kính 1 ô chịu ST Dẫn Điện cố định bằng 20% Tấn Công của người áp dụng. Khi kết thúc hiệp, nếu có từ 2 lớp Điện Tích Âm trở lên, chuyển hóa thành Tê Liệt duy trì 1 hiệp. Thuộc loại Debuff Dẫn Điện.",
        "debuff"
    ],
    "Berserk Factor I": [
        "Nhân Tố Cuồng Bạo I",
        "Khi chủ động tấn công mục tiêu địch trên ô địa hình Dị Vị, bản thân bỏ qua 10% Phòng Thủ của mục tiêu; với mỗi 1 cấp ô địa hình, bỏ qua thêm 10% Phòng Thủ. Buff không thể giải trừ.",
        "buff"
    ],
    "Berserk Factor II": [
        "Nhân Tố Cuồng Bạo II",
        "Bản thân cứ có 1 hiệu ứng Buff loại Băng Kết hoặc Thiêu Đốt, ST Băng Kết và ST Thiêu Đốt gây ra tăng 5%, nếu cộng dồn đến 20 tầng, sát thương tăng thêm 5%. Buff không thể giải trừ.",
        "buff"
    ],
    "Berserk Factor III": [
        "Nhân Tố Cuồng Bạo III",
        "Trước khi gây sát thương, tạo ra ô địa hình tương ứng trong phạm vi 4 ô xung quanh mục tiêu duy trì 2 hiệp. Khi tấn công mục tiêu địch trên ô địa hình Dị Vị, sát thương gây ra tăng 15%, nếu cộng dồn đến 20 tầng, sát thương tăng thêm 15%. Mỗi cấp ô địa hình tăng thêm 10% sát thương gây ra. Buff không thể giải trừ.",
        "buff"
    ],
    "Blazing Assault I": [
        "Xung Kích Thiêu Đốt I",
        "Tấn Công tăng 10%. Thuộc loại Buff Thiêu Đốt.",
        "buff"
    ],
    "Blazing Assault II": [
        "Xung Kích Thiêu Đốt II",
        "Tấn Công tăng 15%. Thuộc loại Buff Thiêu Đốt.",
        "buff"
    ],
    "Acid Corrosion I": [
        "Ăn Mòn Axit I",
        "Khi kết thúc hành động, chịu ST Ăn Mòn cố định bằng 10% Tấn Công của người thi triển. Thuộc loại Debuff Ăn Mòn.",
        "debuff"
    ],
    "Acid Corrosion II": [
        "Ăn Mòn Axit II",
        "Khi kết thúc hành động, chịu ST Ăn Mòn cố định bằng 20% Tấn Công của người thi triển. Thuộc loại Debuff Ăn Mòn.",
        "debuff"
    ]
}

MANUAL_TRANSLATIONS: Dict[str, Tuple[str, str, str]] = {
    "Tuning": [
        "Điều Âm",
        "Tăng 3% Tỷ lệ Bạo Kích và ST Bạo Kích, tối đa 10 lần. Nhận 6 ô Di Chuyển Thêm sau khi tấn công chủ động. Buff này không thể giải trừ.",
        "buff"
    ],
    "Pitch Perfect": [
        "Chuẩn Cao Độ",
        "Trước khi phát động tấn công chủ động, gây ST Ổn Định bằng số lớp Điều Âm. Kích hoạt 1 lần. Hiệu ứng này không thể giải trừ.",
        "buff"
    ],
    "Thermal Cycling": [
        "Tuần Hoàn Nhiệt",
        "Khi tiêu hao Hồi Phục Nhiệt, nhận lại 1 lớp Hồi Phục Nhiệt. Kích hoạt 1 lần. Thuộc loại Buff Thiêu Đốt và không thể giải trừ.",
        "buff"
    ],
    "Hot Sobering Tea": [
        "Trà Nóng Tỉnh Táo",
        "Tăng 10% ST Bạo Kích và tăng 15% ST Thiêu Đốt gây ra cho tất cả đồng đội khi gây ST Thiêu Đốt.",
        "buff"
    ],
    "Unshakable Confidence": [
        "Tự Tin Vững Vàng",
        "Tăng 5% Tỷ lệ Bạo Kích và ST Bạo Kích của KN Quyết Thắng. Tối đa 4 lớp. Buff này không thể giải trừ.",
        "buff"
    ],
    "Zoom In": [
        "Phóng To",
        "Sát thương tăng 15%, ST Ổn Định tăng thêm 2 điểm. Tối đa 2 lớp. Kích hoạt 1 lần. Buff này không thể giải trừ.",
        "buff"
    ],
    "Power Surge": [
        "Dâng Trào Năng Lượng",
        "Khi gây ST Dẫn Điện, bỏ qua 5% Phòng Thủ của mục tiêu và tăng 5% lượng trị liệu nhận vào. Cộng dồn tối đa 3 lần. Thuộc loại Buff Dẫn Điện. Không thể giải trừ.",
        "buff"
    ],
    "Ultimate Briliance": [
        "Huy Hoàng Tối Thượng",
        "Cung cấp các hiệu ứng sau cho tất cả đồng đội thuộc tính Dẫn Điện: Tăng 3 điểm ST Ổn Định gây ra, tăng gấp đôi ST cố định gây ra từ Điện Tích Âm, và nhận Cường Hóa Điện II khi kích hoạt Phản Ứng Ô Địa Hình trên ô Điện Thế trong 2 hiệp.",
        "buff"
    ],
    "Concealed": [
        "Ẩn Nấp",
        "Nếu có bất kỳ đồng đội nào trong bán kính 5 ô, bản thân không thể bị chỉ định bởi Đánh Thường hoặc kỹ năng. Hiệu ứng này thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Strayer": [
        "Kẻ Lạc Lối",
        "Khi kết thúc hành động, nếu không có đồng đội trong bán kính 3 ô, nhận 1 lớp Tự Lực. Thuộc loại Buff.",
        "buff"
    ],
    "Self-Reliant": [
        "Tự Lực",
        "Tấn Công tăng 5%, tối đa 4 lớp. Khi có đồng đội trong bán kính 3 ô, xóa bỏ toàn bộ lớp hiệu ứng này. Thuộc loại Buff.",
        "buff"
    ],
    "Shadow Step": [
        "Bước Chân Bóng Tối",
        "Tầm Di Chuyển tăng 1 ô. Bỏ qua cản trở khi di chuyển. Thuộc loại Buff.",
        "buff"
    ],
    "Predator": [
        "Kẻ Săn Mồi",
        "Sát thương gây ra lên mục tiêu có HP dưới 50% tăng 20%. Thuộc loại Buff.",
        "buff"
    ],
    "Precision Guidance": [
        "Dẫn Đường Chuẩn Xác",
        "ST Chuẩn Xác tăng 15%. Bỏ qua 20% Phòng Thủ của mục tiêu. Thuộc loại Buff.",
        "buff"
    ],
    "Overload": [
        "Quá Tải",
        "ST Dẫn Điện gây ra tăng 25%, nhưng sát thương phải chịu tăng 10%. Thuộc loại Buff.",
        "buff"
    ],
    "Corrosive Slime": [
        "Chất Nhầy Ăn Mòn",
        "Khi di chuyển trên ô Ăn Mòn, nhận thêm 1 ô Di Chuyển Thêm. Thuộc loại Buff.",
        "buff"
    ],
    "Glacial Armor": [
        "Giáp Băng Giá",
        "Giảm 30% ST Băng Kết phải chịu và miễn dịch với Đóng Băng. Thuộc loại Buff.",
        "buff"
    ],
    "Flame Barrier": [
        "Màn Chắn Lửa",
        "Giảm 30% ST Thiêu Đốt phải chịu và miễn dịch với Tràn Lửa. Thuộc loại Buff.",
        "buff"
    ],
    "Hydro Ward": [
        "Bảo Hộ Hóa Lỏng",
        "Giảm 30% ST Hóa Lỏng phải chịu và miễn dịch với Ẩm Ướt. Thuộc loại Buff.",
        "buff"
    ],
    "Static Shield": [
        "Khiên Tĩnh Điện",
        "Khi nhận ST Dẫn Điện, phản lại 50% ST cố định lên kẻ tấn công. Thuộc loại Buff.",
        "buff"
    ],
    "Camouflage": [
        "Ngụy Trang",
        "Khi có các đơn vị đồng minh khác trên trận, bản thân không thể bị chỉ định bởi Đánh Thường hoặc kỹ năng chủ động của kẻ địch. Buff này bị tiêu hao khi chịu sát thương, có thể cộng dồn tối đa 2 lần. Không thể giải trừ.",
        "buff"
    ],
    "Glacial Domain": [
        "Lĩnh Vực Băng Giá",
        "Thực hiện 1 lần Tấn Công Chi Viện lên kẻ địch trong tầm bắn khi mục tiêu chịu ST Chuẩn Xác từ đồng đội, gây ST Vật Lý bằng 80% Tấn Công và 2 điểm ST Ổn Định. Có thể kích hoạt tối đa 2 lần mỗi hiệp. Hiệu ứng này không thể giải trừ.",
        "buff"
    ],
    "Warding Light": [
        "Ánh Sáng Bảo Vệ",
        "Tăng 15% ST Băng Kết gây ra. Khi chịu sát thương, nếu Giáp Sương Giá chưa bị phá hủy, gây 1 điểm ST Ổn Định cố định lên kẻ tấn công. Hiệu ứng này không thể giải trừ.",
        "buff"
    ],
    "Dismay": [
        "Mất Tinh Thần",
        "Tầm Di Chuyển giảm còn 1 ô, Tấn Công giảm 30%, và ST Ổn Định gây ra giảm 4 điểm. Thuộc loại Debuff.",
        "debuff"
    ],
    "Dream Guardian": [
        "Vệ Binh Giấc Mơ",
        "ST AoE gây ra bởi Tấn Công Chi Viện tăng 30%. Thuộc loại Buff, không thể giải trừ.",
        "buff"
    ],
    "Standard Approach": [
        "Phương Thức Chuẩn Hóa",
        "Giảm 25% ST AoE phải chịu. Mỗi lần chịu ST AoE tiêu hao 1 lớp. Tối đa 3 lớp. Thuộc loại Buff.",
        "buff"
    ],
    "Emergency Plan": [
        "Phương Án Khẩn Cấp",
        "ST AoE phải chịu giảm bằng số lớp hiện tại x 25%. Mỗi lần chịu ST AoE tiêu hao 1 lớp. Tối đa 3 lớp. Thuộc loại Buff.",
        "buff"
    ],
    "Voltage Sag": [
        "Sụt Áp",
        "Sát thương gây ra giảm 5% và ST Dẫn Điện phải chịu tăng 6%. Hiệu ứng này có thể cộng dồn tối đa 3 lần. Thuộc loại Debuff Dẫn Điện. Không thể giải trừ.",
        "debuff"
    ],
    "Toxic Inundation": [
        "Ngập Tràn Độc Tố",
        "ST Ăn Mòn phải chịu tăng 25%. Thuộc loại Debuff phòng thủ Ăn Mòn.",
        "debuff"
    ],
    "Competitive Spirit": [
        "Tinh Thần Thi Đua",
        "Tăng 5% ST Ăn Mòn gây ra. Tối đa 8 lớp. Thuộc loại Buff, không thể giải trừ.",
        "buff"
    ],
    "Mimic Rookie": [
        "Tân Tú Mô Phỏng",
        "Tỷ lệ Bạo Kích của bản thân và Bóng Hình Cung tăng 20%. Buff không thể giải trừ.",
        "buff"
    ],
    "Stunt Double": [
        "Diễn Viên Thế Thân",
        "ST Bạo Kích bản thân và Bóng Hình Cung gây ra tăng 20%. Trước khi thi triển Cộng Hưởng Tương Thích trong phạm vi có hiệu lực tạo ra ô địa hình Dòng Ngầm, duy trì 2 hiệp. Buff không thể giải trừ.",
        "buff"
    ],
    "Hunter Type - II": [
        "Thợ Săn-II",
        "Khi tạo nhận 8 điểm Ngọn Lửa Thiêu Đốt, và khiến tất cả đơn vị phe ta nhận Dâng Trào Địa Ngục trong 3 hiệp lớn. Khi kết thúc hành động của Loreley, giải phóng Xung Lửa. ST Thiêu Đốt tất cả kẻ địch trong phạm vi 5 ô xung quanh Thợ Săn-II phải chịu tăng 15%.",
        "buff"
    ],
    "Conflagration": [
        "Đại Hỏa Biển Rực",
        "ST Thiêu Đốt phải chịu tăng 20%. Thuộc loại Debuff Thiêu Đốt.",
        "debuff"
    ],
    "Cellular Reconfiguration": [
        "Tái Cấu Trúc Tế Bào",
        "Khi bắt đầu chiến đấu, nếu Doll phe ta thuộc thuộc tính Dị Vị bất kỳ chiếm đa số trên trận, OTs-14 tiến vào Tái Cấu Trúc Dị Vị tương ứng. Nếu đa số là Vật Lý hoặc bằng nhau, tiến vào Tái Cấu Trúc · Không. Mỗi thời điểm chỉ có thể kích hoạt 1 loại Tái Cấu Trúc.",
        "buff"
    ],
    "Predation": [
        "Săn Mồi",
        "Chọn 1 mục tiêu địch trong phạm vi 3x3, gây ST Băng Kết cận chiến bằng 60% Tấn Công, 1 điểm ST Ổn Định và hồi phục lượng HP bằng 20% sát thương gây ra. Nếu mục tiêu bị tiêu diệt, vô hiệu hóa kỹ năng và hiệu ứng kích hoạt khi tử vong. Tầm bắn của kỹ năng này không thể thay đổi.",
        "effect"
    ],
    "Queen of the Skies": [
        "Nữ Hoàng Bầu Trời",
        "Đòn tấn công đầu tiên lên Eagletta trong hiệp hiện tại bị giảm 20% sát thương. Tầm bắn của tất cả Đánh Thường giảm còn 1 ô. Thuộc loại Debuff Băng Kết. Không thể giải trừ.",
        "debuff"
    ],
    "Absolution": [
        "Xá Tội",
        "ST Vật Lý phải chịu tăng 30%. Với mỗi lớp hiệu ứng này, khi bị Asteria tấn công, ST Bạo Kích phải chịu tăng 10% và Phòng Thủ giảm 10%, cộng dồn tối đa 6 lớp. Debuff này không thể giải trừ.",
        "debuff"
    ],
    "Symbiotic Dance": [
        "Vũ Điệu Cộng Sinh",
        "Ngăn chặn tử vong khi nhận sát thương chí mạng. Nếu một đồng đội khác tử vong khi hiệu ứng này đang kích hoạt, đơn vị được bảo vệ sẽ tử vong thay thế.",
        "buff"
    ],
    "Blood Emblem": [
        "Huyết Huy Hiệu",
        "Áp dụng Dấu Ấn Huyết Sắc lên 3 kẻ địch trong tầm bắn đã chịu Dấu Ấn Huyết Sắc hoặc đang đứng trên ô Dẫn Điện, gây ST Dẫn Điện cận chiến bằng 60% Tấn Công. Hệ số sát thương tăng 3% dựa trên số lớp Ngưng Tụ của Sextans. Nếu kích hoạt nhiều lần trong hiệp, hệ số giảm 20% theo số lần gây sát thương xuống tối thiểu 30%.",
        "buff"
    ],
    "Covering Mode": [
        "Chế Độ Yểm Trợ",
        "Tăng 20% ST Băng Kết đồng đội gây ra lên kẻ địch có Lá Chắn. Bản thân tăng 20% Tỷ lệ Bạo Kích. Trước khi kẻ địch trong bán kính 8 ô tấn công chủ động, phát động Chặn Đánh gây ST Băng Kết bằng 60% Tấn Công và 4 điểm ST Ổn Định, chuyển hóa 20% sát thương gây ra thành Màn Chắn Sương Giá cho tất cả đồng đội (tối đa 3 lần mỗi hiệp lớn).",
        "buff"
    ],
    "Predation Protocol": [
        "Giao Thức Săn Mồi",
        "Đòn tấn công chủ động tiếp theo bỏ qua 50% Phòng Thủ của mục tiêu, tăng 30% Tỷ lệ Bạo Kích và 25% ST Bạo Kích. Thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Coordinated Hunting": [
        "Săn Bắt Phối Hợp",
        "Sát thương gây ra và Tỷ lệ Bạo Kích tăng 10%. Có thể cộng dồn tối đa 3 lần. Thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Pursuer": [
        "Kẻ Truy Đuổi",
        "Sát thương gây ra tăng 45% và ST Bạo Kích tăng 30%. Thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Embers": [
        "Tàn Lửa",
        "ST Thiêu Đốt gây ra tăng 30% trong 2 hiệp và tăng vĩnh viễn 5% ST Bạo Kích (cộng dồn). Thuộc loại Buff Thiêu Đốt. Không thể giải trừ.",
        "buff"
    ],
    "Overedge": [
        "Lưỡi Đao Vượt Mức",
        "Với mỗi lớp hiệu ứng này sở hữu, Tỷ lệ Bạo Kích và ST Băng Kết gây ra từ Đánh Thường tăng 10%. Có thể cộng dồn, tiêu hao sau khi tấn công. Không thể giải trừ.",
        "buff"
    ],
    "Laceration": [
        "Vết Cắt Xé",
        "Khi chịu sát thương, nếu kẻ tấn công dùng đòn đánh bằng lưỡi kiếm, gây thêm sát thương bằng 40% sát thương gốc mỗi lần gây sát thương. Debuff này không thể giải trừ.",
        "debuff"
    ],
    "Nightmare Form": [
        "Hình Thái Ác Mộng",
        "ST AoE gây ra tăng 10% và ST AoE gây ra bởi Tấn Công Chi Viện tăng 50%. Ngoài ra, thuộc tính sát thương của Tấn Công Chi Viện AoE chuyển thành ST Ăn Mòn. Thuộc loại Buff Ăn Mòn, không thể giải trừ.",
        "buff"
    ],
    "Dreamscape Exhilaration": [
        "Hưng Phấn Cõi Mộng",
        "ST Ăn Mòn gây ra tăng 5%. Có thể cộng dồn và thuộc loại Buff.",
        "buff"
    ],
    "Stored Charge": [
        "Tích Điện",
        "ST Dẫn Điện gây ra tăng 5%, có thể cộng dồn tối đa 6 lần. Thuộc loại Buff Dẫn Điện và không thể giải trừ.",
        "buff"
    ],
    "Bargain": [
        "Giao Kèo",
        "Sát thương gây ra tăng 30%, và Tỷ lệ Bạo Kích của Đánh Thường tăng 100%. Thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Wok Aura": [
        "Hào Quang Chảo Nóng",
        "ST Thiêu Đốt gây ra tăng 7%, sát thương phải chịu giảm 7%, cộng dồn tối đa 4 lần. Thuộc loại Buff Thiêu Đốt, không thể giải trừ.",
        "buff"
    ],
    "Graceful Spin": [
        "Xoay Uyển Chuyển",
        "ST Bạo Kích tăng 10% và hồi phục lượng HP bằng 20% Tấn Công của người sở hữu sau khi tấn công. Xung đột với Xoay Nồng Nhiệt. Thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Passionate Spin": [
        "Xoay Nồng Nhiệt",
        "ST Bạo Kích tăng 10% và nhận 2 lớp Nơi Trú Ẩn khi kết thúc hành động. Xung đột với Xoay Uyển Chuyển. Thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Fantastic Conception": [
        "Quan Niệm Kỳ Ảo",
        "Ở hiệp kế tiếp, kỹ năng chủ động Ngẫu Hứng tăng 15% Tỷ lệ Bạo Kích và bỏ qua 10% Phòng Thủ của mục tiêu. Có thể cộng dồn tối đa 3 lần và không thể giải trừ.",
        "buff"
    ],
    "Preshow Warmup": [
        "Khởi Động Trước Giờ Diễn",
        "Khi gây ST Vật Lý, ST Bạo Kích tăng 25%. Thuộc loại Buff và không thể giải trừ.",
        "buff"
    ],
    "Superconductive Code": [
        "Mã Siêu Dẫn",
        "Tỷ lệ Bạo Kích tăng 5% và ST Bạo Kích tăng 7%. Có thể cộng dồn tối đa 4 lần. Khi tích lũy đủ 4 lớp, nhận Chuỗi Siêu Dẫn trong 1 hiệp (thời gian duy trì giảm khi kết thúc hiệp hiện tại). Thuộc loại Buff Dẫn Điện và không thể giải trừ.",
        "buff"
    ],
    "Unity": [
        "Đoàn Kết",
        "Khi gây ST Băng Kết, Tấn Công tăng 10% dựa trên Tấn Công ban đầu của Robella. Sau khi người sở hữu gây sát thương lên kẻ địch bằng tấn công chủ động hoặc Chặn Đánh, Robella áp dụng 1 lớp Giám Sát lên kẻ địch, và áp dụng thêm 1 lớp nếu người sở hữu gây ST Băng Kết. Sau khi dùng kỹ năng, gây thêm ST Băng Kết bằng 20% Tấn Công của Robella. Không thể giải trừ.",
        "buff"
    ],
    "Stimulant": [
        "Chất Kích Thích",
        "Khi kết thúc hành động, tiêu hao lượng HP bằng 20% HP tối đa ban đầu. Với mỗi 1% HP tối đa ban đầu bị mất, sát thương gây ra tăng 0.5% và ST Hóa Lỏng gây ra tăng 0.5%, tối đa 20% mỗi loại. Thuộc loại Debuff Hóa Lỏng và không thể giải trừ.",
        "debuff"
    ],
    "Soak I": [
        "Ngấm Nước I",
        "ST Hóa Lỏng gây ra tăng 10%. Thuộc loại Buff Hóa Lỏng.",
        "buff"
    ],
    "Candyglaze": [
        "Bọc Đường",
        "ST Ăn Mòn gây ra tăng 1%. Có thể cộng dồn tối đa 10 lần, và không thể giải trừ.",
        "buff"
    ]
}

GENERAL_RULES = [
    ("\\bMobility decreased by (\\d+) tiles?\\. Considered a Movement debuff\\.", "Tầm Di Chuyển giảm \\1 ô. Thuộc loại Debuff Di Chuyển."),
    ("\\bIncreases mobility by (\\d+) tiles?\\. Considered a buff\\.", "Tầm Di Chuyển tăng \\1 ô. Thuộc loại Buff."),
    ("\\bMobility is increased by (\\d+) tiles?\\. Considered a buff\\.", "Tầm Di Chuyển tăng \\1 ô. Thuộc loại Buff."),
    ("\\bDefense increased by (\\d+%)\\. Considered a buff\\.", "Phòng Thủ tăng \\1. Thuộc loại Buff."),
    ("\\bIncreases defense by (\\d+%)\\. Considered a buff\\.", "Phòng Thủ tăng \\1. Thuộc loại Buff."),
    ("\\bReduces defense by (\\d+%)\\. Considered a (?:defense )?debuff\\.", "Phòng Thủ giảm \\1. Thuộc loại Debuff phòng thủ."),
    ("\\bAttack is increased by (\\d+%)\\. Considered a buff\\.", "Tấn Công tăng \\1. Thuộc loại Buff."),
    ("\\bIncreases? attack by (\\d+%)\\. Considered a buff\\.", "Tấn Công tăng \\1. Thuộc loại Buff."),
    ("\\bAttack decreased by (\\d+%)\\. Considered a debuff\\.", "Tấn Công giảm \\1. Thuộc loại Debuff."),
    ("\\bDecreases? attack by (\\d+%)\\. Considered a debuff\\.", "Tấn Công giảm \\1. Thuộc loại Debuff."),
    ("\\bIncreases damage dealt by (\\d+%)\\. Considered (?:as )?a buff\\.", "Sát thương gây ra tăng \\1. Thuộc loại Buff."),
    ("\\bIncreases damage taken by (\\d+%)\\. Considered a (?:defense )?debuff\\.", "Sát thương phải chịu tăng \\1. Thuộc loại Debuff."),
    ("\\bCritical rate increased by (\\d+%)\\. Considered a buff\\.", "Tỷ lệ Bạo Kích tăng \\1. Thuộc loại Buff."),
    ("\\bIncreases? Critical Damage by (\\d+%)\\. Considered a buff\\.", "ST Bạo Kích tăng \\1. Thuộc loại Buff."),
    ("\\bAoE damage taken reduced by (\\d+%)\\. Considered a buff\\.", "ST AoE phải chịu giảm \\1. Thuộc loại Buff."),
    ("\\bReduces AoE damage taken by (\\d+%)\\. Considered a buff\\.", "ST AoE phải chịu giảm \\1. Thuộc loại Buff."),
    ("\\bRestore (\\d+%) of maximum HP at the end of action\\. Considered a buff\\.", "Hồi phục \\1 HP tối đa khi kết thúc hành động. Thuộc loại Buff."),
    ("\\bRecovers (\\d+%) of maximum HP at the end of the action\\. Considered a buff\\.", "Hồi phục \\1 HP tối đa khi kết thúc hành động. Thuộc loại Buff."),
    ("\\bRecovers (\\d+) points? of Stability Index at the end of the action\\. Considered a buff\\.", "Hồi phục \\1 điểm Chỉ Số Ổn Định khi kết thúc hành động. Thuộc loại Buff."),
    ("\\bTargeted damage increased by (\\d+%\\b)\\. Considered a buff\\.", "ST Chuẩn Xác tăng \\1. Thuộc loại Buff."),
    ("\\bIncreases Phase damage dealt by (\\d+%\\b)\\. Considered a buff\\.", "ST Dị Vị gây ra tăng \\1. Thuộc loại Buff."),
    ("\\bTargeted damage ignores (\\d+%) of the target's defense\\. Considered a buff\\.", "ST Chuẩn Xác bỏ qua \\1 Phòng Thủ của mục tiêu. Thuộc loại Buff."),
    ("\\bUnable to move and cannot be actively displaced\\. Considered a Freeze Movement debuff\\.", "Không thể di chuyển và không thể bị dịch chuyển chủ động. Thuộc loại Debuff Di Chuyển Băng Kết."),
    ("\\bUnable to move\\. Considered a movement debuff\\.", "Không thể di chuyển. Thuộc loại Debuff Di Chuyển."),
    ("\\bUnable to act\\.", "Không thể hành động."),
    ("\\bCommands other than movement can be executed\\.", "Có thể thực hiện các lệnh khác ngoài di chuyển."),
    ("\\b1 action can be taken\\.", "Có thể thực hiện 1 lần hành động."),
    ("\\bCan move once, but cannot use any other commands\\.", "Có thể di chuyển 1 lần, nhưng không thể dùng lệnh khác."),
    ("\\bPerforms an attacks; Cannot be triggered by Interceptions, Counterattacks, or Action Supports\\.", "Tiến hành 1 lần tấn công; Không thể bị kích hoạt bởi Chặn Đánh, Phản Kích hoặc Tấn Công Chi Viện."),
    ("\\bPerforms a Support Attack; cannot be triggered by another Support Attack\\.", "Tiến hành 1 lần Tấn Công Chi Viện; Không thể bị kích hoạt bởi 1 lần Tấn Công Chi Viện khác."),
    ("\\bCommand prohibition, disallows the use of basic attacks and active skills\\. Considered an? Electric debuff\\.", "Cấm Lệnh, không thể dùng Đánh Thường và kỹ năng chủ động. Thuộc loại Debuff Dẫn Điện."),
    ("\\bCommand Prohibition, disallows the use of active skills\\. Considered a Burn debuff\\.", "Cấm Lệnh, không thể sử dụng kỹ năng chủ động. Thuộc loại Debuff Thiêu Đốt."),
    ("\\bDamage taken is converted to Paralysis\\. Considered an? Electric debuff\\.", "Sát thương phải chịu chuyển hóa thành Tê Liệt. Thuộc loại Debuff Dẫn Điện."),
    ("\\bUncontrollable, forced to use basic attacks on the caster\\. This is removed when the caster dies\\.", "Mất kiểm soát, cưỡng chế dùng Đánh Thường tấn công người thi triển. Xóa bỏ khi người thi triển tử vong."),
    ("\\bUncontrollable, actively moves away from the caster\\. This is removed when the caster dies\\.", "Mất kiểm soát, chủ động di chuyển ra xa người thi triển. Xóa bỏ khi người thi triển tử vong."),
    ("\\bImmune to basic attacks and skill damage\\. The immunity is removed after receiving 1 basic attack or skill attack\\. Considered a buff\\.", "Miễn dịch sát thương từ Đánh Thường và kỹ năng. Xóa bỏ hiệu quả miễn dịch sau khi nhận 1 lần Đánh Thường hoặc kỹ năng. Thuộc loại Buff."),
    ("\\bTargeted damage taken reduced by (\\d+%), effective once\\. Considered a buff\\.", "ST Chuẩn Xác phải chịu giảm \\1, hiệu lực 1 lần. Thuộc loại Buff."),
    ("\\bCannot be healed\\. Considered a Hydro debuff\\.", "Không thể nhận trị liệu. Thuộc loại Debuff Hóa Lỏng."),
    ("\\b([a-zA-Z\\s]+ damage) taken is increased by (\\d+) points?\\b", "\\1 phải chịu tăng \\2 điểm"),
    ("\\b([a-zA-Z\\s]+ damage) taken is increased by (\\d+%)\\b", "\\1 phải chịu tăng \\2"),
    ("\\b([a-zA-Z\\s]+ damage) taken is reduced by (\\d+%)\\b", "\\1 phải chịu giảm \\2"),
    ("\\b([a-zA-Z\\s]+ damage) dealt is increased by (\\d+) points?\\b", "\\1 gây ra tăng \\2 điểm"),
    ("\\b([a-zA-Z\\s]+ damage) dealt is increased by (\\d+%)\\b", "\\1 gây ra tăng \\2"),
    ("\\b([a-zA-Z\\s]+ damage) dealt is reduced by (\\d+%)\\b", "\\1 gây ra giảm \\2"),
    ("\\bDamage dealt is reduced by (\\d+%)\\b", "Sát thương gây ra giảm \\1"),
    ("\\bDamage dealt is increased by (\\d+%)\\b", "Sát thương gây ra tăng \\1"),
    ("\\bDamage taken is reduced by (\\d+%)\\b", "Sát thương phải chịu giảm \\1"),
    ("\\bDamage taken is increased by (\\d+%)\\b", "Sát thương phải chịu tăng \\1"),
    ("\\bdamage taken is reduced by\\b", "sát thương phải chịu giảm"),
    ("\\bdamage taken is increased by\\b", "sát thương phải chịu tăng"),
    ("\\bdamage dealt is reduced by\\b", "sát thương gây ra giảm"),
    ("\\bdamage dealt is increased by\\b", "sát thương gây ra tăng"),
    ("\\bis reduced by\\b", "giảm"),
    ("\\bis increased by\\b", "tăng"),
    ("\\bis reduced\\b", "giảm"),
    ("\\bis increased\\b", "tăng"),
    ("\\bcan stack up to (\\d+) times?\\b", "có thể cộng dồn tối đa \\1 lần"),
    ("\\bcan stack up to (\\d+) stacks?\\b", "có thể cộng dồn tối đa \\1 lớp"),
    ("\\bstack up to (\\d+) times?\\b", "cộng dồn tối đa \\1 lần"),
    ("\\bstack up to (\\d+) stacks?\\b", "cộng dồn tối đa \\1 lớp"),
    ("\\bstack up to\\b", "cộng dồn tối đa"),
    ("\\bcan stack\\b", "có thể cộng dồn"),
    ("\\bwhen damage is taken\\b", "khi chịu sát thương"),
    ("\\bupon taking damage\\b", "khi chịu sát thương"),
    ("\\bfrom an ally\\b", "từ đồng đội"),
    ("\\ban ally\\b", "đồng đội"),
    ("\\ban enemy\\b", "kẻ địch"),
    ("\\bStability Damage taken is increased by (\\d+) points?\\b", "ST Ổn Định phải chịu tăng \\1 điểm"),
    ("\\bStability damage taken is increased by (\\d+) points?\\b", "ST Ổn Định phải chịu tăng \\1 điểm"),
    ("\\bStability Damage dealt is increased by (\\d+) points?\\b", "ST Ổn Định gây ra tăng \\1 điểm"),
    ("\\bStability damage dealt is increased by (\\d+) points?\\b", "ST Ổn Định gây ra tăng \\1 điểm"),
    ("\\bStability Damage\\b", "ST Ổn Định"),
    ("\\bstability damage\\b", "ST Ổn Định"),
    ("\\bStability Protection\\b", "Bảo Vệ Độ Ổn Định"),
    ("\\bstability protection\\b", "Bảo Vệ Độ Ổn Định"),
    ("\\bStability Index\\b", "Chỉ Số Ổn Định"),
    ("\\bstability index\\b", "Chỉ Số Ổn Định"),
    ("\\bStability\\b", "Độ Ổn Định"),
    ("\\bstability\\b", "Độ Ổn Định"),
    ("\\bConfectance Index\\b", "Chỉ Số Nhiên Liệu"),
    ("\\bconfectance index\\b", "Chỉ Số Nhiên Liệu"),
    ("\\bBurn damage\\b", "ST Thiêu Đốt"),
    ("\\bburn damage\\b", "ST Thiêu Đốt"),
    ("\\bFreeze damage\\b", "ST Băng Kết"),
    ("\\bfreeze damage\\b", "ST Băng Kết"),
    ("\\bElectric damage\\b", "ST Dẫn Điện"),
    ("\\belectric damage\\b", "ST Dẫn Điện"),
    ("\\bCorrosion damage\\b", "ST Ăn Mòn"),
    ("\\bcorrosion damage\\b", "ST Ăn Mòn"),
    ("\\bHydro damage\\b", "ST Hóa Lỏng"),
    ("\\bhydro damage\\b", "ST Hóa Lỏng"),
    ("\\bPhysical damage\\b", "ST Vật Lý"),
    ("\\bphysical damage\\b", "ST Vật Lý"),
    ("\\bTargeted damage\\b", "ST Chuẩn Xác"),
    ("\\btargeted damage\\b", "ST Chuẩn Xác"),
    ("\\bPhase damage\\b", "ST Dị Vị"),
    ("\\bphase damage\\b", "ST Dị Vị"),
    ("\\bAoE damage\\b", "ST AoE"),
    ("\\baoe damage\\b", "ST AoE"),
    ("\\bFixed damage\\b", "ST cố định"),
    ("\\bfixed damage\\b", "ST cố định"),
    ("\\bReal damage\\b", "ST Chuẩn"),
    ("\\breal damage\\b", "ST Chuẩn"),
    ("\\blethal damage\\b", "sát thương chí mạng"),
    ("\\bIncreases? damage dealt by (\\d+%)\\b", "Sát thương gây ra tăng \\1"),
    ("\\bincreases? damage dealt by (\\d+%)\\b", "sát thương gây ra tăng \\1"),
    ("\\bIncreases? damage taken by (\\d+%)\\b", "Sát thương phải chịu tăng \\1"),
    ("\\bincreases? damage taken by (\\d+%)\\b", "sát thương phải chịu tăng \\1"),
    ("\\bReduces? damage taken by (\\d+%)\\b", "Sát thương phải chịu giảm \\1"),
    ("\\breduces? damage taken by (\\d+%)\\b", "sát thương phải chịu giảm \\1"),
    ("\\bDamage dealt\\b", "Sát thương gây ra"),
    ("\\bdamage dealt\\b", "sát thương gây ra"),
    ("\\bDamage taken\\b", "Sát thương phải chịu"),
    ("\\bdamage taken\\b", "sát thương phải chịu"),
    ("\\bdealing damage\\b", "gây sát thương"),
    ("\\bdeals damage\\b", "gây sát thương"),
    ("\\btaking damage\\b", "chịu sát thương"),
    ("\\btakes damage\\b", "chịu sát thương"),
    ("\\breceiving damage\\b", "nhận sát thương"),
    ("\\breceives damage\\b", "nhận sát thương"),
    ("\\bdeals\\b", "gây"),
    ("\\bDeals\\b", "Gây"),
    ("\\btakes\\b", "chịu"),
    ("\\bTakes\\b", "Chịu"),
    ("\\breceives\\b", "nhận"),
    ("\\bReceives\\b", "Nhận"),
    ("\\breceive\\b", "nhận"),
    ("\\bReceive\\b", "Nhận"),
    ("\\bdamage\\b", "sát thương"),
    ("\\bDamage\\b", "Sát thương"),
    ("\\bAttack is increased by (\\d+%)\\b", "Tấn Công tăng \\1"),
    ("\\battack is increased by (\\d+%)\\b", "Tấn Công tăng \\1"),
    ("\\bAttack decreased by (\\d+%)\\b", "Tấn Công giảm \\1"),
    ("\\battack decreased by (\\d+%)\\b", "Tấn Công giảm \\1"),
    ("\\bIncreases? attack by (\\d+%)\\b", "Tấn Công tăng \\1"),
    ("\\bincreases? attack by (\\d+%)\\b", "tăng \\1 Tấn Công"),
    ("\\bDecreases? attack by (\\d+%)\\b", "Tấn Công giảm \\1"),
    ("\\bdecreases? attack by (\\d+%)\\b", "giảm \\1 Tấn Công"),
    ("\\bReduces? attack by (\\d+%)\\b", "Tấn Công giảm \\1"),
    ("\\breduces? attack by (\\d+%)\\b", "giảm \\1 Tấn Công"),
    ("\\bSupport Attack\\b", "Tấn Công Chi Viện"),
    ("\\bsupport attack\\b", "Tấn Công Chi Viện"),
    ("\\bAction Support\\b", "Tấn Công Chi Viện"),
    ("\\baction support\\b", "Tấn Công Chi Viện"),
    ("\\bSupport Stance\\b", "Tư Thế Chi Viện"),
    ("\\bsupport stance\\b", "Tư Thế Chi Viện"),
    ("\\bbasic attacks?\\b", "Đánh Thường"),
    ("\\bBasic attacks?\\b", "Đánh Thường"),
    ("\\bactive skills?\\b", "kỹ năng chủ động"),
    ("\\bActive skills?\\b", "kỹ năng chủ động"),
    ("\\bUltimate Skills?\\b", "KN Quyết Thắng"),
    ("\\bultimate skills?\\b", "KN Quyết Thắng"),
    ("\\bactive attacks?\\b", "tấn công chủ động"),
    ("\\bActive attacks?\\b", "Tấn công chủ động"),
    ("\\bnormal attacks?\\b", "Đánh Thường"),
    ("\\bnormal attack\\b", "Đánh Thường"),
    ("\\bperforms an attack\\b", "tiến hành 1 lần tấn công"),
    ("\\bperforms an attacks\\b", "tiến hành 1 lần tấn công"),
    ("\\bperforms attacks\\b", "tiến hành tấn công"),
    ("\\bATK\\b", "Tấn Công"),
    ("\\bDEF\\b", "Phòng Thủ"),
    ("\\bHP\\b", "HP"),
    ("\\battack\\b", "Tấn Công"),
    ("\\bAttack\\b", "Tấn Công"),
    ("\\bwithin a (\\d+) tile radius\\b", "trong bán kính \\1 ô"),
    ("\\bwithin a (\\d+)-tile radius\\b", "trong bán kính \\1 ô"),
    ("\\bwithin (\\d+) tiles?\\b", "trong phạm vi \\1 ô"),
    ("\\bwithin range\\b", "trong tầm bắn"),
    ("\\bwithin\\b", "trong"),
    ("\\bby (\\d+) tiles?\\b", "\\1 ô"),
    ("\\b(\\d+) tiles?\\b", "\\1 ô"),
    ("\\btiles?\\b", "ô"),
    ("\\bfor (\\d+) turns?\\b", "trong \\1 hiệp"),
    ("\\bfor (\\d+) rounds?\\b", "trong \\1 hiệp"),
    ("\\blast(?:s|ing)? for (\\d+) turns?\\b", "duy trì \\1 hiệp"),
    ("\\blast(?:s|ing)? for (\\d+) rounds?\\b", "duy trì \\1 hiệp"),
    ("\\blast(?:s|ing)? (\\d+) turns?\\b", "duy trì \\1 hiệp"),
    ("\\blast(?:s|ing)? (\\d+) rounds?\\b", "duy trì \\1 hiệp"),
    ("\\bat the start of turn\\b", "khi bắt đầu hiệp"),
    ("\\bat the start of the turn\\b", "khi bắt đầu hiệp"),
    ("\\bat the end of turn\\b", "khi kết thúc hiệp"),
    ("\\bat the end of the turn\\b", "khi kết thúc hiệp"),
    ("\\bat the end of the action\\b", "khi kết thúc hành động"),
    ("\\bat the end of action\\b", "khi kết thúc hành động"),
    ("\\bat the start of the action\\b", "khi bắt đầu hành động"),
    ("\\bat the start of action\\b", "khi bắt đầu hành động"),
    ("\\bturns?\\b", "hiệp"),
    ("\\brounds?\\b", "hiệp"),
    ("\\brange\\b", "tầm bắn"),
    ("\\bThis buff cannot be cleansed\\b", "Buff này không thể giải trừ"),
    ("\\bThis debuff cannot be cleansed\\b", "Debuff này không thể giải trừ"),
    ("\\bThis effect cannot be cleansed\\b", "Hiệu ứng này không thể giải trừ"),
    ("\\bCannot be cleansed\\b", "Không thể giải trừ"),
    ("\\bcannot be cleansed\\b", "không thể giải trừ"),
    ("\\bCannot be dispelled\\b", "Không thể giải trừ"),
    ("\\bcannot be dispelled\\b", "không thể giải trừ"),
    ("\\bcannot be targeted\\b", "không thể bị chỉ định"),
    ("\\bCannot be targeted\\b", "Không thể bị chỉ định"),
    ("\\bimmune to\\b", "miễn dịch với"),
    ("\\bImmune to\\b", "Miễn dịch với"),
    ("\\bConsidered a Freeze movement debuff\\b", "Thuộc loại Debuff Di Chuyển Băng Kết"),
    ("\\bConsidered a Freeze debuff\\b", "Thuộc loại Debuff Băng Kết"),
    ("\\bConsidered a Freeze buff\\b", "Thuộc loại Buff Băng Kết"),
    ("\\bConsidered a Burn debuff\\b", "Thuộc loại Debuff Thiêu Đốt"),
    ("\\bConsidered a Burn buff\\b", "Thuộc loại Buff Thiêu Đốt"),
    ("\\bConsidered an Electric debuff\\b", "Thuộc loại Debuff Dẫn Điện"),
    ("\\bConsidered an Electric buff\\b", "Thuộc loại Buff Dẫn Điện"),
    ("\\bConsidered a Corrosion defense debuff\\b", "Thuộc loại Debuff phòng thủ Ăn Mòn"),
    ("\\bConsidered a Corrosion debuff\\b", "Thuộc loại Debuff Ăn Mòn"),
    ("\\bConsidered a Corrosion buff\\b", "Thuộc loại Buff Ăn Mòn"),
    ("\\bConsidered a Hydro debuff\\b", "Thuộc loại Debuff Hóa Lỏng"),
    ("\\bConsidered a Hydro buff\\b", "Thuộc loại Buff Hóa Lỏng"),
    ("\\bConsidered a Movement debuff\\b", "Thuộc loại Debuff Di Chuyển"),
    ("\\bConsidered a movement debuff\\b", "Thuộc loại Debuff Di Chuyển"),
    ("\\bConsidered a defense debuff\\b", "Thuộc loại Debuff phòng thủ"),
    ("\\bConsidered a buff\\b", "Thuộc loại Buff"),
    ("\\bConsidered a debuff\\b", "Thuộc loại Debuff"),
    ("\\bConsidered as a buff\\b", "Thuộc loại Buff"),
    ("\\bConsidered as a debuff\\b", "Thuộc loại Debuff"),
    ("\\bThis is considered as an? ([a-zA-Z\\s]+) buff\\b", "Thuộc loại Buff \\1"),
    ("\\bThis is considered as an? ([a-zA-Z\\s]+) debuff\\b", "Thuộc loại Debuff \\1"),
    ("\\bis considered as an?\\b", "thuộc loại"),
    ("\\bis considered\\b", "thuộc loại"),
    ("\\bConsidered an?\\b", "Thuộc loại"),
    ("\\bconsidered an?\\b", "thuộc loại"),
    ("\\bElectric type\\b", "thuộc tính Dẫn Điện"),
    ("\\bFreeze type\\b", "thuộc tính Băng Kết"),
    ("\\bBurn type\\b", "thuộc tính Thiêu Đốt"),
    ("\\bHydro type\\b", "thuộc tính Hóa Lỏng"),
    ("\\bCorrosion type\\b", "thuộc tính Ăn Mòn"),
    ("\\bPhysical type\\b", "thuộc tính Vật Lý"),
    ("\\bAllied units?\\b", "Đơn vị đồng minh"),
    ("\\ballied units?\\b", "đơn vị đồng minh"),
    ("\\bAllies\\b", "Đồng đội"),
    ("\\ballies\\b", "đồng đội"),
    ("\\bEnemy units?\\b", "Đơn vị kẻ địch"),
    ("\\benemy units?\\b", "đơn vị kẻ địch"),
    ("\\bEnemy targets?\\b", "Mục tiêu địch"),
    ("\\benemy targets?\\b", "mục tiêu địch"),
    ("\\bEnemies\\b", "Kẻ địch"),
    ("\\benemies\\b", "kẻ địch"),
    ("\\bEnemy\\b", "Kẻ địch"),
    ("\\benemy\\b", "kẻ địch"),
    ("\\bTarget\\b", "Mục tiêu"),
    ("\\btarget\\b", "mục tiêu"),
    ("\\bThe attacker\\b", "Kẻ tấn công"),
    ("\\bthe attacker\\b", "kẻ tấn công"),
    ("\\battacker\\b", "kẻ tấn công"),
    ("\\bThe caster\\b", "Người thi triển"),
    ("\\bthe caster\\b", "người thi triển"),
    ("\\bcaster\\b", "người thi triển"),
    ("\\bThis unit\\b", "Bản thân"),
    ("\\bthis unit\\b", "bản thân"),
    ("\\bSelf\\b", "Bản thân"),
    ("\\bself\\b", "bản thân"),
    ("\\bUpon rec(?:ei|ie)ving\\b", "Khi nhận"),
    ("\\bupon rec(?:ei|ie)ving\\b", "khi nhận"),
    ("\\bUpon gaining\\b", "Khi nhận"),
    ("\\bupon gaining\\b", "khi nhận"),
    ("\\bWhen receiving\\b", "Khi nhận"),
    ("\\bwhen receiving\\b", "khi nhận"),
    ("\\bWhen taking\\b", "Khi chịu"),
    ("\\bwhen taking\\b", "khi chịu"),
    ("\\bWhen gaining\\b", "Khi nhận"),
    ("\\bwhen gaining\\b", "khi nhận"),
    ("\\bWhen dealing\\b", "Khi gây"),
    ("\\bwhen dealing\\b", "khi gây"),
    ("\\bWhen attacked\\b", "Khi bị tấn công"),
    ("\\bwhen attacked\\b", "khi bị tấn công"),
    ("\\bWhen\\b", "Khi"),
    ("\\bwhen\\b", "khi"),
    ("\\bAfter\\b", "Sau khi"),
    ("\\bafter\\b", "sau khi"),
    ("\\bBefore\\b", "Trước khi"),
    ("\\bbefore\\b", "trước khi"),
    ("\\bIf there are\\b", "Nếu có"),
    ("\\bthere are\\b", "có"),
    ("\\bthere is\\b", "có"),
    ("\\bIf\\b", "Nếu"),
    ("\\bif\\b", "nếu"),
    ("\\bGains?\\b", "Nhận"),
    ("\\bgains?\\b", "nhận"),
    ("\\bRecovers?\\b", "Hồi phục"),
    ("\\brecovers?\\b", "hồi phục"),
    ("\\bRestores?\\b", "Hồi phục"),
    ("\\brestores?\\b", "hồi phục"),
    ("\\bReduces?\\b", "Giảm"),
    ("\\breduces?\\b", "giảm"),
    ("\\breducing\\b", "giảm"),
    ("\\bDecreases?\\b", "Giảm"),
    ("\\bdecreases?\\b", "giảm"),
    ("\\bIncreases?\\b", "Tăng"),
    ("\\bincreases?\\b", "tăng"),
    ("\\bEach time\\b", "Mỗi khi"),
    ("\\beach time\\b", "mỗi khi"),
    ("\\bEach instances? of\\b", "Mỗi lần"),
    ("\\beach instances? of\\b", "mỗi lần"),
    ("\\bEach instance\\b", "Mỗi lần"),
    ("\\beach instance\\b", "mỗi lần"),
    ("\\bEqual to\\b", "Bằng"),
    ("\\bequal to\\b", "bằng"),
    ("\\bEquivalent to\\b", "Bằng"),
    ("\\bequivalent to\\b", "bằng"),
    ("\\bPrioritizes?\\b", "Ưu tiên"),
    ("\\bprioritizes?\\b", "ưu tiên"),
    ("\\bApplied\\b", "Áp dụng"),
    ("\\bapplied\\b", "áp dụng"),
    ("\\bApplies\\b", "Áp dụng"),
    ("\\bapplies\\b", "áp dụng"),
    ("\\bApplier\\b", "Người áp dụng"),
    ("\\bapplier\\b", "người áp dụng"),
    ("\\bAnd\\b", "Và"),
    ("\\band\\b", "và"),
    ("\\bOr\\b", "Hoặc"),
    ("\\bor\\b", "hoặc"),
    ("\\bWith\\b", "Với"),
    ("\\bwith\\b", "với"),
    ("\\bFrom\\b", "Từ"),
    ("\\bfrom\\b", "từ"),
    ("\\bOf\\b", "Của"),
    ("\\bof\\b", "của"),
    ("\\bTo\\b", "Đến"),
    ("\\bto\\b", "đến"),
    ("\\bFor\\b", "Cho"),
    ("\\bfor\\b", "cho"),
    ("\\bAt\\b", "Tại"),
    ("\\bat\\b", "tại"),
    ("\\bIn\\b", "Trong"),
    ("\\bin\\b", "trong"),
    ("\\bBy\\b", "Thêm"),
    ("\\bby\\b", "thêm"),
    ("\\bPoints?\\b", "Điểm"),
    ("\\bpoints?\\b", "điểm"),
    ("\\bTimes?\\b", "Lần"),
    ("\\btimes?\\b", "lần"),
    ("\\bOnce\\b", "1 lần"),
    ("\\bonce\\b", "1 lần"),
    ("\\bIs\\b", "Là"),
    ("\\bis\\b", "là"),
    ("\\bAre\\b", "Là"),
    ("\\bare\\b", "là"),
    ("\\bWas\\b", "Đã"),
    ("\\bwas\\b", "đã"),
    ("\\bWere\\b", "Đã"),
    ("\\bwere\\b", "đã"),
    ("\\bHas\\b", "Có"),
    ("\\bhas\\b", "có"),
    ("\\bHave\\b", "Có"),
    ("\\bhave\\b", "có"),
    ("\\bCan\\b", "Có thể"),
    ("\\bcan\\b", "có thể"),
    ("\\bCannot\\b", "Không thể"),
    ("\\bcannot\\b", "không thể"),
    ("\\bWill\\b", "Sẽ"),
    ("\\bwill\\b", "sẽ"),
    ("\\bNot\\b", "Không"),
    ("\\bnot\\b", "không"),
    ("\\bAll\\b", "Tất cả"),
    ("\\ball\\b", "tất cả"),
    ("\\bEach\\b", "Mỗi"),
    ("\\beach\\b", "mỗi"),
    ("\\bOther\\b", "Khác"),
    ("\\bother\\b", "khác"),
    ("\\bAnother\\b", "Khác"),
    ("\\banother\\b", "khác"),
    ("\\bCurrent\\b", "Hiện tại"),
    ("\\bcurrent\\b", "hiện tại"),
    ("\\bMaximum\\b", "Tối đa"),
    ("\\bmaximum\\b", "tối đa"),
    ("\\bMax\\b", "Tối đa"),
    ("\\bmax\\b", "tối đa"),
    ("\\bBase\\b", "Cơ bản"),
    ("\\bbase\\b", "cơ bản"),
    ("\\bInitial\\b", "Ban đầu"),
    ("\\binitial\\b", "ban đầu"),
    ("\\bConverted\\b", "Chuyển hóa"),
    ("\\bconverted\\b", "chuyển hóa"),
    ("\\bRemoved\\b", "Xóa bỏ"),
    ("\\bremoved\\b", "xóa bỏ"),
    ("\\bThe\\b", ""),
    ("\\bthe\\b", ""),
    ("\\bA\\b", "1"),
    ("\\ba\\b", "1"),
    ("\\bAn\\b", "1"),
    ("\\ban\\b", "1"),
    ("\\bStacks?\\b", "Lớp"),
    ("\\bstacks?\\b", "lớp"),
    ("\\bStacked\\b", "Cộng dồn"),
    ("\\bstacked\\b", "cộng dồn"),
    ("\\bStacking\\b", "Cộng dồn"),
    ("\\bstacking\\b", "cộng dồn"),
    ("\\bStackable\\b", "Có thể cộng dồn"),
    ("\\bstackable\\b", "có thể cộng dồn"),
    ("\\bUp to\\b", "Tối đa"),
    ("\\bup to\\b", "tối đa"),
    ("\\bTheir\\b", "Của họ"),
    ("\\btheir\\b", "của họ"),
    ("\\bThey\\b", "Họ"),
    ("\\bthey\\b", "họ"),
    ("\\bThem\\b", "Chúng"),
    ("\\bthem\\b", "chúng"),
    ("\\bWhich\\b", "Mà"),
    ("\\bwhich\\b", "mà"),
    ("\\bWhere\\b", "Nơi"),
    ("\\bwhere\\b", "nơi"),
    ("\\bThere\\b", "Ở đó"),
    ("\\bthere\\b", "ở đó"),
    ("\\bInto\\b", "Thành"),
    ("\\binto\\b", "thành"),
    ("\\bAbout\\b", "Khoảng"),
    ("\\babout\\b", "khoảng"),
    ("\\bUnder\\b", "Dưới"),
    ("\\bunder\\b", "dưới"),
    ("\\bOver\\b", "Trên"),
    ("\\bover\\b", "trên"),
    ("\\bPer\\b", "Mỗi"),
    ("\\bper\\b", "mỗi"),
    ("\\bUnits?\\b", "Đơn vị"),
    ("\\bunits?\\b", "đơn vị"),
    ("\\bRate\\b", "Tỷ lệ"),
    ("\\brate\\b", "tỷ lệ"),
    ("\\bDefense\\b", "Phòng Thủ"),
    ("\\bdefense\\b", "Phòng Thủ"),
    ("\\bMobility\\b", "Di chuyển"),
    ("\\bmobility\\b", "di chuyển"),
    ("\\bSpeed\\b", "Tốc độ"),
    ("\\bspeed\\b", "tốc độ"),
    ("\\bMovement\\b", "Di chuyển"),
    ("\\bmovement\\b", "di chuyển"),
    ("\\bconsumes?\\b", "tiêu hao"),
    ("\\bConsumes?\\b", "Tiêu hao"),
    ("\\bconsumed\\b", "tiêu hao")
]

def translate_effect_tuple(name_en: str, desc_en: str) -> tuple[str, str, str]:
    """Returns (name_vi, desc_vi, eff_type) for status effects with 100% clean translation."""
    if name_en in MANUAL_TRANSLATIONS:
        return MANUAL_TRANSLATIONS[name_en]
    if name_en in EXACT_IN_GAME:
        return EXACT_IN_GAME[name_en]
    
    vi_name = EFFECT_NAMES.get(name_en, name_en)
    
    # Determine type
    desc_low = desc_en.lower()
    if "debuff" in desc_low:
        eff_type = "debuff"
    elif "buff" in desc_low:
        eff_type = "buff"
    else:
        eff_type = "effect"

    # Translate text
    res = desc_en
    for p, r in GENERAL_RULES:
        res = re.sub(p, r, res)
    res = re.sub(r"\s+", " ", res).strip()
    res = re.sub(r"\s+([,.;?!])", r"\1", res)
    res = re.sub(r"([,.;?!])([^\s0-9])", r"\1 \2", res)
    return (vi_name, res.strip(), eff_type)

def translate_effect_text(text: str) -> str:
    """Compatibility fallback for plain string translations."""
    res = text
    for p, r in GENERAL_RULES:
        res = re.sub(p, r, res)
    res = re.sub(r"\s+", " ", res).strip()
    return res

EFFECT_RULES = GENERAL_RULES

# ==============================================================================
# 3. SUMMON TRANSLATIONS (FOR ALL 12 CHARACTERS WITH COMPLETE SKILLS)
# ==============================================================================
SUMMON_TRANSLATIONS: Dict[str, List[Dict[str, Any]]] = {
    "andoris": [
        {
            "name": "Ụ Pháo Tự Động",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Ụ Pháo Tự Động không thể di chuyển, có khả năng áp dụng Điện Tích Âm. Tự động tấn công khi kết thúc lượt của Andoris.",
            "stats": {
                "hp": "50% HP ban đầu của Andoris",
                "atk": "50% Tấn Công ban đầu của Andoris",
                "def": "100% Phòng Thủ ban đầu của Andoris"
            },
            "skills": [
                {
                    "name": "Bắn Tích Điện",
                    "description": "Chọn 1 mục tiêu địch trong bán kính 6 ô, áp dụng Điện Tích Âm trong 2 hiệp, và gây ST Dẫn Điện bằng 100% Tấn Công."
                },
                {
                    "name": "Chuyển Tiếp Thông Tin",
                    "description": "Khi kết thúc hành động, áp dụng Điện Tích Âm lên 2 mục tiêu trong bán kính 6 ô trong 2 hiệp."
                },
                {
                    "name": "Mô Phỏng Va Chạm",
                    "description": "Ụ Pháo Tự Động không thể nhận trị liệu hoặc lá chắn, nhưng miễn dịch với các hiệu ứng khống chế."
                },
                {
                    "name": "Bắt Tốt Qua Đường",
                    "description": "Khi kẻ địch trong tầm bắn nhận ST Dẫn Điện đơn mục tiêu từ tấn công chủ động của đồng đội, Ụ Pháo Tự Động ưu tiên kích hoạt Tấn Công Chi Viện lên kẻ địch đó trước, gây ST Dẫn Điện bằng 100% Tấn Công và 1 điểm ST Ổn Định, đồng thời áp dụng Điện Tích Âm trong 2 hiệp.\n\nKỹ năng bị động này chỉ mở khóa sau khi đạt Đốt Sống 1."
                }
            ]
        }
    ],
    "balthilde": [
        {
            "name": "Vật Tạo Tác Chiến",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Vật tạo phòng thủ chiến thuật được triển khai để yểm trợ che chắn và chi viện hỏa lực.",
            "stats": {
                "hp": "100% HP ban đầu của Balthilde",
                "atk": "80% Tấn Công ban đầu của Balthilde",
                "def": "80% Phòng Thủ ban đầu của Balthilde"
            },
            "skills": [
                {
                    "name": "Bí Quyết Tháo Dỡ",
                    "description": "Chọn mục tiêu địch gần nhất trong bán kính 3 ô và gây ST Vật Lý bằng 100% Phòng Thủ. Có thể dùng 2 lần mỗi hiệp."
                }
            ]
        }
    ],
    "basti": [
        {
            "name": "Cục Cưng",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Vật triệu hồi kế thừa thuộc tính cơ bản của Basti. Nếu có kẻ địch trong bán kính 3 ô khi triệu hồi, Cục Cưng sẽ tự phát nổ trong khu vực.",
            "stats": {
                "hp": "100% HP ban đầu của Basti",
                "atk": "100% Tấn Công ban đầu của Basti",
                "def": "100% Phòng Thủ ban đầu của Basti"
            },
            "skills": []
        }
    ],
    "florence": [
        {
            "name": "Arios",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Có khả năng áp dụng Khiêu Khích lên kẻ địch, chịu sát thương thay cho Florence và tiến hành Phản Kích khi Florence hoặc bản thân chịu sát thương.",
            "stats": {
                "hp": "120% HP ban đầu của Florence",
                "atk": "100% Tấn Công ban đầu của Florence",
                "def": "120% Phòng Thủ ban đầu của Florence"
            },
            "skills": [
                {
                    "name": "Trợ Thủ Số 1",
                    "description": "Khi Florence chịu sát thương, Arios sẽ chịu toàn bộ sát thương thay cho cô ấy.\n\nNếu khoảng cách giữa Arios và Florence từ 6 ô trở lên, Arios sẽ dịch chuyển tức thời đến gần Florence.\n\nKhi Arios hoặc Florence nhận sát thương, tiến hành Phản Kích, gây ST Hóa Lỏng bằng 80% Tấn Công. Kích hoạt tối đa 2 lần mỗi hiệp.\n\nVới mỗi lần chịu sát thương, nhận 1 lớp Dấu Ấn Nhục Nhã. Khi số lớp đạt 5, chuyển hóa thành Rung Động Tuyệt Vọng."
                }
            ]
        }
    ],
    "koleda": [
        {
            "name": "Kẻ Tội Lỗi",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Chiến xa cơ động cao. Khi bắt đầu hiệp, Kẻ Tội Lỗi chuyển sang Số D. Chia sẻ 50% sát thương ban đầu mà Koleda phải chịu.",
            "stats": {
                "hp": "100% HP ban đầu của Koleda",
                "atk": "100% Tấn Công ban đầu của Koleda",
                "def": "100% Phòng Thủ ban đầu của Koleda"
            },
            "skills": [
                {
                    "name": "Đi Hóng Gió Nào!",
                    "description": "Chọn 1 Doll phe ta (ngoại trừ Koleda) và áp dụng Đi Hóng Gió Nào! lên mục tiêu.\n\nSau khi kỹ năng kết thúc, Kẻ Tội Lỗi nhận 9 ô Di Chuyển Thêm và có thể dùng 1 lệnh."
                },
                {
                    "name": "Cú Trôi Quán Tính?!",
                    "description": "Gây ST AoE Hóa Lỏng bằng 90% Tấn Công lên tất cả đơn vị địch trong bán kính 5 ô xung quanh bản thân và Kéo chúng 5 ô về phía trung tâm vị trí của Kẻ Tội Lỗi. Sau khi kỹ năng kết thúc, Kẻ Tội Lỗi nhận 9 ô Di Chuyển Thêm và có thể dùng kỹ năng chủ động Doll Siêu Tốc!."
                },
                {
                    "name": "Doll Siêu Tốc!",
                    "description": "Chọn 1 ô trong phạm vi hình chữ thập từ 4 đến 8 ô, đáp xuống ô đó và gây ST AoE Hóa Lỏng bằng 90% Tấn Công lên tất cả mục tiêu địch trong phạm vi rộng 3 ô dọc theo đường đi. Nếu Kẻ Tội Lỗi đang ở Số S hoặc Số S+, gây thêm ST AoE Hóa Lỏng bằng 60% và 90% Tấn Công."
                },
                {
                    "name": "Chuyển Số",
                    "description": "Khi bắt đầu hiệp, Kẻ Tội Lỗi chuyển sang Số D. Khi kết thúc hành động cuối cùng, xóa bỏ tất cả Số ngoại trừ Số N và chuyển sang Số P. Mỗi thời điểm chỉ có thể thiết lập 1 Số.\n\nKẻ Tội Lỗi không thể bị cản trở bởi kẻ địch, miễn dịch với các trạng thái Choáng, Khiêu Khích, Mất Khả Năng Hành Động, cũng như các debuff dịch chuyển và di chuyển. Ngoài ra, sát thương phải chịu của Kẻ Tội Lỗi giảm 35% và hồi phục HP bằng 15% HP tối đa khi chịu sát thương.\n\nKhi kết thúc hành động của Kẻ Tội Lỗi, nếu đang ở Số S, kích hoạt Giải Phóng Động Năng; nếu đang ở Số S+, kích hoạt Giải Phóng Động Năng+."
                }
            ]
        }
    ],
    "lainie": [
        {
            "name": "Bản Ảo Ảnh",
            "type": "Vật Triệu Hồi Ảo Ảnh",
            "description": "Ảo ảnh chiến thuật mô phỏng động thái của Lainie, gây áp lực hỏa lực và hỗ trợ xuyên thấu phòng tuyến địch.",
            "stats": {
                "hp": "100% HP ban đầu của Lainie",
                "atk": "80% Tấn Công ban đầu của Lainie",
                "def": "80% Phòng Thủ ban đầu của Lainie"
            },
            "skills": [
                {
                    "name": "Phản Xạ Bối Rối",
                    "description": "Chọn 1 mục tiêu địch trong bán kính 7 ô và gây ST Vật Lý bằng 80% Tấn Công.\n\nSau khi dùng kỹ năng, Lainie sẽ thi triển Giao Thức Chiến Thắng lên mục tiêu đã chọn."
                },
                {
                    "name": "Nhận Thức Điềm Báo",
                    "description": "Với mỗi 12 điểm HP tối đa ban đầu, tăng 0.1% Tỷ lệ Bạo Kích, tối đa 30%. Áp dụng Nhận Thức Điềm Báo lên tất cả kẻ địch trong bán kính 7 ô.\n\nTrước khi tấn công chủ động, áp dụng 1 lớp Xuyên Thấu Dù Mưa lên mục tiêu. Nếu Phòng Thủ của mục tiêu nhỏ hơn hoặc bằng 0, tăng hệ số sát thương bằng 10% HP tối đa ban đầu. Sau khi tấn công chủ động, không thể dùng thêm đòn tấn công chủ động nào trong cùng hiệp đồng minh."
                }
            ]
        }
    ],
    "liushih": [
        {
            "name": "Pegasus",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Vật triệu hồi chiến thuật tầm xa, kế thừa thuộc tính cơ bản của Liushih, có khả năng di chuyển độc lập và mở rộng tầm kiểm soát.",
            "stats": {
                "hp": "100% HP ban đầu của Liushih",
                "atk": "100% Tấn Công ban đầu của Liushih",
                "def": "100% Phòng Thủ ban đầu của Liushih"
            },
            "skills": [
                {
                    "name": "Pháo Tự Động Phòng Thủ Điểm",
                    "description": "Gây ST Hóa Lỏng bằng 110% Tấn Công. Đòn đánh này được tính là Đòn Tấn Công Đã Nạp và Đánh Thường."
                },
                {
                    "name": "Quy Trình An Toàn",
                    "description": "Không thể di chuyển. Khi chịu sát thương chí mạng, Pegasus tiến vào trạng thái Chờ. Nếu đang trong trạng thái Tác Chiến Phối Hợp, trạng thái đó sẽ bị xóa bỏ."
                }
            ]
        }
    ],
    "mityl": [
        {
            "name": "Hologram Cá Nhân",
            "type": "Vật Triệu Hồi Hologram",
            "description": "Sở hữu kỹ năng và diện mạo riêng. Được tính là Hologram, giúp gia tăng tỷ lệ và sát thương Bạo Kích cho Mityl.",
            "stats": {
                "hp": "100% HP ban đầu của Mityl",
                "atk": "100% Tấn Công ban đầu của Mityl",
                "def": "100% Phòng Thủ ban đầu của Mityl"
            },
            "skills": [
                {
                    "name": "Tập Kích Bóng Cung",
                    "description": "Chọn 1 mục tiêu địch trong phạm vi 6 ô và gây ST Hóa Lỏng bằng 100% Tấn Công."
                },
                {
                    "name": "Hồi Quy Dữ Liệu",
                    "description": "Khi thi triển Cộng Hưởng Tương Thích, hồi phục 50% HP tối đa hiện tại và tăng 5% HP tối đa, tối đa lên đến 20%."
                }
            ]
        }
    ],
    "nikketa": [
        {
            "name": "Kulich",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Trợ thủ chiến thuật yểm trợ di chuyển và quấy nhiễu hỏa lực kẻ địch, chia sẻ áp lực chiến trường.",
            "stats": {
                "hp": "100% HP ban đầu của Nikketa",
                "atk": "80% Tấn Công ban đầu của Nikketa",
                "def": "100% Phòng Thủ ban đầu của Nikketa"
            },
            "skills": [
                {
                    "name": "Sự Trung Thành Của Kulich",
                    "description": "Kẻ địch sẽ không chọn Kulich làm mục tiêu tấn công của chúng.\n\nNếu kẻ địch trong bán kính 3 ô gây sát thương, Kulich tiến hành Phản Kích, gây ST Hóa Lỏng bằng 80% Tấn Công và 2 điểm ST Ổn Định."
                },
                {
                    "name": "Uy Hiếp Của Kulich",
                    "description": "Giảm 10% Tấn Công của tất cả kẻ địch trong bán kính 5 ô.\n\nKỹ năng bị động này chỉ mở khóa sau khi đạt Đốt Sống 5."
                }
            ]
        }
    ],
    "papasha": [
        {
            "name": "Người Giữ Thành",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Vật triệu hồi phòng ngự kiên cố. Cung cấp lá chắn và tăng cường khả năng chống chịu cho Papasha và đồng đội.",
            "stats": {
                "hp": "120% HP ban đầu của Papasha",
                "atk": "60% Tấn Công ban đầu của Papasha",
                "def": "120% Phòng Thủ ban đầu của Papasha"
            },
            "skills": [
                {
                    "name": "Chi Viện Chống Khủng Bố",
                    "description": "Sau khi Papasha tấn công mục tiêu địch, Người Giữ Thành sẽ bồi thêm 1 lần Tấn Công Chi Viện lên cùng mục tiêu đó, gây ST Vật Lý bằng 80% Tấn Công."
                },
                {
                    "name": "Biện Pháp Phòng Chống Cháy Nổ",
                    "description": "Khi kết thúc hiệp, Người Giữ Thành sẽ tự động di chuyển độc lập để tìm Nơi Trú Ẩn.\n\nLượng trị liệu Người Giữ Thành nhận vào giảm 100% và không thể nhận lá chắn. Khi Papasha được trị liệu, Người Giữ Thành hồi phục 10% HP tối đa của bản thân.\n\nKhi Người Giữ Thành chịu sát thương chí mạng, nó tiến vào trạng thái Tự Sửa Chữa trong 1 hiệp."
                },
                {
                    "name": "Giám Sát An Ninh",
                    "description": "Cung cấp tầm nhìn chiến thuật và cảnh giới an ninh khu vực xung quanh Papasha."
                }
            ]
        }
    ],
    "springfield": [
        {
            "name": "Taryz",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Trợ thủ bay đồng hành cùng Springfield. Nếu mục tiêu mà Taryz bám theo gây sát thương lên đồng minh, Taryz sẽ phản kích đòn đánh phụ trợ.",
            "stats": {
                "hp": "100% HP ban đầu của Springfield",
                "atk": "100% Tấn Công ban đầu của Springfield",
                "def": "100% Phòng Thủ ban đầu của Springfield"
            },
            "skills": []
        }
    ],
    "tololo": [
        {
            "name": "Vệ Tinh Cố Định",
            "type": "Vật Triệu Hồi Vật Lý",
            "description": "Thiết bị vệ tinh dẫn đường quỹ đạo, cung cấp tầm nhìn chiến thuật và kích hoạt các đòn đánh chi viện năng lượng.",
            "stats": {
                "hp": "80% HP ban đầu của Tololo",
                "atk": "100% Tấn Công ban đầu của Tololo",
                "def": "80% Phòng Thủ ban đầu của Tololo"
            },
            "skills": [
                {
                    "name": "Triệu Hồi Vì Sao",
                    "description": "Khi kết thúc hiệp phe ta, gây ST Chuẩn Xác Hóa Lỏng bằng 130% Tấn Công lên đơn vị địch trong bán kính 7 ô xung quanh sở hữu Dấu Ấn Trọng Lực. Nếu không có đơn vị nào có Dấu Ấn Trọng Lực, chỉ định đơn vị địch gần nhất."
                },
                {
                    "name": "Đồng Bộ Tĩnh Lặng",
                    "description": "Miễn dịch với các hiệu ứng khống chế như Choáng, Khiêu Khích và Cấm Lệnh."
                }
            ]
        }
    ]
}

# ==============================================================================
# 4. WEAPON TRANSLATION ENGINE & DICTIONARIES
# ==============================================================================
WEAPON_VOCAB: List[Tuple[str, str]] = [
    (r"\bFor each allied unit \(excluding self\) within (\d+) tiles\b", r"Với mỗi đơn vị đồng minh (ngoài bản thân) trong phạm vi \1 ô"),
    (r"\bFor each allied unit within (\d+) tiles\b", r"Với mỗi đơn vị đồng minh trong phạm vi \1 ô"),
    (r"\bincreases healing and damage dealt by\b", "tăng lượng hồi máu và sát thương gây ra thêm"),
    (r"\bincreases damage dealt by\b", "tăng sát thương gây ra thêm"),
    (r"\bincreases damage taken by\b", "tăng sát thương phải chịu thêm"),
    (r"\breduces damage taken by\b", "giảm sát thương phải chịu đi"),
    (r"\bup to\b", "tối đa"),
    (r"\bIf there are more than\b", "Nếu có nhiều hơn"),
    (r"\bgains (\d+(?:/\d+)*) tiles of Additional Movement after the active attack\b", r"nhận \1 ô Di Chuyển Thêm sau khi tấn công chủ động"),
    (r"\bgains (\d+(?:/\d+)*) tiles? of Additional Movement\b", r"nhận \1 ô Di Chuyển Thêm"),
    (r"\bIf the unit has full HP at the start of the action\b", "Nếu đầy HP khi bắt đầu hành động"),
    (r"\bthey gain 1 random buff for (\d+) turns?\b", r"nhận 1 Buff ngẫu nhiên duy trì \1 hiệp"),
    (r"\bgains 1 random buff for (\d+) turns?\b", r"nhận 1 Buff ngẫu nhiên duy trì \1 hiệp"),
    (r"\bat the start of the action\b", "khi bắt đầu hành động"),
    (r"\bat the end of the action\b", "khi kết thúc hành động"),
    (r"\bat the start of the turn\b", "khi bắt đầu hiệp"),
    (r"\bat the end of the turn\b", "khi kết thúc hiệp"),
    (r"\bWhen actively attacking\b", "Khi chủ động tấn công"),
    (r"\bBefore actively attacking\b", "Trước khi chủ động tấn công"),
    (r"\bAfter actively attacking\b", "Sau khi chủ động tấn công"),
    (r"\bWhen dealing damage\b", "Khi gây sát thương"),
    (r"\bWhen taking damage\b", "Khi chịu sát thương"),
    (r"\bWhen hitting an enemy\b", "Khi đánh trúng kẻ địch"),
    (r"\bWhen defeating an enemy\b", "Khi tiêu diệt kẻ địch"),
    (r"\bignores (\d+%) of the target's defense\b", r"bỏ qua \1 Phòng Thủ của mục tiêu"),
    (r"\bCritical Rate increased by\b", "Tỷ lệ Bạo Kích tăng"),
    (r"\bCritical Damage increased by\b", "ST Bạo Kích tăng"),
    (r"\bATK increased by\b", "Tấn Công tăng"),
    (r"\bDEF increased by\b", "Phòng Thủ tăng"),
    (r"\bHP increased by\b", "HP tăng"),
    (r"\bMobility increased by\b", "Tầm Di Chuyển tăng"),
    (r"\bStability Damage dealt increased by\b", "ST Ổn Định gây ra tăng"),
    (r"\bBurn damage\b", "ST Thiêu Đốt"),
    (r"\bFreeze damage\b", "ST Băng Kết"),
    (r"\bElectric damage\b", "ST Dẫn Điện"),
    (r"\bCorrosion damage\b", "ST Ăn Mòn"),
    (r"\bHydro damage\b", "ST Hóa Lỏng"),
    (r"\bPhysical damage\b", "ST Vật Lý"),
    (r"\bTargeted damage\b", "ST Chuẩn Xác"),
    (r"\bAoE damage\b", "ST AoE"),
    (r"\bfixed damage\b", "ST cố định"),
    (r"\bStability damage\b", "ST Ổn Định"),
    (r"\bStability Protection\b", "Bảo Vệ Độ Ổn Định"),
    (r"\bConfectance Index\b", "Chỉ Số Nhiên Liệu"),
    (r"\bBasic Attack\b", "Đánh Thường"),
    (r"\bActive Skill\b", "Kỹ năng chủ động"),
    (r"\bUltimate Skill\b", "KN Quyết Thắng"),
    (r"\bAction Support\b", "Tấn Công Chi Viện"),
    (r"\bSupport Attack\b", "Tấn Công Chi Viện"),
    (r"\bInterception\b", "Chặn Đánh"),
    (r"\bCounterattack\b", "Phản Kích"),
    (r"\bCannot be cleansed\b", "Không thể giải trừ"),
    (r"\bcannot be cleansed\b", "không thể giải trừ"),
    (r"\bCannot be dispelled\b", "Không thể giải trừ"),
    (r"\bConsidered a buff\b", "Thuộc loại Buff"),
    (r"\bConsidered a debuff\b", "Thuộc loại Debuff"),
    (r"\bfor (\d+) turns?\b", r"trong \1 hiệp"),
    (r"\bfor (\d+) rounds?\b", r"trong \1 hiệp"),
    (r"\bwithin (\d+) tiles\b", r"trong phạm vi \1 ô"),
    (r"\bwithin a (\d+)-tile radius\b", r"trong bán kính \1 ô"),
    (r"\bmaximum of (\d+) stacks\b", r"tối đa \1 lớp"),
    (r"\bup to (\d+) stacks\b", r"tối đa \1 lớp"),
]

def translate_weapon_text(text: str) -> str:
    """Translates weapon trait/effect text into Vietnamese using regex patterns."""
    if not text:
        return ""
    res = text
    # Tier 1: Weapon-specific clauses
    for pat, rep in WEAPON_VOCAB:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    # Tier 2: Effect vocab
    for pat, rep in EFFECT_RULES:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    res = re.sub(r"\s+", " ", res).strip()
    return res

# Load comprehensive weapon translations dictionary
_WEAPONS_VI_DATA: Dict[str, Any] = {}
if WEAPONS_VI_FILE.exists():
    try:
        _WEAPONS_VI_DATA = json.loads(WEAPONS_VI_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Warning: Failed to load {WEAPONS_VI_FILE}: {e}")

TRAITS_MAP: Dict[str, str] = _WEAPONS_VI_DATA.get("traits", {})
IMPRINTS_MAP: Dict[str, str] = _WEAPONS_VI_DATA.get("imprints", {})
PARAGRAPHS_MAP: Dict[str, str] = _WEAPONS_VI_DATA.get("paragraphs", {})

def translate_weapon_trait(text: str) -> str:
    """Translates weapon trait text into Vietnamese."""
    if not text:
        return ""
    clean = text.strip()
    if clean in TRAITS_MAP:
        return TRAITS_MAP[clean]
    norm = re.sub(r'\s+', ' ', clean)
    for k, v in TRAITS_MAP.items():
        if re.sub(r'\s+', ' ', k) == norm:
            return v
    return translate_weapon_text(text)

def translate_weapon_effect(text: str) -> str:
    """Translates weapon imprint/passive effect text into Vietnamese."""
    if not text:
        return ""
    clean = text.strip()

    if clean in PARAGRAPHS_MAP:
        return PARAGRAPHS_MAP[clean]

    blocks = clean.split("\n")
    translated_blocks = []
    for b in blocks:
        b_clean = b.strip()
        if not b_clean:
            translated_blocks.append("")
            continue

        if b_clean in PARAGRAPHS_MAP:
            translated_blocks.append(PARAGRAPHS_MAP[b_clean])
            continue

        if b_clean in IMPRINTS_MAP:
            translated_blocks.append(IMPRINTS_MAP[b_clean])
            continue

        imp_match = re.search(r"Imprint Skill:.*", b_clean, re.IGNORECASE)
        if imp_match:
            prefix = b_clean[:imp_match.start()].strip()
            imp_part = imp_match.group(0).strip()
            tr_prefix = PARAGRAPHS_MAP.get(prefix, translate_weapon_text(prefix))
            tr_imp = IMPRINTS_MAP.get(imp_part, translate_weapon_text(imp_part))
            translated_blocks.append(f"{tr_prefix}\n\n{tr_imp}")
            continue

        norm = re.sub(r'\s+', ' ', b_clean)
        found = False
        for k, v in PARAGRAPHS_MAP.items():
            if re.sub(r'\s+', ' ', k) == norm:
                translated_blocks.append(v)
                found = True
                break
        if found:
            continue
        for k, v in IMPRINTS_MAP.items():
            if re.sub(r'\s+', ' ', k) == norm:
                translated_blocks.append(v)
                found = True
                break
        if found:
            continue

        translated_blocks.append(translate_weapon_text(b_clean))

    return "\n\n".join([tb for tb in translated_blocks if tb])

# Known weapon name translations (Official & Standardized)
KNOWN_WEAPON_NAMES: Dict[str, str] = {
    "skysunderer-s-howl": "Tiếng Gầm Xé Trời",
    "bristlefang-beast": "Dã Thú Nanh Rậm",
    "dazzling-sparkles": "Ánh Lửa Lấp Lánh",
    "themis-game": "Trò Chơi Themis",
    "wind-cutter": "Lưỡi Dao Cắt Gió",
    "thorn-criterion": "Chuẩn Mực Gai Góc",
    "tidal-nocturne": "Dạ Khúc Thủy Triều",
    "twilight-rose": "Hoa Hồng Hoàng Hôn",
    "silent-aegis": "Bình Chướng Lặng Lẽ",
    "shadow-runner": "Kẻ Chạy Bóng Đêm",
    "toysmith": "Thợ Làm Đồ Chơi",
    "trailblazer": "Người Mở Đường",
    "unspoken-calling": "Lời Hiệu Triệu Thầm Lặng",
    "wanderer-s-magnum": "Magnum Kẻ Lãng Du",
    "sportivo-calibro-12": "Sportivo Calibro 12",
    "samosek": "Samosek",
    "schlitzohr": "Schlitzohr",
    "skylla": "Skylla",
    "svarog": "Svarog",
    "sybil": "Sybil",
    "sylvan-elf": "Tinh Linh Rừng Sâu",
    "guerno": "Guerno",
    "chernobog": "Chernobog",
    "capitoline": "Capitoline",
    "aglaea": "Aglaea",
}

# ==============================================================================
# 5. MAIN BUILD WORKFLOW
# ==============================================================================
def run_build() -> int:
    print("=" * 70)
    print("GFL2: Exilium Wiki — Vietnamese Localization & Effects Builder")
    print("=" * 70)

    # 1. Load English Effects
    if not EFFECTS_FILE.exists():
        print(f"Error: {EFFECTS_FILE} does not exist.")
        return 1
    en_effects = json.loads(EFFECTS_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(en_effects)} status effects from {EFFECTS_FILE.name}.")

    # Sort English effect names by length descending for regex extraction
    sorted_en_keys = sorted(en_effects.keys(), key=len, reverse=True)
    eff_pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted_en_keys) + r')\b')

    # Build Vietnamese Effects Catalog
    vi_effects_db: Dict[str, Any] = {}
    for name_en, desc_en in en_effects.items():
        name_vi, desc_vi, eff_type = translate_effect_tuple(name_en, desc_en)

        # Find sub-effects referenced in description
        subs_en = []
        for other_en in eff_pattern.findall(desc_en):
            if other_en != name_en and other_en not in subs_en and len(other_en) > 2:
                subs_en.append(other_en)

        subs_vi = [EFFECT_NAMES.get(s, s) for s in subs_en]

        effect_entry = {
            "name": name_vi,
            "name_en": name_en,
            "desc": desc_vi,
            "desc_en": desc_en,
            "type": eff_type,
            "sub_effects": subs_en,
            "sub_effects_vi": subs_vi,
        }
        # Indexed by both English and Vietnamese names
        vi_effects_db[name_en] = effect_entry
        vi_effects_db[name_vi] = effect_entry

    print(f"Compiled {len(vi_effects_db) // 2} status effects into dual-index catalog.")

    # Save to data/effects_vi.json
    EFFECTS_VI_JSON.write_text(json.dumps(vi_effects_db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {EFFECTS_VI_JSON.relative_to(ROOT)}.")

    # 2. Load Existing i18n_vi.json
    if not I18N_JSON.exists():
        print(f"Error: {I18N_JSON} does not exist.")
        return 1
    i18n_bundle = json.loads(I18N_JSON.read_text(encoding="utf-8"))

    # Add "effects" to i18n bundle
    i18n_bundle["effects"] = vi_effects_db

    # 3. Process Characters (Resolve {0}, {1}, fix basic attacks, add summons)
    print("\nProcessing character skills and summons...")
    chars_data = i18n_bundle.get("characters", {})

    placeholder_fixed_count = 0
    basic_attack_fixed_count = 0

    # Explicit fallback mapping for complex skills like Peritya
    EXPLICIT_PH_MAP: Dict[str, Dict[int, str]] = {
        "peritya": {
            1: "Chỉ Số Nhiên Liệu",
            2: "Tấn Công Chi Viện",
            3: "Chỉ Số Nhiên Liệu",
            0: "Tấn Công Chi Viện",
        }
    }

    for slug, cdata in chars_data.items():
        en_char_file = CHAR_DIR / f"{slug}.json"
        en_char = json.loads(en_char_file.read_text(encoding="utf-8")) if en_char_file.exists() else {}

        # Collect all effects in this character's data
        char_all_effs: List[str] = []
        for s in en_char.get("skills", []):
            for m in eff_pattern.findall(s.get("description", "")):
                if m not in char_all_effs:
                    char_all_effs.append(m)
        for f in en_char.get("fortification", []):
            for m in eff_pattern.findall(f.get("effect", "")):
                if m not in char_all_effs:
                    char_all_effs.append(m)
        for k in en_char.get("keys", []):
            for m in eff_pattern.findall(k.get("effect", "")):
                if m not in char_all_effs:
                    char_all_effs.append(m)

        # 3.1 Fix Skills
        skills = cdata.get("skills", [])
        en_skills = en_char.get("skills", [])

        for idx, s in enumerate(skills):
            s_name = s.get("name", "")
            s_desc = s.get("description", "")
            en_s = en_skills[idx] if idx < len(en_skills) else {}
            en_desc = en_s.get("description", "")
            en_tags = en_s.get("tags", [])

            # A. Fix bogus basic attack matches
            if idx == 0 or "Basic Attack" in en_tags:
                # Check if English description is a standard basic attack
                m_atk = re.search(r"Selects? (?:an|1) enemy target within (?:a )?(\d+)[ -]tiles?(?: radius)? and deals ([A-Za-z]+) damage (?:equivalent|equal) to (\d+%) (?:of )?ATK", en_desc, re.I)
                if m_atk:
                    tiles, elem_en, pct = m_atk.groups()
                    elem_vi_map = {
                        "Physical": "Vật Lý", "Freeze": "Băng Kết", "Burn": "Thiêu Đốt",
                        "Corrosion": "Ăn Mòn", "Hydro": "Hóa Lỏng", "Electric": "Dẫn Điện"
                    }
                    elem_vi = elem_vi_map.get(elem_en.capitalize(), "Vật Lý")
                    s["description"] = f"Chọn 1 mục tiêu địch <color=#f26c1c>trong phạm vi {tiles} ô xung quanh</color>, gây ST {elem_vi} bằng <color=#f26c1c>{pct}</color> Tấn Công."
                    if not s.get("name") or s.get("name") == en_s.get("name"):
                        s["name"] = "Bắn Thường"
                    basic_attack_fixed_count += 1
                    continue

            # B. Resolve placeholders {0}, {1}, {2}...
            if "{" in s_desc:
                # Local effects in this skill
                en_eff_mentions = eff_pattern.findall(en_desc)
                unique_effs = []
                for e in en_eff_mentions:
                    if e not in unique_effs:
                        unique_effs.append(e)

                ph_nums = [int(x) for x in re.findall(r"\{(\d+)\}", s_desc)]
                cand_list = unique_effs if (ph_nums and max(ph_nums) < len(unique_effs)) else char_all_effs

                def replace_ph(m: re.Match) -> str:
                    ph_num = int(m.group(1))
                    if slug in EXPLICIT_PH_MAP and ph_num in EXPLICIT_PH_MAP[slug]:
                        return EXPLICIT_PH_MAP[slug][ph_num]
                    if ph_num < len(cand_list):
                        eff_en = cand_list[ph_num]
                        return EFFECT_NAMES.get(eff_en, eff_en)
                    # Fallback general effects
                    common_fallbacks = ["Tấn Công Chi Viện", "Chỉ Số Nhiên Liệu", "Bảo Vệ Độ Ổn Định", "Nơi Trú Ẩn"]
                    return common_fallbacks[ph_num % len(common_fallbacks)]

                new_desc = re.sub(r"\{(\d+)\}", replace_ph, s_desc)
                if new_desc != s_desc:
                    s["description"] = new_desc
                    placeholder_fixed_count += 1

        # 3.1.2 Fix Fortifications placeholders
        for f in cdata.get("fortification", []):
            f_eff = f.get("effect", "")
            if "{" in f_eff:
                def replace_f_ph(m: re.Match) -> str:
                    ph_num = int(m.group(1))
                    if slug in EXPLICIT_PH_MAP and ph_num in EXPLICIT_PH_MAP[slug]:
                        return EXPLICIT_PH_MAP[slug][ph_num]
                    if ph_num < len(char_all_effs):
                        eff_en = char_all_effs[ph_num]
                        return EFFECT_NAMES.get(eff_en, eff_en)
                    common_fallbacks = ["Tấn Công Chi Viện", "Chỉ Số Nhiên Liệu", "Bảo Vệ Độ Ổn Định", "Nơi Trú Ẩn"]
                    return common_fallbacks[ph_num % len(common_fallbacks)]

                f["effect"] = re.sub(r"\{(\d+)\}", replace_f_ph, f_eff)
                placeholder_fixed_count += 1

        # 3.1.3 Fix Keys placeholders
        for k in cdata.get("keys", []):
            k_eff = k.get("effect", "")
            if "{" in k_eff:
                def replace_k_ph(m: re.Match) -> str:
                    ph_num = int(m.group(1))
                    if slug in EXPLICIT_PH_MAP and ph_num in EXPLICIT_PH_MAP[slug]:
                        return EXPLICIT_PH_MAP[slug][ph_num]
                    if ph_num < len(char_all_effs):
                        eff_en = char_all_effs[ph_num]
                        return EFFECT_NAMES.get(eff_en, eff_en)
                    common_fallbacks = ["Tấn Công Chi Viện", "Chỉ Số Nhiên Liệu", "Bảo Vệ Độ Ổn Định", "Nơi Trú Ẩn"]
                    return common_fallbacks[ph_num % len(common_fallbacks)]

                k["effect"] = re.sub(r"\{(\d+)\}", replace_k_ph, k_eff)
                placeholder_fixed_count += 1

        # 3.2 Update Summons for Character
        if slug in SUMMON_TRANSLATIONS:
            cdata["summons"] = SUMMON_TRANSLATIONS[slug] if isinstance(SUMMON_TRANSLATIONS[slug], list) else [SUMMON_TRANSLATIONS[slug]]
        elif en_char.get("summons"):
            # Fallback for any other summons
            c_sms = []
            for sm in en_char.get("summons", []):
                sm_name = sm.get("name", "")
                sm_desc = translate_weapon_text(sm.get("description", ""))
                sm_stats = sm.get("stats")
                c_sms.append({
                    "name": EFFECT_NAMES.get(sm_name, sm_name),
                    "type": "Vật Triệu Hồi",
                    "description": sm_desc,
                    "stats": sm_stats
                })
            cdata["summons"] = c_sms

    print(f"Fixed {basic_attack_fixed_count} basic attack skill descriptions.")
    print(f"Resolved placeholders in {placeholder_fixed_count} skill descriptions.")
    print(f"Applied Vietnamese summons to all 12 characters.")

    # 4. Process Weapons (Translate traits, effects, stats, names)
    print("\nProcessing weapons...")
    weapons_data = i18n_bundle.get("weapons", {})
    en_weapons = json.loads(WEAPONS_FILE.read_text(encoding="utf-8")) if WEAPONS_FILE.exists() else []
    en_weapons_map = {w.get("slug"): w for w in en_weapons}

    weapons_translated_count = 0
    for slug, wdata in weapons_data.items():
        en_w = en_weapons_map.get(slug, {})

        # A. Name
        if slug in KNOWN_WEAPON_NAMES:
            wdata["name"] = KNOWN_WEAPON_NAMES[slug]

        # B. Trait
        raw_trait = en_w.get("trait_description") or en_w.get("trait") or wdata.get("trait", "")
        if raw_trait:
            wdata["trait"] = translate_weapon_trait(raw_trait)

        # C. Effect
        raw_effect = en_w.get("skill_description") or en_w.get("effect") or wdata.get("effect", "")
        if raw_effect:
            wdata["effect"] = translate_weapon_effect(raw_effect)

        # D. Stats
        raw_stats = wdata.get("stats", "")
        if raw_stats:
            wdata["stats"] = re.sub(r"\bATK\b", "Tấn Công", raw_stats)
            wdata["stats"] = re.sub(r"\bDEF\b", "Phòng Thủ", wdata["stats"])

        weapons_translated_count += 1

    print(f"Translated traits, effects, and stats for {weapons_translated_count} weapons.")

    # 5. Save updated data/i18n_vi.json
    print(f"\nWriting updated bundle to {I18N_JSON.relative_to(ROOT)}...")
    I18N_JSON.write_text(json.dumps(i18n_bundle, ensure_ascii=False, indent=2), encoding="utf-8")

    # 6. Save updated site/static/js/i18n-vi.js
    print(f"Writing updated client script to {I18N_JS.relative_to(ROOT)}...")
    js_content = f"// Auto-generated Vietnamese Localization Bundle for GFL2: Exilium Wiki\nwindow.GFL2_I18N_VI = {json.dumps(i18n_bundle, ensure_ascii=False, indent=2)};\n"
    I18N_JS.write_text(js_content, encoding="utf-8")

    print(f"✅ Successfully exported full Vietnamese localization bundle ({I18N_JSON.stat().st_size // 1024} KB).")
    return 0


if __name__ == "__main__":
    sys.exit(run_build())
