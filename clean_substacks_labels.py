# clean_substacks_labels.py — Delete all Substacks/<name> sub-labels.
# APPROVED by Paridhi Nov 22, 2026. Deletes labels only, never mail.
# Keeps the parent label "Substacks". Mail stays under Substacks / All Mail.
# Usage: python clean_substacks_labels.py

from googleapiclient.discovery import build

from auth import get_credentials


def main():
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().labels().list(userId="me").execute()
    labels = result.get("labels", [])

    deleted = 0
    for label in labels:
        name = label["name"]
        if name.startswith("Substacks/"):
            service.users().labels().delete(userId="me", id=label["id"]).execute()
            print(f"Deleted label: {name}")
            deleted += 1

    print(f"Done. Deleted {deleted} Substacks sub-labels. Parent 'Substacks' kept.")


if __name__ == "__main__":
    main()
