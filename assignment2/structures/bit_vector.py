"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""
from __future__ import annotations

from typing import Any

from structures.dynamic_array import DynamicArray


class BitVector:
    """
    A compact storage for bits that uses DynamicArray under the hood.
    Each element stores up to 64 bits, making BitVector 64 times more memory-efficient
    for storing bits than plain DynamicArray.
    """

    BITS_PER_ELEMENT = 64

    def __init__(self) -> None:
        """
        We will use the dynamic array as our data storage mechanism
        """
        self._data = DynamicArray()
        self.is_flipped = False
        # you may want or need more stuff here in the constructor

    def __str__(self) -> str:
        """
        A helper that allows you to print a BitVector type
        via the str() method.
        """
        return str(self._data)

    def __resize(self) -> None:
        pass

    def get_at(self, index: int) -> int | None:
        """
        Get bit at the given index.
        Return None if index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index < 0 or index >= self._data.size:
            return
        if not self.is_flipped:
            return self._data[index]
        if self._data[index] == 1:
            return 0
        return 1

    def __getitem__(self, index: int) -> int | None:
        """
        Same as get_at.
        Allows to use square brackets to index elements.
        """
        return self.get_at(index)

    def set_at(self, index: int) -> None:
        """
        Set bit at the given index to 1.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index < 0 or index >= self._data.size:
            return
        if not self.is_flipped:
            self._data[index] = 1
        else:
            self._data[index] = 0

    def unset_at(self, index: int) -> None:
        """
        Set bit at the given index to 0.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index < 0 or index >= self._data.size:
            return
        if not self.is_flipped:
            self._data[index] = 0
        else:
            self._data[index] = 1

    def __setitem__(self, index: int, state: int) -> None:
        """
        Set bit at the given index.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if state == 0:
            self.unset_at(index)
        else:
            self.set_at(index)

    def append(self, state: int) -> None:
        """
        Add a bit to the back of the vector.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if state != 0:
            state = 1
        if self.is_flipped:
            if state == 1:
                state = 0
            else:
                state = 1
        self._data.append(state)

    def prepend(self, state: Any) -> None:
        """
        Add a bit to the front of the vector.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if state != 0:
            state = 1
        if self.is_flipped:
            if state == 1:
                state = 0
            else:
                state = 1
        self._data.prepend(state)

    def reverse(self) -> None:
        """
        Reverse the bit-vector.
        Time complexity for full marks: O(1)
        """
        self._data.reverse()

    def flip_all_bits(self) -> None:
        """
        Flip all bits in the vector.
        Time complexity for full marks: O(1)
        """
        self.is_flipped = not self.is_flipped

    def shift(self, dist: int) -> None:
        """
        Make a bit shift.
        If dist is positive, perform a left shift by `dist`.
        Otherwise perform a right shift by `dist`.
        Time complexity for full marks: O(N)
        """
        if self.get_size() == 0:
            return
        bit_to_set = 0
        if self.is_flipped:
            bit_to_set = 1
        if dist >= 0:
            dist = min(dist, self.get_size())
            for i in range(0, dist):
                self._data.remove_at(0)
                self.append(bit_to_set)
        else:
            dist *= -1
            dist = min(dist, self.get_size())
            for i in range(0, dist):
                self._data.remove_at(self._data.size - 1)
                self.prepend(bit_to_set)

    def rotate(self, dist: int) -> None:
        """
        Make a bit rotation.
        If dist is positive, perform a left rotation by `dist`.
        Otherwise perform a right rotation by `dist`.
        Time complexity for full marks: O(N)
        """
        if self.get_size() == 0:
            return
        if dist >= 0:
            dist %= self._data.get_size()
            for i in range(0, dist):
                self.append(self._data.remove_at(0))
        else:
            dist *= -1
            dist %= self._data.get_size()
            for i in range(0, dist):
                self.prepend(self._data.remove_at(self._data.size - 1))

    def get_size(self) -> int:
        """
        Return the number of *bits* in the list
        Time complexity for full marks: O(1)
        """
        return self._data.get_size()


# bv = BitVector()
# bv.append(1)
# bv.append(0)
# bv.append(1)
# bv.append(1)
# bv.append(0)
# bv.append(0)
# bv.append(0)
# bv.append(1)
# bv.append(0)
# bv.append(0)
# bv.append(0)
# bv.append(1)
# bv.append(1)
# print(bv.get_size())
# print(bv)
# bv.shift(-2)
# print(bv.get_size())
# print(bv)
# bv.rotate(-2)
# print(bv.get_size())
# print(bv)
# bv.reverse()
# bv.shift(-2)
# print(bv.get_size())
# print(bv)
# bv.rotate(-2)
# print(bv.get_size())
# print(bv)

