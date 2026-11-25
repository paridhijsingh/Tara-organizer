# check_gmail_size.py — List the largest Gmail messages with attachments.
# Usage: python3 scripts/check_gmail_size.py
# Read-only. Deletes nothing. Paridhi approves any cleanup first.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials


def main():
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().messages().list(
        userId="me", q="has:attachment larger:5M", maxResults=10
    ).execute()
    messages = result.get("messages", [])

    if not messages:
        print("No messages with attachments larger than 5 MB found.")
        return

    print("Largest Gmail messages with attachments (over 5 MB):")
    for message in messages:
        full = service.users().messages().get(
            userId="me", id=message["id"], format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        ).execute()
        headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
        size_mb = round(int(full.get("sizeEstimate", 0)) / (1024 ** 2), 1)
        print(f"  - {headers.get('From', '')}: {headers.get('Subject', '')} — {size_mb} MB — {headers.get('Date', '')[:16]}")


if __name__ == "__main__":
    main()