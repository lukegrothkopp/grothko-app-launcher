# app.py
from pathlib import Path
import streamlit as st

# --- Paths ---
LOGO_PATH = Path(__file__).parent / "assets" / "header_logo.png"

# --- Page config (sets browser tab icon too) ---
st.set_page_config(
    page_title="Grothko • App Launcher",
    page_icon=str(LOGO_PATH),   # can be emoji, URL, or local image path
    layout="wide",
)

# --- Header with logo on the left ---
col1, col2 = st.columns([0.8, 12], vertical_alignment="center")
with col1:
    st.image(str(LOGO_PATH), width=68)   # adjust width as you like
with col2:
    st.markdown("## Grothko App Launcher")
    st.caption("One place to access all your tools")

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

st.set_page_config(page_title="Grothko • App Launcher", page_icon="🚀", layout="wide")

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
        "url": "https://bank-customer-support-agent.streamlit.app/",
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
        "url": "https://your-travel-planner.streamlit.app/",
        "tags": ["Travel", "Planner"],
        "emoji": "🧭",
    },
]

# ----------------- UI -----------------
st.title("🚀 Grothko App Launcher")
st.caption("One place to access all your tools.")

# logo banner
# st.image("assets/header_logo.png", use_container_width=False)

# Quick filter
q = st.text_input("Search apps", placeholder="Type a name or tag…").strip().lower()

def matches(app, query):
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
            st.container(border=True)
            st.markdown(f"### {app['emoji']} {app['name']}")
            st.write(app["desc"])
            if app.get("tags"):
                st.markdown(
                    " ".join([f"`{t}`" for t in app["tags"]])
                )
            # Streamlit >=1.30 has st.link_button; fall back to markdown link if needed.
            try:
                st.link_button("Open app", app["url"])
            except Exception:
                st.markdown(f"[Open app]({app['url']})")

st.divider()
st.markdown(
    "Need access or want to add an app? Email **support@grothko.com**."
)
