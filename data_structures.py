"""
Data Structures for FlowTex Factory Simulator
Custom implementations of Queue, Stack, and Linked List
"""


class Queue:
    """FIFO (First In First Out) Queue implementation"""
    
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Add item to the end of the queue"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return item from the front of the queue"""
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Get the number of items in the queue"""
        return len(self.items)
    
    def display(self):
        """Get all items in the queue (without removing them)"""
        return self.items.copy()
    
    def peek(self):
        """View the front item without removing it"""
        if self.is_empty():
            return None
        return self.items[0]


class Stack:
    """LIFO (Last In First Out) Stack implementation"""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to the top of the stack"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return item from the top of the stack"""
        if self.is_empty():
            return None
        return self.items.pop()
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self.items) == 0
    
    def peek(self):
        """View the top item without removing it"""
        if self.is_empty():
            return None
        return self.items[-1]
    
    def size(self):
        """Get the number of items in the stack"""
        return len(self.items)
    
    def display(self):
        """Get all items in the stack (from top to bottom)"""
        return self.items.copy()[::-1]  # Return reversed to show top first


class Node:
    """Node for Linked List"""
    
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Singly Linked List implementation"""
    
    def __init__(self):
        self.head = None
        self.length = 0
    
    def append(self, item):
        """Add item to the end of the linked list"""
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.length += 1
    
    def display(self):
        """Get all items in the linked list as a list"""
        items = []
        current = self.head
        while current is not None:
            items.append(current.data)
            current = current.next
        return items
    
    def size(self):
        """Get the number of items in the linked list"""
        return self.length
    
    def is_empty(self):
        """Check if linked list is empty"""
        return self.head is None

