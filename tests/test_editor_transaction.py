from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

import pytest

from tools.editor_core.transaction import (
    RepositoryTransaction,
    TransactionLockError,
    TransactionRollbackError,
)


def test_transaction_atomic_multi_file_success(tmp_path: Path):
    file1 = tmp_path / "a.json"
    file2 = tmp_path / "b.txt"
    file1.write_text('{"val": 1}', encoding="utf-8")
    file2.write_text("hello", encoding="utf-8")

    tx = RepositoryTransaction(tmp_path)
    with tx:
        tx.stage_write(file1, '{"val": 2}\n')
        tx.stage_write(file2, "world\n")
        tx.commit()

    assert file1.read_text(encoding="utf-8") == '{"val": 2}\n'
    assert file2.read_text(encoding="utf-8") == "world\n"


def test_transaction_rollback_on_fault_injection(tmp_path: Path):
    file1 = tmp_path / "a.json"
    file2 = tmp_path / "b.json"
    file1.write_text('{"origin": "a"}', encoding="utf-8")
    file2.write_text('{"origin": "b"}', encoding="utf-8")

    tx = RepositoryTransaction(tmp_path)
    with pytest.raises(TransactionRollbackError):
        with tx:
            tx.stage_write(file1, '{"origin": "a_modified"}\n')
            tx.stage_write(file2, '{"origin": "b_modified"}\n')
            # Inject fault during commit phase (e.g. simulated failure on second replace)
            tx.commit(fail_after_step=1)

    # Both files must remain in their original state
    assert file1.read_text(encoding="utf-8") == '{"origin": "a"}'
    assert file2.read_text(encoding="utf-8") == '{"origin": "b"}'


def test_transaction_lock_timeout(tmp_path: Path):
    tx1 = RepositoryTransaction(tmp_path, lock_timeout=0.1)
    tx2 = RepositoryTransaction(tmp_path, lock_timeout=0.1)

    tx1.acquire_lock()
    try:
        with pytest.raises(TransactionLockError, match="timeout"):
            tx2.acquire_lock()
    finally:
        tx1.release_lock()


def test_transaction_concurrent_updates_no_lost_update(tmp_path: Path):
    # Simulates two concurrent operations updating a shared bundle
    bundle_file = tmp_path / "bundle.json"
    bundle_file.write_text(json.dumps({"effects": {}, "characters": {}}), encoding="utf-8")

    errors: list[Exception] = []

    def update_effects():
        try:
            tx = RepositoryTransaction(tmp_path, lock_timeout=5.0)
            with tx:
                data = json.loads(bundle_file.read_text(encoding="utf-8"))
                time.sleep(0.02)
                data["effects"]["shield"] = {"name": "Khiên"}
                tx.stage_write(bundle_file, json.dumps(data, indent=2) + "\n")
                tx.commit()
        except Exception as exc:
            errors.append(exc)

    def update_characters():
        try:
            tx = RepositoryTransaction(tmp_path, lock_timeout=5.0)
            with tx:
                data = json.loads(bundle_file.read_text(encoding="utf-8"))
                time.sleep(0.02)
                data["characters"]["alva"] = {"name": "Alva"}
                tx.stage_write(bundle_file, json.dumps(data, indent=2) + "\n")
                tx.commit()
        except Exception as exc:
            errors.append(exc)

    t1 = threading.Thread(target=update_effects)
    t2 = threading.Thread(target=update_characters)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert not errors, f"Concurrent transaction errors: {errors}"
    final_data = json.loads(bundle_file.read_text(encoding="utf-8"))
    assert "shield" in final_data["effects"], "Effect update was lost"
    assert "alva" in final_data["characters"], "Character update was lost"
