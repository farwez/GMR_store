import sqlite3
from datetime import datetime

class HistoryLogger:
    def __init__(self, db_path='data/store.db'):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    item_name TEXT,
                    quantity INTEGER,
                    user TEXT,
                    timestamp TEXT
                )
            ''')

    def log(self, action, item_name, quantity, user):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO history (action, item_name, quantity, user, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (action, item_name, quantity, user, timestamp))

    def get_logs(self):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM history ORDER BY timestamp DESC")
            return cursor.fetchall()