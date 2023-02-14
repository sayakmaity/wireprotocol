from queue import Queue
import threading

class User:
    def __init__(self, username):
        self.username = username
        self.message_queue = Queue() # Queue is already thread-safe, don't need to worry if we use default methods
        self.lock = threading.Lock()

    def add_message(self, message):
        self.message_queue.put(message)

    def get_message(self):
        if self.message_queue.empty():
            return None
        return self.message_queue.get()

