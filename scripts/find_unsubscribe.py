# find_unsubscribe.py — Find unsubscribe links for job-alert senders.
# Usage: python3 scripts/find_unsubscribe.py
# Read-only. Unsubscribes nothing. Paridhi approves the list first.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials

# Senders Paridhi asked to unsubscribe from, Nov 25, 2026
SENDERS = [
    "info@alerts.myjobhelper.com",      # MJH / MyJobHelper — DONE Nov 25
    "info@match.careerconnects.com",    # CareerConnects — DONE Nov 25
    "jobsora.com",                      # Jobsora
    # "careercircle.com",  # KEEP — Paridhi said Nov 25 CareerCircle is important, do NOT unsubscribe
    "wallstreetquants.com",             # WallStreetQuants
]


def main():
    service = build("gmail", "v1", credentials=get_credentials())

    for sender in SENDERS:
        result = service.users().messages().list(
            userId="me", q=f"from:{sender}", maxResults=3
        ).execute()
        messages = result.get("messages", [])
        print(f"\n{sender}: {len(messages)} recent mail found (showing up to 3)")

        for message in messages:
            full = service.users().messages().get(
                userId="me", id=message["id"], format="metadata",
                metadataHeaders=["From", "Subject", "List-Unsubscribe"],
            ).execute()
            headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
            print(f"  - {headers.get('Subject', '')}")
            print(f"    Unsubscribe: {headers.get('List-Unsubscribe', 'No List-Unsubscribe header — check the bottom of the email')}")


if __name__ == "__main__":
    main()