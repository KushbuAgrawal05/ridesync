"""
RideSync. AI-powered carpooling app demo built in Streamlit.

Design thinking notes (EDIPT applied silently in the build):
- Empathize: commuters waste money, time, and emotional bandwidth on solo drives.
  The home page leads with their pain (cost, traffic, isolation), not our features.
- Define: the core problem is trust + matching, not just ride listing.
  So ID verification, ratings, and route-precision get top billing.
- Ideate: instead of a generic "list of rides" UI, we use Smart Match cards with
  compatibility scores, an Eco Tracker that shows real impact, and a Safety center
  with verifiable trust signals.
- Prototype: this app is the prototype. Streamlit constraints respected.
- Test: every interactive piece (search, verify, match, book) has feedback states
  so a user testing the demo always knows what just happened.
"""

import base64
import io
import random
import re
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
# Global styles
# ---------------------------------------------------------------------------
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #0B0F19;
  --bg-soft: #111828;
  --surface: #131B2C;
  --surface-2: #1A2438;
  --border: rgba(255,255,255,0.08);
  --border-strong: rgba(255,255,255,0.16);
  --text: #F4F6FB;
  --text-soft: #B7C0D1;
  --text-mute: #7A8499;
  --accent: #14E0A0;
  --accent-soft: rgba(20, 224, 160, 0.14);
  --accent-deep: #0BAF7C;
  --warn: #FFB547;
  --danger: #FF6B6B;
  --info: #6FA8FF;
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.45);
  --radius: 16px;
}

html, body, [class*="css"]  {
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  color: var(--text);
}

.stApp {
  background:
    radial-gradient(1200px 600px at 80% -10%, rgba(20,224,160,0.10), transparent 60%),
    radial-gradient(900px 500px at -10% 30%, rgba(111,168,255,0.08), transparent 60%),
    var(--bg);
}

/* Hide Streamlit chrome we don't need */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  background: var(--surface);
  padding: 6px;
  border-radius: 14px;
  border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
  background: transparent;
  border-radius: 10px;
  padding: 10px 16px;
  color: var(--text-soft);
  font-weight: 600;
  font-size: 14px;
}
.stTabs [aria-selected="true"] {
  background: var(--accent-soft) !important;
  color: var(--accent) !important;
}

/* Buttons */
.stButton > button {
  background: var(--accent);
  color: #051912;
  border: none;
  border-radius: 12px;
  padding: 12px 20px;
  font-weight: 700;
  font-family: 'Plus Jakarta Sans', sans-serif;
  transition: transform 0.15s ease, box-shadow 0.2s ease;
  box-shadow: 0 8px 22px rgba(20,224,160,0.25);
}
.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 28px rgba(20,224,160,0.35);
  background: var(--accent);
  color: #051912;
}

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stTimeInput > div > div > input {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stDateInput label, .stTimeInput label, .stRadio label, .stFileUploader label {
  color: var(--text-soft) !important;
  font-weight: 600 !important;
  font-size: 13px !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
  background: var(--surface);
  border: 1.5px dashed var(--border-strong);
  border-radius: 14px;
}
[data-testid="stFileUploader"] section:hover {
  border-color: var(--accent);
}

/* ---------- Custom components ---------- */

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Fraunces', serif;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: var(--text);
}
.brand-mark {
  width: 38px; height: 38px;
  border-radius: 11px;
  background: linear-gradient(135deg, var(--accent), var(--accent-deep));
  display: flex; align-items: center; justify-content: center;
  color: #051912;
  font-weight: 800;
  font-size: 18px;
  box-shadow: 0 8px 18px rgba(20,224,160,0.35);
}
.brand-tag {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.4px;
  color: var(--text-mute);
  margin-left: 8px;
  padding: 4px 8px;
  border: 1px solid var(--border);
  border-radius: 6px;
}

