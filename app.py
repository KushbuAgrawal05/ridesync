import streamlit as st
import random
from datetime import datetime, timedelta
import time

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RideSync",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── RESET & BASE ─────────────────────────────────── */
:root {
    --navy:      #0D1B2A;
    --teal:      #1A6B6B;
    --teal-lt:   #2A9B9B;
    --coral:     #E8534A;
    --coral-lt:  #FDECEA;
    --blue:      #3A86FF;
    --blue-lt:   #EBF2FF;
    --slate:     #4A5568;
    --muted:     #8A94A6;
    --bg:        #F7F9FC;
    --card:      #FFFFFF;
    --border:    #E8EDF5;
    --green:     #22C55E;
    --green-lt:  #DCFCE7;
    --amber:     #F59E0B;
    --amber-lt:  #FEF3C7;
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--navy) !important;
}

h1, h2, h3, h4, .display-font {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── HIDE STREAMLIT CHROME ────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── TOP NAV ──────────────────────────────────────── */
.topnav {
    background: var(--navy);
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 20px rgba(13,27,42,0.3);
}
.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: white;
    letter-spacing: -0.5px;
}
.brand span { color: var(--teal-lt); }
.nav-pill {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 30px;
    padding: 6px 18px;
    color: rgba(255,255,255,0.75);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    display: inline-block;
    margin: 0 4px;
    transition: all 0.2s;
}
.nav-pill.active, .nav-pill:hover {
    background: var(--teal);
    border-color: var(--teal);
    color: white;
}

/* ── NOTIFICATION BADGE ───────────────────────────── */
.notif-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--coral);
    color: white;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 600;
    animation: pulse-coral 2s infinite;
}
@keyframes pulse-coral {
    0%, 100% { box-shadow: 0 0 0 0 rgba(232,83,74,0.4); }
    50%       { box-shadow: 0 0 0 8px rgba(232,83,74,0); }
}

/* ── HERO ─────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, var(--navy) 0%, #1A3A4A 60%, var(--teal) 100%);
    padding: 56px 48px 64px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    border-radius: 50%;
    background: rgba(26,107,107,0.25);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 20%;
    width: 240px; height: 240px;
    border-radius: 50%;
    background: rgba(58,134,255,0.12);
}
.hero-tag {
    display: inline-block;
    background: rgba(42,155,155,0.25);
    border: 1px solid var(--teal-lt);
    color: var(--teal-lt);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: white;
    line-height: 1.15;
    margin: 0 0 12px;
    letter-spacing: -1px;
}
.hero-sub {
    color: rgba(255,255,255,0.65);
    font-size: 16px;
    line-height: 1.6;
    max-width: 520px;
}
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 30px;
    padding: 8px 18px;
    color: white;
    font-size: 13px;
    font-weight: 500;
    margin: 4px 4px 0 0;
}
.stat-pill .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green);
    animation: blink 1.5s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
}

/* ── CARDS ────────────────────────────────────────── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 16px;
    transition: box-shadow 0.2s, transform 0.2s;
}
.card:hover {
    box-shadow: 0 8px 32px rgba(13,27,42,0.08);
    transform: translateY(-1px);
}
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}
.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: var(--navy);
}

/* ── RIDE CARD ────────────────────────────────────── */
.ride-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 20px 22px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    transition: all 0.25s;
}
.ride-card:hover {
    border-color: var(--teal-lt);
    box-shadow: 0 6px 24px rgba(26,107,107,0.12);
    transform: translateY(-2px);
}
.ride-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 4px;
    background: var(--teal);
    border-radius: 4px 0 0 4px;
}
.ride-route {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 10px 0;
}
.route-dot-black {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--navy);
    flex-shrink: 0;
}
.route-dot-blue {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--blue);
    border: 2px solid white;
    box-shadow: 0 0 0 2px var(--blue);
    flex-shrink: 0;
}
.route-line {
    width: 1px; height: 20px;
    background: var(--border);
    margin: 2px 4px;
}

