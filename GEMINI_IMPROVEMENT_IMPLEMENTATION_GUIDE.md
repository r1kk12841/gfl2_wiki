# Hướng dẫn triển khai cải thiện GFL2 Wiki cho Gemini

> Tài liệu thực thi. Đọc toàn bộ trước khi sửa. Triển khai theo đúng thứ tự. Không mở rộng phạm vi ngoài tài liệu nếu chưa có xác nhận.

## 1. Mục tiêu

Đưa dự án từ trạng thái “chạy tốt cục bộ” sang trạng thái có thể build, kiểm thử và deploy lặp lại trên máy sạch.

Kết quả cuối phải đạt các mục tiêu sau:

1. Push hoặc pull request luôn chạy validation, test và build trong CI.
2. Push vào `main` deploy GitHub Pages đúng như README mô tả.
3. Build không đọc hoặc sao chép file bị Git ignore.
4. Test không phụ thuộc `dist/` đã tồn tại.
5. Validator từ chối trường sai tên và tham chiếu dữ liệu hỏng.
6. Build không ghi file sinh tự động vào `site/static/`.
7. Asset chính nhẹ hơn, ưu tiên WebP đã có.
8. Filter, FAQ và search dùng được bằng bàn phím và screen reader.
9. Trang Guides không chứa link hỏng hoặc HTML không được kiểm soát.
10. Dependency có phiên bản tái lập được.

## 2. Hiện trạng đã xác minh

- Python + Jinja2 static-site generator.
- Dữ liệu: 64 nhân vật, 187 vũ khí, 7 FAQ.
- Validation hiện tại: 258 record hợp lệ.
- Test hiện tại: 160 test pass khi `dist/` đã build.
- Build hiện tại: 255 trang HTML.
- Có 1.392 tham chiếu ảnh trong dữ liệu; tất cả đang tồn tại.
- Không có slug nhân vật/vũ khí trùng.
- `assets/images/` khoảng 114,9 MiB.
- PNG khoảng 107,3 MiB; 64 file WebP khoảng 7,6 MiB.
- `dist/` local khoảng 153,7 MiB vì build chép thêm thư mục ignored `image/`.
- `.github/workflows/` đang trống dù README nói có `deploy.yml`.
- Chạy build và test cùng lúc có thể gây lỗi do cả hai cùng sửa `dist/`.

## 3. Quy tắc làm việc

1. Không sửa dữ liệu game trừ khi test mới chứng minh dữ liệu đang sai.
2. Không xóa asset chỉ vì chưa thấy template tham chiếu trực tiếp. CSS, JavaScript hoặc guide có thể dùng asset đó.
3. Không commit `dist/`, cache, virtual environment hoặc file tạm.
4. Mỗi phase phải có test trước khi chuyển phase tiếp theo.
5. Giữ URL hiện tại của character và weapon để không tạo link chết.
6. Giữ cả tiếng Anh và tiếng Việt hoạt động.
7. Không đổi thiết kế trực quan ngoài các thay đổi accessibility được yêu cầu.
8. Không dùng network runtime cho website, ngoại trừ Google Fonts hiện có.
9. Không thêm backend, database, tài khoản hoặc framework frontend.
10. Nếu cần thay đổi schema, cập nhật validator, entry tool, dữ liệu, builder và test trong cùng phase.

## 4. Baseline bắt buộc

Chạy trước khi sửa:

```powershell
git status --short --branch
.venv\Scripts\python.exe tools\validate.py
.venv\Scripts\python.exe site\build.py
.venv\Scripts\python.exe -m pytest tests -q
```

Kỳ vọng:

- Validation exit code `0`.
- Build exit code `0` và tạo 255 trang khi chưa có guide.
- Pytest báo 160 test pass tại baseline.
- Ghi lại mọi warning. Không coi warning là lỗi mới nếu warning đã có tại baseline.

Không chạy test và build song song ở baseline. Cả hai đang dùng chung `dist/`.

---

## Phase 1 — CI và GitHub Pages

### Vấn đề

