from datetime import datetime

SESSION_KEYWORDS = {
    "morning":       ["good morning", "morning briefing", "morning brief", "daily brief"],
    "diary":         ["diary", "journal", "i want to reflect", "want to reflect", "vent", "i want to write", "reflection"],
    "wardrobe":      ["what should i wear", "outfit", "what to wear", "does this match", "style advice", "get dressed", "wearing today"],
    "update":        ["update my", "change my", "add to my", "save to my profile", "edit my profile"],
    "goals":         ["goal check", "check my goals", "goals check", "goal check-in", "review my goals"],
    "feelings":      ["how i'm feeling", "i'm feeling", "check in on feelings", "emotional check", "mental health check"],
    "weekly_review": ["weekly review", "week review", "end of week", "weekly check", "review my week"],
    "schedule":      ["plan my day", "plan my week", "help me plan", "schedule my day", "plan for today"],
}


def detect_session(user_input: str, is_first_message: bool = False) -> str:
    now = datetime.now()
    text = user_input.lower().strip()

    if is_first_message and not text and now.hour < 10:
        return "morning"

    for session_type, keywords in SESSION_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return session_type

    return "chat"
