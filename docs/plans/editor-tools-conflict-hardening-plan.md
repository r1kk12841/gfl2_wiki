# Kế hoạch rà soát và chống xung đột cho toàn bộ editor tools

> Tài liệu thực thi cho Gemini. Đây chỉ là kế hoạch; không triển khai trong bước này.

## 1. Mục tiêu

Đưa Data Entry, Effect Editor và Guide Editor về một mô hình chạy thống nhất, có thể phát hiện nhầm static server trước khi đọc/ghi dữ liệu, không mất cập nhật khi hai công cụ cùng sửa các file dùng chung, và có kiểm thử trình duyệt cho các luồng chính.

Kết quả bắt buộc:

- Một lệnh khởi động chính thức cho cả ba editor.
- Mọi URL do launcher in/mở phải dùng `127.0.0.1`, không trộn với `localhost`.
- Effect Editor không được gọi API nếu server hiện tại không phải editor server.
- Các thao tác cùng ghi `data/i18n_vi.json` và `site/static/js/i18n-vi.js` phải tuần tự, nguyên tử và không ghi đè thay đổi của nhau.
- Không thay đổi schema dữ liệu nhân vật, vũ khí, hiệu ứng hoặc guide ngoài phần thật sự cần cho cơ chế lưu.
- Không tự động dừng/kill tiến trình đang chiếm cổng.

## 2. Bằng chứng và nguyên nhân hiện tại

### 2.1 Lỗi đang tái hiện

Ngày kiểm tra: 2026-09-11.

```text
http://localhost:8000/api/effects  -> 404 File not found
http://127.0.0.1:8000/api/effects -> 200 application/json
```

`netstat -ano` cho thấy đồng thời hai listener:

```text
0.0.0.0:8000   LISTENING PID 13280
[::]:8000      LISTENING PID 13280
127.0.0.1:8000 LISTENING PID 12008
```

Trình duyệt mở `localhost:8000`, đi vào static server PID 13280 nên `/api/effects` trả 404. Editor server PID 12008 vẫn hoạt động nhưng chỉ ở `127.0.0.1:8000`.

### 2.2 Điểm dễ xung đột trong mã nguồn

| Khu vực | Hiện trạng | Rủi ro |
|---|---|---|
| `tools/data_entry_server.py` | Có API character + effect, bind mặc định `127.0.0.1:8000` | README lại hướng dẫn `localhost`; Windows có thể cho hai listener theo địa chỉ khác nhau |
| `tools/effect_editor/server.py` | Có một bản handler effect API riêng, mặc định cổng 8765 | Hai implementation API dễ lệch hành vi/validation |
| `tools/effect_editor/app.js` | Gọi trực tiếp `/api/effects`, parse JSON ngay | Khi chạy trên static server chỉ hiện lỗi 404/JSON mơ hồ; không nhận biết sai server |
| `tools/data-entry/app.js` | Gọi `/api/characters/...`; đọc nhiều JSON tĩnh | Có cùng nguy cơ chạy đúng UI trên sai server; phụ thuộc CDN SheetJS |
| `tools/guide-editor/app.js` | Đọc dữ liệu tĩnh, lưu bằng File System Access/download | Không cùng quy tắc cập nhật source; có thể lưu nhầm vị trí hoặc ghi đè thủ công |
| `DataEntryStore` và `EffectStore` | Có staging + `os.replace`; unified handler có lock nội bộ tiến trình | Standalone server và CLI khác không dùng chung lock; hai thao tác đều sửa i18n bundle |
| Các CLI `sync_lang_bytes.py`, `extract_vietnamese.py`, `build_vietnamese_effects.py`, `migrate_effect_ids.py`, `tag_server_data.py` | Ghi trực tiếp các file nguồn/derived | Chạy cùng editor có thể gây lost update hoặc bundle JSON/JS lệch nhau |
| Tài liệu | `README.md` dùng `localhost`; Effect Editor README dùng `127.0.0.1` | Người dùng có thể mở hai origin khác nhau và gặp đúng lỗi hiện tại |

## 3. Nguyên tắc kiến trúc đích

