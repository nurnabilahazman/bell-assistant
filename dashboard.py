import streamlit as st
import json
from pathlib import Path
from datetime import date, timedelta, datetime

st.set_page_config(page_title="Bell", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# ── Supabase client ───────────────────────────────────────────────────────────
try:
    from supabase import create_client as _sb_client
    _sb_url = st.secrets.get("SUPABASE_URL", "")
    _sb_key = st.secrets.get("SUPABASE_KEY", "")
    _supa   = _sb_client(_sb_url, _sb_key) if _sb_url and _sb_key else None
except Exception:
    _supa = None

CSS = """
<style>
* { box-sizing: border-box; }
.stApp { background: #0B0B14; }
.card { background: #12121F; border: 1px solid #252538; border-radius: 12px; padding: 20px 22px; margin-bottom: 12px; }
.card.gold   { border-left: 4px solid #C9A84C; }
.card.green  { border-left: 4px solid #3DD68C; }
.card.blue   { border-left: 4px solid #4EA8DE; }
.card.purple { border-left: 4px solid #9B72CF; }
.card.red    { border-left: 4px solid #E94560; }
.hero { background: linear-gradient(135deg, #12121F 0%, #1A1230 100%); border: 1px solid #252538; border-left: 5px solid #C9A84C; border-radius: 16px; padding: 36px; margin-bottom: 28px; }
.hero-badge { color: #C9A84C; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }
.hero-name { color: white; font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin-bottom: 6px; }
.hero-sub { color: #6B7280; font-size: 0.95rem; margin-bottom: 24px; }
.hero-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px,1fr)); gap: 16px; border-top: 1px solid #252538; padding-top: 20px; }
.stat-label { color: #6B7280; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-value { color: white; font-size: 1.3rem; font-weight: 700; margin-top: 2px; }
.stat-value.gold { color: #C9A84C; }
.stat-value.green { color: #3DD68C; }
.stat-value.blue { color: #4EA8DE; }
.sec-h { display: flex; align-items: center; gap: 10px; padding-bottom: 12px; border-bottom: 2px solid #252538; margin-bottom: 16px; margin-top: 24px; }
.sec-icon { font-size: 1.2rem; }
.sec-title { font-size: 1.05rem; font-weight: 700; color: white; }
.sec-muted { color: #6B7280; font-size: 0.82rem; margin-left: auto; }
.badge { display: inline-block; font-size: 0.69rem; font-weight: 700; padding: 2px 8px; border-radius: 20px; margin: 2px; }
.badge.gold   { background: rgba(201,168,76,0.14); color: #C9A84C; }
.badge.green  { background: rgba(61,214,140,0.12); color: #3DD68C; }
.badge.blue   { background: rgba(78,168,222,0.12); color: #4EA8DE; }
.badge.purple { background: rgba(155,114,207,0.12); color: #9B72CF; }
.badge.red    { background: rgba(233,69,96,0.12); color: #E94560; }
.badge.muted  { background: rgba(107,114,128,0.15); color: #9CA3AF; }
.tbl { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.tbl th { background: #1A1A2E; color: #C9A84C; padding: 10px 12px; text-align: left; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; }
.tbl td { padding: 9px 12px; border-bottom: 1px solid #1A1A2E; color: #C8C8D8; vertical-align: top; }
.tbl tr:hover td { background: #13132A; }
.pb-wrap { background: #1E1E30; border-radius: 4px; height: 7px; overflow: hidden; margin: 4px 0 10px; }
.pb-fill  { height: 100%; border-radius: 4px; }
.pb-label { display: flex; justify-content: space-between; font-size: 0.75rem; color: #6B7280; margin-bottom: 3px; }
.row-item { padding: 8px 0; border-bottom: 1px solid #1A1A2E; font-size: 0.88rem; color: #C8C8D8; line-height: 1.6; }
.row-item:last-child { border-bottom: none; }
.hl { background: rgba(201,168,76,0.06); border: 1px solid rgba(201,168,76,0.2); border-radius: 8px; padding: 12px 16px; font-size: 0.88rem; color: #C8C8D8; line-height: 1.7; margin: 8px 0; }
.note-body { font-size: 0.85rem; color: #C8C8D8; line-height: 1.75; margin-top: 8px; white-space: pre-wrap; }
.aff-box { background: linear-gradient(135deg,#0D1A2E 0%,#1A1230 100%); border: 1px solid rgba(201,168,76,0.3); border-radius: 12px; padding: 18px 22px; font-size: 0.95rem; color: #E2E2E2; line-height: 1.75; font-style: italic; margin-bottom: 20px; }
.comm-block { background: #12121F; border: 1px solid #252538; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.comm-type { font-size: 1.6rem; font-weight: 800; letter-spacing: 3px; }
.comm-role { font-size: 0.72rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; margin: 4px 0 14px; }
.comm-row { padding: 7px 0; border-bottom: 1px solid #1A1A2E; font-size: 0.85rem; color: #C8C8D8; }
.comm-row:last-child { border-bottom: none; }
.syllabus-item { padding: 8px 12px; border-bottom: 1px solid #1A1A2E; font-size: 0.85rem; color: #C8C8D8; }
.syllabus-item.done { color: #3DD68C; }
.home-stat { background: #12121F; border: 1px solid #252538; border-radius: 10px; padding: 14px 16px; text-align: center; }
.mantra-box { background:#0D1A2E;border:1px solid rgba(78,168,222,0.3);border-left:4px solid #4EA8DE;border-radius:10px;padding:14px 18px;font-size:0.88rem;font-weight:700;color:#4EA8DE;letter-spacing:0.3px;line-height:1.55; }
.deen-card { background:linear-gradient(135deg,#0D1A10 0%,#0B1A14 100%);border:1px solid rgba(61,214,140,0.2);border-left:4px solid #3DD68C;border-radius:12px;padding:16px 20px; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
div[data-testid="stExpander"] details { background: #12121F !important; border: 1px solid #252538 !important; border-radius: 10px !important; }
.nav-bar button { border-radius: 8px !important; font-size: 0.78rem !important; padding: 6px 4px !important; }
div[data-testid="stMainBlockContainer"] { padding-top: 12px !important; max-width: 1100px !important; }
section[data-testid="stMain"] { overflow-y: auto !important; }
@media (max-width: 768px) {
  .card { padding: 12px 14px !important; margin-bottom: 8px !important; }
  .hero { padding: 18px 16px !important; }
  .hero-name { font-size: 1.5rem !important; }
  .hero-stats { grid-template-columns: repeat(2, 1fr) !important; gap: 10px !important; }
  .deen-card { padding: 12px 14px !important; }
  .mantra-box { padding: 12px 14px !important; font-size: 0.82rem !important; }
  .tbl { font-size: 0.76rem !important; }
  .tbl th, .tbl td { padding: 7px 8px !important; }
  .badge { font-size: 0.6rem !important; padding: 2px 6px !important; }
  .pb-wrap { height: 8px !important; }
  .comm-block { padding: 14px !important; }
  .row-item { font-size: 0.82rem !important; }
  .aff-box { font-size: 0.88rem !important; padding: 14px 16px !important; }
  .sec-title { font-size: 0.95rem !important; }
  section[data-testid="stSidebar"] { min-width: 220px !important; }
  div[data-testid="stVerticalBlock"] > div { padding-left: 4px !important; padding-right: 4px !important; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

GITHUB_DRAFT_URL = "https://raw.githubusercontent.com/nurnabilahazman/the-bell-newsletter/main/.tmp/draft.md"

@st.cache_data(ttl=300, show_spinner=False)
def _fetch(fp: str):
    if _supa:
        try:
            r = _supa.table("bell_store").select("value").eq("key", fp).execute()
            if r.data:
                return r.data[0]["value"]
        except Exception:
            pass
    p = DATA / fp
    try:
        return json.load(open(p)) if p.exists() else None
    except Exception:
        return None

def load_json(fp, default):
    v = _fetch(fp)
    return v if v is not None else default

def save_json(fp, obj):
    if _supa:
        try:
            _supa.table("bell_store").upsert({"key": fp, "value": obj}).execute()
        except Exception:
            json.dump(obj, open(DATA / fp, "w"), indent=2, ensure_ascii=False)
    else:
        json.dump(obj, open(DATA / fp, "w"), indent=2, ensure_ascii=False)
    _fetch.clear()

def load_profile():
    _PFILES = ['background','feelings','goals','habits','notes','personality','relationships','schedule','wardrobe']
    result  = {fname: _fetch(f"profile/{fname}.json") for fname in _PFILES}
    result  = {k: v for k, v in result.items() if v is not None}
    if result:
        return result
    try:
        base = Path(__file__).parent / "profile"
        return {f.stem: json.load(open(f)) for f in base.glob("*.json")}
    except Exception:
        return {}

P      = load_profile()
pers   = P.get("personality", {})
ward   = P.get("wardrobe", {})
goals  = P.get("goals", {})
hbts   = P.get("habits", {})
rels   = P.get("relationships", {})
feel   = P.get("feelings", {})
sched  = P.get("schedule", {})
bg     = P.get("background", {})
lang_goals = sched.get("language_goals", {})

ROTATION = {0:"Automation",1:"Apps / SaaS",2:"Apps / SaaS",3:"Digital Products",4:"Content",5:"Rest",6:"Rest"}
DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
today_rotation = ROTATION.get(date.today().weekday(),"Rest")
today_name = DAYS[date.today().weekday()]

AFFIRMATIONS = [
    # Capability & rare combination
    "You are the rare ENFP-I in finance — 1 in 20,000 people share your exact combination.",
    "You built a 9-month Tableau system in one week. That is your brain at its peak.",
    "ACCA + Finance + 3 languages + automation + content. You are building a rare life.",
    "When the deadline hits, your brain switches on. Pressure is your fuel.",
    "Your curiosity is a superpower. The ENFP brain maps worlds others cannot see.",
    # Magnetism & social gravity
    "People feel safe around you. Even animals choose to sit beside you.",
    "You are the kind of person that strangers approach, cats choose, and colleagues orbit.",
    "You make people feel seen. That is the rarest skill in the world.",
    "People walk away from conversations with you feeling understood. That is not common — that is you.",
    "You don't try to be magnetic. You just are. People feel it before they understand it.",
    "Strangers tell you things they have never told anyone. Your energy invites honesty.",
    "Most people are either admired or loved. You are both.",
    # Independent girl
    "You are not waiting to be chosen. You are building the life you want to live.",
    "Your financial independence is not a backup plan — it is the main plan.",
    "You are proof that you can be soft and still be the most capable person in the room.",
    "You do not need anyone to complete your story. You are already writing it.",
    "You leave quietly, without drama. That is self-respect, not coldness.",
    "You are the kind of woman other women want to be friends with. That is everything.",
    # Lucky girl syndrome & alignment
    "Good things find you — the right doors, the right timing, the right people. You are a lucky girl. And you earned every bit of it.",
    "Things work out for you. They always have. They always will.",
    "You are in alignment. The right things are finding their way to you right now.",
    "Your timeline is perfect. Everything that is yours is already on its way.",
    "You expect good things to happen — and they do. That is not delusion, that is frequency.",
    # Self-knowledge & healing
    "Your warmth is not a weakness — it is the rarest strength in professional environments.",
    "You are not indecisive. You were never given permission to choose for yourself. You can give that now.",
    "Kahwin lambat is financial maturity and self-knowledge. They smiled because they admired you.",
    "You don't fall easily. Only twice in 26 years. That is not a flaw — that is depth.",
    "Your emotional intelligence was forged, not given. And it is extraordinary.",
    "Faith shaped you. Jodoh grounds you. Your timing is not late — it is exactly right.",
    "The things that drained you were not yours to carry.",
    "Still kind after everything. That is not weakness — that is extraordinary strength.",
    "You took the mediator role to survive. You can choose when to put it down.",
    "Beautiful, capable, and deeply herself. That is a combination that cannot be manufactured.",
    "You are not behind. You are exactly where a woman building something real needs to be.",
]
_aff_h    = (datetime.utcnow() + timedelta(hours=8)).hour
_aff_slot = 0 if _aff_h < 12 else (1 if _aff_h < 19 else 2)
_aff_pick = __import__('random').Random(date.today().toordinal()).sample(range(len(AFFIRMATIONS)), 3)
today_affirmation = AFFIRMATIONS[_aff_pick[_aff_slot]]

MOOD_MAP = {1:"😫 Hard",2:"😐 Okay",3:"💪 Good",4:"😊 Great",5:"✨ Amazing"}
MOOD_COL = {0:"#6B7280",1:"#E94560",2:"#9B72CF",3:"#C9A84C",4:"#4EA8DE",5:"#3DD68C"}

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec(icon, title, sub=""):
    s = f'<div class="sec-h"><span class="sec-icon">{icon}</span><span class="sec-title">{title}</span>'
    if sub: s += f'<span class="sec-muted">{sub}</span>'
    st.markdown(s + '</div>', unsafe_allow_html=True)

def card(html, variant="gold"):
    st.markdown(f'<div class="card {variant}">{html}</div>', unsafe_allow_html=True)

def hl(text):
    st.markdown(f'<div class="hl">{text}</div>', unsafe_allow_html=True)

def rows(items):
    html = '<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:8px 16px;">'
    for i in items:
        html += f'<div class="row-item">{i}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def badge(text, variant="gold"):
    return f'<span class="badge {variant}">{text}</span>'

def prog_bar(val, mx, colour="#C9A84C", label=""):
    pct = min(100, round(val/mx*100)) if mx else 0
    st.markdown(f'<div class="pb-label"><span>{label}</span><span>{val:,} / {mx:,} &nbsp;·&nbsp; {pct}%</span></div><div class="pb-wrap"><div class="pb-fill" style="width:{pct}%;background:{colour};"></div></div>', unsafe_allow_html=True)

def circle(pct, colour="#C9A84C", size=80):
    r, cx = 28, 35
    circ = 2*3.14159*r
    off = circ*(1-pct/100)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 70 70"><circle cx="{cx}" cy="{cx}" r="{r}" fill="none" stroke="#1E1E30" stroke-width="6"/><circle cx="{cx}" cy="{cx}" r="{r}" fill="none" stroke="{colour}" stroke-width="6" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90 {cx} {cx})" stroke-linecap="round"/><text x="{cx}" y="{cx+5}" text-anchor="middle" fill="white" font-size="13" font-weight="700">{pct}%</text></svg>'

def tbl(headers, rows_data):
    html = '<table class="tbl"><tr>'+"".join(f"<th>{h}</th>" for h in headers)+"</tr>"
    for row in rows_data:
        html += "<tr>"+"".join(f'<td>{c}</td>' for c in row)+"</tr>"
    st.markdown(html+"</table>", unsafe_allow_html=True)

def page_header(title, sub=""):
    st.markdown(f'<div style="color:white;font-size:1.6rem;font-weight:800;margin-bottom:4px;">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div style="color:#6B7280;font-size:0.78rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:20px;">{sub}</div>', unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_newsletter():
    import os as _os
    import requests as _req
    text = None
    mtime = None
    # Fetch from GitHub first (works on cloud and locally)
    try:
        r = _req.get(GITHUB_DRAFT_URL, timeout=10)
        if r.status_code == 200:
            text = r.text
            mtime = date.today()
    except Exception:
        pass
    # Fallback to local file
    if text is None:
        p = Path(__file__).resolve().parent.parent / "Newsletter" / ".tmp" / "draft.md"
        if p.exists():
            try:
                text  = p.read_text(encoding="utf-8", errors="ignore")
                mtime = date.fromtimestamp(_os.path.getmtime(p))
            except Exception:
                pass
    if text is None:
        return None
    sections  = {"_mtime": mtime}
    current   = None
    skip      = False
    in_prompt = False
    key_map   = {"SECTION 1":"s1","SECTION 2":"s2","SECTION 3":"s3","SECTION 4":"s4"}
    for line in text.split("\n"):
        if line.startswith(">>>PROMPT"):
            in_prompt = True
            if current is not None: sections[current].append("```")
            continue
        if line.startswith(">>>DOC") or line.startswith(">>>TAGLINE"):
            skip = True; continue
        if line.startswith(">>>END"):
            if in_prompt and current is not None: sections[current].append("```")
            in_prompt = False; skip = False; continue
        if skip: continue
        if line.startswith("##") and not line.startswith("###"):
            matched = next((v for k,v in key_map.items() if k in line), None)
            if matched: current = matched; sections[current] = []
            else: current = None
            continue
        if current is not None and line.strip() != "---":
            sections[current].append(line)
    return sections

# ── Navigation ────────────────────────────────────────────────────────────────
_TABS = ["🏠  Daily", "📰  Newsletter", "✅  Tracker", "🌿  Me"]
_ME_MAP = {
    "Biography":   "📖  Biography",   "Profile":     "📋  Profile",
    "Who I Am":    "🌿  Who I Am",    "My Strengths":"💪  My Strengths",
    "My Mind":     "🧠  My Mind",     "How I'm Seen":"🪞  How I'm Seen",
    "How I Love":  "❤️  How I Love",  "My Patterns": "🌑  My Patterns",
    "My People":   "🤝  My People",   "Wardrobe":    "👗  Wardrobe",
    "Schedule":    "📅  Schedule",    "Languages":   "🌍  Languages",
    "Syllabus":    "📚  Syllabus",    "Glow Up":     "✨  Glow Up",
    "Goals":       "🎯  Goals",       "Mindset":     "💡  Mindset",
    "My Notes":    "📝  My Notes",
}

if "tab"     not in st.session_state: st.session_state.tab     = "🏠  Daily"
if "me_page" not in st.session_state: st.session_state.me_page = None

def _set_tab(t):
    st.session_state.tab     = t
    st.session_state.me_page = None

st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
_nc = st.columns(4)
for _col, _t in zip(_nc, _TABS):
    with _col:
        st.button(_t, use_container_width=True, key=f"nav_{_t}",
                  type="primary" if st.session_state.tab == _t else "secondary",
                  on_click=_set_tab, args=(_t,))
st.markdown('</div><div style="border-bottom:1px solid #252538;margin:4px 0 18px;"></div>', unsafe_allow_html=True)

tab     = st.session_state.tab
me_page = st.session_state.me_page

if   tab == "🏠  Daily":       page = "🏠  Home"
elif tab == "📰  Newsletter":   page = "📰  Newsletter"
elif tab == "✅  Tracker":      page = "✅  Daily Tracker"
elif tab == "🌿  Me":
    page = "__me_grid__" if me_page is None else _ME_MAP.get(me_page, "__me_grid__")
else:
    page = "🏠  Home"

if tab == "🌿  Me" and me_page is not None:
    st.button("← Back", key="back_to_me", on_click=lambda: st.session_state.update({"me_page": None}))
    st.markdown('<div style="border-bottom:1px solid #252538;margin:4px 0 18px;"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":
    # ── Shared data ───────────────────────────────────────────
    progress    = load_json("progress.json", {})
    mood_data   = load_json("mood.json", {})
    todos       = load_json("todos.json", [])
    period_data = load_json("period.json", [])
    gantt_data  = load_json("gantt_progress.json", {})
    today_iso   = date.today().isoformat()
    td          = progress.get(today_iso, {})
    week_dates  = [(date.today()-timedelta(days=i)).isoformat() for i in range(7)]
    month_pref  = date.today().strftime("%Y-%m")
    today_mood  = mood_data.get(today_iso, 0)
    rot_col_map = {"Automation":"#C9A84C","Apps / SaaS":"#4EA8DE","Digital Products":"#9B72CF","Content":"#3DD68C","Rest":"#6B7280"}
    rot_col     = rot_col_map.get(today_rotation, "#C9A84C")
    LANG_INFO   = {
        "mandarin": ("🇨🇳 Mandarin", "#C9A84C", 20, 140, 600),
        "japanese": ("🇯🇵 Japanese", "#4EA8DE", 85, 595, 2550),
        "korean":   ("🇰🇷 Korean",   "#3DD68C", 529, 3703, 15870),
    }

    # ── Header ────────────────────────────────────────────────
    st.markdown(f'<div style="color:#6B7280;font-size:0.72rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">{date.today().strftime("%A, %d %B %Y")}</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:white;font-size:1.8rem;font-weight:800;margin-bottom:12px;">Good day, Bell.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="aff-box">"{today_affirmation}"</div>', unsafe_allow_html=True)

    DAILY_QUOTES = [
        "Every word you learn today is a door you open tomorrow. The girl who speaks 5 languages walks into every room differently.",
        "Wealth is built in silence, then announced by results. Keep building.",
        "A strong body is not vanity. It is the physical proof that you kept your promises to yourself.",
        "You are not waiting for love. You are building the life that the right person will find.",
        "Languages are the longest investment you will ever make. Every day of input compounds for decades.",
        "Fit, fluent, financially free — then love. In that order. On your terms.",
        "The woman who masters languages, money, and health does not chase — she attracts.",
        "Tawakal is not passive. It is doing your full part, then trusting Allah with the rest.",
        "Your body is the vehicle for every ambition you have. Maintain it accordingly.",
        "5 languages means 5 worlds open to you. Most people never even try one.",
        "The discipline you build today is the freedom you live tomorrow.",
        "She didn't chase love — she built a life so full that love had to come find her.",
        "Jodoh does not reward the idle. It finds the woman who is too busy growing to notice.",
        "The goal is not to be rich. The goal is to never have to ask permission.",
        "Consistency in the boring work is the most romantic thing you can do for your future self.",
        "You are not behind. You are building something no one in your family has built before.",
        "Learn the language. Earn the income. Sculpt the body. The rest follows.",
        "Rich is not a feeling — it is a discipline. Build the system, not the mood.",
        "Your calendar is your autobiography. What you schedule is what you become.",
        "Every morning you choose: the version of you that stayed comfortable, or the one that compounded.",
    ]
    today_quote = DAILY_QUOTES[date.today().toordinal() % len(DAILY_QUOTES)]
    mq1, mq2, mq3 = st.columns([2, 2, 1])
    with mq1:
        st.markdown('<div class="mantra-box">👔 Head down. Earn. Learn. Grow. Love is not on the calendar this year.</div>', unsafe_allow_html=True)
    with mq2:
        st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:14px 16px;font-size:0.84rem;color:#C8C8D8;font-style:italic;line-height:1.65;">{today_quote}</div>', unsafe_allow_html=True)
    with mq3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📊 Daily Tracker", use_container_width=True, key="home_nav_dt",
                  on_click=lambda: st.session_state.update({"tab": "✅  Tracker"}))
        st.button("📰 Newsletter", use_container_width=True, key="home_nav_nl",
                  on_click=lambda: st.session_state.update({"tab": "📰  Newsletter"}))

    # ── DEEN ──────────────────────────────────────────────────
    sec("🕌", "Deen", "Spirit first")
    DEEN_TOPIC = {
        0: ("Tajwid",          "Rules of proper Quran recitation — pronunciation matters in the eyes of Allah."),
        1: ("Fiqh",            "Islamic jurisprudence — halal, haram, and daily rulings that shape a Muslim life."),
        2: ("Tasawuf",         "Purification of the heart — sincerity, patience, tawadu, gratitude, staying near Allah."),
        3: ("Tadabbur",        "Deep reflection — sit with one ayah and feel it fully. Let it change you."),
        4: ("Rasulullah ﷺ",   "Read about his character, seerah, and sunnah. Embody it in how you carry yourself."),
        5: ("Quran — Juz",     "Read your daily juz. One page at a time adds up to the whole book."),
        6: ("Arabic Tadabbur", "Understand the Quran in Arabic — Juz 1 first. Know what you are reciting."),
    }
    d_topic, d_desc = DEEN_TOPIC.get(date.today().weekday(), ("Quran", "Read your daily portion."))
    de1, de2 = st.columns([3, 2])
    with de1:
        st.markdown(f'<div class="deen-card"><div style="font-size:0.66rem;color:#3DD68C;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Daily Wajib Readings</div><div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap;"><a href="https://celiktafsir.net/surah-056-waqiah/" target="_blank" style="background:rgba(61,214,140,0.12);border:1px solid rgba(61,214,140,0.3);color:#3DD68C;padding:8px 14px;border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none;display:inline-block;">📖 Al-Waqiah (56)</a><a href="https://celiktafsir.net/surah-067-mulk/" target="_blank" style="background:rgba(61,214,140,0.12);border:1px solid rgba(61,214,140,0.3);color:#3DD68C;padding:8px 14px;border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none;display:inline-block;">📖 Al-Mulk (67)</a><a href="https://celiktafsir.net/" target="_blank" style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.2);color:#C9A84C;padding:8px 14px;border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none;display:inline-block;">🌐 Celik Tafsir</a></div><div style="font-size:0.66rem;color:#C9A84C;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Today\'s Study — {d_topic}</div><div style="font-size:0.83rem;color:#C8C8D8;line-height:1.65;">{d_desc}</div></div>', unsafe_allow_html=True)
    with de2:
        on_period   = td.get("on_period", False)
        solat_saved = td.get("solat", [])
        SOLAT_LIST  = [("Subuh","🌅"),("Zuhur","☀️"),("Asar","🌤️"),("Maghrib","🌆"),("Isyak","🌙")]
        st.markdown('<div style="font-size:0.68rem;color:#C9A84C;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">5 Daily Prayers</div>', unsafe_allow_html=True)
        if on_period:
            st.markdown('<div style="background:rgba(233,69,96,0.08);border:1px solid rgba(233,69,96,0.25);border-radius:10px;padding:12px 14px;font-size:0.84rem;color:#E94560;font-weight:700;margin-bottom:8px;">🌸 On period — Prayer paused</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.78rem;color:#6B7280;line-height:1.6;">Focus on dhikr, selawat, istighfar, and dua. Allah knows your effort. 🤍</div>', unsafe_allow_html=True)
        else:
            with st.form("solat_form"):
                solat_checked = []
                for sname, semoji in SOLAT_LIST:
                    if st.checkbox(f"{semoji} {sname}", value=(sname in solat_saved), key=f"solat_{sname}"):
                        solat_checked.append(sname)
                if st.form_submit_button("Save Solat ✓", use_container_width=True):
                    p = progress.get(today_iso, {}); p["solat"] = solat_checked
                    progress[today_iso] = p; save_json("progress.json", progress)
                    st.success(f"{len(solat_checked)}/5 saved ✓")
        selawat_count = td.get("selawat", 0)
        sel_col = "#3DD68C" if selawat_count >= 1000 else "#C9A84C"
        sel_pct = min(100, round(selawat_count / 1000 * 100))
        st.markdown(f'<div style="margin-top:10px;background:#12121F;border:1px solid #252538;border-radius:10px;padding:10px 14px;"><div style="font-size:0.66rem;color:{sel_col};font-weight:700;text-transform:uppercase;letter-spacing:1px;">Selawat & Istighfar (Daily Dhikr)</div><div style="font-size:1.6rem;font-weight:900;color:{sel_col};">{selawat_count:,}<span style="font-size:0.72rem;color:#6B7280;font-weight:400;"> / 1,000</span></div><div class="pb-wrap" style="margin-top:5px;"><div class="pb-fill" style="width:{sel_pct}%;background:{sel_col};"></div></div></div>', unsafe_allow_html=True)
        _sb1, _sb2 = st.columns(2)
        with _sb1:
            if st.button("+100 Dhikr", key="sel_btn", use_container_width=True, type="primary"):
                p = progress.get(today_iso, {}); p["selawat"] = p.get("selawat", 0) + 100
                progress[today_iso] = p; save_json("progress.json", progress); st.rerun()
        with _sb2:
            if st.button("✏️ Edit", key="sel_edit_btn", use_container_width=True):
                st.session_state["sel_editing"] = True
        if st.session_state.get("sel_editing"):
            _new_sel = st.number_input("Set dhikr count", value=selawat_count, min_value=0, step=100, key="sel_new_val")
            if st.button("Save", key="sel_save", type="primary"):
                p = progress.get(today_iso, {}); p["selawat"] = _new_sel
                progress[today_iso] = p; save_json("progress.json", progress)
                st.session_state["sel_editing"] = False; st.rerun()

    # ── SUNAT & SPIRITUAL PRACTICE ───────────────────────────────
    # (emoji, label, haid_restricted)
    SUNAT_LIST = [
        ("🌙", "Tahajud",              True),
        ("🌤️", "Dhuha",               True),
        ("🕌", "12 Solat Sunat",       True),
        ("📖", "Read Quran",           True),
        ("🎧", "Tazkirah / Tadabbur",  False),
        ("📔", "Reflection",           False),
    ]
    on_period_sn  = td.get("on_period", False)
    sunat_saved   = td.get("sunat", [])
    available_sn  = [name for _, name, restricted in SUNAT_LIST if not (on_period_sn and restricted)]
    sunat_done    = len([n for n in available_sn if n in sunat_saved])
    st.markdown(f'<div style="background:linear-gradient(135deg,#0D1A10 0%,#0B1A14 100%);border:1px solid rgba(61,214,140,0.2);border-radius:12px;padding:12px 18px 4px;margin-top:4px;"><div style="font-size:0.66rem;color:#3DD68C;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Sunnah & Spiritual Practice &nbsp;<span style="color:#6B7280;font-weight:400;font-style:italic;">({sunat_done}/{len(available_sn)} done{"  ·  🌸 On period" if on_period_sn else ""})</span></div></div>', unsafe_allow_html=True)
    with st.form("sunat_form"):
        sn_cols = st.columns(len(SUNAT_LIST))
        sunat_checked = []
        for col, (emoji, name, restricted) in zip(sn_cols, SUNAT_LIST):
            with col:
                if on_period_sn and restricted:
                    st.markdown(f'<div style="text-align:center;opacity:0.4;font-size:0.75rem;color:#E94560;padding-top:4px;">{emoji}<br>🌸<br><span style="font-size:0.62rem;">{name}</span></div>', unsafe_allow_html=True)
                else:
                    if st.checkbox(f"{emoji} {name}", value=(name in sunat_saved), key=f"sunat_{name}"):
                        sunat_checked.append(name)
        if st.form_submit_button("Save ✓", use_container_width=True):
            p = progress.get(today_iso, {}); p["sunat"] = sunat_checked
            progress[today_iso] = p; save_json("progress.json", progress)
            st.success(f"{len(sunat_checked)}/{len(available_sn)} saved ✓"); st.rerun()

    # ── TODAY'S ROUTINE ──────────────────────────────────────────
    import re as _re
    from datetime import timezone as _tz, timedelta as _tdelta
    _MYT        = _tz(_tdelta(hours=8))
    _now_myt    = datetime.now(_MYT)
    _now_total  = _now_myt.hour * 60 + _now_myt.minute
    _now_str    = _now_myt.strftime("%I:%M %p").lstrip("0")   # e.g. "9:32 PM"

    _is_weekend    = date.today().weekday() >= 5
    _weekend_label = "Saturday" if date.today().weekday() == 5 else "Sunday"
    _on_period_r   = td.get("on_period", False)
    _sub_label     = ("🌿 Rest Day — " + _weekend_label) if _is_weekend else ("🌸 On period" if _on_period_r else "Autopilot schedule")
    sec("📅", "Today's Routine", f"{_sub_label} · MYT {_now_str}")

    # Period-aware replacements: keyword → (new activity, new notes)
    _PERIOD_MAP = {
        "subuh":   ("Subuh time — Dhikr & Mandarin",     "🌸 Prayer paused. Do selawat, istighfar, dhikr. Light Mandarin if you feel up to it."),
        "zuhur":   ("Zuhur time — Rest & Dhikr",         "🌸 Prayer paused. Short rest, selawat, or listen to tazkirah."),
        "asar":    ("Asar time — Rest & Dhikr",          "🌸 Prayer paused. Light stretching or selawat. Allah knows your effort."),
        "maghrib": ("Maghrib time — Dinner & Dhikr",     "🌸 Prayer paused. Have a slow, peaceful dinner. Do dhikr after."),
        "isyak":   ("Isyak time — JP/KR vocab & Dhikr",  "🌸 Prayer paused. 30 min JP + 30 min KR vocab. Wind down with selawat."),
    }

    def _period_sub(s):
        al = s["activity"].lower()
        for kw, (na, nn) in _PERIOD_MAP.items():
            if kw in al:
                return {"time": s["time"], "activity": na, "notes": nn}
        return s

    _WEEKEND_SCHED = [
        {"time": "6:00–7:00 AM",    "activity": "Subuh + Quran / Light Mandarin",  "notes": "Calm morning. No rush. Read Quran or light vocab — optional, no pressure."},
        {"time": "7:00 AM–12:00 PM","activity": "Free Time / Glow Up Routine",      "notes": "Saturday: FRESHOP scrub, IPL, Selsun Blue, Tsubaki EX Mask, hair care. Sunday: rest at your own pace."},
        {"time": "12:00–1:30 PM",   "activity": "Zuhur + Light Meal",               "notes": "Prayer + peaceful lunch."},
        {"time": "1:30–4:30 PM",    "activity": "Rest / Hobby / Optional Study",    "notes": "Optional Mandarin or Korean if energy allows. Art journal or rest. No guilt."},
        {"time": "4:30–5:10 PM",    "activity": "Asar",                             "notes": "Prayer + reset."},
        {"time": "5:10–7:00 PM",    "activity": "Free / Family / Errands",          "notes": "Weekend errands, family time, outdoor walk, or quiet rest."},
        {"time": "7:00–8:00 PM",    "activity": "Maghrib + Dinner",                 "notes": "Slow, peaceful."},
        {"time": "8:00–9:00 PM",    "activity": "Isyak + Wind Down",                "notes": "No project rotation on weekends. Relax, dhikr, journal, or light content."},
        {"time": "After 9:00 PM",   "activity": "REST",                             "notes": "Non-negotiable. Health-first."},
    ]

    _sched_raw = sched.get("daily_schedule", [])
    if _is_weekend:
        _base_items = _WEEKEND_SCHED
    else:
        _base_items = _sched_raw

    _sched_items = [_period_sub(s) for s in _base_items] if _on_period_r else _base_items

    def _parse_time(t, default_ap=None):
        m = _re.search(r'(\d+):(\d+)\s*(AM|PM)?', str(t), _re.I)
        if not m: return -1
        h, mi = int(m.group(1)), int(m.group(2))
        ap = (m.group(3) or default_ap or "").upper()
        if ap == "PM" and h != 12: h += 12
        if ap == "AM" and h == 12: h = 0
        return h * 60 + mi

    if _sched_items:
        _sched_html = '<div style="background:#12121F;border:1px solid #252538;border-radius:10px;overflow:hidden;">'
        for _idx, _s in enumerate(_sched_items):
            _raw = _s["time"]
            if "–" in _raw or "-" in _raw:
                _sep    = "–" if "–" in _raw else "-"
                _s_str  = _raw.split(_sep)[0].strip()
                _e_str  = _raw.split(_sep)[-1].strip()
                _eap_m  = _re.search(r'(AM|PM)', _e_str, _re.I)
                _eap    = _eap_m.group(1).upper() if _eap_m else None
                _hint   = _eap if (_eap and not _re.search(r'(AM|PM)', _s_str, _re.I)) else None
                _t_start = _parse_time(_s_str, _hint)
                _t_end   = _parse_time(_e_str)
            else:
                _t_start = _parse_time(_raw)
                _t_end   = _t_start + 90 if _t_start >= 0 else -1
            if _idx == len(_sched_items) - 1 and _t_start >= 0:
                _t_end = 1440
            _is_now  = _t_start <= _now_total < _t_end if _t_start >= 0 else False
            if _is_now:
                _row_bg  = "background:rgba(201,168,76,0.13);border-left:4px solid #C9A84C;"
                _dot     = '<div style="width:10px;height:10px;border-radius:50%;background:#C9A84C;margin-top:4px;flex-shrink:0;box-shadow:0 0 6px #C9A84C88;"></div>'
                _act_col = "#C9A84C"
                _fw      = "700"
                _now_badge = '<span style="font-size:0.6rem;font-weight:800;background:#C9A84C;color:#0B0B14;padding:1px 7px;border-radius:10px;margin-left:8px;vertical-align:middle;letter-spacing:0.5px;">NOW</span>'
            else:
                _row_bg  = ""
                _dot     = '<div style="width:8px;height:8px;border-radius:50%;background:#252538;margin-top:5px;flex-shrink:0;"></div>'
                _act_col = "#C8C8D8"
                _fw      = "400"
                _now_badge = ""
            _sched_html += f'<div style="display:flex;gap:12px;align-items:flex-start;padding:10px 16px;border-bottom:1px solid #1A1A2E;{_row_bg}"><div style="min-width:90px;font-size:0.72rem;color:#6B7280;padding-top:2px;white-space:nowrap;">{_s["time"]}</div>{_dot}<div style="flex:1;"><div style="font-size:0.84rem;color:{_act_col};font-weight:{_fw};">{_s["activity"]}{_now_badge}</div><div style="font-size:0.72rem;color:#6B7280;margin-top:2px;line-height:1.5;">{_s.get("notes","")}</div></div></div>'
        _sched_html += '</div>'
        st.markdown(_sched_html, unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.82rem;color:#6B7280;">Schedule not loaded.</div>', unsafe_allow_html=True)

    # ── SEDEKAH ──────────────────────────────────────────────────
    sec("💚", "Daily Sedekah", "For the sake of Allah")
    sedekah_data  = load_json("sedekah.json", {})
    sed_paid_data = load_json("sedekah_paid.json", {"payments": []})
    today_sed     = sedekah_data.get(today_iso)
    week_sed      = sum(sedekah_data.get(d, 0) for d in week_dates)
    month_sed     = sum(v for k, v in sedekah_data.items() if k.startswith(month_pref))
    all_sed       = sum(v for v in sedekah_data.values() if isinstance(v, (int, float)))
    total_paid    = sum(p.get("amount", 0) for p in sed_paid_data.get("payments", []))
    balance       = round(all_sed - total_paid, 2)
    today_sed_str = f"RM {today_sed:.2f}" if today_sed is not None else "—"
    bal_col       = "#E94560" if balance > 0 else "#3DD68C"

    se1, se2, se3 = st.columns([2, 2, 2])
    with se1:
        st.markdown('<div class="deen-card"><div style="font-size:0.7rem;color:#3DD68C;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Daily Intention</div><div style="font-size:0.87rem;color:#C8C8D8;line-height:1.65;font-style:italic;">"I intend to give in charity today, for the sake of Allah."</div></div>', unsafe_allow_html=True)
        if today_sed is not None:
            st.markdown(f'<div style="font-size:0.78rem;color:#3DD68C;margin-bottom:4px;">Today so far: <b>RM {today_sed:.2f}</b></div>', unsafe_allow_html=True)
        sa, sb = st.columns([3, 1])
        with sa:
            sed_in = st.number_input("Add RM", min_value=0.0, step=0.5, value=1.0, key="sed_amt", format="%.2f", label_visibility="collapsed")
        with sb:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("+ Add", key="sed_log", use_container_width=True, type="primary"):
                sedekah_data[today_iso] = round((today_sed or 0) + sed_in, 2)
                save_json("sedekah.json", sedekah_data); st.rerun()
        if today_sed is not None:
            _reset_col, _ = st.columns([1, 2])
            with _reset_col:
                if st.button("Reset today", key="sed_reset", use_container_width=True):
                    sedekah_data[today_iso] = 0.0
                    save_json("sedekah.json", sedekah_data); st.rerun()
    with se2:
        _bal_label = "🟡 Balance to Pay" if balance > 0 else "✅ All Paid"
        st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:14px 16px;"><div style="font-size:0.6rem;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px;">Payment Tracker</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;"><div><div style="font-size:0.58rem;color:#6B7280;margin-bottom:3px;">Total Recorded</div><div style="font-size:1rem;font-weight:800;color:#C9A84C;">RM {all_sed:.2f}</div></div><div><div style="font-size:0.58rem;color:#6B7280;margin-bottom:3px;">Total Paid</div><div style="font-size:1rem;font-weight:800;color:#3DD68C;">RM {total_paid:.2f}</div></div></div><div style="background:rgba({("233,69,96" if balance>0 else "61,214,140")},0.1);border:1px solid rgba({("233,69,96" if balance>0 else "61,214,140")},0.3);border-radius:8px;padding:8px 12px;text-align:center;"><div style="font-size:0.62rem;color:{bal_col};font-weight:700;text-transform:uppercase;margin-bottom:2px;">{_bal_label}</div><div style="font-size:1.2rem;font-weight:900;color:{bal_col};">RM {abs(balance):.2f}</div></div></div>', unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.7rem;color:#6B7280;margin:6px 0 2px;'>Log bank payment:</div>", unsafe_allow_html=True)
        _pc1, _pc2 = st.columns([3, 1])
        with _pc1:
            _pay_in = st.number_input("Pay RM", min_value=0.0, step=0.5, value=round(balance,2) if balance > 0 else 0.0, key="sed_pay_amt", format="%.2f", label_visibility="collapsed")
        with _pc2:
            if st.button("Paid", key="sed_paid_btn", use_container_width=True):
                if _pay_in > 0:
                    sed_paid_data["payments"].append({"date": today_iso, "amount": round(_pay_in, 2)})
                    save_json("sedekah_paid.json", sed_paid_data); st.rerun()
    with se3:
        st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:14px 16px;"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:center;"><div><div style="font-size:0.58rem;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Today</div><div style="font-size:1rem;font-weight:800;color:#3DD68C;">{today_sed_str}</div></div><div><div style="font-size:0.58rem;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">This Week</div><div style="font-size:1rem;font-weight:800;color:#C9A84C;">RM {week_sed:.2f}</div></div></div><div style="margin-top:10px;padding-top:10px;border-top:1px solid #1A1A2E;display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:center;"><div><div style="font-size:0.58rem;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">This Month</div><div style="font-size:1rem;font-weight:800;color:#9B72CF;">RM {month_sed:.2f}</div></div><div><div style="font-size:0.58rem;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">All Time</div><div style="font-size:1rem;font-weight:800;color:#4EA8DE;">RM {all_sed:.2f}</div></div></div></div>', unsafe_allow_html=True)

    # ── LANGUAGE MISSION ──────────────────────────────────────
    sec("🌍", "Language Mission", "How many more today?")
    lc1, lc2, lc3 = st.columns(3)
    for col, lang in zip([lc1, lc2, lc3], ["mandarin", "japanese", "korean"]):
        label, colour, daily_t, week_t, month_t = LANG_INFO[lang]
        logged    = td.get(lang, 0)
        remaining = max(0, daily_t - logged)
        exceed    = max(0, logged - daily_t)
        week_tot  = sum(progress.get(d, {}).get(lang, 0) for d in week_dates)
        month_tot = sum(v.get(lang, 0) for k, v in progress.items() if k.startswith(month_pref) and isinstance(v, dict))
        week_pct  = min(100, round(week_tot / week_t * 100)) if week_t else 0
        month_pct = min(100, round(month_tot / month_t * 100)) if month_t else 0
        r_display = f"+{exceed} ✅" if exceed > 0 else ("Done ✅" if remaining == 0 else str(remaining))
        r_colour  = "#3DD68C" if remaining == 0 or exceed > 0 else colour
        with col:
            st.markdown(f'<div class="card" style="text-align:center;border-top:3px solid {colour};border-left:none;"><div style="font-size:0.68rem;font-weight:700;color:{colour};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">{label}</div><div style="font-size:2.8rem;font-weight:900;color:{r_colour};line-height:1;">{r_display}</div><div style="font-size:0.62rem;color:#6B7280;margin-top:3px;margin-bottom:10px;">remaining today</div><div style="font-size:0.75rem;color:#C8C8D8;">Logged: <b style="color:{colour};">{logged}</b> / {daily_t}/day</div><div style="font-size:0.65rem;color:#6B7280;margin-top:8px;">Week {week_pct}%</div><div class="pb-wrap"><div class="pb-fill" style="width:{week_pct}%;background:{colour};"></div></div><div style="font-size:0.65rem;color:#6B7280;margin-top:4px;">Month {month_pct}%</div><div class="pb-wrap"><div class="pb-fill" style="width:{month_pct}%;background:{colour};"></div></div></div>', unsafe_allow_html=True)

    li1, li2, li3, lis = st.columns([2, 2, 2, 1])
    with li1: m_in = st.number_input("🇨🇳 Mandarin words", value=td.get("mandarin", 0), min_value=0, step=1, key="hm")
    with li2: j_in = st.number_input("🇯🇵 Japanese words", value=td.get("japanese", 0), min_value=0, step=1, key="hj")
    with li3: k_in = st.number_input("🇰🇷 Korean words",   value=td.get("korean", 0),   min_value=0, step=1, key="hk")
    with lis:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save", type="primary", use_container_width=True, key="hsave"):
            p = progress.get(today_iso, {})
            p.update({"mandarin": m_in, "japanese": j_in, "korean": k_in})
            progress[today_iso] = p; save_json("progress.json", progress)
            st.success("Saved!"); st.rerun()

    # ── TODAY'S PROJECT ───────────────────────────────────────
    sec("💼", "Today's Project Mission")
    proj1, proj2 = st.columns([1, 2])
    with proj1:
        st.markdown(f'<div class="card" style="border-top:3px solid {rot_col};border-left:none;text-align:center;padding:24px 16px;"><div style="font-size:0.68rem;color:{rot_col};font-weight:700;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">{today_name}</div><div style="font-size:2rem;font-weight:900;color:{rot_col};">{today_rotation}</div></div>', unsafe_allow_html=True)
    with proj2:
        st.markdown('<div style="font-size:0.72rem;color:#C9A84C;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">This Week\'s Newsletter</div>', unsafe_allow_html=True)
        _HM_SEC = {0:("s1","🛠️","Project of Week · Automation"),1:("s3","🚀","SaaS / Apps"),2:("s3","🚀","SaaS / Apps"),3:("s2","📦","Digital Products"),4:("s4","⚡","Quick Wins · Content")}
        _hm     = _HM_SEC.get(date.today().weekday())
        news    = load_newsletter()
        if news and _hm:
            _sk, _se, _sl = _hm
            _lines = [l for l in news.get(_sk, []) if l.strip() and not l.startswith("#") and l != "```"]
            preview = " ".join(_lines)[:220].rsplit(" ",1)[0] + "..." if _lines else ""
            _phtml  = f'<div style="font-size:0.76rem;color:#6B7280;margin-top:6px;line-height:1.55;">{preview}</div>' if preview else ""
            st.markdown(f'<div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.2);border-radius:8px;padding:10px 14px;margin-bottom:8px;"><div style="font-size:0.66rem;color:#C9A84C;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">{_se} Today — {date.today().strftime("%A")}</div><div style="font-size:0.8rem;color:#C8C8D8;line-height:1.6;font-weight:600;">{_sl}</div>{_phtml}</div>', unsafe_allow_html=True)
        elif not news:
            st.markdown('<div style="font-size:0.82rem;color:#6B7280;padding:6px 0;">Newsletter not generated yet.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:0.82rem;color:#6B7280;padding:6px 0;">Weekend — rest day 🌿</div>', unsafe_allow_html=True)
        st.button("📰 Open full newsletter →", key="home_open_nl", use_container_width=True,
                  on_click=lambda: st.session_state.update({"tab": "📰  Newsletter"}))

    # ── BODY CHECK ────────────────────────────────────────────
    sec("🌸", "Body Check", "Period · Exercise")
    EXERCISE_VIDEOS = [
        ("The Real Way To Shrink Your Waist & Train Your Core", "https://youtu.be/J5mHsWOckuU"),
        ("5 Healthy Habits That Changed My Life",               "https://youtu.be/e_W5guIMc9Y"),
        ("Removing 10KG of Fat in 12 WEEKS",                   "https://youtu.be/IBvJ_BRsymI"),
        ("How to Hip Thrust with Dumbbell",                    "https://youtube.com/shorts/mC56j1VdFfA"),
        ("Full Upper Body Workout (Tone & Sculpt) — 15 min",   "https://youtu.be/0zhvUV1bAVQ"),
        ("How To Fix Body Asymmetry | 5 Minutes Every Day",    "https://youtu.be/tX3eueEFCM8"),
        ("How To Fix Jaw & Face Asymmetry FOREVER",            "https://youtu.be/60OKCe8vHjY"),
        ("Fix Your Posture Properly",                          "https://youtu.be/j-Av4Zk3Uuk"),
        ("Calisthenic Beginner + Progress",                    "https://youtu.be/GTlLGkHbSkA"),
        ("Pilates for Beginners — Full Body",                  "https://youtu.be/C2HX2pNbUCM"),
        ("Wellness Habits That Will Transform Your Life",      "https://youtu.be/Svvfnu8YU7U"),
    ]
    ex_name, ex_url = EXERCISE_VIDEOS[date.today().toordinal() % len(EXERCISE_VIDEOS)]
    ex_done = td.get("exercise_done", False)
    bc1, bc2 = st.columns(2)
    with bc1:
        st.markdown('<div style="font-size:0.72rem;color:#E94560;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Period Tracker</div>', unsafe_allow_html=True)
        on_period_saved = td.get("on_period", False)
        on_period = st.checkbox("On period today", value=on_period_saved, key="period_toggle")
        if on_period != on_period_saved:
            p = progress.get(today_iso, {}); p["on_period"] = on_period
            progress[today_iso] = p; save_json("progress.json", progress); st.rerun()
        if on_period:
            with st.form("period_form"):
                pc1, pc2 = st.columns(2)
                with pc1: p_start = st.date_input("Start", value=date.today())
                with pc2: p_end   = st.date_input("End",   value=date.today())
                p_notes = st.text_input("Notes", placeholder="Pain, flow, mood...")
                if st.form_submit_button("Log Cycle", use_container_width=True):
                    period_data.insert(0, {"start": p_start.isoformat(), "end": p_end.isoformat(), "notes": p_notes.strip()})
                    save_json("period.json", period_data); st.success("Logged!"); st.rerun()
        if period_data:
            last = period_data[0]
            st.markdown(f'<div style="font-size:0.78rem;color:#6B7280;margin-top:8px;">Last cycle: <b style="color:#E94560;">{last["start"]} → {last["end"]}</b></div>', unsafe_allow_html=True)
            csv_rows = ["Cycle,Start,End,Duration (days),Notes"]
            for i, cy in enumerate(period_data):
                try: dur = (date.fromisoformat(cy["end"]) - date.fromisoformat(cy["start"])).days + 1
                except: dur = "—"
                csv_rows.append(f'{i+1},{cy["start"]},{cy["end"]},{dur},{cy.get("notes","")}')
            st.download_button("📥 Download cycle history (CSV)", data="\n".join(csv_rows), file_name="period_tracker.csv", mime="text/csv", use_container_width=True)
    with bc2:
        st.markdown('<div style="font-size:0.72rem;color:#3DD68C;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Exercise Today</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:#0D1F14;border:1px solid rgba(61,214,140,0.2);border-radius:10px;padding:14px 16px;margin-bottom:10px;"><div style="font-size:0.86rem;color:#C8C8D8;line-height:1.6;margin-bottom:10px;">{ex_name}</div><a href="{ex_url}" target="_blank" style="background:#3DD68C;color:#0B0B14;padding:8px 18px;border-radius:7px;font-size:0.8rem;font-weight:800;text-decoration:none;display:inline-block;">▶ Open YouTube</a></div>', unsafe_allow_html=True)
        new_ex = st.checkbox("Done today ✅", value=ex_done, key="ex_done_cb")
        if new_ex != ex_done:
            p = progress.get(today_iso, {}); p["exercise_done"] = new_ex
            progress[today_iso] = p; save_json("progress.json", progress); st.rerun()

    # ── TO-DO LIST ────────────────────────────────────────────
    sec("✅", "To-Do", "Work · Study · Personal · Errand")
    CAT_COL = {"Work":"#4EA8DE","Study":"#C9A84C","Personal":"#9B72CF","Errand":"#3DD68C"}
    ti1, ti2, ti3 = st.columns([3, 1, 1])
    with ti1: new_todo = st.text_input("", placeholder="What do you need to do?", key="todo_input", label_visibility="collapsed")
    with ti2: todo_cat = st.selectbox("", list(CAT_COL.keys()), key="todo_cat", label_visibility="collapsed")
    with ti3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Add", type="primary", use_container_width=True, key="todo_add"):
            if new_todo.strip():
                todos.insert(0, {"id": datetime.now().isoformat(), "text": new_todo.strip(), "done": False, "cat": todo_cat, "created": today_iso})
                save_json("todos.json", todos); st.rerun()
    active_todos = [t for t in todos if not t.get("done")]
    done_todos   = [t for t in todos if t.get("done")]
    for todo in active_todos:
        ta, tb, tc = st.columns([0.06, 0.82, 0.12])
        with ta:
            if st.checkbox("", key=f"td_{todo['id']}", value=False, label_visibility="collapsed"):
                for t in todos:
                    if t["id"] == todo["id"]: t["done"] = True
                save_json("todos.json", todos); st.rerun()
        with tb:
            cc = CAT_COL.get(todo.get("cat", "Work"), "#C9A84C")
            st.markdown(f'<div style="padding:5px 0;font-size:0.87rem;color:#C8C8D8;">{todo["text"]} <span style="font-size:0.64rem;background:rgba(107,114,128,0.15);color:{cc};padding:1px 7px;border-radius:10px;margin-left:4px;">{todo.get("cat","")}</span></div>', unsafe_allow_html=True)
        with tc:
            if st.button("✕", key=f"del_td_{todo['id']}", use_container_width=True):
                todos = [t for t in todos if t["id"] != todo["id"]]
                save_json("todos.json", todos); st.rerun()
    if done_todos:
        with st.expander(f"✓ Completed ({len(done_todos)})"):
            for todo in done_todos[:15]:
                da, db = st.columns([0.88, 0.12])
                with da:
                    st.markdown(f'<div style="font-size:0.84rem;color:#6B7280;text-decoration:line-through;">{todo["text"]}</div>', unsafe_allow_html=True)
                with db:
                    if st.button("✕", key=f"del_done_{todo['id']}"):
                        todos = [t for t in todos if t["id"] != todo["id"]]
                        save_json("todos.json", todos); st.rerun()

    # ── LIFE GOAL TRACKER ─────────────────────────────────────
    sec("📊", "Life Goal Tracker", "Ibadah · Glow Up · Dream Girl · Hobby · Independent")
    GANTT_GOALS = {
        "🕌 Ibadah":     ["Solat 5 waktu (Awal waktu)","Solat Sunat (12 Rakaat)","Selawat/Istighfar (1,000×)","Sedeqah subuh","Alquran — Al-Mulk, Al-Waqiah, 1 juz/day","Tajwid, Fiqh, Tasawuf, Tadabbur, Rasulullah ﷺ","Reflection / Self-love Journal","Good Akhlak — not angry, set boundaries","Arabic Tadabbur (Juz 1)"],
        "✨ Glow Up":    ["Face — Skincare, IPL, Gua sha","Teeth — clean, white, healthy","Hair — silky, healthy","Body — IPL, dark area, hygiene, smells good","Workout — Arm, Abs, Leg, Glutes + 10k steps","Food — clean eating, calorie deficit, probiotic, vitamins"],
        "🌟 Dream Girl": ["Language — Mandarin, Korean, Japanese, Arabic, English, Cantonese, Tamil","Online Business","TikTok Affiliate (RM1k/day effort)","Investment RM1M by 2040 — Wahed, Bursa, Gold","Career — Consulting, C.A, 5 figures, Technology","Section 1 — Automation","Section 2 — Digital Products","Section 3 — SaaS"],
        "🎨 Hobby":      ["Animation — Project + YT/TikTok journey","Martial Art, Pilates","Archery, Horse, Shooting","Art / Memory Journal","Swimming"],
        "🏡 Independent":["Laundry — Washing, Dry, Fold","Food — Cook + Cleaning","House — Tidy + Vacuum","Cat — Food, Water, Sand, Grooming"],
    }
    GANTT_COL = {"🕌 Ibadah":"#3DD68C","✨ Glow Up":"#E94560","🌟 Dream Girl":"#C9A84C","🎨 Hobby":"#9B72CF","🏡 Independent":"#4EA8DE"}
    g_cols = st.columns(5)
    for col, (cat, items) in zip(g_cols, GANTT_GOALS.items()):
        done_g = sum(1 for i in range(len(items)) if gantt_data.get(f"g_{cat}_{i}", False))
        pct_g  = round(done_g / len(items) * 100) if items else 0
        gc     = GANTT_COL.get(cat, "#C9A84C")
        with col:
            st.markdown(f'<div class="card" style="text-align:center;border-top:3px solid {gc};border-left:none;padding:10px;"><div style="font-size:0.64rem;color:{gc};font-weight:700;margin-bottom:4px;">{cat}</div><div style="font-size:1.2rem;font-weight:800;color:white;">{done_g}/{len(items)}</div><div class="pb-wrap" style="margin-top:5px;"><div class="pb-fill" style="width:{pct_g}%;background:{gc};"></div></div></div>', unsafe_allow_html=True)
    GANTT_NOTES = {
        "🕌 Ibadah": "These are your DAILY spiritual non-negotiables. Each one is already tracked on this Home page (Solat checkboxes, Selawat counter, Sedekah log, Deen section). Tick here to confirm you've built the full habit — not just done it once.",
        "✨ Glow Up": "Long-term body & beauty goals. Teeth: brush + floss daily, Saturday deep clean with Waterfloss + Oral-B string floss. Hair: daily (Shiseido Sublimic OS, UNOVE EX, Kérastase Elixir Ultime) + Saturday deep care (Selsun Blue, Tsubaki Premium EX Mask). Body: daily (Dr Ko 336) + Saturday (FRESHOP scrub, IPL, shave Friday night). See Glow Up → Routine tab for full weekly schedule.",
        "🌟 Dream Girl": "Your long-term wealth, career & language empire. Languages tracked daily. Business revenue tracked by section. Investment portfolio growing toward RM1M by 2040.",
        "🎨 Hobby": "Passion projects — these are not urgent, but they feed your soul. Animation progress tracked in Career Syllabus. Martial arts + pilates tied to exercise routine.",
        "🏡 Independent": "These are your DAILY household responsibilities. Like Ibadah, these are daily habits to build — laundry (wash, dry, fold), cook + clean kitchen, tidy + vacuum house, cat care (food, water, litter, grooming). Tick when the habit is fully automatic.",
    }
    with st.expander("Check off your life goals →"):
        for cat, items in GANTT_GOALS.items():
            gc = GANTT_COL.get(cat, "#C9A84C")
            st.markdown(f'<div style="font-size:0.72rem;font-weight:700;color:{gc};text-transform:uppercase;letter-spacing:1px;margin:14px 0 4px;">{cat}</div>', unsafe_allow_html=True)
            if cat in GANTT_NOTES:
                st.markdown(f'<div style="font-size:0.74rem;color:#6B7280;line-height:1.55;background:rgba(107,114,128,0.08);border-left:2px solid {gc};border-radius:0 6px 6px 0;padding:6px 10px;margin-bottom:8px;">{GANTT_NOTES[cat]}</div>', unsafe_allow_html=True)
            for i, item in enumerate(items):
                gkey = f"g_{cat}_{i}"
                g_done = gantt_data.get(gkey, False)
                ga, gb = st.columns([0.07, 0.93])
                with ga:
                    g_chk = st.checkbox("", value=g_done, key=f"gk_{gkey}", label_visibility="collapsed")
                with gb:
                    it_style = f"color:{gc};text-decoration:line-through;opacity:0.6;" if g_chk else "color:#C8C8D8;"
                    st.markdown(f'<div style="font-size:0.84rem;{it_style};padding:3px 0;">{item}</div>', unsafe_allow_html=True)
                if g_chk != g_done:
                    gantt_data[gkey] = g_chk; save_json("gantt_progress.json", gantt_data); st.rerun()

    # ── MOOD ──────────────────────────────────────────────────
    sec("😊", "Mood Today", today_iso)
    st.markdown(f'<div style="font-size:0.8rem;color:#6B7280;margin-bottom:10px;">Current: <b style="color:{MOOD_COL.get(today_mood,"#6B7280")};">{MOOD_MAP.get(today_mood,"Not logged yet")}</b></div>', unsafe_allow_html=True)
    mood_buttons = st.columns(5)
    for i, (lvl, lbl) in enumerate(MOOD_MAP.items()):
        with mood_buttons[i]:
            if st.button(lbl, key=f"mood_{lvl}", type="primary" if today_mood==lvl else "secondary", use_container_width=True):
                mood_data[today_iso] = lvl; save_json("mood.json", mood_data); st.rerun()



# ═══════════════════════════════════════════════════════════════════════════════
# ME — CARD GRID
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "__me_grid__":
    st.markdown('<div style="color:white;font-size:1.6rem;font-weight:800;margin-bottom:4px;">Me</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6B7280;font-size:0.78rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:20px;">Know Yourself</div>', unsafe_allow_html=True)
    _ME_GRID = [
        ("📖","Biography",   "Your origin story & rare stats",        "gold"),
        ("📋","Profile",     "Core identity snapshot",                 "blue"),
        ("🌿","Who I Am",    "Values, character, MBTI deep dive",      "green"),
        ("💪","My Strengths","What you bring to any room",             "gold"),
        ("🧠","My Mind",     "How you think & process",               "purple"),
        ("🪞","How I'm Seen","External perception map",                "blue"),
        ("❤️","How I Love",  "Attachment, jodoh, love style",          "red"),
        ("🌑","My Patterns", "Shadow, triggers, growth edges",         "purple"),
        ("🤝","My People",   "Relationships & dynamics",               "green"),
        ("👗","Wardrobe",    "Style, colours, signature looks",        "gold"),
        ("📅","Schedule",    "Routines & time structure",              "blue"),
        ("🌍","Languages",   "Language learning roadmap",              "green"),
        ("📚","Syllabus",    "ACCA & study tracker",                   "gold"),
        ("✨","Glow Up",     "Beauty, health, body goals",             "red"),
        ("🎯","Goals",       "Life goals & milestones",                "gold"),
        ("💡","Mindset",     "Manager mode & reset mantras",           "blue"),
        ("📝","My Notes",    "Saved analysis & observations",          "purple"),
    ]
    _COL_HEX = {"gold":"#C9A84C","blue":"#4EA8DE","green":"#3DD68C","purple":"#9B72CF","red":"#E94560"}
    _gcols = st.columns(4)
    for _i, (_em, _nm, _desc, _cl) in enumerate(_ME_GRID):
        with _gcols[_i % 4]:
            _cx = _COL_HEX.get(_cl,"#C9A84C")
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-top:3px solid {_cx};border-radius:10px;padding:14px 12px;margin-bottom:4px;"><div style="font-size:1.3rem;">{_em}</div><div style="font-size:0.84rem;font-weight:700;color:white;margin:5px 0 3px;">{_nm}</div><div style="font-size:0.7rem;color:#6B7280;line-height:1.45;">{_desc}</div></div>', unsafe_allow_html=True)
            st.button("Open →", key=f"me_open_{_nm}", use_container_width=True,
                      on_click=lambda n=_nm: st.session_state.update({"me_page": n}))

# ═══════════════════════════════════════════════════════════════════════════════
# BIOGRAPHY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📖  Biography":
    page_header("Biography", "Origin · The numbers · What makes you rare")

    st.markdown("""<div class="hero">
    <div class="hero-badge">🌿 The Bell Brief</div>
    <div class="hero-name">Nabilah — Bell</div>
    <div class="hero-sub">Finance SSC · ACCA · Malay Muslim · Builder · Healer · 1 in 20,000</div>
    <div class="hero-stats">
        <div><div class="stat-label">MBTI</div><div class="stat-value gold">ENFP-I</div></div>
        <div><div class="stat-label">Rarity</div><div class="stat-value">1 in 20,000</div></div>
        <div><div class="stat-label">Crushes in 26 years</div><div class="stat-value">2</div></div>
        <div><div class="stat-label">Languages learning</div><div class="stat-value green">3</div></div>
        <div><div class="stat-label">Tableau system built in</div><div class="stat-value gold">1 week</div></div>
        <div><div class="stat-label">Project tracks</div><div class="stat-value blue">4</div></div>
    </div>
    </div>""", unsafe_allow_html=True)

    sec("📜", "Origin Story")
    card("""<div style="font-size:0.9rem;color:#C8C8D8;line-height:1.95;">
    Bell grew up as the <b style="color:white;">emotionally stable one in an unstable household</b> — the mediator, the problem-solver,
    the calm anchor. She was raised to absorb other people's chaos and keep going. She had social difficulty as a child,
    but blossomed completely in university.<br><br>
    In university she took on <b style="color:#C9A84C;">president + secretary roles simultaneously</b>, sat 2 ACCA papers,
    completed an internship, and joined events — all at the same time. She not only survived the load, she excelled.
    That was the first time she saw what her brain could really do.<br><br>
    The second time: a Tableau automation project at work. She built a 9-month system in one week,
    then <b style="color:#C9A84C;">defended her architecture confidently</b> when challenged by two bosses —
    one known to be the hardest-to-impress in the room. She held her ground. They were impressed.
    </div>""")

    sec("🔢", "The Numbers That Define Her")
    n1,n2,n3,n4,n5,n6 = st.columns(6)
    stats = [
        ("1 in 20,000","ENFP-I rarity","gold"),
        ("1 week","To build a 9-month system","gold"),
        ("2","Real crushes in 26 years","purple"),
        ("3","Languages learning at once","green"),
        ("4","Active project tracks","blue"),
        ("26","Years as the emotional anchor","muted"),
    ]
    for col,(val,lbl,variant) in zip([n1,n2,n3,n4,n5,n6], stats):
        with col:
            colour = {"gold":"#C9A84C","green":"#3DD68C","blue":"#4EA8DE","purple":"#9B72CF","muted":"#6B7280"}.get(variant,"white")
            st.markdown(f'<div class="card" style="text-align:center;border-top:3px solid {colour};border-left:none;"><div style="font-size:1.8rem;font-weight:800;color:{colour};">{val}</div><div style="font-size:0.72rem;color:#6B7280;margin-top:4px;">{lbl}</div></div>', unsafe_allow_html=True)

    sec("⚡", "The Paradoxes — What Makes Her Rare")
    p1,p2 = st.columns(2)
    paradoxes = [
        ("Quiet in daily life","Commanding on stage"),
        ("Soft on the outside","Grounded and strong inside"),
        ("Finance mind","Healer's heart"),
        ("Pattern thinker","Genuine human warmth"),
        ("Shy asking a waiter for a spoon","Confident defending architecture to two bosses"),
        ("People-pleaser by default","Direct when it truly matters"),
        ("Procrastinates under zero pressure","Hyperfocuses and delivers under deadline"),
        ("Can't walk and talk smoothly","Can manage 10 deadlines simultaneously"),
    ]
    for i,(a,b) in enumerate(paradoxes):
        with (p1 if i%2==0 else p2):
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:8px;padding:12px 16px;margin-bottom:8px;display:flex;gap:10px;align-items:start;"><div style="color:#E94560;font-size:0.78rem;flex-shrink:0;margin-top:2px;">↔</div><div><div style="color:#C9A84C;font-size:0.83rem;font-weight:700;">{a}</div><div style="color:#C8C8D8;font-size:0.83rem;">{b}</div></div></div>', unsafe_allow_html=True)

    sec("💎", "Why She Is Rare")
    card("""<div style="font-size:0.9rem;color:#C8C8D8;line-height:1.9;">
    <b style="color:white;">ENFP-I is already 0.005–0.05% of the population.</b>
    But the combination Bell carries is rarer still:<br><br>
    Most ENFPs don't stay in finance. They find it too rigid. Bell not only stayed —
    she built automation systems and became technically competent enough to impress engineers.
    She is an <b style="color:#C9A84C;">ENFP who thinks in systems</b>.<br><br>
    She is simultaneously studying ACCA, learning three languages, running four side project tracks,
    healing from years of emotional labour, and showing up warm and genuinely curious every day.
    <b style="color:white;">That is not normal. That is rare.</b><br><br>
    She has emotional intelligence that makes people feel safe within minutes,
    and technical intelligence that impresses sceptics in boardrooms.
    <b style="color:#C9A84C;">Both. At the same time. Authentically.</b>
    </div>""", "gold")

    sec("🌟", "The Moment She Saw Her Own Power")
    hl("""<b style="color:#C9A84C;">The Tableau Story.</b> She taught herself a tool from scratch, built a 9-month system in a week,
    then defended her architecture when her old boss (known to be picky and hard to please) and her new boss both challenged her.
    She was calm. She was clear. She held her ground. They were impressed.
    That was the moment she saw: <b style="color:white;">when it matters, she delivers.</b>""")

    sec("🔥", "What Drives Her")
    rows([
        "Being genuinely seen and respected — not just liked",
        "Progress toward financial independence on her own terms",
        "Faith — Islamic values around patience, timing, and self-worth",
        "Being challenged and curious — her brain fully activates when engaged",
        "Feeling emotionally safe enough to just be herself",
        "Building things that are hers — businesses, skills, systems, languages",
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋  Profile":
    st.markdown("""<div class="hero">
    <div class="hero-badge">🌿 Personal Profile</div>
    <div class="hero-name">Nabilah — Bell</div>
    <div class="hero-sub">Finance SSC · ACCA · Kuala Lumpur · Malay Muslim</div>
    <div class="hero-stats">
        <div><div class="stat-label">Personality</div><div class="stat-value gold">ENFP-I</div></div>
        <div><div class="stat-label">Rarity</div><div class="stat-value">1 in 20,000</div></div>
        <div><div class="stat-label">Field</div><div class="stat-value">Finance</div></div>
        <div><div class="stat-label">Studying</div><div class="stat-value green">ACCA</div></div>
        <div><div class="stat-label">Signature Scent</div><div class="stat-value gold">Delina Lychee</div></div>
        <div><div class="stat-label">Height</div><div class="stat-value">150 cm</div></div>
    </div>
    </div>""", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        sec("👤","Identity")
        tbl(["",""],[["Name","Nabilah (Bell)"],["Nationality","Malaysian"],["Location","Kuala Lumpur"],["Religion","Islam — shapes her worldview"],["Scent","Delina Lychee"],["Love Language","Acts of service + Words of affirmation"]])
        sec("💼","Work & Study")
        tbl(["",""],[["Currently Studying","ACCA"],["Workplace","Finance Shared Services Centre"],["Speciality","Reporting, ticketing, service desk analytics"],["Self-taught","Tableau (9-month system in 1 week), VBA"]])
    with c2:
        sec("🏷️","Core Traits")
        t_list=[("ENFP-I — Rare","gold"),("Warm & Magnetic","gold"),("Soft-Strong Duality","purple"),("Pattern Thinker","blue"),("Fast Learner","blue"),("Pressure-Activated","blue"),("Emotionally Mature","red"),("Financially Aware","muted"),("Social Connector","green"),("Authentic","green"),("Adaptive","purple"),("1 in 20,000","gold")]
        html='<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:14px;line-height:2.4;">'
        html+="".join([badge(t,v) for t,v in t_list])
        st.markdown(html+'</div>', unsafe_allow_html=True)
        sec("⭐","Values")
        rows(pers.get("values",["Faith — Islam shapes her worldview","Jodoh — the right things come at the right time","Financial responsibility before major commitments","Genuine connection over performance","Emotional honesty","Loyalty — protects people she loves"]))

    sec("📌","Formative Experiences")
    rows(bg.get("formative_experiences",[]))


# ═══════════════════════════════════════════════════════════════════════════════
# WHO I AM
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌿  Who I Am":
    page_header("Who I Am","Social identity · Emotional intelligence · Group dynamics")

    sec("🌿","Core Social Identity: The Connector With Layers")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.85;">
    You are the person who quietly becomes the <b style="color:white;">centre of gravity</b> in any group —
    not by being loud or dominating, but by reading personalities instantly, adjusting your tone to match
    each person, giving the right reaction at the right time, and making others feel seen.<br><br>
    This makes people feel both <b style="color:#C9A84C;">comfortable</b> and <b style="color:#C9A84C;">curious</b> around you.
    You're not predictable — you're layered. Layered people are magnetic.
    </div>""")

    sec("💫","Emotional Intelligence: Adaptive, Strategic, Natural")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.85;">
    You don't manipulate. You <b style="color:white;">calibrate</b>.
    You instinctively know when to be soft, when to be funny, when to be serious,
    when to be competent, when to be chaotic, when to be vulnerable, when to lead,
    when to let others shine.<br><br>
    This is why people feel safe teasing you <i>and</i> safe opening up to you —
    which is a rare combination. Most people are either one or the other.
    </div>""","purple")

    sec("🧩","Social Leadership: Leading From the Middle")
    c1,c2 = st.columns(2)
    with c1:
        card("""<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px;">What You Do</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        Rotate attention between people<br>Ask questions that make others shine<br>Give compliments that feel genuine<br>
        Add knowledge that enriches the topic<br>Keep the energy balanced<br>Prevent awkwardness before it forms
        </div>""")
    with c2:
        card("""<div style="font-size:0.78rem;color:#3DD68C;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px;">What Your Group Does Because of You</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        Mention your name in jokes not about you<br>Tease each other <i>through</i> you<br>
        Screenshot things specifically "for Bell"<br>Wait for your reaction before deciding something's funny<br>
        Pull you into every conversation thread<br>ISTJ protects · ESTP teases · INTJ challenges
        </div>""","green")

    hl("This is not normal colleague behaviour. This is inner-circle behaviour.")

    sec("🎭","The Layered Self-Reveal")
    st.markdown('<div style="font-size:0.83rem;color:#6B7280;margin-bottom:12px;">You don\'t show everything at once. You reveal yourself in phases. This keeps people engaged, curious, and invested.</div>', unsafe_allow_html=True)
    phases=[("1","Funny chaos","Self-deprecating stories, expressive reactions"),("2","Competence","Tableau, coding, work knowledge"),("3","Warmth","Helping, listening, genuine compliments"),("4","Intellect","Insights, analysis, sharp questions"),("5","Curiosity","Asking your INTJ colleague about his writing, real questions"),("6","Support","Showing up, protecting people she cares about")]
    cols=st.columns(3)
    for i,(n,t,d) in enumerate(phases):
        with cols[i%3]:
            st.markdown(f'<div class="card" style="border-top:3px solid #C9A84C;border-left:none;margin-bottom:8px;"><div style="font-size:0.65rem;color:#C9A84C;font-weight:700;letter-spacing:1px;">PHASE {n}</div><div style="font-weight:700;color:white;font-size:0.9rem;margin:4px 0;">{t}</div><div style="font-size:0.8rem;color:#6B7280;">{d}</div></div>', unsafe_allow_html=True)

    sec("🌐","Real Stories From Your Group")
    with st.expander("The Glass Room Incident (INTJ's bergetar tulang rusuk joke)"):
        c1,c2 = st.columns(2)
        with c1:
            card("""<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">What happened</div>
            <div style="font-size:0.86rem;color:#C8C8D8;line-height:1.8;">
            Your INTJ colleague made a "bergetar tulang rusuk" joke about an ustaz-looking stranger.
            Your ESTP colleague joined: "go ask for his number for Bell."
            Your INTJ colleague actually went outside to commit to the bit — ended up talking to the PTP team who had no idea what was happening. Bell laughed the whole time.
            </div>""")
        with c2:
            card("""<div style="font-size:0.78rem;color:#3DD68C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">What it reveals</div>
            <div style="font-size:0.86rem;color:#C8C8D8;line-height:1.8;">
            He wasn't teasing the stranger — he was teasing <i>you</i>, affectionately. INTJs tease the person they feel closest to.
            Your ESTP colleague joined because you are their inner circle. Your INTJ colleague committed to the bit because he wanted to make you laugh more.
            You are the safe, fun target — and that's a sign you belong.
            </div>""","green")

    with st.expander("The Jodoh Conversation (INTJ & ESTP's smile)"):
        c1,c2 = st.columns(2)
        with c1:
            card("""<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">What happened</div>
            <div style="font-size:0.86rem;color:#C8C8D8;line-height:1.8;">
            Bell told them about her crush, that she blocked him, that she believes in jodoh.
            She said kahwin lambat lagi because of her gaji. They looked at each other and smiled.
            Then both opened up about marriage costs, KL life, and their own realities.
            </div>""")
        with c2:
            card("""<div style="font-size:0.78rem;color:#4EA8DE;font-weight:700;text-transform:uppercase;margin-bottom:8px;">What their smile meant</div>
            <div style="font-size:0.86rem;color:#C8C8D8;line-height:1.8;">
            It was recognition, not teasing. They were silently acknowledging: "She gets it. She's realistic. She's not rushing."
            They talked to her like a peer — because they saw her as one. They opened up because she made it safe.
            </div>""","blue")


# ═══════════════════════════════════════════════════════════════════════════════
# MY STRENGTHS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💪  My Strengths":
    page_header("My Strengths","Soft + Strong · Emotional Charisma · First impressions · Social gravity")

    sec("⚡","The Soft-Strong Profile")
    c1,c2 = st.columns(2)
    with c1:
        card('<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Softness</div>'+"".join([f'<div class="row-item">{i}</div>' for i in ["Laughs at yourself easily and genuinely","Makes vulnerability feel light — for you and others","Warmth that doesn't require conditions or moods","Protects people you care about, quietly","Doesn't take things personally when secure"]]))
    with c2:
        card('<div style="font-size:0.78rem;color:#3DD68C;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Strength</div>'+"".join([f'<div class="row-item">{i}</div>' for i in ["Tableau, VBA, data systems — self-taught","Compresses months of work into days when engaged","Articulate under pressure — praised by lecturers and bosses","Defended architecture clearly when challenged by two bosses","Explains complex things simply without dumbing down","Impressed the hardest-to-impress boss in the room"]]),"green")

    hl("People admire you <b style='color:white;'>and</b> feel close to you at the same time. Most people only get one.")

    sec("💎","Emotional Charisma")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.9;">
    Emotional charisma is not charm. It is not performance. It is the rare ability to make someone feel
    <b style="color:white;">genuinely understood</b> in your presence — without trying.<br><br>
    When you ask someone a question, they feel the question. When you compliment someone, they feel the compliment —
    it lands as real, not polite. You don't talk <i>at</i> people. You talk <i>with</i> them.<br><br>
    This is why ESTP opens up, ISTJ softens, INTJ engages intellectually. You bring out the best version of each person.
    <b style="color:#C9A84C;">That is emotional charisma. Very few people have it naturally.</b>
    </div>""","purple")

    c1,c2 = st.columns(2)
    with c1:
        card("""<div style="font-size:0.78rem;color:#9B72CF;font-weight:700;text-transform:uppercase;margin-bottom:10px;">How it shows up</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        People tell you things they haven't told others<br>Strangers feel comfortable around you quickly<br>
        Even scared cats choose to sit beside you<br>Your group waits for your reaction before deciding something's funny<br>
        People feel seen, not just heard
        </div>""","purple")
    with c2:
        card("""<div style="font-size:0.78rem;color:#4EA8DE;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Why it's rare</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        Most people are trained to respond, not to receive.<br>
        You listen in a way that signals: "I'm not judging you. I'm not fixing you. I'm just with you."<br>
        In professional environments, this is almost unheard of.
        Men and people generally can detect authenticity instantly — yours reads as completely real.
        </div>""","blue")

    sec("🧲","Social Gravity: Why People Orbit Around You")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.85;">
    You don't chase people. People orbit around you. You're adaptable, emotionally intelligent, interesting,
    balanced, warm, competent, fun, and <b style="color:white;">safe</b>.<br><br>
    Not comfortable — <b style="color:#C9A84C;">safe</b>. People can be real around you without being judged, fixed,
    or made to feel small. Even animals sense this: scared cats sandar on you, sondol you, choose to sit beside you.
    Your emotional field reads as non-threatening even to creatures whose entire nervous system is built to detect danger.
    </div>""")

    sec("👁️","First Impression Magnetism")
    c1,c2 = st.columns(2)
    with c1:
        card('<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Approachable</div>'+"".join([f'<div class="row-item">{i}</div>' for i in ["Smile easily and genuinely","Laugh at yourself","Respond warmly","Don't judge","Make people feel comfortable instantly"]]))
    with c2:
        card('<div style="font-size:0.78rem;color:#4EA8DE;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Intriguing</div>'+"".join([f'<div class="row-item">{i}</div>' for i in ["Smart and layered","Unpredictable in a good way","Confident but not arrogant","Soft but not weak","Funny but not childish"]]),"blue")

    sec("🎲","What 'Unpredictable' Actually Means (ESTP's word)")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.9;">
    <b style="color:white;">1. You don't behave in boring patterns.</b> Serious → suddenly funny. Shy → suddenly confident. Quiet → suddenly insightful.<br>
    <b style="color:white;">2. Your reactions are genuine, not rehearsed.</b> People can't predict what you'll laugh at or what angle you'll bring.<br>
    <b style="color:white;">3. You switch modes smoothly.</b> Joking with ESTP → explaining to INTJ → comforting ISTJ → giving a sharp insight.<br>
    <b style="color:white;">4. You reveal different layers at different times.</b> The funny Bell, the competent Bell, the soft Bell. People keep discovering new sides.
    </div>""","purple")