README nói `.github/workflows/deploy.yml` tồn tại, nhưng thư mục workflow đang trống. Không có cơ chế bắt lỗi trước merge hoặc deploy tự động.

### File cần tạo hoặc sửa

- Tạo `.github/workflows/ci.yml`.
- Tạo `.github/workflows/deploy.yml`.
- Sửa `README.md` nếu lệnh hoặc quy trình thực tế thay đổi.

### `ci.yml`

Trigger:

- `pull_request` vào `main`.
- `push` vào `main`.
- `workflow_dispatch`.

Thiết lập tối thiểu:

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install --upgrade pip
      - run: python -m pip install -r requirements.txt
      - run: python tools/validate.py
      - run: python -m pytest tests -q
      - run: python site/build.py
```

Nếu Phase 3 chuyển test sang tự build trong thư mục tạm, vẫn giữ bước production build riêng. Bước đó xác minh CLI thật.

### `deploy.yml`

Trigger deploy chỉ trên push vào `main` hoặc `workflow_dispatch`.

Yêu cầu:

- Dùng GitHub Pages artifact deployment chính thức.
- Cấp `contents: read`, `pages: write`, `id-token: write`.
- Dùng `concurrency` group `pages` với `cancel-in-progress: false`.
- Chạy validation và test trước deploy.
- Build `dist/` trên runner sạch.
- Upload đúng thư mục `dist/`.
- Không push trực tiếp vào branch `gh-pages` bằng token tự tạo.

Khung workflow:

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install --upgrade pip
      - run: python -m pip install -r requirements.txt
      - run: python tools/validate.py
      - run: python -m pytest tests -q
      - run: python site/build.py
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
```

Trước commit, kiểm tra các major version action vẫn được GitHub hỗ trợ. Nếu repo dùng chính sách pin SHA, thay tag bằng commit SHA chính thức và thêm comment tên version.

### Acceptance criteria

- GitHub nhận cả hai workflow, không báo lỗi YAML.
- Pull request chạy validation, pytest và build.
- Push `main` chỉ deploy sau khi mọi bước kiểm tra pass.
- README khớp workflow thật.

---

## Phase 2 — Build sạch, tách output, không dùng file ignored

### Vấn đề

`site/build.py` hiện:

- Ghi `effects-data.js` vào `site/static/js/`.
- Xóa và ghi trực tiếp từng phần trong `dist/`.
- Sao chép thư mục root `image/`, dù thư mục này bị Git ignore.
- Dùng biến global `DIST_DIR`, làm test khó cô lập.

### Thiết kế cần triển khai

Refactor builder để mọi hàm nhận output path rõ ràng.

API mục tiêu:

```python
def build_site(output_dir: Path | None = None) -> int:
    final_dir = output_dir or DIST_DIR
```

Tách thêm các hàm:

```python
def copy_static_assets(output_dir: Path) -> None: ...
def generate_effects_js(output_file: Path) -> None: ...
def generate_search_index(..., output_dir: Path) -> None: ...
```

### Yêu cầu triển khai

1. Xóa `IMAGE_DIR` và toàn bộ logic copy root `image/`.
2. Chỉ copy:
   - `site/static/` vào `<output>/static/`.
   - `assets/` vào `<output>/assets/`.
3. Tiếp tục bỏ qua `assets/images/raw/` và `*LangPackage*`.
4. Sinh `effects-data.js` vào `<output>/static/js/effects-data.js` sau khi copy static.
5. Không sửa bất kỳ file nào dưới `site/static/` trong lúc build.
6. Khi gọi CLI không truyền output, build vào staging directory cùng parent với `dist`.
7. Chỉ thay `dist` sau khi validation, copy và render hoàn tất.
8. Dọn staging directory khi build fail.
9. Khi `output_dir` được truyền bởi test, build thẳng vào thư mục test riêng; không đụng `dist`.
10. Fresh build phải loại bỏ trang cũ không còn trong data.

