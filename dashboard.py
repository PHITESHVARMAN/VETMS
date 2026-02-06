import streamlit as st
import pandas as pd
import database as db

def show_dashboard():
    # ==========================================
    # HEADER SECTION WITH NAVIGATION BUTTON
    # ==========================================
    # We create two columns: Left for Title, Right for the Button
    col_header_1, col_header_2 = st.columns([6, 1])
    
    with col_header_1:
        st.title("📊 VETMS Dashboard")
        st.write("Real-time insights into task distribution and progress.")
    
    with col_header_2:
        # This gives some spacing so the button aligns with the title
        st.write("") 
        st.write("") 
        if st.button("🚀 Task Manager", help="Go to Task Creation Page", use_container_width=True):
            st.session_state.page = "Task Manager"
            st.rerun() # Forces the app to reload and switch to the new page

    st.divider()

    # ==========================================
    # FETCH DATA FROM DATABASE
    # ==========================================
    df = db.fetch_tasks()

    # ==========================================
    # KEY METRICS SECTION
    # ==========================================
    total_tasks = len(df)
    completed_tasks = len(df[df["status"] == "Completed"])
    in_progress_tasks = len(df[df["status"] == "In Progress"])
    pending_tasks = len(df[df["status"] == "Pending"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Tasks", value=total_tasks)
    with col2:
        st.metric(label="Completed Tasks", value=completed_tasks, delta="Finished")
    with col3:
        st.metric(label="In Progress Tasks", value=in_progress_tasks, delta="Active", delta_color="off")
    with col4:
        st.metric(label="Pending Tasks", value=pending_tasks, delta="Action Req.", delta_color="inverse")

    st.divider()

    # ==========================================
    # TASK SUMMARY SECTION
    # ==========================================
    st.subheader("Task Summary List")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "task_title": st.column_config.TextColumn("Task Title", width="medium"),
            "priority": st.column_config.SelectboxColumn("Priority", width="small", options=["Critical", "High", "Medium", "Low"]),
            "status": st.column_config.SelectboxColumn("Status", width="small", options=["Pending", "In Progress", "Completed"]),
            "assigned_user": st.column_config.TextColumn("Assigned To", width="small"),
            "deadline": st.column_config.DateColumn("Deadline", format="YYYY-MM-DD"),
        }
    )