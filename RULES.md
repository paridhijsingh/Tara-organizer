# Tara — Standing Rules

1. Plan first; one feature at a time — docs first, then Step 1 only; do not build Gmail, briefing, or anything else yet.
2. Read-only first in Phase 1; scopes are `gmail.readonly` and `calendar.readonly` only — no sending, deleting, moving, or creating events.
3. No secrets in git, ever — `credentials.json`, `token.json`, `.env`, `.venv/` are gitignored; never commit them.
4. Personal Gmail only (`paridhijaysingh@gmail.com`) — no work Gmail.
5. No specific-sender list — do not hard-code specific senders / emails as “important”.
6. No auto-archiving, ever — Phase 1 only reads and shows mail; never archives, labels, or moves it automatically.
7. Gmail cleaning, categorizing, suspicious mail, folder reduction, bookmarks, and desktop tidy are Phase 2 only — approval every time (flag suspicious for review first; never auto-spam; approve each categorize batch; propose label merges/deletes only, never delete mail; bookmarks and desktop moves only after approval; never lose a bookmark or auto-move/delete a file).
8. Paridhi writes the code — explain the approach first, show small steps, review her code; do not silently build the whole file for her.
9. Log every change in `CHANGELOG.md` — Date, What, Why, When, Log.
10. No hallucinating — show sources; fail safe.
11. Nothing sends without approval.
12. Test before calling it done.
13. Change one thing at a time.
14. Privacy / OSpectra stays out.
