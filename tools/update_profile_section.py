import json
import os
import copy

PROFILE_DIR = os.path.join(os.path.dirname(__file__), "..", "profile")

VALID_SECTIONS = [
    "background", "personality", "feelings", "wardrobe",
    "goals", "schedule", "habits", "relationships", "notes",
]


def _deep_merge(base: dict, updates: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def update_profile_section(section: str, updates: dict) -> dict:
    if section not in VALID_SECTIONS:
        return {"error": f"Unknown section '{section}'. Valid: {VALID_SECTIONS}"}

    path = os.path.join(PROFILE_DIR, f"{section}.json")

    try:
        with open(path, "r") as f:
            current = json.load(f)
    except FileNotFoundError:
        return {"error": f"{section}.json not found"}
    except json.JSONDecodeError:
        return {"error": f"{section}.json is malformed"}

    changed_keys = [k for k, v in updates.items() if current.get(k) != v]
    updated = _deep_merge(current, updates)

    with open(path, "w") as f:
        json.dump(updated, f, indent=2)

    return {"saved": True, "section": section, "changed_keys": changed_keys}


if __name__ == "__main__":
    result = update_profile_section("notes", {"preferred_response_style": "direct and concise"})
    print(result)
