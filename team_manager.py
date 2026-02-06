import streamlit as st
import database as db

def show_team_management():
    st.title("👥 Team Management Module")
    
    team_df = db.fetch_team_data()
    
    if team_df.empty:
        st.warning("No team members found. Please add members to the database.")
        # Quick Add form for testing
        with st.expander("➕ Add First Team Member (Testing)"):
            with st.form("add_member"):
                name = st.text_input("Full Name")
                u_id = st.text_input("User ID (e.g. USR001)")
                email = st.text_input("Email")
                role = st.selectbox("Role", ["Super Admin", "Admin", "Manager", "User"])
                status = st.selectbox("Status", ["Active", "Inactive"])
                if st.form_submit_button("Add Member"):
                    db.add_team_member(name, u_id, email, role, status, True)
                    st.rerun()
        return

    # --- 11.2 METRICS DISPLAY ---
    st.subheader("📊 Team Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Members", len(team_df))
    m2.metric("Active Users", len(team_df[team_df['status'] == 'Active']))
    m3.metric("Inactive Users", len(team_df[team_df['status'] == 'Inactive']))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Super Admins", len(team_df[team_df['role'] == 'Super Admin']))
    c2.metric("Admins", len(team_df[team_df['role'] == 'Admin']))
    c3.metric("Managers", len(team_df[team_df['role'] == 'Manager']))
    c4.metric("Users", len(team_df[team_df['role'] == 'User']))

    st.divider()

    # --- 11.3 TEAM MEMBER LISTING ---
    st.subheader("📇 Team Member Directory")
    
    # Custom display to match 11.3 requirements
    for index, row in team_df.iterrows():
        with st.container(border=True):
            col_a, col_b, col_c = st.columns([2, 2, 1])
            with col_a:
                st.markdown(f"**👤 {row['full_name']}**")
                st.caption(f"ID: {row['user_id']}")
            with col_b:
                st.write(f"📧 {row['email']}")
                st.write(f"💼 Role: **{row['role']}**")
            with col_c:
                st.write(f"Status: `{row['status']}`")
                sync_icon = "✅" if row['calendar_synced'] else "❌"
                st.write(f"Calendar: {sync_icon}")