1. **Một server chính thức**: chỉ một implementation định tuyến API và static files.
2. **Một origin chính thức**: `http://127.0.0.1:<port>`.
3. **Nhận diện server trước khi dùng API**: mọi editor gọi `/api/health` khi boot.
4. **Một cổng ghi dữ liệu**: các editor và CLI dùng chung transaction/lock helper.
5. **Một nguồn sinh bundle**: JS tiếng Việt luôn được render từ `data/i18n_vi.json` bằng cùng một hàm.
6. **Thất bại rõ ràng**: sai server phải hiện banner có lệnh sửa, không tiếp tục fetch/lưu.
7. **Tương thích ngược có kiểm soát**: lệnh cũ còn chạy qua wrapper, nhưng không duy trì handler thứ hai.

## 4. Thiết kế cụ thể

### 4.1 Server và launcher thống nhất

Tạo:

- `tools/editor_server.py`: server chính thức, sở hữu toàn bộ route.
- `tools/editor_core/transaction.py`: lock + atomic multi-file transaction.
- `tools/editor_core/bundle.py`: đọc/ghi JSON và render `i18n-vi.js`.
- `tools/start_editors.py`: preflight cổng, chạy server, mở tool hub.
- `tools/index.html`: hub chứa link tới ba editor và trạng thái API.

Giữ tương thích:

- `tools/data_entry_server.py` chỉ import và gọi `tools.editor_server.main`; không còn định nghĩa handler/store riêng.
- `tools/effect_editor/server.py` chỉ là wrapper gọi server chung với cổng mặc định 8765 hoặc in cảnh báo deprecation; tuyệt đối không giữ bản sao route effect.

Launcher phải:

1. Probe `http://127.0.0.1:<port>/api/health`.
2. Nếu nhận đúng service/version, không tạo server thứ hai; chỉ mở hub hiện hữu.
3. Nếu cổng bị chiếm nhưng health không đúng, thoát mã khác 0 và in PID/cổng nếu tra được, cùng hướng dẫn dừng tiến trình bằng tay.
4. Dùng socket exclusive trên Windows (`SO_EXCLUSIVEADDRUSE`) trước bind; không để một static server `0.0.0.0` và editor server `127.0.0.1` cùng chiếm cổng một cách âm thầm.
5. Chỉ in/mở URL dạng `http://127.0.0.1:<port>/...`.

Không tự động kill PID và không tự đổi cổng âm thầm. Có thể cho phép `--port`, nhưng URL phải lấy đúng `server.server_port`.

### 4.2 Health contract

Thêm:

```http
GET /api/health
```

Response 200:

```json
{
  "service": "gfl2-editor-server",
  "api_version": 1,
  "root": "D:/Project/gfl2_wiki",
  "capabilities": ["characters", "effects", "guides"]
}
```

Không đưa secret hoặc dữ liệu người dùng vào response. Frontend chỉ chấp nhận đúng `service`, đúng major version và capability cần thiết.

### 4.3 API client dùng chung

Tạo `tools/shared/editor-api.js` dưới dạng ES module, export:

- `checkEditorServer(requiredCapability)`
- `requestJson(path, options)`
- `EditorServerError`

`requestJson` phải:

- Kiểm tra status và `Content-Type` trước khi parse JSON.
- Với HTML 404 từ static server, trả lỗi hành động được: “Bạn đang mở tool bằng static server. Chạy `.venv\\Scripts\\python.exe tools\\start_editors.py` rồi mở URL 127.0.0.1 được in ra.”
- Có timeout bằng `AbortController`.
- Không retry PUT tự động.
- Không log payload chứa Gemini API key hoặc nội dung chưa lưu.

Chuyển ba app sang `type="module"` hoặc chỉ expose một namespace duy nhất. Không thêm global ngắn như `t`, `$`, `state` vào `window`; Effect Editor hiện đã có IIFE, cần giữ tính cô lập này.

### 4.4 Route matrix

Server chính thức phải có tối thiểu:

| Method | Route | Capability | Hành vi |
|---|---|---|---|
| GET | `/api/health` | all | Nhận diện server |
| GET | `/api/effects` | effects | Danh sách effect theo ID |
| PUT | `/api/effects/{effect_id}` | effects | Cập nhật effect hiện có, hỗ trợ thêm/xóa `sub_effect_ids` (validate ID tồn tại, chống tự tham chiếu) |
| PUT | `/api/characters/{slug}?lang=en|vi` | characters | Cập nhật record hiện có |
| GET | `/api/guides/{slug}` | guides | Đọc source guide |
| PUT | `/api/guides/{slug}` | guides | Cập nhật guide hiện có |
| POST | `/api/guides` | guides | Tạo guide mới sau validate slug |

