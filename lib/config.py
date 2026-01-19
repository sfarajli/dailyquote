from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, List

def _parse_kv(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out

def _parse_int(s: str, default: int) -> int:
    try:
        return int(s)
    except Exception:
        return default

def _parse_warn(s: str) -> List[int]:
    # comma-separated seconds
    vals: List[int] = []
    for part in (s or "").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            vals.append(int(part))
        except Exception:
            pass
    # unique, descending
    return sorted(set(vals), reverse=True)

@dataclass(frozen=True)
class Config:
    limit_seconds: int = 7200
    poll_seconds: int = 5
    action_cmd: str = "/sbin/poweroff"
    grace_seconds: int = 30
    warn_seconds: List[int] = None  # type: ignore

    @staticmethod
    def defaults() -> "Config":
        return Config(warn_seconds=[600, 300, 60])

    @staticmethod
    def load(path: Path) -> "Config":
        cfg = Config.defaults()
        if not path.exists():
            return cfg
        d = _parse_kv(path.read_text(encoding="utf-8"))
        limit = _parse_int(d.get("limit_seconds", str(cfg.limit_seconds)), cfg.limit_seconds)
        poll = max(1, _parse_int(d.get("poll_seconds", str(cfg.poll_seconds)), cfg.poll_seconds))
        action = d.get("action_cmd", cfg.action_cmd)
        grace = max(0, _parse_int(d.get("grace_seconds", str(cfg.grace_seconds)), cfg.grace_seconds))
        warn = _parse_warn(d.get("warn_seconds", ",".join(map(str, cfg.warn_seconds or []))))
        return Config(
            limit_seconds=limit,
            poll_seconds=poll,
            action_cmd=action,
            grace_seconds=grace,
            warn_seconds=warn,
        )
