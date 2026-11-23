from auth import get_credentials
import datetime
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build



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
