#!/usr/bin/env python3
"""
fetch-read: Print the last user message from the active chat log.

The active log is the lexicographically greatest .md file in _AI/chats/.
Prints everything after the last user heading (e.g. '### Andy') to stdout.

Usage:
    python3 _AI/core/scripts/fetch-read.py
"""

import os
import sys
import re
from pathlib import Path

# The heading name used for user messages in chat log files (e.g. '### Andy').
# Change this to match your own chat log convention.
USER_NAME = "Andy"


def _find_vault_root():
    """Walk up from this file to find the vault root (directory containing CLAUDE.md)."""
    d = Path(__file__).parent
    while d != d.parent:
        if (d / 'CLAUDE.md').exists():
            return str(d)
        d = d.parent
    raise RuntimeError(f"Could not find vault root — no CLAUDE.md found above {__file__}")


VAULT_ROOT = _find_vault_root()
CHAT_DIR = os.path.join(VAULT_ROOT, "_AI", "chats")


def find_active_log():
    files = sorted([f for f in os.listdir(CHAT_DIR) if f.endswith(".md")])
    if not files:
        print("No chat log files found.", file=sys.stderr)
        sys.exit(1)
    return os.path.join(CHAT_DIR, files[-1])


def extract_last_user_message(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(rf"^#{{1,3}} {re.escape(USER_NAME)}\b", re.MULTILINE)
    matches = list(pattern.finditer(content))

    if not matches:
        print(f"No user messages found in {path}", file=sys.stderr)
        sys.exit(1)

    last_match = matches[-1]
    message = content[last_match.start():]
    return path, message


def main():
    log_path = find_active_log()
    log_path, message = extract_last_user_message(log_path)
    print(f"[Active log: {os.path.relpath(log_path, VAULT_ROOT)}]\n")
    print(message)


if __name__ == "__main__":
    main()
