import sqlite3
from models import Message

conn = sqlite3.connect('e2ee_messenger_server.db')
cursor = conn.cursor()


def new_message(message: Message):
    cursor.execute(
        "INSERT INTO messages (recipient_public_key, encrypted_key, encrypted_message) VALUES (?, ?, ?)",
        (message.receiver, message.key, message.message)
    )
    conn.commit()


def get_messages_by_id(p_key: str, last_message_id: int) -> list:
    cursor.execute(
        "SELECT * FROM messages WHERE recipient_public_key = ? AND message_id > ?",
        (p_key, last_message_id)
    )

    result = []

    for r in cursor.fetchall():
        message_id = r[0]
        p_key = r[1]
        key = r[2]
        message = r[3]
        time = r[4]
        result.append(
            Message(
                message_id=message_id,
                receiver=p_key,
                key=key,
                message=message,
                time=time
            )
        )

    return result