/* ── STATUS BADGES ────────────────────────────────── */
.badge {
    display: inline-block;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.badge-confirmed { background: var(--green-lt);  color: #16A34A; }
.badge-pending   { background: var(--amber-lt);  color: #B45309; }
.badge-cancelled { background: var(--coral-lt);  color: var(--coral); }
.badge-teal      { background: rgba(26,107,107,0.1); color: var(--teal); }

/* ── AVATARS ──────────────────────────────────────── */
.avatar-row {
    display: flex;
    align-items: center;
}
.avatar {
    width: 30px; height: 30px;
    border-radius: 50%;
    border: 2px solid white;
    margin-right: -8px;
    font-size: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: white;
}

/* ── NOTIFY BUTTON ────────────────────────────────── */
.notify-btn {
    background: var(--navy);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
}
.notify-btn:hover { background: var(--teal); transform: scale(1.02); }

/* ── MAP PLACEHOLDER ──────────────────────────────── */
.map-block {
    background: linear-gradient(145deg, #1A3A4A 0%, var(--teal) 100%);
    border-radius: 18px;
    padding: 0;
    height: 200px;
    display: flex;
    align-items: flex-end;
    justify-content: flex-start;
    padding: 20px;
    position: relative;
    overflow: hidden;
}
.map-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px);
    background-size: 30px 30px;
}
.map-label {
    background: rgba(13,27,42,0.85);
    color: white;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
    backdrop-filter: blur(8px);
    z-index: 1;
}

/* ── SMART NOTIFY PANEL ───────────────────────────── */
.notify-panel {
    background: linear-gradient(135deg, var(--navy) 0%, #1A3A4A 100%);
    border-radius: 20px;
    padding: 28px;
    color: white;
    position: relative;
    overflow: hidden;
}
.notify-panel::after {
    content: '🔔';
    position: absolute;
    right: 24px; top: 20px;
    font-size: 48px;
    opacity: 0.1;
}
.notify-feature-row {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.nf-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

/* ── STATS GRID ───────────────────────────────────── */
.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px 24px;
    text-align: center;
}
.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--navy);
    line-height: 1;
}
.stat-label {
    font-size: 12px;
    color: var(--muted);
    font-weight: 500;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.stat-change {
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
    color: var(--green);
}

/* ── INPUTS ───────────────────────────────────────── */
.stTextInput input, .stSelectbox select, .stTimeInput input {
    border-radius: 12px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(26,107,107,0.12) !important;
}

/* ── TABS ─────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg) !important;
    border-radius: 12px !important;
    gap: 4px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--navy) !important;
    color: white !important;
}

/* ── BUTTONS ──────────────────────────────────────── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: var(--navy) !important;
    border-color: var(--navy) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--teal) !important;
    border-color: var(--teal) !important;
    transform: translateY(-1px) !important;
}

/* ── SECTION HEADERS ──────────────────────────────── */
.section-head {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--navy);
    margin: 0 0 4px;
}
.section-sub {
    font-size: 13px;
    color: var(--muted);
    margin: 0 0 20px;
}

/* ── DIVIDER ──────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 24px 0;
}

/* ── ALERT BOX ────────────────────────────────────── */
.alert-box {
    background: var(--green-lt);
    border: 1px solid #86EFAC;
    border-radius: 14px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: #166534;
    font-weight: 500;
}
.alert-box-warn {
    background: var(--amber-lt);
    border: 1px solid #FCD34D;
    border-radius: 14px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: #92400E;
    font-weight: 500;
}

/* ── USER AVATARS COLORS ─────────────────────────── */
.av-teal   { background: var(--teal); }
.av-navy   { background: var(--navy); }
.av-coral  { background: var(--coral); }
.av-blue   { background: var(--blue); }
.av-amber  { background: var(--amber); }

/* ── BOTTOM TABS (MOBILE FEEL) ────────────────────── */
.bottom-nav {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: var(--card);
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-around;
    padding: 10px 0 14px;
    z-index: 99;
    box-shadow: 0 -4px 20px rgba(13,27,42,0.06);
}
.bnav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    cursor: pointer;
    padding: 4px 20px;
    border-radius: 10px;
    transition: all 0.2s;
}
.bnav-item.active .bnav-label { color: var(--teal); font-weight: 600; }
.bnav-label {
    font-size: 11px;
    color: var(--muted);
    font-weight: 500;
}
.content-pad { padding: 24px 32px 100px; }

/* ── PROGRESS BAR ─────────────────────────────────── */
.co2-bar-bg {
    background: var(--border);
    border-radius: 99px;
    height: 8px;
    margin: 8px 0;
}
.co2-bar-fill {
    background: linear-gradient(90deg, var(--teal), var(--blue));
    border-radius: 99px;
    height: 8px;
    transition: width 0.8s ease;
}

/* ── FEATURE CHIP ─────────────────────────────────── */
.feature-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--blue-lt);
    border: 1px solid #BFDBFE;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 600;
    color: var(--blue);
    margin: 3px;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"
if "notifications" not in st.session_state:
    st.session_state.notifications = []
if "smart_notify_sent" not in st.session_state:
    st.session_state.smart_notify_sent = False