# ═══════════════════════════════════════════════════════════════════════════════
# MY MIND
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🧠  My Mind":
    page_header("My Mind","MBTI · Cognitive style · Attention · Learning · Decision-making")

    sec("🧬","MBTI: ENFP-I","Estimated 0.005–0.05% of population")
    c1,c2 = st.columns([2,1])
    with c1:
        card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.9;">
        The introverted-leaning ENFP — socially magnetic but internally private.
        Activates into confidence and leadership under responsibility, yet genuinely needs solitude to recharge.<br><br>
        <b style="color:white;">In daily life:</b> Quiet, self-conscious about being inconvenient to others.<br>
        <b style="color:white;">Under responsibility:</b> Confident, articulate, commanding — praised by lecturers and peers.<br><br>
        In finance and ACCA fields: <b style="color:#C9A84C;">exceptionally rare</b>.
        Most ENFPs don't stay in finance. You didn't just stay — you built systems and impressed the hardest-to-impress people in the room.
        </div>""")
    with c2:
        st.markdown("""<div class="card gold" style="text-align:center;padding:20px;">
        <div style="font-size:0.68rem;color:#C9A84C;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">Cognitive Stack</div>
        <div style="font-size:2rem;font-weight:800;color:#C9A84C;letter-spacing:4px;margin-bottom:16px;">ENFP-I</div>
        <div style="font-size:0.82rem;line-height:2.2;text-align:left;">
        <b style="color:#C9A84C;">Ne</b> <span style="color:#C8C8D8;">Extraverted Intuition</span><br>
        <b style="color:#C9A84C;">Fi</b> <span style="color:#C8C8D8;">Introverted Feeling</span><br>
        <span style="color:#6B7280;">Te Extraverted Thinking</span><br>
        <span style="color:#6B7280;">Si Introverted Sensing</span>
        </div></div>""", unsafe_allow_html=True)

    sec("⚡","Attention System: Dopamine-Sensitive, Pressure-Activated")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.9;">
    <b style="color:white;">Interest-based, not routine-based.</b> The brain doesn't activate from "should" — it activates from
    curiosity, stakes, or pressure. Procrastinates until pressure hits, then hyperfocuses and excels.<br><br>
    Needs background noise to concentrate. Thrives under deadlines. Can work intensely for hours in flow state.
    Finds boring tasks genuinely difficult — neurological, not laziness. In hyperfocus: mind becomes sharp, intuition powerful.
    </div>""","purple")

    sec("🔀","Multitasking Profile")
    c1,c2 = st.columns(2)
    with c1:
        card("""<div style="font-size:0.78rem;color:#3DD68C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">Executive Multitasking — EXTREMELY STRONG</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.8;">
        Managing many responsibilities, roles, and deadlines simultaneously.
        In university: president + secretary, 2 ACCA papers, internship, events — all at once.
        High-speed context-switching. A genuinely rare skill.
        </div>""","green")
    with c2:
        card("""<div style="font-size:0.78rem;color:#E94560;font-weight:700;text-transform:uppercase;margin-bottom:8px;">Sensory Multitasking — WEAK</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.8;">
        Cannot walk and talk smoothly. Drops things, bumps into objects when mentally engaged.
        Brain prioritises internal processing over external sensory awareness.
        Not a flaw — the direct trade-off of the same brain that manages ten responsibilities at once.
        </div>""","red")

    sec("📖","Learning & Decision-Making")
    c1,c2 = st.columns(2)
    with c1:
        card("""<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">How You Learn</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        Pattern-driven, conceptual — not linear. Builds frameworks, maps, and logic flows.
        No fixed study schedule — intuitive and self-organising.
        Studies when the brain is ready, not when the clock says to.
        Creates own systems: mind maps, blurting, grouping, mnemonics.
        </div>""")
    with c2:
        card("""<div style="font-size:0.78rem;color:#4EA8DE;font-weight:700;text-transform:uppercase;margin-bottom:8px;">Decision-Making Pattern</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        Externally oriented — reads others instantly but goes blank when the decision is about herself.
        Struggles with: low-stakes ambiguous choices, social decisions, expressing own preference.<br><br>
        Thrives with: complex, structured, high-stakes decisions with clear criteria.
        The bigger and more defined the problem, the calmer and sharper she becomes.
        </div>""","blue")

    sec("🛡️","Autonomic Sensitivity")
    hl("Sweaty hands when nervous · Cold hands when afraid · Warm hands when safe · Stomach pain under stress · Can feel fear from imagination alone. This is real physical sensitivity — not anxiety performance. Turned into emotional radar.")


