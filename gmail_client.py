from googleapiclient.discovery import build
from auth import get_credentials


IMPORTANT_WORDS = [
    "application", "interview", "recruiter", "screening",
    "offer", "hiring", "applied",
    "substack", "tldr", "tech",
]

EXCLUDE_WORDS = [
    "job alert", "applications needed", "hiring now",
    "position is vacant", "job feed", "warehouse associate",
]


def is_important(email):
    """True if this mail is about a company she applied to,
    or is a Substack / TLDR / tech newsletter she subscribes to."""
    text = (email["sender"] + " " + email["subject"] + " " + email["snippet"]).lower()
    if any(word in text for word in EXCLUDE_WORDS):
        return False
    return any(word in text for word in IMPORTANT_WORDS)


def get_important_unread():
    """Return important unread mail as a list of {sender, subject, snippet}.

    Read-only. No specific-sender list, no archiving, no moving mail.
    """
    service = build("gmail", "v1", credentials=get_credentials())

    result = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=10,
    ).execute()
    messages = result.get("messages", [])

    emails = []
    for msg in messages:
        full = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["From", "Subject"],
        ).execute()
        headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
        emails.append({
            "sender": headers.get("From", "(unknown sender)"),
            "subject": headers.get("Subject", "(no subject)"),
            "snippet": full.get("snippet", ""),
        })
    return [e for e in emails if is_important(e)]


if __name__ == "__main__":
    for email in get_important_unread():
        print(email["sender"], "-", email["subject"])
        print("  ", email["snippet"])
