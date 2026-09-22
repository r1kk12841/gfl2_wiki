(function exposeGuideTemplate(root) {
  'use strict';

  const heading = (text) => ({ type: 'heading', level: 2, text });
  const paragraph = (html = '') => ({ type: 'paragraph', html });
  const table = (headers, rowCount) => ({
    type: 'table',
    headers,
    rows: Array.from({ length: rowCount }, () => headers.map(() => '')),
  });

  function createLoreleyStyleGuide({ slug, name, date, author = 'Community' }) {
    if (!slug) throw new Error('Thiếu slug nhân vật.');
    const characterName = name || slug;
    const lastUpdated = date || new Date().toISOString().slice(0, 10);

    return {
      slug,
      title: `Hướng dẫn toàn diện ${characterName}: Lối chơi, Trang bị & Đội hình`,
      char_slug: slug,
      last_updated: lastUpdated,
      author,
      blocks: [
        heading('Tổng quan (Overview)'),
        { type: 'char_card', slug },
        paragraph(`<b>${characterName}</b> — tóm tắt vai trò, thuộc tính, loại đạn và điểm mạnh chính.`),
        paragraph('<b>Các cơ chế chiến đấu cốt lõi:</b><br>• Cơ chế 1<br>• Cơ chế 2<br>• Cơ chế 3'),

        heading('Đột phá & Cung mệnh (Fortifications)'),
        paragraph('Khuyến nghị mốc dừng V0/V1/V2 và lý do.'),
        table(['Cấp độ', 'Chi tiết hiệu ứng', 'Đánh giá & Khuyến nghị'], 7),

        heading('Trang bị Vũ khí (Weapons)'),
        paragraph('Tóm tắt thứ tự ưu tiên vũ khí và điều kiện sử dụng.'),
        table(['Vũ khí', 'Độ hiếm', 'Phân tích & Hiệu quả'], 4),

        heading('Phụ kiện & Chỉ số (Attachments)'),
        paragraph('<b>Thứ tự ưu tiên dòng phụ:</b> …<br><b>Chỉ số mục tiêu:</b> …'),
        table(['Bộ phụ kiện', 'Hiệu ứng set', 'Ghi chú'], 2),

        heading('Khóa Cố Định (Fixed Keys)'),
        paragraph('Tóm tắt mục tiêu của thiết lập Neural Helix.'),
        table(['Khóa', 'Tên Khóa', 'Hiệu ứng', 'Vai trò'], 5),

        heading('Khóa Chung & Khóa Hảo Cảm (Common & Affinity Keys)'),
        paragraph('• <b>Khóa Chung:</b> …<br>• <b>Khóa Hảo Cảm:</b> …'),

        heading('Dữ liệu Tái Cấu Trúc & Lõi Tăng Trưởng (Remolding Core)'),
        paragraph('<b>Chỉ số chính 6 vị trí hoa:</b><br>• …'),
        paragraph('<b>Ưu tiên dòng phụ:</b> …'),

        heading('Chu kỳ Kỹ năng (Rotation)'),
        paragraph('<b>Lưu ý thứ tự hành động:</b> …'),
        table(['Mốc Đột Phá', 'Vòng lặp kỹ năng (Rotation)', 'Chi tiết vận hành'], 2),

        heading('Đội hình đề xuất (Team Compositions)'),
        paragraph('<b>1. Đội hình đề xuất:</b><br>• <b>Đội hình:</b> …<br>• <i>Đặc điểm:</i> …'),
        paragraph('<b>2. Đội hình thay thế:</b><br>• <b>Đội hình:</b> …<br>• <i>Đặc điểm:</i> …'),
        paragraph('<b>3. Đội hình linh hoạt:</b><br>• <b>Đội hình:</b> …<br>• <i>Đặc điểm:</i> …'),

        heading('Tổng kết & Lời khuyên Gacha (Verdict)'),
        paragraph('• <b>Có nên roll không?:</b> …<br>• <b>F2P / Thẻ tháng:</b> …<br>• <b>Meta Player:</b> …'),
      ],
    };
  }

  const api = { createLoreleyStyleGuide };
  root.GuideTemplate = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : window);
