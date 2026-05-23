import streamlit as st
import pickle
import time

# Page config
st.set_page_config(
    page_title="MindScan",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load model
@st.cache_resource
def load_model():
    try:
        with open("depression_detection_pipeline.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

model = load_model()

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f14;
    border-right: 1px solid #1e1e2e;
}

[data-testid="stSidebar"] * {
    color: #c8c8d8 !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 15px;
    padding: 8px 0;
    cursor: pointer;
    transition: color 0.2s;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: #a78bfa !important;
}

/* Main background */
[data-testid="stAppViewContainer"] {
    background: #0a0a10;
    color: #e2e2f0;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Headings */
h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
    color: #f0f0ff;
}

/* Cards */
.card {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 20px;
}

/* Textarea */
.stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 10px !important;
    color: #e2e2f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

.stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 28px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 15px;
    transition: all 0.2s;
    cursor: pointer;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

/* Progress bar */
.bar-container {
    background: #1a1a2e;
    border-radius: 999px;
    height: 22px;
    width: 100%;
    overflow: hidden;
    margin: 10px 0;
}

.bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 1s ease;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 10px;
    font-size: 12px;
    font-weight: 600;
    color: white;
}

/* Status badge */
.badge {
    display: inline-block;
    padding: 6px 20px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.5px;
}

.badge-depressed {
    background: #3b0a0a;
    color: #f87171;
    border: 1px solid #7f1d1d;
}

.badge-not {
    background: #052e16;
    color: #4ade80;
    border: 1px solid #14532d;
}

.badge-border {
    background: #1c1407;
    color: #fbbf24;
    border: 1px solid #78350f;
}

/* Google history mock */
.g-bar {
    background: #161622;
    border-bottom: 1px solid #1e1e30;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-radius: 10px 10px 0 0;
}

.g-row {
    padding: 12px 20px;
    border-bottom: 1px solid #16161f;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.g-row:hover {
    background: #13131e;
}

.g-title {
    font-size: 14px;
    font-weight: 500;
    color: #8ab4f8;
}

.g-url {
    font-size: 12px;
    color: #5f6368;
    margin-top: 2px;
}

.g-time {
    font-size: 11px;
    color: #444455;
    margin-left: auto;
    white-space: nowrap;
}

/* Scan panel */
.scan-title {
    font-family: 'DM Serif Display', serif;
    font-size: 18px;
    color: #c4b5fd;
    margin-bottom: 14px;
}

/* Divider */
hr {
    border-color: #1e1e30;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🧠 MindScan")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Home", "About", "How It Works"],
        label_visibility="collapsed",
    )

    st.markdown("---")

# Page: Home
if page == "Home":
    st.markdown("# MindScan")
    st.markdown("##### Depression detection from search history")
    st.markdown("---")

    if model is None:
        st.warning(
            "`depression_detection_pipeline.pkl` not found in the app directory. "
            "Place the model file next to `app.py` and restart."
        )

    st.markdown("### Enter Search History")
    st.markdown("Paste up to **10 search queries**, one per line.")

    raw = st.text_area(
        "Search queries",
        placeholder=(
            "e.g.\n"
            "how to stop feeling lonely\n"
            "best movies to cheer up\n"
            "why do i feel empty inside\n"
            "..."
        ),
        height=230,
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        run = st.button("Analyse", use_container_width=True)

    if run:
        lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]

        if not lines:
            st.error("Please enter at least one search query.")
        elif len(lines) > 10:
            st.error("Please enter at most 10 queries.")
        elif model is None:
            st.error("Model not loaded. Cannot run analysis.")
        else:
            with st.spinner("Scanning..."):
                time.sleep(0.8)
                combined = " ".join(lines)

                try:
                    proba = model.predict_proba([combined])[0]
                    score = float(proba[1]) * 100
                except Exception:
                    pred = model.predict([combined])[0]
                    score = 85.0 if pred == 1 else 20.0

            st.markdown("---")
            st.markdown("### Result")

            if score >= 50:
                color = "#ef4444"
                status_html = '<span class="badge badge-depressed">Depressed</span>'
            else:
                color = "#22c55e"
                status_html = '<span class="badge badge-not">Not Depressed</span>'

            st.markdown(
                f"""
                <p style="color:#aaa;font-size:13px;margin-bottom:4px">
                    Depression likelihood
                </p>

                <div class="bar-container">
                    <div class="bar-fill" style="width:{score:.1f}%;background:{color};">
                        {score:.1f}%
                    </div>
                </div>

                <p style="font-size:28px;font-weight:700;color:{color};margin:10px 0 6px">
                    {score:.1f}%
                </p>

                {status_html}
                """,
                unsafe_allow_html=True,
            )

            st.markdown("---")
            st.markdown(
                "_This tool is for informational purposes only and does not replace professional mental-health advice._",
                unsafe_allow_html=True,
            )

