# Lang bytes data completion — verification record

## Scope and evidence

- Scanned `D:\Project\gfl2_text_data`: 2,854 `.bytes` tables.
- Parsed `LangPackageTableEnusData.bytes` and `LangPackageTableVtviData.bytes`: 429,779 records each.
- Joined translations by localization ID. A value is auto-applied only when an English project string resolves to one unique Vietnamese value.
- `GunData.bytes`, `GunWeaponData.bytes`, and `BattleBuffData.bytes` use nested configuration schemas. The language-table parser can enumerate their outer records but cannot safely decode their fields, so they are not treated as localization text.

## RED

`python -m pytest tests/test_lang_bytes_sync.py -q`

- Parser was not import-safe and executed during import.
- 8/195 weapons had no Vietnamese record.
- Verified official values such as Alva's `Freezing Touch` and `Shelter` were stale.
- 17 character translation list items were missing.

## GREEN

- Refactored `tools/parse_lang_bytes.py` into bounded, import-safe parsing functions and retained CLI JSON/CSV export.
- Added `tools/sync_lang_bytes.py` with dry-run/apply modes and idempotent EN/VI ID synchronization.
- Applied 1,224 verified field updates, added 17 character translation items, and added 8 weapon records.
- Synchronized `data/effects_vi.json`, `data/i18n_vi.json`, and `site/static/js/i18n-vi.js`.
- Post-sync audit: 1,607 exact matches, 0 unambiguous mismatches; 354 ambiguous and 3,947 unmatched values were intentionally left unchanged.

## Verification

- `python tools/validate.py`: 266 records / 64 character files valid.
- `tests/test_lang_bytes_sync.py tests/test_i18n.py`: 24 passed.
- Related schema, catalog, integrity and build tests: 172 passed.
- Remaining accessibility, asset, SEO, guide and editor/server tests: 35 passed.
- Parser CLI re-read both EN and VI source files: 429,779 records each.
- `git diff --check`: passed.

### Browser bundle propagation regression

- Symptom: updated JSON could remain invisible in an already-open browser because the generated HTML reused the same localization script URL.
- RED: `test_i18n_scripts_are_cache_busted_from_content_hash` found 0 fingerprinted script URLs.
- GREEN: the build now derives a 12-character SHA-256 revision from the localization engine, Vietnamese bundle, and effect catalog; all three script URLs carry that revision.
- Browser QA on `http://localhost:8000/dist/characters/alva.html`: `Chạm Vào Băng Kết` rendered in VI mode.
- Browser QA on `http://localhost:8000/dist/weapons/dazzling-sparkles.html`: `Tia Lửa Rực Rỡ`, Vietnamese trait, and Vietnamese effect rendered.
- `tests/test_i18n.py tests/test_build.py tests/test_lang_bytes_sync.py`: 111 passed.
- Fixed fortification lookup precedence: match `tier` first, use `level` only as a legacy fallback. This prevents Tier 2 from reusing Tier 1's Vietnamese text when both have level 2.
- Post-fix `tests/test_i18n.py`: 23 passed; `node --check site/static/js/i18n.js`: passed.

Reusable commands:

```powershell
python -m tools.sync_lang_bytes D:\Project\gfl2_text_data
python -m tools.sync_lang_bytes D:\Project\gfl2_text_data --apply
```

## Self-evaluation

- Accuracy: 5/5 — ID join is deterministic; zero unambiguous mismatches remain.
- Completeness: 4/5 — all safely attributable localization fields were updated; schema-less config payloads and ambiguous/unmatched strings remain deliberately untouched.
- Clarity: 5/5 — dry-run counts and this verification record expose scope and limits.
- Actionability: 5/5 — sync command is reusable and idempotent.
- Conciseness: 4/5 — generated JSON produces a large diff, though it is required to synchronize the canonical and browser bundles.
- Overall: 4.6/5. The remaining high-impact improvement is obtaining protobuf schemas for configuration tables.
