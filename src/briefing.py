# briefing.py — Build Tara's morning briefing from three pieces:
# today's calendar events, important unread Gmail, and top deadlines.

def build_briefing(events, emails, deadlines):
    """Return the morning briefing as one string.

    events: list of {time, title, attendees} from calendar_client.py
    emails: list of {sender, subject, snippet} from gmail_client.py
    deadlines: list of {date, title} from deadlines.py
    """
    lines = []
    lines.append("Good morning, Paridhi — here's your day with Tara.")
    lines.append("")

    # 1. Calendar
    lines.append("Today's calendar:")
    if not events:
        lines.append("- No events today.")
    else:
        for event in events:
            lines.append(f"- {event['time']} — {event['title']}")

    lines.append("")

    # 2. Important Gmail
    lines.append("Important unread mail:")
    if not emails:
        lines.append("- Nothing important unread.")
    else:
        for email in emails:
            lines.append(f"- {email['sender']}: {email['subject']}")

    lines.append("")

    # 3. Deadlines
    lines.append("Top deadlines:")
    if not deadlines:
        lines.append("- No deadlines listed.")
    else:
        for deadline in deadlines:
            lines.append(f"- {deadline['date']} — {deadline['title']}")

    return "\n".join(lines)
