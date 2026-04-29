"""
RideSync. AI-powered carpooling demo built in Streamlit.

Color system inspired by GoFetch reference screens:
  - Pure white background
  - Deep navy for primary buttons, headings, active states
  - Cobalt blue accent for icons, links, active indicators
  - Soft blue tint for icon backgrounds
  - Coral for status pills and alerts
  - Slate gray for body text
"""

from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="RideSync. Commute smarter, together.",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #FFFFFF;
  --bg-soft: #F7F9FC;
  --surface: #FFFFFF;
  --surface-2: #F4F7FB;
  --ink: #0D1B2A;
  --ink-soft: #4A5A6A;
  --ink-mute: #8A95A3;
  --line: #E8EDF3;
  --line-strong: #D8DFE8;
  --blue: #2563EB;
  --blue-deep: #1D4ED8;
  --blue-soft: #EAF2FF;
  --blue-tint: #C7DBF7;
  --coral: #F25C5C;
  --coral-soft: #FFE8E8;
  --coral-deep: #D63E3E;
  --success: #16A34A;
  --success-soft: #E6F6EC;
  --success-tint: #BFE5CC;
  --shadow-sm: 0 1px 2px rgba(13,27,42,0.04);
  --shadow-md: 0 6px 18px rgba(13,27,42,0.06);
  --shadow-lg: 0 18px 40px rgba(13,27,42,0.08);
}

html, body, [class*="css"] {
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--ink);
}
.stApp { background: var(--bg); }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}
.block-container { padding-top: 2rem; max-width: 1280px; }

.stTabs [data-baseweb="tab-list"] {
  gap: 2px; background: var(--bg-soft); padding: 5px;
  border-radius: 12px; border: 1px solid var(--line);
}
.stTabs [data-baseweb="tab"] {
  background: transparent; border-radius: 9px; padding: 9px 16px;
  color: var(--ink-soft); font-weight: 600; font-size: 13px;
}
.stTabs [aria-selected="true"] {
  background: var(--ink) !important; color: #FFFFFF !important;
}

