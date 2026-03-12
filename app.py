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
        --bg: #f6f7f9;
        --card: #ffffff;
        --text: #182028;
        --muted: #5f6b76;
        --line: #dde3e8;
        --accent: #314c63;
        --soft: #eef2f6;
        --safe: #fff3f3;
        --green-bg: #edf7ef;
        --green-text: #245638;
        --yellow-bg: #fff7df;
        --yellow-text: #8a5c00;
        --orange-bg: #fff0e2;
        --orange-text: #975116;
        --red-bg: #fdecec;
        --red-text: #8e3535;
    }
    .stApp {
        background: var(--bg);
        color: var(--text);
    }
    .block-container {
        max-width: 720px;
        padding-top: 1rem;
        padding-bottom: 7rem;
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
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    .qm-page-intro {
        color: var(--muted);
        margin-top: -4px;
        margin-bottom: 16px;
    }
    .qm-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 18px;
        margin: 10px 0;
    }
    .qm-minimal-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 26px;
        padding: 26px 20px;
        margin: 8px 0 16px 0;
        text-align: center;
    }
    .qm-minimal-title {
        font-size: 34px;
        font-weight: 700;
        margin: 0 0 10px 0;
    }
    .qm-minimal-sub {
        color: var(--muted);
        margin: 0;
    }
    .qm-top-actions {
        display:flex;
        gap:8px;
        margin-bottom: 10px;
    }
    .qm-alert {
        background: var(--safe);
        border: 1px solid #f0cccc;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }
    .qm-result {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 18px;
        margin-top: 14px;
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
    .qm-grid-note {
        color: var(--muted);
        font-size: 14px !important;
    }
    .stButton > button, .stDownloadButton > button, .stLinkButton > a {
        width: 100%;
        min-height: 50px;
        border-radius: 16px;
        border: 1px solid var(--line);
        font-weight: 700;
        background: #fff;
        color: var(--text) !important;
    }
    .stTextInput input, .stNumberInput input, .stTextArea textarea, div[data-baseweb="select"] {
        background: #ffffff !important;
        border-color: var(--line) !important;
        color: var(--text) !important;
    }
    .stRadio label, .stSelectbox label, .stCheckbox label, .stSlider label {
        font-weight: 600 !important;
        color: var(--text) !important;
    }
    .qm-footer-nav {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 999;
        background: rgba(255,255,255,0.96);
        backdrop-filter: blur(10px);
        border-top: 1px solid var(--line);
        padding: 8px 10px calc(8px + env(safe-area-inset-bottom));
    }
    .qm-footer-wrap {
        max-width: 720px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
    }
    .qm-nav-link {
        text-decoration: none;
        text-align: center;
        color: var(--muted) !important;
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 8px 4px;
        font-size: 12px !important;
    }
    .qm-nav-cta {
        background: var(--soft);
        color: var(--text) !important;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


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
            time_pressure, result, reasons
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        f"SELECT created_at, calm, stress, clarity, focus, context, result FROM checkins WHERE user_id = ? ORDER BY id DESC LIMIT {int(limit)}",
        c,
        params=(uid,),
    )
    c.close()
    return df


def get_last_weeklies(uid, limit=8):
    c = conn()
    df = pd.read_sql_query(
        f"SELECT created_at, summary, review_json FROM weekly_reviews WHERE user_id = ? ORDER BY id DESC LIMIT {int(limit)}",
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


init_db()
for k, v in {
    "route": "home",
    "auth_user_id": None,
    "wizard_step": 1,
    "weekly_step": 1,
    "weekly_review_draft": {},
}.items():
    st.session_state.setdefault(k, v)


def go(route: str):
    st.session_state.route = route


def app_header(title=None, logged=False, subtitle=None):
    c1, c2 = st.columns([1, 1])
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
                "<a href='https://www.google.com' target='_self' class='qm-nav-link' style='display:block;padding:11px 4px;'>快速離開</a>",
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
    st.markdown(
        """
        <div class="qm-footer-nav">
          <div class="qm-footer-wrap">
            <a class="qm-nav-link" href="?nav=dashboard">首頁</a>
            <a class="qm-nav-link qm-nav-cta" href="?nav=checkin">校準</a>
            <a class="qm-nav-link" href="?nav=weekly_review">回顧</a>
            <a class="qm-nav-link" href="?nav=decision_check">決策</a>
            <a class="qm-nav-link" href="?nav=settings">我的</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def handle_query_nav():
    nav = st.query_params.get("nav")
    if nav:
        st.session_state.route = nav
        st.query_params.clear()


def checkin_result(calm, stress, clarity, focus):
    score = calm + clarity + focus - stress
    if stress >= 4 and (clarity <= 2 or focus <= 2):
        return "失衡", "先不要做重大決定。"
    if score >= 10 and stress <= 2:
        return "穩定", "照原計畫走。"
    return "偏緊", "先做 2 分鐘恢復。"


def decision_result(sleep_ok, emotion_high, self_describe, time_pressure):
    reasons = []
    risk = 0
    if not sleep_ok:
        reasons.append("睡眠不足")
        risk += 1
    if emotion_high:
        reasons.append("目前情緒偏高")
        risk += 2
    if not self_describe:
        reasons.append("還無法清楚描述自己的狀態")
        risk += 1
    if time_pressure:
        reasons.append("你正在被時間追著跑")
        risk += 1
    if risk >= 4:
        return "紅燈", reasons, "先穩定，再決定"
    if risk == 3:
        return "橘燈", reasons, "先找第二意見"
    if risk >= 1:
        return "黃燈", reasons, "建議先延後"
    return "綠燈", reasons, "可以做決定"


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


def require_login():
    if not st.session_state.auth_user_id:
        st.warning("請先登入。")
        go("login")
        st.rerun()


def onboarding_complete(uid: int) -> bool:
    data = get_profile(uid)["onboarding"]
    required = ["goal", "who5", "bsrs5", "dimensions", "preferences_done", "confirmed"]
    return all(k in data for k in required)


def mood_message(last_result: str | None):
    mapping = {
        None: "先做一次 30 秒校準。",
        "穩定": "你今天狀態相對穩，可以照原計畫走。",
        "偏緊": "你今天偏緊，先不要急著做重要決定。",
        "失衡": "你今天明顯失衡，先穩定，再決定。",
    }
    return mapping.get(last_result, "先做一次 30 秒校準。")


def dimension_suggestion(status, improve):
    if status <= 2:
        return "先降負荷"
    if improve >= 4:
        return "先做一個小調整"
    return "先維持"


# ---------- pages ----------
def page_home():
    app_header(subtitle="安靜、直白、可信任的個人控制台")
    st.markdown(
        """
        <div class='qm-minimal-card'>
            <div class='qm-minimal-title'>先看見自己</div>
            <p class='qm-minimal-sub'>再做重要決定</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.auth_user_id:
        if st.button("進入今天首頁"):
            go("dashboard")
            st.rerun()
        if st.button("30 秒校準"):
            go("checkin")
            st.rerun()
        if st.button("做決策前檢查"):
            go("decision_check")
            st.rerun()
        if st.button("每週回顧"):
            go("weekly_review")
            st.rerun()
    else:
        if st.button("開始使用"):
            go("suitability")
            st.rerun()
        if st.button("登入"):
            go("login")
            st.rerun()
        if st.button("看心理資源"):
            go("resources")
            st.rerun()


def page_suitability():
    app_header("這個服務適合你嗎", subtitle="先用 4 個問題判斷現在最適合的入口")
    with st.form("suitability_form"):
        q1 = st.radio("你現在是想整理近期狀態，還是需要立即幫助？", ["整理近期狀態", "需要立即幫助"])
        q2 = st.radio("你是否已滿 18 歲？", ["是", "否"])
        q3 = st.selectbox("你目前最困擾的是什麼？", ["壓力", "焦慮", "分心", "空洞", "做決定很亂", "其他"])
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
    app_header("目前完整流程僅開放 18+", subtitle="你仍然可以先查看一般資源與危機支援")
    if st.button("看一般資源"):
        go("resources")
        st.rerun()
    if st.button("看危機支援"):
        go("crisis")
        st.rerun()


def page_privacy():
    app_header("隱私與安全", subtitle="這不是法律頁，而是白話版的信任說明")
    items = [
        ("我們收什麼資料", "帳號、你主動填寫的問卷、校準、決策檢查與回顧資料。"),
        ("為什麼要收", "用來生成你的個人首頁、趨勢摘要與回顧結果。"),
        ("哪些必要，哪些選填", "帳號與主要流程資料是必要；備註與偏好可調整。"),
        ("誰可以看到", "預設只有你自己可看到；未經你主動同意，不會分享給他人。"),
        ("怎麼刪除與匯出", "設定頁可匯出資料，也可刪除帳號與歷史資料。"),
    ]
    for title, text in items:
        st.markdown(f"<div class='qm-card'><strong>{title}</strong><p>{text}</p></div>", unsafe_allow_html=True)
    st.warning("本服務不是診斷或治療，也不取代專業協助。")
    if st.button("我了解，前往註冊"):
        go("register")
        st.rerun()


def page_register():
    app_header("註冊")
    with st.form("register_form"):
        name = st.text_input("你的稱呼")
        email = st.text_input("Email")
        age = st.number_input("年齡", min_value=18, max_value=120, value=18)
        password = st.text_input("密碼", type="password")
        consent = st.checkbox("我同意本服務依隱私說明處理我主動提供的敏感資料")
        ok = st.form_submit_button("建立帳號")
    if ok:
        errors = []
        if not email or "@" not in email:
            errors.append("請輸入有效 Email。")
        if len(password) < 6:
            errors.append("密碼至少 6 碼。")
        if not consent:
            errors.append("請先同意敏感資料處理說明。")
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
    app_header("登入")
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
        st.subheader("Step 1｜使用目標")
        goal = st.radio("你現在最想改善什麼？", ["更穩定", "更專注", "少一點空洞", "不要在亂的時候做決定"])
        if st.button("下一步"):
            data["goal"] = goal
            save_profile(uid, onboarding=data)
            st.session_state.wizard_step = 2
            st.rerun()

    elif step == 2:
        st.subheader("Step 2｜WHO-5 基線")
        st.caption("目的：抓近期心理福祉。0 = 從未，5 = 一直如此")
        items = []
        questions = [
            "我感到心情愉快且精神不錯",
            "我感到平靜而放鬆",
            "我感到有活力、醒來時精神不錯",
            "我的日常生活中有讓我感到有興趣的事",
            "我覺得每天都有值得期待的事",
        ]
        for q in questions:
            items.append(st.slider(q, 0, 5, 2))
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步"):
                st.session_state.wizard_step = 1
                st.rerun()
        with c2:
            if st.button("下一步"):
                raw, pct = score_who5(items)
                data["who5"] = {"items": items, "raw": raw, "percent": pct}
                save_profile(uid, onboarding=data)
                st.session_state.wizard_step = 3
                st.rerun()

    elif step == 3:
        st.subheader("Step 3｜BSRS-5 基線")
        st.caption("目的：抓近期情緒困擾與分流。0 = 完全沒有，4 = 非常嚴重")
        items = []
        questions = [
            "感到緊張不安",
            "感到憂鬱、心情低落",
            "容易動怒或煩躁",
            "覺得比不上別人",
            "睡眠困擾",
        ]
        for q in questions:
            items.append(st.slider(q, 0, 4, 1))
        suicide = st.slider("附加題：有沒有出現傷害自己想法？", 0, 4, 0)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="back_bsrs"):
                st.session_state.wizard_step = 2
                st.rerun()
        with c2:
            if st.button("下一步", key="next_bsrs"):
                total, level = score_bsrs5(items, suicide)
                data["bsrs5"] = {"items": items, "suicide": suicide, "total": total, "level": level}
                save_profile(uid, onboarding=data)
                if level == "高風險":
                    go("crisis")
                else:
                    st.session_state.wizard_step = 4
                st.rerun()

    elif step == 4:
        st.subheader("Step 4｜六維度生活盤點")
        dims = ["工作/學業", "關係", "健康/睡眠", "學習/專注", "休閒/恢復", "成長/意義"]
        dim_data = {}
        for d in dims:
            st.markdown(f"##### {d}")
            status = st.slider(f"{d}：現在的狀態", 1, 5, 3, key=f"{d}_status")
            improve = st.slider(f"{d}：最想改善程度", 1, 5, 3, key=f"{d}_improve")
            dim_data[d] = {"status": status, "improve": improve}
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="back_dim"):
                st.session_state.wizard_step = 3
                st.rerun()
        with c2:
            if st.button("下一步", key="next_dim"):
                data["dimensions"] = dim_data
                save_profile(uid, onboarding=data)
                st.session_state.wizard_step = 5
                st.rerun()

    elif step == 5:
        st.subheader("Step 5｜偏好設定")
        reminder_day = st.selectbox("你想每週哪天收到回顧提醒？", ["週一", "週二", "週三", "週四", "週五", "週六", "週日"])
        summary_style = st.radio("你喜歡看文字摘要還是圖表？", ["文字摘要", "圖表", "都可以"])
        focus_time = st.selectbox("你什麼時段通常最能專心？", ["清晨", "上午", "下午", "晚上", "不固定"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="back_pref"):
                st.session_state.wizard_step = 4
                st.rerun()
        with c2:
            if st.button("下一步", key="next_pref"):
                save_profile(uid, prefs={"reminder_day": reminder_day, "summary_style": summary_style, "focus_time": focus_time})
                data["preferences_done"] = True
                save_profile(uid, onboarding=data)
                st.session_state.wizard_step = 6
                st.rerun()

    elif step == 6:
        st.subheader("Step 6｜檢查答案")
        st.markdown(f"<div class='qm-card'><strong>使用目標</strong><p>{data.get('goal', '未填')}</p></div>", unsafe_allow_html=True)
        who5 = data.get("who5", {})
        bsrs5 = data.get("bsrs5", {})
        st.markdown(f"<div class='qm-card'><strong>WHO-5</strong><p>{who5.get('percent', '未填')}%</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='qm-card'><strong>BSRS-5</strong><p>{bsrs5.get('total', '未填')} 分｜{bsrs5.get('level', '未填')}</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='qm-card'><strong>六維度與偏好</strong><p>已完成填寫</p></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="back_check"):
                st.session_state.wizard_step = 5
                st.rerun()
        with c2:
            if st.button("確認並進入 Dashboard", key="done_check"):
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
    app_header("Dashboard", logged=True, subtitle="今天只看必要的資訊")
    profile = get_profile(uid)
    prefs = profile["prefs"] or {}
    dims = profile["onboarding"].get("dimensions", {})
    checkins = get_last_checkins(uid, 8)
    latest_result = None if checkins.empty else checkins.iloc[0]["result"]

    st.markdown(
        f"<div class='qm-card'><strong>今天的問候</strong><p>{mood_message(latest_result)}</p></div>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("30 秒校準"):
            go("checkin")
            st.rerun()
    with c2:
        if st.button("做決策前檢查"):
            go("decision_check")
            st.rerun()

    st.subheader("六維度總覽")
    if dims:
        items = list(dims.items())
        cols = st.columns(2)
        for i, (title, item) in enumerate(items):
            arrow = "↑" if item["improve"] >= 4 else "→"
            suggestion = dimension_suggestion(item["status"], item["improve"])
            with cols[i % 2]:
                st.markdown(
                    f"<div class='qm-card'><strong>{title}</strong><p>本週狀態：{item['status']}/5</p><p>趨勢：{arrow}</p><p>一句建議：{suggestion}</p></div>",
                    unsafe_allow_html=True,
                )

    st.subheader("本週模式")
    focus_time = prefs.get("focus_time", "上午")
    st.markdown(
        f"<div class='qm-card'><p>你最近最穩的時段：<strong>{focus_time}</strong></p><p>你最近最容易失衡的情境：<strong>睡前滑手機後</strong></p></div>",
        unsafe_allow_html=True,
    )

    st.subheader("今日只給一個建議")
    st.markdown("<div class='qm-card'><strong>今晚 11 點後，不要再進高刺激內容。</strong></div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        if st.button("心理資源"):
            go("resources")
            st.rerun()
    with c4:
        if st.button("我的報告"):
            go("reports")
            st.rerun()
    footer_nav()


def page_checkin():
    require_login()
    app_header("30 秒校準", logged=True, subtitle="只做 5 個快速問題")
    uid = st.session_state.auth_user_id
    with st.form("checkin_form"):
        calm = st.slider("你現在比較平靜還是緊繃？（越高越平靜）", 1, 5, 3)
        stress = st.slider("你現在壓力高嗎？（越高壓力越高）", 1, 5, 3)
        clarity = st.slider("你現在腦袋清楚嗎？", 1, 5, 3)
        focus = st.slider("你現在能專心嗎？", 1, 5, 3)
        context = st.selectbox("你現在在哪個情境？", ["起床後", "通勤中", "工作/上課前", "午間", "下班/下課後", "睡前", "其他"])
        note = st.text_area("備註（選填）")
        ok = st.form_submit_button("看結果")
    if ok:
        result, advice = checkin_result(calm, stress, clarity, focus)
        insert_checkin(uid, calm, stress, clarity, focus, context, note, result)
        st.markdown(f"<div class='qm-card'><strong>結果：{result}</strong><p>{advice}</p></div>", unsafe_allow_html=True)
    footer_nav()


def page_decision_check():
    require_login()
    app_header("決策前檢查", logged=True, subtitle="先看狀態，再做決定")
    uid = st.session_state.auth_user_id
    with st.form("decision_form"):
        d_type = st.selectbox("你現在要做什麼類型的決定？", ["工作/學業", "關係", "金錢", "健康", "搬遷/轉換", "其他"])
        sleep_ok = st.radio("昨晚睡得夠嗎？", ["夠", "不夠"], horizontal=True) == "夠"
        emotion_high = st.radio("你現在情緒強度高嗎？", ["低", "高"], horizontal=True) == "高"
        self_describe = st.radio("你現在能清楚描述自己狀態嗎？", ["能", "不能"], horizontal=True) == "能"
        time_pressure = st.radio("你現在是不是被時間追著跑？", ["不是", "是"], horizontal=True) == "是"
        ok = st.form_submit_button("看我的狀態")
    if ok:
        result, reasons, advice = decision_result(sleep_ok, emotion_high, self_describe, time_pressure)
        insert_decision(
            uid,
            {
                "decision_type": d_type,
                "sleep_ok": int(sleep_ok),
                "emotion_high": int(emotion_high),
                "self_describe": int(self_describe),
                "time_pressure": int(time_pressure),
                "result": result,
                "reasons": reasons,
            },
        )
        light_map = {
            "綠燈": ("qm-green", "你現在狀態相對穩，可以做決定。"),
            "黃燈": ("qm-yellow", "你現在不是最適合做決定的狀態。"),
            "橘燈": ("qm-orange", "你現在不適合單獨做判斷，先找第二意見。"),
            "紅燈": ("qm-red", "你現在需要先穩定自己，再回來做決定。"),
        }
        cls, desc = light_map[result]
        suggestions = {
            "綠燈": ["照原計畫往下做", "把決定寫成一句話", "做完後再回頭確認一次"],
            "黃燈": ["先做 2 分鐘呼吸", "30 分鐘後再看", "把現在的擔心先寫下來"],
            "橘燈": ["先找一個人討論", "先列出兩個替代方案", "不要在情緒高點拍板"],
            "紅燈": ["先做 2 分鐘呼吸", "先離開高刺激情境", "今天先不要做重大決定"],
        }
        reason_html = "".join([f"<li>{r}</li>" for r in reasons]) if reasons else "<li>目前沒有明顯風險訊號</li>"
        suggestion_html = "".join([f"<li>{s}</li>" for s in suggestions[result]])
        st.markdown(
            f"""
            <div class='qm-result'>
                <div class='qm-light {cls}'>你的狀態：{result}</div>
                <p>{desc}</p>
                <p><strong>原因：</strong></p>
                <ul>{reason_html}</ul>
                <p><strong>建議：</strong></p>
                <ul>{suggestion_html}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"目前建議：{advice}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.button("先做 2 分鐘呼吸", key=f"breathe_{result}")
        with c2:
            st.button("30 分鐘後再看", key=f"later_{result}")
        with c3:
            st.button("找一個人討論", key=f"talk_{result}")
    footer_nav()


def page_weekly_review():
    require_login()
    app_header("每週回顧", logged=True, subtitle="每頁只做一件事")
    uid = st.session_state.auth_user_id
    step = st.session_state.weekly_step
    review = st.session_state.get("weekly_review_draft", {})
    st.progress(step / 4)

    if step == 1:
        st.subheader("A. 本週總覽")
        stability = st.slider("這週整體穩定度", 1, 5, 3)
        emotion = st.selectbox("最常見情緒", ["平靜", "焦躁", "疲憊", "空洞", "煩躁", "混亂"])
        unstable_time = st.selectbox("最容易失衡時段", ["清晨", "上午", "下午", "晚上", "睡前", "不固定"])
        if st.button("下一步", key="wr1"):
            review["overview"] = {"stability": stability, "emotion": emotion, "unstable_time": unstable_time}
            st.session_state.weekly_review_draft = review
            st.session_state.weekly_step = 2
            st.rerun()

    elif step == 2:
        st.subheader("B. 六維度檢視")
        dims = ["工作/學業", "關係", "健康/睡眠", "學習/專注", "休閒/恢復", "成長/意義"]
        data = {}
        for d in dims:
            state = st.selectbox(f"{d}：這週大致如何？", ["偏差", "普通", "穩定"], key=f"state_{d}")
            impact = st.text_input(f"{d}：最影響你的是什麼？", key=f"impact_{d}")
            adjust = st.text_input(f"{d}：下週最想調整什麼？", key=f"adjust_{d}")
            data[d] = {"state": state, "impact": impact, "adjust": adjust}
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="wr2_back"):
                st.session_state.weekly_step = 1
                st.rerun()
        with c2:
            if st.button("下一步", key="wr2_next"):
                review["dimensions"] = data
                st.session_state.weekly_review_draft = review
                st.session_state.weekly_step = 3
                st.rerun()

    elif step == 3:
        st.subheader("C. 模式辨識")
        trigger = st.text_input("哪個情境最容易打亂你？")
        helpful = st.text_input("哪個行為最有幫助？")
        best_time = st.selectbox("哪個時段最適合做重要事？", ["清晨", "上午", "下午", "晚上", "不固定"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="wr3_back"):
                st.session_state.weekly_step = 2
                st.rerun()
        with c2:
            if st.button("下一步", key="wr3_next"):
                review["patterns"] = {"trigger": trigger, "helpful": helpful, "best_time": best_time}
                st.session_state.weekly_review_draft = review
                st.session_state.weekly_step = 4
                st.rerun()

    elif step == 4:
        st.subheader("D. 下週只選一個實驗")
        experiment = st.radio(
            "選一個就好",
            [
                "起床後 30 分鐘不進高刺激內容",
                "睡前 30 分鐘降刺激",
                "重要任務放到高專注時段",
                "每天做一次 30 秒校準",
            ],
        )
        st.markdown("<div class='qm-card'><strong>檢查答案</strong><p>確認後再完成本週回顧。</p></div>", unsafe_allow_html=True)
        if review.get("overview"):
            st.markdown(f"<div class='qm-card'><p>本週整體穩定度：{review['overview']['stability']}/5</p><p>最常見情緒：{review['overview']['emotion']}</p><p>最容易失衡時段：{review['overview']['unstable_time']}</p></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("上一步", key="wr4_back"):
                st.session_state.weekly_step = 3
                st.rerun()
        with c2:
            if st.button("完成回顧", key="wr4_done"):
                review["experiment"] = experiment
                summary = f"本週最穩時段：{review.get('patterns', {}).get('best_time', '未填')}；下週實驗：{experiment}"
                insert_weekly(uid, review, summary)
                st.session_state.weekly_review_draft = {}
                st.session_state.weekly_step = 1
                st.markdown(f"<div class='qm-card'><strong>已完成本週回顧</strong><p>{summary}</p></div>", unsafe_allow_html=True)
    footer_nav()


def page_reports():
    require_login()
    app_header("報告中心", logged=True, subtitle="先用簡版摘要就好")
    uid = st.session_state.auth_user_id
    checkins = get_last_checkins(uid, 20)
    weeklies = get_last_weeklies(uid, 12)
    st.subheader("趨勢摘要")
    if not checkins.empty:
        chart_df = checkins.copy()
        chart_df["created_at"] = pd.to_datetime(chart_df["created_at"])
        chart_df = chart_df.sort_values("created_at")
        st.line_chart(chart_df.set_index("created_at")[["calm", "stress", "clarity", "focus"]])
        st.caption("這張圖只表達一件事：最近幾次校準波動。")
    else:
        st.markdown("<div class='qm-card'><p>還沒有資料，先做一次 30 秒校準。</p></div>", unsafe_allow_html=True)

    st.subheader("週報列表")
    if weeklies.empty:
        st.markdown("<div class='qm-card'><p>你還沒有週報。</p></div>", unsafe_allow_html=True)
    else:
        for _, row in weeklies.iterrows():
            st.markdown(f"<div class='qm-card'><strong>{row['created_at'][:10]}</strong><p>{row['summary']}</p></div>", unsafe_allow_html=True)
    footer_nav()


def page_toolbox():
    require_login()
    app_header("工具箱", logged=True, subtitle="不用學習，只要執行")
    tools = [
        ("2 分鐘呼吸重置", "吸氣 4 秒，停 2 秒，吐氣 6 秒，連續 10 次。"),
        ("睡前降刺激流程", "睡前 30 分鐘關掉高刺激內容，只保留低亮度與低資訊量。"),
        ("社群滑完後回神", "把手機放下 60 秒，說出你現在的情緒、身體感受、下一步。"),
        ("工作前進入專注模式", "先做 30 秒校準，再只選一件最重要的任務。"),
    ]
    for title, text in tools:
        st.markdown(f"<div class='qm-card'><strong>{title}</strong><p>{text}</p></div>", unsafe_allow_html=True)
    footer_nav()


def page_resources():
    app_header("心理資源 / 轉介", logged=bool(st.session_state.auth_user_id), subtitle="需要時很快連到正確資源")
    st.markdown("<div class='qm-alert'><strong>立即危機</strong><p>若你有立即危險或強烈自傷念頭，請優先使用下方危機支援。</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("撥打 1925", "tel:1925")
    with c2:
        st.link_button("撥打 1995", "tel:1995")
    city = st.selectbox("縣市", ["不限", "台北市", "新北市", "桃園市", "台中市", "台南市", "高雄市", "其他"])
    mode = st.selectbox("線上 / 實體", ["不限", "線上", "實體"])
    subsidy = st.selectbox("補助", ["不限", "可補助", "自費"])
    service_type = st.selectbox("服務類型", ["一般諮詢", "壓力調適", "睡眠", "情緒支持"])
    st.caption(f"目前篩選：{city} / {mode} / {subsidy} / {service_type}")
    resources = [
        ("青壯心理健康支持方案", "適合先找補助與基本資源的人。"),
        ("社區心理衛生中心", "適合需要地方性支持與轉介資訊。"),
        ("心理諮商所", "適合已經想找專業一對一支持的人。"),
        ("線上 / 實體服務", "依你的地點與偏好選擇。"),
    ]
    for title, text in resources:
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
    if st.button("我現在安全，回到服務"):
        go("dashboard" if st.session_state.auth_user_id else "home")
        st.rerun()
    if st.button("我只是想找一般資源"):
        go("resources")
        st.rerun()


def page_settings():
    require_login()
    uid = st.session_state.auth_user_id
    profile = get_profile(uid)
    app_header("我的設定", logged=True)
    with st.form("settings_form"):
        name = st.text_input("稱呼", value=profile["name"])
        age = st.number_input("年齡", min_value=18, max_value=120, value=int(profile["age"] or 18))
        reminder_day = st.selectbox("回顧提醒日", ["週一", "週二", "週三", "週四", "週五", "週六", "週日"], index=["週一", "週二", "週三", "週四", "週五", "週六", "週日"].index(profile["prefs"].get("reminder_day", "週日")))
        summary_style = st.radio("摘要偏好", ["文字摘要", "圖表", "都可以"], index=["文字摘要", "圖表", "都可以"].index(profile["prefs"].get("summary_style", "文字摘要")))
        focus_time = st.selectbox("高專注時段", ["清晨", "上午", "下午", "晚上", "不固定"], index=["清晨", "上午", "下午", "晚上", "不固定"].index(profile["prefs"].get("focus_time", "上午")))
        ok = st.form_submit_button("更新設定")
    if ok:
        save_profile(uid, name=name, age=int(age), prefs={"reminder_day": reminder_day, "summary_style": summary_style, "focus_time": focus_time})
        st.success("設定已更新。")
    st.download_button("下載我的資料（JSON）", export_user_data(uid), file_name="quietmind_export.json", mime="application/json")
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


handle_query_nav()
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
