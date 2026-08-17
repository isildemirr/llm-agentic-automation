import sqlite3

DB_NAME = "chat.db"


# ======================================================
# DATABASE
# ======================================================

def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )
    """)

    conn.commit()
    conn.close()


# ======================================================
# CHAT FUNCTIONS
# ======================================================

def create_chat(title="Yeni Sohbet"):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats(title) VALUES(?)",
        (title,)
    )

    chat_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return chat_id


def get_all_chats():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title
        FROM chats
        ORDER BY created_at DESC
    """)

    chats = cursor.fetchall()

    conn.close()

    return chats


def update_chat_title(chat_id, title):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE chats
        SET title = ?
        WHERE id = ?
        """,
        (title, chat_id)
    )

    conn.commit()
    conn.close()


# ======================================================
# MESSAGE FUNCTIONS
# ======================================================

def save_message(chat_id, role, message):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages(chat_id, role, message)
        VALUES (?, ?, ?)
        """,
        (chat_id, role, message)
    )

    conn.commit()
    conn.close()


def load_messages(chat_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM messages
        WHERE chat_id=?
        ORDER BY id
        """,
        (chat_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def load_last_messages(chat_id, limit=8):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM messages
        WHERE chat_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (chat_id, limit)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows[::-1]


# ======================================================
# STATISTICS
# ======================================================

def get_message_count():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM messages"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ======================================================
# DELETE
# ======================================================

def clear_messages(chat_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM messages
        WHERE chat_id=?
        """,
        (chat_id,)
    )

    conn.commit()
    conn.close()


def delete_chat(chat_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM messages WHERE chat_id=?",
        (chat_id,)
    )

    cursor.execute(
        "DELETE FROM chats WHERE id=?",
        (chat_id,)
    )

    conn.commit()
    conn.close()