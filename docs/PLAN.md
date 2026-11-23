# Tara — Full Plan (Phase 0–7)

## Phase 0: What Tara Is

Tara's one-line job: **one clear morning briefing** — today's calendar, important unread Gmail, and top deadlines.

**Read-only in Phase 1.** No sending, no deleting, no moving, no creating/editing events, no work Gmail, no secrets in git. No auto-archiving, ever.

**Success criteria:**
- Briefing correct 5/5 mornings
- 0 wrong sends
- pytest passes

---

## Phase 1: Morning Briefing (Must)

### Must (only 4 features)
1. Today's calendar
2. Important unread Gmail (no hard-coded sender list)
3. Top deadlines
4. Morning briefing that puts them together

### How it works
- **Interface:** CLI — `python main.py`
- **Logic:** Deterministic code only; no LLM in Phase 1
- **Scopes:** `gmail.readonly` and `calendar.readonly` only
- **Data:** local files only; `credentials.json` + `token.json` gitignored
- **Account:** personal Gmail only (`paridhijaysingh@gmail.com`)

### Modules
| File | Responsibility |
|------|----------------|
| `calendar_client.py` | `get_today_events()` |
| `gmail_client.py` | `get_important_unread()` |
| `deadlines.py` | Hand-edited deadline list |
| `briefing.py` | `build_briefing(events, emails, deadlines)` |

### Build order
1. Calendar first
2. Then Gmail
3. Then briefing
4. Then run it tomorrow morning

**One feature at a time.**

### Not in Phase 1
- Work Gmail
- Auto-archiving (never)
- Smart replies (drafts only — later)
- Trip planning, workout scheduling, calendar reminders

---

## Phase 2: Gmail + Desktop Cleaning (Approval Every Time)

All Phase 2 actions require Paridhi's approval before any change. Tara proposes; she never acts silently.

### Suspicious mail
- Flag it and message Paridhi to review it herself first
- Only after approval, file it to Spam
- Never auto-spam

### Categorizing
- File mail into Promotions, Social, Updates, etc.
- Keep cleaning Gmail only after approval of each batch, time and again
- Never auto-archive

### Gmail folders / labels
- List all labels
- Propose merges / deletes for duplicates and unused ones
- Paridhi approves each one
- Never delete mail — only the label structure

### Bookmarks
- List them
- Propose folders, merge duplicates, flag dead links
- Paridhi approves each move
- Never lose a bookmark

### Desktop
- Give suggestions and assist
- Paridhi approves each move
- Never move or delete a file automatically

---

## Phase 3: Guardrails

- Plan first; one feature at a time
- Read-only first in Phase 1
- Scopes: `gmail.readonly` and `calendar.readonly` only
- Nothing sends / deletes / moves / creates without approval
- No secrets in git
- Personal Gmail only
- No hard-coded specific-sender “important” list
- No auto-archiving, ever
- No hallucinating; show sources; fail safe
- Paridhi writes the code
- Log every change; test before calling it done
- Privacy / OSpectra stays out

---

## Phase 4: Testing

- File: `test_briefing.py`
- 3 tests with fake data; no Google calls:
  1. Empty day
  2. One event + one email
  3. Deadline sorting

---

## Phase 5: Build Loop

1. Calendar first (`calendar_client.py`)
2. Then Gmail
3. Then briefing
4. Then run it tomorrow morning

**One feature at a time. Do not start the next until the current one works.**

---

## Phase 6: Self-Improvement

- Keep `CHANGELOG.md` (Date / What / Why / When / Log)
- Weekly 15-min review
- One change at a time

---

## Phase 7: Portfolio Story

Write the portfolio story **only when Tara works**.