if "rides_offered" not in st.session_state:
    st.session_state.rides_offered = 0
if "notify_contacts" not in st.session_state:
    st.session_state.notify_contacts = ["Priya Sharma", "Rahul Mehta", "Ananya Singh"]
if "co2_saved" not in st.session_state:
    st.session_state.co2_saved = 34.2

# ─── FAKE DATA ────────────────────────────────────────────────────────────────
available_rides = [
    {"driver": "Arjun Patel", "from": "Hinjewadi Phase 1", "to": "Baner", "time": "8:45 AM",
     "seats": 2, "price": "₹45", "rating": 4.8, "verified": True, "eta": "12 min",
     "initials": "AP", "color": "av-teal", "tags": ["AC", "Music OK"]},
    {"driver": "Sneha Kulkarni", "from": "Wakad", "to": "Shivajinagar", "time": "9:00 AM",
     "seats": 1, "price": "₹62", "rating": 4.9, "verified": True, "eta": "8 min",
     "initials": "SK", "color": "av-coral", "tags": ["Female Only", "No Smoking"]},
    {"driver": "Rohan Desai", "from": "Kothrud", "to": "Hadapsar", "time": "9:15 AM",
     "seats": 3, "price": "₹38", "rating": 4.6, "verified": True, "eta": "20 min",
     "initials": "RD", "color": "av-navy", "tags": ["AC", "Pets OK"]},
    {"driver": "Meera Joshi", "from": "Aundh", "to": "Viman Nagar", "time": "9:30 AM",
     "seats": 2, "price": "₹55", "rating": 4.7, "verified": True, "eta": "5 min",
     "initials": "MJ", "color": "av-blue", "tags": ["Express", "AC"]},
]

my_trips = [
    {"from": "Engineering Hall", "to": "Student Residences", "date": "Today", "time": "5:30 PM",
     "price": "₹7.88", "status": "confirmed", "co_travelers": ["AP", "SK"]},
    {"from": "Campus Library", "to": "Downtown Hub", "date": "Yesterday", "time": "6:00 PM",
     "price": "₹9.50", "status": "completed", "co_travelers": ["RD"]},
    {"from": "Gym Center", "to": "Physics Lab", "date": "Apr 26", "time": "7:00 AM",
     "price": "₹5.25", "status": "cancelled", "co_travelers": []},
]

contacts = [
    {"name": "Priya Sharma",    "initials": "PS", "color": "av-coral", "status": "online",  "phone": "+91 98765 43210"},
    {"name": "Rahul Mehta",     "initials": "RM", "color": "av-blue",  "status": "offline", "phone": "+91 87654 32109"},
    {"name": "Ananya Singh",    "initials": "AS", "color": "av-teal",  "status": "online",  "phone": "+91 76543 21098"},
    {"name": "Vikram Nair",     "initials": "VN", "color": "av-navy",  "status": "offline", "phone": "+91 65432 10987"},
    {"name": "Deepa Rao",       "initials": "DR", "color": "av-amber", "status": "online",  "phone": "+91 54321 09876"},
]

