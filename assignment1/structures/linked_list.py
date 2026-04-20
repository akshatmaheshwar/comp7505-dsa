"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

# so we can hint DLLNode get_next
from __future__ import annotations
from collections.abc import Iterator
from typing import Any


class DLLNode:
    """
    A simple type to hold data and a next pointer.
    Note the name change; Node is a "graph" class type, so we call linked
    list nodes DLLNode instead.
    """

    def __init__(self, data: Any) -> None:
        """
        Store some data, and a prev/next ptr.
        """
        self._data = data
        self._next = None
        self._prev = None

    def set_data(self, data: Any) -> None:
        self._data = data

    def get_data(self) -> Any:
        return self._data

    def set_next(self, node: DLLNode) -> None:
        self._next = node

    def get_next(self) -> DLLNode | None:
        return self._next

    def set_prev(self, node: DLLNode) -> None:
        self._prev = node

    def get_prev(self) -> DLLNode | None:
        return self._prev


class DoublyLinkedList:
    """
    A simplified Doubly Linked List Class.
    """

    def __init__(self) -> None:
        self._head = None
        self._tail = None
        self._size = 0

    def __str__(self) -> str:
        """
        A helper that allows you to print a DoublyLinkedList type
        via the str() method.
        """
        list_str = "[HEAD] "
        cur = self._head
        # handle special head print
        if cur is not None:
            list_str += str(cur.get_data())
        cur = cur.get_next()
        # Loops across the LL
        while cur is not None:
            list_str += "<->" + str(cur.get_data())
            cur = cur.get_next()
        list_str += " [TAIL]"
        return list_str

    def get_size(self) -> int:
        """
        Return the size of the list.
        Time complexity for full marks: O(1)
        """
        return self._size

    def get_head(self) -> Any | None:
        """
        Return the data of the leftmost node in the list, if it exists.
        """
        cur = self._head
        if cur is not None:
            return cur.get_data()
        return None

    def get_head_node(self) -> DLLNode | None:
        """
        Return the head node itself, not just the data
        """
        return self._head

    def set_head(self, data: Any) -> None:
        """
        Replace the leftmost node's data with the given data.
        If the list is empty, do nothing.
        """
        cur = self._head
        if cur is not None:
            cur.set_data(data)

    def get_tail(self) -> Any | None:
        """
        Return the data of the rightmost node in the list, if it exists.
        """
        cur = self._tail
        if cur is not None:
            return cur.get_data()
        return None

    def set_tail(self, data: Any) -> None:
        """
        Replace the rightmost node's data with the given data.
        If the list is empty, do nothing.
        """
        cur = self._tail
        if cur is not None:
            cur.set_data(data)
    
    def insert_to_front(self, data: Any) -> None:
        """
        Insert a new Node containing this data to the head of the LL
        """
        node = DLLNode(data)
        cur = self._head
        if cur is not None:
            node.set_next(cur)
            cur.set_prev(node)
        else:
            self._tail = node
        self._head = node
        self._size += 1

    def insert_to_back(self, data: Any) -> None:
        """
        Insert a new Node containing this data to the tail of the LL
        """
        node = DLLNode(data)
        cur = self._tail
        if cur is not None:
            cur.set_next(node)
            node.set_prev(cur)
        else:
            self._head = node
        self._tail = node
        self._size += 1

    def remove_from_front(self) -> Any | None:
        """
        Remove and return the front element
        """
        if self._size == 0:
            return None
        
        cur = self._head
        
        if self._size == 1:
            self._head = None
            self._tail = None
            self._size = 0
            return cur.get_data()

        self._head = cur.get_next()
        self._head.set_prev(None)
        self._size -= 1
        return cur.get_data()

    def remove_from_back(self) -> Any | None:
        """
        Remove and return the back element
        """
        if self._size == 0:
            return None

        cur = self._tail
        
        if self._size == 1:
            self._head = None
            self._tail = None
            self._size = 0
            return cur.get_data()

        self._tail = cur.get_prev()
        self._tail.set_next(None)
        self._size -= 1
        return cur.get_data()

    def find_element(self, elem: Any) -> bool:
        """
        Looks at the data inside each node of the list and returns the
        node if it matches the input elem; returns None otherwise
        """
        cur = self._head
        while cur is not None:
            if cur.get_data() == elem:
                return True
            cur = cur.get_next()
        return False

    def find_and_return_element(self, elem: Any) -> Any | None:
        """
        Looks at the data inside each node of the list and returns the
        node data if it matches the input elem; returns None otherwise
        """
        cur = self._head
        while cur is not None:
            if cur.get_data() == elem:
                return cur.get_data()
            cur = cur.get_next()
        return None



    def find_and_remove_element(self, elem: Any) -> bool:
        """
        Finds, removes, and returns the first instance of elem
        (based on the node data) or returns None if the element is not found.
        """
        # 1. Search and get a reference on the first match
        cur = self._head
        while cur is not None:
            if cur.get_data() == elem:
                break
            cur = cur.get_next()
        # Not found - easy peasy
        if cur is None:
            return False
        # Case: head is tail => single element list
        if self.get_size() == 1:
            self._head = None
            self._tail = None
            self._size = 0
            return True 
        # OK: A "regular" case then
        nxt = cur.get_next()
        prv = cur.get_prev()
        # Easy case: In the middle of two nodes
        if prv is not None and nxt is not None:
            self._size -= 1
            prv.set_next(nxt)
            nxt.set_prev(prv)
            return True
        # Trickier case: At one end of the list.
        head = self._head
        tail = self._tail
        if cur is head:
            self.remove_from_front()
        else:
            self.remove_from_back()
        return True

