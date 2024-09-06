from time import time


class Message:
    def __init__(
            self,
            receiver: str,
            key: str,
            message: str,
            time_stamp: int = -1
    ):
        self.receiver = receiver
        self.key = key
        self.message = message
        if time_stamp == -1:
            self.time_stamp = time()
        else:
            self.time_stamp = time_stamp
