

class Message:
    def __init__(
            self,
            receiver: str,
            key: str,
            message: str,
            message_id: int = -1,
            time: int = -1
    ):
        self.message_id = message_id
        self.receiver = receiver
        self.key = key
        self.message = message
        self.time = time
