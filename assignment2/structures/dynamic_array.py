"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""
from __future__ import annotations

from typing import Any


class DynamicArray:
    def __init__(self) -> None:
        self.array = [None] * 3
        self.size = 0
        self.capacity = 3
        self.starting = 1
        self.is_reversed = False

    def copy_list(self, arr) -> None:
        self.array = arr
        self.size = len(arr)
        self.capacity = len(arr)
        self.starting = 0

    def __str__(self) -> str:
        """
        A helper that allows you to print a DynamicArray type
        via the str() method.
        """
        result = ""
        if not self.is_reversed:
            for i in range(self.starting, self.starting + self.size):
                result += str(self.array[i])
                if i < self.starting + self.size - 1:
                    result += ","
            return result
        else:
            for i in range(self.starting + self.size - 1, self.starting - 1, -1):
                result += str(self.array[i])
                if i > self.starting:
                    result += ","
            return result

    def __resize(self) -> None:
        new_array = [None] * (self.capacity * 2)
        new_starting = self.capacity - (self.size // 2)
        for i in range(self.starting, self.starting + self.size):
            new_array[new_starting + (i - self.starting)] = self.array[i]
        self.array = new_array
        self.starting = new_starting
        self.capacity = 2 * self.capacity

    def get_at(self, index: int) -> Any | None:
        """
        Get element at the given index.
        Return None if index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index < 0 or index >= self.size:
            return None
        return self.array[index + self.starting] if not self.is_reversed else self.array[
            (self.starting + self.size - 1) - index]

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
        Time complexity for full marks: O(1)
        """
        if 0 <= index < self.size:
            if not self.is_reversed:
                self.array[self.starting + index] = element
            else:
                self.array[(self.starting + self.size - 1) - index] = element

    def __setitem__(self, index: int, element: Any) -> None:
        """
        Same as set_at.
        Allows to use square brackets to index elements.
        """
        self.set_at(index, element)

    def append(self, element: Any) -> None:
        """
        Add an element to the back of the array.
        Time complexity for full marks: O(1*) (* means amortized)
        """
        if self.size == self.capacity:
            self.__resize()
        if not self.is_reversed:
            if self.starting + self.size >= self.capacity:
                self.__resize()
            self.array[self.starting + self.size] = element
        else:
            if self.starting - 1 < 0:
                self.__resize()
            self.array[self.starting - 1] = element
            self.starting -= 1
        self.size += 1

    def prepend(self, element: Any) -> None:
        """
        Add an element to the front of the array.
        Time complexity for full marks: O(1*)
        """
        if self.size == self.capacity:
            self.__resize()
        if not self.is_reversed:
            if self.starting - 1 < 0:
                self.__resize()
            self.array[self.starting - 1] = element
            self.starting -= 1
        else:
            if self.starting + self.size >= self.capacity:
                self.__resize()
            self.array[self.starting + self.size] = element
        self.size += 1

    def reverse(self) -> None:
        """
        Reverse the array.
        Time complexity for full marks: O(1)
        """
        self.is_reversed = not self.is_reversed

    def remove(self, element: Any) -> None:
        """
        Remove the first occurrence of the element from the array.
        If there is no such element, leave the array unchanged.
        Time complexity for full marks: O(N)
        """
        if not self.is_reversed:
            for i in range(self.starting, self.starting + self.size):
                if self.array[i] == element:
                    for j in range(i, self.starting + self.size - 1):
                        self.array[j] = self.array[j + 1]
                    self.array[self.starting + self.size - 1] = None
                    self.size -= 1
                    return
        else:
            for i in range(self.starting + self.size - 1, self.starting - 1, -1):
                if self.array[i] == element:
                    for j in range(i, self.starting, -1):
                        self.array[j] = self.array[j - 1]
                    self.array[self.starting] = None
                    self.size -= 1
                    self.starting += 1
                    return

    def remove_at(self, index: int) -> Any | None:
        """
        Remove the element at the given index from the array and return the removed element.
        If there is no such element, leave the array unchanged and return None.
        Time complexity for full marks: O(N)
        """
        if self.is_reversed:
            index = (self.size - 1) - index
        index += self.starting
        result = None
        if self.starting <= index < self.starting + self.size:
            result = self.array[index]
            for j in range(index, self.starting + self.size - 1):
                self.array[j] = self.array[j + 1]
            self.array[self.starting + self.size - 1] = None
            self.size -= 1
        return result

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return self.size == 0

    def is_full(self) -> bool:
        """
        Boolean helper to tell us if the structure is full or not
        Time complexity for full marks: O(1)
        """
        return self.size == self.capacity

    def get_size(self) -> int:
        """
        Return the number of elements in the list
        Time complexity for full marks: O(1)
        """
        return self.size

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of slots) of the list
        Time complexity for full marks: O(1)
        """
        return self.capacity

    def sort(self) -> None:
        """
        Sort elements inside _data based on < comparisons.
        Time complexity for full marks: O(NlogN)
        """
        self.merge_sort(self.array, self.starting, self.starting + self.size - 1)

    def merge_sort(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2

            self.merge_sort(arr, left, mid)
            self.merge_sort(arr, mid + 1, right)
            self.merge(arr, left, mid, right)

    def merge(self, arr, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        # Create temp arrays
        L = [0] * n1
        R = [0] * n2

        # Copy data to temp arrays L[] and R[]
        for i in range(n1):
            L[i] = arr[left + i]
        for j in range(n2):
            R[j] = arr[mid + 1 + j]

        i = 0  # Initial index of first subarray
        j = 0  # Initial index of second subarray
        k = left  # Initial index of merged subarray

        # Merge the temp arrays back
        # into arr[left..right]
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Copy the remaining elements of L[],
        # if there are any
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        # Copy the remaining elements of R[],
        # if there are any
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    def binarySearch(self, x):
        low = self.starting
        high = self.starting + self.size - 1
        while low <= high:
            mid = low + (high - low) // 2
            if self.array[mid] == x:
                return mid
            elif self.array[mid] < x:
                low = mid + 1
            else:
                high = mid - 1
        return -1

# new_list = DynamicArray()
# new_list.append(3)
# new_list.append(4)
# new_list.append(5)
# new_list.append(6)
# new_list.prepend(9)
# new_list.prepend(8)
# new_list.prepend(2)
# new_list.prepend(5)
# # new_list.prepend(-34)
# # new_list.prepend(-3)
# new_list.reverse()
# print(new_list)
# print(new_list.remove_at(10))
# print(new_list)
# # new_list.remove(5)
# # print(new_list).
