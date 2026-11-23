# test_briefing.py — Tests for build_briefing, with fake data only.
# No Google calls here.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from briefing import build_briefing


def test_empty_day():
    """Empty day: no events, no mail, no deadlines."""
    text = build_briefing([], [], [])
    assert "No events today." in text
    assert "Nothing important unread." in text
    assert "No deadlines listed." in text


def test_one_event_one_email():
    """One event + one email: both show up."""
    events = [{"time": "10:00 AM", "title": "Team meeting", "attendees": []}]
    emails = [{"sender": "HPE", "subject": "Interview invite", "snippet": ""}]
    text = build_briefing(events, emails, [])
    assert "10:00 AM — Team meeting" in text
    assert "HPE: Interview invite" in text


def test_deadline_sorting():
    """Deadlines show in the order given — deadlines.py sorts them."""
    deadlines = [
        {"date": "2026-12-10", "title": "FinPath AI results"},
        {"date": "2026-12-01", "title": "Vastra judging starts"},
    ]
    text = build_briefing([], [], deadlines)
    assert "2026-12-10 — FinPath AI results" in text
    assert "2026-12-01 — Vastra judging starts" in text
