# apply_job_status.py — Apply Tara's Job Applications status to approved mail.
# APPROVED by Paridhi Nov 25, 2026, for the 20 mails in the last propose run.
# Not moving forward -> Trash (recoverable 30 days, not permanent delete).
# Active -> label Job Applications/Active.
# Inactive -> label Job Applications/Inactive.
# Unsure -> left alone.
# Then emails Paridhi a summary report.
# Usage: python3 scripts/apply_job_status.py

import base64
import sys
from email.message import EmailMessage
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from googleapiclient.discovery import build

from auth import get_credentials
from job_status import classify_job_email, classify_job_type
from propose_job_status import get_body


def get_or_create_label(service, name):
    result = service.users().labels().list(userId="me").execute()
    for label in result.get("labels", []):
        if label["name"] == name:
            return label["id"]
    created = service.users().labels().create(
        userId="me", body={"name": name, "labelListVisibility": "labelShow"}
    ).execute()
    return created["id"]


def main():
    service = build("gmail", "v1", credentials=get_credentials())

    active_id = get_or_create_label(service, "Job Applications/Active")
    not_moving_id = get_or_create_label(service, "Job Applications/Not moving forward")
    inactive_id = get_or_create_label(service, "Job Applications/Inactive")

    labels_result = service.users().labels().list(userId="me").execute()
    job_label_ids = [
        label["id"]
        for label in labels_result.get("labels", [])
        if label["name"] == "Job Applications" or label["name"].startswith("Job Applications/")
    ]

    seen_ids = set()
    messages = []
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
            full_labels = service.users().messages().get(
                userId="me", id=message["id"], format="metadata",
                metadataHeaders=["From"],
            ).execute().get("labelIds", [])
            if filed_ids.intersection(full_labels):
                continue
            messages.append(message)
        if len(messages) >= 20:
            break

    moved_trash = []
    filed_active = []
    filed_inactive = []
    left_alone = []

    for message in messages[:20]:
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
        line = f"{sender}: {subject}" + (f" ({job_type})" if job_type else "")

        if status == "Not moving forward":
            service.users().messages().trash(userId="me", id=message["id"]).execute()
            # Also keep the status label so you can find it in Trash
            service.users().messages().modify(
                userId="me", id=message["id"],
                body={"addLabelIds": [not_moving_id]},
            ).execute()
            moved_trash.append(line)
            print(f"Moved to Trash: {line}")
        elif status == "Active":
            service.users().messages().modify(
                userId="me", id=message["id"],
                body={"addLabelIds": [active_id]},
            ).execute()
            filed_active.append(line)
            print(f"Filed Active: {line}")
        elif status == "Inactive":
            service.users().messages().modify(
                userId="me", id=message["id"],
                body={"addLabelIds": [inactive_id]},
            ).execute()
            filed_inactive.append(line)
            print(f"Filed Inactive: {line}")
        else:
            left_alone.append(line)
            print(f"Left alone (Unsure): {line}")

    # Summary report email
    report_lines = ["Tara — Job Applications status report", ""]
    report_lines.append(f"Moved to Trash (Not moving forward, {len(moved_trash)}):")
    report_lines += [f"- {line}" for line in moved_trash] or ["- None"]
    report_lines.append("")
    report_lines.append(f"Filed Active ({len(filed_active)}):")
    report_lines += [f"- {line}" for line in filed_active] or ["- None"]
    report_lines.append("")
    report_lines.append(f"Filed Inactive ({len(filed_inactive)}):")
    report_lines += [f"- {line}" for line in filed_inactive] or ["- None"]
    report_lines.append("")
    report_lines.append(f"Left alone — Unsure ({len(left_alone)}):")
    report_lines += [f"- {line}" for line in left_alone] or ["- None"]
    report_lines.append("")
    report_lines.append("Trash mail stays recoverable for 30 days in Gmail.")
    report = "\n".join(report_lines)

    message = EmailMessage()
    message["To"] = "paridhijaysingh@gmail.com"
    message["Subject"] = "Tara — Job Applications status report"
    message.set_content(report)
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("Summary report emailed to paridhijaysingh@gmail.com")


if __name__ == "__main__":
    main()