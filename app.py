import hashlib
import hmac
import io
import json
import math
import secrets
import time
from datetime import datetime, timedelta
from pathlib import Path

import extra_streamlit_components as stx
import pandas as pd
import pydeck as pdk
import streamlit as st
from PIL import ExifTags, Image

import model

# data.py is optional. The app includes a built-in NER dataset fallback so
# an older data.py cannot crash the dashboard.
try:
    import data
except Exception:
    data = None


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="NER Suraksha | Landslide Early Warning",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* ========================================================
       GLOBAL DESIGN
       ======================================================== */
    .stApp {
        background:
            radial-gradient(circle at 0% 0%, rgba(22, 163, 74, .08), transparent 28%),
            radial-gradient(circle at 100% 0%, rgba(14, 116, 144, .10), transparent 30%),
            linear-gradient(180deg, #f8fbfd 0%, #eef5f7 100%);
        color: #172033;
    }

    .block-container {
        max-width: 1420px;
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
    }

    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stCaption {
        color: #172033;
    }

    /* ========================================================
       LOGIN / LANDING PAGE
       ======================================================== */
    .landing-brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 0 0 4px 0;
    }

    .brand-icon {
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        background: linear-gradient(145deg, #0f766e, #155e75);
        box-shadow: 0 10px 24px rgba(15, 118, 110, .20);
        font-size: 28px;
    }

    .brand-name {
        font-size: 2.45rem;
        font-weight: 850;
        letter-spacing: -0.055em;
        color: #10213a;
        line-height: 1;
    }

    .brand-subtitle {
        margin: 8px 0 22px 68px;
        color: #58708a;
        font-size: 1rem;
        line-height: 1.5;
    }

    .feature-panel {
        min-height: 455px;
        padding: 30px;
        border-radius: 26px;
        background: linear-gradient(145deg, #0b486b 0%, #0f766e 58%, #147d92 100%);
        color: white;
        box-shadow: 0 18px 45px rgba(15, 76, 100, .18);
        position: relative;
        overflow: hidden;
    }

    .feature-panel:after {
        content: '';
        position: absolute;
        width: 220px;
        height: 220px;
        right: -80px;
        top: -70px;
        border-radius: 50%;
        background: rgba(255,255,255,.08);
    }

    .feature-kicker {
        font-size: .76rem;
        text-transform: uppercase;
        letter-spacing: .12em;
        font-weight: 800;
        opacity: .78;
        margin-bottom: 10px;
    }

    .feature-title {
        color: white !important;
        font-size: 1.9rem;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 10px;
    }

    .feature-copy {
        color: rgba(255,255,255,.86) !important;
        font-size: .96rem;
        line-height: 1.65;
        margin-bottom: 22px;
    }

    .flow {
        display: grid;
        gap: 9px;
        margin-top: 14px;
    }

    .flow-item {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 10px 12px;
        border-radius: 13px;
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.10);
        color: white;
        font-size: .88rem;
        font-weight: 650;
    }

    .flow-dot {
        width: 28px;
        height: 28px;
        flex: 0 0 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        background: rgba(255,255,255,.16);
        font-size: .86rem;
    }

    .capability-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 20px;
    }

    .capability {
        padding: 7px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,.11);
        border: 1px solid rgba(255,255,255,.10);
        color: rgba(255,255,255,.94);
        font-size: .76rem;
        font-weight: 650;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,.97) !important;
        border: 1px solid #dbe7ec !important;
        border-radius: 26px !important;
        box-shadow: 0 18px 45px rgba(15,23,42,.08);
        padding: 10px 14px 12px 14px;
    }

    .auth-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: #132238;
        margin-bottom: 4px;
    }

    .auth-subtitle {
        color: #718399;
        font-size: .88rem;
        margin-bottom: 16px;
    }

    .auth-badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: #ecfdf5;
        color: #047857;
        font-size: .72rem;
        font-weight: 800;
        margin-bottom: 15px;
    }

    /* Streamlit tabs */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 5px;
        border-bottom: 1px solid #e2e8f0;
    }

    [data-testid="stTabs"] button[role="tab"] {
        color: #66758a !important;
        font-weight: 700;
        font-size: .84rem;
        padding: 10px 9px;
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #0f766e !important;
    }

    /* Labels and helper text */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stCheckbox"] label {
        color: #34465c !important;
        font-weight: 650 !important;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        color: #172033 !important;
        background: #f8fafc !important;
        border: 1px solid #cbd8e2 !important;
        border-radius: 12px !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #0f766e !important;
        box-shadow: 0 0 0 2px rgba(15,118,110,.12) !important;
    }

    [data-testid="stCheckbox"] label p {
        color: #5b6d80 !important;
    }

    .stButton > button {
        border-radius: 12px !important;
        min-height: 2.75rem;
        font-weight: 750 !important;
        border: 1px solid #d3dee6;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0f766e, #0b6073) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 8px 18px rgba(15,118,110,.20);
    }

    .login-note {
        text-align: center;
        color: #7a8999;
        font-size: .75rem;
        margin-top: 16px;
    }

    /* ========================================================
       DASHBOARD
       ======================================================== */
    .hero {
        padding: 1.65rem 1.8rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #0b486b 0%, #0f766e 58%, #147d92 100%);
        color: white;
        box-shadow: 0 14px 40px rgba(15, 118, 110, .18);
        margin: .35rem 0 1.25rem;
    }

    .hero-title {
        color: white !important;
        margin: 0;
        font-size: 2.15rem;
        font-weight: 850;
        letter-spacing: -0.03em;
        line-height: 1.15;
    }

    .hero-subtitle {
        color: rgba(255,255,255,.93) !important;
        margin: .4rem 0 0;
        font-size: 1.02rem;
        font-weight: 550;
    }

    .hero-location, .hero-pill {
        color: white !important;
        display: inline-block;
        margin-top: .9rem;
        padding: .42rem .8rem;
        border-radius: 999px;
        background: rgba(255,255,255,.13);
        border: 1px solid rgba(255,255,255,.15);
        font-size: .82rem;
        font-weight: 650;
    }

    .hero-pill { margin-top: .55rem; background: rgba(255,255,255,.09); font-size: .78rem; }

    .status-card {
        padding: 1rem 1.05rem;
        border-radius: 18px;
        background: white;
        border: 1px solid #dbe5ea;
        box-shadow: 0 6px 22px rgba(15,23,42,.05);
    }

    .status-card .label { color:#64748b; font-size:.76rem; text-transform:uppercase; letter-spacing:.06em; }
    .status-card .value { color:#0f172a; font-size:1.1rem; font-weight:800; margin-top:.15rem; }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #dbe5ea;
        padding: .9rem;
        border-radius: 17px;
        box-shadow: 0 5px 18px rgba(15,23,42,.045);
    }

    [data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #dbe5ea;
    }

    [data-testid="stSidebar"] * {
        color: #26384d;
    }

    [data-testid="stFileUploader"] { border-radius: 16px; }
    .small-note { font-size:.82rem; color:#64748b; }

    /* ========================================================
       LOGIN READABILITY / DARK THEME RESISTANCE
       ======================================================== */
    .auth-title, .auth-subtitle, .auth-badge, .login-note {
        color: #172033 !important;
    }

    .feature-title, .feature-copy, .feature-kicker, .flow-item, .capability {
        color: #ffffff !important;
    }

    [data-testid="stTextInput"] label,
    [data-testid="stTextInput"] p,
    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p {
        color: #26384d !important;
    }

    [data-testid="stTextInput"] input {
        background: #ffffff !important;
        color: #172033 !important;
        border: 1px solid #cbd5e1 !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #94a3b8 !important;
    }

    /* Mobile */
    @media (max-width: 900px) {
        .brand-name { font-size: 2rem; }
        .brand-subtitle { margin-left: 0; }
        .feature-panel { min-height: auto; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# JSON AUTHENTICATION - NO SQL
# ============================================================

USERS_FILE = Path("ner_suraksha_users.json")
AUTH_COOKIE = "ner_suraksha_auth"
COOKIE_DAYS = 30


# ============================================================
# BUILT-IN NER LOCATION DATA
# ============================================================
# This fallback keeps app.py working even if data.py is older or
# missing get_zones(). It also provides relief-centre destinations.
NER_LOCATIONS = {
    "Arunachal Pradesh": [
        {"zone":"Tawang","lat":27.5860,"lon":91.8590,"population":11000,"road_status":"Caution","shelter":"Tawang Relief Centre","base_risk":0.72},
        {"zone":"Itanagar","lat":27.0844,"lon":93.6053,"population":59000,"road_status":"Open","shelter":"Itanagar Community Hall","base_risk":0.44},
        {"zone":"Bomdila","lat":27.2646,"lon":92.4245,"population":8500,"road_status":"Caution","shelter":"Bomdila Relief Centre","base_risk":0.67},
    ],
    "Assam": [
        {"zone":"Guwahati Hills","lat":26.1445,"lon":91.7362,"population":120000,"road_status":"Caution","shelter":"Guwahati Emergency Shelter","base_risk":0.48},
        {"zone":"Dima Hasao","lat":25.3478,"lon":93.0176,"population":22000,"road_status":"Caution","shelter":"Haflong Relief Centre","base_risk":0.64},
        {"zone":"Karbi Anglong","lat":26.0200,"lon":93.4500,"population":31000,"road_status":"Open","shelter":"Diphu Community Hall","base_risk":0.55},
    ],
    "Manipur": [
        {"zone":"Imphal East Hills","lat":24.8170,"lon":93.9368,"population":46000,"road_status":"Caution","shelter":"Imphal East Relief Centre","base_risk":0.62},
        {"zone":"Senapati","lat":25.2670,"lon":94.0200,"population":15000,"road_status":"Caution","shelter":"Senapati Relief Centre","base_risk":0.70},
        {"zone":"Churachandpur","lat":24.3333,"lon":93.6833,"population":28000,"road_status":"Open","shelter":"Churachandpur Community Hall","base_risk":0.52},
    ],
    "Meghalaya": [
        {"zone":"Shillong Hills","lat":25.5788,"lon":91.8933,"population":143000,"road_status":"Caution","shelter":"Shillong Emergency Shelter","base_risk":0.60},
        {"zone":"Cherrapunji","lat":25.2840,"lon":91.7210,"population":12000,"road_status":"Caution","shelter":"Sohra Relief Centre","base_risk":0.78},
        {"zone":"Jowai","lat":25.4500,"lon":92.2000,"population":18000,"road_status":"Open","shelter":"Jowai Community Hall","base_risk":0.49},
    ],
    "Mizoram": [
        {"zone":"Aizawl Hills","lat":23.7271,"lon":92.7176,"population":98000,"road_status":"Caution","shelter":"Aizawl Relief Centre","base_risk":0.68},
        {"zone":"Lunglei","lat":22.8900,"lon":92.7500,"population":24000,"road_status":"Caution","shelter":"Lunglei Relief Centre","base_risk":0.74},
        {"zone":"Champhai","lat":23.4670,"lon":93.3260,"population":16000,"road_status":"Open","shelter":"Champhai Community Hall","base_risk":0.51},
    ],
    "Nagaland": [
        {"zone":"Kohima Hills","lat":25.6751,"lon":94.1086,"population":41000,"road_status":"Caution","shelter":"Kohima Relief Centre","base_risk":0.65},
        {"zone":"Mokokchung","lat":26.3300,"lon":94.5300,"population":17000,"road_status":"Open","shelter":"Mokokchung Community Hall","base_risk":0.46},
        {"zone":"Dimapur Hills","lat":25.9000,"lon":93.7300,"population":30000,"road_status":"Caution","shelter":"Dimapur Relief Centre","base_risk":0.58},
    ],
    "Sikkim": [
        {"zone":"Gangtok Hills","lat":27.3389,"lon":88.6065,"population":100000,"road_status":"Caution","shelter":"Gangtok Emergency Shelter","base_risk":0.70},
        {"zone":"Mangan","lat":27.5000,"lon":88.5300,"population":14000,"road_status":"Caution","shelter":"Mangan Relief Centre","base_risk":0.82},
        {"zone":"Namchi","lat":27.1667,"lon":88.3500,"population":13000,"road_status":"Open","shelter":"Namchi Community Hall","base_risk":0.49},
    ],
    "Tripura": [
        {"zone":"Agartala Fringe","lat":23.8315,"lon":91.2868,"population":70000,"road_status":"Open","shelter":"Agartala Community Hall","base_risk":0.39},
        {"zone":"Jampui Hills","lat":24.0800,"lon":92.2500,"population":9000,"road_status":"Caution","shelter":"Jampui Relief Centre","base_risk":0.61},
        {"zone":"Dhalai","lat":24.0500,"lon":91.8500,"population":12000,"road_status":"Open","shelter":"Dhalai Community Hall","base_risk":0.45},
    ],
}


def get_states_safe():
    if data is not None and hasattr(data, "get_states"):
        try:
            states = data.get_states()
            if states:
                return states
        except Exception:
            pass
    return list(NER_LOCATIONS.keys())


def get_zones_safe(state):
    if data is not None and hasattr(data, "get_zones"):
        try:
            zones = data.get_zones(state)
            if zones:
                return zones
        except Exception:
            pass
    return [dict(z) for z in NER_LOCATIONS.get(state, [])]


def load_users():
    if not USERS_FILE.exists():
        return {"__sessions__": {}}
    try:
        with USERS_FILE.open("r", encoding="utf-8") as f:
            users = json.load(f)
        users.setdefault("__sessions__", {})
        return users
    except Exception:
        return {"__sessions__": {}}


def save_users(users):
    tmp = USERS_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    tmp.replace(USERS_FILE)


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 120_000
    ).hex()
    return salt, digest


def password_ok(password, salt, stored_hash):
    _, digest = hash_password(password, salt)
    return hmac.compare_digest(digest, stored_hash)


def valid_username(username):
    username = username.strip()
    if username == "__sessions__":
        return False
    return (
        3 <= len(username) <= 30
        and all(ch.isalnum() or ch in "._-" for ch in username)
    )


def find_user(identifier):
    identifier = identifier.strip().lower()
    users = load_users()
    for username, user in users.items():
        if username == "__sessions__":
            continue
        if username.lower() == identifier or user.get("email", "").lower() == identifier:
            return username, user
    return None, None


def register_user(name, email, username, password):
    users = load_users()
    username = username.strip()
    email = email.strip().lower()

    if not name.strip() or not email or not valid_username(username):
        return False, "Enter a valid name, email and username.", None
    if len(password) < 8:
        return False, "Password must contain at least 8 characters.", None
    if username in users:
        return False, "Username already exists.", None
    if any(u.get("email", "").lower() == email for u in users.values() if isinstance(u, dict)):
        return False, "An account with that email already exists.", None

    salt, password_hash = hash_password(password)
    recovery_code = secrets.token_urlsafe(9)
    recovery_salt, recovery_hash = hash_password(recovery_code)

    users[username] = {
        "name": name.strip(),
        "email": email,
        "password_hash": password_hash,
        "password_salt": salt,
        "recovery_hash": recovery_hash,
        "recovery_salt": recovery_salt,
        "created_at": datetime.now().isoformat(),
    }
    save_users(users)
    return True, "Account created successfully.", recovery_code


def login_user(identifier, password):
    username, user = find_user(identifier)
    if not user:
        return False, None
    if password_ok(password, user["password_salt"], user["password_hash"]):
        return True, username
    return False, None


def create_session(username):
    users = load_users()
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    users["__sessions__"][token_hash] = {
        "username": username,
        "expires": (datetime.now() + timedelta(days=COOKIE_DAYS)).isoformat(),
    }
    save_users(users)
    return token


def restore_session(cookie_manager):
    try:
        token = cookie_manager.get(AUTH_COOKIE)
    except Exception:
        token = None
    if not token:
        return None

    token_hash = hashlib.sha256(token.encode()).hexdigest()
    users = load_users()
    session = users.get("__sessions__", {}).get(token_hash)
    if not session:
        return None

    try:
        expires = datetime.fromisoformat(session["expires"])
    except Exception:
        return None

    if datetime.now() >= expires:
        users["__sessions__"].pop(token_hash, None)
        save_users(users)
        return None
    return session["username"]


def logout(cookie_manager):
    try:
        token = cookie_manager.get(AUTH_COOKIE)
    except Exception:
        token = None
    if token:
        users = load_users()
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        users.get("__sessions__", {}).pop(token_hash, None)
        save_users(users)
    try:
        cookie_manager.delete(AUTH_COOKIE)
    except Exception:
        pass
    st.session_state.logged_in = False
    st.session_state.username = None


def change_password(username, old_password, new_password):
    users = load_users()
    user = users.get(username)
    if not user or not password_ok(old_password, user["password_salt"], user["password_hash"]):
        return False, "Current password is incorrect."
    if len(new_password) < 8:
        return False, "New password must contain at least 8 characters."
    salt, password_hash = hash_password(new_password)
    user["password_salt"] = salt
    user["password_hash"] = password_hash
    save_users(users)
    return True, "Password changed successfully."


def reset_password(identifier, recovery_code, new_password):
    username, user = find_user(identifier)
    if not user:
        return False, "Account not found."
    if len(new_password) < 8:
        return False, "New password must contain at least 8 characters."
    if user.get("recovery_hash") == "used" or user.get("recovery_salt") == "used":
        return False, "The recovery code has already been used. Please use another recovery method."
    if not password_ok(recovery_code.strip(), user["recovery_salt"], user["recovery_hash"]):
        return False, "Recovery code is incorrect."

    salt, password_hash = hash_password(new_password)
    users = load_users()
    users[username]["password_salt"] = salt
    users[username]["password_hash"] = password_hash
    # Make the recovery code single-use.
    users[username]["recovery_hash"] = "used"
    users[username]["recovery_salt"] = "used"
    save_users(users)
    return True, "Password reset successfully."


cookie_manager = stx.CookieManager(key="ner_cookie_manager")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if not st.session_state.logged_in:
    restored = restore_session(cookie_manager)
    if restored:
        st.session_state.logged_in = True
        st.session_state.username = restored


# ============================================================
# LOGIN SCREEN
# ============================================================

if not st.session_state.logged_in:
    st.markdown(
        """
        <div class="landing-brand">
            <div class="brand-icon">🏔️</div>
            <div class="brand-name">NER Suraksha</div>
        </div>
        <div class="brand-subtitle">
            AI-assisted landslide early warning and emergency monitoring platform for North Eastern India
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.08, 0.92], gap="large")

    with left:
        st.markdown(
            """
            <div class="feature-panel">
                <div class="feature-kicker">NORTH EAST INDIA • SAFETY INTELLIGENCE</div>
                <div class="feature-title">Monitor risk.<br>Prepare early. Protect communities.</div>
                <div class="feature-copy">
                    NER Suraksha combines environmental indicators, machine-learning risk scoring,
                    vulnerability mapping and citizen reports in one simple monitoring workspace.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        flow_items = [
            ("01", "Secure Login"),
            ("02", "Collect rainfall, terrain & soil data"),
            ("03", "Process signals with ML"),
            ("04", "Detect risk & identify priority zones"),
            ("05", "Monitor, alert & support response"),
        ]

        for number, text in flow_items:
            st.markdown(
                f"""
                <div class=\"native-flow-item\">
                    <span class=\"native-flow-dot\">{number}</span>
                    <span>{text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="capability-title">CORE CAPABILITIES</div>
            <div class="native-capabilities">
                <span>🌧️ Rainfall</span>
                <span>⛰️ Terrain</span>
                <span>🤖 ML Risk</span>
                <span>🗺️ GIS</span>
                <span>🚨 Alerts</span>
                <span>📷 Field Reports</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        with st.container(border=True):
            st.markdown(
                '<div class="auth-badge">🔒 SECURE PROTOTYPE ACCESS</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="auth-title">Welcome to NER Suraksha</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="auth-subtitle">Sign in to open the landslide monitoring command centre.</div>',
                unsafe_allow_html=True,
            )

            tab_login, tab_create, tab_forgot = st.tabs(
                ["Sign In", "Create Account", "Reset Password"]
            )

            with tab_login:
                identifier = st.text_input(
                    "Username or Email",
                    placeholder="Enter username or email",
                    key="login_identifier",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password",
                )
                remember = st.checkbox(
                    "Keep me signed in for 30 days",
                    value=True,
                )

                if st.button("🔐  Sign In", type="primary", use_container_width=True):
                    if not identifier.strip() or not password:
                        st.warning("Please enter your username/email and password.")
                    else:
                        ok, username = login_user(identifier, password)
                        if ok:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            if remember:
                                token = create_session(username)
                                cookie_manager.set(
                                    AUTH_COOKIE,
                                    token,
                                    expires_at=datetime.now() + timedelta(days=COOKIE_DAYS),
                                    max_age=COOKIE_DAYS * 24 * 60 * 60,
                                    path="/",
                                    same_site="lax",
                                )
                            st.rerun()
                        else:
                            st.error("Invalid username/email or password.")

                st.markdown(
                    '<div class="login-note">Your password is stored as a secure hash. Never share your password or recovery code.</div>',
                    unsafe_allow_html=True,
                )

            with tab_create:
                name = st.text_input(
                    "Full Name", placeholder="Your name", key="create_name"
                )
                email = st.text_input(
                    "Email", placeholder="you@example.com", key="create_email"
                )
                username = st.text_input(
                    "Username", placeholder="Choose a username", key="create_username"
                )
                new_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="At least 8 characters",
                    key="create_password",
                )
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Repeat password",
                    key="create_confirm",
                )

                if st.button("✨  Create Account", use_container_width=True):
                    if new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        ok, message, recovery = register_user(
                            name, email, username, new_password
                        )
                        if ok:
                            st.success(message)
                            st.warning(
                                "Save this recovery code somewhere safe. It is shown only once: "
                                + recovery
                            )
                        else:
                            st.error(message)

            with tab_forgot:
                st.write("Use your one-time recovery code to create a new password.")
                identifier = st.text_input(
                    "Username or Email",
                    placeholder="Enter username or email",
                    key="forgot_identifier",
                )
                recovery = st.text_input(
                    "Recovery Code",
                    placeholder="Enter recovery code",
                    key="forgot_recovery",
                )
                reset_pw = st.text_input(
                    "New Password",
                    type="password",
                    placeholder="At least 8 characters",
                    key="forgot_password",
                )

                if st.button("🔄  Reset Password", use_container_width=True):
                    ok, message = reset_password(identifier, recovery, reset_pw)
                    if ok:
                        st.success(message)
                    else:
                        st.error(message)

    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

current_user = load_users().get(st.session_state.username, {})

with st.sidebar:
    st.markdown("## 👤 Account")
    st.write(current_user.get("name", st.session_state.username))
    st.caption(current_user.get("email", ""))

    if st.button("Logout", use_container_width=True):
        logout(cookie_manager)
        st.rerun()

    with st.expander("Change Password"):
        old_pw = st.text_input("Current password", type="password", key="old_pw")
        new_pw = st.text_input("New password", type="password", key="new_pw")
        if st.button("Update Password", use_container_width=True):
            ok, message = change_password(st.session_state.username, old_pw, new_pw)
            if ok:
                st.success(message)
            else:
                st.error(message)

    st.divider()
    st.markdown("### 🎛️ Monitoring Controls")
    state = st.selectbox("Select State", get_states_safe(), key="state_select")
    zones = get_zones_safe(state)
    selected_zone_name = st.selectbox(
        "Select Location / Zone",
        [z["zone"] for z in zones],
        key="zone_select",
    )

    st.divider()
    st.caption("Prototype mode — use verified official data before operational decisions.")


# ============================================================
# HEADER
# ============================================================

selected_zone = next(z for z in zones if z["zone"] == selected_zone_name)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">🏔️ NER Suraksha</div>
        <div class="hero-subtitle">AI-Powered Landslide Early Warning &amp; Monitoring System</div>
        <div class="hero-location">📍 North Eastern Region of India</div>
        <div class="hero-pill">🛰️ Monitoring: {selected_zone_name}, {state} &nbsp; • &nbsp; Prototype mode</div>
    </div>
    """,
    unsafe_allow_html=True,
)

hc1, hc2, hc3, hc4 = st.columns(4)
with hc1:
    st.markdown('<div class="status-card"><div class="label">Region</div><div class="value">North East India</div></div>', unsafe_allow_html=True)
with hc2:
    st.markdown(f'<div class="status-card"><div class="label">State</div><div class="value">{state}</div></div>', unsafe_allow_html=True)
with hc3:
    st.markdown(f'<div class="status-card"><div class="label">Monitored Zone</div><div class="value">{selected_zone_name}</div></div>', unsafe_allow_html=True)
with hc4:
    st.markdown(f'<div class="status-card"><div class="label">Population</div><div class="value">{selected_zone["population"]:,}</div></div>', unsafe_allow_html=True)

# ============================================================
# SYSTEM FLOW
# ============================================================

with st.expander("🔄 SYSTEM ARCHITECTURE • LIVE WORKFLOW", expanded=False):
    st.markdown(
        "**START → User Login → Collect Data → Data Processing → ML Prediction → "
        "Risk Detection → Low Risk / High Risk → Monitor / Send Alert → Dashboard / Rescue Team → END**"
    )


# ============================================================
# 1. COLLECT DATA
# ============================================================

st.header("1️⃣ Collect Data")

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    rainfall_24h = st.slider("Rainfall — last 24h (mm)", 0, 300, 120, 5)
    rainfall_6h = st.slider("Rainfall — last 6h (mm)", 0, 180, 55, 5)
    forecast_rainfall = st.slider("Forecast rainfall — next 6h (mm)", 0, 220, 70, 5)

with input_col2:
    soil_moisture = st.slider("Soil moisture (%)", 10, 100, 65, 1)
    slope = st.slider("Average slope (degrees)", 5, 55, 30, 1)
    elevation = st.slider("Elevation (m)", 50, 3200, 1200, 50)

with input_col3:
    historical = st.slider("Historical landslide events", 0, 12, 4, 1)
    st.metric("Zone population", f"{selected_zone['population']:,}")
    st.metric("Road status", selected_zone["road_status"])

st.caption("In a production system, these fields can be populated from weather APIs, sensors, GIS, satellite feeds and verified field reports.")


# ============================================================
# 2. DATA PROCESSING + 3. ML PREDICTION
# ============================================================

st.header("2️⃣ Data Processing & 3️⃣ ML Prediction")

features = {
    "rainfall_24h": rainfall_24h,
    "rainfall_6h": rainfall_6h,
    "soil_moisture": soil_moisture,
    "slope": slope,
    "elevation": elevation,
    "historical_landslides": historical,
    "forecast_rainfall_6h": forecast_rainfall,
}

if st.button("🤖 Run ML Risk Prediction", type="primary", use_container_width=True):
    st.session_state.predicted_risk = model.predict_risk(features)
    st.session_state.predicted_zone = selected_zone_name

risk = st.session_state.get("predicted_risk", model.predict_risk(features))
level = model.risk_level(risk)
exposed = model.population_exposure(risk, selected_zone["population"])
priority = model.emergency_priority(risk, selected_zone["population"], selected_zone["road_status"])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Risk", f"{risk}%")
m2.metric("Risk Level", level)
m3.metric("Potentially Exposed", f"{exposed:,}")
m4.metric("Response Priority", model.priority_label(priority))


# ============================================================
# 4. RISK DETECTION
# ============================================================

st.header("4️⃣ Risk Detection")

if level == "CRITICAL":
    st.error(f"🚨 CRITICAL RISK detected in {selected_zone_name}. Immediate official verification and emergency preparedness are recommended.")
elif level == "HIGH":
    st.warning(f"⚠️ HIGH RISK detected in {selected_zone_name}. Authorities should monitor the zone closely and prepare response resources.")
elif level == "MEDIUM":
    st.warning(f"🟡 MEDIUM RISK in {selected_zone_name}. Continue monitoring rainfall, soil and terrain conditions.")
else:
    st.success(f"🟢 LOW RISK in {selected_zone_name}. Continue routine monitoring.")


# ============================================================
# MAP: ALL ZONES + SELECTED LOCATION
# ============================================================

st.header("🗺️ Vulnerability Map")

map_rows = []
for zone in zones:
    zone_features = {
        **features,
        "rainfall_24h": rainfall_24h * (0.75 + zone["base_risk"] * 0.45),
        "rainfall_6h": rainfall_6h * (0.75 + zone["base_risk"] * 0.45),
        "soil_moisture": min(100, soil_moisture * (0.85 + zone["base_risk"] * 0.30)),
        "slope": min(55, slope * (0.80 + zone["base_risk"] * 0.40)),
        "forecast_rainfall_6h": forecast_rainfall * (0.75 + zone["base_risk"] * 0.50),
        "historical_landslides": min(12, historical + int(zone["base_risk"] * 4)),
    }
    zone_risk = model.predict_risk(zone_features)
    zone_level = model.risk_level(zone_risk)
    zone_exposed = model.population_exposure(zone_risk, zone["population"])

    if zone_level == "CRITICAL":
        marker = [180, 0, 0, 220]
    elif zone_level == "HIGH":
        marker = [255, 140, 0, 220]
    elif zone_level == "MEDIUM":
        marker = [240, 200, 0, 220]
    else:
        marker = [0, 160, 70, 220]

    if zone["zone"] == selected_zone_name:
        marker = [40, 110, 255, 255]

    map_rows.append({
        "zone": zone["zone"],
        "lat": zone["lat"],
        "lon": zone["lon"],
        "risk": zone_risk,
        "level": zone_level,
        "population": zone["population"],
        "exposed": zone_exposed,
        "road_status": zone["road_status"],
        "color": marker,
    })

map_df = pd.DataFrame(map_rows)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position="[lon, lat]",
    get_fill_color="color",
    get_radius=9000,
    pickable=True,
    stroked=True,
    filled=True,
    get_line_color=[30, 30, 30],
    line_width_min_pixels=1,
)

view = pdk.ViewState(
    latitude=float(selected_zone["lat"]),
    longitude=float(selected_zone["lon"]),
    zoom=6.2,
    pitch=0,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        tooltip={
            "html": "<b>{zone}</b><br/>Risk: {risk}%<br/>Level: {level}<br/>Population: {population}<br/>Exposed: {exposed}<br/>Road: {road_status}",
            "style": {"backgroundColor": "white", "color": "black"},
        },
        map_style="light",
    ),
    use_container_width=True,
)

st.caption("🔴 Critical  •  🟠 High  •  🟡 Medium  •  🟢 Low  •  🔵 Selected location")


# ============================================================
# 6-HOUR EARLY WARNING
# ============================================================

st.header("⏱️ 6-Hour Early Warning")

future_features = dict(features)
future_features["rainfall_24h"] = rainfall_24h + forecast_rainfall
future_features["rainfall_6h"] = min(180, rainfall_6h + forecast_rainfall * 0.70)
future_features["forecast_rainfall_6h"] = forecast_rainfall

future_risk = model.predict_risk(future_features)
future_level = model.risk_level(future_risk)

f1, f2, f3 = st.columns(3)
f1.metric("Predicted 6h Risk", f"{future_risk}%")
f2.metric("Predicted Level", future_level)
f3.metric("Change", f"{future_risk - risk:+.1f} points")

if future_risk >= 60:
    st.warning("⚠️ The model indicates elevated future risk. Authorities should verify conditions and prepare appropriate preventive action.")
else:
    st.success("🟢 No high-risk signal from the current prototype forecast scenario.")


# ============================================================
# LOW-RISK / HIGH-RISK BRANCH
# ============================================================

st.header("5️⃣ Response Decision")

if level in ["LOW", "MEDIUM"]:
    st.success("🟢 MONITOR MODE")
    st.write("Continue environmental monitoring, update the dashboard and review new citizen/field reports.")

    monitor_df = map_df[["zone", "risk", "level", "population", "exposed", "road_status"]].sort_values("risk", ascending=False)
    st.dataframe(monitor_df, use_container_width=True, hide_index=True)

else:
    st.error("🚨 ALERT MODE")
    st.write("Generate an emergency notification for authorised disaster-management personnel and prioritise the affected zone.")

    alert_text = (
        f"NER SURAKSHA ALERT | {state} | {selected_zone_name} | "
        f"Risk {risk}% ({level}) | Potential exposure {exposed:,} | "
        f"Road status {selected_zone['road_status']}"
    )

    st.code(alert_text)

    if st.button("🚨 Generate Official Alert", type="primary"):
        st.session_state.alert_generated = True

    if st.session_state.get("alert_generated"):
        st.success("Alert prepared for authorised response channels. Connect an approved SMS/app/authority API for real delivery.")


# ============================================================
# RESCUE TEAM / SAFEST ROUTE
# ============================================================

if level in ["HIGH", "CRITICAL"]:
    st.header("🚑 Rescue Team Prioritisation")

    route_candidates = []
    for zone in map_rows:
        if zone["zone"] == selected_zone_name:
            continue
        route_candidates.append({
            "name": f"Via {zone['zone']}",
            "zone": zone["zone"],
            "lat": zone["lat"],
            "lon": zone["lon"],
            "risk": zone["risk"],
            "road_status": zone["road_status"],
            "exposed": zone["exposed"],
            "shelter": next(z["shelter"] for z in zones if z["zone"] == zone["zone"]),
        })

    safest, all_routes = model.find_safest_route(
        route_candidates,
        selected_zone["lat"],
        selected_zone["lon"],
    )

    if safest:
        st.success(
            f"Recommended lower-risk destination: **{safest['shelter']}** via **{safest['name']}**. "
            f"Route score: {safest['safety_score']}/100."
        )
        st.caption("This is a prototype route-ranking result, not live road navigation. Confirm closures and road conditions with authorities.")

    route_df = pd.DataFrame(all_routes)
    if not route_df.empty:
        st.dataframe(
            route_df[["name", "distance_km", "risk", "road_status", "safety_score", "route_status", "shelter"]],
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# CITIZEN IMAGE AUTHENTICITY SCREENING
# ============================================================

def verify_image_authenticity(uploaded_file):
    try:
        raw_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(raw_bytes))
        image.load()

        width, height = image.size
        image_format = image.format or "Unknown"
        file_hash = hashlib.sha256(raw_bytes).hexdigest()

        metadata = []
        try:
            exif = image.getexif()
            for key, value in exif.items():
                metadata.append(f"{ExifTags.TAGS.get(key, str(key))}: {value}")
        except Exception:
            pass

        gray = image.convert("L")
        hist = gray.histogram()
        total = sum(hist)
        mean = sum(i * hist[i] for i in range(256)) / max(total, 1)
        variance = sum(((i - mean) ** 2) * hist[i] for i in range(256)) / max(total, 1)
        variation = math.sqrt(variance)

        score = 70
        warnings = []

        if width >= 200 and height >= 200:
            score += 10
        else:
            score -= 20
            warnings.append("Very small image dimensions.")

        if image_format in ["JPEG", "PNG", "WEBP", "TIFF"]:
            score += 5

        if variation > 8:
            score += 5
        else:
            warnings.append("Very low image variation.")

        if not metadata:
            warnings.append("No EXIF metadata was found; this is not proof of manipulation.")

        aspect = width / max(height, 1)
        if aspect > 5 or aspect < 0.2:
            score -= 10
            warnings.append("Unusual aspect ratio.")

        score = int(max(0, min(100, score)))

        if score >= 75:
            status = "LIKELY AUTHENTIC"
        elif score >= 50:
            status = "POSSIBLY EDITED"
        else:
            status = "HIGH SUSPICION"

        return {
            "score": score,
            "status": status,
            "checks": [
                f"Format: {image_format}",
                f"Dimensions: {width} × {height}",
                f"SHA-256: {file_hash[:16]}...",
                f"EXIF metadata: {'Present' if metadata else 'Not found'}",
                f"Image variation: {variation:.2f}",
            ],
            "warnings": warnings,
            "metadata": metadata,
        }
    except Exception as exc:
        return {"score": 0, "status": "INVALID", "checks": [], "warnings": [str(exc)], "metadata": []}


st.header("📷 Citizen / Field Image Verification")
st.write("Screen uploaded field photographs for basic technical signs that may require manual verification.")

uploaded = st.file_uploader(
    "Upload a landslide or field photograph",
    type=["jpg", "jpeg", "png", "webp", "tif", "tiff"],
    key="citizen_image",
)

if uploaded:
    c1, c2 = st.columns(2)
    with c1:
        st.image(uploaded, caption="Citizen / Field Report", use_container_width=True)
    with c2:
        if st.button("🔍 Verify Image", type="primary", use_container_width=True):
            st.session_state.image_result = verify_image_authenticity(uploaded)

    result = st.session_state.get("image_result")
    if result:
        a, b, c = st.columns(3)
        a.metric("Screening Score", f"{result['score']}%")
        b.metric("Status", result["status"])
        c.metric("Checks", len(result["checks"]))

        if result["status"] == "LIKELY AUTHENTIC":
            st.success("✅ Image passes the available technical screening checks.")
        elif result["status"] == "POSSIBLY EDITED":
            st.warning("⚠️ Some technical indicators require additional verification.")
        else:
            st.error("🚨 High-suspicion technical indicators detected. Manually verify before using the report operationally.")

        for check in result["checks"]:
            st.write("✓ " + check)
        for warning in result["warnings"]:
            st.warning(warning)

        if result["metadata"]:
            with st.expander("View metadata"):
                for item in result["metadata"]:
                    st.write(item)

        st.info("This screening does not prove that an image is real or fake. A validated forensic/AI model is required for stronger automated detection.")


# ============================================================
# CITIZEN HAZARD REPORT
# ============================================================

st.header("📝 Citizen Hazard Report")

with st.form("hazard_report"):
    report_type = st.selectbox("Hazard Type", ["Landslide", "Road Blockage", "Rockfall", "Heavy Rainfall", "Other"])
    description = st.text_area("Description")
    submitted = st.form_submit_button("Submit Report")

if submitted:
    st.success(f"✅ {report_type} report submitted for verification in {selected_zone_name}.")
    if description.strip():
        st.write("Report summary:", description)


# ============================================================
# END / ABOUT
# ============================================================

st.divider()
st.success("END — Monitoring workflow completed for the selected location.")

with st.expander("ℹ️ About this prototype"):
    st.write(
        "NER Suraksha demonstrates the requested workflow: user login, data collection, "
        "data processing, ML prediction, risk detection, low-risk monitoring, high-risk alerts, "
        "rescue prioritisation, GIS visualisation and citizen image screening. The ML model uses "
        "synthetic training data for demonstration; real deployment requires validated historical "
        "landslide data, official weather/sensor feeds, GIS road networks, satellite data and "
        "authorised emergency communication channels."
    )

st.caption("⛰️ NER Suraksha | AI Landslide Early Warning Prototype | No SQL database")

if st.session_state.get("live_mode", False):
    time.sleep(10)
    st.rerun()
