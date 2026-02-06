import streamlit as st
import database as db
from datetime import date

def show_task_manager():
    st.title("🗂️ Task Management Module")
    
    # ==========================================
    # 1. CREATE TASK FORM
    # ==========================================
    with st.expander("➕ Create New Task", expanded=False):
        with st.form("create_task_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            title = col1.text_input("Task Title*")
            # Uses standardized priority list
            priority = col2.selectbox("Priority*", ["Critical", "High", "Medium", "Low"])
            
            # CHANGED: Added Description Input
            description = st.text_area("Task Description", placeholder="Enter task details here...")
            
            col3, col4, col5 = st.columns(3)
            status = col3.selectbox("Status", ["Pending", "In Progress", "Completed"])
            assigned_to = col4.selectbox("Assign To", ["Admin Team", "DevOps", "Manager", "Frontend Dev"])
            deadline = col5.date_input("Deadline", min_value=date.today())
            
            if st.form_submit_button("Save Task", type="primary"):
                if title:
                    # Pass description to database
                    db.add_task(title, description, priority, status, assigned_to, deadline)
                    st.success("✅ Task Created Successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Title is required.")

    st.divider()

    # ==========================================
    # 2. TASK LIST & SEARCH
    # ==========================================
    st.subheader("Task List")
    
    c1, c2, c3 = st.columns([2, 1, 1])
    search_term = c1.text_input("🔍 Search by Title", placeholder="Type to find task...")
    filter_status = c2.selectbox("Filter Status", ["All", "Pending", "In Progress", "Completed"])
    filter_priority = c3.selectbox("Filter Priority", ["All", "Critical", "High", "Medium", "Low"])

    df = db.fetch_tasks(search_term, filter_status, filter_priority)

    if not df.empty:
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "task_title": st.column_config.TextColumn("Task Title", width="medium"),
                
                # CHANGED: Added Description Column to the display
                "description": st.column_config.TextColumn("Description", width="large"),
                
                "priority": st.column_config.TextColumn("Priority", width="small"),
                "status": st.column_config.SelectboxColumn("Status", width="medium", options=["Pending", "In Progress", "Completed"]),
                "assigned_user": st.column_config.TextColumn("Assigned To", width="medium"),
                "deadline": st.column_config.DateColumn("Deadline", format="YYYY-MM-DD")
            }
        )
        
        # ==========================================
        # 3. DELETE ACTION
        # ==========================================
        st.write("### Actions")
        ac1, ac2 = st.columns([1, 4])
        with ac1:
            task_id_to_action = st.selectbox("Select Task ID to Delete", df['id'])
        with ac2:
            st.write("") 
            st.write("") 
            if st.button("🗑️ Delete Selected Task", type="secondary"):
                db.delete_task(task_id_to_action)
                st.warning(f"Task {task_id_to_action} Deleted.")
                st.rerun()
    else:
        st.info("No tasks found matching your criteria.")