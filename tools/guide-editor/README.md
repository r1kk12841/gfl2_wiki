# Guide Editor

Công cụ soạn thảo cẩm nang và hướng dẫn chiến thuật cho các nhân vật trong Girls' Frontline 2: Exilium.

## Khởi động

Khởi động qua Unified Editor Server:

```bash
.venv\Scripts\python.exe tools/start_editors.py
```

Truy cập: `http://127.0.0.1:8000/tools/guide-editor/index.html`.

## Các chức năng chính

1. **Soạn thảo dạng khối (Block-based)**:
   - Chọn nhân vật rồi dùng **Mở guide nhân vật** để nạp trực tiếp `data/guides/{slug}.json`.
   - Dùng **Tạo theo mẫu Loreley** để tạo sẵn bố cục Tổng quan, Đột phá, Vũ khí, Phụ kiện, Khóa, Rotation, Đội hình và Verdict.
   - Nhân đôi khối bằng nút `⧉`; ô bảng hỗ trợ văn bản nhiều dòng.
   - Paragraph và ô Table là vùng WYSIWYG: nhập, chọn và định dạng trực tiếp như Word.
   - **Quick Format** hỗ trợ hoàn tác/làm lại, cỡ chữ, đậm, nghiêng, gạch dưới, màu chữ, highlight, căn lề, danh sách, link và xóa định dạng.
   - Phím tắt: `Ctrl+B`, `Ctrl+I`, `Ctrl+U`, `Ctrl+Z`, `Ctrl+Y`.
   - Dán từ Word/Google Docs được làm sạch về HTML an toàn trước khi lưu.
   - Kéo tay nắm bên trái để đổi vị trí mọi block, gồm ảnh và bảng.
   - Chỉnh trực tiếp tiêu đề, tác giả và ngày cập nhật.
   - Thêm tiêu đề Section (H2), Sub-section (H3).
   - Thêm đoạn văn bản (hỗ trợ HTML: `<strong>`, `<em>`, `<a>`).
   - Nhúng thẻ nhân vật (Char Card), thẻ vũ khí (Weapon Card).
   - Nhúng kỹ năng tham chiếu (Skill Ref) và kỹ năng triệu hồi (Summon Skill Ref).
   - Chèn bảng số liệu (Table) và liên kết ngoài (Link).
2. **Lưu & Xuất bản**:
   - **Cập nhật JSON gốc**: Gửi trực tiếp tới API server để lưu vào `data/guides/{slug}.json` qua giao dịch nguyên tử `RepositoryTransaction`.
   - **Tải tệp JSON**: Tải tệp JSON về máy tính cho nhu cầu sao lưu hoặc sử dụng offline.
   - **Mở tệp JSON**: Nạp nội dung từ tệp JSON có sẵn trên máy để tiếp tục chỉnh sửa.
3. **An toàn kết nối (Server Gate)**:
   - Tự động nhận diện nếu mở nhầm qua static server (`python -m http.server`) và hiển thị hướng dẫn khắc phục.
