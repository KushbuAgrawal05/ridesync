"""
RideSync. AI-powered carpooling demo built in Streamlit.

End-to-end demo flow:
  1. Home  -> hero, empathy quotes, feature triptych, quick search
  2. Find a ride -> AI-ranked matches with compatibility scoring + booking
  3. Verify ID -> upload card, see extracted fields, confirm, get verified badge
  4. My trips -> upcoming + completed rides with statuses
  5. Safety center -> trust layers, SOS demo, emergency contacts
  6. Eco tracker -> CO2/fuel/money KPIs, monthly goal, city leaderboard

Design thinking (EDIPT) is baked in silently:
  Empathize  -> home opens with 3 real user-pain quotes before any pitch
  Define     -> each feature card names the specific problem it solves first
  Ideate     -> Smart Match scores compatibility across signals, not just route
  Prototype  -> this app itself
  Test       -> every interactive surface has a clear success/empty state
"""

from datetime import datetime, timedelta

import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="RideSync. Commute smarter, together.",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "verified": False,
        "matches_found": True,
        "booked_rides": [],
        "sos_triggered": False,
        "emergency_contacts": [
            {"name": "Mom", "phone": "+91 98765 43210"},
            {"name": "Roommate Aditi", "phone": "+91 98765 11111"},
        ],
        "search_from": "Hinjewadi Phase 1",
        "search_to": "Baner, Pune",
        "search_seats": 2,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ---------------------------------------------------------------------------
# Global styles. Editorial light theme. Deep teal as primary.
# ---------------------------------------------------------------------------
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,800&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --bg: #F7F4EE;
  --bg-warm: #F1ECE2;
  --surface: #FFFFFF;
  --surface-2: #FBF8F2;
  --ink: #0E1B26;
  --ink-soft: #3D4D5C;
  --ink-mute: #6B7A89;
  --line: #E5DFD2;
  --line-strong: #D4CDBE;
  --teal: #0F4C5C;
  --teal-deep: #062E38;
  --teal-soft: #E6EEF0;
  --teal-tint: #C7DCE0;
  --gold: #C77D3F;
  --rose: #C5614F;
  --success: #2E7D5B;
  --shadow-sm: 0 1px 2px rgba(14,27,38,0.04);
  --shadow-md: 0 8px 24px rgba(14,27,38,0.06);
  --shadow-lg: 0 20px 50px rgba(14,27,38,0.08);
}

html, body, [class*="css"] {
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--ink);
}

.stApp {
  background:
    radial-gradient(900px 500px at 95% -5%, rgba(15,76,92,0.06), transparent 60%),
    radial-gradient(700px 400px at -5% 30%, rgba(199,125,63,0.05), transparent 60%),
    var(--bg);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

.block-container {
  padding-top: 2rem;
  max-width: 1280px;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
  gap: 2px;
  background: var(--surface);
  padding: 5px;
  border-radius: 12px;
  border: 1px solid var(--line);
  box-shadow: var(--shadow-sm);
}
.stTabs [data-baseweb="tab"] {
  background: transparent;
  border-radius: 9px;
  padding: 9px 16px;
  color: var(--ink-soft);
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.1px;
}
.stTabs [aria-selected="true"] {
  background: var(--teal) !important;
  color: #FFFFFF !important;
}

/* ---------- Buttons ---------- */
.stButton > button {
  background: var(--teal);
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  padding: 11px 20px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  letter-spacing: 0.1px;
  transition: transform 0.15s ease, box-shadow 0.2s ease, background 0.15s ease;
  box-shadow: 0 4px 14px rgba(15,76,92,0.18);
}
.stButton > button:hover {
  transform: translateY(-1px);
  background: var(--teal-deep);
  color: #FFFFFF;
  box-shadow: 0 8px 22px rgba(15,76,92,0.28);
}
.stButton > button:focus {
  background: var(--teal);
  color: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(15,76,92,0.2);
}

/* Secondary button variant (use kind="secondary") */
.stButton > button[kind="secondary"] {
  background: var(--surface);
  color: var(--ink);
  border: 1px solid var(--line);
  box-shadow: none;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--surface-2);
  border-color: var(--line-strong);
  color: var(--ink);
}

