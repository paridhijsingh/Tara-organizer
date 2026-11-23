# Tara Manual

Tara's textbook — one chapter per feature, in plain language.

---

## Chapter 1 — Auth (shared sign-in)

### What it is

One shared sign-in for Tara, in `auth.py`, so Calendar and Gmail both use the same token.

### Why it exists

Tara needs to read Google Calendar and Gmail, read-only, without signing in twice.

### How it works

1. **Input:** Local `credentials.json` (OAuth Desktop client) and, if present, `token.json`.
2. **Steps:** `get_credentials()` in `auth.py`:
   - If `token.json` exists, load it.
   - If the token is expired, refresh it.
   - If there is no sign-in, open the browser with `InstalledAppFlow` using `credentials.json`, then save the new sign-in to `token.json`.
3. **Output:** Valid OAuth credentials for Google APIs.
4. **Scopes (read-only only):** `calendar.readonly` and `gmail.readonly`.

### What it does NOT do

- Never sends, deletes, or moves mail
- Never creates or edits events
- Never commits `credentials.json` or `token.json` — both are gitignored

### How to test it

Run `python calendar_client.py` — it should open the browser once, then save `token.json` and run with no error.

### What changed, and when

See [CHANGELOG.md](CHANGELOG.md) — **2026-11-21, Step 2:** moved the sign-in out of `calendar_client.py` into shared `auth.py`, added the Gmail scope, re-authorized once. (Related: Gmail Step 2 entry.)

---

## Chapter 2 — Calendar: today's events

### What it is

`get_today_events()` in `calendar_client.py` — returns today's calendar events.

### Why it exists

Today's calendar is the first piece of the morning briefing.

### How it works

1. **Input:** Credentials from `get_credentials()` in `auth.py`.
2. **Steps:** In `calendar_client.py` → `get_today_events()`:
   - Build the Calendar service with `get_credentials()`.
   - Work out today `00:00`–`23:59` in `America/Los_Angeles`.
   - Call `events().list()` with `singleEvents=True`, `orderBy=startTime`.
3. **Output:** A list of `{time, title, attendees}`. All-day events show the date instead of a time.

### What it does NOT do

Read-only only. Never creates, edits, or deletes an event.

### How to test it

Run `python calendar_client.py` — it should print today's events, or nothing if today is empty. On Nov 21 it printed nothing, correctly, because today was empty.

### What changed, and when

See [CHANGELOG.md](CHANGELOG.md) — **2026-11-21, Step 1:** first feature built, fixed a missing `ZoneInfo` import along the way. (Entry: Calendar Step 1 done.)

---

## Chapter 3 — Gmail: important unread mail

### What it is

`get_important_unread()` in `gmail_client.py` — returns important unread mail.

### Why it exists

Important unread Gmail is the second piece of the morning briefing — but only the important mail, not every unread mail.

### How it works

1. **Input:** Credentials from `get_credentials()` in `auth.py`.
2. **Steps:** In `gmail_client.py` → `get_important_unread()`:
   - Build the Gmail service with `get_credentials()`.
   - List up to 10 unread messages with `q="is:unread"`.
   - Fetch sender / subject / snippet for each.
   - Keep only the ones `is_important()` says are important.
3. **Output:** A filtered list of important unread messages.

**What "important" means:** Mail about companies she applies to (application / interview / recruiter / screening / offer / hiring), **plus** Substacks, TLDR, and the tech newsletters she subscribes to. Job alerts / job feeds, promotions, and sales are **not** important. "Important" is a living definition — we keep refining it as Tara runs.

### What it does NOT do

Read-only only. No specific-sender list, no archiving, no labelling, no moving mail, no auto-archiving ever.

### How to test it

Run `python gmail_client.py` — first run returned 10 unread, all noise. Filter v1 matched CareerConnects job alerts ("APPLICATIONS NEEDED", "Hiring now") — false positives. Filter v2 added `EXCLUDE_WORDS` (job alert, applications needed, hiring now, position is vacant, job feed) — second run printed nothing, correctly.

### What changed, and when

See [CHANGELOG.md](CHANGELOG.md) — **2026-11-21, Step 2:** first version, then v2 filter fix. (Entry: Gmail Step 2 done, "important" v2.)

---

## Chapter 4 — Briefing

### What it is

build_briefing() in briefing.py — turns today's calendar, important unread Gmail, and top deadlines into one morning briefing. main.py runs it all with python main.py.

### Why it exists

The briefing is Tara's one job in Phase 1 — one clear message in the morning, instead of checking three places yourself.

### How it works

1. Input: events from get_today_events(), emails from get_important_unread(), deadlines from get_deadlines().
2. Steps: main.py calls all three, hands them to build_briefing(), which writes three sections — Today's calendar, Important unread mail, Top deadlines — with one line per event / email / deadline.
3. Output: One printed string, starting "Good morning, Paridhi — here's your day with Tara."

