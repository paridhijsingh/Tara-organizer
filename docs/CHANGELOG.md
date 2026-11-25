# CHANGELOG

Format for every entry: **Date**, **What**, **Why**, **When**, **Log**.

---

### 2026-11-21 — Setup

- **Date:** 2026-11-21
- **What:** Repo `tara-organizer`, venv, `.gitignore`, `requirements.txt`; pip install succeeded
- **Why:** Bootstrap the project so Tara can use Google APIs safely
- **When:** 2026-11-21
- **Log:** Installed `google-api-python-client` 2.202.0, `google-auth-oauthlib` 1.5.0, `google-auth-httplib2` 0.4.4

---

### 2026-11-21 — Google Cloud access

- **Date:** 2026-11-21
- **What:** Google Cloud project `tara-organizer`; Gmail + Calendar APIs enabled; OAuth consent created; test user `paridhijaysingh@gmail.com`; OAuth client Desktop app; `credentials.json` in repo folder (gitignored)
- **Why:** Enable read-only Calendar and Gmail access for the morning briefing
- **When:** 2026-11-21
- **Log:** Project, APIs, consent screen, Desktop OAuth client, and local credentials ready; secrets stay out of git

---

### 2026-11-21 — Plan created

- **Date:** 2026-11-21
- **What:** Full plan Phase 0–7 written to `PLAN.md`, plus `SKILL.md`, `RULES.md`, and this changelog
- **Why:** Plan first before coding
- **When:** 2026-11-21
- **Log:** Docs only — no feature code yet; later revised to drop hard-coded sender list and add Phase 2 cleaning

---

### 2026-11-21 — Gmail + desktop cleaning decided

- **Date:** 2026-11-21
- **What:** Phase 2 includes suspicious-mail flagging, categorizing (Promotions/Social/Updates), and desktop tidy — all approval-gated
- **Why:** Clean inbox and desktop without silent automation or auto-spam / auto-archive
- **When:** 2026-11-21
- **Log:** Suspicious: flag → Paridhi reviews → Spam only after approval. Categorize and desktop moves: propose, approve each batch/move. Never auto-archive.

---

### 2026-11-21 — Gmail folders + bookmarks decided

- **Date:** 2026-11-21
- **What:** Phase 2 includes Gmail label/folder reduction and bookmark organization — approval every change
- **Why:** Reduce duplicate/unused labels and tidy bookmarks without losing mail or links
- **When:** 2026-11-21
- **Log:** Labels: list → propose merges/deletes → approve each; never delete mail. Bookmarks: list → propose folders/merges/dead links → approve each move; never lose a bookmark.

---

### 2026-11-21 — Calendar Step 1 done

- **Date:** 2026-11-21
- **What:** Created `calendar_client.py` with `get_today_events()` — read-only, `calendar.readonly` scope only
- **Why:** Step 1 in Tara's plan — today's calendar is the first piece of the morning briefing
- **When:** Phase 1, Step 1
- **Log:** `python calendar_client.py` ran with no error, printed no events — today is empty in Google Calendar. `token.json` saved (762 bytes), gitignored, not in git status. Fixed a missing `ZoneInfo` import along the way.

---

### 2026-11-21 — Gmail Step 2 done, "important" v2

- **Date:** 2026-11-21
- **What:** Created `gmail_client.py` with `get_important_unread()` — read-only, `gmail.readonly` scope only, with `is_important()` filter
- **Why:** Step 2 in Tara's plan — important unread Gmail is the second piece of the morning briefing
- **When:** Phase 1, Step 2
- **Log:** First run returned 10 unread, all noise. Filter v1 matched CareerConnects job alerts ("APPLICATIONS NEEDED", "Hiring now") — false positives. Filter v2 added `EXCLUDE_WORDS` (job alert, applications needed, hiring now, position is vacant, job feed) — second run printed nothing, correctly. "Important" is a living definition, we will keep refining it.

---

### 2026-11-22 — Step 3: Briefing done

- **Date:** 2026-11-22
- **What:** Added `deadlines.py` (hand-edited list: Vastra judging Dec 1, FinPath results Dec 10, HPE screening Dec 24), `briefing.py` (`build_briefing`), `main.py` (`python main.py` prints the briefing), `test_briefing.py` (3 tests)
- **Why:** The briefing is Tara's one job in Phase 1 — calendar + important Gmail + deadlines in one morning message
- **When:** Phase 1, Step 3
- **Log:** Live run printed no events, 1 important mail (Chrisnotes), 3 deadlines. First run had 2 false positives (MJH job alert, Carnival sale) — filter v3 added "must hire", "myjobhelper", "cyber sale", "early access", "carnival" to `EXCLUDE_WORDS`, Chrisnotes kept on purpose. `pytest -q`: 3 passed

---

### 2026-11-22 — Phase 2: Morning message by email

- **Date:** 2026-11-22
- **What:** Added `send_briefing.py` (emails the briefing to `paridhijaysingh@gmail.com` only), added `gmail.send` to `auth.py`, re-authorized once, scheduled it with cron at 8am daily (`0 8 * * *`), logging to `tara.log`
- **Why:** Phase 1 was a terminal command; Phase 2 makes Tara message Paridhi each morning
- **When:** Phase 2
- **Log:** Test email landed Nov 22 at 4:07 PM, correct briefing inside. `crontab -l` confirms the 8am schedule. Filter v4: AlgoMonster is noise, excluded. Text messages are later, not yet built

---

### 2026-11-22 — Phase 2: Gmail categorizing and label cleaning, part 1

