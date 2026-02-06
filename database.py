import mysql.connector
import pandas as pd

# ==========================================
# MYSQL CONFIGURATION
# ==========================================
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vetms_db"
}

def get_connection():
    return mysql.connector.connect(**db_config)

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. TASKS Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                priority VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL,
                assigned_user VARCHAR(100) NOT NULL,
                deadline DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(100) DEFAULT 'System'
            )
        ''')

        # 2. MEETINGS Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task_id INT,
                title VARCHAR(255) NOT NULL,
                meeting_type VARCHAR(50),
                description TEXT,
                participants VARCHAR(255),
                meeting_date DATE NOT NULL,
                meeting_time TIME NOT NULL,
                link VARCHAR(500),
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
            )
        ''')

        # 3. VOICE LOGS Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                command_text TEXT,
                status VARCHAR(50),
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 4. TEAM MEMBERS Table (Requirement 11)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                user_id VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255),
                role VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL,
                calendar_synced BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ All Tables Initialized Successfully")
    except mysql.connector.Error as err:
        print(f"❌ DB Init Error: {err}")

# ==========================================
# TASK FUNCTIONS
# ==========================================
def add_task(title, description, priority, status, assigned_to, deadline):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO tasks (title, description, priority, status, assigned_user, deadline) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (title, description, priority, status, assigned_to, deadline))
        conn.commit()
        conn.close()
        return True
    except Exception: return False

def fetch_tasks(search_query=None, status_filter=None, priority_filter=None):
    try:
        conn = get_connection()
        query = "SELECT id, title as task_title, description, priority, status, assigned_user, deadline FROM tasks WHERE 1=1"
        params = []
        if search_query:
            query += " AND title LIKE %s"; params.append(f"%{search_query}%")
        if status_filter and status_filter != "All":
            query += " AND status = %s"; params.append(status_filter)
        if priority_filter and priority_filter != "All":
            query += " AND priority = %s"; params.append(priority_filter)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception: return pd.DataFrame()

def get_task_by_id(task_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        if task: task['task_title'] = task['title']
        conn.close()
        return task
    except Exception: return None

def update_task(task_id, title, description, priority, status, assigned_to, deadline):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = 'UPDATE tasks SET title=%s, description=%s, priority=%s, status=%s, assigned_user=%s, deadline=%s WHERE id=%s'
        cursor.execute(sql, (title, description, priority, status, assigned_to, deadline, task_id))
        conn.commit(); conn.close()
        return True
    except Exception: return False

def delete_task(task_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit(); conn.close()
        return True
    except Exception: return False

# ==========================================
# MEETING & TEAM FUNCTIONS
# ==========================================
def add_meeting(task_id, title, m_type, description, participants, m_date, m_time, link):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO meetings (task_id, title, meeting_type, description, participants, meeting_date, meeting_time, link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (task_id, title, m_type, description, participants, m_date, m_time, link))
        conn.commit(); conn.close()
        return True
    except Exception: return False

def fetch_meetings():
    try:
        conn = get_connection()
        query = 'SELECT m.*, t.title as task_title FROM meetings m LEFT JOIN tasks t ON m.task_id = t.id'
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception: return pd.DataFrame()

def add_team_member(name, u_id, email, role, status, synced):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO team_members (full_name, user_id, email, role, status, calendar_synced) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, u_id, email, role, status, synced))
        conn.commit(); conn.close()
        return True
    except Exception: return False

def fetch_team_data():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM team_members", conn)
        conn.close()
        return df
    except Exception: return pd.DataFrame()

# ==========================================
# VOICE LOGS
# ==========================================
def log_command(text, status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO command_logs (command_text, status) VALUES (%s, %s)", (text, status))
        conn.commit(); conn.close()
    except Exception: pass

def fetch_command_logs():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM command_logs ORDER BY id DESC LIMIT 10", conn)
        conn.close()
        return df
    except Exception: return pd.DataFrame()

if __name__ == "__main__":
    init_db()