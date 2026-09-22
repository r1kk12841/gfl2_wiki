# GFL2: Exilium Wiki

A statically-generated HTML wiki for *Girls' Frontline 2: Exilium*, built from manually-entered JSON data.

## Project Layout

```
data/
  characters/*.json     ← one file per character (filled via entry tool)
  weapons.json
  faq.json
assets/images/          ← saved manually alongside data entry
tools/
  data-entry/           ← browser-based form (Phase 1)
  validate.py           ← pydantic schema check
site/
  templates/            ← Jinja2 templates
  static/               ← CSS + JS
  build.py              ← site generator
dist/                   ← generated output (git-ignored)
tests/                  ← pytest suite
```

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Editor Tools

Khởi động Unified Editor Server cho cả 3 công cụ (Data Entry, Effect Editor, Guide Editor):

```bash
.venv\Scripts\python.exe tools/start_editors.py
# hoặc entrypoint wrapper: python tools/data_entry_server.py
# Hub tập trung: http://127.0.0.1:8000/tools/index.html
# Data entry: http://127.0.0.1:8000/tools/data-entry/index.html
# Effect editor: http://127.0.0.1:8000/tools/effect_editor/index.html
# Guide editor: http://127.0.0.1:8000/tools/guide-editor/index.html
```

> **Lưu ý**: Địa chỉ chính thức luôn dùng `127.0.0.1`, không trộn lẫn với `localhost`. Lệnh `python -m http.server` chỉ dùng xem preview site tĩnh trong `dist/`, tuyệt đối không dùng để chạy các editor tools.

1. Open a character tab in the source spreadsheet.
2. Fill in the form (Basic Info → Skills → Fortification → Neural Helix → Keys).
3. Save the character's portrait + class icon to `assets/images/characters/<slug>/`.
4. Click **Download JSON** → move the file to `data/characters/<slug>.json`.
5. Run `python tools/validate.py` to catch schema errors early.

For weapons: switch to the **Weapon** tab. Append the exported weapon object to `data/weapons.json`.  
For FAQ: switch to the **FAQ** tab and download / replace `data/faq.json` directly.

### Editing an existing character

1. Open the entry tool, click **Load JSON**, pick the character's `.json` file.
2. Make changes, click **Download JSON**, replace the file in `data/characters/`.

## Validate Data

```bash
python tools/validate.py
```

Exits `0` on success, `1` with error details on failure.

## Build Site

```bash
python site/build.py
```

Output goes to `dist/`. Open `dist/index.html` in a browser to preview locally.

## Run Tests

```bash
pytest tests/
```

## Deploy (GitHub Pages)

Push to `main`. The GitHub Action in `.github/workflows/deploy.yml` runs `validate.py` → `pytest` → `build.py` → deploys `dist/` directly via GitHub Pages artifact deployment. Pull requests and commits run automated validation, testing, and build checks via `.github/workflows/ci.yml`.

## Dependency Management

Direct dependencies are tracked in `requirements.in`. Pinned and transitive dependencies are locked in `requirements.txt` via `pip-tools`.

To recompile or upgrade the lock file:
```bash
python -m pip install pip-tools
python -m piptools compile requirements.in -o requirements.txt
```

## Adding a New Character

1. Enter data via the entry tool (see above).
2. Save images at the expected paths.
3. Move the JSON to `data/characters/`.
4. Run `python tools/validate.py`.
5. Commit and push → GitHub Action rebuilds the site.

## Credits

Source data compiled by the GFL2 community. See the `Home` tab of the source spreadsheet for full credits.
