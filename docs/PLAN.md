# Tara — Full Plan (Phase 0–7)

## Phase 0: What Tara Is

Tara's one-line job: **one clear morning briefing** — today's calendar, important unread Gmail, and top deadlines.

**Phase 1 is read-first.** No work Gmail, no secrets in git, no auto-archiving ever. Sending mail, labelling, and label deletes happen only in Phase 2 with Paridhi's approval.

**Success criteria:**
- Briefing correct 5/5 mornings
- 0 wrong sends
- pytest passes

---

## Phase 1: Morning Briefing (Must) — done

### Must (only 4 features)
1. Today's calendar
2. Important unread Gmail (no hard-coded sender list)
3. Top deadlines
4. Morning briefing that puts them together

### How it works
- **Interface:** CLI — `python src/main.py`
- **Logic:** Deterministic code only; no LLM in Phase 1
- **Account:** personal Gmail only (`paridhijaysingh@gmail.com`)
- **Data:** local files only; `credentials.json` + `token.json` at repo root, gitignored

### Modules (`src/`)
| File | Responsibility |
|------|----------------|
| `auth.py` | Shared OAuth — `get_credentials()` |
| `calendar_client.py` | `get_today_events()` |
| `gmail_client.py` | `get_important_unread()` |
| `deadlines.py` | Hand-edited deadline list — `get_deadlines()` |
| `briefing.py` | `build_briefing(events, emails, deadlines)` |
| `main.py` | Print the morning briefing |

### Build order (completed)
1. Calendar first
2. Then Gmail
3. Then briefing
4. Run it in the morning

**One feature at a time.**

### Not in Phase 1
- Work Gmail
- Auto-archiving (never)
- Smart replies (drafts only — later)
- Trip planning, workout scheduling, calendar reminders

---

## Phase 2: Messaging + Gmail / Desktop Cleaning (Approval Every Time)

All Phase 2 actions that change mail or labels require Paridhi's approval first (except the scheduled morning email she already approved). Tara proposes; she never acts silently on cleaning.

### Morning message by email — done
- `src/send_briefing.py` emails the briefing to `paridhijaysingh@gmail.com` only
- Cron at 8am: `python …/src/send_briefing.py`
- Scope used: `gmail.send` (plus the read scopes)

### Suspicious mail — not built yet
- Flag it and message Paridhi to review it herself first
- Only after approval, file it to Spam
- Never auto-spam

### Categorizing — in progress
- `src/categorize.py` suggests Promotions / Social / Updates / Important
- `scripts/propose_categories.py` shows suggestions (read-only)
- `scripts/apply_categories.py` applies only an approved batch
- Never auto-archive

### Gmail folders / labels — in progress
- `scripts/list_labels.py` lists all labels
- `scripts/clean_applications_labels.py` / `clean_substacks_labels.py` delete only approved labels
- Never delete mail — only the label structure

### Bookmarks — not built yet
- List them; propose folders, merge duplicates, flag dead links
- Paridhi approves each move; never lose a bookmark

### Desktop — not built yet
- Give suggestions and assist
- Paridhi approves each move; never move or delete a file automatically

---

## Phase 3: Guardrails

- Plan first; one feature at a time
- Phase 1 is read-first; Phase 2 changes need approval
- Scopes in use: `calendar.readonly`, `gmail.readonly`, `gmail.send`, `gmail.modify`
- Nothing sends / deletes / moves / creates without approval (morning cron is the approved send path)
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

| File | Tests |
|------|--------|
| `tests/test_briefing.py` | Empty day; one event + one email; deadlines show up |
| `tests/test_categorize.py` | Important newsletter; promotion; updates fallback |

Fake data only — no Google calls. Run: `pytest tests/ -q`

---

## Phase 5: Build Loop

1. Calendar → Gmail → briefing (Phase 1 — done)
2. Morning email + categorizing + label cleaning (Phase 2 — in progress)
3. One feature at a time; do not start the next until the current one works

---

## Phase 6: Self-Improvement

- Keep `docs/CHANGELOG.md` (Date / What / Why / When / Log)
- Weekly 15-min review
- One change at a time

---

## Phase 7: Portfolio Story

Write the portfolio story **only when Tara works**.

---

## Repo layout

```
tara-organizer/
  README.md, requirements.txt, .gitignore
  credentials.json, token.json   # root, gitignored
  docs/     PLAN, SKILL, RULES, CHANGELOG, MANUAL
  src/      auth, calendar, gmail, deadlines, briefing, categorize, main, send_briefing
  scripts/  propose_categories, apply_categories, list_labels, clean_*
  tests/    test_briefing, test_categorize
```
