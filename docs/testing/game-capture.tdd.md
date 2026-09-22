# Game Capture fallback — TDD evidence

## Scope

Read-only Win32 GDI capture for the running window whose exact title is
`EXILIUM` and whose process is `GF2_Exilium.exe`. The tool does not inject
input and does not update project JSON.

## User journey

- Capture the windowed game when Windows Graphics Capture is unavailable.
- Save the frame and target-window metadata for later skill/effect review.
- Refuse a missing, ambiguous, or wrong-process target.

## RED evidence

Command:

```bat
.venv\Scripts\python.exe -m pytest tests\test_game_capture.py -q --basetemp=scratch\pytest-game-capture-red
```

Result: collection failed with `ModuleNotFoundError: tools.game_capture`, proving
the tests preceded the implementation.

The first live capture also failed inside the filesystem sandbox because the
process could not see the interactive desktop. Running the same read-only
command with desktop permission found the exact target.

## GREEN evidence

```text
5 passed in 0.13s
```

Live target evidence:

```json
{"hwnd": 1769650, "title": "EXILIUM", "process_name": "GF2_Exilium.exe", "rect": [160, 71, 1760, 1000]}
```

After bringing the game to the foreground, the tool produced:

- `scratch/game-capture/capture-20260914-110927.bmp`
- `scratch/game-capture/capture-20260914-110927.json`

Visual inspection confirmed a readable 1600×929 frame of Voymastina's overview.
The visible skill levels were `1 / 2 / 2 / 2 / 1`.

## Test specification

| Guarantee | Test | Result |
|---|---|---|
| Exact title and process select one window | `test_select_unique_window_requires_exact_title_and_process` | PASS |
| Missing/ambiguous targets are rejected | `test_select_unique_window_rejects_missing_or_ambiguous_target` | PASS |
| BMP output has a valid top-down 32-bit header | `test_encode_bmp_writes_valid_top_down_32_bit_header` | PASS |
| Invalid pixel length is rejected | `test_encode_bmp_rejects_wrong_pixel_count` | PASS |
| Image and metadata artifacts are paired | `test_write_capture_artifacts_writes_image_and_metadata` | PASS |

## Known limitation

The game did not react to synthetic clicks sent by Computer Use at three
visually verified coordinates. Automated navigation is therefore not claimed.
Current safe workflow: user performs the game click; the capture tool records
the resulting skill/effect panel for review.