- **Date:** 2026-11-22
- **What:** Added `categorize.py` (`suggest_category`: Promotions / Social / Updates / Important), `propose_categories.py` (read-only proposals), `list_labels.py` (read-only label list), `clean_applications_labels.py` (deletes 5 approved labels by ID), `test_categorize.py` (3 tests). Added `gmail.modify` to `auth.py`, re-authorized once
- **Why:** Gmail had ~200 labels; Tara proposes categories and helps decide which labels to combine and clean, with Paridhi approving each batch
- **When:** Phase 2
- **Log:** `pytest -q`: 6 passed. Live propose run: Daily Dose + Chrisnotes Important, Carnival + Algo Monster Promotions. Deleted, approved: Applications/FAFSA, Applications/Santa Barbara, Applications/Indian Universities, Applications/CSS Profile, Applications/University of California. Parent Applications kept, mail never deleted, Job Applications and Substacks untouched

---

### 2026-11-22 — Phase 2: Gmail categorizing, first approved move

- **Date:** 2026-11-22
- **What:** Added `apply_categories.py`. Applied the approved batch of 10 unread mails
- **Why:** Tara proposes first, Paridhi approves, then Tara moves only the approved mail
- **When:** Phase 2
- **Log:** Moved 8: Carnival + Algo Monster to Promotions; OpenRouter, Chris Ching, Apollo, WallStreetQuants, CareerCircle, MJH to Updates. Left alone: Daily Dose + Chrisnotes (Important). Nothing deleted, archived, or marked read

---

### 2026-11-22 — Phase 2: Substacks labels collapsed

- **Date:** 2026-11-22
- **What:** Added `clean_substacks_labels.py`. Deleted all `Substacks/<name>` sub-labels, kept parent Substacks
- **Why:** Paridhi has not been reading Substacks lately; 43 separate folders were not being used
- **When:** Phase 2
- **Log:** Deleted 43 sub-labels, verified with `list_labels.py | grep Substacks` — only Substacks (`Label_81`) remains. Mail never deleted

---

### 2026-11-22 — Repo reorganized into folders

- **Date:** 2026-11-22
- **What:** Moved files into `docs/` (PLAN, SKILL, RULES, CHANGELOG, MANUAL), `src/` (auth, calendar, gmail, briefing, deadlines, categorize, main, send*briefing), `scripts/` (propose, apply, list_labels, clean*\*), `tests/` (test_briefing, test_categorize). Used `git mv`, fixed import paths, `credentials.json` / `token.json` stay at root
- **Why:** Repo root had loads of files; folders make it easier to find code, docs, scripts, and tests
- **When:** Phase 2
- **Log:** Verified: `python src/main.py` prints briefing, `pytest tests/ -q`: 6 passed, `list_labels` + `propose_categories` work from `scripts/`. Cron updated to `src/send_briefing.py` at 8am, old cron line deleted

---

### 2026-11-22 — Docs synced to current repo

- **Date:** 2026-11-22
- **What:** Updated `docs/PLAN.md`, `SKILL.md`, `RULES.md`, `MANUAL.md`, and root `README.md` to match folder layout, built features, and scopes (`calendar.readonly`, `gmail.readonly`, `gmail.send`, `gmail.modify`)
- **Why:** Docs still pointed at root paths, said Phase 1 files were “not built,” and claimed read-only-only scopes after Phase 2 send/modify shipped
- **When:** Phase 2
- **Log:** Paths now use `src/`, `scripts/`, `docs/`, `tests/`. RULES softened to “one feature at a time” (still 15 rules). MANUAL chapters use current run commands. No feature code changed

---

### 2026-11-22 — README: cron + approval-gated scripts

- **Date:** 2026-11-22
- **What:** Added cron line, approval-gated script note, and scopes line to `README.md`
- **Why:** Close the last small gaps so the README matches live setup
- **When:** Phase 2
- **Log:** Docs only — no feature code changed

## 2026-11-25 — Phase 2: Job Applications status sorting

- **What:** Added src/job_status.py (status + Full-time / Intern type), scripts/propose_job_status.py (read-only, full body), scripts/apply_job_status.py (trash Not moving forward, file Active / Inactive, email summary report), tests/test_job_status.py (5 tests).
- **Why:** Job Applications mail had no status; Tara sorts Active / Not moving forward / Inactive, with a summary report.
- **When:** Nov 25, 2026.
- **Log:** pytest tests/ -q: 11 passed. First propose run (subject only): Active 10, Unsure 10, 0 rejections found. Body-read run: Active 9, Not moving forward 4, Unsure 7. Approved batch applied: 4 trashed (Vagaro, Amex x3), 9 filed Active, 7 left alone. Summary report emailed Nov 25 10:28 AM.

## 2026-11-25 — Phase 2: Unsubscribe from job-alert senders

- **What:** Added scripts/find_unsubscribe.py (read-only, prints List-Unsubscribe links).
- **Why:** Paridhi asked to unsubscribe from MJH, CareerConnects, US Navy, and other weird job boards sending unrelated positions.
- **When:** Nov 25, 2026.
- **Log:** find_unsubscribe.py found links for MJH and CareerConnects (3 mails each, same token per sender). Paridhi clicked one link per sender and confirmed unsubscribe. US Navy / Veterans Affairs alerts came via CareerConnects, so they stop with that unsubscribe.
- Batch 2, Nov 25: Jobsora unsubscribed via Gmail's Unsubscribe button (pasted list-unsubscribe link gave 405 Method Not Allowed — Gmail's button works, pasted link does not). CareerCircle is KEEP — Paridhi said Nov 25 it is important, do NOT unsubscribe; commented out of find_unsubscribe.py. WallStreetQuants: 0 recent mail, nothing to do.
