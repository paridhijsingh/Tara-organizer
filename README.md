# Tara — Personal AI Organizer

> Meet Tara, a personal AI organizer that keeps your calendar, inbox, and deadlines in order — starting with a simple morning briefing.

## What Tara does

**Phase 1**
- **Today's calendar** — read-only, Google Calendar
- **Important unread Gmail** — read-only, Gmail, no specific-sender list
- **Top deadlines** — hand-edited list, next 7 days
- **Morning briefing** — `python main.py`

## What Tara does NOT do

**Phase 1**
- No sending, replying, archiving, labelling, or deleting mail
- No creating, editing, or deleting calendar events
- No auto-archiving, ever
- Personal Gmail only — no work Gmail

**Phase 2** (with approval every time): Gmail cleaning and categorizing, suspicious mail to Spam after review, reducing Gmail folders, organizing bookmarks, and desktop tidy with suggestions.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then create a Google Cloud project, enable **Gmail API** and **Google Calendar API**, create an OAuth client (Desktop app), and download `credentials.json` into this folder.

`credentials.json` is gitignored — never commit it.

## Usage

```bash
python calendar_client.py   # Step 1 — today's events, read-only
python main.py              # morning briefing — once all of Phase 1 is done
```

## Files

| File | Role |
|------|------|
| `PLAN.md` | Full plan, Phase 0–7 |
| `SKILL.md` | How Tara works |
| `RULES.md` | 15 standing rules |
| `CHANGELOG.md` | Every change — Date / What / Why / When / Log |
| `calendar_client.py` | `get_today_events()` |
| `gmail_client.py` | `get_important_unread()` |
| `briefing.py` | `build_briefing(events, emails, deadlines)` |
| `deadlines.py` | Hand-edited deadlines list |
| `test_briefing.py` | Tests — no Google calls needed |

## Rules

Plan first, one feature at a time, read-only first, nothing sends without approval, no secrets in git, log every change.

See [RULES.md](RULES.md).
