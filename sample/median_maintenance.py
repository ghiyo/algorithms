"""
filename: median_maintenance.py
"""

import os
from heap import Heap


def heap_rebalance(min_heap, max_heap):
    """if one heap is smaller by more than 1 element rebalance"""
    difference = abs(len(min_heap) - len(max_heap))
    # print(difference)
    if difference > 1:
        if len(min_heap) > len(max_heap):
            v = min_heap.extract()
            max_heap.insert(v)
            # print('<<< 1 >>>')
        else:
            v = max_heap.extract()
            min_heap.insert(v)
            # print('<<< 2 >>>')
    elif difference == 1 and len(min_heap) < len(max_heap):
        # print('<<< 3 >>>')
        v = max_heap.extract()
        min_heap.insert(v)


def medians_total(arr):
    """Finds the medians and adds them all up and finds the mod 10000"""
    max_heap = Heap("min")
    min_heap = Heap("max")
    median_total = []
    for i in arr:
        if min_heap.is_empty():
            min_heap.insert(i)
        else:
            median_total.append(min_heap.peek())
            if i <= min_heap.peek():
                min_heap.insert(i)
            if i > min_heap.peek():
                max_heap.insert(i)
            if min_heap.peek() < i < max_heap.peek():
                min_heap.insert(i)
        heap_rebalance(min_heap, max_heap)
    median_total.append(min_heap.peek())
    print(median_total)
    print(len(median_total))
    return median_total


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/Median-Maintenance.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    line = f.read()
    num_input = [int(i) for i in line.split()]
    f.close()
    print(sum(medians_total(num_input)) % 10000)


if __name__ == "__main__":
    main()
