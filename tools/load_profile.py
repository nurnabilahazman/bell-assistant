import json
import os

PROFILE_DIR = os.path.join(os.path.dirname(__file__), "..", "profile")

SECTIONS = {
    "background":    "BACKGROUND",
    "personality":   "PERSONALITY",
    "feelings":      "CURRENT FEELINGS",
    "wardrobe":      "WARDROBE & STYLE",
    "goals":         "GOALS",
    "schedule":      "SCHEDULE",
    "habits":        "HABITS",
    "relationships": "RELATIONSHIPS",
    "notes":         "PERSONAL NOTES",
}


def _format_value(value, indent=0):
    pad = "  " * indent
    if isinstance(value, list):
        if not value:
            return "(empty)"
        items = []
        for item in value:
            if isinstance(item, dict):
                sub = ", ".join(f"{k}: {v}" for k, v in item.items())
                items.append(f"{pad}- {sub}")
            else:
                items.append(f"{pad}- {item}")
        return "\n" + "\n".join(items)
    elif isinstance(value, dict):
        lines = []
        for k, v in value.items():
            formatted = _format_value(v, indent + 1)
            lines.append(f"{pad}{k.replace('_', ' ').title()}: {formatted}")
        return "\n" + "\n".join(lines)
    else:
        return str(value) if value else "(not set)"


def load_profile() -> str:
    sections = []
    for filename, label in SECTIONS.items():
        path = os.path.join(PROFILE_DIR, f"{filename}.json")
        try:
            with open(path, "r") as f:
                data = json.load(f)
            lines = [f"## {label}"]
            for key, value in data.items():
                formatted = _format_value(value)
                lines.append(f"{key.replace('_', ' ').title()}: {formatted}")
            sections.append("\n".join(lines))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print(f"Warning: {filename}.json is malformed — skipping")
    return "\n\n".join(sections)


if __name__ == "__main__":
    print(load_profile())
