import streamlit as st
import speech_recognition as sr
import database as db
import pandas as pd
from datetime import date

# Initialize Recognizer
recognizer = sr.Recognizer()

def process_voice_command(command):
    """
    NLP Logic: Parses the string to find intent (Create, Delete, Show).
    """
    command = command.lower()
    response_msg = ""
    status = "Failed"

    # --- INTENT 1: CREATE TASK ---
    # Pattern: "create task [title]"
    if "create task" in command:
        try:
            # Remove "create task" from string to get the title
            task_title = command.replace("create task", "").strip()
            if task_title:
                # Default values for voice-created tasks
                db.add_task(task_title, "Created via Voice", "Medium", "Pending", "Admin Team", date.today())
                response_msg = f"✅ Success: Created task '{task_title}'"
                status = "Success"
            else:
                response_msg = "⚠️ Error: No title detected."
        except Exception as e:
            response_msg = f"❌ Error: {str(e)}"

    # --- INTENT 2: DELETE TASK ---
    # Pattern: "delete task [ID]" (e.g., "delete task 5")
    elif "delete task" in command:
        try:
            # Find numbers in the string
            words = command.split()
            task_id = None
            for word in words:
                if word.isdigit():
                    task_id = int(word)
                    break
            
            if task_id:
                db.delete_task(task_id)
                response_msg = f"🗑️ Success: Deleted task #{task_id}"
                status = "Success"
            else:
                response_msg = "⚠️ Error: Could not hear a Task ID number."
        except Exception:
            response_msg = "❌ Error processing delete command."

    # --- INTENT 3: SHOW TASKS ---
    elif "show tasks" in command or "list tasks" in command:
        response_msg = "📂 Navigating to Task Manager..."
        status = "Navigation"
        # In a real web app, we can't force navigation easily, but we can show the data here
        st.session_state.show_preview = True

    # --- UNKNOWN COMMAND ---
    else:
        response_msg = "❓ Unknown Command. Try 'Create task...' or 'Delete task...'"
        status = "Unknown"

    # Log to Database (Requirement 10.4)
    db.log_command(command, status)
    return response_msg

def show_voice_commands():
    st.title("🎙️ Voice Command Module")
    st.markdown("Control your system using natural language.")

    # ==========================================
    # 1. INPUT SECTION (Req 10.2 & 10.3)
    # ==========================================
    col1, col2 = st.columns(2)

    with col1:
        st.info("🗣️ **Voice Input**")
        if st.button("🎤 Start Recording"):
            with st.spinner("Listening... Speak now!"):
                try:
                    with sr.Microphone() as source:
                        # Adjust for ambient noise
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.listen(source, timeout=5)
                        
                        try:
                            # Convert Speech to Text
                            text = recognizer.recognize_google(audio)
                            st.success(f"You said: '{text}'")
                            
                            # Process
                            result = process_voice_command(text)
                            st.markdown(f"### {result}")
                            
                        except sr.UnknownValueError:
                            st.error("Could not understand audio.")
                        except sr.RequestError:
                            st.error("Speech service unavailable.")
                            
                except Exception as e:
                    st.error(f"Microphone Error: {e}. Check your microphone settings.")

    with col2:
        st.info("⌨️ **Manual Input** (Req 10.3)")
        with st.form("manual_voice_form"):
            text_input = st.text_input("Type command here:", placeholder="e.g., Create task Buy Groceries")
            if st.form_submit_button("🚀 Process Command"):
                if text_input:
                    result = process_voice_command(text_input)
                    st.markdown(f"### {result}")

    st.divider()

    # ==========================================
    # 2. COMMAND HISTORY (Req 10.4)
    # ==========================================
    st.subheader("📜 Command History")
    history_df = db.fetch_command_logs()
    
    if not history_df.empty:
        st.dataframe(
            history_df, 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.caption("No voice commands recorded yet.")

    # ==========================================
    # 3. CHEAT SHEET
    # ==========================================
    with st.expander("ℹ️ Supported Voice Commands"):
        st.markdown("""
        * **"Create task [Title]"** -> Creates a new task with Medium priority.
        * **"Delete task [ID]"** -> Deletes the task with that number (e.g., "Delete task 2").
        * **"Show tasks"** -> Displays the command logs.
        """)