import datetime
import os.path
from zoneinfo import ZoneInfo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Read-only — Tara can never create, edit, or delete an event
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_today_events():
    """Return today's events as a list of {time, title, attendees}."""
    service = build("calendar", "v3", credentials=get_credentials())
    tz = ZoneInfo("America/Los_Angeles")
    today = datetime.datetime.now(tz).date()
    start_of_day = datetime.datetime.combine(today, datetime.time.min, tzinfo=tz)
    end_of_day = datetime.datetime.combine(today, datetime.time.max, tzinfo=tz)

    events = service.events().list(
        calendarId="primary",
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute().get("items", [])

    return [
        {"time": e["start"].get("dateTime", e["start"].get("date")),
         "title": e.get("summary", "(no title)"),
         "attendees": [a.get("email") for a in e.get("attendees", [])]}
        for e in events
    ]


if __name__ == "__main__":
    for event in get_today_events():
        print(event["time"], "-", event["title"])
