# propose_job_status.py — Show Tara's Job Applications status + type for each mail.
# Usage: python3 scripts/propose_job_status.py
# Read-only. Moves nothing. Paridhi approves a batch first.

import base64
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials
from job_status import classify_job_email, classify_job_type


def get_body(payload):
    """Return the plain-text body of a Gmail message, or ''."""
    if not payload:
        return ""
    # Single-part message
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
    # Multi-part message: find the text/plain part
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
        if part.get("parts"):
            text = get_body(part)
            if text:
                return text
    return ""


def main():
    service = build("gmail", "v1", credentials=get_credentials())

    labels_result = service.users().labels().list(userId="me").execute()
    job_label_ids = [
        label["id"]
        for label in labels_result.get("labels", [])
        if label["name"] == "Job Applications" or label["name"].startswith("Job Applications/")
    ]

    seen_ids = set()
    messages = []
    # Skip mail already filed by apply_job_status.py, so each run is a fresh batch
    filed_label_names = {
        "Job Applications/Active",
        "Job Applications/Not moving forward",
        "Job Applications/Inactive",
    }
    all_labels = {label["name"]: label["id"] for label in labels_result.get("labels", [])}
    filed_ids = {all_labels[name] for name in filed_label_names if name in all_labels}

    for label_id in job_label_ids:
        result = service.users().messages().list(
            userId="me", labelIds=[label_id], maxResults=50
        ).execute()
        for message in result.get("messages", []):
            if message["id"] in seen_ids:
                continue
            seen_ids.add(message["id"])
            # messages().list does not return labelIds, so check the full message
            full_labels = service.users().messages().get(
                userId="me", id=message["id"], format="metadata",
                metadataHeaders=["From"],
            ).execute().get("labelIds", [])
            if filed_ids.intersection(full_labels):
                continue
            messages.append(message)
        if len(messages) >= 20:
            break

    messages = messages[:20]

    if not messages:
        print("No Job Applications mail found.")
        return

    counts = {"Active": 0, "Not moving forward": 0, "Inactive": 0, "Unsure": 0}

    for message in messages:
        full = service.users().messages().get(
            userId="me", id=message["id"], format="full"
        ).execute()
        headers = {h["name"]: h["value"] for h in full.get("payload", {}).get("headers", [])}
        sender = headers.get("From", "")
        subject = headers.get("Subject", "")
        body = get_body(full.get("payload", {}))
        text = f"{sender} {subject} {body}"
        status = classify_job_email(text)
        job_type = classify_job_type(text)
        counts[status] += 1
        type_label = f" | {job_type}" if job_type else ""
        print(f"[{status}{type_label}] {sender}: {subject}")

    print("")
    print(f"Summary: {counts}")


if __name__ == "__main__":
    main()

