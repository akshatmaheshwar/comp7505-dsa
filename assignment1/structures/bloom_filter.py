"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.bit_vector import BitVector
from structures.util import object_to_byte_array


class BloomFilter:
    """
    A BloomFilter uses a BitVector as a container. To insert a given key, we
    hash the key using a series of h unique hash functions to set h bits.
    Looking up a given key follows the same logic, but only checks if all
    bits are set or not.

    Note that a BloomFilter is considered static. It is initialized with the
    number of total keys desired (as a parameter) and will not grow. You
    must decide what this means in terms of allocating your bitvector space
    accordingly.

    You can add functions if you need to.

    *** A NOTE ON KEYS ***
    We will only ever use int or str keys.
    We will not use `None` as a key.
    You might like to look at the `object_to_byte_array` function
    stored in util.py -- This function can be used to convert a string
    or integer key into a byte array, and then you can use the byte array
    to make your own hash function (bytes are just integers in the range
    [0-255] of course).
    """

    def __init__(self, max_keys: int) -> None:
        # You should use max_keys to decide how many bits your bitvector
        # should have, and allocate it accordingly.
        self._data = BitVector()
        self._data.allocate(max_keys * 10)
        self._is_empty = True

        # More variables here if you need, of course

    def __str__(self) -> str:
        """
        A helper that allows you to print a BloomFilter type
        via the str() method.
        This is not marked. <<<<
        """
        pass

    def fnv1a_hash(self, byte_array: bytes) -> int:
        """
        FNV-1a hash function (32-bit). It uses a prime multiplier and XORs
        the current hash value with each byte of the input.
        """
        FNV_prime = 0x01000193  # 16777619
        FNV_offset_basis = 0x811C9DC5  # 2166136261

        hash_value = FNV_offset_basis
        for byte in byte_array:
            hash_value ^= byte
            hash_value = (hash_value * FNV_prime) & 0xFFFFFFFF  # Limiting to 32 bits

        return hash_value

    def insert(self, key: Any) -> None:
        """
        Insert a key into the Bloom filter.
        """
        self._is_empty = False
        key_bytes = object_to_byte_array(key)
        hashed_value = self.fnv1a_hash(key_bytes)
        bit_index = hashed_value % self.get_capacity()
        self._data[bit_index] = 1

    def contains(self, key: Any) -> bool:
        """
        Check if a key is probably in the Bloom filter.
        """
        key_bytes = object_to_byte_array(key)
        hashed_value = self.fnv1a_hash(key_bytes)
        bit_index = hashed_value % self.get_capacity()
        return self._data[bit_index] == 1

    def __contains__(self, key: Any) -> bool:
        """
        Same as contains, but lets us do magic like:
        `if key in my_bloom_filter:`
        Time complexity for full marks: O(1)
        """
        return self.contains(key)

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us
        if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return self._is_empty

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity for full marks: O(1)
        """
        return self._data.get_size()


# def test_bloom() -> None:
#     """
#     Bloom Filter tests. Not marked.
#     """
#     # Seed PRNG
#     random.seed(1337)
#
#     # Some parameters we might like to mess around with
#     MAX_KEYS = 200_000
#     GEN_MAX = 100_000
#     MIN_LEN = 5
#     MAX_LEN = 15
#
#     print("==== Executing BFF Tests ====")
#     bf = BloomFilter(MAX_KEYS)
#     assert bf.is_empty() == True, "Error: is_empty() is not True on an empty BF."
#
#     print("Generating", GEN_MAX, "random strings to insert into the BF...")
#     alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
#     random_strings = [''.join(random.choice(alphabet) for _ in range(random.randint(MIN_LEN, MAX_LEN))) for _ in
#                       range(GEN_MAX)]
#     print("Removing duplicates...")
#     random_strings = list(set(random_strings))
#     print("Retained", len(random_strings), "elements...")
#
#     # Now add them to the BF
#     print("Adding all strings to the BF now...")
#     for string in random_strings:
#         bf.insert(string)
#     print("Done!")
#
#     # Now look them all up
#     print("Now looking up every key; the BF must return true for every single one.")
#     for string in random_strings:
#         assert bf.contains(string) == True, "Bloom Filter did not return True for a key that was inserted."
#
#     # Now generate some new random strings
#     print("Generating new query strings that ARE NOT contained in the BF...")
#     query_strings = [''.join(random.choice(alphabet) for _ in range(random.randint(5, 15))) for _ in range(100000)]
#     query_strings = list(set(query_strings).difference(random_strings))
#     print("Retained", len(query_strings), "query strings that are NOT in the BF.")
#
#     # Now we'll look for these; we might get false positives, so we can measure
#     # this and return the false positive rate
#     pos = 0
#     for string in query_strings:
#         if bf.contains(string):
#             pos += 1
#     print("Querying for", len(query_strings), "unique strings not in the BF returned a count of", pos,
#           " 'True' - False positive rate = ", pos / len(query_strings))
#
#
# test_bloom()
