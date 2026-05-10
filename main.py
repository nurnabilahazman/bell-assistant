import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

import agent
from session_router import detect_session
from tools.get_daily_brief import get_daily_brief
from tools.list_diary_entries import list_diary_entries
from tools.load_profile import load_profile
from tools.save_diary_entry import save_diary_entry
from tools.update_profile_section import update_profile_section

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")


def load_prompt(name: str) -> str:
    with open(os.path.join(PROMPTS_DIR, f"{name}.txt"), "r") as f:
        return f.read()


def build_system_prompt(profile_context: str) -> str:
    prompt = load_prompt("base_system")
    today = datetime.now()
    prompt = prompt.replace("{PROFILE_CONTEXT}", profile_context)
    prompt = prompt.replace("{TODAY_DATE}", today.strftime("%B %d, %Y"))
    prompt = prompt.replace("{DAY_OF_WEEK}", today.strftime("%A"))
    return prompt


def handle_morning(system_prompt: str, messages: list):
    brief = get_daily_brief()
    if "error" in brief:
        brief_context = "(Schedule not set up yet.)"
    else:
        targets = "\n".join(f"  - {t}" for t in brief.get("todays_targets", [])) or "  (none set)"
        recurring = "\n".join(f"  - {r}" for r in brief.get("recurring_today", [])) or "  (none set)"
        brief_context = (
            f"Today's targets:\n{targets}\n\n"
            f"Today's schedule:\n{recurring}\n\n"
            f"Work hours: {brief.get('work_hours', '(not set)')}"
        )

    morning_prompt = load_prompt("morning_briefing") + f"\n\n{brief_context}"
    print("\nBell: ", end="")
    reply = agent.chat(system_prompt, messages, morning_prompt)
    messages.append({"role": "user", "content": morning_prompt})
    messages.append({"role": "assistant", "content": reply})
    print()


def handle_diary(system_prompt: str, messages: list, initial_input: str = ""):
    print("\nBell: I'm here. Write what's on your mind.\n")

    if initial_input:
        user_text = initial_input
        print(f"You: {user_text}")
    else:
        print("You: ", end="")
        user_text = input().strip()

    if not user_text:
        print("Bell: Whenever you're ready.\n")
        return

    diary_prompt = load_prompt("diary").replace("{USER_DIARY_TEXT}", user_text)

    print("\nBell: ", end="")
    reply = agent.chat(system_prompt, messages, diary_prompt)
    messages.append({"role": "user", "content": diary_prompt})
    messages.append({"role": "assistant", "content": reply})

    print("\nSave this entry? (y/n): ", end="")
    try:
        if input().strip().lower() == "y":
            path = save_diary_entry(user_text, reply)
            print(f"[Saved → {os.path.basename(path)}]\n")
    except (KeyboardInterrupt, EOFError):
        pass


def handle_wardrobe(system_prompt: str, messages: list, initial_input: str = ""):
    print()
    occasion = input("Occasion: ").strip() or "casual"
    vibe = input("Vibe/mood: ").strip() or "comfortable"
    constraints = input("Constraints (weather, dress code — or press Enter to skip): ").strip() or "none"

    wardrobe_prompt = (
        load_prompt("wardrobe")
        .replace("{OCCASION}", occasion)
        .replace("{VIBE OR MOOD}", vibe)
        .replace("{CONSTRAINTS}", constraints)
    )

    print("\nBell: ", end="")
    reply = agent.chat(system_prompt, messages, wardrobe_prompt)
    messages.append({"role": "user", "content": wardrobe_prompt})
    messages.append({"role": "assistant", "content": reply})
    print()


def handle_schedule(system_prompt: str, messages: list, user_input: str):
    schedule_prompt = (
        load_prompt("schedule_planning")
        .replace("{today / this week / specific day}", "today")
        .replace("{USER LISTS THEIR COMMITMENTS OR LEAVES BLANK}", user_input)
    )
    print("\nBell: ", end="")
    reply = agent.chat(system_prompt, messages, schedule_prompt)
    messages.append({"role": "user", "content": schedule_prompt})
    messages.append({"role": "assistant", "content": reply})
    print()


def handle_goals(system_prompt: str, messages: list):
    print("\nBell: ", end="")
    reply = agent.chat(system_prompt, messages, load_prompt("goal_checkin"))
    messages.append({"role": "user", "content": "goal check-in"})
    messages.append({"role": "assistant", "content": reply})
    print()


