from __future__ import annotations
import json, os, time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

def today_local() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())

def now_epoch() -> int:
    return int(time.time())

def _atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(data, encoding="utf-8")
    os.replace(tmp, path)

@dataclass
class State:
    date: str
    used_seconds: int
    last_ts: int
    triggered: bool

    @staticmethod
    def fresh() -> "State":
        ts = now_epoch()
        return State(date=today_local(), used_seconds=0, last_ts=ts, triggered=False)

    @staticmethod
    def load(path: Path) -> "State":
        if not path.exists():
            return State.fresh()
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
            return State(
                date=str(obj.get("date") or today_local()),
                used_seconds=int(obj.get("used_seconds") or 0),
                last_ts=int(obj.get("last_ts") or now_epoch()),
                triggered=bool(obj.get("triggered") or False),
            )
        except Exception:
            return State.fresh()

    def save(self, path: Path) -> None:
        _atomic_write(path, json.dumps({
            "date": self.date,
            "used_seconds": int(self.used_seconds),
            "last_ts": int(self.last_ts),
            "triggered": bool(self.triggered),
        }, indent=2) + "\n")

def rollover_if_needed(st: State) -> None:
    t = today_local()
    if st.date != t:
        st.date = t
        st.used_seconds = 0
        st.last_ts = now_epoch()
        st.triggered = False

def clamp_delta(delta: int, max_delta: int) -> int:
    if delta < 0:
        return 0
    if delta > max_delta:
        return max_delta
    return delta