Trên Windows, không giả định rename đè được thư mục không rỗng. Dùng quy trình staging, backup và cleanup có kiểm soát. Không dùng `shutil.rmtree()` trên path chưa resolve và chưa kiểm tra nằm trong project root.

### Test cần thêm

Thêm vào `tests/test_build.py` hoặc file mới:

- Build vào `tmp_path / "dist"` thành công.
- Build test không tạo hoặc sửa `site/static/js/effects-data.js`.
- Output không có thư mục `image/`.
- Output có `static/js/effects-data.js`.
- File giả trong output cũ biến mất sau fresh build.
- Build fail giữa chừng không phá output hợp lệ trước đó.
- Hai build dùng hai output directory riêng có thể chạy độc lập.

### Acceptance criteria

- `git status --short` không đổi sau build, ngoài file đã sửa có chủ đích.
- Xóa `dist/`, chạy build một lần vẫn thành công.
- Tạm đổi tên root `image/`, build vẫn cho output giống về số trang và link.
- `dist/image/` không tồn tại.

---

## Phase 3 — Test tự chứa, không dùng `dist/` cũ

### Vấn đề

`tests/test_build.py` đang đọc trực tiếp `ROOT / "dist"`. Test có thể pass trên artifact cũ hoặc fail trên clean checkout.

### Cách sửa

Tạo fixture session trong `tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def built_site(tmp_path_factory):
    output = tmp_path_factory.mktemp("site-output")
    assert build_site(output_dir=output) == 0
    return output
```

Sửa test build để nhận `built_site` thay vì dùng constant `DIST_DIR`.

Không gọi build ở import time. Không để test phụ thuộc thứ tự chạy.

### Test chất lượng output cần thêm

- Mọi character JSON có đúng một trang HTML.
- Mọi weapon JSON có đúng một trang HTML.
- Mọi URL trong `search-index.json` trỏ tới file tồn tại.
- Mọi đường dẫn asset lấy từ character/weapon JSON tồn tại trong output.
- Không có link nội bộ tới `tools/guide-editor/` trong output public.
- Không có URL bắt đầu bằng path local Windows.
- `search-index.json` không có slug trùng.

### Acceptance criteria

Lệnh sau phải pass khi `dist/` không tồn tại:

```powershell
.venv\Scripts\python.exe -m pytest tests -q
```

---

## Phase 4 — Schema strict và kiểm tra quan hệ dữ liệu

### Vấn đề

Pydantic mặc định bỏ qua extra fields. Một typo có thể qua validation nhưng không xuất hiện trên website.

### File cần sửa

- `tools/validate.py`.
- `tests/test_data_schema.py`.
- Có thể tạo `tests/test_data_integrity.py`.
- Cập nhật `tools/data-entry/` nếu schema thay đổi.

### Model base strict

Tạo base model dùng chung:

```python
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_default=True,
    )
```

Cho toàn bộ model dữ liệu kế thừa `StrictModel`.

Đổi list default từ `[]` sang `Field(default_factory=list)` để ý nghĩa rõ ràng và tránh shared mutable defaults.

### Validator field

Thêm kiểm tra:

