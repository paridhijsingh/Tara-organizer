# list_desktop.py — List files on the Desktop, with size and date.
# Usage: python3 scripts/list_desktop.py
# Read-only. Moves nothing. Paridhi approves any move first.

import os
from datetime import datetime
from pathlib import Path


def main():
    desktop = Path.home() / "Desktop"
    files = []
    for item in desktop.iterdir():
        if item.is_file():
            stat = item.stat()
            files.append((item.name, stat.st_size / (1024 ** 2), datetime.fromtimestamp(stat.st_mtime).date()))

    print(f"Desktop: {len(files)} files")
    for name, size_mb, modified in sorted(files, key=lambda x: -x[1]):
        print(f"  - {name} — {size_mb:.1f} MB — {modified}")
    total_mb = sum(f[1] for f in files)
    print(f"\nTotal: {total_mb:.1f} MB on Desktop")


if __name__ == "__main__":
    main()