Guide Editor cần hai nút tách nghĩa: “Cập nhật JSON gốc” và “Tải tệp JSON”. Không dùng file picker làm đường lưu source chính thức.

Mọi path parameter phải decode một lần, validate whitelist (`slug`/`effect_id`), resolve path và kiểm tra vẫn nằm trong thư mục cho phép. Giới hạn Content-Length theo loại tài nguyên.

### 4.5 Transaction và chống lost update

Tạo `RepositoryTransaction` dùng:

- `threading.RLock` cho nhiều request trong một server process.
- Lock file liên tiến trình, ví dụ `data/.editor-write.lock` (`msvcrt.locking` trên Windows, `fcntl.flock` trên POSIX), timeout hữu hạn.
- Stage tất cả output vào cùng filesystem với file đích.
- Validate toàn bộ JSON và derived content trước replace.
- `os.replace` theo transaction; nếu bước giữa lỗi, rollback tất cả file đã thay.
- Ghi newline/UTF-8 thống nhất.

Quy tắc nguồn dữ liệu:

- Effect: `effects_vi.json` là nguồn effect; transaction đồng bộ `i18n_vi.json["effects"]`, rồi sinh `i18n-vi.js`.
- Character VI: cập nhật record trong `i18n_vi.json`, rồi sinh `i18n-vi.js`.
- Character EN: chỉ cập nhật `data/characters/{slug}.json`.
- Guide: chỉ cập nhật `data/guides/{slug}.json`.
- Không merge từ snapshot cũ sau khi chờ lock. Phải acquire lock trước, sau đó đọc file mới nhất, merge, validate và ghi.

Chuyển các CLI có `--apply` và có thể chạm file dùng chung sang helper này:

- `tools/sync_lang_bytes.py`
- `tools/extract_vietnamese.py`
- `tools/build_vietnamese_effects.py`
- `tools/migrate_effect_ids.py`
- `tools/tag_server_data.py` nếu ghi i18n bundle

Các exporter chỉ ghi file độc lập vẫn dùng atomic single-file helper để tránh file dở dang.

### 4.6 UX boot và lỗi

Mỗi editor thực hiện theo thứ tự:

1. Render shell tối thiểu.
2. Gọi health check.
3. Nếu fail: khóa các nút ghi, hiện banner cố định gồm origin hiện tại, status nhận được và lệnh launcher chính xác.
4. Nếu pass: mới load dữ liệu và bind thao tác lưu.

Effect Editor không được chỉ toast “Không thể tải dữ liệu” rồi để workspace trống. Data Entry phải khóa “Cập nhật JSON gốc” nếu thiếu capability. Guide Editor vẫn cho phép download JSON khi API lỗi nhưng không cho nút cập nhật source.

Thêm chỉ báo “Editor server: connected / unavailable” ở header. Không phụ thuộc `localStorage` để boot.

### 4.7 Tài liệu thống nhất

Cập nhật:

- `README.md`
- `tools/effect_editor/README.md`
- README/hướng dẫn mới cho Guide Editor
- Các link giữa tool

Chỉ dùng một lệnh chính thức:

```bat
.venv\Scripts\python.exe tools\start_editors.py
```

Chỉ dùng URL `127.0.0.1` trong tài liệu. Ghi rõ `python -m http.server` chỉ dùng preview site tĩnh, không dùng cho editor, và không được chạy cùng cổng editor.

### 4.8 Quản lý hiệu ứng con (Sub-effects Management)

Trong Effect Editor hiện tại, `sub_effect_ids` chỉ được hiển thị ở chế độ đọc (read-only chips) và backend `update_effect` chỉ nhận `{name, desc, type}`, giữ nguyên `sub_effect_ids`. Cần bổ sung tính năng quản lý hiệu ứng con:

1. **Giao diện Effect Editor (`tools/effect_editor/index.html` & `app.js`)**:
   - Thêm nút **"+ Thêm hiệu ứng con"** (`#add-sub-effect`) bên cạnh tiêu đề "Hiệu ứng con" trong `.reference-box`.
   - Khi bấm, hiển thị bộ chọn (dropdown / modal picker) lọc danh sách toàn bộ effect hiện có theo tên EN / tên VI, tự động loại trừ chính effect đang chọn và các effect con đã có trong danh sách.
   - Thêm nút xóa (`×`) trên từng chip của `#sub-effects` để gỡ hiệu ứng con đã gán.
   - Thao tác thêm/xóa effect con đánh dấu `state.dirty = true`, kích hoạt nút "Lưu thay đổi".
