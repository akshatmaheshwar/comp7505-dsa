"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from collections.abc import Iterator
from random import randint


class DynamicArray:
    """
    A simplified *append only* dynamic array. We have removed some of the
    tricky functionality from A1. If you want/need that, check out the
    solution we provided for A1.
    """

    def __init__(self) -> None:
        self._data = [None] * 128
        self._size = 0
        self._capacity = 128

    def __str__(self) -> str:
        """
        A helper that allows you to print a DynamicArray type
        via the str() method.
        """
        string_rep = "["
        for elem in self._data:
            string_rep += str(elem) + ", "
        string_rep += "]"
        return string_rep

    def __resize(self) -> None:
        """
        Double when full: O(1*) appends.
        """
        self._capacity = self._capacity * 2
        new_list = [None] * self._capacity
        for i in range(self._size):
            new_list[i] = self._data[i]
        self._data = new_list

    def build_from_list(self, inlist: list) -> None:
        """
        Given a python list, take ownership of it.
        """
        self._data = inlist
        self._capacity = len(inlist)
        self._size = len(inlist)

    def allocate(self, elements_desired: int, default_val: Any) -> None:
        """
        Allow the user to allocate a slab of elements at once, all
        initialized to the default value
        """
        self._data = [default_val] * elements_desired
        self._size = elements_desired
        self._capacity = elements_desired

    def get_at(self, index: int) -> Any | None:
        """
        Get element at the given index.
        Return None if index is out of bounds.
        """
        if index >= 0 and index < self._size:
            return self._data[index]
        return None

    def __getitem__(self, index: int) -> Any | None:
        """
        Same as get_at.
        Allows to use square brackets to index elements.
        """
        return self.get_at(index)

    def set_at(self, index: int, element: Any) -> None:
        """
        Get element at the given index.
        Do not modify the list if the index is out of bounds.
        """
        if index >= 0 and index < self._size:
            self._data[index] = element

    def __setitem__(self, index: int, element: Any) -> None:
        """
        Same as set_at.
        Allows to use square brackets to index elements.
        """
        self.set_at(index, element)

    def append(self, element: Any) -> None:
        """
        Add an element to the back of the array.
        """
        if self._size == self._capacity:
            self.__resize()
        self._data[self._size] = element
        self._size += 1

    def remove(self, element: Any) -> None:
        """
        Remove the first occurrence of the element from the array.
        If there is no such element, leave the array unchanged.
        """
        found_idx = -1
        for idx in range(self._size):
            if self._data[idx] == element:
                self.remove_at(idx)
                return

    def remove_at(self, index: int) -> Any | None:
        """
        Remove the element at the given index from the array and return the removed element.
        If there is no such element, leave the array unchanged and return None.
        """
        elem = None
        if index >= 0 and index < self._size:
            elem = self._data[index]
            for i in range(index, self._size - 1):
                self._data[i] = self._data[i + 1]
            self._size -= 1
            self._data[self._size] = None
        return elem

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        """
        return self._size == 0

    def is_full(self) -> bool:
        """
        Boolean helper to tell us if the structure is full or not
        """
        return self._size == self._capacity

    def get_size(self) -> int:
        """
        Return the number of elements in the list
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of slots) of the list
        """
        return self._capacity

    def sort(self) -> None:
        """
        Sort elements inside _data based on < comparisons.
        """
        self.__qsort(0, self._size - 1)

    def __qsort(self, lo: int, hi: int) -> None:
        """
        A simple randomized quicksort
        """
        if lo >= hi:
            return
        pivot = self.__random_pivot(lo, hi)
        self.__qsort(lo, pivot)
        self.__qsort(pivot + 1, hi)

    def __random_pivot(self, lo: int, hi: int) -> int:
        """
        Return the index of the pivot after shuffling elements into < and >
        """
        pidx = randint(lo, hi)
        pivot = self._data[pidx]
        left = lo - 1
        right = hi + 1

        # Loop until we've moved everything around the pivot into < and >
        # groups.
        while True:
            left += 1
            # Find an element smaller than the pivot
            while self._data[left] < pivot:
                left += 1

            right -= 1
            # Find an element greater than the pivot
            while self._data[right] > pivot:
                right -= 1

            # If true, we are done; it means the list is already segmented,
            # so back out at this point
            if left >= right:
                return right

            # Otherwise, we swap the elements and continue
            self._data[left], self._data[right] = self._data[right], self._data[left]
