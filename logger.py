import sqlite3
from datetime import datetime

DB_NAME = "bot.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    conn.commit()
    conn.close()


def log_message(user_message, bot_response, user_id=None, user_name=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_message TEXT,
            bot_response TEXT,
            user_id INTEGER,
            user_name TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO chat_logs (timestamp, user_message, bot_response, user_id, user_name)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, user_message, bot_response, user_id, user_name))

    if user_name and user_id:
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, name) 
            VALUES (?, ?)
        ''', (user_id, user_name))

    conn.commit()
    conn.close()


def get_user(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


init_db()