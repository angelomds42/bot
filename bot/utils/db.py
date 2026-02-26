import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "bot", "data", "bot.db")


def get_db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id  INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT
        )
    """
    )
    return conn
