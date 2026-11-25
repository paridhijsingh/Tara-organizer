# job_status.py — Classify a Job Applications email by status and by type.
# Read-only, moves nothing.
# Status: Active, Not moving forward, Inactive, or Unsure.
# Type: Full-time, Intern, or "" (not stated).

REJECTION_PHRASES = [
    "we regret to inform you",
    "we have decided to move forward with other candidates",
    "decided to move forward with other candidates",
    "will not be moving forward",
    "we will not be moving forward",
    "not selected",
    "unfortunately, we have decided",
    "after careful consideration, we will not",
    "we have chosen to pursue other candidates",
]

ACTIVE_PHRASES = [
    "thanks for applying",
    "thank you for applying",
    "we will reach out shortly",
    "we'll be in touch",
    "we will be in touch",
    "application received",
    "we received your application",
    "we have received your application",
]

INACTIVE_PHRASES = [
    "job has expired",
    "position has expired",
    "posting has expired",
    "no longer accepting applications",
    "this job is no longer available",
    "this position has been closed",
]


def classify_job_email(text):
    """Return Active, Not moving forward, Inactive, or Unsure."""
    text = text.lower()
    if any(phrase in text for phrase in REJECTION_PHRASES):
        return "Not moving forward"
    if any(phrase in text for phrase in INACTIVE_PHRASES):
        return "Inactive"
    if any(phrase in text for phrase in ACTIVE_PHRASES):
        return "Active"
    return "Unsure"


def classify_job_type(text):
    """Return Full-time, Intern, or '' if the type is not stated."""
    text = text.lower()
    if "intern" in text:
        return "Intern"
    if "full-time" in text or "full time" in text:
        return "Full-time"
    return ""