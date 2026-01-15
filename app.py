# app.py
from pathlib import Path
import streamlit as st

# --- Paths ---
LOGO_PATH = Path(__file__).parent / "assets" / "header_logo.png"

# --- Page config (sets browser tab icon too) ---
st.set_page_config(
    page_title="Grothko • App Launcher",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🚀",
    layout="wide",
)

# --- Header with logo on the left ---
try:
    col1, col2 = st.columns([0.8, 12], vertical_alignment="center")
except TypeError:
    # For older Streamlit versions without vertical_alignment
    col1, col2 = st.columns([0.8, 12])

with col1:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=68)  # adjust width as you like
    else:
        st.write("🚀")

with col2:
    st.markdown("## Grothko App Launcher")

    caption_text = (
        "One place to access all our sample tools, but links may be dormant, click blue button to activate "
        "(some require you to load sample CSV or PDF files to test)."
    )

    st.markdown(
        f"""
        <div style="
            color: #4ade80;                  /* bright green for dark mode */
            font-weight: 600;
            font-size: 0.95rem;
            line-height: 1.35rem;
            padding: 0.5rem 0.75rem;
            border-left: 4px solid #22c55e;  /* accent bar */
            background: rgba(34, 197, 94, 0.10);
            border-radius: 0.5rem;
            margin-top: 0.25rem;
        ">
            {caption_text}
        </div>
        """,
        unsafe_allow_html=True
    )

def require_auth(app_name: str = "App"):
    # 1) Pull secrets
    # Option A: single password string
    single_pw = st.secrets.get("APP_PASSWORD", None)
    # Option B: allowlist of passwords (e.g., per-person)
    allowed_pws = set(st.secrets.get("APP_PASSWORDS", []))

    if "is_authed" not in st.session_state:
        st.session_state.is_authed = False

    # Already authenticated this session
    if st.session_state.is_authed:
        # Optional: tiny logout button in the sidebar
        with st.sidebar:
            if st.button("Logout"):
                st.session_state.is_authed = False
                st.rerun()
        return  # Let the app continue

    st.title(f"🔒 {app_name} – Restricted Access")
    pw = st.text_input("Enter access password", type="password")

    def check(pw_input: str) -> bool:
        if not pw_input:
            return False
        # Match single or any from list
        if single_pw and pw_input == single_pw:
            return True
        if allowed_pws and pw_input in allowed_pws:
            return True
        return False

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Unlock"):
            if check(pw):
                st.session_state.is_authed = True
                st.success("Access granted.")
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

    # Stop executing the rest of the app until authed
    st.stop()

# OPTIONAL: Uncomment to require password for the launcher itself
# require_auth("Grothko App Launcher")

# ----------------- DATA -----------------
APPS = [
    {
        "name": "BIG (Business Intelligence Generator)",
        "desc": "Explore AI-powered BI insights & visualizations!",
        "url": "https://grothko-big.streamlit.app/",
        "tags": ["BI", "AI", "Dashboards"],
        "emoji": "📊",
    },
    {
        "name": "Corporate Scorecard",
        "desc": "Comprehensive view of performance, aligns departmental goals with the overall strategy, and improves communication and accountability.",
        "url": "https://grothko-corporate-scorecard.streamlit.app/",
        "tags": ["Corporate", "Scorecard", "AI", "OKR"],
        "emoji": "🏢",
    },
    {
        "name": "Banking Customer AI Agent",
        "desc": "Classifier → Feedback Handler / Query Handler • Evaluation • Logs • DB Viewer",
        "url": "https://bank-customer-support-agent.streamlit.app/",
        "tags": ["Banking", "Customer", "AI"],
        "emoji": "🏦",
    },
    {
        "name": "Percipient Finance",
        "desc": "KPIs, BvA, runway. Current form requires KPI and Budget CSV files for analysis.",
        "url": "https://grothko-percipient-finance.streamlit.app/",
        "tags": ["Finance", "CFO"],
        "emoji": "💵",
    },
    {
        "name": "Resume Analyzer",
        "desc": "Upload a resume, analyze it against a job description you provide, filter relevant chunks, and search across stored resumes.",
        "url": "https://grothko-resume-analyzer.streamlit.app/",
        "tags": ["Resume", "HR", "Analysis"],
        "emoji": "📑",
    },
    {
        "name": "HR Assistant",
        "desc": "Self-hosted HR policy chatbot. Ingest PDFs, create embeddings, and query in natural language. Streamlit UI, LangChain retriever, Chroma vector store, OpenAI models.",
        "url": "https://grothkoconsulting-hr-assistant.streamlit.app/",
        "tags": ["Resume", "HR", "Analysis"],
        "emoji": "👩🏽‍💼",
    },
    {
        "name": "Healthcare Assistant",
        "desc": "Agentic workflows for patients & clinicians.",
        "url": "https://grothko-agentic-healthcare-assistant.streamlit.app/",
        "tags": ["Healthcare", "Agents"],
        "emoji": "⚕️",
    },
    {
        "name": "Travel Planner",
        "desc": "Itineraries, budgets, and bookings.",
        "url": "https://grothko-travel-planner.streamlit.app/",
        "tags": ["Travel", "Planner"],
        "emoji": "🧭",
    },
]

# ----------------- UI -----------------

# Quick filter
q = st.text_input("Search apps", placeholder="Type a name or tag…").strip().lower()

def matches(app, query: str) -> bool:
    if not query:
        return True
    hay = " ".join([app["name"], app["desc"], " ".join(app["tags"])]).lower()
    return query in hay

filtered = [a for a in APPS if matches(a, q)]

# Grid of app cards
cols_per_row = 2
rows = (len(filtered) + cols_per_row - 1) // cols_per_row
for r in range(rows):
    cols = st.columns(cols_per_row)
    for i, col in enumerate(cols):
        idx = r * cols_per_row + i
        if idx >= len(filtered):
            continue
        app = filtered[idx]
        with col:
            with st.container(border=True):
                st.markdown(f"### {app['emoji']} {app['name']}")
                st.write(app["desc"])
                if app.get("tags"):
                    st.markdown(" ".join([f"`{t}`" for t in app["tags"]]))
                # Streamlit >=1.30 has st.link_button; fall back to markdown link if needed.
                try:
                    st.link_button("Open app", app["url"])
                except Exception:
                    st.markdown(f"[Open app]({app['url']})")

st.divider()
st.markdown("Need access or want to add an app? Email **admin@lrgbllc.org**.")
