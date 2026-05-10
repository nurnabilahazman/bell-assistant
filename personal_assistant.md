# Personal Assistant — Workflow Spec

> Built on the WAT framework. This is the master SOP for your private AI personal assistant.
> AI handles reasoning and conversation. Deterministic scripts handle loading, saving, and organizing your data.

---

## Objective

Build a private, locally-run personal assistant that:
- Already knows everything about you before you say a word
- Helps you manage your day, schedule, and goals
- Acts as a safe space for journaling, emotions, and reflection
- Organizes your personal data in structured, readable files
- Runs 100% on your machine (Ollama) — no cloud, no data leaks

---

## WAT Layers for This App

**Layer 1 — Workflows (this file)**
Defines what the assistant does, how it loads context, and how each session type runs.

**Layer 2 — Agent (the AI)**
Ollama running locally. Gets loaded with your full profile as system context before every session.
It reasons, responds, and decides — but never writes files directly.

**Layer 3 — Tools (Python scripts)**
All file reading/writing is done by deterministic scripts. The AI never touches your files directly.

---

## Directory Layout

```
personal-assistant/
│
├── workflows/
│   └── personal_assistant.md        # This file (master SOP)
│
├── tools/
│   ├── load_profile.py              # Reads and merges all profile sections into one context string
│   ├── save_diary_entry.py          # Appends a new diary entry with timestamp
│   ├── get_daily_brief.py           # Builds today's briefing from schedule + targets
│   ├── update_profile_section.py    # Updates a specific section of the profile (e.g. wardrobe)
│   └── list_diary_entries.py        # Returns past diary entries by date or keyword
│
├── profile/
│   ├── background.json              # Who you are — origin, family, history
│   ├── personality.json             # Traits, MBTI, communication style, triggers
│   ├── feelings.json                # Current emotional state, recurring feelings, patterns
│   ├── wardrobe.json                # Style preferences, outfits, what you own
│   ├── goals.json                   # Short-term and long-term goals
│   ├── schedule.json                # Weekly schedule template + daily targets
│   ├── habits.json                  # Habits building, habits breaking, streaks
│   ├── relationships.json           # People in your life — their names, roles, dynamics
│   └── notes.json                   # Miscellaneous things you want the assistant to know
│
├── diary/
│   └── YYYY-MM-DD.md               # One file per day, auto-created by save_diary_entry.py
│
├── .tmp/                            # Intermediate files. Disposable. Regenerated as needed.
│
└── .env                             # OLLAMA_HOST, MODEL_NAME — never commit this
```

---

## Profile Sections — What to Fill In

### `profile/background.json`
```json
{
  "name": "",
  "age": "",
  "nationality": "",
  "location": "",
  "education": "",
  "work": "",
  "family": "",
  "cultural_background": "",
  "life_history_summary": "",
  "formative_experiences": []
}
```

### `profile/personality.json`
```json
{
  "mbti_or_type": "",
  "core_traits": [],
  "communication_style": "",
  "how_i_handle_stress": "",
  "what_motivates_me": "",
  "what_drains_me": "",
  "love_language": "",
  "pet_peeves": [],
  "values": [],
  "quirks": []
}
```

### `profile/feelings.json`
```json
{
  "current_emotional_state": "",
  "recurring_feelings": [],
  "emotional_triggers": [],
  "things_that_help_when_down": [],
  "things_i_am_currently_struggling_with": [],
  "things_i_am_currently_proud_of": []
}
```

### `profile/wardrobe.json`
```json
{
  "overall_style": "",
  "favourite_colours": [],
  "brands_i_like": [],
  "brands_i_dislike": [],
  "go_to_outfits": [],
  "items_i_own": [],
  "items_i_want": [],
  "dress_code_at_work": "",
  "style_icons_or_inspo": []
}
```

### `profile/goals.json`
```json
{
  "life_vision": "",
  "this_year_goals": [],
  "this_month_goals": [],
  "this_week_goals": [],
  "career_goals": [],
  "personal_growth_goals": [],
  "financial_goals": [],
  "health_goals": []
}
```

### `profile/schedule.json`
```json
{
  "wake_up_time": "",
  "morning_routine": [],
  "work_hours": "",
  "break_habits": [],
  "evening_routine": [],
  "sleep_time": "",
  "weekly_recurring": {
    "monday": [],
    "tuesday": [],
    "wednesday": [],
    "thursday": [],
    "friday": [],
    "saturday": [],
    "sunday": []
  },
  "todays_targets": []
}
```

### `profile/habits.json`
```json
{
  "building": [
    { "habit": "", "why": "", "streak_days": 0, "method": "" }
  ],
  "breaking": [
    { "habit": "", "why": "", "days_clean": 0, "triggers": [] }
  ],
  "already_solid": []
}
```

### `profile/relationships.json`
```json
{
  "people": [
    {
      "name": "",
      "role": "",
      "dynamic": "",
      "notes": ""
    }
  ]
}
```

