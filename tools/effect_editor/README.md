# Effect Editor

Tool cục bộ để sửa bản dịch hiệu ứng tiếng Việt.

```bash
python tools/data_entry_server.py
```

Mở `http://127.0.0.1:8000/tools/effect_editor/`.

Không dùng `python -m http.server`: static server không cung cấp API lưu dữ liệu.

Server riêng vẫn dùng được qua `python tools/effect_editor/server.py` tại cổng `8765`.

Khi lưu, tool cập nhật đồng thời:

- `data/effects_vi.json`
- mục `effects` trong `data/i18n_vi.json`
- `site/static/js/i18n-vi.js`
- quan hệ `sub_effect_ids` vẫn giữ nguyên khi đổi tên, kể cả khi nhiều hiệu ứng trùng tên

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
