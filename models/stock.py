import sqlite3
from datetime import datetime

class StockManager:
    def __init__(self, db_path='data/store.db'):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    cost_price REAL,
                    supplier TEXT,
                    date TEXT,
                    deleted INTEGER DEFAULT 0
                )
            ''')

    def add_stock(self, item_name, quantity, cost_price, supplier, date):
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO stock (item_name, quantity, cost_price, supplier, date, deleted)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (item_name, quantity, cost_price, supplier, date))

    def get_all_stock(self):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM stock WHERE deleted = 0 ORDER BY date DESC")
            return cursor.fetchall()

    def get_stock_by_id(self, stock_id):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM stock WHERE id = ?", (stock_id,))
            return cursor.fetchone()

    def soft_delete_stock(self, stock_id):
        with self._connect() as conn:
            conn.execute("UPDATE stock SET deleted=1 WHERE id=?", (stock_id,))

    def restore_stock(self, stock_id):
        with self._connect() as conn:
            conn.execute("UPDATE stock SET deleted=0 WHERE id=?", (stock_id,))

    def get_deleted_stock(self):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM stock WHERE deleted = 1 ORDER BY date DESC")
            return cursor.fetchall()

    def get_low_stock(self, threshold=10):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM stock WHERE quantity < ? AND deleted = 0", (threshold,))
            return cursor.fetchall()