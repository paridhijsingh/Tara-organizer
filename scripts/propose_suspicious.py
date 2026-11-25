# propose_suspicious.py — Show Tara's suspicious-mail flags for recent unread mail.
# Usage: python3 scripts/propose_suspicious.py
# Read-only. Moves nothing. Paridhi reviews first, approves, then Tara files to Spam.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials
from suspicious import is_suspicious


def main():
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().messages().list(
        userId="me", q="is:unread", maxResults=20
    ).execute()
    messages = result.get("messages", [])

    if not messages:
        print("No unread mail found.")
        return

    flagged = 0
    for message in messages:
        full = service.users().messages().get(
            userId="me", id=message["id"], format="metadata",
            metadataHeaders=["From", "Subject"],
        ).execute()
        headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
        sender = headers.get("From", "")
        subject = headers.get("Subject", "")
        snippet = full.get("snippet", "")
        if is_suspicious(sender, subject, snippet):
            flagged += 1
            print(f"[SUSPICIOUS] {sender}: {subject}")
        else:
            print(f"[OK] {sender}: {subject}")

    print("")
    print(f"Summary: {flagged} suspicious out of {len(messages)} unread")
    check_spam(service)

def check_spam(service):
    """List mail in Spam and flag any that looks legitimate."""
    print("")
    print("--- Spam folder check ---")
    result = service.users().messages().list(
        userId="me", labelIds=["SPAM"], maxResults=10
    ).execute()
    messages = result.get("messages", [])

    if not messages:
        print("Spam folder is empty.")
        return

    for message in messages:
        full = service.users().messages().get(
            userId="me", id=message["id"], format="metadata",
            metadataHeaders=["From", "Subject"],
        ).execute()
        headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
        sender = headers.get("From", "")
        subject = headers.get("Subject", "")
        print(f"[SPAM] {sender}: {subject}")


if __name__ == "__main__":
    main()