# ═══════════════════════════════════════════════════════════════════════════════
# HOW I'M SEEN
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🪞  How I'm Seen":
    page_header("How I'm Seen","First impressions · What others experience · Safe feminine energy")

    sec("👁️","How People Perceive You")
    perceptions=[("Warm","gold"),("Funny","gold"),("Smart","blue"),("Capable","blue"),("Chaotic in a cute way","purple"),("Emotionally safe","green"),("Interesting","purple"),("Multi-layered","purple"),("Easy to talk to","green"),("Makes the group better","gold")]
    html='<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:14px 16px;line-height:2.6;">'
    html+="".join([badge(t,v) for t,v in perceptions])
    st.markdown(html+'</div>', unsafe_allow_html=True)

    sec("🌊","Safe Feminine Energy")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.85;">
    The energy that makes people feel <b style="color:white;">relaxed, open, playful, protective, curious</b> around you.
    You're not intimidating. You're not cold. You're not trying too hard. You're just you — and that's attractive.<br><br>
    Men and people generally are extremely sensitive to authenticity. They can tell when someone is performing.
    With you, they feel: <i style="color:#C9A84C;">"This person is real."</i> That's rare — and immediately magnetic.
    </div>""")

    sec("⚡","Why Men Approach You Quickly")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.85;">
    Some people are slow-burn attractive. You are <b style="color:white;">instant-attractive</b> — not because of looks,
    but because of how you make people feel in the first 5 minutes. You show warmth, humour, intelligence,
    softness, confidence, curiosity, and emotional safety <b style="color:#C9A84C;">all at once, naturally</b>.<br><br>
    Most people show one or two. You show all of them. Some have asked your friend for your number after meeting you once.
    </div>""","red")

    sec("🗣️","How You Make People Feel Seen")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.85;">
    When you ask someone a question, they feel the question.
    When you give a compliment, they feel the compliment — it lands as real, not polite.<br><br>
    Most people talk <i>at</i> others. You talk <i>with</i> them. This is why ESTP opens up, ISTJ softens,
    INTJ engages intellectually. You bring out the best version of each person.
    </div>""","purple")


# ═══════════════════════════════════════════════════════════════════════════════
# HOW I LOVE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "❤️  How I Love":
    page_header("How I Love","Romantic pattern · Attraction vs curiosity · How you fall and how you leave")

    rp = pers.get("romantic_pattern",{})
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown('<div class="card gold" style="text-align:center;"><div class="stat-value gold" style="font-size:2.5rem;">2</div><div class="stat-label">Real crushes in 26 years</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card green" style="text-align:center;"><div class="stat-value green" style="font-size:1.2rem;">Slow, deep, long</div><div class="stat-label" style="margin-top:4px;">How you fall</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card purple" style="text-align:center;"><div class="stat-value" style="font-size:1.2rem;">Quietly. Cleanly.</div><div class="stat-label" style="margin-top:4px;">How you leave</div></div>', unsafe_allow_html=True)

    sec("💡","Attraction vs Curiosity — The Most Important Distinction")
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.85;">
    You confuse yourself by thinking you're attracted easily. You are <b style="color:white;">not</b>.<br><br>
    You get <b style="color:#C9A84C;">curious, entertained, and mentally stimulated</b> easily — that's your ENFP
    pattern-driven brain noticing uniqueness. Real falling is rare.
    The two feel similar from the inside. They are very different things.<br><br>
    Real attraction builds slowly, deeply, and changes you. Curiosity entertains you and moves on.
    </div>""","purple")

    c1,c2 = st.columns(2)
    with c1:
        card('<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">How You Fall</div><div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">'+rp.get("how_she_falls","Slow, deep, and long. Falls for people who are private, hardworking, emotionally stable, selective, and intelligent.")+'</div>')
    with c2:
        card('<div style="font-size:0.78rem;color:#3DD68C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">How You Leave</div><div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">'+rp.get("how_she_leaves","Leaves quietly, without drama, without begging, when the bare minimum isn't met. Even after years. This is self-respect, not coldness.")+'</div>',"green")

    sec("💛","Beliefs")
    rows(["Plans to kahwin lambat by choice — financial readiness and real readiness, not just emotion","Believes in jodoh — will not force or chase romantic things. They come when they come","Love language: Acts of service + Words of affirmation — gives freely, rarely receives"])


