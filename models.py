class Message:
    def __init__(
            self,
            key: str,
            message: str,
            time_stamp: int
    ):
        self.key = key
        self.message = message
        self.time_stamp = time_stamp