.hero {
  position: relative;
  padding: 56px 48px 48px;
  border-radius: 24px;
  background:
    radial-gradient(600px 280px at 90% 0%, rgba(20,224,160,0.18), transparent 60%),
    linear-gradient(180deg, #0F1626 0%, #0B0F19 100%);
  border: 1px solid var(--border);
  overflow: hidden;
  margin-bottom: 28px;
}
.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
  mask-image: radial-gradient(ellipse at top right, black 30%, transparent 75%);
}
.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  background: var(--accent-soft);
  border: 1px solid rgba(20,224,160,0.35);
  border-radius: 999px;
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  position: relative;
  z-index: 2;
}
.hero h1 {
  font-family: 'Fraunces', serif;
  font-size: 64px;
  font-weight: 600;
  line-height: 1.05;
  letter-spacing: -2px;
  margin: 18px 0 14px;
  color: var(--text);
  position: relative;
  z-index: 2;
}
.hero h1 em {
  font-style: italic;
  font-weight: 500;
  color: var(--accent);
}
.hero p {
  font-size: 17px;
  line-height: 1.55;
  color: var(--text-soft);
  max-width: 560px;
  position: relative;
  z-index: 2;
  margin-bottom: 24px;
}
.stat-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  position: relative;
  z-index: 2;
}
.stat-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--text);
  font-size: 13px;
  font-weight: 600;
}
.stat-chip .dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 10px var(--accent);
  animation: pulse 1.6s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.3); }
}

.section-title {
  font-family: 'Fraunces', serif;
  font-size: 30px;
  font-weight: 600;
  letter-spacing: -0.8px;
  color: var(--text);
  margin: 8px 0 6px;
}
.section-sub {
  color: var(--text-mute);
  font-size: 14px;
  margin-bottom: 22px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px;
  height: 100%;
}
.card.elev:hover {
  border-color: var(--border-strong);
  transform: translateY(-2px);
  transition: all 0.2s ease;
}

.feature-card {
  background: linear-gradient(180deg, var(--surface) 0%, var(--bg-soft) 100%);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 24px;
  height: 100%;
  position: relative;
  overflow: hidden;
}
.feature-card .icon {
  width: 44px; height: 44px;
  border-radius: 12px;
  background: var(--accent-soft);
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  margin-bottom: 16px;
}
.feature-card h3 {
  font-family: 'Fraunces', serif;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.4px;
  margin: 0 0 8px;
  color: var(--text);
}
.feature-card p {
  font-size: 14px;
  color: var(--text-soft);
  line-height: 1.55;
  margin: 0;
}

.match-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 20px;
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: all 0.2s ease;
}
.match-card:hover { border-color: var(--accent); }
.match-head { display: flex; align-items: center; gap: 14px; }
.avatar {
  width: 52px; height: 52px;
  border-radius: 14px;
  background: linear-gradient(135deg, #6FA8FF, #14E0A0);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; color: #051912; font-size: 18px;
}
.avatar.verified::after {
  content: "✓";
  position: absolute;
  width: 18px; height: 18px;
  background: var(--accent);
  border-radius: 50%;
  color: #051912;
  font-size: 11px;
  font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  transform: translate(34px, -8px);
  border: 2px solid var(--surface);
}
.match-name { font-size: 16px; font-weight: 700; color: var(--text); }
.match-sub { font-size: 12px; color: var(--text-mute); margin-top: 2px; }
.match-score {
  margin-left: auto;
  text-align: right;
}
.match-score .num {
  font-family: 'Fraunces', serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}
.match-score .label {
  font-size: 10px;
  color: var(--text-mute);
  text-transform: uppercase;
  letter-spacing: 1px;
}
.route-row { display: flex; gap: 12px; align-items: center; padding: 10px 14px; background: var(--bg-soft); border-radius: 12px; }
.route-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent); }
.route-dot.end { background: var(--info); }
.route-line { flex: 1; height: 1px; background: var(--border); }
.route-text { font-size: 13px; color: var(--text); font-weight: 600; }

.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-radius: 999px;
  font-size: 11px;
  color: var(--text-soft);
  font-weight: 600;
}
.tag.green { color: var(--accent); border-color: rgba(20,224,160,0.3); background: var(--accent-soft); }
.tag.blue { color: var(--info); border-color: rgba(111,168,255,0.3); background: rgba(111,168,255,0.1); }

