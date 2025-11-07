# app.py
import streamlit as st

st.set_page_config(page_title="Grothko • App Launcher", page_icon="🚀", layout="wide")

# ----------------- DATA -----------------
APPS = [
    {
        "name": "InsightForge BI",
        "desc": "AI-powered dashboards and KPI search.",
        "url": "https://your-insightforge-app.streamlit.app/",
        "tags": ["BI", "AI", "Dashboards"],
        "emoji": "📊",
    },
    {
        "name": "Percipient Finance",
        "desc": "13-week cash, BvA, runway.",
        "url": "https://your-percipient-finance.streamlit.app/",
        "tags": ["Finance", "CFO"],
        "emoji": "💵",
    },
    {
        "name": "Healthcare Assistant",
        "desc": "Agentic workflows for patient ops.",
        "url": "https://your-healthcare-assistant.streamlit.app/",
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

# (Optional) logo banner
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
