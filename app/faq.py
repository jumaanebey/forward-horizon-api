from typing import Optional

FAQ_KB = [
    ("pricing", "Our pricing is flexible. Most plans start at $99/mo. Want details?"),
    ("price", "Our pricing is flexible. Most plans start at $99/mo. Want details?"),
    ("free", "We offer a free trial. Would you like me to set that up?"),
    ("trial", "We offer a free trial. Would you like me to set that up?"),
    ("cancel", "You can cancel anytime from your dashboard or by replying CANCEL."),
    ("support", "You can reach support 24/7 via this thread or support@example.com."),
]


def answer_for(text: str) -> Optional[str]:
    lower = text.lower()
    for keyword, reply in FAQ_KB:
        if keyword in lower:
            return reply
    return None