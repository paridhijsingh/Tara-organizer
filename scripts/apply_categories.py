# apply_categories.py — Apply Tara's suggested categories to unread mail.
# APPROVED by Paridhi Nov 22, 2026, for the 10 mails in the last propose run.
# Moves 8 mails to Promotions / Updates, leaves 2 Important mails alone.
# Never deletes, archives, or marks mail as read.
# Usage: python apply_categories.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials
from categorize import suggest_category

CATEGORY_LABELS = {
    "Promotions": "CATEGORY_PROMOTIONS",
    "Social": "CATEGORY_SOCIAL",
    "Updates": "CATEGORY_UPDATES",
}


def main():
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().messages().list(userId="me", q="is:unread", maxResults=10).execute()
    messages = result.get("messages", [])

    for message in messages:
        full = service.users().messages().get(
            userId="me", id=message["id"], format="metadata",
            metadataHeaders=["From", "Subject"],
        ).execute()
        headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
        sender = headers.get("From", "")
        subject = headers.get("Subject", "")
        snippet = full.get("snippet", "")
        category = suggest_category(sender, subject, snippet)

        if category in CATEGORY_LABELS:
            service.users().messages().modify(
                userId="me", id=message["id"],
                body={"addLabelIds": [CATEGORY_LABELS[category]]},
            ).execute()
            print(f"Moved to {category}: {sender}: {subject}")
        else:
            print(f"Left alone ({category}): {sender}: {subject}")


if __name__ == "__main__":
    main()