.kpi {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
}
.kpi .label { font-size: 12px; color: var(--text-mute); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.kpi .value { font-family: 'Fraunces', serif; font-size: 38px; font-weight: 600; color: var(--text); line-height: 1.1; margin-top: 6px; }
.kpi .delta { font-size: 12px; color: var(--accent); font-weight: 600; margin-top: 4px; }
.kpi .delta.down { color: var(--danger); }

.id-field {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px;
  background: var(--bg-soft);
  border-radius: 10px;
  margin-bottom: 8px;
  border: 1px solid var(--border);
}
.id-field .k { font-size: 12px; color: var(--text-mute); font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; }
.id-field .v { font-size: 14px; color: var(--text); font-weight: 600; }
.id-field.ok { border-color: rgba(20,224,160,0.3); }
.id-field .check { color: var(--accent); font-weight: 800; }

.verify-result {
  padding: 18px 20px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(20,224,160,0.15), rgba(20,224,160,0.05));
  border: 1px solid rgba(20,224,160,0.4);
  display: flex; align-items: center; gap: 14px;
}
.verify-result .ico { font-size: 28px; }
.verify-result .title { font-size: 16px; font-weight: 700; color: var(--text); }
.verify-result .sub { font-size: 13px; color: var(--text-soft); margin-top: 2px; }

.eco-bar {
  height: 10px;
  background: var(--bg-soft);
  border-radius: 999px;
  overflow: hidden;
  margin: 8px 0 4px;
}
.eco-bar > div {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-deep));
  border-radius: 999px;
}

.safety-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin-bottom: 10px;
}
.safety-row .left { display: flex; align-items: center; gap: 12px; }
.safety-row .ico { width: 36px; height: 36px; border-radius: 10px; background: var(--accent-soft); display: flex; align-items: center; justify-content: center; font-size: 16px; }
.safety-row .label { font-size: 14px; font-weight: 600; color: var(--text); }
.safety-row .desc { font-size: 12px; color: var(--text-mute); margin-top: 2px; }

.divider {
  height: 1px;
  background: var(--border);
  margin: 32px 0;
}

