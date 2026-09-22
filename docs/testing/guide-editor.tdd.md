# Guide Editor TDD evidence

## Source and journeys

Requirements were derived from the conversation; no external plan file was used.

- As an editor, I can open an existing character guide directly from the repository.
- As an editor, I can create a new guide with the same section structure as Loreley's guide.
- As an editor, I can edit metadata, duplicate blocks, and write long table cells quickly.
- As an editor, I can format selected paragraph text with bold, italic, underline, text color, or highlight controls.
- As an editor, I can insert Vietnamese skill, weapon, and related-effect references for the character whose guide I am editing.
- As an editor, I can search every reference picker without typing Vietnamese diacritics.
- As an editor, I see the current character's signature weapon first and can inspect its image in a hover/focus popover.
- As an editor, clearing a reference search restores the complete list, and references insert at my saved caret even after cut/paste.
- As an editor, I can drag a table header edge to resize a column and preserve that width in the guide JSON and public page.
- As a reader, weapon and skill popovers remain readable and fully inside the viewport on hover or keyboard focus.
- As a maintainer, I can save the canonical guide schema without transient editor IDs.

## RED and GREEN evidence

| Behavior | RED | GREEN | Guarantee |
|---|---|---|---|
| Loreley-style template and fast editor controls | `pytest tests/test_guide_editor.py -q`: 3 failed because `template.js`, controls, duplicate action, and multiline cells were absent | `pytest tests/test_guide_editor.py -q`: 3 passed | Template emits canonical metadata and ten Loreley sections; editor exposes load/template controls and clean serialization. |
| Word-style Quick Format | Focused test: 1 failed because format controls and styles were absent | `pytest tests/test_guide_editor.py -q --basetemp scratch/pytest-guide-format-green-1205`: 4 passed | Bold, italic, underline, text-color, and highlight controls exist with public-site styles. |
| Guide/server regression | Initial combined run was blocked by Windows temp-directory permissions | `pytest tests/test_guide_editor.py tests/test_guides.py tests/test_editor_server.py -q --basetemp scratch/pytest-guide-editor-1151`: 21 passed | Guide validation and editor API behavior remain intact. |
| Static build smoke tests | N/A | Three targeted `tests/test_build.py` tests passed with an isolated `--basetemp` | Core pages, static assets, and absence of internal editor links remain valid. |
| Data validation | N/A | `.venv/Scripts/python.exe tools/validate.py`: 270 records valid | Saved Loreley guide and all current project records pass schema validation. |
| Free-form rich editing inside blocks | Four focused tests initially failed because paragraph/table fields were plain text, drag support was missing, and the renderer did not preserve rich table markup | `pytest tests/test_guide_editor.py tests/test_guides.py -q`: 17 passed | Paragraphs and table cells are contenteditable; toolbar supports history, size, emphasis, colors, alignment, lists, links, and clear-format while the canonical block JSON schema stays unchanged. |
| Dangerous rich table markup | Focused validator test initially failed because an event-handler payload was accepted | `pytest tests/test_guides.py -q`: passed | Table cells reject dangerous HTML before repository writes; rendering also sanitizes allowed markup and classes. |
| GFL2 element text colors | Two focused tests failed because the menu and sanitizer lacked the seven element classes | Focused tests: 2 passed; combined regression: 22 passed | Text-color menu preserves and renders Burn, Electric, Hydro, Corrosion, Physical, Freeze, and Resonance colors safely. |
| Compact inline character/weapon/skill references | Four focused tests failed because toolbar actions created standalone blocks and the sanitizer removed inline images; the static asset test failed because `%20` was not decoded | Focused tests passed; combined guide/server regression: 37 passed | References append to the active paragraph/table cell with a 20px avatar or icon, keep safe links through save/build, and weapon files containing spaces load correctly. |
| Vietnamese skill, weapon, and related-effect picker | Three focused tests failed because the editor only loaded English character data and had no effect selector; two popover tests failed before class/metadata sanitizer support | Focused tests passed; combined guide regression: 29 passed | Skill/weapon names and descriptions come from `i18n_vi.json`; effects are filtered from the current character's EN+VI data and preserve ID-keyed popover metadata. |
| Dandegate weapon-image mapping audit | Focused test failed because Transience referenced `General Liu Rifle.png` | Focused test passed after mapping Transience to its equivalent `Shadow Runner.png` asset | Transience no longer renders General Liu Rifle; the correction is backed by Dandegate API image comparison. |
| Searchable reference pickers and weapon image popover | `python -m pytest tests\\test_guide_editor.py -q`: 3 failed because search inputs, canonical weapon loading, signature prioritization, and popover markup/styles were absent | Focused run: 16 passed; combined guide/assets regression: 36 passed | Character, weapon, skill, summon-skill, and effect selectors support accent-insensitive filtering; the weapon picker merges canonical `weapons.json`, prioritizes the current character's signature, and preserves a safe image popover through editing/build. |
| Search reset and caret-safe reference insertion | Focused run: 2 failed because reset replaced the full option cache and insertion used `target.append()`; a further focused test failed because blur replaced editor DOM and invalidated the Range; Effect QA exposed a missing dynamic-cache refresh | Focused run: 19 passed; combined guide/assets regression: 39 passed | Clearing search filters from the immutable cached options; Character, Weapon, Skill, and Effect insert via the saved Range; blur/cut/paste preserve the live editor DOM and caret; dynamically rebuilt Effect options refresh their cache before filtering. |
| Resizable table columns | Two focused tests failed because table blocks had no width model, resize handle, validation, or public rendering; a cache regression test then failed because the editor stylesheet URL was not versioned | Focused tests passed; relevant guide/assets/data regression: 110 passed | Header drag handles resize from 80–1200 px, persist `column_widths`, render through `<colgroup>` in editor/preview/public pages, and the cache-busted stylesheet exposes the handle immediately. |
| Viewport-safe weapon and formatted skill popovers | Two focused tests failed because the build sanitizer removed nested popover classes and the public runtime had no formatted skill popover or viewport positioning | Focused tests passed; combined guide/editor/assets regression: 43 passed | Nested weapon/skill classes survive save and build; legacy skill titles are upgraded to formatted Vietnamese popovers; fixed-position popovers are clamped to the viewport and weapon artwork stays at 92×68 px. |
| Popover runtime cache and scroll lifecycle | Cache regression test failed because `search.js` had no asset version; scroll lifecycle test failed because hidden popovers retained fixed `left/top` values | Three focused tests passed; combined guide/editor/assets regression: 45 passed | Every build changes the `search.js` version when its content changes; CSS falls back beside the reference; active popovers are repositioned after scroll/resize and stale coordinates are cleared when closed. |

