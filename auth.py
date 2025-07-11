import sqlite3
import bcrypt

def create_user_table():
    conn = sqlite3.connect('data/store.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    role TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = sqlite3.connect('data/store.db')
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed, role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('data/store.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    return False

def get_user_role(username):
    conn = sqlite3.connect('data/store.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
