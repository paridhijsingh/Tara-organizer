# CHANGELOG

Format for every entry: **Date**, **What**, **Why**, **When**, **Log**.

---

### 2026-11-21 — Setup

| Field    | Detail                                                                                                   |
| -------- | -------------------------------------------------------------------------------------------------------- |
| **Date** | 2026-11-21                                                                                               |
| **What** | Repo `tara-organizer`, venv, `.gitignore`, `requirements.txt`; pip install succeeded                     |
| **Why**  | Bootstrap the project so Tara can use Google APIs safely                                                 |
| **When** | 2026-11-21                                                                                               |
| **Log**  | Installed `google-api-python-client` 2.202.0, `google-auth-oauthlib` 1.5.0, `google-auth-httplib2` 0.4.4 |

---

### 2026-11-21 — Google Cloud access

| Field    | Detail                                                                                                                                                                                                       |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Date** | 2026-11-21                                                                                                                                                                                                   |
| **What** | Google Cloud project `tara-organizer`; Gmail + Calendar APIs enabled; OAuth consent created; test user `paridhijaysingh@gmail.com`; OAuth client Desktop app; `credentials.json` in repo folder (gitignored) |
| **Why**  | Enable read-only Calendar and Gmail access for the morning briefing                                                                                                                                          |
| **When** | 2026-11-21                                                                                                                                                                                                   |
| **Log**  | Project, APIs, consent screen, Desktop OAuth client, and local credentials ready; secrets stay out of git                                                                                                    |

---

### 2026-11-21 — Plan created

| Field    | Detail                                                                                                 |
| -------- | ------------------------------------------------------------------------------------------------------ |
| **Date** | 2026-11-21                                                                                             |
| **What** | Full plan Phase 0–7 written to `PLAN.md`, plus `SKILL.md`, `RULES.md`, and this changelog              |
| **Why**  | Plan first before coding                                                                               |
| **When** | 2026-11-21                                                                                             |
| **Log**  | Docs only — no feature code yet; later revised to drop hard-coded sender list and add Phase 2 cleaning |

---

### 2026-11-21 — Gmail + desktop cleaning decided

| Field    | Detail                                                                                                                                             |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Date** | 2026-11-21                                                                                                                                         |
| **What** | Phase 2 includes suspicious-mail flagging, categorizing (Promotions/Social/Updates), and desktop tidy — all approval-gated                         |
| **Why**  | Clean inbox and desktop without silent automation or auto-spam / auto-archive                                                                      |
| **When** | 2026-11-21                                                                                                                                         |
| **Log**  | Suspicious: flag → Paridhi reviews → Spam only after approval. Categorize and desktop moves: propose, approve each batch/move. Never auto-archive. |

---

### 2026-11-21 — Gmail folders + bookmarks decided

| Field    | Detail                                                                                                                                                                   |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Date** | 2026-11-21                                                                                                                                                               |
| **What** | Phase 2 includes Gmail label/folder reduction and bookmark organization — approval every change                                                                          |
| **Why**  | Reduce duplicate/unused labels and tidy bookmarks without losing mail or links                                                                                           |
| **When** | 2026-11-21                                                                                                                                                               |
| **Log**  | Labels: list → propose merges/deletes → approve each; never delete mail. Bookmarks: list → propose folders/merges/dead links → approve each move; never lose a bookmark. |

### 2026-11-21 — Calendar Step 1 done

- **Date:** 2026-11-21
- **What:** Created calendar_client.py with get_today_events() — read-only, calendar.readonly scope only
- **Why:** Step 1 in Tara's plan — today's calendar is the first piece of the morning briefing
- **When:** Phase 1, Step 1
- **Log:** python calendar_client.py ran with no error, printed no events — today is empty in Google Calendar. token.json saved (762 bytes), gitignored, not in git status. Fixed a missing ZoneInfo import along the way.

### 2026-11-21 — Gmail Step 2 done, "important" v2

- **Date:** 2026-11-21
- **What:** Created gmail_client.py with get_important_unread() — read-only, gmail.readonly scope only, with is_important() filter
- **Why:** Step 2 in Tara's plan — important unread Gmail is the second piece of the morning briefing
- **When:** Phase 1, Step 2
- **Log:** First run returned 10 unread, all noise. Filter v1 matched CareerConnects job alerts ("APPLICATIONS NEEDED", "Hiring now") — false positives. Filter v2 added EXCLUDE_WORDS (job alert, applications needed, hiring now, position is vacant, job feed) — second run printed nothing, correctly. "Important" is a living definition, we will keep refining it.

## 2026-11-22 — Step 3: Briefing done

- **What:** Added deadlines.py (hand-edited list: Vastra judging Dec 1, FinPath results Dec 10, HPE screening Dec 24), briefing.py (build_briefing), main.py (python main.py prints the briefing), test_briefing.py (3 tests).
- **Why:** The briefing is Tara's one job in Phase 1 — calendar + important Gmail + deadlines in one morning message.
- **When:** Nov 22, 2026.
- **Log:** Live run printed no events, 1 important mail (Chrisnotes), 3 deadlines. First run had 2 false positives (MJH job alert, Carnival sale) — filter v3 added "must hire", "myjobhelper", "cyber sale", "early access", "carnival" to EXCLUDE_WORDS, Chrisnotes kept on purpose. pytest -q: 3 passed.

## 2026-11-22 — Phase 2: Morning message by email

- **What:** Added send_briefing.py (emails the briefing to paridhijaysingh@gmail.com only), added gmail.send to auth.py, re-authorized once, scheduled it with cron at 8am daily (0 8 \* \* \*), logging to tara.log.
- **Why:** Phase 1 was a terminal command; Phase 2 makes Tara message Paridhi each morning.
- **When:** Nov 22, 2026.
- **Log:** Test email landed Nov 22 at 4:07 PM, correct briefing inside. crontab -l confirms the 8am schedule. Filter v4: AlgoMonster is noise, excluded. Text messages are later, not yet built.

## 2026-11-22 — Phase 2: Gmail categorizing and label cleaning, part 1

- **What:** Added categorize.py (suggest_category: Promotions / Social / Updates / Important), propose_categories.py (read-only proposals), list_labels.py (read-only label list), clean_applications_labels.py (deletes 5 approved labels by ID), test_categorize.py (3 tests). Added gmail.modify to auth.py, re-authorized once.
- **Why:** Gmail had ~200 labels; Tara proposes categories and helps decide which labels to combine and clean, with Paridhi approving each batch.
- **When:** Nov 22, 2026.
- **Log:** pytest -q: 6 passed. Live propose run: Daily Dose + Chrisnotes Important, Carnival + Algo Monster Promotions. Deleted, approved: Applications/FAFSA, Applications/Santa Barbara, Applications/Indian Universities, Applications/CSS Profile, Applications/University of California. Parent Applications kept, mail never deleted, Job Applications and Substacks untouched.

## 2026-11-22 — Phase 2: Gmail categorizing, first approved move

- **What:** Added apply_categories.py. Applied the approved batch of 10 unread mails.
- **Why:** Tara proposes first, Paridhi approves, then Tara moves only the approved mail.
- **When:** Nov 22, 2026.
- **Log:** Moved 8: Carnival + Algo Monster to Promotions; OpenRouter, Chris Ching, Apollo, WallStreetQuants, CareerCircle, MJH to Updates. Left alone: Daily Dose + Chrisnotes (Important). Nothing deleted, archived, or marked read.
