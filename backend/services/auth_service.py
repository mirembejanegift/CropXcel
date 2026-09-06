import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "agrisense.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def register_user(name, email, password, role="farmer", location=None):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role, location) VALUES (?, ?, ?, ?, ?)",
            (name, email, password_hash, role, location)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "name": name, "email": email, "role": role}
    except sqlite3.IntegrityError:
        raise ValueError("An account with this email already exists")
    finally:
        conn.close()


def authenticate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        raise ValueError("Invalid email or password")

    if not check_password_hash(user["password_hash"], password):
        raise ValueError("Invalid email or password")

    return {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}