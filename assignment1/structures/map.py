"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation.
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""
import random
from typing import Any
from structures.entry import Entry
from structures.linked_list import DoublyLinkedList
from structures.util import get_hash_of_obj


class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self._map = [None] * 10
        self.size = 0

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, you must return the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity for full marks: O(1*)
        """
        hash_key = entry.get_hash() % len(self._map)
        curent_value = self.find(entry.get_key())
        if curent_value is not None:
            self.remove(entry.get_key())
        if self._map[hash_key] is None:
            self._map[hash_key] = DoublyLinkedList()
        self._map[hash_key].insert_to_back(entry)
        self.size += 1
        n = len(self._map)
        if self.size / n > 0.75:
            n *= 2
            old_map = self._map
            self._map = [None] * n
            for i in range(len(old_map)):
                if old_map[i] is not None:
                    curr = old_map[i].get_head_node()
                    while curr:
                        self.size -= 1
                        self.insert(curr.get_data())
                        curr = curr.get_next()
        return curent_value

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind. You can modify this if you want, as long as it behaves.
        Time complexity for full marks: O(1*)
        """
        # hint: entry = Entry(key, value)
        return self.insert(Entry(key, value))

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        Time complexity for full marks: O(1*)
        """
        self.insert_kv(key, value)

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity for full marks: O(1*)
        """
        hash_key = get_hash_of_obj(key) % len(self._map)
        if self._map[hash_key] is None:
            return
        cur = self._map[hash_key].get_head_node()
        while cur is not None:
            if cur.get_data().get_key() == key:
                break
            cur = cur.get_next()
        # Not found - easy peasy
        if cur is None:
            return
        self.size -= 1
        # Case: head is tail => single element list
        if self._map[hash_key].get_size() == 1:
            self._map[hash_key]._head = None
            self._map[hash_key]._tail = None
            self._map[hash_key]._size = 0
            return
            # OK: A "regular" case then
        nxt = cur.get_next()
        prv = cur.get_prev()
        # Easy case: In the middle of two nodes
        if prv is not None and nxt is not None:
            self._map[hash_key]._size -= 1
            prv.set_next(nxt)
            nxt.set_prev(prv)
            return
            # Trickier case: At one end of the list.
        head = self._map[hash_key]._head
        tail = self._map[hash_key]._tail
        if cur is head:
            self._map[hash_key].remove_from_front()
        else:
            self._map[hash_key].remove_from_back()
        return

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity for full marks: O(1*)
        """
        hash_key = get_hash_of_obj(key) % len(self._map)
        if self._map[hash_key] is not None:
            cur = self._map[hash_key].get_head_node()
            while cur is not None:
                if cur.get_data().get_key() == key:
                    return cur.get_data().get_value()
                cur = cur.get_next()
        return None

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        Time complexity for full marks: O(1*)
        """
        return self.find(key)

    def get_size(self) -> int:
        """
        Time complexity for full marks: O(1)
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Time complexity for full marks: O(1)
        """
        return self.size == 0


# random.seed(1337)
# print("==== Executing Map Tests ====")
# my_map = Map()
# my_map.insert_kv(0,4)
# print(my_map.get_size())
# my_map.insert_kv(0,7)
# print(my_map.get_size())
# my_map[0] = 0
# my_map[1] = 1
# my_map[2] = 2
# my_map[3] = 3
# my_map[4] = 4
# my_map[5] = 5
# my_map[6] = 6
# my_map[7] = 7
# my_map[8] = 8
# my_map[9] = 9
# my_map[10] = 10
# my_map[11] = 11
# my_map[12] = 12
# print(my_map.get_size())
# print(my_map[10])

# print(Entry(1,1) == Entry(1,1))