import os
import glob

DIARY_DIR = os.path.join(os.path.dirname(__file__), "..", "diary")


def list_diary_entries(last_n: int = 7, keyword: str = None) -> list:
    os.makedirs(DIARY_DIR, exist_ok=True)
    files = sorted(glob.glob(os.path.join(DIARY_DIR, "*.md")), reverse=True)

    if not files:
        return []

    results = []

    for filepath in files:
        filename = os.path.basename(filepath)
        date_str = filename.replace(".md", "")

        try:
            with open(filepath, "r") as f:
                content = f.read()
        except Exception:
            continue

        if keyword and keyword.lower() not in content.lower():
            continue

        lines = [l.strip() for l in content.split("\n") if l.strip()]
        preview = lines[1] if len(lines) > 1 else "(empty)"

        results.append({
            "date": date_str,
            "path": filepath,
            "preview": preview[:120],
            "full": content if keyword else None,
        })

        if not keyword and len(results) >= last_n:
            break

    return results


if __name__ == "__main__":
    import pprint
    entries = list_diary_entries(last_n=5)
    if entries:
        pprint.pprint(entries)
    else:
        print("No diary entries yet.")
