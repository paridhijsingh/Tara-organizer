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

### Why it exists

### How it works

### What it does NOT do

### How to test it

### What changed, and when