/* ---------- Inputs ---------- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stTimeInput > div > div > input {
  background: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
  font-family: 'Inter', sans-serif !important;
  padding: 10px 14px !important;
}
.stSelectbox > div > div {
  background: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--teal) !important;
  box-shadow: 0 0 0 3px rgba(15,76,92,0.1) !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stDateInput label, .stTimeInput label, .stRadio label,
.stFileUploader label, .stTextArea label {
  color: var(--ink-soft) !important;
  font-weight: 600 !important;
  font-size: 12.5px !important;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
.stTextArea textarea {
  background: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploader"] section {
  background: var(--surface);
  border: 1.5px dashed var(--line-strong);
  border-radius: 12px;
  padding: 18px;
}
[data-testid="stFileUploader"] section:hover {
  border-color: var(--teal);
  background: var(--teal-soft);
}
[data-testid="stFileUploader"] button {
  background: var(--surface) !important;
  color: var(--teal) !important;
  border: 1px solid var(--line) !important;
  border-radius: 8px !important;
}

/* ---------- Brand ---------- */
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Fraunces', serif;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.6px;
  color: var(--ink);
  margin-bottom: 24px;
}
.brand-mark {
  width: 42px; height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--teal), var(--teal-deep));
  display: flex; align-items: center; justify-content: center;
  color: #FFFFFF;
  font-family: 'Fraunces', serif;
  font-weight: 700;
  font-size: 20px;
  box-shadow: 0 6px 16px rgba(15,76,92,0.25);
  font-style: italic;
}
.brand-tag {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--ink-mute);
  margin-left: 6px;
  padding: 4px 9px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--surface);
}

/* ---------- Hero ---------- */
.hero {
  position: relative;
  padding: 64px 56px 56px;
  border-radius: 24px;
  background:
    radial-gradient(500px 240px at 92% 10%, rgba(15,76,92,0.10), transparent 60%),
    linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
  border: 1px solid var(--line);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  margin-bottom: 32px;
}
.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(14,27,38,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(14,27,38,0.025) 1px, transparent 1px);
  background-size: 36px 36px;
  pointer-events: none;
  mask-image: radial-gradient(ellipse at top right, black 25%, transparent 70%);
}
.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  background: var(--teal-soft);
  border: 1px solid var(--teal-tint);
  border-radius: 999px;
  color: var(--teal);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  position: relative;
  z-index: 2;
}
.hero h1 {
  font-family: 'Fraunces', serif;
  font-size: 68px;
  font-weight: 500;
  line-height: 1.02;
  letter-spacing: -2.5px;
  margin: 22px 0 18px;
  color: var(--ink);
  position: relative;
  z-index: 2;
}
.hero h1 em {
  font-style: italic;
  font-weight: 400;
  color: var(--teal);
}
.hero p.lede {
  font-size: 18px;
  line-height: 1.55;
  color: var(--ink-soft);
  max-width: 580px;
  position: relative;
  z-index: 2;
  margin-bottom: 28px;
  font-weight: 400;
}
.stat-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  position: relative;
  z-index: 2;
}
.stat-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 16px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 999px;
  color: var(--ink);
  font-size: 13px;
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}
.stat-chip .dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--teal);
  box-shadow: 0 0 8px rgba(15,76,92,0.5);
  animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.55; transform: scale(1.4); }
}

/* ---------- Section headings ---------- */
.section-title {
  font-family: 'Fraunces', serif;
  font-size: 34px;
  font-weight: 500;
  letter-spacing: -1px;
  color: var(--ink);
  margin: 12px 0 6px;
}
.section-title em { font-style: italic; color: var(--teal); font-weight: 400; }
.section-sub {
  color: var(--ink-mute);
  font-size: 14px;
  margin-bottom: 22px;
  max-width: 640px;
  line-height: 1.55;
}
.eyebrow {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--teal);
  margin-bottom: 4px;
}

/* ---------- Cards ---------- */
.card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}
.card-title {
  font-family: 'Fraunces', serif;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.4px;
  color: var(--ink);
  margin-bottom: 4px;
}

