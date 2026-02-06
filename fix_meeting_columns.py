import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vetms_db"
}

def fix_meeting_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check existing columns
        cursor.execute("DESCRIBE meetings")
        columns = [c[0] for c in cursor.fetchall()]
        
        # Add 'meeting_type' if missing
        if "meeting_type" not in columns:
            cursor.execute("ALTER TABLE meetings ADD COLUMN meeting_type VARCHAR(50) AFTER title")
            print("✅ Added 'meeting_type' column.")

        # Add 'description' if missing
        if "description" not in columns:
            cursor.execute("ALTER TABLE meetings ADD COLUMN description TEXT AFTER meeting_type")
            print("✅ Added 'description' column.")
            
        conn.commit()
        conn.close()
        print("🎉 Meeting table updated successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_meeting_table()