# list_labels.py — List Tara's Gmail labels, read-only.
# Usage: python list_labels.py
# Changes nothing. Paridhi decides which labels to combine / clean.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials


def main():
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().labels().list(userId="me").execute()
    labels = result.get("labels", [])

    for label in labels:
        print(f"{label['name']} — {label.get('type', '')} ({label['id']})")


if __name__ == "__main__":
    main()
