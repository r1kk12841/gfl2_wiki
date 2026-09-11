// ============================================================
//  GFL2 Wiki — Data Entry Tool Internationalization (i18n.js)
// ============================================================

'use strict';

const DATA_ENTRY_I18N = {
  en: {
    // Header & Navigation
    app_title: 'GFL2: Exilium Wiki',
    app_subtitle: 'Data Entry Tool',
    tab_character: 'Character',
    tab_weapon: 'Weapon',
    tab_faq: 'FAQ',
    tab_guide_editor: '✍ Guide Editor ↗',
    switch_lang_title: 'Switch Language / Chuyển Ngôn Ngữ',

    // Character selector bar
    load_existing: '📋 Load existing:',
    select_char_placeholder: '— Select a character —',
    btn_load: 'Load →',
    or: 'or',
    btn_clear_char: '✕ New / Clear',

    // Action buttons
    btn_save_disk: '💾 Update source JSON',
    btn_download_json: '⬇ Download JSON',
    btn_load_json: '📂 Load JSON',
    btn_excel_autofill: '✨ Auto-fill from Excel',
    btn_save_i18n_vi: '💾 Update i18n_vi.json',
    btn_download_i18n_vi: '⬇ Download i18n_vi.json',

    // Section 1: Basic Info
    sec_basic_title: 'Basic Info',
    field_name: 'Name',
    field_slug: 'Slug',
    field_class: 'Class',
    field_rarity: 'Rarity',
    field_phase: 'Phase',
    field_weapon_type: 'Weapon Type',
    field_ammo_type: 'Ammo Type',
    field_sig_weapon: 'Signature Weapon (slug)',
    field_skill_attr: 'Skill Attribute',
    field_weakness: 'Weakness',
    field_hp: 'HP',
    field_atk: 'ATK',
    field_def: 'DEF',
    field_stab_gauge: 'Stability Gauge',
    field_move_speed: 'Movement Speed',
    placeholder_select: '— select —',
    placeholder_name: 'e.g. Groza',
    placeholder_slug: 'auto-generated',
    placeholder_sig_weapon: 'e.g. ots-14',
    placeholder_optional: 'optional',
    placeholder_stab_gauge: 'e.g. 10 points',
    placeholder_move_speed: 'e.g. 6 tiles',

    // Section 2: Effects Glossary
    sec_glossary_title: 'Effects Glossary',
    sec_glossary_desc: "Status effects referenced on this character's tab. One entry per effect.",
    btn_add_glossary: '+ Add Status Effect',

    // Section 3: Skills
    sec_skills_title: 'Skills',
    btn_add_skill: '+ Add Skill',
    skill_name: 'Skill Name',
    skill_tags: 'Tags',
    skill_ammo_type: 'Ammo Type',
    skill_stab_dmg: 'Stability Damage',
    skill_cooldown: 'Cooldown',
    skill_confectance: 'Confectance Cost',
    skill_range: 'Range',
    skill_effect_area: 'Effect Area',
    skill_desc: 'Description',
    skill_icon: 'Icon Path',
    skill_range_img: 'Range Image Path',
    placeholder_skill_name: 'Skill name',
    placeholder_skill_cd: 'e.g. 0 turns',
    placeholder_skill_cost: 'e.g. 1',
    placeholder_skill_range: 'e.g. 6',
    placeholder_skill_area: 'e.g. Target',
    placeholder_skill_desc: 'Skill description…',

    // Section 4: Summon Units
    sec_summons_title: 'Summon Units',
    sec_summons_desc: 'For units with separate stats and skills (e.g. drones, turrets).',
    btn_add_summon: '+ Add Summon Unit',
    summon_name: 'Summon Name',
    btn_add_summon_skill: '+ Add Summon Skill',

    // Section 5: Fortification
    sec_fort_title: 'Fortification (Vertebrae Upgrade)',
    sec_fort_desc: 'Transcribe from the Vertebrae Upgrade summary table at the bottom of the character tab (6 rows).',
    tier_label: 'Tier',
    target_skill_label: 'Target Skill',
    req_level_label: 'Required Level',
    effect_label: 'Effect',
    placeholder_fort_effect: 'Vertebrae Upgrade effect description…',

    // Section 6: Neural Helix
    sec_nh_title: 'Neural Helix — Enhancement Nodes',
    sec_nh_desc: 'Flat stat-boost nodes (Enhancement 1–6) unlocked at set character levels.',
    node_name_label: 'Node Name',
    placeholder_nh_effect: 'e.g. ATK +35\nDEF +21',
    placeholder_nh_materials: 'materials',

    // Section 7: Keys
    sec_keys_title: 'Neural Helix — Keys',
    sec_keys_desc: 'Fixed Keys 1–6, Affinity Key, Common Key, Expansion Key.',
    key_name_label: 'Key Name',
    placeholder_key_effect: 'Key effect description…',
    placeholder_key_materials: 'materials',

    // Section 8: Images
    sec_images_title: 'Images',
    sec_images_desc: 'Expected asset paths (auto-update from slug). Use the file pickers below to upload images to the correct folders.',
    img_portrait: 'Portrait',
    img_class_icon: 'Class Icon',
    upload_section_title: 'Upload Images to Assets',
    upload_section_subtitle: '(Files are saved locally via browser picker)',
    btn_add_img_slot: '+ Add Image Slot',
    btn_pick_img: 'Pick File…',
    btn_save_img: 'Save',
    btn_remove_img: '✕ Remove',

    // Section 9: Source Notes
    sec_notes_title: 'Source Notes',
    field_source_notes: 'Free notes (flags, irregularities, rework info…)',
    placeholder_source_notes: 'e.g. pre-rework kit — see Jiangyu(old)',

    // Weapon Tab
    btn_download_weapon: '⬇ Download JSON',
    btn_load_weapon: '📂 Load JSON',
    btn_clear_weapon: '✕ Clear',
    sec_weapon_title: 'Weapon Info',
    field_weapon_trait: 'Trait Name',
    field_weapon_trait_desc: 'Trait Description',
    field_weapon_effect: 'Inscript / Weapon Effect',
    img_weapon: 'Weapon Image',

    // FAQ Tab
    btn_download_faq: '⬇ Download faq.json',
    btn_load_faq: '📂 Load faq.json',
    btn_clear_faq: '✕ Clear',
    sec_faq_title: 'FAQ Entries',
    btn_add_faq: '+ Add Q&A',
    field_faq_q: 'Question',
    field_faq_a: 'Answer',

    // Preview Pane
    preview_title: 'JSON Preview',
    preview_status: 'live',

    // Toasts
    toast_saved: 'Saved',
    toast_downloaded: 'Downloaded',
    toast_loaded: 'Loaded',
    toast_cleared: 'Form cleared',
    toast_slug_req: 'Slug is required',
    toast_name_req: 'Name is required',
    toast_switched_en: 'Switched to English mode',
    toast_switched_vi: 'Đã chuyển sang chế độ Tiếng Việt',
    toast_i18n_updated: 'Updated in-memory i18n_vi.json'
  },

  vi: {
    // Header & Navigation
    app_title: 'GFL2: Exilium Wiki',
    app_subtitle: 'Công Cụ Nhập Dữ Liệu',
    tab_character: 'Nhân Vật',
    tab_weapon: 'Vũ Khí',
    tab_faq: 'Hỏi Đáp',
    tab_guide_editor: '✍ Soạn Thảo Hướng Dẫn ↗',
    switch_lang_title: 'Chuyển Ngôn Ngữ / Switch Language',

    // Character selector bar
    load_existing: '📋 Tải nhân vật có sẵn:',
    select_char_placeholder: '— Chọn một nhân vật —',
    btn_load: 'Tải →',
    or: 'hoặc',
    btn_clear_char: '✕ Tạo mới / Xóa trắng',

    // Action buttons
    btn_save_disk: '💾 Cập nhật JSON gốc',
    btn_download_json: '⬇ Tải tệp JSON',
    btn_load_json: '📂 Mở tệp JSON',
    btn_excel_autofill: '✨ Tự động điền từ Excel',
    btn_save_i18n_vi: '💾 Cập nhật i18n_vi.json',
    btn_download_i18n_vi: '⬇ Tải i18n_vi.json',

    // Section 1: Basic Info
    sec_basic_title: 'Thông Tin Cơ Bản',
    field_name: 'Tên Nhân Vật',
    field_slug: 'Mã định danh (Slug)',
    field_class: 'Lớp Tác Chiến',
    field_rarity: 'Độ Hiếm',
    field_phase: 'Thuộc Tính',
    field_weapon_type: 'Loại Vũ Khí',
    field_ammo_type: 'Loại Đạn',
    field_sig_weapon: 'Vũ Khí Đặc Trưng (slug)',
    field_skill_attr: 'Thuộc Tính Kỹ Năng',
    field_weakness: 'Điểm Yếu',
    field_hp: 'HP',
    field_atk: 'Tấn Công (ATK)',
    field_def: 'Phòng Thủ (DEF)',
    field_stab_gauge: 'Độ Ổn Định',
    field_move_speed: 'Khoảng Cách Di Chuyển',
    placeholder_select: '— chọn —',
    placeholder_name: 'vd: Groza',
    placeholder_slug: 'tự động tạo',
    placeholder_sig_weapon: 'vd: ots-14',
    placeholder_optional: 'tùy chọn',
    placeholder_stab_gauge: 'vd: 10 điểm',
    placeholder_move_speed: 'vd: 6 ô',

    // Section 2: Effects Glossary
    sec_glossary_title: 'Thuật Ngữ Hiệu Ứng',
    sec_glossary_desc: 'Các hiệu ứng trạng thái được tham chiếu trên trang nhân vật này.',
    btn_add_glossary: '+ Thêm Hiệu Ứng',

    // Section 3: Skills
    sec_skills_title: 'Kỹ Năng & Năng Lực',
    btn_add_skill: '+ Thêm Kỹ Năng',
    skill_name: 'Tên Kỹ Năng',
    skill_tags: 'Thẻ Kỹ Năng',
    skill_ammo_type: 'Loại Đạn Tiêu Hao',
    skill_stab_dmg: 'Sát Thương Ổn Định',
    skill_cooldown: 'Thời Gian Hồi',
    skill_confectance: 'Điểm Nhiên Liệu',
    skill_range: 'Phạm Vi',
    skill_effect_area: 'Vùng Hiệu Lực',
    skill_desc: 'Mô Tả Kỹ Năng',
    skill_icon: 'Đường dẫn Icon',
    skill_range_img: 'Đường dẫn Ảnh Phạm Vi',
    placeholder_skill_name: 'Tên kỹ năng',
    placeholder_skill_cd: 'vd: 0 hiệp',
    placeholder_skill_cost: 'vd: 1',
    placeholder_skill_range: 'vd: 6',
    placeholder_skill_area: 'vd: Mục Tiêu',
    placeholder_skill_desc: 'Mô tả chi tiết kỹ năng…',

    // Section 4: Summon Units
    sec_summons_title: 'Vật Thể Triệu Hồi',
    sec_summons_desc: 'Dành cho các đơn vị có chỉ số và kỹ năng riêng biệt (vd: drone, ụ súng).',
    btn_add_summon: '+ Thêm Vật Thể Triệu Hồi',
    summon_name: 'Tên Vật Thể',
    btn_add_summon_skill: '+ Thêm Kỹ Năng Triệu Hồi',

    // Section 5: Fortification
    sec_fort_title: 'Cường Hóa Tâm Trí (Mảnh Xương)',
    sec_fort_desc: 'Trích từ bảng nâng cấp Đốt Sống ở cuối tab nhân vật (6 tầng).',
    tier_label: 'Tầng',
    target_skill_label: 'Kỹ Năng Cường Hóa',
    req_level_label: 'Cấp Yêu Cầu',
    effect_label: 'Hiệu Ứng Nâng Cấp',
    placeholder_fort_effect: 'Mô tả hiệu ứng cường hóa tâm trí…',

    // Section 6: Neural Helix
    sec_nh_title: 'Mạch Tâm Trí — Mắt Cường Hóa',
    sec_nh_desc: 'Các mắt tăng chỉ số cơ bản (Cường Hóa 1–6) mở khóa theo cấp nhân vật.',
    node_name_label: 'Tên Mắt Mạch',
    placeholder_nh_effect: 'vd: Tấn Công +35\nPhòng Thủ +21',
    placeholder_nh_materials: 'nguyên liệu',

    // Section 7: Keys
    sec_keys_title: 'Mạch Tâm Trí — Chìa Khóa',
    sec_keys_desc: 'Khóa Cố Định 1–6, Khóa Độ Thân Thiết, Khóa Thường, Khóa Mở Rộng.',
    key_name_label: 'Tên Khóa',
    placeholder_key_effect: 'Mô tả hiệu ứng khóa tâm trí…',
    placeholder_key_materials: 'nguyên liệu',

    // Section 8: Images
    sec_images_title: 'Hình Ảnh & Tài Nguyên',
    sec_images_desc: 'Đường dẫn tài nguyên dự kiến. Sử dụng công cụ bên dưới để chọn và lưu ảnh vào thư mục tương ứng.',
    img_portrait: 'Ảnh Chân Dung',
    img_class_icon: 'Icon Lớp',
    upload_section_title: 'Tải Lên Hình Ảnh Vào Thư Mục Assets',
    upload_section_subtitle: '(Tệp được lưu cục bộ qua trình chọn tệp của trình duyệt)',
    btn_add_img_slot: '+ Thêm Vị Trí Ảnh',
    btn_pick_img: 'Chọn Tệp…',
    btn_save_img: 'Lưu',
    btn_remove_img: '✕ Xóa',

    // Section 9: Source Notes
    sec_notes_title: 'Ghi Chú Nguồn',
    field_source_notes: 'Ghi chú tự do (bản làm lại, lưu ý phiên bản…)',
    placeholder_source_notes: 'vd: bộ kỹ năng trước khi làm lại — xem Jiangyu(cũ)',

    // Weapon Tab
    btn_download_weapon: '⬇ Tải Tệp JSON',
    btn_load_weapon: '📂 Mở Tệp JSON',
    btn_clear_weapon: '✕ Xóa Trắng',
    sec_weapon_title: 'Thông Tin Vũ Khí',
    field_weapon_trait: 'Tên Đặc Tính',
    field_weapon_trait_desc: 'Mô Tả Đặc Tính',
    field_weapon_effect: 'Hiệu Ứng Khắc Ấn / Bị Động',
    img_weapon: 'Ảnh Vũ Khí',

    // FAQ Tab
    btn_download_faq: '⬇ Tải tệp faq.json',
    btn_load_faq: '📂 Mở tệp faq.json',
    btn_clear_faq: '✕ Xóa Trắng',
    sec_faq_title: 'Nội Dung Hỏi Đáp (FAQ)',
    btn_add_faq: '+ Thêm Câu Hỏi & Trả Lời',
    field_faq_q: 'Câu Hỏi',
    field_faq_a: 'Câu Trả Lời',

    // Preview Pane
    preview_title: 'Xem Trước JSON',
    preview_status: 'trực tiếp',

    // Toasts
    toast_saved: 'Đã lưu',
    toast_downloaded: 'Đã tải về',
    toast_loaded: 'Đã tải thành công',
    toast_cleared: 'Đã xóa trắng biểu mẫu',
    toast_slug_req: 'Mã định danh (slug) là bắt buộc',
    toast_name_req: 'Tên là bắt buộc',
    toast_switched_en: 'Đã chuyển sang tiếng Anh',
    toast_switched_vi: 'Đã chuyển sang chế độ Tiếng Việt',
    toast_i18n_updated: 'Đã cập nhật dữ liệu i18n_vi.json trong bộ nhớ'
  }
};

