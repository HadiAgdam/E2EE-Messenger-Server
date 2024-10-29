import sqlite3
from models import Message

# cursor = conn.cursor()


def new_message(
        encryption_key: str,
        encrypted_message: str,
        iv: str,
        recipient_public_key):
    conn = sqlite3.connect('e2ee_messenger_server.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO messages (encrypted_key, encrypted_message, iv, recipient_public_key) "
            "VALUES (?, ?, ?, ?)",
            (encryption_key, encrypted_message, iv, recipient_public_key)
        )
        conn.commit()
        return True
    except Exception as e:
        print("insert error :", e)
        conn.close()
        return False


def get_messages_by_id(recipient_public_key: str, last_message_id: int) -> list:
    conn = sqlite3.connect('e2ee_messenger_server.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT message_id, encrypted_key, encrypted_message, time, iv "
        "FROM messages WHERE recipient_public_key = ? AND message_id > ?",
        (recipient_public_key, last_message_id)
    )

    result = []

    for r in cursor.fetchall():
        result.append(
            Message(
                message_id=r[0],
                encryption_key=r[1],
                encrypted_message=r[2],
                time=r[3],
                iv=r[4]
            )
        )
    conn.close()
    return result
