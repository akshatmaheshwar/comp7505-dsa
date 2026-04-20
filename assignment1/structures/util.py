"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from abc import ABC, abstractmethod
from enum import Enum
import pickle


class Hashable(ABC):
    """
    A special object that can be inherited to enforce objects to be hashable
    """

    def __init__(self) -> None:
        """
        You are free to do anything you find suitable to initialise your
        Hashable class. But maybe you don't need to do anything!
        """
        pass

    @abstractmethod
    def get_hash(self) -> int:
        """
        Return an integer hash of the given object. You MUST use this
        if you wish to hash keys of a specific type. See entry.py for more
        help in this direction, as well as map.py
        """
        pass


"""
Any other utilities can go below here.
"""


def object_to_byte_array(obj: Any) -> list[bytes]:
    """
    This converts any object into a byte array. The byte array can then
    be iterated across to yield integers. This may be useful for hashing
    arbitrary objects.
    
    Example:
    x = 1234
    x_bytes = object_to_byte_array(x)
    for byte_int in x_bytes:
        print(byte_int, type(byte_int))


    WARNING: If you are interpreting objects as byte arrays for hashing,
    you had better not let the object be mutated, or the hash will be
    different (screaming.mp4) and this will make things break. Our
    recommendation is to only use this on simple types like str or int
    """
    return pickle.dumps(obj)


def get_hash_of_obj(obj: Any) -> int:

    byte_stream = object_to_byte_array(obj)

    byte_as_integers = [b for b in byte_stream]

    hash_value = 0
    for byte in byte_as_integers:
        hash_value = (hash_value * 31 + byte) % (2 ** 32)

    return hash_value