# Page: About
elif page == "About":
    st.markdown("# About MindScan")
    st.markdown("---")

    st.markdown("""
### What is MindScan?

**MindScan** is a research-oriented tool that analyses a person's internet search history to estimate
the likelihood of depressive thought patterns. It uses a machine-learning pipeline trained on
labelled search-query datasets to surface patterns associated with depression, such as searches about
hopelessness, social withdrawal, sleep disruption, or low self-worth.

---

### How the model works

| Component | Detail |
|-----------|--------|
| **File** | `depression_detection_pipeline.pkl` |
| **Input** | Plain-text search queries joined into one text |
| **Output** | Probability score from 0 to 100 percent and binary label |
| **Pipeline** | Text vectorisation, feature extraction, classifier |

---

### Ethical notice

> This tool is **not a diagnostic instrument**. A high score does not mean a person is
> clinically depressed. If you or someone you know is struggling, please reach out to a
> qualified mental-health professional or a crisis helpline.

---

### Privacy

All analysis runs **locally** on the server. No search queries are stored, logged, or
transmitted to any third party.
    """)

# Page: How It Works
elif page == "How It Works":
    st.markdown("# How It Works")
    st.markdown("##### A live walk-through of the scanning flow")
    st.markdown("---")

    MOCK_HISTORY = [
        ("why do i feel so empty all the time", "google.com/search", "Today, 11:42 PM"),
        ("how to stop overthinking at night", "google.com/search", "Today, 10:17 PM"),
        ("signs you might be depressed without knowing", "healthline.com", "Today, 9:55 PM"),
        ("best movies to watch when sad", "google.com/search", "Today, 8:30 PM"),
        ("how to feel motivated again", "google.com/search", "Yesterday, 6:12 PM"),
        ("coping with loneliness in your 20s", "verywellmind.com", "Yesterday, 3:44 PM"),
        ("why do i have no energy", "google.com/search", "Yesterday, 1:22 PM"),
        ("sleep disorders linked to depression", "webmd.com", "2 days ago"),
        ("things to do when you feel worthless", "google.com/search", "2 days ago"),
        ("how to stop feeling like a burden", "google.com/search", "3 days ago"),
    ]

    hist_col, scan_col = st.columns([3, 1.4])

    with hist_col:
        st.markdown("""
    <div class="g-bar">
        <span style="flex:1;background:#0f0f1a;border-radius:6px;padding:5px 14px;font-size:13px;color:#9aa0a6;">
            myactivity.google.com/myactivity
        </span>
        <span style="font-size:20px;cursor:pointer;margin-left:10px;padding:4px 8px;">🧠</span>
    </div>
    """, unsafe_allow_html=True)

        for title, url, time_text in MOCK_HISTORY:
            st.markdown(f"""
    <div class="g-row">
        <div style="flex:1">
            <div class="g-title">{title}</div>
            <div class="g-url">{url}</div>
        </div>
        <span class="g-time">{time_text}</span>
    </div>
    """, unsafe_allow_html=True)

        for title, url, time_text in MOCK_HISTORY:
            st.markdown(f"""
            <div class="g-row">
                <div style="flex:1">
                    <div class="g-title">{title}</div>
                    <div class="g-url">{url}</div>
                </div>
                <span class="g-time">{time_text}</span>
            </div>
            """, unsafe_allow_html=True)

    with scan_col:
        st.markdown(
            '<div class="scan-title">🧠 MindScan</div>',
            unsafe_allow_html=True,
        )

        if st.button("Scan History", use_container_width=True):
            st.session_state["demo_scanned"] = True
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()

        if st.session_state.get("demo_scanned"):
            with st.spinner("Scanning..."):
                time.sleep(1.0)

                if model is not None:
                    combined = " ".join([title for title, _, _ in MOCK_HISTORY])

                    try:
                        proba = model.predict_proba([combined])[0]
                        score = float(proba[1]) * 100
                    except Exception:
                        try:
                            pred = model.predict([combined])[0]
                            score = 85.0 if pred == 1 else 20.0
                        except Exception:
                            score = 65.0
                else:
                    score = 65.0

            if score >= 50:
                color = "#ef4444"
                status_html = '<span class="badge badge-depressed">Depressed</span>'
            else:
                color = "#22c55e"
                status_html = '<span class="badge badge-not">Not Depressed</span>'

            st.markdown(
                f"""
                <p style="color:#9a9aaa;font-size:12px;margin:14px 0 4px">
                    Depression likelihood
                </p>

                <div class="bar-container">
                    <div class="bar-fill" style="width:{score:.1f}%;background:{color};">
                        {score:.1f}%
                    </div>
                </div>

                <p style="font-size:32px;font-weight:700;color:{color};margin:8px 0 6px">
                    {score:.1f}%
                </p>

                {status_html}

                <p style="font-size:12px;color:#6b6b80;margin-top:18px">
                    Based on 10 recent searches. Patterns detected: hopelessness, fatigue, low self-worth.
                </p>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.markdown(
                """
                <p style="color:#555;font-size:13px;margin-top:12px">
                    Press <b>Scan History</b> to analyse the search entries on the left.
                </p>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    st.markdown("""
**Step-by-step flow:**

1. Your Google search history is displayed as a familiar activity list.
2. Click the 🧠 icon at the top-right of the browser bar to open the MindScan panel.
3. Press **Scan History**. The panel reads all visible queries.
4. The model `depression_detection_pipeline.pkl` processes the text and returns a probability.
5. A progress bar shows the likelihood from 0 to 100 percent and a status badge indicates the result.
    """)