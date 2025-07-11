import sqlite3
from datetime import datetime

class SalesManager:
    def __init__(self, db_path='data/store.db'):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    total REAL NOT NULL,
                    customer TEXT,
                    date TEXT,
                    user TEXT,
                    deleted INTEGER DEFAULT 0
                )
            ''')

    def add_sale(self, item_name, quantity, price, customer, date, user):
        total = quantity * price
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO sales (item_name, quantity, price, total, customer, date, user, deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """, (item_name, quantity, price, total, customer, date, user))

    def get_sales(self):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM sales WHERE deleted = 0 ORDER BY date DESC")
            return cursor.fetchall()

    def get_sale_by_id(self, sale_id):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
            return cursor.fetchone()

    def get_sales_by_date(self, start_date, end_date):
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT * FROM sales
                WHERE deleted=0 AND date BETWEEN ? AND ?
                ORDER BY date DESC
            """, (start_date, end_date))
            return cursor.fetchall()

    def soft_delete_sale(self, sale_id):
        with self._connect() as conn:
            conn.execute("UPDATE sales SET deleted=1 WHERE id=?", (sale_id,))

    def restore_sale(self, sale_id):
        with self._connect() as conn:
            conn.execute("UPDATE sales SET deleted=0 WHERE id=?", (sale_id,))

    def get_deleted_sales(self):
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM sales WHERE deleted = 1 ORDER BY date DESC")
            return cursor.fetchall()