.stButton > button {
  background: var(--ink); color: #FFFFFF; border: none;
  border-radius: 999px; padding: 13px 24px; font-weight: 700;
  font-family: 'Inter', sans-serif; font-size: 14px;
  transition: transform 0.15s ease, box-shadow 0.2s ease, background 0.15s ease;
  box-shadow: 0 4px 14px rgba(13,27,42,0.18);
}
.stButton > button:hover {
  transform: translateY(-1px); background: #000000; color: #FFFFFF;
  box-shadow: 0 8px 22px rgba(13,27,42,0.28);
}
.stButton > button:focus {
  background: var(--ink); color: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.25);
}
.stButton > button[kind="secondary"] {
  background: var(--surface); color: var(--ink);
  border: 1px solid var(--line-strong); box-shadow: none;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--bg-soft); border-color: var(--ink-mute); color: var(--ink);
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stTimeInput > div > div > input {
  background: var(--surface) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: 12px !important; color: var(--ink) !important;
  font-family: 'Inter', sans-serif !important; padding: 12px 14px !important;
}
.stSelectbox > div > div {
  background: var(--surface) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: 12px !important; color: var(--ink) !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stDateInput label, .stTimeInput label, .stRadio label,
.stFileUploader label, .stTextArea label {
  color: var(--ink-soft) !important; font-weight: 600 !important;
  font-size: 12.5px !important;
}
.stTextArea textarea {
  background: var(--surface) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: 12px !important; color: var(--ink) !important;
}

[data-testid="stFileUploader"] section {
  background: var(--bg-soft); border: 1.5px dashed var(--line-strong);
  border-radius: 14px; padding: 18px;
}
[data-testid="stFileUploader"] section:hover {
  border-color: var(--blue); background: var(--blue-soft);
}
[data-testid="stFileUploader"] button {
  background: var(--surface) !important; color: var(--ink) !important;
  border: 1px solid var(--line-strong) !important; border-radius: 999px !important;
}

.brand {
  display: flex; align-items: center; gap: 12px;
  font-size: 22px; font-weight: 800; letter-spacing: -0.4px;
  color: var(--ink); margin-bottom: 24px;
}
.brand-mark {
  width: 40px; height: 40px; border-radius: 12px;
  background: var(--ink); display: flex; align-items: center; justify-content: center;
  color: #FFFFFF; font-weight: 800; font-size: 18px;
  box-shadow: 0 6px 14px rgba(13,27,42,0.18);
}
.brand-tag {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1.2px; color: var(--blue); margin-left: 4px;
  padding: 4px 10px; border-radius: 999px; background: var(--blue-soft);
}

.hero {
  position: relative; padding: 48px 44px 44px; border-radius: 20px;
  background: var(--surface); border: 1px solid var(--line);
  box-shadow: var(--shadow-sm); overflow: hidden; margin-bottom: 32px;
}
.hero-pill {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 7px 14px; background: var(--blue-soft);
  border: 1px solid var(--blue-tint); border-radius: 999px;
  color: var(--blue); font-size: 11px; font-weight: 700;
  letter-spacing: 0.6px; text-transform: uppercase;
}
.hero h1 {
  font-size: 52px; font-weight: 800; line-height: 1.05;
  letter-spacing: -1.6px; margin: 18px 0 14px; color: var(--ink);
}
.hero h1 span.accent { color: var(--blue); }
.hero p.lede {
  font-size: 17px; line-height: 1.55; color: var(--ink-soft);
  max-width: 620px; margin-bottom: 26px; font-weight: 400;
}
.stat-row { display: flex; flex-wrap: wrap; gap: 10px; }
.stat-chip {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 14px; background: var(--bg-soft);
  border: 1px solid var(--line); border-radius: 999px;
  color: var(--ink); font-size: 13px; font-weight: 600;
}
.stat-chip .dot {
  width: 8px; height: 8px; border-radius: 50%; background: var(--blue);
  box-shadow: 0 0 8px rgba(37,99,235,0.5);
  animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.55; transform: scale(1.4); }
}

.section-title {
  font-size: 28px; font-weight: 800; letter-spacing: -0.7px;
  color: var(--ink); margin: 12px 0 6px;
}
.section-sub {
  color: var(--ink-mute); font-size: 14px; margin-bottom: 22px;
  max-width: 640px; line-height: 1.55;
}
.eyebrow {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1.2px; color: var(--blue); margin-bottom: 4px;
}

.card {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 16px; padding: 24px; box-shadow: var(--shadow-sm);
}
.card-title {
  font-size: 18px; font-weight: 700; letter-spacing: -0.2px;
  color: var(--ink); margin-bottom: 4px;
}

.empathy {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 14px; margin: 8px 0 32px;
}
.empathy .item {
  padding: 22px; background: var(--bg-soft); border: 1px solid var(--line);
  border-radius: 16px; position: relative;
}
.empathy .item::before {
  content: "\\201C"; position: absolute; top: -6px; left: 16px;
  font-size: 56px; color: var(--blue); line-height: 1;
  opacity: 0.35; font-weight: 800;
}
.empathy .item .q {
  font-size: 16px; line-height: 1.45; color: var(--ink);
  margin-bottom: 12px; font-weight: 500;
}
.empathy .item .a {
  font-size: 11px; color: var(--ink-mute); font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.6px;
}

