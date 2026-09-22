from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.editor_core.transaction import RepositoryTransaction


def render_i18n_vi_js(bundle_dict: dict[str, Any]) -> str:
    """Renders the standard client-side JavaScript bundle for Vietnamese localization."""
    json_text = json.dumps(bundle_dict, ensure_ascii=False, indent=2)
    return (
        "// Auto-generated Vietnamese Localization Bundle for GFL2: Exilium Wiki\n"
        f"window.GFL2_I18N_VI = {json_text};\n"
    )


def read_json_dict(path: Path) -> dict[str, Any]:
    """Reads a JSON file that must contain a root object/dictionary."""
    if not path.exists():
        raise FileNotFoundError(f"Tệp JSON không tồn tại: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise ValueError(f"Không thể đọc JSON {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} phải là JSON Object.")
    return data


def stage_i18n_bundle(
    repo_root: Path,
    tx: RepositoryTransaction,
    i18n_bundle: dict[str, Any],
    effects_data: dict[str, Any] | None = None,
) -> None:
    """
    Stages synchronization across:
      - data/effects_vi.json (optional if effects_data provided)
      - data/i18n_vi.json
      - site/static/js/i18n-vi.js
    """
    repo = Path(repo_root)
    if effects_data is not None:
        effects_path = repo / "data" / "effects_vi.json"
        effects_text = json.dumps(effects_data, ensure_ascii=False, indent=2) + "\n"
        tx.stage_write(effects_path, effects_text)
        i18n_bundle["effects"] = effects_data

    i18n_path = repo / "data" / "i18n_vi.json"
    i18n_text = json.dumps(i18n_bundle, ensure_ascii=False, indent=2) + "\n"
    tx.stage_write(i18n_path, i18n_text)

    js_path = repo / "site" / "static" / "js" / "i18n-vi.js"
    # Ensure parent dir exists if needed in tests
    js_text = render_i18n_vi_js(i18n_bundle)
    tx.stage_write(js_path, js_text)
