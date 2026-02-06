import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vetms_db"
}

def add_description_column():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if description exists
        cursor.execute("DESCRIBE tasks")
        columns = [c[0] for c in cursor.fetchall()]
        
        if "description" not in columns:
            # Add description column back
            cursor.execute("ALTER TABLE tasks ADD COLUMN description TEXT AFTER title")
            print("✅ Success: 'description' column added to database.")
        else:
            print("ℹ️ 'description' column already exists.")
            
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_description_column()