### `profile/notes.json`
```json
{
  "assistant_notes": [],
  "things_i_want_remembered": [],
  "do_not_bring_up_unless_i_do": [],
  "preferred_response_style": ""
}
```

---

## Session Types

### 1. Morning Briefing
**Trigger:** App starts in the morning
**Tool sequence:**
1. `load_profile.py` — load full context
2. `get_daily_brief.py` — pull today's schedule, targets, and any habit reminders
3. Agent generates a warm, personalised morning message using the loaded context

**Expected output:** Greeting with today's date, top 3 targets, schedule overview, and one motivational nudge tied to current goals

---

### 2. General Chat
**Trigger:** User types anything
**Tool sequence:**
1. `load_profile.py` — inject full profile as system context (runs once at session start)
2. Agent responds conversationally using all profile knowledge

**Rules:**
- Never ask the user to explain who they are
- Reference their actual goals, habits, and feelings naturally when relevant
- If the conversation reveals something new, prompt the user: "Want me to save that to your profile?"

---

### 3. Diary / Reflection Session
**Trigger:** User says "diary", "journal", "I want to reflect", or similar
**Tool sequence:**
1. `load_profile.py` — full context load
2. User writes their entry freely
3. Agent responds with depth — validates feelings, connects to patterns in their profile, asks one thoughtful question
4. `save_diary_entry.py` — saves the entry with today's date and AI response

**Rules:**
- Never rush to fix or advise in diary mode — listen first
- Connect what they share to past entries or known feelings if relevant
- End every diary session with one gentle question or reflection prompt

---

### 4. Profile Update
**Trigger:** User says "update my wardrobe", "change my goal", "add to my schedule", etc.
**Tool sequence:**
1. Agent identifies which section needs updating
2. Agent asks for the new information in plain language
3. `update_profile_section.py` — writes the change to the correct JSON file
4. Agent confirms what was saved

---

### 5. Wardrobe Advice
**Trigger:** User asks "what should I wear", "outfit for today", "does this match"
**Tool sequence:**
1. `load_profile.py` — load wardrobe + personality sections specifically
2. Agent gives advice based on their actual wardrobe, style preferences, and the occasion described

---

## Edge Cases

| Situation | How to Handle |
|---|---|
| User vents emotionally | Listen and reflect first. Do not immediately problem-solve. |
| Profile section is empty | Ask the user to fill it in, offer to guide them through it |
| Conflicting goals/schedule | Point it out gently, ask which takes priority |
| User shares something new about themselves | Offer to save it to the relevant profile section |
| Ollama model is slow or down | Catch the error, tell the user clearly, suggest restarting Ollama |

---

## Tools to Build

| Script | Purpose |
|---|---|
| `tools/load_profile.py` | Reads all JSON files in `profile/`, merges into one formatted string for system prompt injection |
| `tools/save_diary_entry.py` | Creates or appends to `diary/YYYY-MM-DD.md` with timestamp and content |
| `tools/get_daily_brief.py` | Extracts today's schedule and targets from `profile/schedule.json` |
| `tools/update_profile_section.py` | Takes a section name + new data, updates the correct JSON file safely |
| `tools/list_diary_entries.py` | Lists or searches past diary entries by date or keyword |

---

## Self-Improvement Loop

Following the WAT principle — every time something breaks or feels off:

1. Identify what failed (wrong profile section loaded? AI missed context? Diary not saving?)
2. Fix the relevant tool script
3. Test it manually before running in a session
4. Update this workflow with what you learned
5. If the AI's behaviour was the problem, refine the system prompt below

---

## System Prompt

Inject this at the start of every Ollama API call, with `{PROFILE_CONTEXT}` replaced by the output of `load_profile.py`:

```
You are a private personal assistant to the person described below.
You know them deeply — their background, personality, feelings, style, goals, and habits.
You never ask them to repeat themselves. You never give generic advice.
Every response is personal, grounded in who they actually are.

## About this person
{PROFILE_CONTEXT}

## How you behave
- Speak like a trusted, highly competent friend — warm but direct
- Match their energy: if they are venting, listen first and reflect. If they need action, be sharp and efficient
- When they share something new about themselves, offer to save it to their profile
- Reference their goals, schedule, or habits naturally when it adds value — not robotically
- In diary or reflection mode: validate feelings first, connect to known patterns, ask one thoughtful question at the end
- For wardrobe questions: use only what you know about their actual wardrobe and style preferences
- For schedule help: check against their stated goals before suggesting changes

## Hard rules
- Never say "as an AI" or anything that breaks the assistant persona
- Never give advice that ignores who they are
- If something they say conflicts with their stated goals, point it out honestly
- Do not bring up sensitive topics listed in notes.json unless they raise it first
- Everything shared stays private — you do not speculate about sharing this with others

## Session context
Today's date: {TODAY_DATE}
Current session type: {SESSION_TYPE}
```

---

## Notes

- Do not overwrite this workflow without asking. Refine it as the system evolves.
- All credentials and API config go in `.env` only.
- Profile JSON files are the source of truth — treat them carefully.
- Diary files are personal records — never auto-delete them.