## Manual browser proof

- Opened Loreley through **Mở guide nhân vật** and verified all 30 blocks rendered.
- Saved through **Cập nhật JSON gốc**; UI confirmed `data/guides/loreley.json` was updated.
- Selected `đậm`, clicked **B**, and observed `<b>đậm</b>` plus formatted preview.
- Selected `Văn bản`, applied yellow highlight, and observed `<span class="guide-highlight-yellow">Văn bản</span>`.
- Reloaded Loreley afterward, discarding temporary smoke-test content.
- Opened Soppo and verified 37 draggable blocks, 118 rich editors, and 104 editable table cells.
- Applied bold and unordered-list formatting to temporary content, then reloaded Soppo without saving.
- Browser console contained no errors after the rich-editor interaction pass.
- Verified all seven element labels in the browser; applying Burn produced `guide-text-burn` with `rgb(237, 79, 18)`, then reloaded Loreley without saving.
- In a temporary unsaved paragraph, inserted Thorn Criterion after `Core:`; editor and preview each rendered one compact reference and a 1024px-source thumbnail. Browser console contained no errors.
- Selected Loreley, inserted `Vết Sẹo Rực Cháy`, `Quy Tắc Gai Nhọn`, and `Tàn Tro Lửa Rực`; editor and preview retained Vietnamese text/metadata and browser console remained clean. No guide was saved during QA.
- Selected Loreley and opened Weapon: `★ Vũ khí đặc trưng — Dạ Khúc Thủy Triều / Tidal Nocturne` appeared first. Searching `da khuc thuy trieu` reduced the list to that single weapon.
- Inserted the weapon without saving. Both editor and preview loaded `assets/images/weapons/Tidal Nocturne.png` at natural width 1024px in the inline thumbnail and image popover; the request returned HTTP 200 and browser console remained clean.
- Verified accent-insensitive searches: `lore` matched Loreley, `vet seo` matched `Vết Sẹo Rực Cháy`, and `lua` matched Loreley's related Vietnamese effects.
- Verified clearing `lore` restored all 66 Character choices. Character (Alva), Weapon (Nighttide Nocturne), and Skill (Vết Sẹo Rực Cháy) were each inserted between `BEGIN` and `END`, not appended.
- Cut `CUT` from `BEGIN CUT END`, pasted it at the end, moved the caret back after `BEGIN`, then inserted `Chỉ Lệnh Bổ Sung`; resulting DOM order was `BEGIN` → Effect → `END CUT`, with no console errors.
- Created a 3-column table, dragged the first header edge from 180 px to 280 px, and observed matching editor/preview widths `[280, 180, 180]`; browser console contained no errors and no guide was saved.
- Opened the built Soppo guide at 1280×720 and keyboard-focused both reference types. The skill popover rendered at 420×287 px with preserved line breaks; the Capitoline popover rendered at 360×112 px with a 92×68 px contained image. Both bounding boxes stayed fully inside the viewport.
- Reloaded the rebuilt Soppo guide with `search.js?v=4d9c4eb2f42c`. All 10 legacy skill references became formatted popovers and lost their native `title`; Capitoline stayed adjacent to its link before and after page scrolling, with both popovers inside the 1280×720 viewport.

## Coverage and gaps

- No coverage plugin is installed, so percentage coverage was not measured.
- Full `test_build.py` run was stopped after a long run exposed one unidentified failure; task-relevant build tests passed separately.
- Git checkpoints were not created because the working tree already contains many unrelated user changes.
- Final build: `python site\\build.py` validated 271 records and rendered 269 HTML pages; generated public CSS contains the weapon popover styles.
- Caret/search regression build: `python site\\build.py` validated 272 records and rendered 270 HTML pages.
- Popover regression build: `python site\\build.py` validated 272 records and rendered 270 HTML pages; `pytest tests/test_guide_editor.py tests/test_guides.py tests/test_assets.py -q` passed 43 tests.
- Popover cache/lifecycle regression: the same combined command passed 45 tests; JavaScript syntax check and a fresh 270-page build also passed.
