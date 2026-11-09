#!/usr/bin/env bash
# Install or remove a macOS LaunchAgent that regenerates NEXT.md every 10 minutes.
#
#   bash scripts/frontier-timer.sh install
#   bash scripts/frontier-timer.sh uninstall
#
# The job runs vault/scripts/frontier.py with no folder argument, so it covers
# every folder listed under frontier_folders: in shared/config.yml. Add or
# remove a folder there; the job itself doesn't change. Paths are worked out
# here at install time, so nothing machine-specific is committed.
set -euo pipefail

LABEL="com.ai-layer.frontier"
INTERVAL=600
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$REPO_ROOT/vault/scripts/frontier.py"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/ai-layer-frontier.log"
DOMAIN="gui/$(id -u)"

install() {
  [[ -f "$SCRIPT" ]] || { echo "frontier-timer: $SCRIPT not found" >&2; exit 1; }
  grep -q '^frontier_folders:' "$REPO_ROOT/shared/config.yml" 2>/dev/null \
    || echo "frontier-timer: warning: no frontier_folders: in shared/config.yml yet, so each run will exit with an error until it's added" >&2
  mkdir -p "$(dirname "$PLIST")" "$(dirname "$LOG")"
  # The list itself goes nowhere (it's in each NEXT.md); only errors are logged.
  cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$SCRIPT</string>
  </array>
  <key>StartInterval</key>
  <integer>$INTERVAL</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/dev/null</string>
  <key>StandardErrorPath</key>
  <string>$LOG</string>
</dict>
</plist>
EOF
  launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
  launchctl bootstrap "$DOMAIN" "$PLIST"
  echo "frontier-timer: installed $LABEL (every ${INTERVAL}s). Errors go to $LOG"
}

uninstall() {
  launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
  rm -f "$PLIST"
  echo "frontier-timer: removed $LABEL"
}

case "${1:-}" in
  install) install ;;
  uninstall) uninstall ;;
  *) echo "usage: $0 install|uninstall" >&2; exit 2 ;;
esac