def handle_feelings(system_prompt: str, messages: list, user_input: str):
    feelings_prompt = load_prompt("feelings_checkin").replace(
        "{USER DESCRIBES THEIR FEELINGS OR LEAVES BLANK TO START OPEN-ENDED}", user_input
    )
    print("\nBell: ", end="")
    reply = agent.chat(system_prompt, messages, feelings_prompt)
    messages.append({"role": "user", "content": feelings_prompt})
    messages.append({"role": "assistant", "content": reply})
    print()


def handle_weekly_review(system_prompt: str, messages: list):
    # Pull any diary entries from this week to give AI context
    entries = list_diary_entries(last_n=7)
    context = ""
    if entries:
        context = "\n\nDiary entries this week:\n"
        for e in entries:
            context += f"\n### {e['date']}\n{e['preview']}...\n"

    weekly_prompt = load_prompt("weekly_review") + context
    print("\nBell: ", end="")
    reply = agent.chat(system_prompt, messages, weekly_prompt)
    messages.append({"role": "user", "content": weekly_prompt})
    messages.append({"role": "assistant", "content": reply})
    print()


def handle_update(system_prompt: str, messages: list):
    valid = "background / personality / feelings / wardrobe / goals / schedule / habits / relationships / notes"
    print(f"\nSection ({valid}): ", end="")
    section = input().strip().lower()
    print(f"What to change in '{section}'? ", end="")
    change_desc = input().strip()

    extract_prompt = (
        f"The user wants to update their '{section}' profile section. "
        f"They said: '{change_desc}'. "
        "Extract the key-value pairs to update as a valid JSON object. "
        "Reply with ONLY the JSON object, no explanation, no markdown."
    )

    raw = agent.chat(system_prompt, [], extract_prompt, stream=False)

    try:
        # Strip markdown code fences if model adds them
        clean = raw.strip().strip("```json").strip("```").strip()
        updates = json.loads(clean)
        print(f"\nAbout to save to {section}.json:")
        print(json.dumps(updates, indent=2))
        print("Confirm? (y/n): ", end="")
        if input().strip().lower() == "y":
            result = update_profile_section(section, updates)
            if result.get("saved"):
                print(f"[Bell] Saved. Changed fields: {result.get('changed_keys', [])}\n")
            else:
                print(f"[Bell] Error: {result.get('error')}\n")
    except (json.JSONDecodeError, ValueError):
        print(f"\n[Bell] Couldn't parse that into a clean update. You can edit {section}.json directly.\n")


def main():
    print("\n── Bell ──────────────────────────────────")
    print("Loading your profile...\n")

    try:
        profile_context = load_profile()
        system_prompt = build_system_prompt(profile_context)
    except Exception as e:
        print(f"[Error loading profile: {e}]")
        print("Make sure your profile/ JSON files exist and are valid.")
        return

    messages = []
    now = datetime.now()

    if now.hour < 10:
        handle_morning(system_prompt, messages)

    print("──────────────────────────────────────────")
    print("Commands: /diary  /wardrobe  /goals  /week  /update  /quit")
    print("Or just talk naturally.\n")

    while True:
        try:
            print("You: ", end="")
            user_input = input().strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nBell: Talk soon.\n")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ["/quit", "/exit", "quit", "exit", "bye", "goodbye"]:
            print("\nBell: Talk soon.\n")
            break

        if cmd == "/diary":
            handle_diary(system_prompt, messages)
            continue

        if cmd == "/wardrobe":
            handle_wardrobe(system_prompt, messages)
            continue

        if cmd == "/goals":
            handle_goals(system_prompt, messages)
            continue

        if cmd == "/week":
            handle_weekly_review(system_prompt, messages)
            continue

        if cmd == "/update":
            handle_update(system_prompt, messages)
            continue

        # Natural language session detection
        session = detect_session(user_input)

        if session == "diary":
            handle_diary(system_prompt, messages, user_input)
        elif session == "wardrobe":
            handle_wardrobe(system_prompt, messages, user_input)
        elif session == "goals":
            handle_goals(system_prompt, messages)
        elif session == "feelings":
            handle_feelings(system_prompt, messages, user_input)
        elif session == "weekly_review":
            handle_weekly_review(system_prompt, messages)
        elif session == "schedule":
            handle_schedule(system_prompt, messages, user_input)
        elif session == "update":
            handle_update(system_prompt, messages)
        elif session == "morning":
            handle_morning(system_prompt, messages)
        else:
            # General chat
            print("\nBell: ", end="")
            reply = agent.chat(system_prompt, messages, user_input)
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": reply})
            print()


if __name__ == "__main__":
    main()
