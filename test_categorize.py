# test_categorize.py — Tests for suggest_category, with fake data only.

from categorize import suggest_category


def test_important_newsletter():
    assert suggest_category("chrispathway", "Everything in AI/tech", "") == "Important"


def test_promotion():
    assert suggest_category("Carnival", "Cyber Sale", "20% OFF") == "Promotions"


def test_updates_fallback():
    assert suggest_category("OpenRouter", "How models score", "") == "Updates"
