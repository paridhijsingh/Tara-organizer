# categorize.py — Suggest a Gmail category for a mail, read-only.
# No mail is moved here. Tara shows the suggestion, Paridhi approves it first.

def suggest_category(sender, subject, snippet):
    """Return a suggested category: Promotions, Social, Updates, or Important."""
    text = f"{sender} {subject} {snippet}".lower()

    # Important first — same idea as the briefing filter
    important_words = ["application", "interview", "recruiter", "screening", "offer", "hiring", "applied", "substack", "tldr", "tech", "daily dose"]
    exclude_words = ["job alert", "applications needed", "hiring now", "position is vacant", "job feed", "must hire", "cyber sale", "black friday", "blowout", "% off"]
    if any(word in text for word in exclude_words):
        pass
    elif any(word in text for word in important_words):
        return "Important"

    # Promotions: sales, discounts, offers
    if any(word in text for word in ["sale", "discount", "% off", "coupon", "deal", "offer", "promo"]):
        return "Promotions"

    # Social: social networks, people
    if any(word in text for word in ["facebook", "instagram", "linkedin", "twitter", "social"]):
        return "Social"

    # Updates: everything else that is a notification / update
    return "Updates"
