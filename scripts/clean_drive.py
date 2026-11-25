# clean_drive.py — Trash the one approved Drive file.
# APPROVED by Paridhi Nov 25, 2026: SoCal Consortium for DS_2024_best.mov only.
# Trash in Drive = recoverable 30 days, not permanent delete.
# Usage: python3 scripts/clean_drive.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials
from drive_client import get_storage

APPROVED_FILE = "SoCal Consortium for DS_2024_best.mov"


def main():
    service = build("drive", "v3", credentials=get_credentials())

    result = service.files().list(
        q=f"name = '{APPROVED_FILE}'",
        fields="files(id,name,size)",
    ).execute()
    files = result.get("files", [])

    if not files:
        print(f"Not found: {APPROVED_FILE}")
        return

    if len(files) > 1:
        print(f"Found {len(files)} files with that name — stopping, Paridhi must pick one.")
        return

    file = files[0]
    size_mb = round(int(file.get("size", 0)) / (1024 ** 2), 1)
    print(f"Trashing: {file['name']} — {size_mb} MB")

    service.files().update(
        fileId=file["id"], body={"trashed": True}
    ).execute()
    print("Moved to Trash (recoverable 30 days).")

    used, limit, used_gb, limit_gb, percent = get_storage()
    print(f"Drive storage now: {used_gb:.1f} GB used of {limit_gb:.1f} GB ({percent:.1f}% full)")


if __name__ == "__main__":
    main()