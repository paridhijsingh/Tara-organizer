# tidy_desktop.py — Tidy the Desktop, approved groups only.
# APPROVED by Paridhi Nov 25, 2026:
#   1. Screenshots -> Desktop/Screenshots/
#   2. Screen Recordings -> Desktop/Screen Recordings/
#   3. Delete: Cursor-darwin-universal.dmg + ~$*.docx lock files (to Trash, recoverable)
# Usage: python3 scripts/tidy_desktop.py
# Moves nothing else. Leaves PDFs, zips, resume alone.

import shutil
from pathlib import Path


def main():
    desktop = Path.home() / "Desktop"
    trash = Path.home() / ".Trash"

    screenshots_dir = desktop / "Screenshots"
    recordings_dir = desktop / "Screen Recordings"
    screenshots_dir.mkdir(exist_ok=True)
    recordings_dir.mkdir(exist_ok=True)

    moved_shots = moved_recs = deleted = 0
    for item in list(desktop.iterdir()):
        if not item.is_file():
            continue
        name = item.name
        if name.startswith("Screenshot ") or name.startswith("Simulator Screenshot"):
            shutil.move(str(item), str(screenshots_dir / name))
            moved_shots += 1
        elif name.startswith("Screen Recording "):
            shutil.move(str(item), str(recordings_dir / name))
            moved_recs += 1
        elif name == "Cursor-darwin-universal.dmg" or name.startswith("~$"):
            shutil.move(str(item), str(trash / name))
            print(f"Moved to Trash: {name}")
            deleted += 1

    print(f"\nMoved {moved_shots} screenshots -> Desktop/Screenshots/")
    print(f"Moved {moved_recs} screen recordings -> Desktop/Screen Recordings/")
    print(f"Moved {deleted} files to Trash (Cursor .dmg + Word lock files)")


if __name__ == "__main__":
    main()