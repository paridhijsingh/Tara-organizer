# Tara — Personal AI Organizer

> Meet Tara, a personal AI organizer that keeps your calendar, inbox, and deadlines in order — starting with a simple morning briefing.

## What Tara does

**Phase 1** (done)
- **Today's calendar** — read-only, Google Calendar
- **Important unread Gmail** — read-only filter, no specific-sender list
- **Top deadlines** — hand-edited list
- **Morning briefing** — `python src/main.py`

**Phase 2** (in progress, approval every time)
- Morning briefing by email (cron at 8am)
- Gmail categorizing (propose → approve → apply)
- Reducing unused Gmail labels
- Later: suspicious mail to Spam after review, bookmarks, desktop tidy

## What Tara does NOT do

- No work Gmail — personal only (`paridhijaysingh@gmail.com`)
- No creating, editing, or deleting calendar events
- No auto-archiving, ever
- No silent labelling, label deletes, or spam moves — Paridhi approves each batch
- Sends only to Paridhi, via the approved morning path

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then create a Google Cloud project, enable **Gmail API** and **Google Calendar API**, create an OAuth client (Desktop app), and download `credentials.json` into the **repo root**.

`credentials.json` and `token.json` are gitignored — never commit them.

## Usage

```bash
python src/main.py                      # morning briefing (print)
python src/send_briefing.py             # email briefing to Paridhi
python src/calendar_client.py           # today's events only
python scripts/propose_categories.py    # category suggestions — moves nothing
python scripts/list_labels.py           # list Gmail labels — changes nothing
pytest tests/ -q                        # 6 tests, no Google calls
```

## Files

| Path | Role |
|------|------|
| `docs/PLAN.md` | Full plan, Phase 0–7 |
| `docs/SKILL.md` | How Tara works |
| `docs/RULES.md` | 15 standing rules |
| `docs/CHANGELOG.md` | Every change — Date / What / Why / When / Log |
| `docs/MANUAL.md` | Textbook — one chapter per feature |
| `src/auth.py` | Shared OAuth — `get_credentials()` |
| `src/calendar_client.py` | `get_today_events()` |
| `src/gmail_client.py` | `get_important_unread()` |
| `src/deadlines.py` | Hand-edited deadlines |
| `src/briefing.py` | `build_briefing(...)` |
| `src/categorize.py` | `suggest_category(...)` |
| `src/main.py` | Print morning briefing |
| `src/send_briefing.py` | Email morning briefing |
| `scripts/` | Propose / apply categories, list / clean labels |
| `tests/` | `test_briefing.py`, `test_categorize.py` |

## Rules

Plan first, one feature at a time, Phase 1 read-first, nothing sends or changes mail without approval, no secrets in git, log every change.

See [docs/RULES.md](docs/RULES.md).
