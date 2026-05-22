#!/usr/bin/env python3
"""
fetch-write: Append a response to the active chat log.

The active log is the lexicographically greatest .md file in _AI/chats/.
If that file's date does not match today, a new dated file is created first.

The response is read from a file path passed as the first argument, or from
stdin if no argument is given.

If --heading is provided, fetch-write injects the heading and current timestamp
at the top of the response automatically. The response file then contains only
the body. If --heading is omitted, the response must include the heading itself.

Usage:
    python3 _AI/core/scripts/fetch-write.py /path/to/response.md --heading "Claude Cowork (Sonnet 4.6)"
    python3 _AI/core/scripts/fetch-write.py /path/to/response.md  # response includes heading
    echo "body text" | python3 _AI/core/scripts/fetch-write.py --heading "Claude Cowork (Sonnet 4.6)"

Example workflow (heading injected by script):
    cat > /tmp/response.md << 'RESPONSE'
    Your response body here...
    RESPONSE

    python3 _AI/core/scripts/fetch-write.py /tmp/response.md --heading "Claude Cowork (Sonnet 4.6)"
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


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


PREFIX = "chat-"


def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def filename_for(date_str):
    return f"{PREFIX}{date_str}.md"


def date_from_filename(filename):
    """Extract YYYY-MM-DD from 'chat-YYYY-MM-DD.md'."""
    name = filename.replace(".md", "")
    if name.startswith(PREFIX):
        return name[len(PREFIX):]
    return name  # fallback for unexpected formats


def find_or_create_active_log():
    today = get_today()
    files = sorted([f for f in os.listdir(CHAT_DIR) if f.endswith(".md")])

    if files:
        latest = files[-1]
        latest_date = date_from_filename(latest)
        if latest_date == today:
            return os.path.join(CHAT_DIR, latest), False
        else:
            # Today is newer — create a new file
            new_name = filename_for(today)
            new_path = os.path.join(CHAT_DIR, new_name)
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(f"# Chat log — {today}\n")
            return new_path, True
    else:
        # No files at all — create today's
        new_name = filename_for(today)
        new_path = os.path.join(CHAT_DIR, new_name)
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(f"# Chat log — {today}\n")
        return new_path, True


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('response_file', nargs='?', default=None,
                   help='Path to response file (reads stdin if omitted)')
    p.add_argument('--heading', default=None,
                   help='AI heading text, e.g. "Claude Cowork (Sonnet 4.6)". '
                        'If provided, heading and timestamp are injected automatically.')
    return p.parse_args()


def read_response(response_file):
    if response_file:
        with open(response_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return sys.stdin.read()


def main():
    args = parse_args()
    log_path, created = find_or_create_active_log()
    response = read_response(args.response_file)

    if not response.strip():
        print("Empty response — nothing written.", file=sys.stderr)
        sys.exit(1)

    if args.heading:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        response = f"## {args.heading}\n{timestamp}\n\n{response.lstrip()}"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n")
        f.write(response.rstrip("\n"))
        f.write("\n")

    action = "Created" if created else "Appended to"
    print(f"{action}: {os.path.relpath(log_path, VAULT_ROOT)}")


if __name__ == "__main__":
    main()