/* Empathy strip */
.empathy {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 8px 0 28px;
}
.empathy .item {
  padding: 18px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
}
.empathy .item .q {
  font-family: 'Fraunces', serif;
  font-style: italic;
  font-size: 16px;
  line-height: 1.4;
  color: var(--text);
  margin-bottom: 8px;
}
.empathy .item .a {
  font-size: 12px;
  color: var(--text-mute);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header / brand
# ---------------------------------------------------------------------------
col_brand, col_nav = st.columns([1, 2])
with col_brand:
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
# Tabs
# ---------------------------------------------------------------------------
tab_home, tab_find, tab_verify, tab_safety, tab_eco = st.tabs(
    ["Home", "Find a ride", "Verify ID", "Safety center", "Eco tracker"]
)

# ===========================================================================
# HOME TAB
# ===========================================================================
with tab_home:
    st.markdown(
        """
        <div class="hero">
          <span class="hero-pill">✦ AI-powered carpooling</span>
          <h1>Commute smarter,<br/><em>together.</em></h1>
          <p>RideSync matches you with verified co-travellers on your exact route.
          Save money, cut traffic, and lower your carbon footprint without changing how you live.</p>
          <div class="stat-row">
            <div class="stat-chip"><span class="dot"></span> 247 rides active now</div>
            <div class="stat-chip">🌱 1.2 tonnes CO₂ saved today</div>
            <div class="stat-chip">⭐ 4.8 average rating</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Empathy strip. This is where the Empathize phase shows up.
    st.markdown(
        """
        <div class="empathy">
          <div class="item">
            <div class="q">"My fuel costs are killing me, but Ola surge pricing is worse."</div>
            <div class="a">— Daily commuter, IT corridor</div>
          </div>
          <div class="item">
            <div class="q">"I have an empty car going the same way every morning."</div>
            <div class="a">— Driver, Hinjewadi to Baner</div>
          </div>
          <div class="item">
            <div class="q">"I'd carpool, but I don't want to ride with strangers."</div>
            <div class="a">— Student, Symbiosis</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick search
    st.markdown('<div class="section-title">Quick ride search</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Find a ride or offer seats on your route.</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([3, 3, 1.2, 1.4])
    with c1:
        st.text_input("From", value="Hinjewadi Phase 1", key="home_from")
    with c2:
        st.text_input("To", value="Baner, Pune", key="home_to")
    with c3:
        st.selectbox("Seats", [1, 2, 3, 4], index=1, key="home_seats")
    with c4:
        st.write("")
        st.write("")
        st.button("🔍 Search rides", use_container_width=True, key="home_search")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Feature showcase. Define + Ideate phases.
    st.markdown('<div class="section-title">What makes RideSync different</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Three things our users actually care about, built right.</div>',
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
              <div class="icon">🛡️</div>
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
              <p>See your real CO₂ savings, fuel cost avoided, and traffic reduction
              per trip. Compete on a city leaderboard with other green commuters.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ===========================================================================
# FIND RIDE TAB
# ===========================================================================
with tab_find:
    st.markdown('<div class="section-title">Find your ride</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">AI-ranked matches on your route, sorted by compatibility.</div>',
        unsafe_allow_html=True,
    )

    fc1, fc2, fc3, fc4 = st.columns([2, 2, 1.2, 1.2])
    with fc1:
        from_loc = st.text_input("From", value="Hinjewadi Phase 1", key="find_from")
    with fc2:
        to_loc = st.text_input("To", value="Baner, Pune", key="find_to")
    with fc3:
        depart = st.time_input("Depart by", value=datetime.now().time(), key="find_time")
    with fc4:
        seats = st.selectbox("Seats", [1, 2, 3], key="find_seats")

    if st.button("Find matches", key="btn_find_matches"):
        st.session_state["matches_found"] = True

    if st.session_state.get("matches_found", True):
        # Mock match data
        matches = [
            {
                "name": "Aarav K.",
                "initials": "AK",
                "trips": 142,
                "rating": 4.9,
                "score": 96,
                "from": from_loc,
                "to": to_loc,
                "time": "8:45 AM",
                "fare": 85,
                "tags": ["Verified", "Quiet ride", "Same office"],
            },
            {
                "name": "Priya S.",
                "initials": "PS",
                "trips": 78,
                "rating": 4.8,
                "score": 91,
                "from": from_loc,
                "to": to_loc,
                "time": "9:00 AM",
                "fare": 80,
                "tags": ["Verified", "Music OK", "Female-only riders"],
            },
            {
                "name": "Rohan M.",
                "initials": "RM",
                "trips": 211,
                "rating": 4.7,
                "score": 84,
                "from": from_loc,
                "to": to_loc,
                "time": "8:30 AM",
                "fare": 90,
                "tags": ["Verified", "AC car", "Pet-friendly"],
            },
        ]

        for m in matches:
            tags_html = "".join(f'<span class="tag">{t}</span>' for t in m["tags"])
            st.markdown(
                f"""
                <div class="match-card">
                  <div class="match-head">
                    <div class="avatar">{m['initials']}</div>
                    <div>
                      <div class="match-name">{m['name']}</div>
                      <div class="match-sub">{m['trips']} trips · ⭐ {m['rating']}</div>
                    </div>
                    <div class="match-score">
                      <div class="num">{m['score']}</div>
                      <div class="label">Match score</div>
                    </div>
                  </div>
                  <div class="route-row">
                    <div class="route-dot"></div>
                    <div class="route-text">{m['from']}</div>
                    <div class="route-line"></div>
                    <div class="route-dot end"></div>
                    <div class="route-text">{m['to']}</div>
                  </div>
                  <div style="display:flex;align-items:center;justify-content:space-between;">
                    <div style="display:flex;gap:6px;flex-wrap:wrap;">{tags_html}</div>
                    <div style="display:flex;align-items:center;gap:14px;">
                      <div style="font-size:12px;color:var(--text-mute);">Departs</div>
                      <div style="font-size:14px;font-weight:700;color:var(--text);">{m['time']}</div>
                      <div style="font-family:'Fraunces',serif;font-size:22px;font-weight:600;color:var(--accent);">₹{m['fare']}</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ===========================================================================
# VERIFY ID TAB
# ===========================================================================
with tab_verify:
    st.markdown('<div class="section-title">Verify your identity</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Upload a government or institutional ID. We extract details, '
        'cross-check against your profile, and approve trusted users only.</div>',
        unsafe_allow_html=True,
    )

    vc1, vc2 = st.columns([1, 1.1])

    with vc1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Step 1 of 3** · Upload your ID card", help=None)
        uploaded = st.file_uploader(
            "Drop your ID card image here",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
            key="id_upload",
        )
        if uploaded is not None:
            st.image(uploaded, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with vc2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Step 2 of 3** · Confirm extracted details")

        if uploaded is None:
            st.markdown(
                '<div style="padding:30px 0;text-align:center;color:var(--text-mute);font-size:13px;">'
                "Waiting for your ID upload. Once you drop a card, our OCR pipeline will extract the fields below.</div>",
                unsafe_allow_html=True,
            )
        else:
            # Demo-grade extracted fields. In production this would be Tesseract / AWS Textract / Google Vision.
            extracted = {
                "Full name": "Kushbu Niraj Agrawal",
                "Institution": "Symbiosis Institute of Technology",
                "Course": "B.Tech. CS",
                "PRN / ID number": "23070122267",
                "Date of birth": "05 Oct 2004",
                "Validity": "June 2027",
                "Blood group": "O+",
                "Address": "Hinjawadi, Phase I, Pune 411057",
                "Mobile": "7709458333",
            }
            for k, v in extracted.items():
                st.markdown(
                    f'<div class="id-field ok"><span class="k">{k}</span>'
                    f'<span class="v">{v} <span class="check">✓</span></span></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("Confirm & verify", key="confirm_verify", use_container_width=True):
                st.session_state["verified"] = True
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("verified"):
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
# SAFETY CENTER TAB
# ===========================================================================
with tab_safety:
    st.markdown('<div class="section-title">Safety center</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Every protection layer between you and a stranger\'s car.</div>',
        unsafe_allow_html=True,
    )

    safety_items = [
        ("🪪", "ID verification", "Government or institutional ID required for every user."),
        ("📍", "Live trip tracking", "Share your live location with up to 5 emergency contacts."),
        ("🚨", "SOS button", "One-tap alert to local police, your contacts, and our 24/7 ops team."),
        ("🎙️", "Trip audio recording", "Optional encrypted recording, accessible only on incident report."),
        ("⭐", "Two-way ratings", "Riders rate drivers and drivers rate riders. Below 4.0 means review."),
        ("👮", "Background-checked drivers", "Driving licence, vehicle RC, and insurance verified at signup."),
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
              <div class="tag green">Active</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ===========================================================================
# ECO TRACKER TAB
# ===========================================================================
with tab_eco:
    st.markdown('<div class="section-title">Your eco impact</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Real numbers, calculated per trip from distance, vehicle type, and seats filled.</div>',
        unsafe_allow_html=True,
    )

    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown(
            '<div class="kpi"><div class="label">CO₂ saved</div>'
            '<div class="value">42.6 <span style="font-size:18px;color:var(--text-mute);">kg</span></div>'
            '<div class="delta">↑ 18% vs last month</div></div>',
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            '<div class="kpi"><div class="label">Fuel saved</div>'
            '<div class="value">18.2 <span style="font-size:18px;color:var(--text-mute);">L</span></div>'
            '<div class="delta">↑ 22%</div></div>',
            unsafe_allow_html=True,
        )
    with e3:
        st.markdown(
            '<div class="kpi"><div class="label">Money saved</div>'
            '<div class="value">₹3,420</div>'
            '<div class="delta">↑ 11%</div></div>',
            unsafe_allow_html=True,
        )
    with e4:
        st.markdown(
            '<div class="kpi"><div class="label">Trips shared</div>'
            '<div class="value">27</div>'
            '<div class="delta">↑ 6 trips</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Monthly goal: 60 kg CO₂ saved**")
    st.markdown(
        '<div class="eco-bar"><div style="width:71%;"></div></div>'
        '<div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text-mute);">'
        '<span>42.6 kg saved</span><span>71% of goal</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:22px;">City leaderboard · Pune</div>', unsafe_allow_html=True)
    leaders = [
        ("1", "Aarav K.", "184 kg"),
        ("2", "Priya S.", "172 kg"),
        ("3", "You", "42.6 kg"),
        ("4", "Rohan M.", "38.1 kg"),
        ("5", "Sneha P.", "31.4 kg"),
    ]
    for rank, name, val in leaders:
        is_you = name == "You"
        bg = "var(--accent-soft)" if is_you else "var(--surface)"
        border = "rgba(20,224,160,0.4)" if is_you else "var(--border)"
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:14px 18px;background:{bg};border:1px solid {border};
                        border-radius:12px;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:14px;">
                <div style="font-family:'Fraunces',serif;font-size:20px;font-weight:600;
                            color:var(--text-mute);width:24px;">#{rank}</div>
                <div style="font-size:14px;font-weight:700;color:var(--text);">{name}</div>
              </div>
              <div style="font-size:14px;font-weight:700;color:var(--accent);">{val} CO₂ saved</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
