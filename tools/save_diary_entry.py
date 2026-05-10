import os
from datetime import datetime

DIARY_DIR = os.path.join(os.path.dirname(__file__), "..", "diary")


def save_diary_entry(user_text: str, ai_response: str) -> str:
    os.makedirs(DIARY_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M")
    filepath = os.path.join(DIARY_DIR, f"{today}.md")

    entry = f"\n## Entry — {timestamp}\n\n**You:** {user_text}\n\n**Bell:** {ai_response}\n\n---\n"

    with open(filepath, "a") as f:
        f.write(entry)

    return filepath


if __name__ == "__main__":
    path = save_diary_entry("This is a test entry.", "This is a test AI response.")
    print(f"Saved to: {path}")
