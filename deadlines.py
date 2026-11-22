# deadlines.py — Tara's hand-edited deadlines list.
# Paridhi edits this file herself when a deadline changes.
# Format: {"date": "YYYY-MM-DD", "title": "..."}

DEADLINES = [
    {"date": "2026-12-01", "title": "Vastra judging starts (Dec 1-15)"},
    {"date": "2026-12-10", "title": "FinPath AI results"},
    {"date": "2026-12-24", "title": "HPE screening due 11:59 PM EST"},
]


def get_deadlines():
    """Return the deadlines list, sorted by date."""
    return sorted(DEADLINES, key=lambda d: d["date"])
