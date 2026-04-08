import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="s_core_vault.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS logs 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_id TEXT, role TEXT, content TEXT, date TEXT)''')
            conn.commit()

    def log_interaction(self, user_id, role, content):
        # التأكد أن الدور هو أحد القيم الثلاث المسموحة فقط
        if role not in ["system", "user", "assistant"]: role = "user"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO logs (user_id, role, content, date) VALUES (?, ?, ?, ?)",
                         (str(user_id), role, str(content), datetime.now().isoformat()))
            conn.commit()

    def get_chat_history(self, user_id, limit=6):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT role, content FROM (SELECT role, content, id FROM logs WHERE user_id = ? ORDER BY id DESC LIMIT ?) ORDER BY id ASC",
                (str(user_id), limit)
            )
            return [{"role": r, "content": c} for r, c in cursor.fetchall()]


