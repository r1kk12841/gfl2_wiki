from __future__ import annotations

import copy
import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any

from tools.effects_catalog import canonicalize_effects


ALLOWED_TYPES = {"buff", "debuff", "effect"}


class EffectValidationError(ValueError):
    pass


class EffectStore:
    """Read and safely update the ID-keyed Vietnamese effects catalog."""

    def __init__(self, effects_path: Path, i18n_path: Path, i18n_js_path: Path | None = None):
        self.effects_path = Path(effects_path)
        self.i18n_path = Path(i18n_path)
        self.i18n_js_path = Path(i18n_js_path) if i18n_js_path else None
        self._lock = threading.Lock()

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            raise EffectValidationError(f"Không thể đọc {path.name}: {exc}") from exc
        if not isinstance(data, dict):
            raise EffectValidationError(f"{path.name} phải chứa JSON object.")
        return data

    @staticmethod
    def _canonical_entries(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return canonicalize_effects(data)

    def list_effects(self) -> list[dict[str, Any]]:
        data = self._read_json(self.effects_path)
        canonical = self._canonical_entries(data)
        referenced_by: dict[str, list[dict[str, str]]] = {effect_id: [] for effect_id in canonical}
        for source_id, entry in canonical.items():
            for target_id in entry.get("sub_effect_ids", []):
                if target_id in referenced_by:
                    referenced_by[target_id].append(
                        {"id": source_id, "name_en": str(entry["name_en"]), "name": str(entry.get("name", entry["name_en"]))}
                    )

        rows = []
        for effect_id, entry in canonical.items():
            row = copy.deepcopy(entry)
            row["referenced_by"] = sorted(
                referenced_by[effect_id], key=lambda item: item["name_en"].casefold()
            )
            rows.append(row)
        return sorted(rows, key=lambda item: item["name_en"].casefold())

    def update_effect(self, effect_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            effects = self._read_json(self.effects_path)
            i18n = self._read_json(self.i18n_path)
            canonical = self._canonical_entries(effects)
            if effect_id not in canonical:
                raise EffectValidationError(f"Hiệu ứng ID '{effect_id}' không tồn tại.")

            new_name = str(changes.get("name", "")).strip()
            new_desc = str(changes.get("desc", "")).strip()
            new_type = str(changes.get("type", "")).strip().lower()
            if not new_name:
                raise EffectValidationError("Tên tiếng Việt không được để trống.")
            if not new_desc:
                raise EffectValidationError("Mô tả tiếng Việt không được để trống.")
            if new_type not in ALLOWED_TYPES:
                raise EffectValidationError("Loại hiệu ứng phải là buff, debuff hoặc effect.")

            updated_entry = copy.deepcopy(canonical[effect_id])
            updated_entry.update({"name": new_name, "desc": new_desc, "type": new_type})
            updated_effects = copy.deepcopy(canonical)
            updated_effects[effect_id] = updated_entry
            renamed_reference_sources = {
                source_id for source_id, entry in updated_effects.items()
                if effect_id in entry.get("sub_effect_ids", [])
            }

            updated_i18n = copy.deepcopy(i18n)
            updated_i18n["effects"] = updated_effects
            self._write_outputs(updated_effects, updated_i18n)
            return {
                "effect": next(row for row in self.list_effects() if row["id"] == effect_id),
                "preserved_references": len(renamed_reference_sources),
            }

    @staticmethod
    def _json_text(data: dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"

    @staticmethod
    def _stage(path: Path, content: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise
        return temp_path

    def _write_outputs(self, effects: dict[str, Any], i18n: dict[str, Any]) -> None:
        outputs = [
            (self.effects_path, self._json_text(effects)),
            (self.i18n_path, self._json_text(i18n)),
        ]
        if self.i18n_js_path:
            outputs.append(
                (
                    self.i18n_js_path,
                    "// Auto-generated Vietnamese Localization Bundle for GFL2: Exilium Wiki\n"
                    f"window.GFL2_I18N_VI = {json.dumps(i18n, ensure_ascii=False, indent=2)};\n",
                )
            )

        staged = [(path, self._stage(path, content)) for path, content in outputs]
        originals = {path: path.read_bytes() if path.exists() else None for path, _ in staged}
        replaced: list[Path] = []
        try:
            for path, temp_path in staged:
                os.replace(temp_path, path)
                replaced.append(path)
        except Exception:
            for path in reversed(replaced):
                original = originals[path]
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    rollback = self._stage(path, original.decode("utf-8-sig"))
                    os.replace(rollback, path)
            raise
        finally:
            for _, temp_path in staged:
                temp_path.unlink(missing_ok=True)
