from __future__ import annotations

import os
import shutil
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl


class TransactionLockError(TimeoutError):
    pass


class TransactionRollbackError(RuntimeError):
    pass


_global_lock = threading.RLock()
_locks_by_root: dict[Path, threading.RLock] = {}


def _get_root_lock(root: Path) -> threading.RLock:
    with _global_lock:
        resolved = root.resolve()
        if resolved not in _locks_by_root:
            _locks_by_root[resolved] = threading.RLock()
        return _locks_by_root[resolved]


class RepositoryTransaction:
    """Provides atomic multi-file staging, rollback, and inter-process locking."""

    def __init__(self, root: Path, lock_timeout: float = 10.0):
        self.root = Path(root).resolve()
        self.lock_timeout = lock_timeout
        self.lock_file_path = self.root / "data" / ".editor-write.lock"
        self._root_rlock = _get_root_lock(self.root)
        self._lock_file_handle: Any = None
        self._in_context = False
        self._is_locked = False
        self._staged_files: list[tuple[Path, Path]] = []  # (target_path, temp_path)

    def acquire_lock(self) -> None:
        if self._is_locked:
            return

        # 1. Acquire thread RLock with timeout
        start_time = time.monotonic()
        acquired_thread_lock = self._root_rlock.acquire(timeout=self.lock_timeout)
        if not acquired_thread_lock:
            raise TransactionLockError(f"Giao dịch timeout khi chờ luồng khác ({self.lock_timeout}s)")

        try:
            # 2. Acquire filesystem lock with timeout
            self.lock_file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.lock_file_path.exists():
                self.lock_file_path.touch(exist_ok=True)

            self._lock_file_handle = open(self.lock_file_path, "r+b")
            fd = self._lock_file_handle.fileno()

            while True:
                try:
                    if sys.platform == "win32":
                        self._lock_file_handle.seek(0)
                        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    else:
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self._is_locked = True
                    return
                except (OSError, IOError):
                    elapsed = time.monotonic() - start_time
                    if elapsed >= self.lock_timeout:
                        raise TransactionLockError(
                            f"Giao dịch timeout khi chờ lockfile {self.lock_file_path.name} ({self.lock_timeout}s)"
                        )
                    time.sleep(0.05)
        except Exception:
            if self._lock_file_handle:
                try:
                    self._lock_file_handle.close()
                except Exception:
                    pass
                self._lock_file_handle = None
            self._root_rlock.release()
            raise

    def release_lock(self) -> None:
        if not self._is_locked:
            return

        try:
            if self._lock_file_handle:
                fd = self._lock_file_handle.fileno()
                try:
                    if sys.platform == "win32":
                        self._lock_file_handle.seek(0)
                        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                    else:
                        fcntl.flock(fd, fcntl.LOCK_UN)
                except Exception:
                    pass
                finally:
                    self._lock_file_handle.close()
                    self._lock_file_handle = None
        finally:
            self._is_locked = False
            self._root_rlock.release()

    def __enter__(self) -> RepositoryTransaction:
        self.acquire_lock()
        self._in_context = True
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            self.discard()
        finally:
            self.release_lock()
            self._in_context = False

    def stage_write(self, target: Path, content: str | bytes) -> Path:
        """Writes content to a staged temporary file on the same filesystem."""
        target_path = Path(target).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        fd, temp_name = tempfile.mkstemp(
            prefix=f".{target_path.name}.",
            suffix=".tmp",
            dir=target_path.parent,
        )
        temp_path = Path(temp_name)
        try:
            if isinstance(content, str):
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)
                    f.flush()
                    os.fsync(f.fileno())
            else:
                with os.fdopen(fd, "wb") as f:
                    f.write(content)
                    f.flush()
                    os.fsync(f.fileno())
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise

        self._staged_files.append((target_path, temp_path))
        return temp_path

    def commit(self, fail_after_step: int | None = None) -> None:
        """Atomically applies all staged files. Rolls back everything if any step fails."""
        if not self._staged_files:
            return

        applied_backups: list[tuple[Path, Path | None]] = []  # (target, backup_path_if_existed)

        try:
            step = 0
            for target_path, temp_path in self._staged_files:
                if fail_after_step is not None and step >= fail_after_step:
                    raise IOError(f"Fault injection triggered after step {step}")

                backup_path = None
                if target_path.exists():
                    backup_fd, backup_name = tempfile.mkstemp(
                        prefix=f".{target_path.name}.backup.",
                        suffix=".tmp",
                        dir=target_path.parent,
                    )
                    os.close(backup_fd)
                    backup_path = Path(backup_name)
                    shutil.copy2(target_path, backup_path)

                # Atomically replace target with temp
                os.replace(temp_path, target_path)
                applied_backups.append((target_path, backup_path))
                step += 1

            # All succeeded: clean up backups
            for _, backup_path in applied_backups:
                if backup_path and backup_path.exists():
                    backup_path.unlink(missing_ok=True)
            self._staged_files.clear()

        except Exception as exc:
            # Rollback any applied targets
            rollback_errors: list[str] = []
            for target_path, backup_path in reversed(applied_backups):
                try:
                    if backup_path and backup_path.exists():
                        os.replace(backup_path, target_path)
                    elif target_path.exists():
                        target_path.unlink(missing_ok=True)
                except Exception as rb_exc:
                    rollback_errors.append(f"Không thể rollback {target_path}: {rb_exc}")

            self.discard()
            error_msg = f"Transaction commit thất bại, đã rollback: {exc}"
            if rollback_errors:
                error_msg += " (Cảnh báo: " + "; ".join(rollback_errors) + ")"
            raise TransactionRollbackError(error_msg) from exc

    def discard(self) -> None:
        """Cleans up any uncommitted staged files."""
        for _, temp_path in self._staged_files:
            try:
                if temp_path.exists():
                    temp_path.unlink(missing_ok=True)
            except Exception:
                pass
        self._staged_files.clear()
