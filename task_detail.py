import streamlit as st
import database as db
from datetime import datetime

def show_task_detail():
    st.title("📄 Task Detail View")

    # 1. Select Task
    tasks = db.fetch_tasks()
    
    if tasks.empty:
        st.info("No tasks available.")
        return

    # Dropdown to pick a task
    task_options = tasks.apply(lambda x: f"{x['id']} - {x['task_title']}", axis=1).tolist()
    selected_task_string = st.selectbox("Select Task to View", task_options)
    selected_task_id = int(selected_task_string.split(" - ")[0])

    # 2. Fetch Full Details
    task = db.get_task_by_id(selected_task_id)

    if task:
        st.divider()
        
        # --- REQUIREMENT 8.1: Information Displayed ---
        c1, c2 = st.columns([3, 1])
        c1.subheader(f"📌 {task['task_title']}")
        
        # Badge Logic
        status_color = "gray"
        if task['status'] == "Completed":
            status_color = "green"
        elif task['status'] == "In Progress":
            status_color = "blue"
        elif task['status'] == "Pending":
            status_color = "orange"
            
        c2.markdown(f":{status_color}[**{task['status']}**] | **{task['priority']}** Priority")

        with st.container(border=True):
            st.markdown("### 📝 Description")
            # Safe access to description
            if task.get('description'):
                st.write(task['description'])
            else:
                st.caption("No description provided.")
            
            st.divider()
            
            # Creator & User Info
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**👤 Assigned To:** {task['assigned_user']}")
                st.write(f"**🤖 Created By:** {task.get('created_by', 'System')}")
            with col_b:
                st.write(f"**📅 Deadline:** {task['deadline']}")
                st.write(f"**🕒 Created At:** {task.get('created_at', 'N/A')}")

        # --- REQUIREMENT 8.2: Quick Actions ---
        st.subheader("⚡ Quick Actions")
        qa1, qa2, qa3 = st.columns(3)
        
        with qa1:
            # Action: Mark as Completed
            if task['status'] != "Completed":
                if st.button("✅ Mark as Completed", use_container_width=True):
                    # Keep existing values, just change status
                    db.update_task(
                        task['id'], task['task_title'], task.get('description'), 
                        task['priority'], "Completed", task['assigned_user'], task['deadline']
                    )
                    st.success("Task marked as Completed!")
                    st.rerun()
            else:
                st.button("✅ Already Completed", disabled=True, use_container_width=True)

        with qa2:
            st.info("To Edit: Use 'Edit & Update' in Sidebar")

        with qa3:
            # Action: Delete
            if st.button("🗑️ Delete Task", type="primary", use_container_width=True):
                db.delete_task(task['id'])
                st.warning("Task Deleted.")
                st.rerun()

        st.divider()

        # --- REQUIREMENT 8.3: Meeting Integration ---
        st.subheader("📅 Meeting Integration")
        with st.expander("Schedule a Meeting for this Task", expanded=True):
            with st.form("quick_meeting_form", clear_on_submit=True):
                m_title = st.text_input("Meeting Title", value=f"Discussion: {task['task_title']}")
                m_participants = st.text_input("Participants", placeholder="e.g. John, Sarah, DevOps Team")
                
                mc1, mc2 = st.columns(2)
                m_date = mc1.date_input("Date")
                m_time = mc2.time_input("Time")
                
                m_link = st.text_input("Meeting Link (Zoom/Teams)", placeholder="https://...")
                
                # UPDATED BUTTON: Now explicitly calls the database function
                if st.form_submit_button("Schedule Meeting"):
                    if m_title:
                        db.add_meeting(task['id'], m_title, m_participants, m_date, m_time, m_link)
                        st.success(f"Meeting scheduled for {task['task_title']}!")
                    else:
                        st.error("Meeting title is required.")

    else:
        st.error("Task not found.")