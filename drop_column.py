import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vetms_db"
}

def remove_description_column():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if column exists before trying to drop it
        cursor.execute("DESCRIBE tasks")
        columns = [c[0] for c in cursor.fetchall()]
        
        if "description" in columns:
            cursor.execute("ALTER TABLE tasks DROP COLUMN description")
            print("✅ 'description' column successfully removed from Database.")
        else:
            print("ℹ️ Column 'description' does not exist (already removed).")
            
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    remove_description_column()