- `slug`: lowercase kebab-case, regex `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- `name`: không rỗng sau `strip()`.
- `hp`, `atk`, `def`: số nguyên không âm khi có.
- `range`, `stability_damage`, `confectance_cost`: không âm khi có.
- `tier`: chỉ 1 đến 6.
- Fortification có đủ tier 1 đến 6, không chỉ kiểm tra length.
- Neural Helix node không trùng.
- Weapon `weapon_type` thuộc `VALID_WEAPON_TYPES` khi có.
- Weapon `rarity` thuộc `VALID_W_RARITIES` khi có.
- Server thuộc `global` hoặc `cn`.

### Kiểm tra liên file trong `validate_all()`

Sau khi parse toàn bộ record, kiểm tra:

1. Character slug duy nhất.
2. Weapon slug duy nhất.
3. Character slug khớp tên file JSON.
4. Mỗi `signature_weapon` khớp name hoặc slug của một weapon.
5. Mọi đường dẫn ảnh là relative path, không chứa `..`, không phải URL và tồn tại dưới project root.
6. Mọi guide `char_slug`, character card, weapon card và skill index tham chiếu hợp lệ.
7. FAQ question không trùng sau normalize whitespace và lowercase.

Không chỉ in warning rồi tiếp tục. Lỗi schema hoặc quan hệ phải trả exit code `1`.

### Test âm bắt buộc

Mỗi rule mới cần ít nhất một test fail đúng lý do:

- Extra field bị từ chối.
- Duplicate slug bị từ chối.
- Slug sai format bị từ chối.
- Signature weapon không tồn tại bị từ chối.
- Asset path traversal bị từ chối.
- Weapon rarity không hợp lệ bị từ chối.
- Fortification có 6 item nhưng trùng tier bị từ chối.

### Acceptance criteria

- Dữ liệu hiện tại vẫn pass hoặc chỉ cần sửa lỗi thật được test chỉ ra.
- Không có typo field nào bị bỏ qua âm thầm.
- Error message chứa file hoặc record gây lỗi.

---

## Phase 5 — Giảm dung lượng asset

### Mục tiêu trước mắt

Dùng 64 portrait WebP đã có. Không chuyển đổi toàn bộ asset trong cùng pull request.

### Cách triển khai an toàn

1. Thêm field tùy chọn `portrait_webp` vào model `Images`.
2. Thêm `portrait_webp` vào từng character JSON khi file tương ứng tồn tại.
3. Cập nhật data-entry tool để giữ field này khi load và export.
4. Trong character card và character detail, dùng `<picture>`:

```html
<picture>
  {% if doll.images and doll.images.portrait_webp %}
  <source srcset="{{ rel_prefix }}{{ doll.images.portrait_webp }}" type="image/webp">
  {% endif %}
  <img src="{{ rel_prefix }}{{ doll.images.portrait }}" ...>
