import streamlit as st
import database as db
from datetime import date

def show_edit_interface():
    st.title("✏️ Edit & Update Task")

    # 1. Select Task to Edit
    tasks = db.fetch_tasks()
    
    if tasks.empty:
        st.info("No tasks available to edit.")
        return

    # Create a dropdown list like "1 - Design Login"
    task_options = tasks.apply(lambda x: f"{x['id']} - {x['task_title']}", axis=1).tolist()
    selected_task_string = st.selectbox("Select Task to Edit", task_options)
    
    # Extract ID (e.g., gets "1" from "1 - Design Login")
    selected_task_id = int(selected_task_string.split(" - ")[0])

    # 2. Fetch current details
    task_details = db.get_task_by_id(selected_task_id)

    if task_details:
        st.divider()
        with st.form("edit_task_form"):
            st.subheader(f"Editing Task #{selected_task_id}")
            
            c1, c2 = st.columns([3, 1])
            new_title = c1.text_input("Task Title", value=task_details['task_title'])
            
            # Priority Handling: Ensure current value is in the list
            priority_options = ["Critical", "High", "Medium", "Low"]
            current_priority = task_details['priority']
            if current_priority not in priority_options:
                priority_options.insert(0, current_priority) # Fallback if old data is different
            
            new_priority = c2.selectbox("Priority", priority_options, index=priority_options.index(current_priority))
            
            # NEW: Description Field (Pre-filled)
            current_desc = task_details.get('description', '') 
            # Handle None/NULL values from DB
            if current_desc is None:
                current_desc = ""
                
            new_description = st.text_area("Description", value=current_desc)

            c3, c4, c5 = st.columns(3)
            
            # Status
            status_opts = ["Pending", "In Progress", "Completed"]
            current_status = task_details['status']
            # Fallback for status index
            status_index = 0
            if current_status in status_opts:
                status_index = status_opts.index(current_status)
                
            new_status = c3.selectbox("Status", status_opts, index=status_index)

            # Assigned To
            user_opts = ["Admin Team", "DevOps", "Manager", "Frontend Dev"]
            current_user = task_details['assigned_user']
            # If current user isn't in list (e.g. old data), add it temporarily
            if current_user not in user_opts:
                user_opts.append(current_user)
            new_assigned = c4.selectbox("Assigned To", user_opts, index=user_opts.index(current_user))

            # Deadline
            new_deadline = c5.date_input("Deadline", value=task_details['deadline'])

            # 3. Save Changes
            if st.form_submit_button("💾 Update Task"):
                if new_title:
                    # Pass new description to DB
                    db.update_task(selected_task_id, new_title, new_description, new_priority, new_status, new_assigned, new_deadline)
                    st.success("✅ Task updated successfully!")
                    st.rerun()
                else:
                    st.error("Title cannot be empty.")