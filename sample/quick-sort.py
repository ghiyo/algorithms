"""
filename: quick-sort.py
"""


import math
import os


class QuickSort:
    """Quick Sort Implementations with first, last, and middle element being pivots"""

    def __init__(self):
        self.q1_swap_count = 0
        self.q2_swap_count = 0
        self.q3_swap_count = 0

    def Swap(self, arr, i, j):
        """swaps two elements of an array"""
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp

    def Partition(self, arr, l, r):
        """Partition an array around a pivot."""
        pivot = arr[l]
        j = i = l + 1
        while j < r:
            if arr[j] < pivot:
                self.Swap(arr, i, j)
                i += 1
            j += 1
        pivot_index = i-1
        self.Swap(arr, l, pivot_index)
        return pivot_index

    def _QuickSort_aux_1(self, arr, l, r):
        """Quick Sort implementation with first elements always being the pivot"""
        if r - l <= 1:
            return
        else:
            self.q1_swap_count += r-l-1
            pivot_index = self.Partition(arr, l, r)
            self._QuickSort_aux_1(arr, l, pivot_index)
            self._QuickSort_aux_1(arr, pivot_index+1, r)

    def _QuickSort_aux_2(self, arr, l, r):
        """Quick Sort implementation with last elements always being the pivot"""
        if r - l <= 1:
            return
        else:
            self.q2_swap_count += r-l-1
            self.Swap(arr, l, r-1)  # have last element be the pivot
            pivot_index = self.Partition(arr, l, r)
            self._QuickSort_aux_2(arr, l, pivot_index)
            self._QuickSort_aux_2(arr, pivot_index+1, r)

    def _QuickSort_aux_3(self, arr, l, r):
        """Quick Sort implementation with median of first, last, and middle elements always being the pivot"""
        if r - l <= 1:
            return 0
        else:
            m = math.ceil((r-l)/2) - 1 + l
            if arr[l] < arr[m] < arr[r-1] or arr[l] > arr[m] > arr[r-1]:
                pivot = m
            elif arr[m] < arr[l] < arr[r-1] or arr[m] > arr[l] > arr[r-1]:
                pivot = l
            else:
                pivot = r-1
            self.Swap(arr, l, pivot)
            pivot_index = self.Partition(arr, l, r)
            left = self._QuickSort_aux_3(arr, l, pivot_index)
            right = self._QuickSort_aux_3(arr, pivot_index+1, r)
            return r - l - 1 + left + right

    def QuickSort_1(self, arr):
        """Quick Sort implementation with first elements always being the pivot"""
        self._QuickSort_aux_1(arr, 0, len(arr))

    def QuickSort_2(self, arr):
        """Quick Sort implementation with first elements always being the pivot"""
        self._QuickSort_aux_2(arr, 0, len(arr))

    def QuickSort_3(self, arr):
        """Quick Sort implementation with first elements always being the pivot"""
        return self._QuickSort_aux_3(arr, 0, len(arr))


def main():
    """main function"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/QuickSort.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    nums = f.read().strip().split("\n")
    f.close()
    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    for i in range(len(nums)):
        arr1.append(int(nums[i]))
        arr2.append(int(nums[i]))
        arr3.append(int(nums[i]))
        arr4.append(int(nums[i]))
    qs = QuickSort()
    qs.QuickSort_1(arr1)
    qs.QuickSort_2(arr2)
    q3_swap_count = qs.QuickSort_3(arr3)
    print(f'Quick Sort with first element being Pivot {qs.q1_swap_count}')
    print(f'Quick Sort with first element being Pivot {qs.q2_swap_count}')
    print(f'Quick Sort with first element being Pivot {q3_swap_count}')


if __name__ == "__main__":
    main()