</picture>
```

5. Giữ PNG fallback trong phase này.
6. Thêm `width` và `height` phù hợp cho ảnh để giảm layout shift.
7. Giữ `loading="lazy"` cho ảnh ngoài viewport.
8. Không lazy-load ảnh hero/LCP của trang detail.

### Bước sau, tách pull request

- Tạo asset manifest từ dữ liệu, template và CSS.
- Chỉ copy asset public có trong manifest.
- Chuyển skill/range/weapon images sang WebP hoặc AVIF sau visual regression test.
- Cân nhắc Git LFS chỉ cho asset nguồn lớn, không dùng Git LFS cho file cần GitHub Pages phục vụ trực tiếp nếu pipeline không resolve LFS.

### Test cần thêm

- Mỗi `portrait_webp` tồn tại.
- Output `<picture>` có WebP source và PNG fallback.
- Không có ảnh public tham chiếu tới root `image/`.
- Test giới hạn dung lượng output. Đặt ngưỡng ban đầu theo clean build, không theo local build chứa `image/`.

### Acceptance criteria

- Tất cả card và detail portrait hiển thị khi browser hỗ trợ WebP.
- PNG fallback vẫn hoạt động.
- Dung lượng network cho trang character index giảm rõ rệt.

---

## Phase 6 — Accessibility và mobile

### Filter chips

Đổi mọi clickable filter `<span class="chip">` thành:

```html
<button type="button" class="chip" data-filter="..." data-value="..." aria-pressed="false">
```

Nút active dùng `aria-pressed="true"`. JavaScript cập nhật đồng thời class và ARIA state.

### FAQ accordion

Đổi `.faq-question` thành `<button type="button">`.

Mỗi câu hỏi cần:

- ID duy nhất.
- `aria-expanded="false"` ban đầu.
- `aria-controls` trỏ tới answer ID.

Mỗi answer cần:

- ID tương ứng.
- `hidden` ban đầu.
- `role="region"`.
- `aria-labelledby` trỏ về question ID.

JavaScript dùng `answer.hidden`, không kiểm tra `style.display`.

### Global search

Input cần:

- Label dành cho screen reader.
- `role="combobox"`.
- `aria-autocomplete="list"`.
- `aria-controls="search-dropdown"`.
- `aria-expanded` đúng trạng thái.

Dropdown dùng `role="listbox"`. Result dùng role phù hợp. Thêm điều khiển:

- `ArrowDown` và `ArrowUp` đổi result active.
- `Enter` mở result active.
- `Escape` đóng dropdown.
- Focus không bị mất khi danh sách cập nhật.
- Trạng thái không có kết quả được thông báo bằng `aria-live="polite"`.

### Focus và chuyển động

- Thêm `:focus-visible` rõ cho link, button, card và input.
- Không đặt `outline: none` nếu không có outline thay thế.
- Thêm `@media (prefers-reduced-motion: reduce)` để tắt smooth scroll, transform và transition không cần thiết.

### Mobile navigation

Kiểm tra viewport 320, 375, 768 và 1024 px.

Nếu nav tràn tại 320/375 px, thêm menu toggle thật bằng `<button>` với `aria-expanded`. Không chỉ ẩn link mà không cung cấp đường truy cập thay thế.

### Test cần thêm

- Test HTML xác nhận semantic button và ARIA attributes.
- Browser test cho keyboard filter, FAQ và search.
- Test `Escape` đóng search và effect popover.
- Test không có horizontal scroll ở 320 px trên home, character index và một character detail.

---

## Phase 7 — Hoàn thiện Guides

### Vấn đề

- Navigation luôn hiện Guides dù chưa có guide.
- Empty state trỏ tới `../tools/guide-editor/index.html`, nhưng builder không publish `tools/`.
- Guide CSS dùng biến chưa khai báo: `--surface`, `--border`, `--radius`, `--surface-hover`.
- Guide paragraph dùng `{{ block.html | safe }}` mà chưa có sanitizer hoặc schema.
- `load_guides()` bắt exception rồi bỏ qua guide lỗi.

### Cách sửa

1. Giữ trang Guides public nhưng bỏ link tới editor local khỏi empty state.
2. Đổi empty state thành thông báo “Chưa có guide”.
3. Không copy toàn bộ `tools/` vào public site.
4. Thay biến CSS guide bằng biến đã có:
   - `--surface` thành `--bg-surface`.
   - `--surface-hover` thành `--bg-card-hover`.
   - `--border` thành `--border-subtle`.
   - `--radius` thành `--radius-md`.
5. Tạo Pydantic schema cho guide và từng block type.
6. Validator phải từ chối block type, heading level, index hoặc reference không hợp lệ.
7. Không bỏ qua guide parse error. Build phải fail.
8. Xử lý paragraph HTML theo một trong hai cách:
   - Ưu tiên: lưu plain text và để Jinja autoescape.
   - Nếu cần formatting: sanitize bằng allowlist trước khi tạo `Markup`; chỉ cho phép tag trình bày cần thiết, không cho `script`, inline event, `style`, `iframe` hoặc URL scheme nguy hiểm.

### Acceptance criteria

- `dist/guides/index.html` không có link chết.
- Guide lỗi làm validation/build fail với tên file rõ ràng.
- Không có raw HTML không được sanitize.
- CSS guide không tham chiếu custom property chưa định nghĩa.

---

## Phase 8 — Dependency và môi trường tái lập

### Vấn đề

`requirements.txt` đang dùng `>=`, nên cùng commit có thể cài dependency khác nhau theo thời điểm.

### Cách sửa

1. Chọn Python 3.12 làm phiên bản hỗ trợ chuẩn trong CI.
2. Tạo `requirements.in` chứa dependency trực tiếp:

```text
Jinja2>=3.1,<4
pydantic>=2,<3
pytest>=8,<9
```

3. Dùng `pip-tools` tạo `requirements.txt` pin toàn bộ dependency transitive.
4. Commit cả `requirements.in` và `requirements.txt`.
5. Thêm hướng dẫn cập nhật lock file vào README.
6. Có thể tách runtime và dev dependency sau khi pipeline ổn định:
   - `requirements.in`: Jinja2, pydantic.
   - `requirements-dev.in`: include runtime, pytest và công cụ QA.

Không tự lấy version từ máy local rồi pin nếu chưa chạy test với chính lock file đó.

### Acceptance criteria

- Cài từ lock file trong virtual environment mới thành công.
- Validation, test và build pass với Python 3.12.
- CI dùng đúng lock file.

---

## Phase 9 — SEO và metadata

Triển khai sau khi CI, build và test ổn định.

### Yêu cầu

1. Thêm canonical URL theo từng trang.
2. Thêm Open Graph title, description, type, URL và image.
3. Thêm Twitter card metadata.
4. Sinh `sitemap.xml` từ chính danh sách trang đã render.
5. Sinh `robots.txt` tham chiếu sitemap.
6. Thêm JSON-LD phù hợp cho website và trang article/guide nếu có.
7. Không hardcode domain ở nhiều template. Dùng một `SITE_URL` chuẩn hóa trong builder.
8. Nếu `SITE_URL` chưa cấu hình, build local vẫn chạy nhưng bỏ canonical/sitemap absolute URL hoặc dùng giá trị mặc định được ghi rõ.

### Test cần thêm

- Sitemap chứa mọi trang public và không chứa file editor/tool.
- Canonical URL đúng GitHub Pages base path.
- Open Graph image tồn tại.
- Không có duplicate canonical URL.

---

## 5. Ma trận kiểm chứng cuối

Chạy trên clean checkout hoặc virtual environment mới:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe tools\validate.py
.venv\Scripts\python.exe -m pytest tests -q
.venv\Scripts\python.exe site\build.py
git diff --check
git status --short
```

