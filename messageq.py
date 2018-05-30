import threading
import time
from collections import deque

class MessageQ:
    """This is a class to mimic a message queue."""
    def __init__(self, q):
        """Initialize the message queue with internal queue and lock."""
        self.q = q
        self.lock = threading.RLock()

    def get_message(self):
        """Send the first message to a consumer."""
        time.sleep(0.2)
        with self.lock:
            if self.q:
                return self.q[0]
            return None

    def enqueue(self, message):
        """Enqueue a new message from a producer."""
        time.sleep(0.2)
        self.q.append(message)

    def ack(self, message):
        """Received an acknowledgement that the message is processed.
        Now remove it from the queue.
        """
        time.sleep(0.2)
        self.q.popleft()