// ── Bi-directional Terminology Maps ──────────────────────────────────────────
const TERMS = {
  classes: [
    { en: 'Bulwark', vi: 'Hộ Vệ' },
    { en: 'Vanguard', vi: 'Tiên Phong' },
    { en: 'Support', vi: 'Hỗ Trợ' },
    { en: 'Sentinel', vi: 'Vệ Binh' }
  ],
  rarities: [
    { en: 'Elite', vi: 'Tinh Nhuệ' },
    { en: 'Standard', vi: 'Tiêu Chuẩn' }
  ],
  rarities_weapon: [
    { en: 'SSR', vi: 'SSR' },
    { en: 'SR', vi: 'SR' },
    { en: 'R', vi: 'R' }
  ],
  phases: [
    { en: 'Physical', vi: 'Vật Lý' },
    { en: 'Burn', vi: 'Thiêu Đốt' },
    { en: 'Hydro', vi: 'Hóa Lỏng' },
    { en: 'Electric', vi: 'Dẫn Điện' },
    { en: 'Freeze', vi: 'Băng Kết' },
    { en: 'Corrosion', vi: 'Ăn Mòn' },
    { en: 'Resonance', vi: 'Cộng Hưởng' }
  ],
  weapon_types: [
    { en: 'Assault Rifle', vi: 'Súng Trường' },
    { en: 'SMG', vi: 'Súng Tiểu Liên' },
    { en: 'Shotgun', vi: 'Súng Shotgun' },
    { en: 'MG', vi: 'Súng Máy' },
    { en: 'Sniper Rifle', vi: 'Súng Bắn Tỉa' },
    { en: 'Handgun', vi: 'Súng Lục' },
    { en: 'Blade', vi: 'Lưỡi Đao' }
  ],
  ammo_types: [
    { en: 'Light Ammo', vi: 'Đạn Nhẹ' },
    { en: 'Medium Ammo', vi: 'Đạn Vừa' },
    { en: 'Heavy Ammo', vi: 'Đạn Nặng' },
    { en: 'Shotgun Ammo', vi: 'Súng Shotgun' },
    { en: 'Melee', vi: 'Cận Chiến' }
  ],
  tags: [
    { en: 'Basic Attack', vi: 'Đánh Thường' },
    { en: 'Active', vi: 'Chủ Động' },
    { en: 'Passive', vi: 'Bị Động' },
    { en: 'Buff', vi: 'Cường Hóa' },
    { en: 'Debuff', vi: 'Suy Yếu' },
    { en: 'Targeted', vi: 'Chỉ Định' },
    { en: 'AoE', vi: 'Phạm Vi' },
    { en: 'Healing', vi: 'Trị Liệu' },
    { en: 'Shield', vi: 'Tạo Khiên' }
  ],
  keys: [
    { en: 'Fixed Key 1', vi: 'Khóa Cố Định 1' },
    { en: 'Fixed Key 2', vi: 'Khóa Cố Định 2' },
    { en: 'Fixed Key 3', vi: 'Khóa Cố Định 3' },
    { en: 'Fixed Key 4', vi: 'Khóa Cố Định 4' },
    { en: 'Fixed Key 5', vi: 'Khóa Cố Định 5' },
    { en: 'Fixed Key 6', vi: 'Khóa Cố Định 6' },
    { en: 'Affinity Key', vi: 'Khóa Độ Thân Thiết' },
    { en: 'Common Key', vi: 'Khóa Thường' },
    { en: 'Expansion Key', vi: 'Khóa Mở Rộng' }
  ]
};

// Map a term between English and Vietnamese
function mapTerm(term, category, targetLang) {
  if (!term || !TERMS[category]) return term;
  const match = TERMS[category].find(t => t.en.toLowerCase() === term.toLowerCase() || t.vi.toLowerCase() === term.toLowerCase());
  if (!match) return term;
  return targetLang === 'vi' ? match.vi : match.en;
}

// Get list of terms in requested language
function getTermList(category, lang) {
  if (!TERMS[category]) return [];
  return TERMS[category].map(t => lang === 'vi' ? t.vi : t.en);
}

// Helper: translation lookup with fallback
function t(key, lang = 'en') {
  const dict = DATA_ENTRY_I18N[lang] || DATA_ENTRY_I18N.en;
  return dict[key] || DATA_ENTRY_I18N.en[key] || key;
}

window.DATA_ENTRY_I18N = DATA_ENTRY_I18N;
window.TERMS = TERMS;
window.mapTerm = mapTerm;
window.getTermList = getTermList;
window.t = t;