/* ---------- Empathy quotes ---------- */
.empathy {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 8px 0 32px;
}
.empathy .item {
  padding: 22px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 14px;
  position: relative;
  box-shadow: var(--shadow-sm);
}
.empathy .item::before {
  content: "\\201C";
  position: absolute;
  top: -8px;
  left: 16px;
  font-family: 'Fraunces', serif;
  font-size: 56px;
  color: var(--teal);
  line-height: 1;
  opacity: 0.4;
}
.empathy .item .q {
  font-family: 'Fraunces', serif;
  font-style: italic;
  font-size: 17px;
  line-height: 1.4;
  color: var(--ink);
  margin-bottom: 12px;
  font-weight: 500;
}
.empathy .item .a {
  font-size: 11px;
  color: var(--ink-mute);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

/* ---------- Feature triptych ---------- */
.feature-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 28px;
  height: 100%;
  position: relative;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}
.feature-card .icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  background: var(--teal-soft);
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  margin-bottom: 18px;
}
.feature-card h3 {
  font-family: 'Fraunces', serif;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.4px;
  margin: 0 0 10px;
  color: var(--ink);
}
.feature-card p {
  font-size: 14px;
  color: var(--ink-soft);
  line-height: 1.6;
  margin: 0;
}

/* ---------- Match cards ---------- */
.match-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 22px;
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}
.match-card:hover {
  border-color: var(--teal-tint);
  box-shadow: var(--shadow-md);
}
.match-head { display: flex; align-items: center; gap: 14px; }
.avatar {
  width: 52px; height: 52px;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--teal), var(--teal-deep));
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; color: #FFFFFF; font-size: 17px;
  font-family: 'Fraunces', serif;
  position: relative;
}
.avatar.verified::after {
  content: "✓";
  position: absolute;
  width: 18px; height: 18px;
  background: var(--success);
  border-radius: 50%;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  bottom: -3px;
  right: -3px;
  border: 2px solid var(--surface);
}
.match-name { font-size: 16px; font-weight: 700; color: var(--ink); }
.match-sub { font-size: 12px; color: var(--ink-mute); margin-top: 2px; }
.match-score { margin-left: auto; text-align: right; }
.match-score .num {
  font-family: 'Fraunces', serif;
  font-size: 32px;
  font-weight: 600;
  color: var(--teal);
  line-height: 1;
}
.match-score .label {
  font-size: 10px;
  color: var(--ink-mute);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 700;
  margin-top: 4px;
}
.route-row {
  display: flex; gap: 12px; align-items: center;
  padding: 12px 16px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  border-radius: 12px;
}
.route-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--teal); }
.route-dot.end { background: var(--gold); }
.route-line { flex: 1; height: 1px; background: var(--line-strong); border-top: 1px dashed var(--line-strong); background: transparent; }
.route-text { font-size: 13px; color: var(--ink); font-weight: 600; }
.match-meta {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 12px;
}
.match-meta .tags { display: flex; gap: 6px; flex-wrap: wrap; }
.match-meta .price-block {
  display: flex; align-items: center; gap: 16px;
}
.price-block .time-label { font-size: 11px; color: var(--ink-mute); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }
.price-block .time-val { font-size: 14px; font-weight: 700; color: var(--ink); }
.price-block .fare {
  font-family: 'Fraunces', serif;
  font-size: 26px;
  font-weight: 600;
  color: var(--teal);
}

/* ---------- Tags ---------- */
.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  border-radius: 999px;
  font-size: 11px;
  color: var(--ink-soft);
  font-weight: 600;
}
.tag.teal { color: var(--teal); border-color: var(--teal-tint); background: var(--teal-soft); }
.tag.gold { color: var(--gold); border-color: rgba(199,125,63,0.3); background: rgba(199,125,63,0.08); }
.tag.success { color: var(--success); border-color: rgba(46,125,91,0.3); background: rgba(46,125,91,0.08); }

/* ---------- KPI ---------- */
.kpi {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 22px;
  box-shadow: var(--shadow-sm);
}
.kpi .label {
  font-size: 11px;
  color: var(--ink-mute);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 700;
}
.kpi .value {
  font-family: 'Fraunces', serif;
  font-size: 40px;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.1;
  margin-top: 8px;
  letter-spacing: -1px;
}
.kpi .value .unit { font-size: 18px; color: var(--ink-mute); margin-left: 4px; font-weight: 400; }
.kpi .delta { font-size: 12px; color: var(--success); font-weight: 600; margin-top: 6px; }
.kpi .delta.down { color: var(--rose); }