.feature-card {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 18px; padding: 26px; height: 100%;
  position: relative; box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.feature-card:hover {
  transform: translateY(-3px); box-shadow: var(--shadow-lg);
}
.feature-card .icon {
  width: 52px; height: 52px; border-radius: 14px; background: var(--blue-soft);
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; margin-bottom: 18px;
}
.feature-card.coral .icon { background: var(--coral-soft); }
.feature-card.success .icon { background: var(--success-soft); }
.feature-card h3 {
  font-size: 19px; font-weight: 800; letter-spacing: -0.3px;
  margin: 0 0 8px; color: var(--ink);
}
.feature-card p {
  font-size: 14px; color: var(--ink-soft); line-height: 1.55; margin: 0;
}

.match-card {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 18px; padding: 22px; margin-bottom: 14px;
  display: flex; flex-direction: column; gap: 14px;
  transition: all 0.2s ease; box-shadow: var(--shadow-sm);
}
.match-card:hover { border-color: var(--blue-tint); box-shadow: var(--shadow-md); }
.match-head { display: flex; align-items: center; gap: 14px; }
.avatar {
  width: 52px; height: 52px; border-radius: 50%;
  background: var(--ink); display: flex; align-items: center; justify-content: center;
  font-weight: 700; color: #FFFFFF; font-size: 16px; position: relative;
}
.avatar.verified::after {
  content: "✓"; position: absolute; width: 18px; height: 18px;
  background: var(--blue); border-radius: 50%; color: #FFFFFF;
  font-size: 11px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  bottom: -3px; right: -3px; border: 2px solid var(--surface);
}
.match-name { font-size: 16px; font-weight: 700; color: var(--ink); }
.match-sub { font-size: 12px; color: var(--ink-mute); margin-top: 2px; font-weight: 500; }
.match-score { margin-left: auto; text-align: right; }
.match-score .num {
  font-size: 30px; font-weight: 800; color: var(--blue);
  line-height: 1; letter-spacing: -0.5px;
}
.match-score .label {
  font-size: 10px; color: var(--ink-mute); text-transform: uppercase;
  letter-spacing: 0.8px; font-weight: 700; margin-top: 4px;
}
.route-row {
  display: flex; gap: 12px; align-items: center;
  padding: 14px 16px; background: var(--bg-soft); border-radius: 12px;
}
.route-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--ink); }
.route-dot.end { background: transparent; border: 2px solid var(--blue); }
.route-line { flex: 1; height: 1px; border-top: 1px dashed var(--line-strong); }
.route-text { font-size: 13px; color: var(--ink); font-weight: 600; }
.match-meta {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 12px;
}
.match-meta .tags { display: flex; gap: 6px; flex-wrap: wrap; }
.match-meta .price-block { display: flex; align-items: center; gap: 16px; }
.price-block .time-label {
  font-size: 10px; color: var(--ink-mute); text-transform: uppercase;
  letter-spacing: 0.8px; font-weight: 700;
}
.price-block .time-val { font-size: 14px; font-weight: 700; color: var(--ink); }
.price-block .fare {
  font-size: 22px; font-weight: 800; color: var(--ink); letter-spacing: -0.3px;
}

.tag {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 11px; background: var(--bg-soft); border: 1px solid var(--line);
  border-radius: 999px; font-size: 11px; color: var(--ink-soft); font-weight: 600;
}
.tag.blue { color: var(--blue); border-color: var(--blue-tint); background: var(--blue-soft); }
.tag.coral { color: var(--coral-deep); border-color: rgba(242,92,92,0.3); background: var(--coral-soft); }
.tag.success { color: var(--success); border-color: var(--success-tint); background: var(--success-soft); }

