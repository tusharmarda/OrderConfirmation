import threading
import time
from collections import deque

class MessageQ:
    """This is a class to mimic a message queue."""
    def __init__(self, q):
        """Initialize the message queue with internal queue and lock."""
        self.q = q
        self.lock = threading.RLock()
        self.waiting_size = 0;
        self.registered_consumers = {}
        self.queue_in = ListNode(None)
        self.queue_out = ListNode(None)
        self.queue_in.add_next(self.queue_out)

    def get_message(self, consumer_id):
        """Send the first message to a consumer."""
        time.sleep(0.2)
        with self.lock:
            if consumer_id in self.registered_consumers and len(self.q) > 0:
                ret = self.registered_consumers[consumer_id]
                if ret is None:
                    ret = ListNode((time.time(), self.q.popleft(), consumer_id))
                    self.waiting_size += 1
                    self.queue_in.add_next(ret)
                    self.registered_consumers[consumer_id] = ret
                return ret.data[1]
            else:
                return None

    def enqueue(self, message):
        """Enqueue a new message from a producer."""
        time.sleep(0.2)
        self.q.append(message)

    def ack(self, message, consumer_id):
        """Received an acknowledgement that the message is processed.
        Now remove it from the queue.
        """
        time.sleep(0.2)
        with self.lock:
            if consumer_id in self.registered_consumers:
                ret = self.registered_consumers[consumer_id]
                if ret is not None and ret.data[1] == message:
                    ret.delete()
                    self.registered_consumers[consumer_id] = None
                    self.waiting_size -= 1
                    return True
        return False

    def cleanup_stragglers(self, run_event):
        """If any consumers have not acknowledged their message for 5 minutes,
        put it back in the queue.
        """
        while run_event.is_set():
            with self.lock:
                if self.waiting_size > 0:
                    message_node = self.queue_out.prev
                    while message_node != self.queue_in and time.time() - message_node.data[0] > 300:
                        # Message has not been ack'ed for 5 minutes.
                        message = message_node.data[1]
                        consumer_id = message_node.data[2]
                        self.q.appendleft(message)
                        self.registered_consumers[consumer_id] = None
                        message_node.delete()
                        waiting_size -= 1
                        message_node = self.queue_out.prev
                        print('Consumer id {} did not acknowledge message for 5 minutes'.format(consumer_id))
            for i in range(12):
                time.sleep(5)
                if not run_event.is_set():
                    break

    def register(self):
        """Register a new consumer for the message queue.
        Return True if new consumer was added, False otherwise.
        """
        consumer_id = threading.get_ident()
        with self.lock:
            while consumer_id in self.registered_consumers:
                consumer_id += 1
            self.registered_consumers[consumer_id] = None
        return consumer_id

    def deregister(self, consumer_id):
        """Deregister an existing consumer from the message queue.
        Return True if existing consumer was removed, False otherwise.
        """
        with self.lock:
            if consumer_id in self.registered_consumers:
                del(self.registered_consumers[consumer_id])
                return True
            return False



class ListNode:
    """A node of a doubly linked list"""
    def __init__(self, data):
        """Initialize a node with given data"""
        self.data = data
        self.next = None
        self.prev = None

    def delete(self):
        """Delete the node from the doubly linked list, and return the adjoining nodes."""
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev
        return self.prev, self.next

    def add_prev(self, node):
        """Insert the given node previous to self."""
        node.prev = self.prev
        node.next = self
        self.prev = node
        if node.prev is not None:
            node.prev.next = node

    def add_next(self, node):
        """Insert the given node next to self."""
        node.prev = self
        node.next = self.next
        self.next = node
        if node.next is not None:
            node.next.prev = node


# class DLListQ:
#     """Implementation of a Doubly Linked List"""
#     def __init__(self):
#         """Initialize a new doubly linked list"""
#         self.len = 0
#         self.first = None
#         self.last = None

#     def __len__(self):
#         """Return length of underlying doubly linked list"""
#         return self.len

#     def push(self )