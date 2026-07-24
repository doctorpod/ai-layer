#!/usr/bin/env python3
"""
Check a downloaded image's dimensions/filesize and resize in place if needed.
Used by ingest.md Step 2b after downloading an image from Wikimedia Commons.

Usage:
  python3 normalize-image.py <path-to-image>

Behaviour:
  - Reads pixel dimensions via `sips -g pixelHeight -g pixelWidth`.
  - If either dimension is >1200px or the file is >500KB, resizes the
    longest edge to 1200px via `sips -Z 1200` (macOS only).
  - Prints one line reporting what happened.
"""

import subprocess
import sys
from pathlib import Path

MAX_DIMENSION = 1200
MAX_BYTES = 500 * 1024


def get_dimensions(path):
    result = subprocess.run(
        ['sips', '-g', 'pixelHeight', '-g', 'pixelWidth', str(path)],
        capture_output=True, text=True, check=True,
    )
    height = width = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith('pixelHeight:'):
            height = int(line.split(':')[1].strip())
        elif line.startswith('pixelWidth:'):
            width = int(line.split(':')[1].strip())
    if height is None or width is None:
        raise RuntimeError(f'Could not parse sips output:\n{result.stdout}')
    return width, height


def main():
    if len(sys.argv) != 2:
        print('Usage: normalize-image.py <path-to-image>', file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f'Error: file not found: {path}', file=sys.stderr)
        sys.exit(1)

    width, height = get_dimensions(path)
    size_bytes = path.stat().st_size

    if width <= MAX_DIMENSION and height <= MAX_DIMENSION and size_bytes <= MAX_BYTES:
        print(f'{path.name}: {width}x{height}, {size_bytes // 1024}KB — within limits, no resize needed')
        return

    subprocess.run(['sips', '-Z', str(MAX_DIMENSION), str(path)], capture_output=True, text=True, check=True)
    new_width, new_height = get_dimensions(path)
    new_size = path.stat().st_size
    print(f'{path.name}: resized {width}x{height} ({size_bytes // 1024}KB) -> {new_width}x{new_height} ({new_size // 1024}KB)')


if __name__ == '__main__':
    main()
