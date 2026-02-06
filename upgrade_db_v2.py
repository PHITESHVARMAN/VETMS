import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vetms_db"
}

def add_new_columns():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check current columns
        cursor.execute("DESCRIBE tasks")
        columns = [c[0] for c in cursor.fetchall()]
        
        # 1. Add Creation Timestamp (default to NOW)
        if "created_at" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✅ Added 'created_at' column.")
            
        # 2. Add Creator Info (default to 'System')
        if "created_by" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN created_by VARCHAR(100) DEFAULT 'System'")
            print("✅ Added 'created_by' column.")
            
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_new_columns()