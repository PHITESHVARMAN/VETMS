import streamlit as st
import dashboard
import task_manager
import task_editor
import task_detail
import meeting_manager
import voice_assistant
import team_manager       # <--- New Import for Module 11
import database as db

# ==========================================
# 1. GLOBAL PAGE SETTINGS
# ==========================================
st.set_page_config(page_title="VETMS System", page_icon="🎙️", layout="wide")

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

def update_page():
    st.session_state.page = st.session_state.nav_selection

# ==========================================
# 2. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("VETMS Navigation")

# Full list of modules
page_options = [
    "Dashboard", 
    "Task Manager", 
    "Edit & Update", 
    "Task Detail", 
    "Meeting Scheduler", 
    "Team Management",   # <--- Added to Sidebar
    "Voice Commands"
]

st.sidebar.radio(
    "Go To:", 
    page_options,
    key="nav_selection",
    on_change=update_page,
    index=page_options.index(st.session_state.page) if st.session_state.page in page_options else 0
)

st.sidebar.markdown("---")
st.sidebar.caption("Voice-Enabled Task Management System v1.0")

# ==========================================
# 3. PAGE ROUTING LOGIC
# ==========================================
if st.session_state.page == "Dashboard":
    import importlib
    importlib.reload(dashboard)
    dashboard.show_dashboard()

elif st.session_state.page == "Task Manager":
    task_manager.show_task_manager()

elif st.session_state.page == "Edit & Update":
    task_editor.show_edit_interface()

elif st.session_state.page == "Task Detail":
    task_detail.show_task_detail()

elif st.session_state.page == "Meeting Scheduler":
    meeting_manager.show_meeting_manager()

elif st.session_state.page == "Team Management":   # <--- Routing for Module 11
    team_manager.show_team_management()

elif st.session_state.page == "Voice Commands":
    voice_assistant.show_voice_commands()