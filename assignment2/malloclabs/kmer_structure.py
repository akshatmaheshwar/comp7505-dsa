"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

MallocLabs K-mer Querying Structure
"""

from typing import Any

"""
You may wish to import your data structures to help you with some of the
problems. Or maybe not.
"""
from structures.bit_vector import BitVector
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList, Node


class KmerStore:
    """
    A data structure for maintaining and querying k-mers.
    You may add any additional functions or member variables
    as you see fit.
    At any moment, the structure is maintaining n distinct k-mers.
    """

    def __init__(self, k: int) -> None:
        self.kmers_list = DynamicArray()
        self.count_list = DynamicArray()
        self.prefix_list = [0] * 16

    def read(self, infile: str) -> None:
        """
        Given a path to an input file, break the sequences into
        k-mers and load them into your data structure.
        """
        pass

    def convert_prefix_to_index(self, first_char, second_char):
        first = 0
        second = 0
        if first_char == 'A':
            first = 0
        elif first_char == 'C':
            first = 1
        elif first_char == 'G':
            first = 2
        elif first_char == 'T':
            first = 3
        if second_char == 'A':
            second = 0
        elif second_char == 'C':
            second = 1
        elif second_char == 'G':
            second = 2
        elif second_char == 'T':
            second = 3
        return (first << 2) | second

    def batch_insert(self, kmers: list[str]) -> None:
        """
        Given a list of m k-mers, delete the matching ones
        (including all duplicates).
        [V2: Correction]
        If the data structure contains n elements, and the input kmer list
        contains m elements, the targeted time complexity is:
        O(m log m) + O(n + m) amortized time (or better, of course!)
        """
        temp_kmers = []
        temp_count = []
        array = DynamicArray()
        array.copy_list(kmers)
        array.sort()
        old_list_ptr = 0
        new_list_ptr = 0
        for i in kmers:
            self.prefix_list[self.convert_prefix_to_index(i[0], i[1])] += 1
        while old_list_ptr < self.kmers_list.get_size() or new_list_ptr < array.get_size():
            if old_list_ptr == self.kmers_list.get_size():
                if len(temp_kmers) == 0 or temp_kmers[len(temp_kmers) - 1] != array[new_list_ptr]:
                    temp_kmers.append(array[new_list_ptr])
                    temp_count.append(0)
                temp_count[len(temp_count) - 1] += 1
                new_list_ptr += 1
            elif new_list_ptr == array.get_size():
                if len(temp_kmers) == 0 or temp_kmers[len(temp_kmers) - 1] != self.kmers_list[old_list_ptr]:
                    temp_kmers.append(self.kmers_list[old_list_ptr])
                    temp_count.append(self.count_list[old_list_ptr])
                old_list_ptr += 1
            elif self.kmers_list[old_list_ptr] < array[new_list_ptr]:
                if len(temp_kmers) == 0 or temp_kmers[len(temp_kmers) - 1] != self.kmers_list[old_list_ptr]:
                    temp_kmers.append(self.kmers_list[old_list_ptr])
                    temp_count.append(self.count_list[old_list_ptr])
                old_list_ptr += 1
            elif array[new_list_ptr] < self.kmers_list[old_list_ptr]:
                if len(temp_kmers) == 0 or temp_kmers[len(temp_kmers) - 1] != array[new_list_ptr]:
                    temp_kmers.append(array[new_list_ptr])
                    temp_count.append(0)
                temp_count[len(temp_count) - 1] += 1
                new_list_ptr += 1
            elif array[new_list_ptr] == self.kmers_list[old_list_ptr]:
                if len(temp_kmers) == 0 or temp_kmers[len(temp_kmers) - 1] != array[new_list_ptr]:
                    temp_kmers.append(array[new_list_ptr])
                    temp_count.append(self.count_list[old_list_ptr])
                temp_count[len(temp_count) - 1] += 1
                new_list_ptr += 1
                old_list_ptr += 1
        self.kmers_list.copy_list(temp_kmers)
        self.count_list.copy_list(temp_count)

    def batch_delete(self, kmers: list[str]) -> None:
        """
        Given a list of m k-mers, delete the matching ones
        (including all duplicates).
        [V2: Correction]
        If the data structure contains n elements, and the input kmer list
        contains m elements, the targeted time complexity is:
        O(m log m) + O(n + m) amortized time (or better, of course!)
        """
        array = DynamicArray()
        array.copy_list(kmers)
        array.sort()
        temp_kmer = []
        temp_count = []
        ptr = 0
        for i in range(0, self.kmers_list.get_size()):
            while ptr < array.get_size() and self.kmers_list[i] > array[ptr]:
                ptr += 1
            if ptr < array.get_size() and self.kmers_list[i] == array[ptr]:
                self.prefix_list[self.convert_prefix_to_index(array[ptr][0], array[ptr][1])] -= self.count_list[i]
                ptr += 1
                continue
            temp_kmer.append(self.kmers_list[i])
            temp_count.append((self.count_list[i]))
        self.kmers_list.copy_list(temp_kmer)
        self.count_list.copy_list(temp_count)

    def freq_geq(self, m: int) -> list[str]:
        """
        Given an integer m, return a list of k-mers that occur
        >= m times in your data structure.
        Time complexity for full marks: O(n)
        """
        result = []
        for i in range(0, self.count_list.get_size()):
            if self.count_list[i] >= m:
                result.append(self.kmers_list[i])
        return result

    def count(self, kmer: str) -> int:
        """
        Given a k-mer, return the number of times it appears in
        your data structure.
        Time complexity for full marks: O(log n)
        """
        idx = self.kmers_list.binarySearch(kmer)
        if idx == -1:
            return 0
        return self.count_list[idx]

    def count_geq(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of k-mers that
        are lexicographically greater or equal.
        Time complexity for full marks: O(log n)
        """
        result = 0
        for i in range(self.convert_prefix_to_index(kmer[0], kmer[1]), 16):
            result += self.prefix_list[i]
        idx = self.kmers_list.binarySearch(kmer)
        for i in range(idx-1, -1, -1):
            if self.kmers_list[i][0] < kmer[0] or self.kmers_list[i][1] < kmer[1]:
                break
            result -= self.count_list[i]
        return result

    def compatible(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of compatible
        k-mers. You will be using the two suffix characters
        of the input k-mer to compare against the first two
        characters of all other k-mers.
        Time complexity for full marks: O(1) :-)
        """
        return self.prefix_list[~(self.convert_prefix_to_index(kmer[len(kmer)-2], kmer[len(kmer)-1])) & ((1 << 4) - 1)]

    # Any other functionality you may need

ks = KmerStore(3)
ks.batch_insert(["GTC", "TCG", "CGT","GAA","GAT", "TGA","GTA","GAA", "GAC", "GAC", "AAG", "GTC", "TCG"])
print(ks.kmers_list)
print(ks.count_list)
print(ks.count_geq("GAT"))
# print(ks.kmers_list)
# ks.batch_delete(["TCG"])
# print(ks.prefix_list)
# print(bin(ks.convert_prefix_to_index('T', 'G')))
# print(ks.compatible("GAC"))
# ks.batch_insert(["GTC", "TCG", "CGT", "TGA", "GAA", "AAG", "GTC", "TCG"])
# print(ks.kmers_list)
# print(ks.count_list)
# print(ks.kmers_list.get_size())
# ks.batch_delete(["GTC","CGT","GAA"])
# ks.batch_insert(["GAA","TGA","TGA","TGA","TGA"])
# ks.batch_delete(["GTC","CGT","TGA"])
# print(ks.kmers_list)
# print(ks.count_list)
# print(ks.freq_geq(2))
