# check_drive.py — Print Tara's Drive storage report.
# Usage: python3 scripts/check_drive.py
# Read-only. Deletes nothing. Paridhi approves any cleanup first.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from drive_client import get_storage, get_largest_files


def main():
    used, limit, used_gb, limit_gb, percent, quota = get_storage()
    print(f"Breakdown: {quota}")
    print(f"Drive storage: {used_gb:.1f} GB used of {limit_gb:.1f} GB ({percent:.1f}% full)")
    # Breakdown — add this after get_storage() in drive_client.py returns the full quota dict
    print(f"Free: {limit_gb - used_gb:.1f} GB")
    print("")
    print("Largest files:")
    for file in get_largest_files(10):
       print(f"  - {file['name']} — {file['size_mb']} MB — {file['modified']} — {file['mime_type']} — owner: {file['owner']}")


if __name__ == "__main__":
    main()