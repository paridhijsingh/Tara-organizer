# Tara Skill

## What Tara Is

Tara is a personal organizer agent. In Phase 1 her one job is **one clear morning briefing**: today's calendar, important unread Gmail, and top deadlines — read-only, personal Gmail only.

## When to Use This Skill

Use this skill when working on Tara in the `tara-organizer` repo — planning, implementing, testing, or reviewing. Follow `PLAN.md` and `RULES.md`. Log every change in `CHANGELOG.md`.

## How She Works (Phase 1)

- CLI: `python main.py`
- Deterministic Python only — no LLM in Phase 1
- Read-only Google Calendar + personal Gmail (`paridhijaysingh@gmail.com`)
- Scopes: `calendar.readonly` and `gmail.readonly` only
- Hand-edited local deadlines list
- Assembles a briefing from events + emails + deadlines
- No hard-coded sender allowlist for “important”
- No sending, deleting, moving, creating events, or auto-archiving

### Modules
- `calendar_client.py` — `get_today_events()`
- `gmail_client.py` — `get_important_unread()`
- `deadlines.py` — hand-edited deadline list
- `briefing.py` — `build_briefing(events, emails, deadlines)`

Credentials stay local: `credentials.json` and `token.json` are gitignored.

Phase 2 (Gmail cleaning, labels, bookmarks, desktop tidy) is approval-only — see `PLAN.md`. Not built in Phase 1.

## Briefing Output Format

```
=== Tara Morning Briefing — YYYY-MM-DD ===

Calendar (today)
- [time] Event title (source: calendar)

Important unread
- From: sender — subject (source: gmail)

Deadlines
- [due date] Deadline item (source: deadlines)

=== End ===
```

- Show sources for every item
- Empty sections say so explicitly (fail safe — never invent data)

## Files

| File | Role |
|------|------|
| [PLAN.md](PLAN.md) | Full plan, Phase 0–7 |
| [RULES.md](RULES.md) | Standing rules |
| [CHANGELOG.md](CHANGELOG.md) | Change log |
| `main.py` | CLI entry (not built yet) |
| `calendar_client.py` | Today's events (Step 1 — you write) |
| `gmail_client.py` | Important unread (not built yet) |
| `deadlines.py` | Hand-edited deadlines (not built yet) |
| `briefing.py` | Build briefing (not built yet) |
| `test_briefing.py` | Fake-data tests (not built yet) |