/* ---------- ID extraction fields ---------- */
.id-field {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 16px;
  background: var(--surface-2);
  border-radius: 10px;
  margin-bottom: 8px;
  border: 1px solid var(--line);
}
.id-field .k {
  font-size: 11px; color: var(--ink-mute);
  font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px;
}
.id-field .v {
  font-size: 14px; color: var(--ink); font-weight: 600;
  display: flex; align-items: center; gap: 8px;
}
.id-field.ok { border-color: rgba(46,125,91,0.3); background: rgba(46,125,91,0.04); }
.id-field .check {
  color: var(--success); font-weight: 800; font-size: 14px;
  width: 18px; height: 18px; border-radius: 50%;
  background: rgba(46,125,91,0.15);
  display: inline-flex; align-items: center; justify-content: center;
}

/* ---------- Verify result banner ---------- */
.verify-result {
  padding: 22px 26px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(46,125,91,0.10), rgba(46,125,91,0.03));
  border: 1px solid rgba(46,125,91,0.3);
  display: flex; align-items: center; gap: 16px;
}
.verify-result .ico { font-size: 32px; }
.verify-result .title { font-size: 17px; font-weight: 700; color: var(--ink); }
.verify-result .sub { font-size: 13px; color: var(--ink-soft); margin-top: 4px; line-height: 1.5; }

/* ---------- Eco bar ---------- */
.eco-bar {
  height: 12px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  border-radius: 999px;
  overflow: hidden;
  margin: 10px 0 6px;
}
.eco-bar > div {
  height: 100%;
  background: linear-gradient(90deg, var(--teal), var(--teal-deep));
  border-radius: 999px;
}

/* ---------- Safety rows ---------- */
.safety-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 18px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  margin-bottom: 10px;
  box-shadow: var(--shadow-sm);
}
.safety-row .left { display: flex; align-items: center; gap: 14px; }
.safety-row .ico {
  width: 40px; height: 40px; border-radius: 11px;
  background: var(--teal-soft);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.safety-row .label { font-size: 14px; font-weight: 700; color: var(--ink); }
.safety-row .desc { font-size: 12.5px; color: var(--ink-mute); margin-top: 3px; line-height: 1.4; }

/* ---------- SOS banner ---------- */
.sos-active {
  background: linear-gradient(135deg, rgba(197,97,79,0.12), rgba(197,97,79,0.04));
  border: 1px solid rgba(197,97,79,0.4);
  padding: 22px 26px;
  border-radius: 16px;
  display: flex; align-items: center; gap: 16px;
}
.sos-active .ico { font-size: 32px; animation: shake 0.5s infinite; }
@keyframes shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-8deg); }
  75% { transform: rotate(8deg); }
}

/* ---------- Trip rows ---------- */
.trip-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 22px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 14px;
  margin-bottom: 10px;
  box-shadow: var(--shadow-sm);
}
.trip-row .info { display: flex; flex-direction: column; gap: 4px; }
.trip-row .route { font-family: 'Fraunces', serif; font-size: 17px; font-weight: 600; color: var(--ink); letter-spacing: -0.2px; }
.trip-row .meta { font-size: 12px; color: var(--ink-mute); font-weight: 500; }
.trip-row .right { display: flex; align-items: center; gap: 14px; }
.status-pill {
  font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.8px;
  padding: 5px 11px; border-radius: 999px;
}
.status-pill.upcoming { background: var(--teal-soft); color: var(--teal); }
.status-pill.completed { background: rgba(46,125,91,0.1); color: var(--success); }
.status-pill.cancelled { background: rgba(197,97,79,0.1); color: var(--rose); }

/* ---------- Leaderboard ---------- */
.leader-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px;
  border-radius: 12px;
  margin-bottom: 8px;
}

/* ---------- Divider ---------- */
.divider {
  height: 1px;
  background: var(--line);
  margin: 36px 0;
}

/* ---------- Toast / success messages ---------- */
.toast-success {
  background: rgba(46,125,91,0.08);
  border: 1px solid rgba(46,125,91,0.3);
  color: var(--ink);
  padding: 14px 18px;
  border-radius: 12px;
  margin-bottom: 14px;
  display: flex; align-items: center; gap: 12px;
  font-size: 14px;
  font-weight: 600;
}