.status-pill {
  font-size: 10px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 0.8px; padding: 5px 10px; border-radius: 999px;
}
.status-pill.upcoming { background: var(--blue-soft); color: var(--blue); }
.status-pill.completed { background: var(--coral-soft); color: var(--coral-deep); }
.status-pill.cancelled { background: var(--coral-soft); color: var(--coral-deep); }
.status-pill.confirmed { background: var(--ink); color: #FFFFFF; }

.kpi {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 16px; padding: 22px; box-shadow: var(--shadow-sm);
}
.kpi .label {
  font-size: 11px; color: var(--ink-mute); text-transform: uppercase;
  letter-spacing: 0.8px; font-weight: 700;
}
.kpi .value {
  font-size: 34px; font-weight: 800; color: var(--ink);
  line-height: 1.1; margin-top: 8px; letter-spacing: -1px;
}
.kpi .value .unit { font-size: 16px; color: var(--ink-mute); margin-left: 4px; font-weight: 600; }
.kpi .delta { font-size: 12px; color: var(--success); font-weight: 700; margin-top: 6px; }
.kpi .delta.down { color: var(--coral-deep); }

.id-field {
  display: flex; justify-content: space-between; align-items: center;
  padding: 13px 16px; background: var(--bg-soft); border-radius: 12px;
  margin-bottom: 8px; border: 1px solid var(--line);
}
.id-field .k {
  font-size: 11px; color: var(--ink-mute); font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.6px;
}
.id-field .v {
  font-size: 14px; color: var(--ink); font-weight: 600;
  display: flex; align-items: center; gap: 8px;
}
.id-field.ok { border-color: var(--success-tint); background: var(--success-soft); }
.id-field .check {
  color: var(--success); font-weight: 800; font-size: 14px;
  width: 20px; height: 20px; border-radius: 50%;
  background: rgba(22,163,74,0.18);
  display: inline-flex; align-items: center; justify-content: center;
}

.verify-result {
  padding: 22px 26px; border-radius: 16px;
  background: var(--success-soft); border: 1px solid var(--success-tint);
  display: flex; align-items: center; gap: 16px;
}
.verify-result .ico { font-size: 32px; }
.verify-result .title { font-size: 17px; font-weight: 800; color: var(--ink); }
.verify-result .sub { font-size: 13px; color: var(--ink-soft); margin-top: 4px; line-height: 1.5; }

.eco-bar {
  height: 12px; background: var(--bg-soft); border: 1px solid var(--line);
  border-radius: 999px; overflow: hidden; margin: 10px 0 6px;
}
.eco-bar > div { height: 100%; background: var(--blue); border-radius: 999px; }

.safety-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 18px; background: var(--surface); border: 1px solid var(--line);
  border-radius: 14px; margin-bottom: 10px; box-shadow: var(--shadow-sm);
}
.safety-row .left { display: flex; align-items: center; gap: 14px; }
.safety-row .ico {
  width: 42px; height: 42px; border-radius: 12px; background: var(--blue-soft);
  display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.safety-row .ico.coral { background: var(--coral-soft); }
.safety-row .label { font-size: 14px; font-weight: 700; color: var(--ink); }
.safety-row .desc { font-size: 12.5px; color: var(--ink-mute); margin-top: 3px; line-height: 1.4; }

.sos-active {
  background: var(--coral-soft); border: 1px solid rgba(242,92,92,0.4);
  padding: 22px 26px; border-radius: 16px;
  display: flex; align-items: center; gap: 16px;
}
.sos-active .ico { font-size: 32px; animation: shake 0.5s infinite; }
@keyframes shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-8deg); }
  75% { transform: rotate(8deg); }
}

.trip-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 22px; background: var(--surface); border: 1px solid var(--line);
  border-radius: 16px; margin-bottom: 10px; box-shadow: var(--shadow-sm);
}
.trip-row .info { display: flex; flex-direction: column; gap: 4px; }
.trip-row .route { font-size: 16px; font-weight: 700; color: var(--ink); letter-spacing: -0.2px; }
.trip-row .meta { font-size: 12px; color: var(--ink-mute); font-weight: 500; }
.trip-row .right { display: flex; align-items: center; gap: 14px; }

.leader-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px; border-radius: 14px; margin-bottom: 8px;
}

.divider { height: 1px; background: var(--line); margin: 36px 0; }

.toast-success {
  background: var(--success-soft); border: 1px solid var(--success-tint);
  color: var(--ink); padding: 14px 18px; border-radius: 12px;
  margin-bottom: 14px; display: flex; align-items: center; gap: 12px;
  font-size: 14px; font-weight: 600;
}

