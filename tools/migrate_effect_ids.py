from __future__ import annotations

import argparse
import json
from pathlib import Path

from effects_catalog import canonicalize_effects


ROOT = Path(__file__).resolve().parents[1]
EFFECTS_PATH = ROOT / "data" / "effects_vi.json"
I18N_PATH = ROOT / "data" / "i18n_vi.json"
I18N_JS_PATH = ROOT / "site" / "static" / "js" / "i18n-vi.js"
BACKUP_PATH = ROOT / "scratch" / "migrations" / "effects_vi.before_id_migration.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate effect catalogs from name keys to stable IDs")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    legacy = json.loads(EFFECTS_PATH.read_text(encoding="utf-8-sig"))
    effects = canonicalize_effects(legacy)
    if not args.apply:
        print(f"Would migrate {len(legacy)} name keys to {len(effects)} stable IDs.")
        return 0

    if not BACKUP_PATH.exists():
        BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
        BACKUP_PATH.write_text(json.dumps(legacy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    i18n = json.loads(I18N_PATH.read_text(encoding="utf-8-sig"))
    from tools.editor_core.bundle import stage_i18n_bundle
    from tools.editor_core.transaction import RepositoryTransaction

    tx = RepositoryTransaction(ROOT)
    with tx:
        stage_i18n_bundle(ROOT, tx, i18n_bundle=i18n, effects_data=effects)
        tx.commit()
    print(f"Migrated {len(effects)} effects; backup: {BACKUP_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
