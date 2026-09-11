# Effect Editor — TDD Evidence

## User journeys

- An editor compares English source text and Vietnamese translation side by side.
- Saving updates the Vietnamese effect catalog, localization bundle, and generated browser bundle.
- Renaming an effect preserves every `sub_effect_ids` reference without relying on either display name.
- Duplicate Vietnamese names remain separate records because all writes use stable IDs.
- Invalid IDs or types fail before any file changes.
- Opening the editor through the documented project server loads `/api/effects` successfully.

## Evidence

| Guarantee | Test or command | Type | Result |
|---|---|---|---|
| Catalog lists each English effect once and reports inbound references | `test_list_effects_returns_one_row_per_english_effect_with_references` | Unit | PASS |
| Rename preserves ID references and synchronizes `i18n_vi.json` | `test_rename_preserves_id_references_and_updates_i18n_bundle` | Integration | PASS |
| Duplicate names remain distinct; unknown IDs and invalid types do not write | validation tests in `tests/test_effect_editor.py` | Unit | PASS |
| Legacy name aliases migrate to ID keys and `sub_effect_ids` | `tests/test_effects_catalog.py` | Migration | 3 passed |
| Generated character markup and browser catalog use IDs | effect tests in `tests/test_build.py` | Integration | 3 passed |
| Shared editor server exposes `/api/effects` | `test_combined_editor_server_exposes_effect_api` | HTTP integration | PASS |
| Documented launcher imports and starts correctly | `test_editor_server_script_can_start_from_readme_command` | CLI integration | PASS |
| Project test suite | `pytest tests` | Integration | 224 passed |
| All project data remains valid | `python tools/validate.py` | Integration | 266 records valid |
| Static wiki remains buildable | `python site/build.py` | End-to-end | 264 pages built |

## RED/GREEN record

- RED 1: import failed because `tools.effect_editor` did not exist.
- GREEN 1: initial editor store implementation made 4 tests pass.
- RED 2: name-keyed expectations could not represent two effects named `Ẩn Nấp` safely.
- GREEN 2: 765 name/alias keys migrated to 381 ID-keyed records; 8 focused tests passed.
- RED 3: shared port `8000` static server returned HTTP 404 for `/api/effects`; README still launched `http.server`.
- GREEN 3: shared editor server now handles effect API; 14 focused tests and 224 full-suite tests passed.

## Coverage and QA

- Python `trace` reported 100% executed-line coverage for `tools.effect_editor.store` during its five focused tests.
- Browser QA confirmed 381 effects load; `Concealed` and `Concealment` remain independently selectable despite the same Vietnamese name.
- Browser QA on the shared server confirmed zero console errors and opened `Absolute Defense` in the EN/VI workspace.
- Character QA confirmed 37 triggers carry `data-effect-id`; popovers render in EN/VI and nested references resolve by ID.
- No committed visual baseline exists, so pixel-level visual regression status is inconclusive.
