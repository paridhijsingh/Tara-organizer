# suspicious.py — Flag suspicious mail for Paridhi to review.
# Read-only, moves nothing.

SUSPICIOUS_PHRASES = [
    "confirm your password",
    "click here to claim",
    "you have won",
    "program fee is applicable",
    "placement assured",
]

SUSPICIOUS_SENDERS = [
    "support@",
    "security@",
    "noreply@",
]


def is_suspicious(sender, subject, snippet):
    """Return True if the mail looks suspicious, else False."""
    text = f"{sender} {subject} {snippet}".lower()
    return any(phrase in text for phrase in SUSPICIOUS_PHRASES)