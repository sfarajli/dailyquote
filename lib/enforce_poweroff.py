from __future__ import annotations
import subprocess

def run_poweroff(action_cmd: str) -> int:
    # shell=True keeps config simple; command should be controlled by the user.
    # returns process return code.
    p = subprocess.run(action_cmd, shell=True)
    return int(p.returncode)
