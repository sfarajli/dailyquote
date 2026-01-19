from __future__ import annotations
import os
from pathlib import Path

APP = "dailyquota"

def xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))

def xdg_data_home() -> Path:
    return Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share")))

def xdg_state_home() -> Path:
    return Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state")))

def config_path() -> Path:
    return xdg_config_home() / APP / "config.conf"

def state_path() -> Path:
    return xdg_data_home() / APP / "state.json"

def runtime_dir() -> Path:
    return xdg_state_home() / APP

def lock_path() -> Path:
    return runtime_dir() / "daemon.lock"

def pid_path() -> Path:
    return runtime_dir() / "daemon.pid"
