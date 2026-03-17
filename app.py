import streamlit as st
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).with_name("app.db")

st.set_page_config(
    page_title="QuietMind",
    page_icon="🫶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #f4f6f7;
        --card: #ffffff;
        --card-soft: #f8fafb;
        --text: #17232d;
        --muted: #61707c;
        --line: #d9e1e6;
        --accent: #314c63;
        --accent-soft: #ecf1f5;
        --sage: #708c7a;
        --safe-bg: #fff4f4;
        --safe-line: #efcaca;
        --green-bg: #eef7ef;
        --green-text: #28533a;
        --yellow-bg: #fff7df;
        --yellow-text: #8a5c00;
        --orange-bg: #fff0e2;
        --orange-text: #975116;
        --red-bg: #fdecec;
        --red-text: #8e3535;
        --shadow: 0 6px 20px rgba(23, 35, 45, 0.05);
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 760px;
        padding-top: 1rem;
        padding-bottom: 5rem;
    }

    html, body, [class*="css"], p, div, span, label, li, input, textarea, select {
        color: var(--text) !important;
        font-size: 16px !important;
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.01em;
    }

    .stCaption, small {
        color: var(--muted) !important;
    }

    .qm-brand {
        font-size: 30px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .qm-page-intro {
        color: var(--muted);
        margin-top: -4px;
        margin-bottom: 16px;
        line-height: 1.5;
    }

    .qm-hero {
        background: linear-gradient(180deg, #ffffff 0%, #f7f9fb 100%);
        border: 1px solid var(--line);
        border-radius: 28px;
        padding: 26px 22px;
        margin: 8px 0 18px 0;
        box-shadow: var(--shadow);
    }

    .qm-hero-kicker {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent) !important;
        font-size: 13px !important;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .qm-hero-title {
        font-size: 34px;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.15;
    }

    .qm-hero-sub {
        color: var(--muted);
        margin: 0;
        line-height: 1.6;
    }

    .qm-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 18px;
        margin: 10px 0;
        box-shadow: var(--shadow);
    }

    .qm-soft-card {
        background: var(--card-soft);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 16px;
        margin: 10px 0;
    }

    .qm-metric {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 16px;
        margin: 6px 0;
        min-height: 120px;
        box-shadow: var(--shadow);
    }

    .qm-metric-label {
        color: var(--muted);
        font-size: 14px !important;
        margin-bottom: 10px;
    }

    .qm-metric-value {
        font-size: 30px !important;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }

    .qm-metric-note {
        color: var(--muted);
        font-size: 14px !important;
        line-height: 1.5;
    }

    .qm-alert {
        background: var(--safe-bg);
        border: 1px solid var(--safe-line);
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }

    .qm-light {
        display: inline-block;
        border-radius: 999px;
        padding: 7px 14px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .qm-green { background: var(--green-bg); color: var(--green-text) !important; border: 1px solid #cfe3d4; }
    .qm-yellow { background: var(--yellow-bg); color: var(--yellow-text) !important; border: 1px solid #ecd59b; }
    .qm-orange { background: var(--orange-bg); color: var(--orange-text) !important; border: 1px solid #eac29c; }
    .qm-red { background: var(--red-bg); color: var(--red-text) !important; border: 1px solid #efc5c5; }

    .qm-trust {
        background: #fbfcfd;
        border: 1px dashed #cfd8df;
        border-radius: 18px;
        padding: 14px 16px;
        margin-top: 12px;
    }

    .qm-step {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 24px 20px;
        margin: 10px 0;
        box-shadow: var(--shadow);
    }

    .qm-step-title {
        font-size: 26px !important;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .qm-step-sub {
        color: var(--muted);
        margin-bottom: 16px;
        line-height: 1.6;
    }

    .qm-result {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 20px;
        margin-top: 16px;
        box-shadow: var(--shadow);
    }

    .qm-divider-title {
        margin-top: 22px;
        margin-bottom: 8px;
        font-weight: 700;
    }

    .qm-mini {
        color: var(--muted);
        font-size: 14px !important;
        line-height: 1.5;
    }

    .qm-nav-sep {
        margin-top: 16px;
        margin-bottom: 10px;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stLinkButton > a {
        width: 100%;
        min-height: 50px;
        border-radius: 16px;
        border: 1px solid var(--line);
        font-weight: 700;
        background: #fff !important;
        color: var(--text) !important;
        box-shadow: none !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stLinkButton > a:hover {
        border-color: #c7d1d8 !important;
        background: #fcfdfe !important;
        color: var(--text) !important;
    }

    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    div[data-baseweb="select"] {
        background: #ffffff !important;
        border-color: var(--line) !important;
        color: var(--text) !important;
    }

    .stRadio label, .stSelectbox label, .stCheckbox label, .stSlider label {
        font-weight: 600 !important;
        color: var(--text) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 30px !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def ensure_column(table: str, column: str, definition: str):
    c = conn()
    cur = c.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cur.fetchall()]
    if column not in columns:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        c.commit()
    c.close()


def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            consent INTEGER DEFAULT 0,
            prefs_json TEXT DEFAULT '{}',
            onboarding_json TEXT DEFAULT '{}',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            created_at TEXT,
            calm INTEGER,
            stress INTEGER,
            clarity INTEGER,
            focus INTEGER,
            context TEXT,
            note TEXT,
            result TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS decision_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            created_at TEXT,
            decision_type TEXT,
            sleep_ok INTEGER,
            emotion_high INTEGER,
            self_describe INTEGER,
            time_pressure INTEGER,
            result TEXT,
            reasons TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS weekly_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            created_at TEXT,
            review_json TEXT,
            summary TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    c.commit()
    c.close()

    ensure_column("decision_checks", "fatigue", "INTEGER DEFAULT 3")
    ensure_column("decision_checks", "stress_level", "INTEGER DEFAULT 3")
    ensure_column("decision_checks", "clarity", "INTEGER DEFAULT 3")
    ensure_column("decision_checks", "focus", "INTEGER DEFAULT 3")
    ensure_column("decision_checks", "rumination", "INTEGER DEFAULT 3")
    ensure_column("decision_checks", "advice", "TEXT DEFAULT ''")
    ensure_column("decision_checks", "readiness_score", "INTEGER DEFAULT 50")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(email: str, password: str):
    c = conn()
    cur = c.cursor()
    cur.execute(
        "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
        (email.lower().strip(), hash_password(password), datetime.utcnow().isoformat()),
    )
    uid = cur.lastrowid
    cur.execute("INSERT INTO profiles (user_id) VALUES (?)", (uid,))
    c.commit()
    c.close()
    return uid


def auth_user(email: str, password: str):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email = ?", (email.lower().strip(),))
    row = cur.fetchone()
    c.close()
    if not row:
        return None
    uid, pw_hash = row
    return uid if hash_password(password) == pw_hash else None


def get_profile(uid: int):
    c = conn()
    cur = c.cursor()
    cur.execute(
        "SELECT name, age, consent, prefs_json, onboarding_json FROM profiles WHERE user_id = ?",
        (uid,),
    )
    row = cur.fetchone()
    c.close()
    if not row:
        return {"name": "", "age": None, "consent": 0, "prefs": {}, "onboarding": {}}
    name, age, consent, prefs_json, onboarding_json = row
    return {
        "name": name or "",
        "age": age,
        "consent": bool(consent),
        "prefs": json.loads(prefs_json or "{}"),
        "onboarding": json.loads(onboarding_json or "{}"),
    }


def save_profile(uid: int, name=None, age=None, consent=None, prefs=None, onboarding=None):
    profile = get_profile(uid)
    name = profile["name"] if name is None else name
    age = profile["age"] if age is None else age
    consent_val = 1 if (profile["consent"] if consent is None else consent) else 0
    prefs_json = json.dumps(profile["prefs"] if prefs is None else prefs, ensure_ascii=False)
    onboarding_json = json.dumps(profile["onboarding"] if onboarding is None else onboarding, ensure_ascii=False)
    c = conn()
    cur = c.cursor()
    cur.execute(
        """
        UPDATE profiles
        SET name = ?, age = ?, consent = ?, prefs_json = ?, onboarding_json = ?
        WHERE user_id = ?
        """,
        (name, age, consent_val, prefs_json, onboarding_json, uid),
    )
    c.commit()
    c.close()


def current_user_email(uid: int):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT email FROM users WHERE id = ?", (uid,))
    row = cur.fetchone()
    c.close()
    return row[0] if row else ""


def insert_checkin(uid, calm, stress, clarity, focus, context, note, result):
    c = conn()
    cur = c.cursor()
    cur.execute(
        """
        INSERT INTO checkins (user_id, created_at, calm, stress, clarity, focus, context, note, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (uid, datetime.utcnow().isoformat(), calm, stress, clarity, focus, context, note, result),
    )
    c.commit()
    c.close()


def insert_decision(uid, payload):
    c = conn()
    cur = c.cursor()
    cur.execute(
        """
        INSERT INTO decision_checks (
            user_id, created_at, decision_type, sleep_ok, emotion_high, self_describe,
            time_pressure, result, reasons, fatigue, stress_level, clarity, focus,
            rumination, advice, readiness_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            uid,
            datetime.utcnow().isoformat(),
            payload["decision_type"],
            payload["sleep_ok"],
            payload["emotion_high"],
            payload["self_describe"],
            payload["time_pressure"],
            payload["result"],
            json.dumps(payload["reasons"], ensure_ascii=False),
            payload["fatigue"],
            payload["stress_level"],
            payload["clarity"],
            payload["focus"],
            payload["rumination"],
            payload["advice"],
            payload["readiness_score"],
        ),
    )
    c.commit()
    c.close()


def insert_weekly(uid, review_json, summary):
    c = conn()
    cur = c.cursor()
    cur.execute(
        "INSERT INTO weekly_reviews (user_id, created_at, review_json, summary) VALUES (?, ?, ?, ?)",
        (uid, datetime.utcnow().isoformat(), json.dumps(review_json, ensure_ascii=False), summary),
    )
    c.commit()
    c.close()


def get_last_checkins(uid, limit=12):
    c = conn()
    df = pd.read_sql_query(
        f"""
        SELECT created_at, calm, stress, clarity, focus, context, note, result
        FROM checkins
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT {int(limit)}
        """,
        c,
        params=(uid,),
    )
    c.close()
    return df


def get_last_weeklies(uid, limit=8):
    c = conn()
    df = pd.read_sql_query(
        f"""
        SELECT created_at, summary, review_json
        FROM weekly_reviews
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT {int(limit)}
        """,
        c,
        params=(uid,),
    )
    c.close()
    return df


def get_last_decisions(uid, limit=8):
    c = conn()
    df = pd.read_sql_query(
        f"""
        SELECT created_at, decision_type, result, advice, readiness_score
        FROM decision_checks
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT {int(limit)}
        """,
        c,
        params=(uid,),
    )
    c.close()
    return df


def export_user_data(uid):
    profile = get_profile(uid)
    c = conn()
    checkins = pd.read_sql_query("SELECT * FROM checkins WHERE user_id = ? ORDER BY id DESC", c, params=(uid,))
    decisions = pd.read_sql_query("SELECT * FROM decision_checks WHERE user_id = ? ORDER BY id DESC", c, params=(uid,))
    weeklies = pd.read_sql_query("SELECT * FROM weekly_reviews WHERE user_id = ? ORDER BY id DESC", c, params=(uid,))
    c.close()
    payload = {
        "exported_at": datetime.utcnow().isoformat(),
        "email": current_user_email(uid),
        "profile": profile,
        "checkins": checkins.to_dict(orient="records"),
        "decision_checks": decisions.to_dict(orient="records"),
        "weekly_reviews": weeklies.to_dict(orient="records"),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def delete_user_data(uid):
    c = conn()
    cur = c.cursor()
    cur.execute("DELETE FROM checkins WHERE user_id = ?", (uid,))
    cur.execute("DELETE FROM decision_checks WHERE user_id = ?", (uid,))
    cur.execute("DELETE FROM weekly_reviews WHERE user_id = ?", (uid,))
    cur.execute("DELETE FROM profiles WHERE user_id = ?", (uid,))
    cur.execute("DELETE FROM users WHERE id = ?", (uid,))
    c.commit()
    c.close()


def onboarding_complete(uid: int) -> bool:
    data = get_profile(uid)["onboarding"]
    required = ["goal", "who5", "bsrs5", "dimensions", "preferences_done", "confirmed"]
    return all(k in data for k in required)


def require_login():
    if not st.session_state.auth_user_id:
        st.warning("請先登入。")
        go("login")
        st.rerun()


def go(route: str):
    st.session_state.route = route


def safe_label(result):
    mapping = {
        "穩定": ("qm-green", "狀態穩定"),
        "偏緊": ("qm-yellow", "壓力偏高"),
        "失衡": ("qm-red", "先穩定再決定"),
        "綠燈": ("qm-green", "現在做"),
        "黃燈": ("qm-yellow", "晚一點做"),
        "橘燈": ("qm-orange", "先找第二意見"),
        "紅燈": ("qm-red", "先穩定"),
    }
    return mapping.get(result, ("qm-yellow", result))


def app_header(title=None, logged=False, subtitle=None):
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("<p class='qm-brand'>QuietMind</p>", unsafe_allow_html=True)
    with c2:
        a, b = st.columns(2)
        with a:
            if st.button("立即幫助", key=f"crisis_{title or 'top'}"):
                go("crisis")
                st.rerun()
        with b:
            st.markdown(
                "<a href='https://www.google.com' target='_self' style='display:block;text-align:center;text-decoration:none;background:#fff;border:1px solid #dde3e8;border-radius:16px;padding:12px 4px;color:#17232d !important;font-weight:700;'>快速離開</a>",
                unsafe_allow_html=True,
            )
    if title:
        st.title(title)
    if subtitle:
        st.markdown(f"<div class='qm-page-intro'>{subtitle}</div>", unsafe_allow_html=True)
    if logged and st.session_state.auth_user_id:
        st.caption(f"已登入：{current_user_email(st.session_state.auth_user_id)}")


def footer_nav():
    if not st.session_state.auth_user_id:
        return

    st.markdown("<div class='qm-nav-sep'></div>", unsafe_allow_html=True)
    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        if st.button("Today", key=f"nav_dashboard_{st.session_state.route}"):
            go("dashboard")
            st.rerun()
    with c2:
        if st.button("檢測", key=f"nav_checkin_{st.session_state.route}"):
            go("checkin")
            st.rerun()
    with c3:
        if st.button("決策", key=f"nav_decision_{st.session_state.route}"):
            go("decision_check")
            st.rerun()
    with c4:
        if st.button("回顧", key=f"nav_weekly_{st.session_state.route}"):
            go("weekly_review")
            st.rerun()
    with c5:
        if st.button("我的", key=f"nav_settings_{st.session_state.route}"):
            go("settings")
            st.rerun()


def score_who5(items):
    raw = sum(items)
    percent = raw * 4
    return raw, percent


def score_bsrs5(items, suicide):
    total = sum(items)
    if total > 15 or suicide > 2:
        return total, "高風險"
    if total >= 10:
        return total, "中度風險"
    return total, "一般風險"


def checkin_result(calm, stress, clarity, focus):
    readiness = round((calm * 0.28 + clarity * 0.30 + focus * 0.24 + (6 - stress) * 0.18) * 20)

    if stress >= 5 and (clarity <= 2 or focus <= 2):
        return {
            "status": "失衡",
            "readiness": max(20, readiness - 15),
            "headline": "你現在比較不適合做高代價決定。",
            "body": "先把自己穩下來，再回來評估。今天的重點不是撐住，而是降低刺激。",
            "actions": ["先做 2 分鐘降刺激", "先不要做重大決定", "需要時直接走 Support"],
        }

    if readiness >= 72 and stress <= 2:
        return {
            "status": "穩定",
            "readiness": readiness,
            "headline": "你現在狀態相對穩，可以照原計畫往下走。",
            "body": "適合處理重要但需要清楚判斷的事情。做決策前仍可再快速檢查一次。",
            "actions": ["照原計畫走", "先做最重要的一件事", "需要時再做決策檢查"],
        }

    return {
        "status": "偏緊",
        "readiness": readiness,
        "headline": "你現在偏緊，先不要急著往前衝。",
        "body": "先做一個小恢復動作，讓壓力降一點，再看要不要繼續。",
        "actions": ["先做 2 分鐘恢復", "30 分鐘後再看", "先把擔心寫成一句話"],
    }


def decision_result(sleep_ok, fatigue, stress_level, clarity, focus, rumination):
    reasons = []
    score = 100

    if not sleep_ok:
        score -= 14
        reasons.append("睡眠不足")
    if fatigue >= 4:
        score -= 12
        reasons.append("疲勞偏高")
    if stress_level >= 4:
        score -= 16
        reasons.append("壓力偏高")
    if clarity <= 2:
        score -= 18
        reasons.append("情緒清晰度偏低")
    if focus <= 2:
        score -= 14
        reasons.append("專注度不足")
    if rumination >= 4:
        score -= 16
        reasons.append("反芻明顯")

    score = max(0, min(100, score))

    if score >= 75:
        return "綠燈", score, reasons, "現在做"
    if score >= 55:
        return "黃燈", score, reasons, "晚一點做"
    if score >= 35:
        return "橘燈", score, reasons, "找第二意見"
    return "紅燈", score, reasons, "先穩定"


def readiness_copy(score):
    if score >= 75:
        return "你目前狀態相對穩，可以做重要決定。"
    if score >= 55:
        return "你可以先暫停一下，稍晚再做決定會更好。"
    if score >= 35:
        return "你現在不太適合單獨做判斷，先找第二意見。"
    return "你現在先不要做重大決定，先穩定自己。"


def mood_message(last_result):
    mapping = {
        None: "今天先做一次 30 秒微檢測。",
        "穩定": "你目前大致穩定，適合先做最重要的一件事。",
        "偏緊": "你今天偏緊，先降刺激，再進入重要任務。",
        "失衡": "你今天先不要急著往前推進，先把狀態穩住。",
    }
    return mapping.get(last_result, "今天先做一次 30 秒微檢測。")


def dimension_suggestion(status, improve):
    if status <= 2 and improve >= 4:
        return "先做一個最小調整"
    if status <= 2:
        return "先降負荷"
    if improve >= 4:
        return "先排進本週實驗"
    return "先維持"


def default_four_dimensions(profile, checkins):
    dims = profile["onboarding"].get("dimensions", {})
    groups = {
        "恢復": ["健康/睡眠", "休閒/恢復"],
        "穩定": ["工作/學業", "學習/專注"],
        "連結": ["關係"],
        "意義": ["成長/意義"],
    }

    results = {}
    for group, names in groups.items():
        values = []
        for n in names:
            if n in dims:
                values.append(int(dims[n]["status"]) * 20)
        if values:
            base = int(sum(values) / len(values))
        else:
            base = 60

        if not checkins.empty:
            latest = checkins.iloc[0]
            if group == "恢復":
                base = int((base + (6 - int(latest["stress"])) * 15 + int(latest["calm"]) * 10) / 2)
            elif group == "穩定":
                base = int((base + int(latest["clarity"]) * 12 + int(latest["focus"]) * 12) / 2)
            elif group == "連結":
                base = int((base + 72) / 2)
            elif group == "意義":
                base = int((base + 68) / 2)
        results[group] = max(0, min(100, base))
    return results


def get_best_time_from_data(profile, checkins, weeklies):
    prefs = profile["prefs"] or {}
    if not weeklies.empty:
        try:
            latest_review = json.loads(weeklies.iloc[0]["review_json"])
            best_time = latest_review.get("patterns", {}).get("best_time")
            if best_time:
                return best_time
        except Exception:
            pass
    return prefs.get("focus_time", "上午")


def get_top_today_action(uid, checkins, weeklies):
    if checkins.empty:
        return "補做微檢測"
    latest = checkins.iloc[0]["result"]
    if latest == "失衡":
        return "先做 2 分鐘降刺激"
    if latest == "偏緊":
        return "先把最重要的一件事延後 30 分鐘"
    if weeklies.empty:
        return "今晚安排一次每週回顧"
    return "把重要決策排進狀態較穩的時段"


def weekly_insight_from_data(checkins, review):
    overview = review.get("overview", {})
    patterns = review.get("patterns", {})
    emotion = overview.get("emotion", "混亂")
    unstable_time = overview.get("unstable_time", "晚上")
    best_time = patterns.get("best_time", "上午")

    if checkins.empty:
        return f"你這週最需要補上的不是更多努力，而是一個穩定的回報節奏。先把微檢測變成儀式，再談優化。"

    avg_stress = round(checkins["stress"].mean(), 1)
    avg_focus = round(checkins["focus"].mean(), 1)

    if avg_stress >= 4 and avg_focus <= 3:
        return f"本週你不是單純效率差，而是壓力偏高把專注拉走了。最容易失衡的時段在{unstable_time}，較適合做重要事的時段反而是{best_time}。"
    if emotion in ["疲憊", "空洞"]:
        return f"本週核心問題不是事情太多，而是恢復不足。你比較像是在低電量運作，先補恢復，再談推進。"
    return f"本週你不是狀態很差，而是穩定度不夠。當情境切換變多時，注意力容易散掉；把重要事放到{best_time}會更有利。"


def trend_lines_from_checkins(checkins):
    if checkins.empty:
        return None
    df = checkins.copy()
    df["created_at"] = pd.to_datetime(df["created_at"])
    df = df.sort_values("created_at")
    return df.set_index("created_at")[["calm", "stress", "clarity", "focus"]]


init_db()

for k, v in {
    "route": "home",
    "auth_user_id": None,
    "wizard_step": 1,
    "weekly_step": 1,
    "weekly_review_draft": {},
    "checkin_step": 1,
    "checkin_draft": {},
}.items():
    st.session_state.setdefault(k, v)


def page_home():
    app_header(subtitle="先穩定狀態，再做重要決定")
    st.markdown(
        """
        <div class='qm-hero'>
            <div class='qm-hero-kicker'>Decision wellness</div>
            <div class='qm-hero-title'>先看見自己<br>再做重要決定</div>
            <p class='qm-hero-sub'>
                QuietMind 不是要你停留更久，而是幫你少在失衡時做出代價高的決定。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='qm-trust'>
            <strong>你會看到什麼</strong>
            <p class='qm-mini'>Today 首頁、30 秒微檢測、決策前檢查、每週回顧、Support 專業橋接。</p>
            <strong>資料怎麼用</strong>
            <p class='qm-mini'>只用來生成你的狀態摘要、回顧與提醒；你可以在設定頁下載或刪除資料。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.auth_user_id:
        if st.button("開始 30 秒微檢測", type="primary"):
            st.session_state.checkin_step = 1
            st.session_state.checkin_draft = {}
            go("checkin")
            st.rerun()
        if st.button("進入 Today 首頁"):
            go("dashboard")
            st.rerun()
    else:
        if st.button("開始使用", type="primary"):
            go("suitability")
            st.rerun()
        if st.button("登入"):
            go("login")
            st.rerun()

    if st.button("看 Support / 心理資源"):
        go("resources")
        st.rerun()


def page_suitability():
    app_header("先選最適合的入口", subtitle="這不是測驗，只是幫你少走彎路")
    with st.form("suitability_form"):
        q1 = st.radio("你現在比較需要哪一種幫助？", ["先自己整理狀態", "需要立即幫助"])
        q2 = st.radio("你是否已滿 18 歲？", ["是", "否"])
        q3 = st.selectbox("你目前最困擾的是什麼？", ["壓力偏高", "焦慮反芻", "專注很碎", "空洞疲憊", "做決定很亂", "其他"])
        q4 = st.radio("你希望先自己整理，還是直接找專業資源？", ["先自己整理", "直接找專業資源"])
        submitted = st.form_submit_button("看建議")

    if submitted:
        if q1 == "需要立即幫助":
            go("crisis")
        elif q2 == "否":
            go("under18")
        elif q4 == "直接找專業資源":
            go("resources")
        else:
            go("privacy")
        st.rerun()


def page_under18():
    app_header("目前完整流程僅開放 18+", subtitle="你仍然可以直接查看一般資源與危機支援")
    if st.button("看一般 Support"):
        go("resources")
        st.rerun()
    if st.button("看危機支援"):
        go("crisis")
        st.rerun()


def page_privacy():
    app_header("隱私與安全", subtitle="用白話建立信任，而不是用長篇條款把你淹沒")
    blocks = [
        ("我們收什麼", "帳號資料、你主動填寫的基線盤點、每日檢測、決策檢查與回顧資料。"),
        ("拿來做什麼", "生成 Today 首頁、決策建議、每週摘要與個人化提醒。"),
        ("哪些是必要", "帳號與主要流程資料是必要；備註與偏好是選填。"),
        ("誰能看見", "預設只有你自己可見；未經你明確同意，不會分享給第三方。"),
        ("你可以怎麼控制", "設定頁可下載你的資料，也可刪除帳號與歷史資料。"),
    ]
    for t, txt in blocks:
        st.markdown(f"<div class='qm-card'><strong>{t}</strong><p>{txt}</p></div>", unsafe_allow_html=True)

    st.warning("本服務不做診斷、不做治療宣稱，也不取代專業協助。")
    if st.button("我了解，前往註冊", type="primary"):
        go("register")
        st.rerun()


def page_register():
    app_header("建立帳號", subtitle="先建立你的私人控制台")
    with st.form("register_form"):
        name = st.text_input("你的稱呼")
        email = st.text_input("Email")
        age = st.number_input("年齡", min_value=18, max_value=120, value=18)
        password = st.text_input("密碼", type="password")
        consent = st.checkbox("我同意本服務依說明處理我主動提供的敏感資料")
        ok = st.form_submit_button("建立帳號")

    if ok:
        errors = []
        if not email or "@" not in email:
            errors.append("請輸入有效 Email。")
        if len(password) < 6:
            errors.append("密碼至少 6 碼。")
        if not consent:
            errors.append("請先同意資料處理說明。")
        if errors:
            st.error("\n".join(errors))
        else:
            try:
                uid = create_user(email, password)
                save_profile(uid, name=name, age=int(age), consent=True)
                st.session_state.auth_user_id = uid
                st.session_state.wizard_step = 1
                go("onboarding")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("這個 Email 已註冊，請直接登入。")


def page_login():
    app_header("登入", subtitle="回到你的 Today 首頁")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("密碼", type="password")
        ok = st.form_submit_button("登入")

    if ok:
        uid = auth_user(email, password)
        if uid:
            st.session_state.auth_user_id = uid
            if onboarding_complete(uid):
                go("dashboard")
            else:
                st.session_state.wizard_step = 1
                go("onboarding")
            st.rerun()
        else:
            st.error("帳號或密碼錯誤。")

    if st.button("前往註冊"):
        go("register")
        st.rerun()


def page_onboarding():
    require_login()
    uid = st.session_state.auth_user_id
    profile = get_profile(uid)
    data = profile["onboarding"] or {}
    step = st.session_state.wizard_step

    app_header("第一次設定", logged=True, subtitle=f"Step {step} / 6")
    st.progress(step / 6)

    if step == 1:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>你最想改善什麼？</div><div class='qm-step-sub'>只要選一個主要方向，之後都可以調整。</div></div>", unsafe_allow_html=True)
        goal = st.radio("使用目標", ["更穩定", "更專注", "少一點空洞", "不要在亂的時候做決定"], label_visibility="collapsed")
        if st.button("下一步", type="primary"):
            data["goal"] = goal
            save_profile(uid, onboarding=data)
            st.session_state.wizard_step = 2
            st.rerun()

    elif step == 2:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>先做 WHO-5 基線</div><div class='qm-step-sub'>抓近期心理福祉。0 = 從未，5 = 一直如此。</div></div>", unsafe_allow_html=True)
        questions = [
            "我感到心情愉快且精神不錯",
            "我感到平靜而放鬆",
            "我感到有活力、醒來時精神不錯",
            "我的日常生活中有讓我感到有興趣的事",
            "我覺得每天都有值得期待的事",
        ]
        items = [st.slider(q, 0, 5, 2) for q in questions]
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步"):
                st.session_state.wizard_step = 1
                st.rerun()
        with c2:
            if st.button("下一步", type="primary"):
                raw, pct = score_who5(items)
                data["who5"] = {"items": items, "raw": raw, "percent": pct}
                save_profile(uid, onboarding=data)
                st.session_state.wizard_step = 3
                st.rerun()

    elif step == 3:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>再做 BSRS-5 基線</div><div class='qm-step-sub'>抓近期情緒困擾與分流。0 = 完全沒有，4 = 非常嚴重。</div></div>", unsafe_allow_html=True)
        questions = [
            "感到緊張不安",
            "感到憂鬱、心情低落",
            "容易動怒或煩躁",
            "覺得比不上別人",
            "睡眠困擾",
        ]
        items = [st.slider(q, 0, 4, 1) for q in questions]
        suicide = st.slider("附加題：是否出現傷害自己的想法？", 0, 4, 0)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="onb_bsrs_back"):
                st.session_state.wizard_step = 2
                st.rerun()
        with c2:
            if st.button("下一步", key="onb_bsrs_next", type="primary"):
                total, level = score_bsrs5(items, suicide)
                data["bsrs5"] = {"items": items, "suicide": suicide, "total": total, "level": level}
                save_profile(uid, onboarding=data)
                if level == "高風險":
                    go("crisis")
                else:
                    st.session_state.wizard_step = 4
                st.rerun()

    elif step == 4:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>六維度生活盤點</div><div class='qm-step-sub'>這些資料之後會被濃縮成四構面摘要：恢復、穩定、連結、意義。</div></div>", unsafe_allow_html=True)
        dims = ["工作/學業", "關係", "健康/睡眠", "學習/專注", "休閒/恢復", "成長/意義"]
        dim_data = {}
        for d in dims:
            st.markdown(f"##### {d}")
            status = st.slider(f"{d}｜目前狀態", 1, 5, 3, key=f"{d}_status")
            improve = st.slider(f"{d}｜改善優先度", 1, 5, 3, key=f"{d}_improve")
            dim_data[d] = {"status": status, "improve": improve}
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="onb_dim_back"):
                st.session_state.wizard_step = 3
                st.rerun()
        with c2:
            if st.button("下一步", key="onb_dim_next", type="primary"):
                data["dimensions"] = dim_data
                save_profile(uid, onboarding=data)
                st.session_state.wizard_step = 5
                st.rerun()

    elif step == 5:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>設定你的回顧偏好</div><div class='qm-step-sub'>重點不是每天黏著，而是週報真的值得等。</div></div>", unsafe_allow_html=True)
        reminder_day = st.selectbox("你想每週哪天收到回顧提醒？", ["週一", "週二", "週三", "週四", "週五", "週六", "週日"])
        summary_style = st.radio("你偏好哪種摘要形式？", ["文字摘要", "圖表", "都可以"])
        focus_time = st.selectbox("你通常哪個時段最能專心？", ["清晨", "上午", "下午", "晚上", "不固定"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="onb_pref_back"):
                st.session_state.wizard_step = 4
                st.rerun()
        with c2:
            if st.button("下一步", key="onb_pref_next", type="primary"):
                save_profile(uid, prefs={"reminder_day": reminder_day, "summary_style": summary_style, "focus_time": focus_time})
                data["preferences_done"] = True
                save_profile(uid, onboarding=data)
                st.session_state.wizard_step = 6
                st.rerun()

    elif step == 6:
        who5 = data.get("who5", {})
        bsrs5 = data.get("bsrs5", {})
        st.markdown("<div class='qm-step'><div class='qm-step-title'>檢查你的設定</div><div class='qm-step-sub'>確認後，你的 Today 首頁就會開始運作。</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='qm-card'><strong>使用目標</strong><p>{data.get('goal', '未填')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='qm-card'><strong>WHO-5</strong><p>{who5.get('percent', '未填')}%</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='qm-card'><strong>BSRS-5</strong><p>{bsrs5.get('total', '未填')} 分｜{bsrs5.get('level', '未填')}</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='qm-card'><strong>偏好設定</strong><p>已完成</p></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="onb_done_back"):
                st.session_state.wizard_step = 5
                st.rerun()
        with c2:
            if st.button("確認並進入 Today", key="onb_done", type="primary"):
                data["confirmed"] = True
                save_profile(uid, onboarding=data)
                go("dashboard")
                st.rerun()


def page_dashboard():
    require_login()
    uid = st.session_state.auth_user_id
    if not onboarding_complete(uid):
        go("onboarding")
        st.rerun()

    profile = get_profile(uid)
    checkins = get_last_checkins(uid, 20)
    weeklies = get_last_weeklies(uid, 8)
    decisions = get_last_decisions(uid, 8)

    latest_checkin = None if checkins.empty else checkins.iloc[0]
    latest_result = None if latest_checkin is None else latest_checkin["result"]

    if decisions.empty:
        decision_readiness = 64
    else:
        decision_readiness = int(decisions.iloc[0]["readiness_score"])

    dimensions = default_four_dimensions(profile, checkins)
    top_action = get_top_today_action(uid, checkins, weeklies)
    best_time = get_best_time_from_data(profile, checkins, weeklies)

    app_header("Today", logged=True, subtitle="我現在怎麼樣、今天先做什麼、現在適不適合做重要決定")
    status_text = mood_message(latest_result)

    st.markdown(
        f"""
        <div class='qm-hero'>
            <div class='qm-hero-kicker'>Today</div>
            <div class='qm-hero-title'>{status_text}</div>
            <p class='qm-hero-sub'>
                Decision readiness <strong>{decision_readiness} / 100</strong><br>
                今天先處理：<strong>{top_action}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("開始 30 秒微檢測", type="primary"):
            st.session_state.checkin_step = 1
            st.session_state.checkin_draft = {}
            go("checkin")
            st.rerun()
    with c2:
        if st.button("做決策前檢查"):
            go("decision_check")
            st.rerun()

    st.subheader("四構面概覽")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='qm-metric'><div class='qm-metric-label'>恢復</div><div class='qm-metric-value'>{dimensions['恢復']}</div><div class='qm-metric-note'>睡眠、降刺激、恢復節奏</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='qm-metric'><div class='qm-metric-label'>穩定</div><div class='qm-metric-value'>{dimensions['穩定']}</div><div class='qm-metric-note'>壓力、清晰度、專注</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='qm-metric'><div class='qm-metric-label'>連結</div><div class='qm-metric-value'>{dimensions['連結']}</div><div class='qm-metric-note'>關係支持與互動品質</div></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='qm-metric'><div class='qm-metric-label'>意義</div><div class='qm-metric-value'>{dimensions['意義']}</div><div class='qm-metric-note'>方向感、目的感、價值一致</div></div>", unsafe_allow_html=True)

    if latest_checkin is not None:
        st.subheader("今日狀態摘要")
        st.markdown(
            f"""
            <div class='qm-card'>
                <p><strong>最新校準：</strong>{latest_checkin['result']}</p>
                <p>壓力 {latest_checkin['stress']}/5 ・ 清晰度 {latest_checkin['clarity']}/5 ・ 專注 {latest_checkin['focus']}/5</p>
                <p>今天較適合做重要事的時段：<strong>{best_time}</strong></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='qm-card'>
                <p><strong>還沒有今日訊號。</strong></p>
                <p>先完成一次微檢測，Today 首頁才會開始真正運作。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("今天最值得先做的事")
    suggestions = [
        f"• {top_action}",
        "• 把高代價決策排到狀態較穩的時段",
        "• 晚上只保留一個低刺激收尾流程",
    ]
    st.markdown(
        f"<div class='qm-card'><p>{'<br>'.join(suggestions)}</p></div>",
        unsafe_allow_html=True,
    )

    c3, c4 = st.columns(2)
    with c3:
        if st.button("查看週報"):
            go("reports")
            st.rerun()
    with c4:
        if st.button("進入 Support"):
            go("resources")
            st.rerun()

    footer_nav()


def page_checkin():
    require_login()
    uid = st.session_state.auth_user_id
    step = st.session_state.checkin_step
    draft = st.session_state.get("checkin_draft", {})

    app_header("30 秒微檢測", logged=True, subtitle="每頁只問 1–2 題，完成後立刻回饋你的狀態")
    st.progress(step / 3)

    if step == 1:
        st.markdown(
            """
            <div class='qm-step'>
                <div class='qm-step-title'>你現在的情緒比較接近哪一邊？</div>
                <div class='qm-step-sub'>不要想太久，只選現在最接近的感覺。</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        calm = st.slider("低落 ←→ 平穩 / 緊繃", 1, 5, draft.get("calm", 3), help="越高越平靜")
        stress = st.slider("壓力有多高？", 1, 5, draft.get("stress", 3))
        if st.button("下一步", type="primary"):
            draft["calm"] = calm
            draft["stress"] = stress
            st.session_state.checkin_draft = draft
            st.session_state.checkin_step = 2
            st.rerun()

    elif step == 2:
        st.markdown(
            """
            <div class='qm-step'>
                <div class='qm-step-title'>你能清楚分辨自己在感受什麼嗎？</div>
                <div class='qm-step-sub'>這一步只抓必要訊號，不需要回想很多細節。</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        clarity = st.slider("非常模糊 ←→ 非常清楚", 1, 5, draft.get("clarity", 3))
        focus = st.slider("很碎裂 ←→ 很穩定", 1, 5, draft.get("focus", 3))
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步"):
                st.session_state.checkin_step = 1
                st.rerun()
        with c2:
            if st.button("下一步", type="primary"):
                draft["clarity"] = clarity
                draft["focus"] = focus
                st.session_state.checkin_draft = draft
                st.session_state.checkin_step = 3
                st.rerun()

    elif step == 3:
        st.markdown(
            """
            <div class='qm-step'>
                <div class='qm-step-title'>最後補一個情境</div>
                <div class='qm-step-sub'>讓後續回顧知道你是在什麼情境下變化。</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        context = st.selectbox("你現在在哪個情境？", ["起床後", "通勤中", "工作/上課前", "午間", "下班/下課後", "睡前", "其他"])
        note = st.text_area("備註（選填）", value=draft.get("note", ""), placeholder="例如：剛被通知打斷、昨晚睡不好、準備開會")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="checkin_back_final"):
                st.session_state.checkin_step = 2
                st.rerun()
        with c2:
            if st.button("完成檢測", key="checkin_done", type="primary"):
                draft["context"] = context
                draft["note"] = note

                result_obj = checkin_result(draft["calm"], draft["stress"], draft["clarity"], draft["focus"])
                insert_checkin(
                    uid,
                    draft["calm"],
                    draft["stress"],
                    draft["clarity"],
                    draft["focus"],
                    context,
                    note,
                    result_obj["status"],
                )

                st.session_state.checkin_draft = {}
                st.session_state.checkin_step = 1

                cls, label = safe_label(result_obj["status"])
                st.markdown(
                    f"""
                    <div class='qm-result'>
                        <div class='qm-light {cls}'>{label}</div>
                        <p><strong>Decision readiness {result_obj['readiness']} / 100</strong></p>
                        <p>{result_obj['headline']}</p>
                        <p>{result_obj['body']}</p>
                        <p><strong>接下來做這些就好：</strong></p>
                        <ul>
                            <li>{result_obj['actions'][0]}</li>
                            <li>{result_obj['actions'][1]}</li>
                            <li>{result_obj['actions'][2]}</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c3, c4 = st.columns(2)
                with c3:
                    if st.button("回 Today 首頁", key="checkin_to_today"):
                        go("dashboard")
                        st.rerun()
                with c4:
                    if st.button("做決策前檢查", key="checkin_to_decision"):
                        go("decision_check")
                        st.rerun()

    footer_nav()


def page_decision_check():
    require_login()
    uid = st.session_state.auth_user_id

    app_header("決策前檢查", logged=True, subtitle="產品不是幫你做決定，而是幫你判斷現在是不是適合做決定的狀態")
    with st.form("decision_form"):
        d_type = st.selectbox("你現在要做什麼類型的決定？", ["工作/學業", "關係", "金錢", "健康", "搬遷/轉換", "其他"])
        sleep_ok = st.radio("昨晚睡得夠嗎？", ["夠", "不夠"], horizontal=True) == "夠"
        fatigue = st.slider("疲勞程度", 1, 5, 3)
        stress_level = st.slider("壓力程度", 1, 5, 3)
        clarity = st.slider("你現在能清楚描述自己狀態嗎？", 1, 5, 3)
        focus = st.slider("你現在的專注度如何？", 1, 5, 3)
        rumination = st.slider("你有一直在腦中反覆想同一件事嗎？", 1, 5, 3)
        ok = st.form_submit_button("看我的狀態")

    if ok:
        result, score, reasons, advice = decision_result(sleep_ok, fatigue, stress_level, clarity, focus, rumination)

        desc_map = {
            "綠燈": "你目前狀態相對穩，可以做重要決定。",
            "黃燈": "你不是完全不能做，只是晚一點做會更好。",
            "橘燈": "現在不建議單獨拍板，先找第二意見。",
            "紅燈": "你現在先不要做重大決定，先穩定自己。",
        }

        action_map = {
            "綠燈": ["把決定寫成一句話", "列出最重要的取捨", "做完後再回頭確認一次"],
            "黃燈": ["先休息 20–30 分鐘", "把情境刺激降下來", "稍晚再做一次檢查"],
            "橘燈": ["先找一個可信任的人討論", "先列出兩個替代方案", "不要在情緒高點定案"],
            "紅燈": ["先做 2 分鐘降刺激", "先離開高刺激情境", "需要時直接走 Support"],
        }

        insert_decision(
            uid,
            {
                "decision_type": d_type,
                "sleep_ok": int(sleep_ok),
                "emotion_high": int(stress_level >= 4),
                "self_describe": int(clarity >= 3),
                "time_pressure": int(rumination >= 4),
                "result": result,
                "reasons": reasons,
                "fatigue": int(fatigue),
                "stress_level": int(stress_level),
                "clarity": int(clarity),
                "focus": int(focus),
                "rumination": int(rumination),
                "advice": advice,
                "readiness_score": int(score),
            }
        )

        cls, label = safe_label(result)
        if reasons:
            reason_html = "".join([f"<li>{r}</li>" for r in reasons])
        else:
            reason_html = "<li>目前沒有明顯風險訊號</li>"

        suggestion_html = "".join([f"<li>{s}</li>" for s in action_map[result]])

        st.markdown(
            f"""
            <div class='qm-result'>
                <div class='qm-light {cls}'>{label}</div>
                <p><strong>Decision readiness {score} / 100</strong></p>
                <p>{desc_map[result]}</p>
                <p><strong>原因</strong></p>
                <ul>{reason_html}</ul>
                <p><strong>建議</strong></p>
                <ul>{suggestion_html}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"結論：{advice}")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("回 Today", key="decision_to_today"):
                go("dashboard")
                st.rerun()
        with c2:
            if st.button("先做微檢測", key="decision_to_checkin"):
                go("checkin")
                st.rerun()
        with c3:
            if st.button("進入 Support", key="decision_to_support"):
                go("resources")
                st.rerun()

    footer_nav()


def page_weekly_review():
    require_login()
    uid = st.session_state.auth_user_id
    step = st.session_state.weekly_step
    review = st.session_state.get("weekly_review_draft", {})
    checkins = get_last_checkins(uid, 20)

    app_header("每週回顧", logged=True, subtitle="先說洞察，再說數據；先說模式，再說指標")
    st.progress(step / 4)

    if step == 1:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>A. 本週總覽</div><div class='qm-step-sub'>先回答整體感，不用一次講很多。</div></div>", unsafe_allow_html=True)
        stability = st.slider("這週整體穩定度", 1, 5, 3)
        emotion = st.selectbox("最常見情緒", ["平靜", "焦躁", "疲憊", "空洞", "煩躁", "混亂"])
        unstable_time = st.selectbox("最容易失衡時段", ["清晨", "上午", "下午", "晚上", "睡前", "不固定"])
        if st.button("下一步", key="wr1_next", type="primary"):
            review["overview"] = {"stability": stability, "emotion": emotion, "unstable_time": unstable_time}
            st.session_state.weekly_review_draft = review
            st.session_state.weekly_step = 2
            st.rerun()

    elif step == 2:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>B. 六維度檢視</div><div class='qm-step-sub'>不是每一面都要修，只要先看出真正影響你的那一面。</div></div>", unsafe_allow_html=True)
        dims = ["工作/學業", "關係", "健康/睡眠", "學習/專注", "休閒/恢復", "成長/意義"]
        data = {}
        for d in dims:
            state = st.selectbox(f"{d}｜這週大致如何？", ["偏差", "普通", "穩定"], key=f"state_{d}")
            impact = st.text_input(f"{d}｜最影響你的是什麼？", key=f"impact_{d}")
            adjust = st.text_input(f"{d}｜下週最想調整什麼？", key=f"adjust_{d}")
            data[d] = {"state": state, "impact": impact, "adjust": adjust}
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="wr2_back"):
                st.session_state.weekly_step = 1
                st.rerun()
        with c2:
            if st.button("下一步", key="wr2_next", type="primary"):
                review["dimensions"] = data
                st.session_state.weekly_review_draft = review
                st.session_state.weekly_step = 3
                st.rerun()

    elif step == 3:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>C. 模式辨識</div><div class='qm-step-sub'>把這週的散亂訊號變成一個可行的模式。</div></div>", unsafe_allow_html=True)
        trigger = st.text_input("哪個情境最容易打亂你？")
        helpful = st.text_input("哪個行為最有幫助？")
        best_time = st.selectbox("哪個時段最適合做重要事？", ["清晨", "上午", "下午", "晚上", "不固定"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="wr3_back"):
                st.session_state.weekly_step = 2
                st.rerun()
        with c2:
            if st.button("下一步", key="wr3_next", type="primary"):
                review["patterns"] = {"trigger": trigger, "helpful": helpful, "best_time": best_time}
                st.session_state.weekly_review_draft = review
                st.session_state.weekly_step = 4
                st.rerun()

    elif step == 4:
        st.markdown("<div class='qm-step'><div class='qm-step-title'>D. 下週只選一個實驗</div><div class='qm-step-sub'>不要一次修全部，只選一個最有槓桿的動作。</div></div>", unsafe_allow_html=True)
        experiment = st.radio(
            "選一個就好",
            [
                "起床後 30 分鐘不進高刺激內容",
                "睡前 30 分鐘降刺激",
                "重要任務放到高專注時段",
                "每天做一次 30 秒微檢測",
            ],
        )

        if review.get("overview"):
            insight = weekly_insight_from_data(checkins, review)
            st.markdown(
                f"""
                <div class='qm-result'>
                    <p><strong>本週你真正發生了什麼</strong></p>
                    <p>{insight}</p>
                    <p><strong>下週實驗</strong>：{experiment}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="wr4_back"):
                st.session_state.weekly_step = 3
                st.rerun()
        with c2:
            if st.button("完成回顧", key="wr4_done", type="primary"):
                review["experiment"] = experiment
                insight = weekly_insight_from_data(checkins, review)
                summary = f"{insight}｜下週實驗：{experiment}"
                insert_weekly(uid, review, summary)
                st.session_state.weekly_review_draft = {}
                st.session_state.weekly_step = 1
                st.markdown(f"<div class='qm-card'><strong>已完成本週回顧</strong><p>{summary}</p></div>", unsafe_allow_html=True)

    footer_nav()


def page_reports():
    require_login()
    uid = st.session_state.auth_user_id
    app_header("報告中心", logged=True, subtitle="真正重要的不是圖表多漂亮，而是它有沒有把你這週說清楚")

    checkins = get_last_checkins(uid, 20)
    weeklies = get_last_weeklies(uid, 12)
    trends = trend_lines_from_checkins(checkins)

    st.subheader("最近幾次波動")
    if trends is not None:
        st.line_chart(trends)
        st.caption("這張圖只做一件事：讓你看見最近幾次壓力、清晰度與專注的波動。")
    else:
        st.markdown("<div class='qm-card'><p>還沒有資料，先做一次微檢測。</p></div>", unsafe_allow_html=True)

    st.subheader("週報列表")
    if weeklies.empty:
        st.markdown("<div class='qm-card'><p>你還沒有週報，先完成一次每週回顧。</p></div>", unsafe_allow_html=True)
    else:
        for _, row in weeklies.iterrows():
            st.markdown(
                f"<div class='qm-card'><strong>{row['created_at'][:10]}</strong><p>{row['summary']}</p></div>",
                unsafe_allow_html=True,
            )

    footer_nav()


def page_resources():
    app_header("Support", logged=bool(st.session_state.auth_user_id), subtitle="你可以先不解釋很多，只要先選一條路")
    st.markdown(
        """
        <div class='qm-alert'>
            <strong>如果你現在有立即危險、強烈自傷念頭，或擔心自己撐不住，請優先使用危機支援。</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("你現在想要哪一種幫助？")

    st.markdown(
        """
        <div class='qm-card'>
            <strong>一般支持</strong>
            <p>2 分鐘穩定、睡前降刺激、反芻中斷、社群滑完後回神。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("查看一般支持工具"):
        go("toolbox")
        st.rerun()

    st.markdown(
        """
        <div class='qm-card'>
            <strong>預約專業</strong>
            <p>合作心理師、諮商所、校園資源、企業 EAP。先找到可連上的人，再決定細節。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    city = st.selectbox("縣市", ["不限", "台北市", "新北市", "桃園市", "台中市", "台南市", "高雄市", "其他"])
    mode = st.selectbox("形式", ["不限", "線上", "實體"])
    subsidy = st.selectbox("費用", ["不限", "可補助", "自費"])

    resources = [
        ("青壯心理健康支持方案", "適合先找補助與基本支持的人。"),
        ("社區心理衛生中心", "適合需要地方資源、轉介與持續支持的人。"),
        ("心理諮商所", "適合準備進入專業一對一支持的人。"),
        ("校園 / 企業資源", "適合先從身邊已存在的支持系統開始。"),
    ]

    st.caption(f"目前篩選：{city} / {mode} / {subsidy}")
    for title, text in resources:
        st.markdown(f"<div class='qm-soft-card'><strong>{title}</strong><p>{text}</p></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='qm-card'>
            <strong>我現在可能不太安全</strong>
            <p>危機資源不應該被藏太深。真的撐不住時，先讓人連上你。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("撥打 1925", "tel:1925")
    with c2:
        st.link_button("撥打 1995", "tel:1995")

    c3, c4 = st.columns(2)
    with c3:
        st.link_button("撥打 1980", "tel:1980")
    with c4:
        st.link_button("撥打 119", "tel:119")

    footer_nav()


def page_toolbox():
    require_login()
    app_header("一般支持工具", logged=True, subtitle="不用學習很多，只要先執行一個最小動作")
    tools = [
        ("2 分鐘降刺激", "吸氣 4 秒，停 2 秒，吐氣 6 秒，連續 10 次。"),
        ("睡前 30 分鐘降刺激", "關掉高刺激內容，只保留低亮度、低資訊量的收尾。"),
        ("反芻中斷", "把腦中一直重播的想法寫成一句話，然後問自己：現在要做的下一步是什麼？"),
        ("社群滑完後回神", "把手機放下 60 秒，說出你此刻的情緒、身體感受、下一步。"),
        ("工作前進入專注模式", "先做一次微檢測，再只選一件最重要的任務。"),
    ]
    for title, text in tools:
        st.markdown(f"<div class='qm-card'><strong>{title}</strong><p>{text}</p></div>", unsafe_allow_html=True)
    footer_nav()


def page_crisis():
    app_header("危機支援")
    st.markdown(
        """
        <div class='qm-alert'>
            <strong>如果你現在有立即危險、強烈自傷想法，或擔心自己撐不住，請不要繼續一般流程。</strong>
            <p>先用最直接的方式找人連上你。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button("立即撥打 1925", "tel:1925")
    st.link_button("立即撥打 1995", "tel:1995")
    st.link_button("立即撥打 1980", "tel:1980")
    st.link_button("緊急狀況撥打 119", "tel:119")

    if st.button("我現在安全，回到服務"):
        go("dashboard" if st.session_state.auth_user_id else "home")
        st.rerun()
    if st.button("我只是想找一般 Support"):
        go("resources")
        st.rerun()


def page_settings():
    require_login()
    uid = st.session_state.auth_user_id
    profile = get_profile(uid)

    app_header("我的設定", logged=True, subtitle="你可以修改偏好，也可以下載或刪除資料")

    with st.form("settings_form"):
        name = st.text_input("稱呼", value=profile["name"])
        age = st.number_input("年齡", min_value=18, max_value=120, value=int(profile["age"] or 18))
        reminder_day = st.selectbox(
            "回顧提醒日",
            ["週一", "週二", "週三", "週四", "週五", "週六", "週日"],
            index=["週一", "週二", "週三", "週四", "週五", "週六", "週日"].index(profile["prefs"].get("reminder_day", "週日")),
        )
        summary_style = st.radio(
            "摘要偏好",
            ["文字摘要", "圖表", "都可以"],
            index=["文字摘要", "圖表", "都可以"].index(profile["prefs"].get("summary_style", "文字摘要")),
        )
        focus_time = st.selectbox(
            "高專注時段",
            ["清晨", "上午", "下午", "晚上", "不固定"],
            index=["清晨", "上午", "下午", "晚上", "不固定"].index(profile["prefs"].get("focus_time", "上午")),
        )
        ok = st.form_submit_button("更新設定")

    if ok:
        save_profile(
            uid,
            name=name,
            age=int(age),
            prefs={
                "reminder_day": reminder_day,
                "summary_style": summary_style,
                "focus_time": focus_time,
            },
        )
        st.success("設定已更新。")

    st.download_button(
        "下載我的資料（JSON）",
        export_user_data(uid),
        file_name="quietmind_export.json",
        mime="application/json",
    )

    danger = st.checkbox("我知道刪除後無法復原")
    if st.button("刪除我的帳號與所有資料"):
        if not danger:
            st.error("請先勾選確認。")
        else:
            delete_user_data(uid)
            st.session_state.auth_user_id = None
            go("home")
            st.rerun()

    footer_nav()


def page_error():
    app_header("發生錯誤")
    st.error("系統暫時無法完成這個動作，請稍後再試。")


def page_404():
    app_header("找不到頁面")
    if st.button("回首頁"):
        go("home")
        st.rerun()


routes = {
    "home": page_home,
    "suitability": page_suitability,
    "under18": page_under18,
    "privacy": page_privacy,
    "register": page_register,
    "login": page_login,
    "onboarding": page_onboarding,
    "dashboard": page_dashboard,
    "checkin": page_checkin,
    "decision_check": page_decision_check,
    "weekly_review": page_weekly_review,
    "reports": page_reports,
    "toolbox": page_toolbox,
    "resources": page_resources,
    "crisis": page_crisis,
    "settings": page_settings,
    "error": page_error,
}

routes.get(st.session_state.route, page_404)()