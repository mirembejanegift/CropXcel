import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "agrisense.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'farmer',
            location TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized at:", DB_PATH)


if __name__ == "__main__":
    init_db()