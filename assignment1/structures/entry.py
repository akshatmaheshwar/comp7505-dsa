"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.util import Hashable, object_to_byte_array, get_hash_of_obj


class Entry(Hashable):
    """
    Implements a simple type that holds keys and values. Extends the Hashable
    type to ensure get_hash() is available/used for arbitrary key types.

    You can add to the API, but do not change what is already here.
    """

    def __init__(self, key: Any, value: Any) -> None:
        """
        An entry has a key (used for comparing to other entries or for hashing)
        and a corresponding value which represents some arbitrary data associated
        with the key.
        """
        super().__init__()
        self._key = key
        self._value = value

    def get_key(self) -> Any:
        return self._key

    def get_value(self) -> Any:
        return self._value

    def update_key(self, nk: Any) -> None:
        self._key = nk

    def update_value(self, nv: Any) -> None:
        self._value = nv

    def __eq__(self, other) -> bool:
        """
        Compares two Entry objects by their keys; returns true if keys are
        equal, false otherwise. Relies on keys having __eq__ implemented.
        """
        return self.get_key() == other.get_key()

    def __lt__(self, other) -> bool:
        """
        Compares two Entry objects by their keys; returns true if self is less
        than other. Relies on keys having __lt__ implemented.
        """
        return self.get_key() < other.get_key()

    def get_hash(self) -> int:
        """
        Returns a hash of self._key - this hash function MUST be implemented if
        you need to hash Entry types. In other words, do not use Python's magic
        __hash__() function, but rather, you need to make your own. You are
        welcome to use existing functions, but you need to implement it here
        (and cite it in your statement file).

        As a hint: We can treat any object as bytes (and bytes as integers in
        the range [0, 2**8] which may help us with hashing. Look inside util.py
        to see object_to_byte_array() for example.

        This function might be better named "prehash" - this function is just
        trying to convert a key to an integer in the universe (and in this
        assignment, your universe could be something like integers in
        [0, 2^32-1].
        """
        return get_hash_of_obj(self._key)


class Compound:
    """
    Implements the Compound Type used in Task 3.3. Please do not modify this
    class.
    """

    def __init__(self, x: int, y: int, r: float, cid: int) -> None:
        self._x = x
        self._y = y
        self._r = r
        self._cid = cid

    def get_coordinates(self) -> tuple[int, int]:
        return (self._x, self._y)

    def get_radius(self) -> float:
        return self._r

    def get_compound_id(self) -> int:
        return self._cid

    def __str__(self) -> str:
        return ("x = " + str(self._x) +
                ", y = " + str(self._y) +
                ", r = " + str(self._r) +
                ", cid = " + str(self._cid))


class Offer:
    """
    Implements the Offer Type used in Task 3.4. Please do not modify this
    class.
    """

    def __init__(self, n: int, m: int, k: int, cost: int, oid: int) -> None:
        self._n = n
        self._m = m
        self._k = k
        self._cost = cost
        self._oid = oid

    def get_n(self) -> int:
        return self._n

    def get_m(self) -> int:
        return self._m

    def get_k(self) -> int:
        return self._k

    """ Friendlier names """

    def get_num_nodes(self) -> int:
        return self._n

    def get_num_edges(self) -> int:
        return self._m

    def get_diameter(self) -> int:
        return self._k

    def get_cost(self) -> int:
        return self._cost

    def get_offer_id(self) -> int:
        return self._oid

    def __str__(self) -> str:
        return ("n = " + str(self._n) +
                ", m = " + str(self._m) +
                ", k = " + str(self._k) +
                ", cost = " + str(self._cost) +
                ", oid = " + str(self._oid))
