from __future__ import annotations
import os
from pathlib import Path
import fcntl

class LockError(RuntimeError):
    pass

class LockFile:
    def __init__(self, path: Path):
        self.path = path
        self.fd = None

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = open(self.path, "a+")
        try:
            fcntl.flock(self.fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise LockError(f"Lock is held: {self.path}")
        # record pid for debugging
        self.fd.seek(0)
        self.fd.truncate()
        self.fd.write(str(os.getpid()) + "\n")
        self.fd.flush()

    def release(self) -> None:
        if not self.fd:
            return
        try:
            fcntl.flock(self.fd.fileno(), fcntl.LOCK_UN)
        finally:
            self.fd.close()
            self.fd = None
