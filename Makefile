PREFIX ?= $(HOME)/.local
BINDIR ?= $(PREFIX)/bin
DATADIR ?= $(PREFIX)/share/dailyquota
CFGDIR ?= $(HOME)/.config/dailyquota
CFGFILE := $(CFGDIR)/config.conf

PYTHON ?= python3

# Files in repo
LIBSRC := lib/paths.py lib/config.py lib/state.py lib/timefmt.py lib/lock.py lib/enforce_poweroff.py
CLISRC := dailyquota
DAEMONSRC := dailyquota-daemon

# Installed python entrypoints (copied)
CLI_DST := $(DATADIR)/dailyquota.py
DAEMON_DST := $(DATADIR)/dailyquota_daemon.py
LIBDSTDIR := $(DATADIR)/lib

# Wrapper scripts installed into ~/.local/bin
WRAP_CLI := $(BINDIR)/dailyquota
WRAP_DAEMON := $(BINDIR)/dailyquota-daemon

.PHONY: all install uninstall config dirs check

all:
	@echo "Targets: install, uninstall"

dirs:
	mkdir -p "$(BINDIR)" "$(DATADIR)" "$(LIBDSTDIR)" "$(CFGDIR)"

check:
	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "Missing $(PYTHON)"; exit 1)

install: check dirs
	# Copy python entrypoints into data dir
	install -m 0644 "$(CLISRC)" "$(CLI_DST)"
	install -m 0644 "$(DAEMONSRC)" "$(DAEMON_DST)"
	# Copy libs
	install -m 0644 $(LIBSRC) "$(LIBDSTDIR)/"

	# Write wrappers into ~/.local/bin
	@printf '%s\n' '#!/bin/sh' \
		'exec env PYTHONPATH="$$HOME/.local/share/dailyquota" $(PYTHON) "$$HOME/.local/share/dailyquota/dailyquota.py" "$$@"' \
		> "$(WRAP_CLI)"
	chmod 0755 "$(WRAP_CLI)"

	@printf '%s\n' '#!/bin/sh' \
		'exec env PYTHONPATH="$$HOME/.local/share/dailyquota" $(PYTHON) "$$HOME/.local/share/dailyquota/dailyquota_daemon.py" "$$@"' \
		> "$(WRAP_DAEMON)"
	chmod 0755 "$(WRAP_DAEMON)"

	# Install default config if missing
	@if [ ! -f "$(CFGFILE)" ]; then \
		printf '%s\n' \
			'# dailyquota configuration' \
			'limit_seconds=7200' \
			'poll_seconds=5' \
			'action_cmd=sudo /sbin/poweroff' \
			'grace_seconds=30' \
			'warn_seconds=600,300,60' \
			> "$(CFGFILE)"; \
		echo "Installed default config: $(CFGFILE)"; \
	else \
		echo "Config exists: $(CFGFILE)"; \
	fi

	@echo ""
	@echo "Installed:"
	@echo "  $(WRAP_CLI)"
	@echo "  $(WRAP_DAEMON)"
	@echo ""
	@echo "Start the daemon from your X startup (no systemd):"
	@echo "  $(WRAP_DAEMON) &"
	@echo ""
	@echo "CLI:"
	@echo "  dailyquota status"
	@echo "  dailyquota remaining"

uninstall:
	rm -f "$(WRAP_CLI)" "$(WRAP_DAEMON)"
	rm -rf "$(DATADIR)"
	@echo "Removed binaries + data dir. Config kept at: $(CFGFILE)"
