"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.dynamic_array import DynamicArray


class BitVector:
    """
    A compact storage for bits that uses DynamicArray under the hood.
    Each element stores up to 64 bits, making BitVector 64 times more
    memory-efficient for storing bits than plain DynamicArray.
    This is a simplified "append only" version without any
    flips, rotates, etc.
    """

    BITS_PER_ELEMENT = 64
    BYTES_PER_ELEMENT = 8

    def __init__(self) -> None:
        """
        We will use the dynamic array as our data storage mechanism.
        We also track how many elements we are storing, an offset into each
        of the end integers.
        """
        self._data = DynamicArray()
        self._size = 0
        self._right_offset = -1

    def __str__(self) -> str:
        """
        A helper that allows you to print a BitVector type
        via the str() method.
        """
        bits = ""
        for i in range(self._size):
            bits += str(self.get_at(i))
        return bits

    def __repr__(self):
        return self.__str__()

    def __resize(self) -> None:
        pass

    def allocate(self, bits_desired: int) -> None:
        """
        Allow the user to allocate a slab of bits at once, all initialized
        to zero.
        """
        # Ceil division, see: https://stackoverflow.com/q/14822184/
        ints_required = -(bits_desired // -self.BITS_PER_ELEMENT)
        self._data.allocate(ints_required, 0)
        self._size = bits_desired

        ptr = bits_desired % self.BITS_PER_ELEMENT

        if ptr == 0:
            self._right_offset = -1
        else:
            self._right_offset = self.BITS_PER_ELEMENT - ptr - 1

    def get_at(self, index: int) -> int | None:
        """
        Get bit at the given index.
        Return None if index is out of bounds.
        """
        if index < 0 or index >= self._size:
            return
        return self.__get(index)

    def __get(self, index: int) -> int:
        """
        Get a bit at a given position.
        """
        data_ix = index // self.BITS_PER_ELEMENT
        bit_ix = self.BITS_PER_ELEMENT - (index % self.BITS_PER_ELEMENT) - 1
        bit = self._data[data_ix] & (1 << bit_ix)
        if bit != 0:
            bit = 1
        return bit

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
        """
        self.__setitem__(index, 1)

    def unset_at(self, index: int) -> None:
        """
        Set bit at the given index to 0.
        Do not modify the vector if the index is out of bounds.
        """
        self.__setitem__(index, 0)

    def __setitem__(self, index: int, state: int) -> None:
        """
        Set bit at the given index.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Do not modify the vector if the index is out of bounds.
        """

        if index < 0 or index >= self._size:
            return
        if state != 0:
            state = 1
        self.__assign(index, state)

    def __assign(self, index: int, state: int) -> None:
        """
        Assign a state to a given index (bit)
        """
        data_ix = index // self.BITS_PER_ELEMENT
        bit_ix = self.BITS_PER_ELEMENT - (index % self.BITS_PER_ELEMENT) - 1
        if state == 1:
            self._data[data_ix] |= (state << bit_ix)
        else:
            self._data[data_ix] |= (1 << bit_ix)
            self._data[data_ix] ^= (1 << bit_ix)

    def append(self, state: int) -> None:
        """
        Add a bit to the back of the vector.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if state != 0:
            state = 1
        self.__append(state)

    def __append(self, state: int) -> None:
        """
        Handle the actual append operation
        """
        if self._right_offset < 0:
            self._right_offset = self.BITS_PER_ELEMENT - 1
            self._data.append(0)
        last = self._data.get_size() - 1
        self._data[last] |= (state << self._right_offset)
        self._right_offset -= 1
        self._size += 1

    def get_size(self) -> int:
        """
        Return the number of *bits* in the list
        """
        return self._size

    def to_byte_arr(self) -> bytes:
        """
        Converts the BitVector into a byte array.
        Note that we pad the final (perhaps-not-entirely-full) integer.
        """
        byte_data = bytearray()
        for integer in self._data:
            if integer is None:
                break
            byte_data.extend(integer.to_bytes(self.BYTES_PER_ELEMENT, byteorder='big'))
        return bytes(byte_data)

    def from_byte_arr(self, byte_data: bytes) -> None:
        """
        Converts the byte array into a BitVector. Note that this will result
        in a BV that is padded to a 64-bit interval.
        """
        recovered_integers = DynamicArray()

        # Pad to 8-byte interval
        mut_bytes = bytearray(byte_data)
        while len(mut_bytes) % self.BYTES_PER_ELEMENT != 0:
            mut_bytes.append(0)

        # Extract 8-byte units as integers
        for idx in range(0, len(mut_bytes), self.BYTES_PER_ELEMENT):
            data = mut_bytes[idx:idx + self.BYTES_PER_ELEMENT]
            recovered_integers.append(int.from_bytes(data, byteorder='big'))

        # Set up the sizes and data now
        self._data = recovered_integers
        self._size = len(mut_bytes) * self.BYTES_PER_ELEMENT
        self._right_offset = -1