# ─── TOP NAV ─────────────────────────────────────────────────────────────────
notif_count = len(st.session_state.notifications)
st.markdown(f"""
<div class="topnav">
  <div class="brand">Ride<span>Sync</span></div>
  <div style="display:flex;align-items:center;gap:8px;">
    {'<div class="notif-badge">🔔 ' + str(notif_count) + ' new</div>' if notif_count else ''}
    <div style="width:34px;height:34px;border-radius:50%;background:var(--teal);
                display:flex;align-items:center;justify-content:center;
                color:white;font-weight:700;font-size:14px;">G</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab_home, tab_find, tab_notify, tab_trips, tab_safety, tab_eco = st.tabs([
    "🏠 Home", "🔍 Find Ride", "🔔 Smart Notify", "🗺 My Trips", "🛡 Safety", "🌿 Eco Tracker"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – HOME
# ═══════════════════════════════════════════════════════════════════════════════
with tab_home:
    st.markdown("""
    <div class="hero">
      <div class="hero-tag">✦ AI-Powered Carpooling</div>
      <h1 class="hero-title">Commute Smarter,<br>Together.</h1>
      <p class="hero-sub">RideSync matches you with verified co-travellers on your exact route — saving money, cutting traffic, and helping the planet.</p>
      <div style="margin-top:24px;">
        <span class="stat-pill"><span class="dot"></span> 247 rides active now</span>
        <span class="stat-pill">🌿 1.2 tonnes CO₂ saved today</span>
        <span class="stat-pill">⭐ 4.8 avg rating</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-pad">', unsafe_allow_html=True)

    # Quick Search
    st.markdown('<p class="section-head">Quick Ride Search</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Find a ride or offer seats on your route</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        st.text_input("📍 From", placeholder="e.g. Hinjewadi Phase 1", key="home_from")
    with col2:
        st.text_input("🎯 To", placeholder="e.g. Baner, Pune", key="home_to")
    with col3:
        st.selectbox("👥 Seats", [1, 2, 3, 4], key="home_seats")
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Search Rides", type="primary", use_container_width=True):
            st.toast("🔍 Searching for matching rides...", icon="🚗")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Upcoming confirmed ride
    st.markdown('<p class="section-head">Your Next Ride</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ride-card">
      <div class="card-header">
        <div style="display:flex;align-items:center;gap:10px;">
          <div class="avatar av-teal">AP</div>
          <div>
            <div style="font-weight:600;font-size:15px;font-family:'Space Grotesk',sans-serif;">Arjun Patel</div>
            <div style="font-size:12px;color:var(--muted);">Today · 8:45 AM</div>
          </div>
        </div>
        <span class="badge badge-confirmed">✓ Confirmed</span>
      </div>
      <div style="display:flex;flex-direction:column;gap:2px;margin:12px 0 16px;">
        <div class="ride-route">
          <span class="route-dot-black"></span>
          <span style="font-size:14px;font-weight:500;">Hinjewadi Phase 1</span>
        </div>
        <div style="width:1px;height:14px;background:var(--border);margin-left:4px;"></div>
        <div class="ride-route">
          <span class="route-dot-blue"></span>
          <span style="font-size:14px;font-weight:500;">Baner, Pune</span>
        </div>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;">
        <div class="avatar-row">
          <div class="avatar av-coral" style="font-size:11px;">SK</div>
          <div class="avatar av-blue"  style="font-size:11px;">+1</div>
        </div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;color:var(--navy);">₹45</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Map placeholder
    st.markdown("""
    <div class="map-block">
      <div class="map-grid"></div>
      <div class="map-label">📍 3 drivers nearby · Route optimized</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Why RideSync
    st.markdown('<p class="section-head">Why RideSync?</p>', unsafe_allow_html=True)
    wc1, wc2, wc3 = st.columns(3)
    for col, icon, title, desc in [
        (wc1, "🛡", "Verified Users", "ID & phone verified members only. Rate every ride for community trust."),
        (wc2, "🤖", "AI Matching",    "Our engine finds riders on your exact route, time, and preferences."),
        (wc3, "🌿", "Go Green",       "Track CO₂ saved per trip. Every carpool removes one car off the road."),
    ]:
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:28px 20px;">
              <div style="font-size:32px;margin-bottom:12px;">{icon}</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:15px;margin-bottom:8px;">{title}</div>
              <div style="font-size:13px;color:var(--muted);line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – FIND A RIDE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_find:
    st.markdown('<div class="content-pad">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">Find Available Rides</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">AI-matched rides along your commute route</p>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([2, 2, 1])
    with col_a:
        search_from = st.text_input("📍 Pickup", placeholder="Hinjewadi, Wakad, Kothrud…", key="find_from")
    with col_b:
        search_to   = st.text_input("🎯 Drop",   placeholder="Baner, FC Road, Hadapsar…",  key="find_to")
    with col_c:
        price_max = st.slider("Max ₹", 20, 150, 80, key="price_slider")

    # Filter chips
    st.markdown("""
    <div style="margin:12px 0 20px;">
      <span class="feature-chip">⚡ Departing Soon</span>
      <span class="feature-chip">❄️ AC Only</span>
      <span class="feature-chip">⭐ 4.5+</span>
      <span class="feature-chip">🔒 Verified Only</span>
      <span class="feature-chip">👩 Female Preferred</span>
    </div>
    """, unsafe_allow_html=True)

    for ride in available_rides:
        stars = "⭐" * int(ride["rating"]) + f" {ride['rating']}"
        tags_html = "".join([f'<span class="badge badge-teal" style="font-size:10px;padding:2px 8px;margin-right:4px;">{t}</span>' for t in ride["tags"]])
        st.markdown(f"""
        <div class="ride-card">
          <div class="card-header">
            <div style="display:flex;align-items:center;gap:10px;">
              <div class="avatar {ride['color']}" style="width:40px;height:40px;font-size:14px;">{ride['initials']}</div>
              <div>
                <div style="font-weight:600;font-size:15px;font-family:'Space Grotesk',sans-serif;">{ride['driver']}</div>
                <div style="font-size:12px;color:var(--muted);">{stars} · ETA {ride['eta']}</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;color:var(--navy);">{ride['price']}</div>
              <div style="font-size:11px;color:var(--muted);">per seat</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;margin:10px 0;">
            <div style="flex:1;">
              <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px;">FROM</div>
              <div style="font-weight:500;font-size:14px;">📍 {ride['from']}</div>
            </div>
            <div style="color:var(--muted);align-self:center;font-size:18px;">→</div>
            <div style="flex:1;">
              <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px;">TO</div>
              <div style="font-weight:500;font-size:14px;">🎯 {ride['to']}</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">
            <div>
              <span style="font-size:12px;color:var(--muted);">🕐 {ride['time']} · {ride['seats']} seat{'s' if ride['seats']>1 else ''} left</span><br>
              <div style="margin-top:6px;">{tags_html}</div>
            </div>
            {'<span class="badge badge-confirmed">✓ ID Verified</span>' if ride['verified'] else ''}
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_r1, col_r2 = st.columns([1, 1])
        with col_r1:
            if st.button(f"Book Seat — {ride['price']}", key=f"book_{ride['driver']}", use_container_width=True, type="primary"):
                st.toast(f"✅ Seat booked with {ride['driver']}! Notification sent.", icon="🚗")
                st.session_state.notifications.append(f"Ride booked with {ride['driver']} at {ride['time']}")
        with col_r2:
            if st.button(f"🔔 Notify & Book", key=f"notif_{ride['driver']}", use_container_width=True):
                st.toast(f"📲 Your contacts notified! Booking {ride['driver']}'s ride.", icon="🔔")
                st.session_state.notifications.append(f"Smart notify sent for {ride['driver']}'s ride at {ride['time']}")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 – 🔔 SMART NOTIFY (UNIQUE FEATURE)
# ═══════════════════════════════════════════════════════════════════════════════
with tab_notify:
    st.markdown('<div class="content-pad">', unsafe_allow_html=True)

    st.markdown("""
    <div class="notify-panel">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;margin-bottom:6px;">
        Smart Departure Notify 🔔
      </div>
      <div style="color:rgba(255,255,255,0.65);font-size:14px;line-height:1.6;max-width:480px;">
        Instantly ping your regular ride group the moment you're leaving. 
        No calls, no WhatsApp threads — one tap sends your ETA, location, and available seats to everyone.
      </div>
      <div style="margin-top:20px;display:flex;flex-wrap:wrap;gap:10px;">
        <div class="notify-feature-row" style="flex:1;min-width:200px;">
          <div class="nf-icon" style="background:rgba(42,155,155,0.3);">📍</div>
          <div>
            <div style="font-weight:600;font-size:13px;">Live Location Share</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.55);">Your real-time location sent automatically</div>
          </div>
        </div>
        <div class="notify-feature-row" style="flex:1;min-width:200px;">
          <div class="nf-icon" style="background:rgba(58,134,255,0.3);">⏱</div>
          <div>
            <div style="font-weight:600;font-size:13px;">Auto ETA Calculation</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.55);">AI computes your arrival time live</div>
          </div>
        </div>
        <div class="notify-feature-row" style="flex:1;min-width:200px;">
          <div class="nf-icon" style="background:rgba(232,83,74,0.3);">🚨</div>
          <div>
            <div style="font-weight:600;font-size:13px;">Delay Alert</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.55);">Auto re-notifies if you're running late</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Departure Setup ──────────────────────────────────────────────────────
    st.markdown('<p class="section-head">Set Your Departure</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Configure who gets notified and when</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        depart_from  = st.text_input("📍 Leaving from", placeholder="Your current location", key="dep_from")
        depart_seats = st.slider("🪑 Empty seats in your car", 1, 4, 2)
    with col2:
        depart_dest = st.text_input("🎯 Going to", placeholder="Office, college, etc.", key="dep_to")
        depart_time = st.time_input("🕐 Planned departure time", value=datetime.now().replace(hour=8, minute=45).time())

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Contact Selector ─────────────────────────────────────────────────────
    st.markdown('<p class="section-head">Who to Notify?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Choose from your regular ride group</p>', unsafe_allow_html=True)

    selected_contacts = []
    for c in contacts:
        status_color = "#22C55E" if c["status"] == "online" else "#CBD5E1"
        col_chk, col_info = st.columns([1, 6])
        with col_chk:
            checked = st.checkbox("", key=f"chk_{c['name']}", value=(c["name"] in st.session_state.notify_contacts))
        with col_info:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:6px 0;">
              <div style="position:relative;">
                <div class="avatar {c['color']}" style="width:38px;height:38px;font-size:13px;">{c['initials']}</div>
                <div style="position:absolute;bottom:1px;right:1px;width:9px;height:9px;border-radius:50%;
                            background:{status_color};border:2px solid white;"></div>
              </div>
              <div>
                <div style="font-weight:600;font-size:14px;">{c['name']}</div>
                <div style="font-size:12px;color:var(--muted);">{c['phone']} · {"🟢 Online" if c['status']=="online" else "⚫ Offline"}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        if checked:
            selected_contacts.append(c["name"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Notification Options ─────────────────────────────────────────────────
    st.markdown('<p class="section-head">Notification Settings</p>', unsafe_allow_html=True)

    nc1, nc2 = st.columns(2)
    with nc1:
        auto_remind   = st.toggle("⏰ Auto-remind 15 min before departure", value=True)
        share_loc     = st.toggle("📍 Share live location with group", value=True)
    with nc2:
        delay_alert   = st.toggle("🚨 Auto-alert if delayed >10 min", value=True)
        whatsapp_fwd  = st.toggle("💬 Also forward to WhatsApp group", value=False)

    msg_template = st.text_area(
        "📝 Notification message (auto-filled, editable)",
        value=f"Hey! 👋 I'm leaving for {depart_dest or 'office'} at {depart_time.strftime('%I:%M %p')} from {depart_from or 'my location'}. I have {depart_seats} seat(s) available. Reply or tap below to join my ride on RideSync! 🚗",
        height=100
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_send, col_sched = st.columns(2)
    with col_send:
        if st.button("🔔 Notify Now — Send to All", type="primary", use_container_width=True):
            if selected_contacts:
                with st.spinner("Sending notifications..."):
                    time.sleep(1.2)
                names = ", ".join(selected_contacts[:2]) + (f" +{len(selected_contacts)-2} more" if len(selected_contacts) > 2 else "")
                st.markdown(f"""
                <div class="alert-box">
                  ✅ Notifications sent to <strong>{names}</strong>! 
                  They can see your live location and available seats.
                </div>
                """, unsafe_allow_html=True)
                st.session_state.smart_notify_sent = True
                for c in selected_contacts:
                    st.session_state.notifications.append(f"Departure notify sent to {c}")
                st.balloons()
            else:
                st.markdown('<div class="alert-box-warn">⚠️ Please select at least one contact to notify.</div>', unsafe_allow_html=True)

    with col_sched:
        if st.button("⏰ Schedule Notify (at departure time)", use_container_width=True):
            st.markdown(f"""
            <div class="alert-box">
              ✅ Scheduled! Notification will auto-send at <strong>{depart_time.strftime('%I:%M %p')}</strong> to your selected contacts.
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.smart_notify_sent:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="border:1.5px solid var(--green);background:var(--green-lt);">
          <div style="font-weight:600;font-size:15px;color:#166534;margin-bottom:12px;">📲 Notification Status</div>
        """, unsafe_allow_html=True)
        for c in contacts[:3]:
            resp = random.choice(["✅ Joining!", "👀 Seen", "⏳ Pending…"])
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(0,0,0,0.06);">
              <div style="display:flex;align-items:center;gap:8px;">
                <div class="avatar {c['color']}" style="width:28px;height:28px;font-size:11px;">{c['initials']}</div>
                <span style="font-size:13px;font-weight:500;color:var(--navy);">{c['name']}</span>
              </div>
              <span style="font-size:13px;font-weight:600;color:#166534;">{resp}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 – MY TRIPS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_trips:
    st.markdown('<div class="content-pad">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">My Trips</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Your ride history and upcoming bookings</p>', unsafe_allow_html=True)

    # Stats row
    sc1, sc2, sc3, sc4 = st.columns(4)
    for col, num, label, chg in [
        (sc1, "23",   "Total Rides",   "+3 this week"),
        (sc2, "₹847", "Total Saved",   "vs solo cabs"),
        (sc3, "4.9",  "Your Rating",   "Top 5% rider"),
        (sc4, "34kg", "CO₂ Avoided",   "🌿 Great job!"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-num">{num}</div>
              <div class="stat-label">{label}</div>
              <div class="stat-change">{chg}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    filter_tab = st.radio("Filter", ["All", "Completed", "Upcoming", "Cancelled"], horizontal=True, label_visibility="collapsed")

    for trip in my_trips:
        if filter_tab == "Completed" and trip["status"] != "completed": continue
        if filter_tab == "Cancelled" and trip["status"] != "cancelled": continue
        if filter_tab == "Upcoming"  and trip["status"] not in ["confirmed"]: continue

        badge_class = {"confirmed": "badge-confirmed", "completed": "badge-confirmed",
                       "cancelled": "badge-cancelled"}.get(trip["status"], "badge-pending")
        badge_label = trip["status"].upper()
        co_html = "".join([f'<div class="avatar av-teal" style="width:26px;height:26px;font-size:10px;">{c}</div>' for c in trip["co_travelers"]])

        st.markdown(f"""
        <div class="ride-card">
          <div class="card-header">
            <div>
              <div style="font-size:12px;color:var(--muted);">📅 {trip['date']} · {trip['time']}</div>
            </div>
            <span class="badge {badge_class}">{badge_label}</span>
          </div>
          <div style="display:flex;flex-direction:column;gap:3px;margin:8px 0 14px;">
            <div class="ride-route"><span class="route-dot-black"></span><span style="font-size:14px;font-weight:500;">{trip['from']}</span></div>
            <div style="width:1px;height:12px;background:var(--border);margin-left:4px;"></div>
            <div class="ride-route"><span class="route-dot-blue"></span><span style="font-size:14px;font-weight:500;">{trip['to']}</span></div>
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <div class="avatar-row">{co_html if co_html else '<span style="font-size:12px;color:var(--muted);">Solo ride</span>'}</div>
            <div style="font-family:\'Space Grotesk\',sans-serif;font-size:20px;font-weight:700;">{trip['price']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 – SAFETY
# ═══════════════════════════════════════════════════════════════════════════════
with tab_safety:
    st.markdown('<div class="content-pad">', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#FFF0EF,#FDECEA);border:1.5px solid #FECACA;
                border-radius:20px;padding:28px;margin-bottom:24px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div style="font-size:40px;">🛡</div>
        <div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;color:var(--coral);">Safety First, Always</div>
          <div style="font-size:14px;color:var(--slate);">Real-time tracking, SOS alerts, and verified profiles for your peace of mind.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown('<p class="section-head">🚨 SOS Alert</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Send emergency alert with live location</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="border:1.5px solid var(--coral);text-align:center;padding:32px;">
          <div style="font-size:48px;margin-bottom:12px;">🆘</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;margin-bottom:8px;color:var(--coral);">Emergency SOS</div>
          <div style="font-size:13px;color:var(--muted);margin-bottom:16px;">Sends location to emergency contacts & RideSync support instantly</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚨 SEND SOS ALERT", use_container_width=True):
            st.error("🚨 SOS SENT! Emergency contacts notified with your live location. Help is on the way.")

    with sc2:
        st.markdown('<p class="section-head">📍 Share Trip</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Let trusted contacts track your ride</p>', unsafe_allow_html=True)
        share_name = st.text_input("Share with (name or phone)", placeholder="+91 98765 43210")
        if st.button("📤 Share Live Trip Link", use_container_width=True, type="primary"):
            st.success("✅ Live trip link sent! They can track your ride in real-time.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">Trusted Contacts</p>', unsafe_allow_html=True)

    for c in contacts[:3]:
        st.markdown(f"""
        <div class="card" style="padding:16px 22px;">
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div class="avatar {c['color']}">{c['initials']}</div>
              <div>
                <div style="font-weight:600;font-size:14px;">{c['name']}</div>
                <div style="font-size:12px;color:var(--muted);">{c['phone']}</div>
              </div>
            </div>
            <span class="badge badge-teal">✓ Trusted</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-head">Safety Features</p>', unsafe_allow_html=True)

    safety_features = [
        ("🔒", "ID Verification",    "All users verified with govt ID + phone number"),
        ("📷", "Photo Match",         "Driver photo shown before ride confirmation"),
        ("🗺",  "Route Deviation Alert","Alert if driver goes off planned route"),
        ("⭐",  "Ratings & Reviews",   "Community-driven trust scores for every user"),
        ("📞",  "In-App Calling",      "Call without sharing your real number"),
        ("🎥",  "Ride Recording",      "Optional audio recording stored for 7 days"),
    ]

    sfc1, sfc2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(safety_features):
        col = sfc1 if i % 2 == 0 else sfc2
        with col:
            st.markdown(f"""
            <div class="card" style="padding:18px;">
              <div style="display:flex;align-items:flex-start;gap:12px;">
                <div style="font-size:24px;">{icon}</div>
                <div>
                  <div style="font-weight:600;font-size:14px;margin-bottom:4px;">{title}</div>
                  <div style="font-size:12px;color:var(--muted);">{desc}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 – ECO TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
with tab_eco:
    st.markdown('<div class="content-pad">', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,var(--teal),#0F4C4C);border-radius:20px;
                padding:32px;color:white;margin-bottom:24px;">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:26px;font-weight:700;margin-bottom:8px;">🌿 Your Green Impact</div>
      <div style="color:rgba(255,255,255,0.7);font-size:15px;">Every shared ride counts. Here's your contribution to a cleaner planet.</div>
      <div style="margin-top:24px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
        <div style="background:rgba(255,255,255,0.1);border-radius:14px;padding:18px;text-align:center;">
          <div style="font-size:32px;font-weight:700;font-family:'Space Grotesk',sans-serif;">34.2</div>
          <div style="font-size:12px;opacity:0.7;margin-top:4px;">kg CO₂ Saved</div>
        </div>
        <div style="background:rgba(255,255,255,0.1);border-radius:14px;padding:18px;text-align:center;">
          <div style="font-size:32px;font-weight:700;font-family:'Space Grotesk',sans-serif;">₹1,240</div>
          <div style="font-size:12px;opacity:0.7;margin-top:4px;">Fuel Saved</div>
        </div>
        <div style="background:rgba(255,255,255,0.1);border-radius:14px;padding:18px;text-align:center;">
          <div style="font-size:32px;font-weight:700;font-family:'Space Grotesk',sans-serif;">3.4 🌳</div>
          <div style="font-size:12px;opacity:0.7;margin-top:4px;">Trees Equivalent</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-head">Monthly CO₂ Progress</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Your goal: Save 50kg CO₂ this month</p>', unsafe_allow_html=True)

    pct = int((34.2 / 50) * 100)
    st.markdown(f"""
    <div class="card">
      <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
        <span style="font-weight:600;font-size:14px;">34.2 kg saved</span>
        <span style="font-size:14px;color:var(--muted);">Goal: 50 kg</span>
      </div>
      <div class="co2-bar-bg"><div class="co2-bar-fill" style="width:{pct}%;"></div></div>
      <div style="font-size:12px;color:var(--teal);margin-top:6px;font-weight:600;">{pct}% of monthly goal · 15.8 kg to go! 🌿</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-head">This Week — Trip Breakdown</p>', unsafe_allow_html=True)

    weekly = [
        ("Mon", 6.2, "Hinjewadi → Baner"),
        ("Tue", 0,   "No ride"),
        ("Wed", 5.8, "Wakad → FC Road"),
        ("Thu", 7.1, "Kothrud → Hadapsar"),
        ("Fri", 4.4, "Aundh → Viman Nagar"),
    ]
    for day, co2, route in weekly:
        bar_w = int((co2 / 10) * 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
          <div style="width:36px;font-size:12px;font-weight:600;color:var(--muted);">{day}</div>
          <div style="flex:1;">
            <div class="co2-bar-bg" style="height:10px;">
              <div class="co2-bar-fill" style="width:{bar_w}%;height:10px;"></div>
            </div>
          </div>
          <div style="width:80px;font-size:12px;font-weight:600;color:var(--teal);text-align:right;">
            {"🌿 " + str(co2) + " kg" if co2 else "—"}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Badges
    st.markdown('<p class="section-head">🏆 Your Eco Badges</p>', unsafe_allow_html=True)
    badges = [
        ("🌱", "First Green Ride",  "Completed your first shared ride"),
        ("🔥", "10-Ride Streak",    "10 consecutive days of carpooling"),
        ("🌍", "Carbon Crusher",    "Saved 25kg+ CO₂ in a month"),
        ("🌳", "Tree Planter",      "Your savings = 3 trees planted"),
    ]
    bc1, bc2 = st.columns(2)
    for i, (icon, name, desc) in enumerate(badges):
        col = bc1 if i % 2 == 0 else bc2
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:22px 16px;">
              <div style="font-size:36px;margin-bottom:8px;">{icon}</div>
              <div style="font-weight:700;font-size:14px;font-family:'Space Grotesk',sans-serif;">{name}</div>
              <div style="font-size:12px;color:var(--muted);margin-top:4px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:var(--navy);color:rgba(255,255,255,0.5);text-align:center;
            padding:20px;font-size:12px;margin-top:40px;">
  RideSync © 2026 · Smart Ride Sharing Platform · Built for commuters, by commuters 🚗
</div>
""", unsafe_allow_html=True)
