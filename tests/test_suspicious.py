# test_suspicious.py — Tests for suspicious, with fake text only.

from suspicious import is_suspicious


def test_suspicious_phrases():
    assert is_suspicious("Someone", "Confirm your password", "") is True
    assert is_suspicious("Someone", "You have won a prize, click here to claim", "") is True


def test_not_suspicious():
    assert is_suspicious("Someone", "Verify your account now", "") is False
    assert is_suspicious("Someone", "Update your payment", "") is False
    assert is_suspicious("Someone", "Your account will be closed", "") is False
    assert is_suspicious("Someone", "Urgent action required", "") is False
    assert is_suspicious("NVIDIA", "Your Personalized Developer News", "") is False
    assert is_suspicious("Substack", "New notes posted", "") is False
    assert is_suspicious("CareerCircle", "IBM SkillsBuild Virtual Career Fair", "") is False


def test_elytespark():
    assert is_suspicious("aditya_kumar@elytespark.com", "Internship Opportunity for Students & Recent Graduates", "A small program fee is applicable") is True