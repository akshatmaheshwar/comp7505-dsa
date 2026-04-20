"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

# so we can hint Node get_next
from __future__ import annotations

from typing import Any


class Node:
    """
    A simple type to hold data and a next pointer
    """

    def __init__(self, data: Any) -> None:
        self._data = data  # This is the payload data of the node
        self._next = None  # This is the "next" pointer to the next Node
        self._prev = None  # This is the "previous" pointer to the previous Node

    def set_data(self, data: Any) -> None:
        self._data = data

    def get_data(self) -> Any:
        return self._data

    def set_next(self, node: Node) -> None:
        self._next = node

    def get_next(self) -> Node | None:
        return self._next

    def set_prev(self, node: Node) -> None:
        self._prev = node

    def get_prev(self) -> Node | None:
        return self._prev


class DoublyLinkedList:
    """
    Your doubly linked list code goes here.
    Note that any time you see `Any` in the type annotations,
    this refers to the "data" stored inside a Node.

    [V3: Note that this API was changed in the V3 spec] 
    """

    def __init__(self) -> None:
        # You probably need to track some data here...
        self.size = 0
        self.head: Node = None
        self.tail: Node = None
        self.is_reversed: bool = False

    def __str__(self) -> str:
        """
        A helper that allows you to print a DoublyLinkedList type
        via the str() method.
        """
        if not self.is_reversed:
            temp = self.head
            result = ""
            while temp is not None:
                result += (str(temp.get_data()))
                if temp.get_next() is not None:
                    result += "<->"
                temp = temp.get_next()
            return result
        else:
            temp = self.tail
            result = ""
            while temp is not None:
                result += (str(temp.get_data()))
                if temp.get_prev() is not None:
                    result += "<->"
                temp = temp.get_prev()
            return result

    """
    Simple Getters and Setters below
    """

    def get_size(self) -> int:
        """
        Return the size of the list.
        Time complexity for full marks: O(1)
        """
        return self.size

    def get_head(self) -> Any | None:
        """
        Return the data of the leftmost node in the list, if it exists.
        Time complexity for full marks: O(1)
        """
        head = self.tail if self.is_reversed else self.head
        if self.size != 0:
            return head.get_data()

    def set_head(self, data: Any) -> None:
        """
        Replace the leftmost node's data with the given data.
        If the list is empty, do nothing.
        Time complexity for full marks: O(1)
        """
        head = self.tail if self.is_reversed else self.head
        if data is None:
            return
        if self.size != 0:
            head.set_data(data)

    def get_tail(self) -> Any | None:
        """
        Return the data of the rightmost node in the list, if it exists.
        Time complexity for full marks: O(1)
        """
        tail = self.head if self.is_reversed else self.tail
        if self.size != 0:
            return tail.get_data()

    def set_tail(self, data: Any) -> None:
        """
        Replace the rightmost node's data with the given data.
        If the list is empty, do nothing.
        Time complexity for full marks: O(1)
        """
        tail = self.head if self.is_reversed else self.tail
        if data is None:
            return
        if self.size != 0:
            tail.set_data(data)

    """
    More interesting functionality now.
    """

    def insert_to_front(self, data: Any) -> None:
        """
        Insert the given data to the front of the list.
        Hint: You will need to create a Node type containing
        the given data.
        Time complexity for full marks: O(1)
        """
        if not self.is_reversed:
            temp = Node(data)
            if self.head is not None:
                temp.set_next(self.head)
                self.head.set_prev(temp)
            else:
                self.tail = temp
            self.head = temp
            self.size += 1
        else:
            temp = Node(data)
            if self.tail is not None:
                self.tail.set_next(temp)
                temp.set_prev(self.tail)
            else:
                self.head = temp
            self.tail = temp
            self.size += 1

    def insert_to_back(self, data: Any) -> None:
        """
        Insert the given data (in a node) to the back of the list
        Time complexity for full marks: O(1)
        """
        if not self.is_reversed:
            temp = Node(data)
            if self.tail is not None:
                self.tail.set_next(temp)
                temp.set_prev(self.tail)
            else:
                self.head = temp
            self.tail = temp
            self.size += 1
        else:
            temp = Node(data)
            if self.head is not None:
                temp.set_next(self.head)
                self.head.set_prev(temp)
            else:
                self.tail = temp
            self.head = temp
            self.size += 1

    def remove_from_front(self) -> Any | None:
        """
        Remove the front node, and return the data it holds.
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return None
        if not self.is_reversed:
            temp = self.head
            if self.size == 1:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.get_next()
                if self.head:
                    self.head.set_prev(None)
            self.size -= 1
            return temp.get_data()
        else:
            temp = self.tail
            if self.size == 1:
                self.head = None
                self.tail = None
            else:
                self.tail = self.tail.get_prev()
                if self.tail:
                    self.tail.set_next(None)
            self.size -= 1
            return temp.get_data()

    def remove_from_back(self) -> Any | None:
        """
        Remove the back node, and return the data it holds.
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return None
        if not self.is_reversed:
            temp = self.tail
            if self.size == 1:
                self.head = None
                self.tail = None
            else:
                self.tail = self.tail.get_prev()
                if self.tail:
                    self.tail.set_next(None)
            self.size -= 1
            return temp.get_data()
        else:
            temp = self.head
            if self.size == 1:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.get_next()
                if self.head:
                    self.head.set_prev(None)
            self.size -= 1
            return temp.get_data()

    def find_element(self, elem: Any) -> bool:
        """
        Looks at the data inside each node of the list and returns True
        if a match is found; False otherwise.
        Time complexity for full marks: O(N)
        """
        temp = self.head
        while temp is not None:
            if temp.get_data() == elem:
                return True
            temp = temp.get_next()
        return False

    def find_and_remove_element(self, elem: Any) -> bool:
        """
        Looks at the data inside each node of the list; if a match is
        found, this node is removed from the linked list, and True is returned.
        False is returned if no match is found.
        Time complexity for full marks: O(N)
        """
        temp = self.head
        while temp:
            if temp.get_data() == elem:
                if temp == self.head:
                    return self.remove_from_front() is not None
                elif temp == self.tail:
                    return self.remove_from_back() is not None
                else:
                    temp.get_prev().set_next(temp.get_next())
                    temp.get_next().set_prev(temp.get_prev())
                    self.size -= 1
                    return True
            temp = temp.get_next()
        return False

    def reverse(self) -> None:
        """
        Reverses the linked list
        Time complexity for full marks: O(1)
        """
        self.is_reversed = not self.is_reversed
