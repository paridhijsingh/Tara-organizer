# Tara Skill

## What Tara Is

Tara is a personal organizer agent. Her Phase 1 job is **one clear morning briefing**: today's calendar, important unread Gmail, and top deadlines — personal Gmail only. Phase 2 adds an emailed briefing plus approval-gated Gmail cleaning.

## When to Use This Skill

Use this skill when working on Tara in the `tara-organizer` repo — planning, implementing, testing, or reviewing. Follow [PLAN.md](PLAN.md) and [RULES.md](RULES.md). Log every change in [CHANGELOG.md](CHANGELOG.md). See [MANUAL.md](MANUAL.md) for how each feature works.

## How She Works

### Phase 1 — morning briefing (done)
- CLI: `python src/main.py`
- Deterministic Python only — no LLM
- Google Calendar + personal Gmail (`paridhijaysingh@gmail.com`)
- Hand-edited local deadlines list
- Assembles a briefing from events + emails + deadlines
- No hard-coded sender allowlist for “important”
- No auto-archiving

### Phase 2 — messaging + cleaning (in progress, approval every time)
- `python src/send_briefing.py` — email briefing to Paridhi only (cron at 8am)
- Propose categories → approve batch → apply
- List / clean labels — delete approved labels only, never mail
- Bookmarks and desktop tidy — not built yet

### Scopes (`src/auth.py`)
- `calendar.readonly`, `gmail.readonly` — read calendar and mail
- `gmail.send` — morning briefing email only
- `gmail.modify` — apply category labels / delete labels after approval

Credentials stay at repo root: `credentials.json` and `token.json` are gitignored. `auth.py` resolves them from the parent of `src/`.

## Briefing Output Format

```
Good morning, Paridhi — here's your day with Tara.

Today's calendar:
- No events today.
  (or) - [time] — Event title

Important unread mail:
- Nothing important unread.
  (or) - sender: subject

Top deadlines:
- No deadlines listed.
  (or) - YYYY-MM-DD — Deadline title
```

Empty sections say so explicitly (fail safe — never invent data).

## Files

| Path | Role |
|------|------|
| [PLAN.md](PLAN.md) | Full plan, Phase 0–7 |
| [RULES.md](RULES.md) | Standing rules |
| [CHANGELOG.md](CHANGELOG.md) | Change log |
| [MANUAL.md](MANUAL.md) | Textbook — one chapter per feature |
| `src/auth.py` | Shared OAuth — `get_credentials()` |
| `src/calendar_client.py` | `get_today_events()` |
| `src/gmail_client.py` | `get_important_unread()` |
| `src/deadlines.py` | Hand-edited deadlines — `get_deadlines()` |
| `src/briefing.py` | `build_briefing(events, emails, deadlines)` |
| `src/categorize.py` | `suggest_category(...)` |
| `src/main.py` | Print morning briefing |
| `src/send_briefing.py` | Email morning briefing |
| `scripts/propose_categories.py` | Show category suggestions (read-only) |
| `scripts/apply_categories.py` | Apply approved category batch |
| `scripts/list_labels.py` | List Gmail labels (read-only) |
| `scripts/clean_applications_labels.py` | Delete approved Applications sub-labels |
| `scripts/clean_substacks_labels.py` | Delete approved Substacks sub-labels |
| `tests/test_briefing.py` | Briefing tests — no Google calls |
| `tests/test_categorize.py` | Categorize tests — no Google calls |