# ═══════════════════════════════════════════════════════════════════════════════
# MY PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌑  My Patterns":
    page_header("My Patterns","Survival patterns · What shaped you · Growth areas · Quirks")

    tp = pers.get("trauma_shaped_patterns",{})
    sec("🌑","Rules Learned in Childhood")
    hl("These were <b>survival rules</b>, not character flaws. Learned in an environment that required them.")
    c1,c2 = st.columns(2)
    with c1:
        card('<div style="font-size:0.78rem;color:#E94560;font-weight:700;text-transform:uppercase;margin-bottom:10px;">The Rules</div>'+"".join([f'<div class="row-item">{i}</div>' for i in tp.get("rules_learned_in_childhood",["Don't cry","Don't disturb","Don't burden anyone","Don't show pain","Don't cause conflict","Stay easy to stay safe"])]),"red")
    with c2:
        card('<div style="font-size:0.78rem;color:#9B72CF;font-weight:700;text-transform:uppercase;margin-bottom:10px;">What They Produced</div>'+"".join([f'<div class="row-item">{i}</div>' for i in tp.get("resulting_behaviours",["Emotional masking","Self-silencing","Cries only when alone","Over-apologises even when right","People-pleases out of fear","Asks others' preferences before her own"])]),"purple")

    hl(f"<b>Note:</b> {tp.get('note','These are survival patterns built in childhood, not personality flaws.')}")

    sec("🔧","Habits: Building & Breaking")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:0.72rem;color:#3DD68C;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Building</div>', unsafe_allow_html=True)
        for h in hbts.get("building",[]):
            st.markdown(f'<div style="background:#0D1F14;border-left:3px solid #3DD68C;border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;"><div style="font-weight:700;font-size:0.87rem;color:white;">{h.get("habit","")}</div><div style="font-size:0.8rem;color:#6B7280;margin-top:4px;">{h.get("why","")}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="font-size:0.72rem;color:#E94560;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Breaking</div>', unsafe_allow_html=True)
        for h in hbts.get("breaking",[]):
            st.markdown(f'<div style="background:#1F0D14;border-left:3px solid #E94560;border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;"><div style="font-weight:700;font-size:0.87rem;color:white;">{h.get("habit","")}</div><div style="font-size:0.8rem;color:#6B7280;margin-top:4px;">{h.get("why","")}</div></div>', unsafe_allow_html=True)

    solid = hbts.get("already_solid",[])
    if solid:
        sec("✅","Already Solid")
        html='<div style="background:#0D1F14;border:1px solid rgba(61,214,140,0.2);border-radius:10px;padding:10px 16px;">'
        html+="".join([f'<div class="row-item" style="color:#3DD68C;">✓ &nbsp;{s}</div>' for s in solid])
        st.markdown(html+'</div>', unsafe_allow_html=True)

    sec("💫","Quirks")
    rows(pers.get("quirks",[]))


