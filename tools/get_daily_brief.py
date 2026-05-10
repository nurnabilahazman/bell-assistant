import json
import os
from datetime import datetime

PROFILE_DIR = os.path.join(os.path.dirname(__file__), "..", "profile")


def get_daily_brief() -> dict:
    path = os.path.join(PROFILE_DIR, "schedule.json")
    try:
        with open(path, "r") as f:
            schedule = json.load(f)
    except FileNotFoundError:
        return {"error": "schedule.json not found"}
    except json.JSONDecodeError:
        return {"error": "schedule.json is malformed"}

    today = datetime.now().strftime("%A").lower()

    return {
        "today": datetime.now().strftime("%A, %B %d, %Y"),
        "todays_targets": schedule.get("todays_targets", []),
        "recurring_today": schedule.get("weekly_recurring", {}).get(today, []),
        "morning_routine": schedule.get("morning_routine", []),
        "work_hours": schedule.get("work_hours", ""),
        "evening_routine": schedule.get("evening_routine", []),
        "sleep_time": schedule.get("sleep_time", ""),
    }


if __name__ == "__main__":
    import pprint
    pprint.pprint(get_daily_brief())
