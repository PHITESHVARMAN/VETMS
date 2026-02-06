import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vetms_db"
}

def create_meetings_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create Meetings Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task_id INT,
                title VARCHAR(255) NOT NULL,
                participants VARCHAR(255),
                meeting_date DATE NOT NULL,
                meeting_time TIME NOT NULL,
                link VARCHAR(500),
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
            )
        ''')
        
        print("✅ 'meetings' table created successfully.")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_meetings_table()