Kết quả bắt buộc:

- Mọi lệnh exit code `0`.
- Test pass khi `dist/` không tồn tại trước test.
- Build không làm dirty tracked files.
- `dist/image/` không tồn tại.
- `dist/static/js/effects-data.js` tồn tại.
- Mọi URL trong search index tồn tại.
- Không có link public tới `tools/guide-editor/`.
- Không có asset reference bị thiếu.
- Không có duplicate slug.
- CI và deploy workflow chạy xanh trên GitHub.

Kiểm tra thủ công tối thiểu:

1. Home ở desktop và 375 px.
2. Character index: từng filter và nhiều filter kết hợp.
3. Global search bằng chuột và bàn phím, cả EN và VI.
4. Một character Global và một character CN.
5. Một character có summon.
6. Weapon index và weapon detail.
7. FAQ bằng chuột và bàn phím.
8. Effect popover bằng hover, click, focus và Escape.
9. Guides empty state và một guide mẫu hợp lệ.
10. Refresh trực tiếp ở URL nested sau deploy Pages.

## 6. Thứ tự pull request khuyến nghị

Không gộp mọi phase thành một pull request lớn.

1. PR 1: CI + GitHub Pages.
2. PR 2: Output directory + atomic build + self-contained tests.
3. PR 3: Strict schema + integrity validation.
4. PR 4: WebP portraits + output size guard.
5. PR 5: Accessibility + mobile browser tests.
6. PR 6: Guides hardening.
7. PR 7: Dependency lock + SEO.

Mỗi PR cần ghi:

- Vấn đề được sửa.
- File và hành vi thay đổi.
- Test đã thêm.
- Lệnh verification và kết quả.
- Rủi ro còn lại.
- Cách rollback.

## 7. Điều kiện dừng

Dừng và hỏi người dùng trước khi:

- Đổi URL public hiện có.
- Xóa asset hoặc rewrite toàn bộ lịch sử Git.
- Thêm dịch vụ third-party.
- Đổi hosting khỏi GitHub Pages.
- Đổi schema khiến phải sửa hàng loạt nội dung game bằng phán đoán.
- Publish data-entry hoặc guide-editor lên website public.
- Thay đổi thuật ngữ tiếng Việt hoặc tiếng Anh của dữ liệu game.

Không báo hoàn tất nếu chỉ có test unit pass. Hoàn tất chỉ khi validation, test, production build và CI đều pass.