@media (max-width: 900px) {
  .hero { padding: 36px 24px; }
  .hero h1 { font-size: 36px; letter-spacing: -1px; }
  .empathy { grid-template-columns: 1fr; }
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

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

tab_home, tab_find, tab_verify, tab_trips, tab_safety, tab_eco = st.tabs(
    ["Home", "Find a ride", "Verify ID", "My trips", "Safety", "Eco tracker"]
)

# ============== HOME ==============
with tab_home:
    verified_badge = ""
    if st.session_state.verified:
        verified_badge = '<div class="stat-chip"><span style="color:var(--success);">✓</span> Identity verified</div>'

    st.markdown(
        f"""
        <div class="hero">
          <span class="hero-pill">✦ AI-powered carpooling</span>
          <h1>Commute smarter,<br/><span class="accent">together.</span></h1>
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

    st.markdown('<div class="eyebrow">Why we built this</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">The commute is broken. We listened.</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="empathy">
          <div class="item">
            <div class="q">My fuel costs are killing me, but Ola surge pricing is even worse during rains.</div>
            <div class="a">Aadith Sukumar, IT corridor commuter</div>
          </div>
          <div class="item">
            <div class="q">I have an empty car going the same way every morning. Feels like such a waste.</div>
            <div class="a">Niraj, Hinjewadi to Baner</div>
          </div>
          <div class="item">
            <div class="q">I would carpool, but I just don't trust riding with random strangers.</div>
            <div class="a">Sriya, Symbiosis student</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            st.success("Showing matches in the Find a ride tab.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">What makes us different</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Three things our users actually care about.</div>', unsafe_allow_html=True)

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
            <div class="feature-card coral">
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
            <div class="feature-card success">
              <div class="icon">🌿</div>
              <h3>Eco Tracker</h3>
              <p>See your real CO₂ savings, fuel cost avoided, and money saved per trip.
              Compete on a city leaderboard with other green commuters.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============== FIND A RIDE ==============
with tab_find:
    st.markdown('<div class="eyebrow">Smart Match</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Find your ride.</div>', unsafe_allow_html=True)
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

    fb1, _ = st.columns([1, 5])
    with fb1:
        if st.button("Find matches", key="btn_find_matches", use_container_width=True):
            st.session_state.matches_found = True

    if st.session_state.matches_found:
        st.markdown("<br/>", unsafe_allow_html=True)

        matches = [
            {"id": "m1", "name": "Aarav K.", "initials": "AK", "trips": 142, "rating": 4.9,
             "score": 96, "time": "8:45 AM", "fare": 85,
             "tags": [("Verified", "success"), ("Quiet ride", ""), ("Same office", "blue")]},
            {"id": "m2", "name": "Priya S.", "initials": "PS", "trips": 78, "rating": 4.8,
             "score": 91, "time": "9:00 AM", "fare": 80,
             "tags": [("Verified", "success"), ("Music OK", ""), ("Female riders only", "coral")]},
            {"id": "m3", "name": "Rohan M.", "initials": "RM", "trips": 211, "rating": 4.7,
             "score": 84, "time": "8:30 AM", "fare": 90,
             "tags": [("Verified", "success"), ("AC car", ""), ("Pet-friendly", "")]},
        ]

        for m in matches:
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

            bcol1, _, _ = st.columns([1.2, 1.2, 4])
            with bcol1:
                if booked:
                    st.markdown(
                        '<div class="toast-success" style="margin-bottom:18px;">'
                        '<span style="color:var(--success);">✓</span> Booked. See My trips.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    if st.button("Book this ride", key=f"book_{m['id']}", use_container_width=True):
                        st.session_state.booked_rides.append({
                            "id": m["id"], "name": m["name"],
                            "from": from_loc, "to": to_loc,
                            "time": m["time"], "fare": m["fare"], "status": "upcoming",
                        })
                        st.rerun()

# ============== VERIFY ID ==============
with tab_verify:
    st.markdown('<div class="eyebrow">Trust layer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Verify your identity.</div>', unsafe_allow_html=True)
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
        uploaded = st.file_uploader("ID image", type=["png", "jpg", "jpeg"],
                                     label_visibility="collapsed", key="id_upload")
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

# ============== MY TRIPS ==============
with tab_trips:
    st.markdown('<div class="eyebrow">Your journey</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">My trips.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Upcoming and past rides, all in one place.</div>', unsafe_allow_html=True)

    upcoming = [t for t in st.session_state.booked_rides if t["status"] == "upcoming"]
    completed_demo = [
        {"name": "Sneha P.", "from": "Hinjewadi Phase 1", "to": "Baner, Pune",
         "time": "Mon, 8:30 AM", "fare": 80, "status": "completed"},
        {"name": "Karthik V.", "from": "Aundh", "to": "Hinjewadi Phase 1",
         "time": "Fri, 7:15 PM", "fare": 95, "status": "completed"},
        {"name": "Meera J.", "from": "Wakad", "to": "FC Road",
         "time": "Wed, 9:00 AM", "fare": 110, "status": "cancelled"},
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
                    <span class="status-pill confirmed">CONFIRMED</span>
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
    st.markdown('<div class="card-title" style="margin-bottom:14px;">Past rides</div>', unsafe_allow_html=True)
    for t in completed_demo:
        pill_class = t["status"]
        pill_text = t["status"].upper()
        st.markdown(
            f"""
            <div class="trip-row">
              <div class="info">
                <div class="route">{t['from']} → {t['to']}</div>
                <div class="meta">With {t['name']} · {t['time']} · ₹{t['fare']}</div>
              </div>
              <div class="right">
                <span class="status-pill {pill_class}">{pill_text}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============== SAFETY ==============
with tab_safety:
    st.markdown('<div class="eyebrow">Peace of mind</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Safety center.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Every protection layer between you and a stranger\'s car.</div>',
        unsafe_allow_html=True,
    )

    sc1, sc2 = st.columns([1.4, 1])

    with sc1:
        safety_items = [
            ("🪪", "ID verification", "Government or institutional ID required for every user.", ""),
            ("📍", "Live trip tracking", "Share your live location with up to 5 emergency contacts.", ""),
            ("🚨", "SOS button", "One-tap alert to local police, your contacts, and our 24/7 ops team.", "coral"),
            ("🎙️", "Trip audio recording", "Optional encrypted recording, accessible only on incident report.", ""),
            ("⭐", "Two-way ratings", "Riders rate drivers and drivers rate riders. Below 4.0 means review.", ""),
            ("👮", "Background checks", "Driving licence, vehicle RC, and insurance verified at signup.", ""),
        ]
        for ico, label, desc, ico_class in safety_items:
            st.markdown(
                f"""
                <div class="safety-row">
                  <div class="left">
                    <div class="ico {ico_class}">{ico}</div>
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
                    <div style="font-weight:800;font-size:15px;color:var(--ink);">SOS active</div>
                    <div style="font-size:12.5px;color:var(--ink-soft);margin-top:4px;line-height:1.5;">
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

# ============== ECO TRACKER ==============
with tab_eco:
    st.markdown('<div class="eyebrow">Real impact</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your eco impact.</div>', unsafe_allow_html=True)
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
        bg = "var(--blue-soft)" if is_you else "var(--surface)"
        border = "var(--blue-tint)" if is_you else "var(--line)"
        weight = "800" if is_you else "600"
        st.markdown(
            f"""
            <div class="leader-row" style="background:{bg};border:1px solid {border};">
              <div style="display:flex;align-items:center;gap:16px;">
                <div style="font-size:20px;font-weight:800;
                            color:var(--ink-mute);width:32px;letter-spacing:-0.3px;">#{rank}</div>
                <div style="font-size:14px;font-weight:{weight};color:var(--ink);">{name}</div>
              </div>
              <div style="font-size:14px;font-weight:800;color:var(--blue);">{val} kg CO₂</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