2. **Backend API & Store (`tools/editor_server.py` & `tools/effect_editor/store.py`)**:
   - Endpoint `PUT /api/effects/{effect_id}` nhận trường tùy chọn `sub_effect_ids: list[str]`.
   - Xác thực:
     - Toàn bộ `sub_effect_ids` phải là ID hợp lệ tồn tại trong danh mục canonical effects.
     - Chống tự tham chiếu (`effect_id not in sub_effect_ids`).
     - Tự động loại bỏ trùng lặp (deduplicate) giữ nguyên thứ tự.
   - Khi lưu: Cập nhật `sub_effect_ids` của effect, tự động tính toán lại ma trận `referenced_by` cho toàn bộ các effect liên quan, ghi nguyên tử qua `RepositoryTransaction`.

## 5. Trình tự triển khai bắt buộc cho Gemini

### Phase 0 — Baseline, không sửa mã

1. Chụp `git status --short`; không reset hoặc ghi đè thay đổi hiện có.
2. Chạy test hiện tại với `--basetemp` nằm trong workspace.
3. Ghi lại kết quả `curl` cho `localhost` và `127.0.0.1`.
4. Lập inventory route, file được ghi và script tag của từng tool.

### Phase 1 — Viết test đỏ

Thêm test trước production code:

- Health endpoint trả đúng contract.
- Launcher từ chối cổng bị chiếm bởi server không tương thích.
- Launcher tái sử dụng server tương thích.
- Static 404/HTML được API client biến thành thông báo sai server rõ ràng.
- Effect/Data Entry không enable nút lưu khi health fail.
- Hai update song song: một effect và một character VI; cả hai thay đổi còn tồn tại trong JSON và JS bundle.
- Fault injection ở lần replace thứ hai phải rollback mọi file.
- Standalone effect wrapper dùng cùng handler, không có route implementation riêng.
- Guide update/create validate slug và không thoát khỏi `data/guides`.
- Mỗi HTML chỉ load script một lần; Node `--check` cho mọi JS.

Chạy riêng từng test và xác nhận fail vì thiếu hành vi, không phải lỗi fixture/quyền temp.

### Phase 2 — Core server + transaction

1. Implement transaction/bundle helper.
2. Di chuyển store/route vào server chính thức.
3. Biến hai server cũ thành wrapper.
4. Thêm exclusive bind, health và launcher preflight.
5. Chạy unit + HTTP integration tests đến GREEN.

### Phase 3 — Frontend integration

1. Implement shared API client.
2. Tích hợp health gate vào Effect Editor trước; xác nhận lỗi 404 hiện tại chuyển thành banner hành động được.
3. Tích hợp Data Entry, giữ nguyên luồng EN/VI và save-to-source.
4. Tích hợp Guide Editor; giữ nút download, thêm source API riêng.
5. Kiểm tra không phát sinh global redeclaration và không bind event hai lần.

### Phase 4 — CLI writers

Chuyển từng CLI sang transaction helper, mỗi script một commit logic nhỏ. Sau mỗi script:

1. Dry-run không ghi file.
2. Apply trên fixture/temp repo.
3. So sánh JSON và JS bundle.
4. Test concurrent lock timeout.

Không chạy apply trên dữ liệu thật cho đến khi fixture tests pass.

### Phase 5 — Documentation + full verification

1. Cập nhật mọi URL/lệnh.
2. Tìm toàn repo các chuỗi `localhost:8000`, `python -m http.server 8000`, `/api/effects`, server class trùng lặp.
3. Chạy full test suite.
4. Build site.
5. Browser QA cả ba editor từ cùng một server process.

## 6. Ma trận test trình duyệt

Khởi động một server trên port test ngẫu nhiên hoặc port 8000 sạch.