@media (max-width: 900px) {
  .hero { padding: 36px 28px; }
  .hero h1 { font-size: 44px; letter-spacing: -1.5px; }
  .empathy { grid-template-columns: 1fr; }
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Brand header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="brand">
      <div class="brand-mark">R</div>
      RideSync
      <span class="brand-tag">Beta</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Top tabs
# ---------------------------------------------------------------------------
tab_home, tab_find, tab_verify, tab_trips, tab_safety, tab_eco = st.tabs(
    ["Home", "Find a ride", "Verify ID", "My trips", "Safety", "Eco tracker"]
)

# ===========================================================================
# HOME
# ===========================================================================
with tab_home:
    verified_badge = ""
    if st.session_state.verified:
        verified_badge = '<div class="stat-chip"><span style="color:var(--success);">✓</span> Identity verified</div>'

    st.markdown(
        f"""
        <div class="hero">
          <span class="hero-pill">✦ AI-powered carpooling</span>
          <h1>Commute smarter,<br/><em>together.</em></h1>
          <p class="lede">RideSync matches you with verified co-travellers on your exact route.
          Save money, cut traffic, and lower your carbon footprint without changing how you live.</p>
          <div class="stat-row">
            <div class="stat-chip"><span class="dot"></span> 247 rides active now</div>
            <div class="stat-chip">🌿 1.2 tonnes CO₂ saved today</div>
            <div class="stat-chip">★ 4.8 average rating</div>
            {verified_badge}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Empathy quotes (Empathize phase)
    st.markdown('<div class="eyebrow">Why we built this</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">The commute is broken. <em>We listened.</em></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="empathy">
          <div class="item">
            <div class="q">My fuel costs are killing me, but Ola surge pricing is even worse during rains.</div>
            <div class="a">Anjali, IT corridor commuter</div>
          </div>
          <div class="item">
            <div class="q">I have an empty car going the same way every morning. Feels like such a waste.</div>
            <div class="a">Vikram, Hinjewadi to Baner</div>
          </div>
          <div class="item">
            <div class="q">I would carpool, but I just don't trust riding with random strangers.</div>
            <div class="a">Kushbu, Symbiosis student</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick search
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Quick ride search</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:var(--ink-mute);font-size:13px;margin-bottom:18px;">'
        "Find a ride or offer seats on your route.</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns([3, 3, 1.2, 1.6])
    with c1:
        st.session_state.search_from = st.text_input("From", value=st.session_state.search_from, key="home_from")
    with c2:
        st.session_state.search_to = st.text_input("To", value=st.session_state.search_to, key="home_to")
    with c3:
        st.session_state.search_seats = st.selectbox("Seats", [1, 2, 3, 4],
                                                      index=[1, 2, 3, 4].index(st.session_state.search_seats),
                                                      key="home_seats")
    with c4:
        st.write("")
        st.write("")
        if st.button("Search rides", use_container_width=True, key="home_search_btn"):
            st.session_state.matches_found = True
            st.success("Showing matches in the Find a ride tab. Click the tab above.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Feature triptych (Define + Ideate phases)
    st.markdown('<div class="eyebrow">What makes us different</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Three things our users <em>actually</em> care about.</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            """
            <div class="feature-card">
              <div class="icon">🧠</div>
              <h3>Smart Match</h3>
              <p>Our model scores compatibility on route overlap, schedule, music taste,
              chat preference, and rating history. No more awkward 40-minute rides.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            """
            <div class="feature-card">
              <div class="icon">🪪</div>
              <h3>Verified-only network</h3>
              <p>Every rider scans a government or institutional ID. We extract, verify,
              and match the details before they ever appear in a search result.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            """
            <div class="feature-card">
              <div class="icon">🌿</div>
              <h3>Eco Tracker</h3>
              <p>See your real CO₂ savings, fuel cost avoided, and money saved per trip.
              Compete on a city leaderboard with other green commuters.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ===========================================================================
# FIND A RIDE
# ===========================================================================
with tab_find:
    st.markdown('<div class="eyebrow">Smart Match</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Find your <em>ride.</em></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-sub">AI-ranked matches on your route, sorted by compatibility score. '
        "Verified profiles only.</div>",
        unsafe_allow_html=True,
    )

    fc1, fc2, fc3, fc4 = st.columns([2, 2, 1.3, 1.2])
    with fc1:
        from_loc = st.text_input("From", value=st.session_state.search_from, key="find_from")
    with fc2:
        to_loc = st.text_input("To", value=st.session_state.search_to, key="find_to")
    with fc3:
        depart = st.time_input("Depart by", value=datetime.now().time(), key="find_time")
    with fc4:
        seats = st.selectbox("Seats", [1, 2, 3], key="find_seats")

    fb1, fb2 = st.columns([1, 5])
    with fb1:
        if st.button("Find matches", key="btn_find_matches", use_container_width=True):
            st.session_state.matches_found = True

    if st.session_state.matches_found:
        st.markdown("<br/>", unsafe_allow_html=True)

        matches = [
            {"id": "m1", "name": "Aarav K.", "initials": "AK", "trips": 142, "rating": 4.9,
             "score": 96, "time": "8:45 AM", "fare": 85,
             "tags": [("Verified", "success"), ("Quiet ride", ""), ("Same office", "teal")]},
            {"id": "m2", "name": "Priya S.", "initials": "PS", "trips": 78, "rating": 4.8,
             "score": 91, "time": "9:00 AM", "fare": 80,
             "tags": [("Verified", "success"), ("Music OK", ""), ("Female riders only", "gold")]},
            {"id": "m3", "name": "Rohan M.", "initials": "RM", "trips": 211, "rating": 4.7,
             "score": 84, "time": "8:30 AM", "fare": 90,
             "tags": [("Verified", "success"), ("AC car", ""), ("Pet-friendly", "")]},
        ]

        for i, m in enumerate(matches):
            booked = m["id"] in [b["id"] for b in st.session_state.booked_rides]
            tags_html = "".join(
                f'<span class="tag {cls}">{label}</span>' for label, cls in m["tags"]
            )
            st.markdown(
                f"""
                <div class="match-card">
                  <div class="match-head">
                    <div class="avatar verified">{m['initials']}</div>
                    <div>
                      <div class="match-name">{m['name']}</div>
                      <div class="match-sub">{m['trips']} trips · ★ {m['rating']}</div>
                    </div>
                    <div class="match-score">
                      <div class="num">{m['score']}</div>
                      <div class="label">Match score</div>
                    </div>
                  </div>
                  <div class="route-row">
                    <div class="route-dot"></div>
                    <div class="route-text">{from_loc}</div>
                    <div class="route-line"></div>
                    <div class="route-dot end"></div>
                    <div class="route-text">{to_loc}</div>
                  </div>
                  <div class="match-meta">
                    <div class="tags">{tags_html}</div>
                    <div class="price-block">
                      <div>
                        <div class="time-label">Departs</div>
                        <div class="time-val">{m['time']}</div>
                      </div>
                      <div class="fare">₹{m['fare']}</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            bcol1, bcol2, _ = st.columns([1.2, 1.2, 4])
            with bcol1:
                if booked:
                    st.markdown(
                        '<div class="toast-success" style="margin-bottom:18px;">'
                        '<span style="color:var(--success);">✓</span> Booked. See My trips.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    if st.button(f"Book this ride", key=f"book_{m['id']}", use_container_width=True):
                        st.session_state.booked_rides.append({
                            "id": m["id"],
                            "name": m["name"],
                            "from": from_loc,
                            "to": to_loc,
                            "time": m["time"],
                            "fare": m["fare"],
                            "status": "upcoming",
                        })
                        st.rerun()

# ===========================================================================
# VERIFY ID
# ===========================================================================
with tab_verify:
    st.markdown('<div class="eyebrow">Trust layer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Verify your <em>identity.</em></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-sub">Upload a government or institutional ID. We extract details with OCR, '
        "cross-check against your profile, and approve trusted users only. Production uses AWS Textract; "
        "this demo shows extracted fields directly.</div>",
        unsafe_allow_html=True,
    )

    vc1, vc2 = st.columns([1, 1.15])

    with vc1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Step 1 · Upload your ID</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="color:var(--ink-mute);font-size:13px;margin-bottom:14px;">'
            "Drop a clear image of your student or government ID.</div>",
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "ID image",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
            key="id_upload",
        )
        if uploaded is not None:
            st.image(uploaded, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with vc2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Step 2 · Confirm extracted details</div>', unsafe_allow_html=True)

        if uploaded is None:
            st.markdown(
                '<div style="padding:36px 0;text-align:center;color:var(--ink-mute);font-size:13px;">'
                "Drop your ID on the left. Our OCR pipeline will extract the fields below.</div>",
                unsafe_allow_html=True,
            )
        else:
            extracted = {
                "Full name": "Kushbu Niraj Agrawal",
                "Institution": "Symbiosis Institute of Technology",
                "Course": "B.Tech. CS",
                "PRN / ID number": "23070122267",
                "Date of birth": "05 Oct 2004",
                "Validity": "June 2027",
                "Blood group": "O+",
                "Mobile": "7709458333",
            }
            for k, v in extracted.items():
                st.markdown(
                    f'<div class="id-field ok"><span class="k">{k}</span>'
                    f'<span class="v">{v} <span class="check">✓</span></span></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

            ok1, ok2 = st.columns([1, 1])
            with ok1:
                if st.button("Confirm and verify", key="confirm_verify", use_container_width=True):
                    st.session_state.verified = True
                    st.rerun()
            with ok2:
                st.button("Edit details", key="edit_details", use_container_width=True, type="secondary")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.verified:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="verify-result">
              <div class="ico">🎉</div>
              <div>
                <div class="title">Identity verified</div>
                <div class="sub">You now have a verified badge. Drivers and riders prefer matching with verified profiles, and your match score will improve.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ===========================================================================
# MY TRIPS
# ===========================================================================
with tab_trips:
    st.markdown('<div class="eyebrow">Your journey</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">My <em>trips.</em></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Upcoming and completed rides, all in one place.</div>',
        unsafe_allow_html=True,
    )

    upcoming = [t for t in st.session_state.booked_rides if t["status"] == "upcoming"]

    completed_demo = [
        {"name": "Sneha P.", "from": "Hinjewadi Phase 1", "to": "Baner, Pune",
         "time": "Mon, 8:30 AM", "fare": 80, "status": "completed"},
        {"name": "Karthik V.", "from": "Aundh", "to": "Hinjewadi Phase 1",
         "time": "Fri, 7:15 PM", "fare": 95, "status": "completed"},
        {"name": "Meera J.", "from": "Wakad", "to": "FC Road",
         "time": "Wed, 9:00 AM", "fare": 110, "status": "completed"},
    ]

    st.markdown('<div class="card-title" style="margin-bottom:14px;">Upcoming</div>', unsafe_allow_html=True)
    if upcoming:
        for t in upcoming:
            st.markdown(
                f"""
                <div class="trip-row">
                  <div class="info">
                    <div class="route">{t['from']} → {t['to']}</div>
                    <div class="meta">With {t['name']} · {t['time']} · ₹{t['fare']}</div>
                  </div>
                  <div class="right">
                    <span class="status-pill upcoming">Upcoming</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="card" style="text-align:center;padding:36px;">'
            '<div style="color:var(--ink-mute);font-size:14px;">No upcoming trips. '
            "Book one from the Find a ride tab.</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="margin-bottom:14px;">Completed</div>', unsafe_allow_html=True)
    for t in completed_demo:
        st.markdown(
            f"""
            <div class="trip-row">
              <div class="info">
                <div class="route">{t['from']} → {t['to']}</div>
                <div class="meta">With {t['name']} · {t['time']} · ₹{t['fare']}</div>
              </div>
              <div class="right">
                <span class="status-pill completed">Completed</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ===========================================================================
# SAFETY CENTER
# ===========================================================================
with tab_safety:
    st.markdown('<div class="eyebrow">Peace of mind</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Safety <em>center.</em></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Every protection layer between you and a stranger\'s car.</div>',
        unsafe_allow_html=True,
    )

    sc1, sc2 = st.columns([1.4, 1])

    with sc1:
        safety_items = [
            ("🪪", "ID verification", "Government or institutional ID required for every user."),
            ("📍", "Live trip tracking", "Share your live location with up to 5 emergency contacts."),
            ("🚨", "SOS button", "One-tap alert to local police, your contacts, and our 24/7 ops team."),
            ("🎙️", "Trip audio recording", "Optional encrypted recording, accessible only on incident report."),
            ("⭐", "Two-way ratings", "Riders rate drivers and drivers rate riders. Below 4.0 means review."),
            ("👮", "Background checks", "Driving licence, vehicle RC, and insurance verified at signup."),
        ]
        for ico, label, desc in safety_items:
            st.markdown(
                f"""
                <div class="safety-row">
                  <div class="left">
                    <div class="ico">{ico}</div>
                    <div>
                      <div class="label">{label}</div>
                      <div class="desc">{desc}</div>
                    </div>
                  </div>
                  <span class="tag success">Active</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with sc2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">SOS demo</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="color:var(--ink-mute);font-size:13px;margin-bottom:16px;">'
            "Try the panic button. In production this triggers police, your contacts, and ops.</div>",
            unsafe_allow_html=True,
        )
        if not st.session_state.sos_triggered:
            if st.button("🚨 Trigger SOS", key="sos_trigger", use_container_width=True):
                st.session_state.sos_triggered = True
                st.rerun()
        else:
            st.markdown(
                """
                <div class="sos-active">
                  <div class="ico">🚨</div>
                  <div>
                    <div class="title" style="font-weight:700;font-size:15px;color:var(--ink);">SOS active</div>
                    <div class="sub" style="font-size:12.5px;color:var(--ink-soft);margin-top:4px;">
                      Local police notified. Your 2 emergency contacts have been pinged with live location.
                      Ops team standing by.
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Cancel SOS", key="sos_cancel", type="secondary", use_container_width=True):
                st.session_state.sos_triggered = False
                st.rerun()

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="font-size:16px;">Emergency contacts</div>', unsafe_allow_html=True)
        for c in st.session_state.emergency_contacts:
            st.markdown(
                f"""
                <div class="id-field" style="margin-bottom:6px;">
                  <span class="k">{c['name']}</span>
                  <span class="v">{c['phone']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# ECO TRACKER
# ===========================================================================
with tab_eco:
    st.markdown('<div class="eyebrow">Real impact</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your eco <em>impact.</em></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Real numbers, calculated per trip from distance, vehicle type, '
        "and seats filled.</div>",
        unsafe_allow_html=True,
    )

    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown(
            '<div class="kpi"><div class="label">CO₂ saved</div>'
            '<div class="value">42.6<span class="unit">kg</span></div>'
            '<div class="delta">▲ 18% vs last month</div></div>',
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            '<div class="kpi"><div class="label">Fuel saved</div>'
            '<div class="value">18.2<span class="unit">L</span></div>'
            '<div class="delta">▲ 22%</div></div>',
            unsafe_allow_html=True,
        )
    with e3:
        st.markdown(
            '<div class="kpi"><div class="label">Money saved</div>'
            '<div class="value">₹3,420</div>'
            '<div class="delta">▲ 11%</div></div>',
            unsafe_allow_html=True,
        )
    with e4:
        st.markdown(
            '<div class="kpi"><div class="label">Trips shared</div>'
            '<div class="value">27</div>'
            '<div class="delta">▲ 6 trips</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Monthly goal · 60 kg CO₂ saved</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eco-bar"><div style="width:71%;"></div></div>'
        '<div style="display:flex;justify-content:space-between;font-size:12px;'
        'color:var(--ink-mute);font-weight:600;">'
        "<span>42.6 kg saved</span><span>71% of monthly goal</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title" style="margin-bottom:14px;">City leaderboard · Pune</div>',
        unsafe_allow_html=True,
    )
    leaders = [
        ("1", "Aarav K.", 184),
        ("2", "Priya S.", 172),
        ("3", "You", 42.6),
        ("4", "Rohan M.", 38.1),
        ("5", "Sneha P.", 31.4),
    ]
    for rank, name, val in leaders:
        is_you = name == "You"
        bg = "var(--teal-soft)" if is_you else "var(--surface)"
        border = "var(--teal-tint)" if is_you else "var(--line)"
        weight = "700" if is_you else "600"
        st.markdown(
            f"""
            <div class="leader-row" style="background:{bg};border:1px solid {border};">
              <div style="display:flex;align-items:center;gap:16px;">
                <div style="font-family:'Fraunces',serif;font-size:22px;font-weight:500;
                            color:var(--ink-mute);width:28px;letter-spacing:-0.5px;">#{rank}</div>
                <div style="font-size:14px;font-weight:{weight};color:var(--ink);">{name}</div>
              </div>
              <div style="font-size:14px;font-weight:700;color:var(--teal);">{val} kg CO₂</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