### What it does NOT do

Read-only only. It never sends, deletes, or moves mail, never creates or edits events, and never adds deadlines by itself — deadlines.py is hand-edited by Paridhi.

### How to test it

Run pytest -q — 3 tests pass: empty day, one event + one email, deadlines show up.
Run python main.py live — on Nov 22 it printed no events, one important mail (Chrisnotes, kept on purpose), and three deadlines. Filter v3 fixed two false positives first: MJH job alert ("must hire") and Carnival Cyber Sale.

### What changed, and when

See CHANGELOG.md — 2026-11-22, Step 3: deadlines.py, briefing.py, main.py, test_briefing.py added; Gmail filter v3.

## Chapter 5 — Morning message by email

### What it is

send_briefing.py — sends Tara's morning briefing by email to Paridhi, every morning at 8am.

### Why it exists

Phase 1 was a terminal command — you had to run Tara yourself. Phase 2 makes Tara message you, so the briefing arrives without you running anything.

### How it works

1. Input: the same three pieces as the briefing — events, important mail, deadlines.
2. Steps: send_briefing.py builds the briefing with build_briefing(), makes an email to paridhijaysingh@gmail.com with subject "Tara — your morning briefing", and sends it with the Gmail API.
3. Schedule: a cron job on Paridhi's Mac — 0 8 \* \* \* — runs send_briefing.py at 8am every day, and logs to tara.log.
4. Output: An email in her inbox, from herself, with the briefing inside.

### What it does NOT do

Sends ONLY to paridhijaysingh@gmail.com, never to anyone else. It never sends on its own without the schedule, and it never changes the briefing — it sends the same text main.py prints. Text messages are later, not yet built.

### How to test it

Run python send_briefing.py by hand once — on Nov 22 it landed in the inbox at 4:07 PM, with the right calendar, Chrisnotes, and deadlines. Run crontab -l to check the schedule is saved.

### What changed, and when

See CHANGELOG.md — 2026-11-22, Phase 2: added gmail.send to auth.py scopes, re-authorized once, added send_briefing.py, added the 8am cron job. Filter v4 excluded AlgoMonster ("black friday", "blowout", "% off", "algo monster").

## Chapter 6 — Gmail categorizing and label cleaning

### What it is

categorize.py suggests a category for a mail (Promotions, Social, Updates, Important). propose_categories.py shows those suggestions for up to 10 unread mails. list_labels.py lists all Gmail labels. clean_applications_labels.py deletes only the labels Paridhi approved.

### Why it exists

Gmail had about 200 labels, and unread mail was a mix of important mail, promotions, and job alerts. Tara helps decide what each mail is, and which labels to combine and clean, so the inbox stays tidy.

### How it works

1. Input: sender + subject + snippet for each unread mail, and the full label list from Gmail.
2. Steps: suggest_category() checks important words first (application, interview, recruiter, substack, tldr, tech, daily dose), then promotions words (sale, discount, % off), then social words, then falls back to Updates. Exclude words (job alert, must hire, cyber sale, black friday, algo monster) stop a mail being called Important.
3. Output: propose_categories.py prints [Category] sender: subject for each mail. list_labels.py prints name — type (id) for each label.
4. Labels: Paridhi approved deleting 5 old college Applications sub-labels only. clean_applications_labels.py deletes them by exact label ID.

### What it does NOT do

Proposing moves nothing. Deleting a label never deletes mail — mail stays in All Mail / Inbox. Tara never moves mail or deletes a label without Paridhi approving that exact batch first. Job Applications and Substacks labels were not touched in this step.

### How to test it

Run pytest -q — 6 passed (3 briefing + 3 categorize). Run python propose_categories.py — on Nov 22 it showed Daily Dose and Chrisnotes as Important, Carnival and Algo Monster as Promotions, the rest as Updates. Run python list_labels.py | grep Applications — after cleaning, only the parent Applications label remains, plus all Job Applications labels.

### What changed, and when

See CHANGELOG.md — 2026-11-22, Phase 2: added categorize.py, propose_categories.py, list_labels.py, clean_applications_labels.py, test_categorize.py; added gmail.modify to auth.py; deleted 5 Applications sub-labels.

Also, Nov 22: apply_categories.py added — applies the suggested Promotions / Social / Updates label to approved mail only, leaves Important mail alone, never deletes, archives, or marks mail as read. First approved batch moved 8 mails, left 2 Important alone.

Also, Nov 22: clean_substacks_labels.py added — deletes all Substacks/<name> sub-labels by name prefix, keeps the parent Substacks label. Deleted 43 sub-labels, mail never deleted. Paridhi has not been reading Substacks lately, so they were collapsed into the parent; a per-newsletter label can be made again later if she resumes reading one.
