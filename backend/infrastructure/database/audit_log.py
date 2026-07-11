import time
from backend.infrastructure.database.connection import DbConnection

class AuditLogger:
    @staticmethod
    def initialize_audit_table():
        conn = DbConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL,
            details TEXT NOT NULL,
            user_role TEXT NOT NULL,
            timestamp INTEGER NOT NULL
        )
        """)
        conn.commit()

    @staticmethod
    def log_action(action_type: str, details: str, user_role: str):
        conn = DbConnection.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO audit_log (action_type, details, user_role, timestamp) VALUES (?, ?, ?, ?)",
                (action_type, details, user_role, int(time.time()))
            )
            conn.commit()
        except Exception:
            AuditLogger.initialize_audit_table()
            cursor.execute(
                "INSERT INTO audit_log (action_type, details, user_role, timestamp) VALUES (?, ?, ?, ?)",
                (action_type, details, user_role, int(time.time()))
            )
            conn.commit()
            
    @staticmethod
    def get_audit_trail() -> list:
        conn = DbConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT action_type, details, user_role, timestamp FROM audit_log ORDER BY id DESC")
            return cursor.fetchall()
        except Exception:
            return []
