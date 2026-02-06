import streamlit as st
import database as db
from datetime import date

def show_meeting_manager():
    st.title("📅 Meeting & Call Scheduling Module")

    # ==========================================
    # 1. SCHEDULE NEW MEETING (Requirement 9.2)
    # ==========================================
    with st.expander("➕ Schedule New Meeting/Call", expanded=True):
        
        # Req 9.2 Feature: Select Associated Task
        tasks = db.fetch_tasks()
        task_options = {} # Dict to map "Title" -> ID
        if not tasks.empty:
            task_list = ["-- Select Task --"] + tasks.apply(lambda x: f"{x['id']} - {x['task_title']}", axis=1).tolist()
        else:
            task_list = ["No Tasks Available"]

        with st.form("schedule_meeting_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            # Field: Task Selection
            selected_task_str = col1.selectbox("Associate with Task*", task_list)
            
            # Req 9.2 Feature: Choose Call/Meeting Type
            m_type = col2.selectbox("Meeting Type*", ["Video Call (Zoom/Teams)", "Voice Call", "In-Person Meeting", "Client Presentation"])

            # Req 9.2 Feature: Define Title & Description
            m_title = st.text_input("Meeting Title*", placeholder="e.g. Weekly Status Sync")
            m_desc = st.text_area("Description / Agenda", placeholder="Topics to discuss...")
            
            # Additional useful fields
            m_participants = st.text_input("Participants", placeholder="John, Sarah, DevOps Team")
            
            # Req 9.2 Feature: Set Date and Time
            c3, c4 = st.columns(2)
            m_date = c3.date_input("Date*", min_value=date.today())
            m_time = c4.time_input("Time*")
            
            m_link = st.text_input("Meeting Link (Optional)", placeholder="https://zoom.us/j/...")

            if st.form_submit_button("📅 Schedule Now", type="primary"):
                if m_title and selected_task_str != "-- Select Task --":
                    # Extract ID from string "1 - Task Title"
                    task_id = int(selected_task_str.split(" - ")[0])
                    
                    db.add_meeting(task_id, m_title, m_type, m_desc, m_participants, m_date, m_time, m_link)
                    st.success("✅ Meeting Scheduled Successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please select a Task and enter a Title.")

    st.divider()

    # ==========================================
    # 2. UPCOMING MEETINGS LIST
    # ==========================================
    st.subheader("🗓️ Scheduled Meetings")
    
    meetings_df = db.fetch_meetings()
    
    if not meetings_df.empty:
        # Display as a clean table
        st.dataframe(
            meetings_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "task_title": st.column_config.TextColumn("Related Task", width="medium"),
                "title": st.column_config.TextColumn("Meeting Title", width="medium"),
                "meeting_type": st.column_config.TextColumn("Type", width="small"),
                "meeting_date": "Date",
                "meeting_time": "Time",
                "link": st.column_config.LinkColumn("Join Link")
            }
        )
        
        # Delete Action
        col_del, _ = st.columns([1, 3])
        with col_del:
            m_id_to_del = st.selectbox("Select Meeting ID to Cancel", meetings_df['id'])
            if st.button("❌ Cancel Meeting"):
                db.delete_meeting(m_id_to_del)
                st.warning("Meeting Cancelled.")
                st.rerun()
    else:
        st.info("No upcoming meetings scheduled.")