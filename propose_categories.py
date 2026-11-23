# propose_categories.py — Show Tara's category suggestions, read-only.
# Usage: python propose_categories.py
# Moves nothing. Paridhi approves a batch first, then Tara moves it.

from googleapiclient.discovery import build

from auth import get_credentials
from categorize import suggest_category


def main():
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().messages().list(userId="me", q="is:unread", maxResults=10).execute()
    messages = result.get("messages", [])

    if not messages:
        print("No unread mail.")
        return

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
        print(f"[{category}] {sender}: {subject}")


if __name__ == "__main__":
    main()