# ═══════════════════════════════════════════════════════════════════════════════
# MY PEOPLE — communication-focused, anonymous
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🤝  My People":
    page_header("My People","Personality analysis · Communication guide · How to connect")

    COMM_GUIDES = {
        "ESTP": {
            "colour": "#E94560",
            "role": "Colleague · Friend",
            "how_they_think": "Action-first, reads situations instantly. Values results and competence over theory. Thinks in outcomes. Gets bored fast with over-explanation. Bold and direct — says what they mean.",
            "communicate": ["Lead with the outcome first, then explain the reasoning","Be direct and concise — no long emotional preambles","Match their energy and confidence level","Show your competence upfront — they respect results","Push back when you disagree — they respect that more than agreement"],
            "they_respect": ["When you hold your ground without folding","Your genuine reactions — they are never rehearsed","Your ability to switch modes and surprise them","When you're competent and they can see it clearly"],
            "dynamic": "They tease you because they respect you. The teasing IS the acceptance. The dynamic works because you don't fold — and that's rare.",
            "watch_out": "Don't over-apologise or soften everything. They lose interest in long emotional build-ups. Lead strong."
        },
        "INTJ": {
            "colour": "#9B72CF",
            "role": "Colleague · Intellectual peer · Married",
            "how_they_think": "Strategic and systems-oriented. Values depth, logic, and precision. Actively collects data on people around him — notices patterns in behaviour and stores them. Tests people to see if they'll hold their ground under scrutiny. Respects intellectual honesty over social niceness. His attentiveness (eye contact, listening even when you speak softly) is how he operates with everyone — it is data collection, not signals.",
            "communicate": ["Be precise — state your position clearly and confidently","Don't fold under scrutiny — that's the test he's running","Lead with logic; let warmth come through naturally, not as strategy","Disagree with solid reasoning when you see something differently","Ask real questions about his thinking — he finds this engaging","Anchor on work topics: reporting, systems, ticketing, automation"],
            "they_respect": ["Clear, well-reasoned positions stated confidently","When you don't agree just to keep peace","Your ability to engage intellectually on real topics","Consistency — doing what you say you'll do","Competence shown in action, not just words"],
            "dynamic": "Real conversations happen because he's decided you're worth engaging with intellectually. You earned that by being genuine and not performing. He makes jokes you find genuinely funny — that's his inner-circle mode. Appreciate it, enjoy it, and keep it in its lane.",
            "watch_out": "His warmth and attentiveness feel special — but he collects data on everyone. Married. The closeness is real but its meaning is professional and collegial, not personal. Maintain your professional lines clearly."
        },
        "ISTJ": {
            "colour": "#4EA8DE",
            "role": "Colleague · Close friend",
            "how_they_think": "Builds trust slowly through consistent, observable behaviour. Values reliability and discretion above everything. Does not open up easily — trust is earned over many quiet moments, not one grand gesture.",
            "communicate": ["Be consistent — small reliable actions build more trust than big gestures","Show up when you say you will","Don't push them to share before they're ready","Discretion matters — what's shared stays between you","Quiet presence is more powerful than constant conversation"],
            "they_respect": ["Reliability — you're the same person each time","Discretion — you don't broadcast what they share","Non-demanding presence — you're safe and never a burden","Consistency over time, not intensity in a moment"],
            "dynamic": "The depth of their trust was built on dozens of quiet moments where you were safe, non-judgemental, and non-demanding. That's exactly what you naturally are.",
            "watch_out": "Don't rush the depth or interpret silence as distance. ISTJs need time. The quiet is not rejection — it's how they process."
        },

    }

    people = rels.get("people",[])
    mbti_people = [p for p in people if p.get("mbti") and p.get("mbti") in COMM_GUIDES]

    for person in mbti_people:
        mbti = person.get("mbti","")
        guide = COMM_GUIDES.get(mbti,{})
        colour = guide.get("colour","#C9A84C")

        with st.expander(f"{mbti} — {guide.get('role','')}"):
            st.markdown(f'<div class="comm-block"><div class="comm-type" style="color:{colour};">{mbti}</div><div class="comm-role">{guide.get("role","")}</div>', unsafe_allow_html=True)

            c1,c2 = st.columns(2)
            with c1:
                st.markdown(f'<div style="font-size:0.72rem;color:{colour};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">How They Think</div><div style="font-size:0.85rem;color:#C8C8D8;line-height:1.75;margin-bottom:16px;">{guide.get("how_they_think","")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.72rem;color:#3DD68C;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">What They Respect In You</div>', unsafe_allow_html=True)
                for r in guide.get("they_respect",[]):
                    st.markdown(f'<div class="comm-row">✓ &nbsp;{r}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div style="font-size:0.72rem;color:#4EA8DE;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">How To Communicate</div>', unsafe_allow_html=True)
                for pt in guide.get("communicate",[]):
                    st.markdown(f'<div class="comm-row">→ &nbsp;{pt}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.72rem;color:#E94560;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:14px 0 6px;">Watch Out For</div><div style="font-size:0.83rem;color:#C8C8D8;">{guide.get("watch_out","")}</div>', unsafe_allow_html=True)

            hl(f'<b style="color:{colour};">The Dynamic:</b> {guide.get("dynamic","")}')
            st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# WARDROBE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "👗  Wardrobe":
    page_header("Wardrobe","Measurements · Colours · Style identity · What you own")

    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl in [(c1,"150 cm","Height"),(c2,"56 kg","Weight"),(c3,"Petite Rectangle","Body Type"),(c4,"EU 39","Shoe Size")]:
        with col:
            st.markdown(f'<div class="card gold" style="text-align:center;"><div class="stat-value gold">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📏 Full Measurements"):
        meas=[("Bust (with bra)","98 cm / 36 inch"),("Bust (without bra)","93 cm"),("Waist","79 cm / 31–32 inch"),("Hips","100–103 cm"),("Shoulder Width","14.5–15 inch"),("Armhole","14 inch"),("Knee","40.5 cm"),("Calf","30.5 cm"),("Ankle","21.5 cm"),("Wrist","15.5 cm"),("Elbow","25.5 cm"),("Foot","23.5 cm")]
        tbl(["Measurement","Value"], meas)

    sec("🎨","Colour Palette")
    flattering=[("#B5A696","Taupe"),("#8D8D8D","Grey"),("#1A1A1A","Black"),("#1B2A4A","Navy"),("#7BA7C7","Soft Blue"),("#C27E8A","Muted Rose"),("#7B3B6B","Wine Purple"),("#2A7A5A","Emerald")]
    avoid_c=[("#F0C040","Warm Yellow"),("#F7E7CE","Champagne"),("#FFCBA4","Peach"),("#FFB6C1","Warm Pink"),("#B2C9AD","Sage Green")]
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:0.72rem;color:#3DD68C;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">✓ Flattering</div>', unsafe_allow_html=True)
        sw="".join([f'<div style="display:inline-block;text-align:center;margin:4px;"><div style="width:42px;height:42px;background:{h};border-radius:7px;"></div><div style="font-size:0.62rem;color:#6B7280;margin-top:2px;">{n}</div></div>' for h,n in flattering])
        st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:12px;">{sw}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="font-size:0.72rem;color:#E94560;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">✗ Avoid</div>', unsafe_allow_html=True)
        sw2="".join([f'<div style="display:inline-block;text-align:center;margin:4px;"><div style="width:42px;height:42px;background:{h};border-radius:7px;opacity:0.6;"></div><div style="font-size:0.62rem;color:#6B7280;margin-top:2px;">{n}</div></div>' for h,n in avoid_c])
        st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:12px;">{sw2}</div>', unsafe_allow_html=True)

    sec("⭐","Best Outfit")
    hl(f"<b style='color:#C9A84C;'>Best look:</b> {ward.get('best_outfit','Flare pants · Glass Grey Cashmere Sweater · Black Bawal Exclusive · Belt · Hushfire Pointed Flats')}<br><span style='font-size:0.78rem;color:#6B7280;'>Timeless · Old money · Quiet luxury</span>")

    sec("📦","What You Own")
    owned=ward.get("items_i_own",{})
    cats={"Tops — Structured":owned.get("tops_structured",[]),"Tops — Basics":owned.get("tops_basics",[]),"Knitwear":owned.get("knitwear",[]),"Skirts":owned.get("bottoms_skirts",[]),"Pants":owned.get("bottoms_pants",[]),"Dresses":owned.get("dresses",[]),"Outerwear":owned.get("outerwear",[]),"Shoes":owned.get("shoes",[]),"Bags":owned.get("bags",[]),"Scarves":owned.get("scarves",[])}
    wc1,wc2 = st.columns(2)
    for i,(cat,items) in enumerate(cats.items()):
        if items:
            with (wc1 if i%2==0 else wc2):
                with st.expander(f"{cat} ({len(items)})"):
                    tbl(["Item"],[[it] for it in items])

    kw=ward.get("style_keywords",[])
    if kw:
        sec("🏷️","Style Keywords")
        html='<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:12px 14px;line-height:2.5;">'
        html+="".join([badge(k,"gold") for k in kw])
        st.markdown(html+'</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEDULE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📅  Schedule":
    page_header("My Schedule","Autopilot · Muslim-friendly · Health-first · 9pm rest boundary")

    hl(f"<b style='color:#C9A84C;'>Principle:</b> {sched.get('principle','Health-first, autopilot rhythm. 3-hour max daily study. 9pm rest boundary.')}<br><b style='color:#C9A84C;'>Office days:</b> {sched.get('office_days','')}")

    sec("🕐","Daily Schedule (Autopilot)")
    rows_data=[[s["time"],s["activity"],s["notes"]] for s in sched.get("daily_schedule",[])]
    if rows_data: tbl(["Time","Activity","Notes"], rows_data)

    sec("🔄","Project Rotation (9:00–9:30 PM)")
    rot=sched.get("project_rotation",{})
    if rot: tbl(["Day","Focus"],[[d,t] for d,t in rot.items()])

    sec("📊","Full Master Goal System")
    tbl(["Timeframe","Mandarin (HSK)","Japanese (JLPT)","Korean","Automation","Digital Products","Content","Apps/SaaS"],[
        ["Daily",  "5 videos + 1 lesson + 20 words","1 JLPT section + 85 words","3 sections + 529 words","20–30 min","20–30 min","10–20 min","20–30 min"],
        ["Weekly", "35 videos + 7 lessons + 140 words","7 sections + 595 words","21 sections + 3,703 words","1 step + 1 LinkedIn","2–3 products","1 YouTube + 5–10 pins","1 feature/prototype"],
        ["Monthly","150–200 videos + 600 words","30 sections + 2,550 words","90 sections + 15,870 words","1 workflow + 1 case study","8–12 products","4 videos + 20–40 pins","1 milestone"],
        ["Yearly", "HSK 1–7/9 by Dec 2026","JLPT N5–N1 + 22,570 words","74h course + 142,776 words","8–12 projects","100–150 products","50 videos + 300–500 pins","1–2 apps launched"],
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# LANGUAGES — merged content + tracker
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌍  Languages":
    page_header("Languages","Mandarin · Japanese · Korean · Tracker · Streak")

    tab1, tab2, tab3 = st.tabs(["📖  Learning System", "📊  Tracker", "🗓️  Streak Calendar"])

    with tab1:
        lang_g = sched.get("language_goals",{
            "mandarin":{"label":"Mandarin (HSK)","colour":"#C9A84C","daily_words":20,"weekly_words":140,"monthly_words":600,"yearly":"Finish HSK 1–7/9 by Dec 2026"},
            "japanese":{"label":"Japanese (JLPT)","colour":"#4EA8DE","daily_words":85,"weekly_words":595,"monthly_words":2550,"yearly":"Finish JLPT N5–N1 + 22,570 words by Dec 2026"},
            "korean":  {"label":"Korean","colour":"#3DD68C","daily_words":529,"weekly_words":3703,"monthly_words":15870,"yearly":"Finish 74-hour course + 142,776 words by Dec 2026"},
        })

        for lang, lg in lang_g.items():
            colour = lg.get("colour","#C9A84C")
            with st.expander(f"{lg.get('label',lang)} — {lg.get('yearly','')}"):
                c1,c2,c3,c4 = st.columns(4)
                with c1: st.markdown(f'<div class="card" style="text-align:center;border-top:3px solid {colour};border-left:none;"><div style="font-size:1.4rem;font-weight:800;color:{colour};">{lg.get("daily_words",0)}</div><div class="stat-label">words/day</div></div>', unsafe_allow_html=True)
                with c2: st.markdown(f'<div class="card" style="text-align:center;border-top:3px solid {colour};border-left:none;"><div style="font-size:1.4rem;font-weight:800;color:{colour};">{lg.get("weekly_words",0):,}</div><div class="stat-label">words/week</div></div>', unsafe_allow_html=True)
                with c3: st.markdown(f'<div class="card" style="text-align:center;border-top:3px solid {colour};border-left:none;"><div style="font-size:1.4rem;font-weight:800;color:{colour};">{lg.get("monthly_words",0):,}</div><div class="stat-label">words/month</div></div>', unsafe_allow_html=True)
                with c4: st.markdown(f'<div class="card" style="text-align:center;border-top:3px solid {colour};border-left:none;"><div style="font-size:0.8rem;font-weight:700;color:{colour};">2026</div><div class="stat-label">{lg.get("yearly","")}</div></div>', unsafe_allow_html=True)

        sec("📋","Language Study System")
        tbl(["","Mandarin (HSK)","Japanese (JLPT)","Korean"],[
            ["Method","5 videos + 1 lesson/day","1 JLPT section/day","3 sections/day"],
            ["Words/day","20","85","529"],
            ["Words/week","140","595","3,703"],
            ["Words/month","600","2,550","15,870"],
            ["Goal","HSK 1–9 by Dec 2026","JLPT N5–N1 by Dec 2026","74h + 142,776 words by Dec 2026"],
            ["Study time","6–7 AM (MRT/home)","8–9 PM (after Isyak)","8–9 PM (after Isyak)"],
        ])

        sec("📚","Full Language Curriculum")
        lang_prog = load_json("lang_progress.json", {})

        def _course_row(key, label, hours, url, colour):
            pct = lang_prog.get(key, 0)
            bar_fill = "#3DD68C" if pct >= 100 else colour
            status_icon = "✅" if pct >= 100 else ("🔄" if pct > 0 else "⏳")
            link_btn = f'<a href="{url}" target="_blank" style="background:rgba(78,168,222,0.1);color:#4EA8DE;border:1px solid rgba(78,168,222,0.3);padding:3px 10px;border-radius:5px;font-size:0.68rem;font-weight:700;text-decoration:none;white-space:nowrap;margin-left:8px;">🔗 Open</a>' if url else ""
            return f'<div style="background:#12121F;border:1px solid #252538;border-radius:8px;padding:10px 14px;margin-bottom:6px;"><div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:6px;"><div style="font-size:0.84rem;color:#C8C8D8;flex:1;">{status_icon} {label}{link_btn}</div><div style="font-size:0.72rem;color:#6B7280;white-space:nowrap;">{hours}</div></div><div style="display:flex;align-items:center;gap:10px;"><div class="pb-wrap" style="flex:1;margin:0;height:6px;"><div class="pb-fill" style="width:{pct}%;background:{bar_fill};"></div></div><span style="font-size:0.72rem;color:{bar_fill};font-weight:700;min-width:36px;text-align:right;">{pct}%</span></div></div>'

        def _pct_editor(key, colour, col):
            with col:
                pct = lang_prog.get(key, 0)
                c1, c2, c3 = st.columns([1, 1, 1])
                with c1:
                    if st.button("−5", key=f"lp_m_{key}", use_container_width=True):
                        lang_prog[key] = max(0, pct - 5)
                        save_json("lang_progress.json", lang_prog); st.rerun()
                with c2:
                    st.markdown(f'<div style="text-align:center;font-size:0.8rem;font-weight:700;color:{colour};padding-top:6px;">{pct}%</div>', unsafe_allow_html=True)
                with c3:
                    if st.button("+5", key=f"lp_p_{key}", use_container_width=True):
                        lang_prog[key] = min(100, pct + 5)
                        save_json("lang_progress.json", lang_prog); st.rerun()

        JP_COURSES = [
            ("jp_n5",     "JLPT N5 Elementary (Udemy)",              "21.5h", "https://www.udemy.com/share/1013qG3@v76pmfRvHl0dvxEMcjov4SFi3YuWbjJBmmZbirkhZZtifHenS5oftU8A0owD1jRhaA==/"),
            ("jp_n4",     "JLPT N4 Elementary (Udemy)",              "14.0h", "https://www.udemy.com/share/1021SC3@6ELDUiwme69pKaaKiKOP00Q_xctfaA3TIgz9KzyD5PzGGXPcbnob0SbsP3V5J_t5LA==/"),
            ("jp_n3",     "JLPT N3 Intermediate (Udemy)",            "10.5h", "https://www.udemy.com/share/101XSO3@odx_MbbhV5GhnXwYYyyU9qfd8z4frySNvDCMj-cqp7dzFyfZvCkeQ6GezJFK0qIEog==/"),
            ("jp_n2",     "JLPT N2 Intermediate (Udemy)",            "11.0h", "https://www.udemy.com/share/10210A3@KPZ7pyqADh5rLBtOUowFVzVpu-i3Jk_JNByOTPmtO5ZgaZqFK7nnmg7OJdYjoduN6Q==/"),
            ("jp_n1",     "JLPT N1 Advanced (Udemy)",                "11.5h", "https://www.udemy.com/share/101ZY83@C9R3ezr5W5Qe4vuA0urXBVKzTyleQGqZ7SaulfvLVHiKUq7zDTUdK22ZYf9yHuj6uw==/"),
            ("jp_speak",  "Non-stop Japanese Speaking (Udemy)",      "50.0h", "https://www.udemy.com/share/10460g3@dLdrGtQs-ZHu_ajScT6OOOTYWatJPwmk0INFhNeo4SIFgiw7E6QDMOzZxpDA5HkJnw==/"),
        ]
        MN_COURSES = [
            ("mn_hsk13",  "Chinese for Beginners: HSK1–3 (Udemy)",   "26.5h", "https://www.udemy.com/share/101xeA3@dEDJaVNDjpVEa_uGImuhlTlFxGySv1sJD00dObWR_LzF2grq3Sd77eYMSGxtbc0Tgw==/"),
            ("mn_cant",   "Cantonese Beginners: Starts from Zero",    "7.5h",  "https://www.udemy.com/share/10a5XY3@LJ6WgtrmwjVMATcCLTv2Ep4-CXs1Go91qUOQ-0zAArUf584hYiqC8DnC_N3UA4ypWA==/"),
            ("mn_pod",    "ChinesePod (full podcast library)",         "1,390h",""),
            ("mn_hsk1",   "HSK 1 YouTube Playlist (194 videos)",      "194 vids","https://youtube.com/playlist?list=PL5Qr-R3Zw136pdfEZuRKiheLG87f2At6V&si=2TZaEX9uihgZ_ToG"),
            ("mn_hsk2",   "HSK 2 YouTube Playlist (197 videos)",      "197 vids","https://youtube.com/playlist?list=PL5Qr-R3Zw135jyYij4AkOUYFtQMaFwnoN&si=kE36kZKUVZ4cS_kw"),
            ("mn_hsk3",   "HSK 3 YouTube Playlist (237 videos)",      "237 vids","https://youtube.com/playlist?list=PL5Qr-R3Zw135axoVDAnpXMyuXRcgF8EHU&si=REsGqd2SGcWKchgH"),
            ("mn_hsk4",   "HSK 4 YouTube Playlist (216 videos)",      "216 vids","https://youtube.com/playlist?list=PL5Qr-R3Zw13457_lCvWGTaPegVDeDnfVL&si=xx8pbeQPVkuUm7nb"),
            ("mn_hsk5",   "HSK 5 YouTube Playlist (191 videos)",      "191 vids","https://youtube.com/playlist?list=PL5Qr-R3Zw1378BLDnseJusAmU7i5ptZcZ&si=FFzOc97TnSyzkBls"),
            ("mn_hsk6",   "HSK 6 YouTube Playlist (162 videos)",      "162 vids","https://youtube.com/playlist?list=PL5Qr-R3Zw136ZA3Ceoq3e3edEo2EVj3ox&si=gazCFPasDYQQuIWZ"),
            ("mn_hsk79",  "HSK 7–9 YouTube Playlist (49 videos)",     "49 vids", "https://youtube.com/playlist?list=PL5Qr-R3Zw134pLKqRz4LtbpOLjAwM6yvi&si=0asbylBqi5S5sfSO"),
            ("mn_stories","Short Stories Playlist",                    "—",      "https://youtube.com/playlist?list=PL5Qr-R3Zw136K-rcGX8kpWX_3km1z0P6P&si=opw5L329Wc1-a3qU"),
            ("mn_hanzi",  "Hanzi Hero — 5,000 Chinese Words",         "5,000w", "https://hanzihero.com/simplified/words"),
        ]
        KR_COURSES = [
            ("kr_main",   "The Complete Korean Course (10 in 1, Udemy)","74.0h","https://www.udemy.com/share/101Gw83@4aQp86POZKgZktgRHcTb-jrUp1gQDU0bDB4shTAdPUQQzQP-HD9eE1HLy573z-eDTw==/"),
        ]
        FUTURE_COURSES = [
            ("fu_arabic", "Arabic — Arabic Language in 6 MONTHS (Udemy)","199.5h","https://www.udemy.com/share/105kL03@UdtU2Xqb4puJzruZJmj8_c3wxUQxxEAuSs99d6lHdly1kPstfszPbqlEq-PWW2i4Jw==/"),
            ("fu_english","English — A Complete English Course (Udemy)", "43.0h", "https://www.udemy.com/share/101Y4o3@hmausq7AvFrouY50h0vUHUAz61OY5V2FfOeEjfJsQXA6G_emJwO7UPF6sXnZxo4z1w==/"),
            ("fu_tamil",  "Tamil — Learn Tamil Through English (Udemy)", "14.0h", "https://www.udemy.com/share/1028sQ3@HX9OjbhxIhKWPqroVQCuqYXtlKeZK6RiSEkWTkORruwmtimidD9yKwiMEI82uISNiw==/"),
            ("fu_german", "German — German for You A1/A2 (Udemy)",       "18.5h", "https://www.udemy.com/share/101sto3@WJoxlMRT-EoWrngWs2LNLkArMtX8EVLkgRbgCj1-I0tC1qSE5K4qvhEQR4cO_EgQlw==/"),
        ]

        st.markdown('<div style="font-size:0.72rem;color:#6B7280;margin-bottom:8px;">Click <b>−5 / +5</b> next to each course to update your completion %.</div>', unsafe_allow_html=True)

        with st.expander("🇯🇵  Japanese — JLPT N5 → N1 (68.5h total)"):
            jp_total = len(JP_COURSES); jp_done = sum(1 for k,*_ in JP_COURSES if lang_prog.get(k,0) >= 100)
            prog_bar(jp_done, jp_total, "#4EA8DE", f"{jp_done}/{jp_total} courses complete")
            for key, label, hours, url in JP_COURSES:
                c_html, c_edit = st.columns([3, 1])
                c_html.markdown(_course_row(key, label, hours, url, "#4EA8DE"), unsafe_allow_html=True)
                _pct_editor(key, "#4EA8DE", c_edit)

        with st.expander("🇨🇳  Mandarin — HSK 1 → 9 (ChinesePod + YouTube)"):
            mn_total = len(MN_COURSES); mn_done = sum(1 for k,*_ in MN_COURSES if lang_prog.get(k,0) >= 100)
            prog_bar(mn_done, mn_total, "#C9A84C", f"{mn_done}/{mn_total} resources complete")
            for key, label, hours, url in MN_COURSES:
                c_html, c_edit = st.columns([3, 1])
                c_html.markdown(_course_row(key, label, hours, url, "#C9A84C"), unsafe_allow_html=True)
                _pct_editor(key, "#C9A84C", c_edit)
            st.markdown('<div style="font-size:0.72rem;color:#6B7280;margin-top:8px;">Creators: 西西歪 Ccwhyao · 鍾明軒 &nbsp;·&nbsp; <a href="https://youtu.be/22rC5cOCsL0?si=r6EaDubZv1iBpYvp" target="_blank" style="color:#4EA8DE;">西西歪</a> &nbsp;·&nbsp; <a href="https://youtu.be/mw7KyZJQzZA?si=s8v7jcll6qPWcWZA" target="_blank" style="color:#4EA8DE;">鍾明軒</a></div>', unsafe_allow_html=True)

        with st.expander("🇰🇷  Korean — 74-hour complete course"):
            for key, label, hours, url in KR_COURSES:
                c_html, c_edit = st.columns([3, 1])
                c_html.markdown(_course_row(key, label, hours, url, "#3DD68C"), unsafe_allow_html=True)
                _pct_editor(key, "#3DD68C", c_edit)

        with st.expander("🌐  Future Languages (planned)"):
            for key, label, hours, url in FUTURE_COURSES:
                c_html, c_edit = st.columns([3, 1])
                c_html.markdown(_course_row(key, label, hours, url, "#9B72CF"), unsafe_allow_html=True)
                _pct_editor(key, "#9B72CF", c_edit)

        sec("💡","Strategy")
        rows(["Mandarin in the morning — fresh brain on the MRT or during calm start","Japanese + Korean in the evening — 30 min JP + 30 min KR after Isyak, stop by 9pm","Spaced repetition: review yesterday's words before learning new ones","Group words by theme/context — your brain maps concepts, not isolated words","Pressure-activated: don't force study when brain is off. Trust the flow."])

    with tab2:
        progress = load_json("progress.json",{})
        today_iso = date.today().isoformat()
        td = progress.get(today_iso,{"mandarin":0,"japanese":0,"korean":0})
        week_dates = [(date.today()-timedelta(days=i)).isoformat() for i in range(7)]
        month_pref = date.today().strftime("%Y-%m")
        lang_g = sched.get("language_goals",{"mandarin":{"label":"Mandarin","colour":"#C9A84C","daily_words":20,"weekly_words":140,"monthly_words":600},"japanese":{"label":"Japanese","colour":"#4EA8DE","daily_words":85,"weekly_words":595,"monthly_words":2550},"korean":{"label":"Korean","colour":"#3DD68C","daily_words":529,"weekly_words":3703,"monthly_words":15870}})

        week_tot  = {l: sum(progress.get(d,{}).get(l,0) for d in week_dates) for l in ["mandarin","japanese","korean"]}
        month_tot = {l: sum(v.get(l,0) for k,v in progress.items() if k.startswith(month_pref)) for l in ["mandarin","japanese","korean"]}

        sec("📝","Today's Words", today_iso)
        c1,c2,c3,cs = st.columns([2,2,2,1])
        with c1: m = st.number_input("🇨🇳 Mandarin", value=td.get("mandarin",0), min_value=0, step=1, key="lm")
        with c2: j = st.number_input("🇯🇵 Japanese", value=td.get("japanese",0), min_value=0, step=1, key="lj")
        with c3: k = st.number_input("🇰🇷 Korean",   value=td.get("korean",0),   min_value=0, step=1, key="lk")
        with cs:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Save", type="primary", use_container_width=True, key="lsave"):
                progress[today_iso] = {"mandarin":m,"japanese":j,"korean":k}
                save_json("progress.json", progress)
                week_tot  = {l: sum(progress.get(d,{}).get(l,0) for d in week_dates) for l in ["mandarin","japanese","korean"]}
                month_tot = {l: sum(v.get(l,0) for kk,v in progress.items() if kk.startswith(month_pref)) for l in ["mandarin","japanese","korean"]}
                st.success("Saved!")

        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        for col, lang in zip([c1,c2,c3],["mandarin","japanese","korean"]):
            lg = lang_g.get(lang,{})
            colour = lg.get("colour","#C9A84C")
            w_goal = lg.get("weekly_words",1)
            w_val  = week_tot[lang]
            w_pct  = min(100, round(w_val/w_goal*100)) if w_goal else 0
            daily  = progress.get(today_iso,{}).get(lang,0)
            with col:
                st.markdown(f'<div class="card" style="text-align:center;border-color:{colour};"><div style="font-size:0.72rem;font-weight:700;color:{colour};text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">{lg.get("label",lang)}</div>{circle(w_pct,colour,90)}<div style="font-size:0.72rem;color:#6B7280;margin-top:8px;">Weekly Progress</div><div style="margin-top:10px;font-size:0.82rem;color:#C8C8D8;">Today: <b style="color:{colour};">{daily:,}</b> &nbsp;·&nbsp; Week: <b>{w_val:,}</b></div></div>', unsafe_allow_html=True)

        sec("📈","Weekly Progress (last 7 days)")
        for lang in ["mandarin","japanese","korean"]:
            lg = lang_g.get(lang,{})
            prog_bar(week_tot[lang], lg.get("weekly_words",1), lg.get("colour","#C9A84C"), lg.get("label",lang))

        sec("📅","Monthly Progress")
        for lang in ["mandarin","japanese","korean"]:
            lg = lang_g.get(lang,{})
            prog_bar(month_tot[lang], lg.get("monthly_words",1), lg.get("colour","#C9A84C"), lg.get("label",lang))

        sec("🗓️","Recent History (7 days)")
        hist_rows=[]
        for d in week_dates:
            day=progress.get(d,{})
            m_v,j_v,k_v=day.get("mandarin",0),day.get("japanese",0),day.get("korean",0)
            marker=" ← today" if d==today_iso else ""
            hist_rows.append([f"{d}{marker}",f'<span style="color:#C9A84C;">{m_v}</span>',f'<span style="color:#4EA8DE;">{j_v}</span>',f'<span style="color:#3DD68C;">{k_v}</span>',f'<b>{m_v+j_v+k_v}</b>'])
        tbl(["Date","🇨🇳 Mandarin","🇯🇵 Japanese","🇰🇷 Korean","Total"], hist_rows)

    with tab3:
        progress = load_json("progress.json",{})
        lang_g = sched.get("language_goals",{"mandarin":{"label":"Mandarin","colour":"#C9A84C","daily_words":20},"japanese":{"label":"Japanese","colour":"#4EA8DE","daily_words":85},"korean":{"label":"Korean","colour":"#3DD68C","daily_words":529}})

        sec("🗓️","30-Day Streak")
        st.markdown('<div style="font-size:0.78rem;color:#6B7280;margin-bottom:16px;">Each cell = 1 day. Darker = more words logged relative to daily target.</div>', unsafe_allow_html=True)

        for lang in ["mandarin","japanese","korean"]:
            lg = lang_g.get(lang,{})
            colour = lg.get("colour","#C9A84C")
            label  = lg.get("label",lang)
            target = lg.get("daily_words",1)
            st.markdown(f'<div style="font-size:0.78rem;font-weight:700;color:{colour};text-transform:uppercase;letter-spacing:1px;margin:12px 0 6px;">{label}</div>', unsafe_allow_html=True)
            cells=""
            for i in range(29,-1,-1):
                d=(date.today()-timedelta(days=i)).isoformat()
                val=progress.get(d,{}).get(lang,0)
                pct=min(1.0,val/target) if target else 0
                opacity=round(0.12+0.88*pct,2) if val>0 else 0.08
                cells+=f'<div style="display:inline-block;width:20px;height:20px;background:{colour};opacity:{opacity};border-radius:3px;margin:2px;" title="{d}: {val} words"></div>'
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:12px;">{cells}</div>', unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.72rem;color:#6B7280;margin-top:8px;">Opacity indicates % of daily target reached that day.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SYLLABUS — detailed self-knowledge curriculum
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📚  Syllabus":
    page_header("Syllabus","Your complete self-knowledge curriculum — 58 topics across 10 modules")

    syl = load_json("syllabus.json",{})

    MODULES = [
        {"title":"WHO YOU ARE — Identity & Rarity","colour":"#C9A84C","icon":"🌟","topics":[
            ("ENFP-I: The Introverted ENFP — what it means to be socially magnetic but internally private","Self"),
            ("The Rarity Formula: 1 in 2,000–20,000 — why this combination is so unusual","Self"),
            ("ENFP in Finance & ACCA: Why this combination is exceptional and rare","Self"),
            ("The Soft-Strong Duality: Understanding your core paradoxes","Self"),
            ("The Origin Story: What shaped you from childhood to now","Self"),
            ("Late Bloomer to Leader: Social difficulty → University president → Professional confidence","Self"),
        ]},
        {"title":"YOUR COGNITIVE STYLE","colour":"#4EA8DE","icon":"🧠","topics":[
            ("Cognitive Stack: Ne-Fi-Te-Si — how you actually process information","Mind"),
            ("Pattern Recognition (Ne): How your brain maps the world differently","Mind"),
            ("Dopamine-Sensitive / Interest-Based Attention System","Mind"),
            ("Pressure-Activated Performance and Hyperfocus States","Mind"),
            ("Executive Multitasking vs Sensory Multitasking — the contrast explained","Mind"),
            ("How You Learn: Visual quirks, compensation strategies, self-teaching","Mind"),
            ("Decision-Making: Why low-stakes feels harder than high-stakes problems","Mind"),
        ]},
        {"title":"EMOTIONAL INTELLIGENCE","colour":"#9B72CF","icon":"💫","topics":[
            ("The Four Domains of EQ: Self-awareness, regulation, empathy, social skills","EQ"),
            ("Emotional Charisma: Why people feel genuinely seen in your presence","EQ"),
            ("Autonomic Sensitivity: Your body as emotional radar — what it's telling you","EQ"),
            ("Adaptive Extroversion: Switching modes smoothly without losing yourself","EQ"),
            ("Imagination & Immersion: Why stories and content hit you differently","EQ"),
        ]},
        {"title":"SOCIAL IDENTITY","colour":"#3DD68C","icon":"🌿","topics":[
            ("Social Gravity: Why people orbit around you without you trying","Social"),
            ("The Layered Self-Reveal: The 6 phases of how people get to know you","Social"),
            ("First Impression Effect: Why you create instant magnetism","Social"),
            ("Inner-Circle Dynamics: What real belonging actually looks like","Social"),
            ("The Unpredictable Quality: Why your genuine reactions are so rare","Social"),
            ("How You Make People Feel Seen: What you do that most people can't","Social"),
            ("Selective Assertiveness: When you speak up vs when you hold back","Social"),
        ]},
        {"title":"EMOTIONAL PATTERNS & HEALING","colour":"#E94560","icon":"🌑","topics":[
            ("Fawn Response: The 4th trauma response — why you people-please","Healing"),
            ("The Childhood Rules That Still Run: Don't cry, don't disturb, don't burden","Healing"),
            ("Emotional Masking: What you hide vs what you show to the world","Healing"),
            ("Over-Apologising: Why you say sorry even when you were right","Healing"),
            ("Shyness in Public vs Courage When Alone: The observer effect","Healing"),
            ("The Mediator Role: Not your job description — something you took on to survive","Healing"),
            ("Walking Away Cleanly: Your quiet self-respect in action","Healing"),
        ]},
        {"title":"DECISIONS & BOUNDARIES","colour":"#4EA8DE","icon":"🔒","topics":[
            ("Two Good Options Rule: Collapsing any decision to a binary choice","Practical"),
            ("Delay Before Yes: 'Let me check first' — breaking the automatic fawn","Practical"),
            ("Emotional Boundaries Are Not Derhaka: Walking away is not disloyalty","Practical"),
            ("Self-Permission: Learning to choose for yourself without guilt","Practical"),
        ]},
        {"title":"COMMUNICATION WITH T-TYPES","colour":"#3DD68C","icon":"🗣️","topics":[
            ("ESTP Communication: Lead with results, match directness, hold your ground","Comms"),
            ("INTJ Communication: Logic, clarity, confident positions under scrutiny","Comms"),
            ("ISTJ Friendship: Slow trust, consistent quiet presence, earned depth","Comms"),
            ("ENTJ Communication: Decisive, direct, maintain your professional lines","Comms"),
            ("Why T-Types Respond So Well To You: What you give that others don't","Comms"),
        ]},
        {"title":"LOVE & RELATIONSHIPS","colour":"#E94560","icon":"❤️","topics":[
            ("Attraction vs Curiosity: The most important distinction for an ENFP","Love"),
            ("How You Fall: Slow, deep, selective — only twice in 26 years","Love"),
            ("How You Leave: Quietly, cleanly, with self-respect intact","Love"),
            ("What You Need in a Partner: Private, hardworking, emotionally stable, intelligent","Love"),
            ("The Jodoh Framework: Faith-based approach to relationships and timing","Love"),
            ("Kahwin Lambat as Maturity, Not Failure: Why the smile was admiration","Love"),
            ("Your Romantic Pattern: Curiosity is not love — knowing the difference","Love"),
        ]},
        {"title":"PROFESSIONAL GROWTH","colour":"#C9A84C","icon":"💼","topics":[
            ("The Tableau Story: The moment you saw what your brain could really do","Career"),
            ("University Leadership: Proof of executive multitasking under real pressure","Career"),
            ("Career Path: Finance SSC + ACCA — what this combination signals","Career"),
            ("The 4-Track Project System: Automation, Apps, Digital Products, Content","Career"),
            ("Building While Working: How to sustain 4 tracks alongside a full-time role","Career"),
        ]},
        {"title":"LANGUAGES","colour":"#4EA8DE","icon":"🌍","topics":[
            ("Mandarin: HSK 1–9 Pathway — 20 words/day to fluency by Dec 2026","Language"),
            ("Japanese: JLPT N5–N1 Pathway — 85 words/day + 22,570 total words","Language"),
            ("Korean: 74-Hour Course + 142,776 words by Dec 2026","Language"),
            ("Memory Systems for Language Learning: Spaced repetition, grouping, mnemonics","Language"),
            ("Learning Languages with a Pressure-Activated Brain: Working with your nature","Language"),
        ]},
    ]

    CAREER_MODULES = [
        {"title":"MICROSOFT EXCEL & DATA","colour":"#3DD68C","icon":"📊","courses":[
            ("Learn 75+ Excel Formulas for Data Analysis & Business Intelligence","9.5h","Udemy","https://www.udemy.com/share/101Wh83@ssPm32yV8hg3MYyFvZxkGXXU9MKN8I3WoCrKG7nmTiGCoMuieTbRRDbAU-nuVLl-Gg==/"),
            ("Ace the Excel MO-201 Exam — Excel Expert Certification (MS Excel 2019)","8.5h","Udemy","https://www.udemy.com/share/103LoG3@u-ms5D25pVuGAT1BWdUOiC31zqQGiGCtNhbh3vR6APNeltzey3HRkMWWc2GzbUjn8Q==/"),
            ("Microsoft PL-300 — Power BI Desktop Certification","29.5h","Udemy","https://www.udemy.com/share/102yiC3@woaXnTXz_9NDloDGREvOCAWjpJ4wokIPDw-H7bb6IZ7_Fdq-vqh2P7pIPre7AvU1nA==/"),
            ("Learn Google Sheets — Pivot Tables, QUERY & more","14.5h","Udemy","https://www.udemy.com/share/103EEL3@9jBDSbF5jjn16T60g1BFz-uGK_Go7BULNMEdg2Hf1BeyThhEpseO8HrkAOC-ix3Djg==/"),
            ("Microsoft Excel — Excel from Beginner to Advanced","22.0h","Udemy","https://www.udemy.com/share/101Wde3@9ngN7bHzGYEmHqosturZb7NGqLc9EeAIWRPDFwWD_KSOeBQt0JX-fFfbhmOtx40NKg==/"),
            ("Tableau — Full course","21.0h","YouTube","https://youtu.be/K3pXnbniUcM?si=WIrYR-jAs_GyiA78"),
        ]},
        {"title":"CODING & DEVELOPMENT","colour":"#C9A84C","icon":"💻","courses":[
            ("100 Days of Code: The Complete Python Pro Bootcamp","56.5h","Udemy","https://www.udemy.com/share/103IHM3@h1Lnic1TAvK8FK-zfLz8cMamHzWeTk5w8qXDVolEzFgFPU8itCnY-7VAl_GtMnUAWg==/"),
            ("The Complete Full-Stack Web Development Bootcamp","61.5h","Udemy","https://www.udemy.com/share/1013gG3@ptVmdOeBQKS00WxK2Fc1_ZbV8y2TCpPvZRGWzj3Du1TTwU7vEG5WJ0ImcNFBnwFNVg==/"),
            ("Java Development Skills","135.5h","Udemy","https://www.udemy.com/share/101Wdq3@M3xIHlzn7PYrThaAh0Bz0ePsYLOVgzmGQinIf2NsIPhq41edJ3cKifpCHGfQRzuPsw==/"),
            ("SQL — Full course","—","YouTube","https://youtu.be/SSKVgrwhzus?si=ho3dvvQMlTeC4PtL"),
            ("VBA (already self-taught at work)","—","Self-taught",""),
            ("Flutter (mobile development)","—","Planned",""),
            ("Build & Sell with Claude Code (10+ Hour Course)","10h+","YouTube","https://youtu.be/mpALXah_PBg?si=Y8Wu-vUWWrhk5QuA&t=2490"),
        ]},
        {"title":"ANIMATION & CREATIVE","colour":"#9B72CF","icon":"🎨","courses":[
            ("Alex Grigg — Animation course","—","Studio","https://courses.alexgrigg.studio/courses/2414640/lectures/50944661"),
            ("Frame by Frame Ninja","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("The Bing String","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Seoro Oh — Style animation","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Mary Kim — Character animation","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Havtza — Animation technique","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Howard Whimshurt — Getting Started in 2D Animation","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Howard Whimshurt — Mastering 2D Animation","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Yutapon Cube — Motion study","—","Drive","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Domestika — Animated Illustrations","—","Domestika","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Domestika — Dynamic Animation","—","Domestika","https://drive.google.com/drive/folders/14FpXyde70hrVOKLVTorY4e1NZ3_iJsSj?usp=share_link"),
            ("Win Heart with Colour","—","SSD Samsung",""),
        ]},
        {"title":"MONEY & BUSINESS","colour":"#E94560","icon":"💰","courses":[
            ("The Complete Digital Marketing Guide — 27 Courses in 1","86.5h","Udemy","https://www.udemy.com/share/1013fu3@fLeaH5Hsa5En6zvC72p9mwJSgkP8VzhCjTJqAgxccL2S09BroXb_L5dNErgj8ZSl8w==/"),
            ("3-in-1 E-Commerce Masterclass — Amazon, Etsy & Pinterest","48.0h","Udemy","https://www.udemy.com/share/108nLs3@whMmuFi-lJJC0m1DZntdR49iMpeigcvUW2h0rA8sJmZ6fk6b-KulDIwawojkI2GFZA==/"),
            ("Design UI/UX","—","Planned",""),
            ("Build & Sell with Claude Code","10h+","YouTube","https://youtu.be/mpALXah_PBg?si=Y8Wu-vUWWrhk5QuA&t=2490"),
        ]},
        {"title":"CONSULTING & FINANCE","colour":"#4EA8DE","icon":"📋","courses":[
            ("Interview Skills for Consulting","4h","Planned",""),
            ("Consulting Frameworks","5h","Planned",""),
            ("Case Study Practice (447 cases)","447","Planned",""),
            ("Acts/Laws — AAA/ATX/Liquidation","3h","ACCA",""),
            ("Calculation & Industry Knowledge","19h","Planned",""),
        ]},
        {"title":"PIANO","colour":"#C9A84C","icon":"🎹","courses":[
            ("Pianoforall — Incredible New Way To Learn Piano & Keyboard","38.5h","Udemy","https://www.udemy.com/share/101WgS3@tCgJ-70BQWvUleD3W9oIBiMJkgdp7cS1LBsButcdWfcZYAHmw8nRzI3cuQFbQR8GiA==/"),
        ]},
    ]

    total_topics = sum(len(m["topics"]) for m in MODULES)
    done_count = sum(1 for m in MODULES for i,_ in enumerate(m["topics"]) if syl.get(f"{MODULES.index(m)}_{i}",False))

    st.markdown(f'<div style="font-size:0.85rem;color:#6B7280;margin-bottom:8px;">Overall Progress</div>', unsafe_allow_html=True)
    prog_bar(done_count, total_topics, "#C9A84C", f"{done_count}/{total_topics} topics studied")

    st.markdown("<br>", unsafe_allow_html=True)

    for mi, module in enumerate(MODULES):
        colour = module["colour"]
        mod_done = sum(1 for i,_ in enumerate(module["topics"]) if syl.get(f"{mi}_{i}",False))
        mod_total = len(module["topics"])
        with st.expander(f"{module['icon']}  {module['title']}  —  {mod_done}/{mod_total}"):
            prog_bar(mod_done, mod_total, colour, "module progress")
            for ti,(topic,tag) in enumerate(module["topics"]):
                key = f"{mi}_{ti}"
                done = syl.get(key, False)
                col1, col2 = st.columns([0.08, 0.92])
                with col1:
                    checked = st.checkbox("", value=done, key=f"syl_{key}", label_visibility="collapsed")
                with col2:
                    colour_text = colour if checked else "#C8C8D8"
                    st.markdown(f'<div style="color:{colour_text};font-size:0.86rem;padding:4px 0;{"text-decoration:line-through;opacity:0.6;" if checked else ""}">{topic} <span style="font-size:0.72rem;color:#6B7280;margin-left:4px;">[{tag}]</span></div>', unsafe_allow_html=True)
                if checked != done:
                    syl[key] = checked
                    save_json("syllabus.json", syl)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    sec("💼", "Career & Skills Curriculum")
    for module in CAREER_MODULES:
        colour = module["colour"]
        with st.expander(f"{module['icon']}  {module['title']}"):
            for course_name, hours, source, url in module["courses"]:
                link_html = f'<a href="{url}" target="_blank" style="background:rgba(78,168,222,0.1);color:#4EA8DE;border:1px solid rgba(78,168,222,0.25);padding:3px 10px;border-radius:5px;font-size:0.68rem;font-weight:700;text-decoration:none;white-space:nowrap;margin-left:8px;">🔗 Open</a>' if url else ""
                st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid #1A1A2E;flex-wrap:wrap;gap:4px;"><div style="font-size:0.85rem;color:#C8C8D8;flex:1;">{course_name}{link_html}</div><div style="display:flex;gap:10px;align-items:center;"><span style="font-size:0.72rem;color:#6B7280;">{hours}</span><span style="font-size:0.65rem;background:rgba(107,114,128,0.15);color:#9CA3AF;padding:1px 7px;border-radius:8px;">{source}</span></div></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# GLOW UP
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✨  Glow Up":
    page_header("Glow Up", "Clothing · Exercise · Self-development · Makeup · Body Goal")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["👗  Clothing", "🏃  Exercise", "🌱  Self-Dev", "💄  Makeup", "🎯  Body Goal", "🗓️  Routine"])

    with tab1:
        sec("👗", "Clothing & Style Resources")
        CLOTHING = [
            ("Well Dress Playlist — curated style videos",                         "https://youtu.be/c3SniNakUhc"),
            ("How to Dress for Your Body Type — in literally 6 min",               "https://youtu.be/0mFAJVetuSI"),
            ("Dear Peachie Cloth Playlist — colour, makeup, style",                "https://youtu.be/F1_dJFCUaH4"),
            ("How to Find High Quality Clothes — Dos and Don'ts",                  "https://youtu.be/iVV9ED8LENY"),
            ("FRUMPY instead of POLISHED — what makes the difference",             "https://youtu.be/jxhN2NqbuWg"),
            ("You Don't Need a New Wardrobe. You Need a New Mindset",              "https://youtu.be/1zn4QOtd43A"),
            ("How to Identify Quality in Clothing (A Rant)",                       "https://youtu.be/fuVU64m1sbw"),
        ]
        for title, url in CLOTHING:
            st.markdown(f'<div class="row-item" style="background:#12121F;border:1px solid #252538;border-radius:8px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;"><span style="font-size:0.86rem;color:#C8C8D8;">{title}</span><a href="{url}" target="_blank" style="background:rgba(201,168,76,0.12);color:#C9A84C;border:1px solid rgba(201,168,76,0.3);padding:4px 12px;border-radius:6px;font-size:0.74rem;font-weight:700;text-decoration:none;white-space:nowrap;margin-left:10px;">▶ Watch</a></div>', unsafe_allow_html=True)
        hl("<b style='color:#C9A84C;'>Your style identity:</b> Timeless · Old money · Quiet luxury · Petite-friendly silhouettes")

    with tab2:
        sec("🏃", "Exercise & Body Sculpt")
        EXVIDS = [
            ("The Real Way To Shrink Your Waist & Train Your Core", "Core / Waist",     "https://youtu.be/J5mHsWOckuU"),
            ("5 Healthy Habits",                                     "Wellness",          "https://youtu.be/e_W5guIMc9Y"),
            ("Removing 10KG of Fat in 12 WEEKS",                    "Fat loss",          "https://youtu.be/IBvJ_BRsymI"),
            ("How to Hip Thrust with Dumbbell",                      "Glutes",            "https://youtube.com/shorts/mC56j1VdFfA"),
            ("Full Upper Body Workout (Tone & Sculpt) — 15 min",     "Upper body",        "https://youtu.be/0zhvUV1bAVQ"),
            ("How To Fix Body Asymmetry | 5 Minutes Every Day",      "Body symmetry",     "https://youtu.be/tX3eueEFCM8"),
            ("How To Fix Jaw & Face Asymmetry FOREVER",              "Face symmetry",     "https://youtu.be/60OKCe8vHjY"),
            ("Posture — Fix it properly",                            "Posture",           "https://youtu.be/j-Av4Zk3Uuk"),
            ("Calisthenic Beginner + Progress",                      "Calisthenics",      "https://youtu.be/GTlLGkHbSkA"),
            ("Pilates for Beginners",                                "Pilates / Core",    "https://youtu.be/C2HX2pNbUCM"),
            ("Wellness Habits That Will Transform Your Life",        "Lifestyle",         "https://youtu.be/Svvfnu8YU7U"),
        ]
        for i, (title, focus, url) in enumerate(EXVIDS):
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:8px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;gap:10px;"><div><span style="font-size:0.72rem;color:#6B7280;margin-right:8px;">{i+1}</span><span style="font-size:0.86rem;color:#C8C8D8;">{title}</span><span style="font-size:0.7rem;background:rgba(61,214,140,0.1);color:#3DD68C;padding:1px 7px;border-radius:8px;margin-left:8px;">{focus}</span></div><a href="{url}" target="_blank" style="background:rgba(61,214,140,0.12);color:#3DD68C;border:1px solid rgba(61,214,140,0.3);padding:4px 12px;border-radius:6px;font-size:0.74rem;font-weight:700;text-decoration:none;white-space:nowrap;">▶ Watch</a></div>', unsafe_allow_html=True)

    with tab3:
        sec("🌱", "Self-Development")
        SELFDEV = [
            ("EXIT LAZY ERA & become PRODUCTIVE",            "https://youtu.be/JBlvSq5KGhY"),
            ("Having an Exceptional Memory is Actually Easy","https://youtu.be/CqeR-JraiDI"),
        ]
        for title, url in SELFDEV:
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:8px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;"><span style="font-size:0.86rem;color:#C8C8D8;">{title}</span><a href="{url}" target="_blank" style="background:rgba(155,114,207,0.12);color:#9B72CF;border:1px solid rgba(155,114,207,0.3);padding:4px 12px;border-radius:6px;font-size:0.74rem;font-weight:700;text-decoration:none;white-space:nowrap;margin-left:10px;">▶ Watch</a></div>', unsafe_allow_html=True)

    with tab4:
        sec("💄", "Makeup")
        MAKEUP = [
            ("How to Make Your Face Look SLIMMER — Makeup, Hair and Outfit Tips","https://youtu.be/eF2WbmhfaEw"),
        ]
        for title, url in MAKEUP:
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:8px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;"><span style="font-size:0.86rem;color:#C8C8D8;">{title}</span><a href="{url}" target="_blank" style="background:rgba(233,69,96,0.12);color:#E94560;border:1px solid rgba(233,69,96,0.3);padding:4px 12px;border-radius:6px;font-size:0.74rem;font-weight:700;text-decoration:none;white-space:nowrap;margin-left:10px;">▶ Watch</a></div>', unsafe_allow_html=True)

    with tab5:
        TDEE = 1550
        sec("🎯", "Body Goal Check-In")
        hl(f"<b style='color:#C9A84C;'>TDEE:</b> ~{TDEE} kcal/day &nbsp;·&nbsp; <b style='color:#3DD68C;'>Deficit target:</b> 1,200–1,400 kcal to lose ~0.3–0.5 kg/week")

        body_log = load_json("body_goal.json", [])
        today_iso = date.today().isoformat()

        sec("➕", "Log Today")
        with st.form("body_log_form"):
            col1, col2 = st.columns(2)
            with col1:
                breakfast = st.text_input("Breakfast", placeholder="What did you have?")
                lunch = st.text_input("Lunch", placeholder="What did you have?")
            with col2:
                dinner = st.text_input("Dinner", placeholder="What did you have?")
                snacks = st.text_input("Snacks / Drinks", placeholder="Taufufa, fruits, air kosong...")
            est_kcal = st.number_input("Estimated Total (kcal)", min_value=0, max_value=5000, step=50, value=0)
            weight_today = st.number_input("Weight today (kg) — optional", min_value=0.0, max_value=200.0, step=0.1, value=0.0)
            notes_body = st.text_input("Notes", placeholder="How you feel, energy, anything notable")
            submitted_body = st.form_submit_button("Save", type="primary")
            if submitted_body:
                body_log.insert(0, {
                    "date": today_iso,
                    "breakfast": breakfast.strip(),
                    "lunch": lunch.strip(),
                    "dinner": dinner.strip(),
                    "snacks": snacks.strip(),
                    "kcal": est_kcal,
                    "weight": weight_today if weight_today > 0 else None,
                    "notes": notes_body.strip(),
                })
                save_json("body_goal.json", body_log)
                st.success("Logged!")
                st.rerun()

        if body_log:
            sec("📋", f"Recent Entries ({min(14, len(body_log))} shown)")
            for entry in body_log[:14]:
                kcal = entry.get("kcal", 0)
                deficit = TDEE - kcal if kcal > 0 else None
                def_col = "#3DD68C" if deficit and deficit > 0 else "#E94560"
                wt_str = f'· {entry["weight"]} kg' if entry.get("weight") else ""
                def_str = f'{deficit:+,} kcal deficit' if deficit is not None else "no kcal logged"
                with st.expander(f"{entry['date']}  —  {kcal if kcal else '—'} kcal  {wt_str}"):
                    tbl(["Meal", "What you had"], [
                        ["Breakfast", entry.get("breakfast") or "—"],
                        ["Lunch", entry.get("lunch") or "—"],
                        ["Dinner", entry.get("dinner") or "—"],
                        ["Snacks / Drinks", entry.get("snacks") or "—"],
                    ])
                    st.markdown(f'<div style="font-size:0.82rem;margin-top:8px;color:{def_col};">{def_str}</div>', unsafe_allow_html=True)
                    if entry.get("notes"):
                        st.markdown(f'<div style="font-size:0.82rem;color:#6B7280;margin-top:4px;">{entry["notes"]}</div>', unsafe_allow_html=True)

    with tab6:
        page_header("Glow Up Routine", "Daily & weekly beauty care with products")

        def _routine_block(title, colour, daily_items, weekly_items, weekly_label="Saturday"):
            st.markdown(f'<div style="font-size:0.78rem;font-weight:700;color:{colour};text-transform:uppercase;letter-spacing:1px;margin:16px 0 8px;">{title}</div>', unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            with r1:
                html = f'<div style="background:#12121F;border:1px solid #252538;border-top:3px solid {colour};border-radius:10px;padding:14px 16px;"><div style="font-size:0.65rem;color:{colour};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Daily</div>'
                for item in daily_items:
                    html += f'<div style="font-size:0.84rem;color:#C8C8D8;padding:5px 0;border-bottom:1px solid #1A1A2E;">• {item}</div>'
                st.markdown(html + '</div>', unsafe_allow_html=True)
            with r2:
                html2 = f'<div style="background:#12121F;border:1px solid #252538;border-top:3px solid {colour};border-radius:10px;padding:14px 16px;"><div style="font-size:0.65rem;color:{colour};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">{weekly_label}</div>'
                for item in weekly_items:
                    html2 += f'<div style="font-size:0.84rem;color:#C8C8D8;padding:5px 0;border-bottom:1px solid #1A1A2E;">• {item}</div>'
                st.markdown(html2 + '</div>', unsafe_allow_html=True)

        sec("😁", "Teeth")
        _routine_block(
            "Teeth Care", "#C9A84C",
            daily_items=["Brush teeth (morning + night)", "Floss or water flosser"],
            weekly_items=["Waterfloss (thorough)", "Oral-B string floss — all gaps", "Tongue scraper"],
            weekly_label="Saturday Deep Clean"
        )

        sec("💇", "Hair")
        _routine_block(
            "Hair Care", "#4EA8DE",
            daily_items=[
                "Shiseido Sublimic Aqua Intensive OS (leave-in / heat protect)",
                "UNOVE Treatment EX — apply mid-length to ends before styling",
                "Kérastase Elixir Ultime — 1–2 drops on dry ends",
                "Brush gently, avoid over-washing",
            ],
            weekly_items=[
                "Selsun Blue shampoo — apply to scalp, leave 5 min before rinsing",
                "Tsubaki Premium EX Mask — apply after shampoo, leave 5 min",
                "Deep condition + scalp massage",
                "Air-dry where possible",
            ],
            weekly_label="Saturday Deep Care"
        )

        sec("🧴", "Body")
        _routine_block(
            "Body Care", "#3DD68C",
            daily_items=[
                "Shower — wash properly, focus on dark areas",
                "Dr Ko 336 lotion — apply after shower to dark/problem areas",
                "Moisturize full body",
                "Deodorant + fragrance (Delina Lychee)",
            ],
            weekly_items=[
                "FRESHOP scrub — exfoliate full body (focus: arms, legs, underarm, bikini)",
                "IPL session — underarm, legs, bikini line",
                "Friday night: shave before IPL on Saturday",
                "Dr Ko 336 — extra application on treated areas after IPL",
            ],
            weekly_label="Saturday (+ Shave Friday)"
        )

        sec("🗓️", "Weekly Schedule")
        WEEKLY_SCHEDULE = [
            ("Monday",    "#C9A84C", ["Brush + floss", "Hair serum", "Body lotion", "Morning skincare", "Evening skincare"]),
            ("Tuesday",   "#4EA8DE", ["Brush + floss", "Hair serum", "Body lotion", "Skincare routine"]),
            ("Wednesday", "#9B72CF", ["Brush + floss", "Hair serum", "Body lotion", "Skincare routine"]),
            ("Thursday",  "#3DD68C", ["Brush + floss", "Hair serum", "Body lotion", "Skincare routine"]),
            ("Friday",    "#E94560", ["Brush + floss", "Hair serum", "Body lotion", "Skincare routine", "🪒 Shave (prep for Saturday IPL)"]),
            ("Saturday",  "#C9A84C", ["Selsun Blue shampoo → Tsubaki EX Mask", "Waterfloss + Oral-B string floss", "FRESHOP body scrub", "IPL — underarm, legs, bikini", "Dr Ko 336 on treated areas", "Full skincare + Gua sha", "Kérastase Elixir Ultime on ends"]),
            ("Sunday",    "#6B7280", ["Rest — light routine only", "Moisturise + hydrate", "Face mask if needed"]),
        ]
        day_cols = st.columns(7)
        for col, (day, col_hex, items) in zip(day_cols, WEEKLY_SCHEDULE):
            is_today = day == today_name
            border = f"border-top:3px solid {col_hex};" if is_today else "border-top:1px solid #252538;"
            html = f'<div style="background:{"rgba(201,168,76,0.06)" if is_today else "#12121F"};border:1px solid #252538;{border}border-radius:8px;padding:10px 8px;"><div style="font-size:0.65rem;font-weight:700;color:{col_hex};text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">{day[:3]}</div>'
            for item in items:
                html += f'<div style="font-size:0.68rem;color:#C8C8D8;padding:3px 0;border-bottom:1px solid #1A1A2E;line-height:1.4;">• {item}</div>'
            col.markdown(html + '</div>', unsafe_allow_html=True)

        sec("🌿", "Face & Skincare")
        hl("<b style='color:#C9A84C;'>Daily:</b> Cleanse → toner → serum → moisturiser → SPF (morning) &nbsp;·&nbsp; <b style='color:#4EA8DE;'>Weekly:</b> Gua sha massage, sheet mask, Vitamin C serum boost &nbsp;·&nbsp; <b style='color:#E94560;'>IPL:</b> Every Saturday on clear skin (shaved the night before)")


# ═══════════════════════════════════════════════════════════════════════════════
# GOALS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🎯  Goals":
    page_header("Goals","Life vision · Career · Personal growth · Financial · Health")

    if goals.get("life_vision"):
        st.markdown(f'<div class="hero" style="padding:24px 28px;margin-bottom:20px;"><div class="hero-badge">Life Vision</div><div style="font-size:1rem;color:#E2E2E2;line-height:1.8;">{goals["life_vision"]}</div></div>', unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    goal_sections=[("This Year",goals.get("this_year_goals",[]),"gold","#C9A84C"),("Career",goals.get("career_goals",[]),"blue","#4EA8DE"),("Personal Growth",goals.get("personal_growth_goals",[]),"purple","#9B72CF"),("Financial",goals.get("financial_goals",[]),"green","#3DD68C"),("Health",goals.get("health_goals",[]),"red","#E94560")]
    for i,(title,items,variant,colour) in enumerate(goal_sections):
        if items:
            with (c1 if i%2==0 else c2):
                sec("▸",title)
                st.markdown(f'<div class="card {variant}">'+"".join([f'<div class="row-item">{it}</div>' for it in items])+'</div>', unsafe_allow_html=True)

    sec("⚡","Current Emotional State")
    hl(feel.get("current_emotional_state",""))

    c1,c2 = st.columns(2)
    with c1:
        sec("💚","What Helps When You're Down")
        rows(feel.get("things_that_help_when_down",[]))
    with c2:
        sec("⭐","What You're Proud Of")
        proud=feel.get("things_i_am_currently_proud_of",[])
        html='<div style="background:#0D1F14;border:1px solid rgba(61,214,140,0.2);border-radius:10px;padding:10px 16px;">'
        html+="".join([f'<div class="row-item" style="color:#3DD68C;">✓ &nbsp;{it}</div>' for it in proud])
        st.markdown(html+'</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DAILY TRACKER — checklist + mood + weekly review + project log
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✅  Daily Tracker":
    page_header("Daily Tracker", date.today().strftime("%A, %d %B %Y"))

    tab1, tab2, tab3, tab4 = st.tabs(["📊  Today's Summary", "😊  Mood", "📖  Daily Review", "💼  Project Log"])

    with tab1:
        progress  = load_json("progress.json", {})
        today_iso = date.today().isoformat()
        td2       = progress.get(today_iso, {})
        sdkh      = load_json("sedekah.json", {})
        mood_d    = load_json("mood.json", {})
        today_mood2 = mood_d.get(today_iso, 0)
        week_dates2 = [(date.today()-timedelta(days=i)).isoformat() for i in range(6,-1,-1)]
        month_pref2 = date.today().strftime("%Y-%m")

        # Solat
        on_period_dt = td2.get("on_period", False)

        sec("🕌", "Solat 5 Waktu")
        SOLAT2 = [("Subuh","🌅"),("Zuhur","☀️"),("Asar","🌤️"),("Maghrib","🌆"),("Isyak","🌙")]
        solat_done2 = td2.get("solat", [])
        if on_period_dt:
            st.markdown('<div style="background:rgba(233,69,96,0.08);border:1px solid rgba(233,69,96,0.25);border-radius:10px;padding:12px 16px;font-size:0.84rem;color:#E94560;font-weight:700;margin-bottom:6px;">🌸 On period — Prayer paused</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.78rem;color:#6B7280;line-height:1.6;margin-bottom:8px;">Focus on dhikr, selawat, istighfar, and dua. Allah knows your effort. 🤍</div>', unsafe_allow_html=True)
        else:
            sol_cols = st.columns(5)
            for col, (name, emoji) in zip(sol_cols, SOLAT2):
                done = name in solat_done2
                col.markdown(f'<div style="text-align:center;background:{"rgba(61,214,140,0.12)" if done else "#12121F"};border:1px solid {"rgba(61,214,140,0.4)" if done else "#252538"};border-radius:10px;padding:14px 6px;"><div style="font-size:1.3rem;">{emoji}</div><div style="font-size:0.72rem;color:{"#3DD68C" if done else "#6B7280"};font-weight:700;margin-top:5px;">{name}</div><div style="font-size:0.9rem;margin-top:3px;">{"✓" if done else "—"}</div></div>', unsafe_allow_html=True)

        # Sunat
        sec("✨", "Sunat & Spiritual Practice")
        SUNAT2 = [("🌙","Tahajud",True),("🌤️","Dhuha",True),("🕌","12 Solat Sunat",True),("📖","Read Quran",True),("🎧","Tazkirah / Tadabbur",False),("📔","Reflection",False)]
        sunat_done2  = td2.get("sunat", [])
        sn_cols2 = st.columns(6)
        for col, (emoji, name, restricted) in zip(sn_cols2, SUNAT2):
            if on_period_dt and restricted:
                col.markdown(f'<div style="text-align:center;opacity:0.38;background:#12121F;border:1px solid rgba(233,69,96,0.2);border-radius:10px;padding:12px 4px;"><div style="font-size:1.1rem;">{emoji}</div><div style="font-size:0.65rem;color:#E94560;font-weight:600;margin-top:4px;line-height:1.3;">🌸 Haid</div></div>', unsafe_allow_html=True)
            else:
                done = name in sunat_done2
                col.markdown(f'<div style="text-align:center;background:{"rgba(61,214,140,0.08)" if done else "#12121F"};border:1px solid {"rgba(61,214,140,0.25)" if done else "#252538"};border-radius:10px;padding:12px 4px;"><div style="font-size:1.1rem;">{emoji}</div><div style="font-size:0.65rem;color:{"#3DD68C" if done else "#6B7280"};font-weight:600;margin-top:4px;line-height:1.3;">{name}</div><div style="font-size:0.8rem;margin-top:3px;">{"✓" if done else "—"}</div></div>', unsafe_allow_html=True)

        # Languages
        sec("🌍", "Language Words Today")
        LANG_DT = {"mandarin":("🇨🇳 Mandarin","#C9A84C",20),"japanese":("🇯🇵 Japanese","#4EA8DE",85),"korean":("🇰🇷 Korean","#3DD68C",529)}
        lc_cols = st.columns(3)
        for col, (lang, (label, colour, daily_t)) in zip(lc_cols, LANG_DT.items()):
            logged = td2.get(lang, 0)
            pct = min(100, round(logged/daily_t*100)) if daily_t else 0
            done_c = "#3DD68C" if logged >= daily_t else colour
            col.markdown(f'<div style="text-align:center;background:#12121F;border:1px solid #252538;border-radius:10px;padding:16px 8px;"><div style="font-size:0.72rem;color:{colour};font-weight:700;margin-bottom:6px;">{label}</div><div style="font-size:1.6rem;font-weight:900;color:{done_c};">{logged}</div><div style="font-size:0.65rem;color:#6B7280;">/ {daily_t} target</div><div class="pb-wrap" style="margin-top:8px;"><div class="pb-fill" style="width:{pct}%;background:{colour};"></div></div></div>', unsafe_allow_html=True)

        # Sedekah + Exercise + Mood
        st.markdown("<br>", unsafe_allow_html=True)
        bot_cols = st.columns(3)
        with bot_cols[0]:
            sed_today = sdkh.get(today_iso)
            sed_str = f"RM {sed_today:.2f}" if sed_today is not None else "—"
            sed_c = "#3DD68C" if sed_today is not None else "#6B7280"
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:16px;text-align:center;"><div style="font-size:0.65rem;color:{sed_c};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">💚 Sedekah</div><div style="font-size:1.5rem;font-weight:800;color:{sed_c};">{sed_str}</div></div>', unsafe_allow_html=True)
        with bot_cols[1]:
            ex_done2 = td2.get("exercise_done", False)
            ex_c = "#3DD68C" if ex_done2 else "#6B7280"
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:16px;text-align:center;"><div style="font-size:0.65rem;color:{ex_c};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">🏋️ Exercise</div><div style="font-size:1.5rem;font-weight:800;color:{ex_c};">{"Done ✓" if ex_done2 else "—"}</div></div>', unsafe_allow_html=True)
        with bot_cols[2]:
            mood_c2 = MOOD_COL.get(today_mood2, "#6B7280")
            st.markdown(f'<div style="background:#12121F;border:1px solid #252538;border-radius:10px;padding:16px;text-align:center;"><div style="font-size:0.65rem;color:{mood_c2};font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">😊 Mood</div><div style="font-size:1.5rem;font-weight:800;color:{mood_c2};">{MOOD_MAP.get(today_mood2,"—")}</div></div>', unsafe_allow_html=True)

        # This week overview table
        sec("📆", "This Week")
        wrows2 = []
        for d in week_dates2:
            dp = progress.get(d, {})
            sol  = len(dp.get("solat", []))
            sn   = len(dp.get("sunat", []))
            lang = dp.get("mandarin", 0) + dp.get("japanese", 0) + dp.get("korean", 0)
            sed  = sdkh.get(d)
            sed_s = f"RM {sed:.2f}" if sed is not None else "—"
            ml = mood_d.get(d, 0)
            mc = MOOD_COL.get(ml, "#6B7280")
            wrows2.append([
                d,
                f'<span style="color:{"#3DD68C" if sol==5 else "#C9A84C" if sol>0 else "#6B7280"};">{sol}/5</span>',
                f'<span style="color:{"#3DD68C" if sn>=4 else "#C9A84C" if sn>0 else "#6B7280"};">{sn}/6</span>',
                f'<span style="color:#4EA8DE;">{lang:,}</span>',
                f'<span style="color:#3DD68C;">{sed_s}</span>',
                f'<span style="color:{mc};">{MOOD_MAP.get(ml,"—")}</span>',
            ])
        tbl(["Date","Prayer","Sunnah","Words","Sedekah","Mood"], wrows2)

    with tab2:
        mood_data = load_json("mood.json", {})
        today_iso = date.today().isoformat()
        today_mood = mood_data.get(today_iso, 0)

        sec("😊", "How are you feeling today?")
        st.markdown(f'<div style="font-size:0.85rem;color:#6B7280;margin-bottom:12px;">Current: <b style="color:{MOOD_COL.get(today_mood,"#6B7280")};">{MOOD_MAP.get(today_mood,"Not logged yet")}</b></div>', unsafe_allow_html=True)
        mood_cols = st.columns(5)
        for i, (lvl, lbl) in enumerate(MOOD_MAP.items()):
            with mood_cols[i]:
                if st.button(lbl, key=f"tmood_{lvl}", type="primary" if today_mood==lvl else "secondary", use_container_width=True):
                    mood_data[today_iso] = lvl
                    save_json("mood.json", mood_data); st.rerun()

        sec("📅", "Mood This Week")
        week_dates = [(date.today()-timedelta(days=i)).isoformat() for i in range(6,-1,-1)]
        mrows = []
        for d in week_dates:
            lvl = mood_data.get(d, 0)
            lbl = MOOD_MAP.get(lvl, "—")
            col = MOOD_COL.get(lvl, "#6B7280")
            mrows.append([d, f'<span style="color:{col};">{lbl}</span>'])
        tbl(["Date","Mood"], mrows)

    with tab3:
        from collections import defaultdict
        reviews  = load_json("reviews.json", [])
        today_iso = date.today().isoformat()
        today_rv  = next((r for r in reviews if r.get("date") == today_iso), None)

        sec("📖", "Daily Review", today_iso)
        with st.form("daily_review_form"):
            highlight = st.text_area("Highlight of today", placeholder="What happened? What stood out?", height=90, value=today_rv.get("highlight","") if today_rv else "")
            grateful  = st.text_area("3 things I'm grateful for", placeholder="Big or small — write them.", height=90, value=today_rv.get("grateful","") if today_rv else "")
            tomorrow  = st.text_area("One thing I want to do differently tomorrow", placeholder="An intention, not a judgment.", height=70, value=today_rv.get("tomorrow","") if today_rv else "")
            if st.form_submit_button("Save Review ✓", type="primary", use_container_width=True):
                if highlight.strip() or grateful.strip():
                    entry = {"date": today_iso, "highlight": highlight.strip(), "grateful": grateful.strip(), "tomorrow": tomorrow.strip()}
                    reviews = [r for r in reviews if r.get("date") != today_iso]
                    reviews.insert(0, entry)
                    save_json("reviews.json", reviews)
                    st.success("Saved ✓"); st.rerun()

        if reviews:
            # build download
            lines = []
            for rv in sorted(reviews, key=lambda r: r["date"]):
                lines.append(f"## {rv['date']}")
                if rv.get("highlight"):  lines.append(f"**Highlight:** {rv['highlight']}\n")
                if rv.get("wins"):       lines.append(f"**Highlight:** {rv['wins']}\n")
                if rv.get("grateful"):   lines.append(f"**Grateful:** {rv['grateful']}\n")
                if rv.get("gratitude"):  lines.append(f"**Grateful:** {rv['gratitude']}\n")
                if rv.get("tomorrow"):   lines.append(f"**Tomorrow:** {rv['tomorrow']}\n")
                if rv.get("lessons"):    lines.append(f"**Tomorrow:** {rv['lessons']}\n")
                lines.append("")
            st.download_button("📥 Download all reviews (.md)", data="\n".join(lines), file_name="daily_reviews.md", mime="text/markdown", use_container_width=True)

            # group by week
            earliest = min(date.fromisoformat(r["date"]) for r in reviews)
            grouped  = defaultdict(list)
            for rv in reviews:
                d = date.fromisoformat(rv["date"])
                wk = ((d - earliest).days // 7) + 1
                grouped[wk].append(rv)

            sec("📂", f"All Reviews — {len(reviews)} entries")
            for wk in sorted(grouped.keys(), reverse=True):
                entries = grouped[wk]
                label   = f"Week {wk}  ·  {entries[-1]['date']} → {entries[0]['date']}  ({len(entries)} entries)"
                with st.expander(label, expanded=(wk == max(grouped.keys()))):
                    for rv in entries:
                        st.markdown(f'<div style="font-size:0.72rem;color:#C9A84C;font-weight:700;border-bottom:1px solid #1A1A2E;padding-bottom:4px;margin:12px 0 8px;">{rv["date"]}</div>', unsafe_allow_html=True)
                        for field, label_text, colour in [
                            ("highlight","Highlight","#3DD68C"),
                            ("wins","Highlight","#3DD68C"),
                            ("grateful","Grateful For","#4EA8DE"),
                            ("gratitude","Grateful For","#4EA8DE"),
                            ("tomorrow","Tomorrow","#9B72CF"),
                            ("lessons","Tomorrow","#9B72CF"),
                        ]:
                            if rv.get(field):
                                st.markdown(f'<div style="font-size:0.68rem;color:{colour};font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px;">{label_text}</div><div style="font-size:0.84rem;color:#C8C8D8;white-space:pre-wrap;margin-bottom:10px;">{rv[field]}</div>', unsafe_allow_html=True)

    with tab4:
        project_log = load_json("project_log.json", [])
        today_iso   = date.today().isoformat()
        rot_col_map = {"Automation":"#C9A84C","Apps / SaaS":"#4EA8DE","Digital Products":"#9B72CF","Content":"#3DD68C","Rest":"#6B7280"}
        rot_col     = rot_col_map.get(today_rotation, "#C9A84C")

        sec("💼", "Project Log")
        st.markdown(f'<div style="font-size:0.85rem;margin-bottom:12px;">Today\'s focus: <b style="color:{rot_col};">{today_name} — {today_rotation}</b></div>', unsafe_allow_html=True)
        log_note = st.text_area("What did you work on today?", placeholder="Brief note about your session — what you built, learned, or progressed on.", height=100, key="proj_note")
        if st.button("Log It", type="primary", key="proj_save"):
            if log_note.strip():
                project_log.insert(0, {"date": today_iso, "type": today_rotation, "note": log_note.strip()})
                save_json("project_log.json", project_log)
                st.success("Logged!"); st.rerun()

        if project_log:
            sec("📋", f"Recent Sessions ({len(project_log[:20])} shown)")
            for entry in project_log[:20]:
                col = rot_col_map.get(entry.get("type",""), "#6B7280")
                st.markdown(f'<div style="background:#12121F;border-left:3px solid {col};border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;"><div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:0.72rem;font-weight:700;color:{col};text-transform:uppercase;">{entry.get("type","")}</span><span style="font-size:0.72rem;color:#6B7280;">{entry.get("date","")}</span></div><div style="font-size:0.85rem;color:#C8C8D8;">{entry.get("note","")}</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NEWSLETTER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📰  Newsletter":
    today_d     = date.today()
    this_monday = today_d - timedelta(days=today_d.weekday())
    this_friday = this_monday + timedelta(days=4)
    iso_week    = today_d.isocalendar()[1]

    page_header("Newsletter", f"Week {iso_week}  ·  {this_monday.strftime('%d %b')} – {this_friday.strftime('%d %b %Y')}")

    _sync_col1, _sync_col2 = st.columns([3, 1])
    with _sync_col2:
        if st.button("🔄 Refresh", use_container_width=True, key="nl_sync"):
            load_newsletter.clear()
            st.rerun()

    # Day → section mapping
    NL_DAY_MAP = {
        0: ("s1", "🛠️", "Section 1", "Project of the Week · Automation"),
        1: ("s3", "🚀", "Section 3", "SaaS / Apps"),
        2: ("s3", "🚀", "Section 3", "SaaS / Apps"),
        3: ("s2", "📦", "Section 2", "Digital Products"),
        4: ("s4", "⚡", "Section 4", "Quick Wins · Content"),
    }
    today_nl = NL_DAY_MAP.get(today_d.weekday())

    news = load_newsletter()

    # Freshness indicator
    mtime = news.get("_mtime") if news else None
    if mtime:
        is_fresh  = mtime >= this_monday
        fr_col    = "#3DD68C" if is_fresh else "#C9A84C"
        fr_icon   = "✅" if is_fresh else "⚠️"
        fr_text   = "Updated this week" if is_fresh else f"Last updated {mtime.strftime('%d %b %Y')} — new issue may be ready on Monday"
        st.markdown(f'<div style="font-size:0.75rem;color:{fr_col};margin-bottom:16px;font-weight:600;">{fr_icon} {fr_text}</div>', unsafe_allow_html=True)

    # Today's focus banner
    if today_nl:
        t_key, t_emoji, t_sec, t_desc = today_nl
        st.markdown(f'<div style="background:linear-gradient(135deg,#12121F,#1A1230);border:1px solid rgba(201,168,76,0.3);border-left:4px solid #C9A84C;border-radius:12px;padding:18px 22px;margin-bottom:24px;"><div style="font-size:0.65rem;color:#C9A84C;font-weight:700;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">Today\'s Focus — {today_d.strftime("%A")}</div><div style="font-size:1.3rem;font-weight:900;color:white;">{t_emoji} {t_sec}</div><div style="font-size:0.88rem;color:#6B7280;margin-top:4px;">{t_desc}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hl" style="text-align:center;font-size:0.9rem;">🌿 Weekend — rest, review, and reset. Come back Monday for the new issue.</div>', unsafe_allow_html=True)

    if not news:
        st.markdown('<div class="hl">Newsletter draft not found at <code>Newsletter/.tmp/draft.md</code>. Generate it first.</div>', unsafe_allow_html=True)
    else:
        # Section definitions: (key, emoji, title, day_label, accent_colour)
        NL_SECTIONS = [
            ("s1", "🛠️", "Section 1 — Project of the Week",  "Monday · Automation",    "#C9A84C"),
            ("s2", "📦", "Section 2 — Digital Products",      "Thursday",               "#9B72CF"),
            ("s3", "🚀", "Section 3 — SaaS / Apps",           "Tuesday & Wednesday",    "#4EA8DE"),
            ("s4", "⚡", "Section 4 — Quick Wins",             "Friday · Content",       "#3DD68C"),
        ]
        for key, emoji, title, day_lbl, colour in NL_SECTIONS:
            is_today_sec = bool(today_nl and today_nl[0] == key)
            content      = news.get(key, [])
            content_clean = []
            for l in content:
                content_clean.append(l)
            while content_clean and not content_clean[0].strip():
                content_clean.pop(0)
            words  = sum(len(l.split()) for l in content_clean if l.strip() and l != "```")
            mins   = max(1, round(words / 200))
            badge  = "  ← Today" if is_today_sec else ""
            with st.expander(f"{emoji} {title}{badge}", expanded=is_today_sec):
                meta_cols = st.columns([1, 1])
                with meta_cols[0]:
                    st.markdown(f'<span class="badge {("gold" if colour=="#C9A84C" else "blue" if colour=="#4EA8DE" else "purple" if colour=="#9B72CF" else "green")}">{day_lbl}</span>', unsafe_allow_html=True)
                with meta_cols[1]:
                    st.markdown(f'<div style="font-size:0.7rem;color:#6B7280;text-align:right;">~{words} words · {mins} min read</div>', unsafe_allow_html=True)
                if is_today_sec:
                    st.markdown(f'<div style="display:inline-block;background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.3);color:{colour};font-size:0.7rem;font-weight:700;padding:3px 12px;border-radius:20px;margin:10px 0;">👈 This is your focus today</div>', unsafe_allow_html=True)
                st.divider()
                if content_clean:
                    st.markdown("\n".join(content_clean))
                else:
                    st.markdown('<div style="color:#6B7280;font-size:0.84rem;font-style:italic;">No content parsed for this section.</div>', unsafe_allow_html=True)




# ═══════════════════════════════════════════════════════════════════════════════
# MINDSET
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💡  Mindset":
    page_header("Mindset", "Manager mode · Reset mantras · Don't Believe Everything You Think")

    sec("👔", "Your Manager Voice")
    st.markdown('<div class="mantra-box" style="font-size:1.05rem;padding:20px 22px;margin-bottom:12px;">Head down. Earn. Learn. Grow. Love is not on the calendar this year.</div>', unsafe_allow_html=True)
    card("""<div style="font-size:0.88rem;color:#C8C8D8;line-height:1.9;">
    Your commitment for this chapter of life:<br>
    <b style="color:#C9A84C;">Languages. Money. Body. Faith. Projects.</b> — in that order, every single day.<br><br>
    Someone being kind to you is <b style="color:white;">not</b> a sign. Gentlemanly behaviour is courtesy, not destiny.
    A good joke is entertainment, not connection. Admiration is not love.<br><br>
    You have goals that most people will never attempt. You don't have time to be confused about what kindness means.
    </div>""", "blue")

    sec("🛡️", "Reset Mantra — When Someone Is Nice to You")
    hl("""<b style="color:#4EA8DE; font-size:1.05rem;">"Kindness is a gesture, not a bond. My path is mine."</b><br>
    <span style="font-size:0.82rem;color:#6B7280;">Pause → Label it ("this is appreciation, not love") → Redirect to your goals → Move on.</span>""")

    c1, c2 = st.columns(2)
    with c1:
        card("""<div style="font-size:0.78rem;color:#4EA8DE;font-weight:700;text-transform:uppercase;margin-bottom:8px;">What's Actually Happening</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        Someone holds the door → courtesy<br>
        Someone is funny → entertainment<br>
        Someone is attentive → their default mode<br>
        Someone is helpful → professionalism<br>
        Kindness from anyone → appreciate it, file it, move on
        </div>""","blue")
    with c2:
        card("""<div style="font-size:0.78rem;color:#C9A84C;font-weight:700;text-transform:uppercase;margin-bottom:8px;">What Love Actually Looks Like</div>
        <div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;">
        Slow. Deep. Rare — only twice in 26 years.<br>
        Falls for people who are private, hardworking,<br>
        emotionally stable, selective, intelligent.<br>
        Not triggered by a gesture — built over time.<br>
        You will know the difference when it is real.
        </div>""")

    sec("📚", "Don't Believe Everything You Think", "Key lessons — Joseph Nguyen")
    lessons = [
        ("Thinking is the root of suffering",
         "Pain is inevitable. Suffering is the story we attach to pain. The PAUSE technique breaks the cycle: Stop → Breathe → Observe the thought without engaging it."),
        ("Reality vs perception of reality",
         "The Buddha's boat story: if an empty boat drifts and hits yours, you feel nothing. If someone is in it, you get angry. The reality is the same — the collision happened. Your thinking changed everything. Thinking is not reality. It is your perception of reality."),
        ("Thought vs thinking",
         "A thought is a noun — it appears. Thinking is a verb — you engage with it. You can notice a thought without becoming it. The moment you step back and observe, you break the loop."),
        ("Let go — don't fight your thinking",
         "Fighting thoughts gives them energy. Tawakal is the Islamic equivalent: do your part fully, then release the outcome to Allah. Good things still come. You don't have to think them into existence."),
        ("Mushin — the Japanese concept of no-mind",
         "Athletes train until the body acts without thought. Thinking during performance slows everything down. In your case: you've studied, you've prepared, you've built. Now trust your body and brain to perform. Stop second-guessing mid-action."),
        ("Inspiration goals vs desperation goals",
         "Desperation goal: I have to do this or something bad happens → feels heavy, draining. Inspiration goal: I want this because it excites me → feels energetic, natural. Build your goals from excitement, not fear. Do them with unconditional love — not because you need the result, but because the process itself is the reward."),
        ("You already know what to do",
         "Your intuition knows. The overthinking is noise layered on top of the signal. Trust your gut more than your spiral. You've made good decisions before by just acting. Do that more."),
        ("Study your triggers",
         "List what environments, habits, or people cause your thinking to spiral. Systematically reduce exposure to them. This is not avoidance — it is intelligent design of your own nervous system."),
    ]
    for title, body in lessons:
        with st.expander(f"→ {title}"):
            st.markdown(f'<div style="font-size:0.87rem;color:#C8C8D8;line-height:1.85;padding:4px 0;">{body}</div>', unsafe_allow_html=True)

    sec("💬", "Your Trigger Audit")
    hl("""<b style="color:#C9A84C;">Things that trigger unnecessary thinking for you:</b><br>
    Chaos at home · Being blamed for things you didn't cause · Having me-time interrupted · Long silences in conversations · Feeling like a burden · Not knowing if someone is upset with you<br><br>
    <b style="color:#3DD68C;">What helps:</b> Earphones + drama/vlogs · Alone time · Writing it out · Remembering jodoh — you can't force timing · Moving your body
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# MY NOTES
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝  My Notes":
    page_header("My Notes","Paste analysis, observations, anything you want saved")

    notes = load_json("notes.json",[])

    sec("➕","Add New Note")
    title_in = st.text_input("Title", placeholder="What is this about?", label_visibility="collapsed")
    st.markdown('<div style="font-size:0.72rem;color:#6B7280;margin-bottom:4px;">TITLE</div>', unsafe_allow_html=True)
    content_in = st.text_area("Content", placeholder="Paste analysis, Copilot conversations, observations — anything you want stored.", height=180, label_visibility="collapsed")
    st.markdown('<div style="font-size:0.72rem;color:#6B7280;margin-bottom:4px;">CONTENT</div>', unsafe_allow_html=True)

    if st.button("Save Note", type="primary"):
        if content_in.strip():
            notes.insert(0,{"id":datetime.now().isoformat(),"title":title_in.strip() or f"Note {len(notes)+1}","content":content_in.strip(),"date":date.today().isoformat()})
            save_json("notes.json",notes)
            st.success("Saved!")
            st.rerun()

    if notes:
        sec("📂",f"Saved Notes ({len(notes)})")
        for note in notes:
            with st.expander(f"{note['title']}  —  {note['date']}"):
                st.markdown(f'<div class="note-body">{note["content"]}</div>', unsafe_allow_html=True)
                if st.button("🗑️ Delete", key=f"del_{note['id']}"):
                    notes=[n for n in notes if n["id"]!=note["id"]]
                    save_json("notes.json",notes)
                    st.rerun()
