# send_briefing.py — Send Tara's morning briefing by email to Paridhi.
# Usage: python send_briefing.py
# Sends ONLY to paridhijaysingh@gmail.com, never to anyone else.

import base64
from email.message import EmailMessage

from googleapiclient.discovery import build

from auth import get_credentials
from calendar_client import get_today_events
from gmail_client import get_important_unread
from deadlines import get_deadlines
from briefing import build_briefing

TO_EMAIL = "paridhijaysingh@gmail.com"


def send_briefing():
    events = get_today_events()
    emails = get_important_unread()
    deadlines = get_deadlines()
    text = build_briefing(events, emails, deadlines)

    message = EmailMessage()
    message["To"] = TO_EMAIL
    message["Subject"] = "Tara — your morning briefing"
    message.set_content(text)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    service = build("gmail", "v1", credentials=get_credentials())
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("Briefing emailed to", TO_EMAIL)


if __name__ == "__main__":
    send_briefing()
