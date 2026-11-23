# clean_applications_labels.py — Delete 5 old college Applications sub-labels.
# APPROVED by Paridhi Nov 22, 2026. Deletes labels only, never mail.
# Keeps the parent label "Applications".
# Usage: python clean_applications_labels.py

from googleapiclient.discovery import build

from auth import get_credentials

# Exact label IDs from list_labels.py, Nov 22 — do not change these.
LABELS_TO_DELETE = [
    ("Applications/FAFSA", "Label_1044439552686148410"),
    ("Applications/Santa Barbara", "Label_1928292399050428768"),
    ("Applications/Indian Universities", "Label_4108883579527769121"),
    ("Applications/CSS Profile", "Label_5395904355837585680"),
    ("Applications/University of California", "Label_7152221525110716217"),
]


def main():
    service = build("gmail", "v1", credentials=get_credentials())
    for name, label_id in LABELS_TO_DELETE:
        service.users().labels().delete(userId="me", id=label_id).execute()
        print(f"Deleted label: {name}")


if __name__ == "__main__":
    main()
