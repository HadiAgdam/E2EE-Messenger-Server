

class Message:
    def __init__(
            self,
            encryption_key: str,
            encrypted_message: str,
            time: float,
            iv: str,
            message_id: int = -1,
    ):
        self.message_id = message_id
        self.encryption_key = encryption_key
        self.encrypted_message = encrypted_message
        self.time = time
        self.iv = iv
