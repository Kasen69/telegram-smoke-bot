import sqlite3
import os


if os.path.exists("/workspace/data"):
    DB_NAME = "/workspace/data/smokes.db"
else:
    DB_NAME = "smokes.db"


def get_connection():
    conn = sqlite3.connect(
        DB_NAME,
        timeout=10,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn


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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id INTEGER PRIMARY KEY,
            chat_type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promo_codes (
            code TEXT PRIMARY KEY,
            type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS used_promos (
            user_id INTEGER,
            code TEXT,
            PRIMARY KEY (user_id, code)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            user_id INTEGER,
            item_id TEXT,
            amount INTEGER DEFAULT 1,
            PRIMARY KEY (user_id, item_id)
        )
    """)

    conn.commit()
    conn.close()

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

def get_users_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()
    return count

def add_chat(chat_id, chat_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO chats(chat_id, chat_type)
        VALUES (?, ?)
    """, (chat_id, chat_type))

    conn.commit()
    conn.close()

def get_user_rank(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) + 1
        FROM users
        WHERE smokes > (
            SELECT smokes
            FROM users
            WHERE user_id = ?
        )
    """, (user_id,))

    rank = cursor.fetchone()[0]

    conn.close()
    return rank

def get_private_chats_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM chats
        WHERE chat_type = 'private'
    """)

    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_group_chats_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM chats
        WHERE chat_type IN ('group', 'supergroup')
    """)

    count = cursor.fetchone()[0]

    conn.close()
    return count

def add_promo(code, promo_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO promo_codes(code, type)
        VALUES (?, ?)
    """, (code, promo_type))

    conn.commit()
    conn.close()


def get_promo(code):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM promo_codes
        WHERE code = ?
    """, (code,))

    promo = cursor.fetchone()

    conn.close()
    return promo


def use_promo(user_id, code):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO used_promos(user_id, code)
        VALUES (?, ?)
    """, (user_id, code))

    conn.commit()
    conn.close()


def is_promo_used(user_id, code):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM used_promos
        WHERE user_id = ? AND code = ?
    """, (user_id, code))

    used = cursor.fetchone() is not None

    conn.close()
    return used

def get_inventory(self, user_id):
    # Цей код покаже в логах, які колонки у вас СЕЙЧАС є в таблиці
    cursor = self.conn.cursor()
    cursor.execute("PRAGMA table_info(inventory)")
    columns = cursor.fetchall()
    print(f"!!! СТРУКТУРА ТАБЛИЦІ INVENTORY: {columns}", flush=True)
    
    # Тимчасове повернення порожніього списку, щоб бот не падав
    return []



def add_item(user_id, item_id, amount=1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inventory (user_id, item_id, amount)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, item_id)
        DO UPDATE SET amount = amount + excluded.amount
    """, (user_id, item_id, amount))

    conn.commit()
    conn.close()