| Tool | Luồng bắt buộc | Kỳ vọng |
|---|---|---|
| Hub | Mở `/tools/` | Health connected; ba link cùng origin |
| Effect Editor | Load danh sách, chọn effect, sửa rồi hủy/không lưu | Không console error; ID/reference đúng |
| Effect Editor | Sửa fixture effect và PUT | Ba file effect/i18n/JS đồng bộ; reload giữ dữ liệu |
| Effect Editor | Thêm/xóa effect con qua nút UI và lưu | `sub_effect_ids` được lưu đúng, không cho tự trỏ chính mình, ma trận `referenced_by` cập nhật chuẩn xác |
| Data Entry | Load Alva EN → VI → EN | Không exception; không mất tag/text |
| Data Entry | Update character fixture | File gốc đúng; trường ngoài payload được giữ |
| Guide Editor | Load guide, update fixture | Đúng file source; download vẫn hoạt động |
| Sai server | Chạy static server rồi mở từng editor | Banner “sai server”; nút ghi disabled; không fetch loop |
| Conflict | Chiếm port trên `0.0.0.0` hoặc `::` rồi chạy launcher | Launcher fail rõ ràng, không tạo listener thứ hai |
| Concurrent | Gửi PUT effect + character VI gần đồng thời | Không mất update, JSON parse được, JS khớp JSON |

Thu console errors và network failures. `favicon.ico` 404 có thể xử lý bằng favicon thật hoặc route 204, nhưng không được tính là lỗi nghiệp vụ API.

## 7. Lệnh kiểm tra dự kiến

```bat
.venv\Scripts\python.exe -m pytest tests\test_editor_server.py tests\test_data_entry_server.py tests\test_effect_editor.py tests\test_guide_editor.py -q --basetemp=scratch\pytest-editors
C:\Users\rintr\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe --check tools\data-entry\app.js
C:\Users\rintr\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe --check tools\effect_editor\app.js
C:\Users\rintr\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe --check tools\guide-editor\app.js
.venv\Scripts\python.exe -m pytest -q --basetemp=scratch\pytest-full
.venv\Scripts\python.exe site\build.py
```

Nếu tên test/file được tổ chức khác, giữ nguyên các acceptance condition; không bỏ test chỉ vì đổi cấu trúc.

## 8. Acceptance criteria

Chỉ coi hoàn thành khi toàn bộ điều kiện sau đúng:

- `curl http://127.0.0.1:8000/api/health` trả service/version hợp lệ.
- Không còn tài liệu editor dùng `localhost`.
- Không còn hai bản implementation effect API.
- Mở Effect Editor qua static server không tạo 404 khó hiểu; UI chỉ rõ lệnh đúng và khóa save.
- Launcher phát hiện conflict trên IPv4 wildcard/IPv6/127.0.0.1 và không chạy server nửa đúng nửa sai.
- Effect và character VI update đồng thời không gây lost update.
- `effects_vi.json`, `i18n_vi.json["effects"]` và `i18n-vi.js` luôn đồng bộ sau save thành công.
- Effect Editor cho phép thêm và xóa effect con; backend validate chặt chẽ ID tồn tại và chống tự tham chiếu.
- Lỗi giữa transaction rollback đầy đủ.
- Data Entry load Alva VI không exception và không mất tag khi save.
- Guide Editor không ghi source qua file picker mơ hồ.
- Không có `SyntaxError`, unhandled rejection hoặc API 4xx/5xx trong các luồng hợp lệ.
- Focused tests, full suite, build và browser QA đều pass.

## 9. Giới hạn phạm vi và quy tắc an toàn

- Không sửa nội dung dịch/character/weapon/effect ngoài fixture cần cho test.
- Không đổi effect ID hoặc quay lại map bằng tên.
- Không xóa standalone entry point đột ngột; dùng wrapper/deprecation.
- Không reset worktree đang bẩn; chỉ sửa file thuộc phase hiện tại.
- Không tự động kill server cũ.
- Không retry thao tác ghi không idempotent.
- Nếu phát hiện schema hoặc đường dẫn ngoài kế hoạch, dừng phase đó, bổ sung test và ghi lý do trước khi mở rộng phạm vi.

## 10. Deliverables Gemini phải bàn giao

1. Danh sách file thay đổi theo từng phase.
2. Log RED/GREEN của test mới.
3. Kết quả full suite và build.
4. Bảng Browser QA gồm console/network cho ba editor và wrong-server case.
5. Bằng chứng concurrent update + rollback.
6. Hướng dẫn chạy duy nhất dùng `127.0.0.1`.
7. Danh sách rủi ro còn lại; không ghi “hoàn thành” nếu acceptance criterion nào chưa có bằng chứng.
