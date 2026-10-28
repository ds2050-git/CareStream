import sqlite3
import datetime

class WorkflowEngine:
    def __init__(self,db_path="carestream.db"):
        self.db_path=db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn=self._get_conn()
        c=conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        status TEXT DEFAULT 'ACTIVE'
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS care_tasks(
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        encounter_id INTEGER NOT NULL,
        assigned_role TEXT NOT NULL,
        task_description TEXT NOT NULL,
        status TEXT DEFAULT 'PENDING',
        created_at TEXT,
        updated_at TEXT
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs(
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action_type TEXT NOT NULL,
        entity_name TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        action_time TEXT
        )""")
        conn.commit()
        conn.close()

    def add_user(self,username,role):
        conn=self._get_conn()
        c=conn.cursor()
        c.execute("INSERT INTO users(username,role) VALUES(?,?)",(username,role))
        uid=c.lastrowid
        conn.commit()
        conn.close()
        return uid

    def create_task(self,user_id,encounter_id,assigned_role,description):
        conn=self._get_conn()
        c=conn.cursor()
        c.execute("SELECT role FROM users WHERE user_id=? AND status='ACTIVE'",(user_id,))
        res=c.fetchone()
        if not res:
            conn.close()
            raise PermissionError("User unauthorized or inactive")
        now=datetime.datetime.now().isoformat()
        c.execute("""
        INSERT INTO care_tasks(encounter_id,assigned_role,task_description,status,created_at,updated_at)
        VALUES(?,?,?,'PENDING',?,?)
        """,(encounter_id,assigned_role,description,now,now))
        tid=c.lastrowid
        c.execute("""
        INSERT INTO audit_logs(user_id,action_type,entity_name,entity_id,action_time)
        VALUES(?,'CREATE_TASK','care_tasks',?,?)
        """,(user_id,tid,now))
        conn.commit()
        conn.close()
        return tid

    def update_task_status(self,user_id,task_id,new_status):
        conn=self._get_conn()
        c=conn.cursor()
        c.execute("SELECT role FROM users WHERE user_id=? AND status='ACTIVE'",(user_id,))
        user_res=c.fetchone()
        if not user_res:
            conn.close()
            raise PermissionError("User unauthorized")
        c.execute("SELECT status FROM care_tasks WHERE task_id=?",(task_id,))
        task_res=c.fetchone()
        if not task_res:
            conn.close()
            raise ValueError("Task not found")
        now=datetime.datetime.now().isoformat()
        c.execute("""
        UPDATE care_tasks SET status=?,updated_at=? WHERE task_id=?
        """,(new_status,now,task_id))
        c.execute("""
        INSERT INTO audit_logs(user_id,action_type,entity_name,entity_id,action_time)
        VALUES(?,'UPDATE_TASK_STATUS','care_tasks',?,?)
        """,(user_id,task_id,now))
        conn.commit()
        conn.close()
        return True

    def get_audit_trail(self,entity_name,entity_id):
        conn=self._get_conn()
        c=conn.cursor()
        c.execute("""
        SELECT a.log_id,u.username,a.action_type,a.action_time
        FROM audit_logs a
        JOIN users u ON a.user_id=u.user_id
        WHERE a.entity_name=? AND a.entity_id=?
        ORDER BY a.log_id ASC
        """,(entity_name,entity_id))
        logs=c.fetchall()
        conn.close()
        return logs