# main.py — Run Tara's morning briefing.
# Usage: python main.py

from calendar_client import get_today_events
from gmail_client import get_important_unread
from deadlines import get_deadlines
from briefing import build_briefing


def main():
    events = get_today_events()
    emails = get_important_unread()
    deadlines = get_deadlines()
    print(build_briefing(events, emails, deadlines))


if __name__ == "__main__":
    main()
