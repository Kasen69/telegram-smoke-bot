import sqlite3

DB_NAME = "smokes.db"

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA journal_mode=WAL")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        smokes INTEGER DEFAULT 0,
        last_smoke REAL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect(
        DB_NAME,
        timeout=10,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn

def add_user(user_id, username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users(user_id, username)
        VALUES (?, ?)
    """, (user_id, username))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()
    return user


def update_username(user_id, username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET username = ?
        WHERE user_id = ?
    """, (username, user_id))

    conn.commit()
    conn.close()


def update_smoke(user_id, smokes, last_smoke):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET smokes = ?, last_smoke = ?
        WHERE user_id = ?
    """, (smokes, last_smoke, user_id))

    conn.commit()
    conn.close()


def get_top(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, smokes
        FROM users
        ORDER BY smokes DESC
        LIMIT ?
    """, (limit,))

    users = cursor.fetchall()

    conn.close()
    return users


def import_from_json(data):
    conn = get_connection()
    cursor = conn.cursor()

    for user in data["users"]:
        cursor.execute("""
            INSERT OR REPLACE INTO users
            (user_id, username, smokes, last_smoke)
            VALUES (?, ?, ?, ?)
        """, (
            user["user_id"],
            user["username"],
            user["smokes"],
            user["last_smoke"]
        ))

    conn.commit()
    conn.close()
