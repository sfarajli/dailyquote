# dailyquota (no systemd)

A small per-user daily usage quota daemon for X sessions (e.g., Arch + Xorg + dwm).

- Tracks elapsed time **per local day**
- When the daily limit is reached, it runs a configured shutdown command (default: `sudo /sbin/poweroff`)
- Provides a CLI to show **remaining time** from the command line

## Quick start

1) Install into your home:
```sh
./scripts/install.sh
```

2) Ensure you can power off non-interactively (choose ONE approach):

### Option A (recommended): sudoers rule (no password) for poweroff
Run `visudo` and add:
```
%sudo ALL=(root) NOPASSWD: /sbin/poweroff
```
Or, more narrowly for a single user:
```
YOURUSER ALL=(root) NOPASSWD: /sbin/poweroff
```

3) Start the daemon from your X startup file (no systemd):
Add this line to `~/.xinitrc` (or your dwm autostart script):
```sh
~/.local/bin/dailyquota-daemon &
```

4) Check remaining time:
```sh
dailyquota status
dailyquota remaining
```

## Configuration

Config path:
- `~/.config/dailyquota/config.conf`

Example:
```
limit_seconds=7200
poll_seconds=5
action_cmd=sudo /sbin/poweroff
grace_seconds=30
warn_seconds=600,300,60
```

## State

State path:
- `~/.local/share/dailyquota/state.json`

## Notes

- Default "usage" is **session wall-clock time** while the daemon runs (idle counts).
- If you want "active time" later, you can add an idle meter; the repo structure keeps this easy.
