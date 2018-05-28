import threading
from collections import deque

class MessageQ:
    def __init__(self, q):
        self.q = q
        self.lock = threading.RLock()

    def get_message(self):
        with self.lock:
            if self.q:
                return self.q[0]
            return None

    def enqueue(self, message):
        self.q.append(message)

    def ack(self, message):
        self.q.popleft()
