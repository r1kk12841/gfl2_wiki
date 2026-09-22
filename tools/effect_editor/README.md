# Effect Editor

Tool cục bộ để sửa bản dịch hiệu ứng tiếng Việt.

```bash
.venv\Scripts\python.exe tools/start_editors.py
```

Mở `http://127.0.0.1:8000/tools/effect_editor/index.html`.

Không dùng `python -m http.server`: static server không cung cấp API lưu dữ liệu.

Khi lưu, tool cập nhật đồng thời qua giao dịch nguyên tử (`RepositoryTransaction`):

- `data/effects_vi.json`
- mục `effects` trong `data/i18n_vi.json`
- `site/static/js/i18n-vi.js`
- Quản lý hiệu ứng con: Hỗ trợ thêm hiệu ứng con mới qua nút "+ Thêm hiệu ứng con" và gỡ bỏ bằng nút `×` trên chip.
- Quan hệ `sub_effect_ids` và `referenced_by` được tự động tính toán và bảo toàn bằng ID ổn định.

Catalog dùng khóa `effect_<sha1>` ổn định. API cập nhật theo ID:

```text
PUT /api/effects/effect_0123456789ab
```

Chạy kiểm tra sau khi chỉnh nhiều hiệu ứng:

```bash
python tools/validate.py
python site/build.py
pytest tests/test_effect_editor.py tests/test_build.py tests/test_i18n.py
```
