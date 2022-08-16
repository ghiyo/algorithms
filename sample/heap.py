"""
filename: heap.py
"""


from copy import deepcopy
import heapq
import os


class Heap:
    """Implementation of a Min-Heap data structure"""

    def __init__(self, t="min"):
        self.items = []
        self.type = t

    def __len__(self):
        return len(self.items)

    def _swap(self, i, j):
        """Swaps two elements in the heap using their indices"""
        temp = deepcopy(self.items[i])
        self.items[i] = self.items[j]
        self.items[j] = temp

    def _left_child(self, pos):
        return pos*2-1

    def _right_child(self, pos):
        return pos*2

    def _has_left_child(self, pos):
        return self._left_child(pos) < len(self.items)

    def _has_right_child(self, pos):
        return self._right_child(pos) < len(self.items)

    def _heap_condition(self, p, c, t):
        """returns true if p < c for min heap and p > c for max heap"""
        if t == "max":
            return self.items[p] <= self.items[c]
        return self.items[p] >= self.items[c]

    def _bubble_down_aux(self, p, l, r, t):
        # print(f'{p} -> l: {l} r: {r}')
        if l > len(self.items) and r > len(self.items):
            return
        if r > len(self.items):
            if self._heap_condition(p-1, l-1, t):
                self._swap(p-1, l-1)
            return
        # if self.items[l] < self.items[r] and self.items[p] > self.items[l]:
        if self._heap_condition(r-1, l-1, t) and self._heap_condition(p-1, l-1, t):
            self._swap(p-1, l-1)
            self._bubble_down_aux(l, l*2, l*2+1, t)
        # elif self.items[p] > self.items[r]:
        elif self._heap_condition(p-1, r-1, t):
            self._swap(p-1, r-1)
            self._bubble_down_aux(r, r*2, r*2+1, t)

    def _bubble_down(self, t, index=1):
        """Restores the heap property by moving keys down"""
        if len(self.items) > 1:
            p = index - 1
            l = 2 * index - 1
            r = 2 * index
            if len(self.items) >= 3:
                self._bubble_down_aux(p+1, l+1, r+1, t)
            # elif self.items[l] < self.items[p]:
            elif self._heap_condition(p, l, t):
                self._swap(p, l)

    def _bubble_up(self, index, t):
        """Restores the heap property by moving keys up"""
        if index > 1:
            current_index = index - 1
            if index % 2 == 0:
                parent_index = int(index / 2) - 1
            else:
                parent_index = int(index // 2) - 1
            # if self.items[parent_index] > self.items[current_index]:
            if self._heap_condition(parent_index, current_index, t):
                self._swap(parent_index, current_index)
                self._bubble_up(parent_index + 1, t)

    def is_empty(self):
        """returns true is heap is empty otherwise false"""
        return not self.items

    def insert(self, k):
        """Inserts a value into the heap"""
        self.items.append(k)
        self._bubble_up(len(self.items), self.type)

    def extract(self):
        """Removes the priority key from the heap and returns it"""
        key = None
        if len(self.items) > 0:
            temp = self.items[0]
            self.items[0] = self.items[len(self.items)-1]
            self.items[len(self.items)-1] = temp
            key = self.items.pop()
            self._bubble_down(self.type)
        return key

    def peek(self):
        """Returns a copy of the value at the top of the heap"""
        if self.is_empty():
            return None
        return deepcopy(self.items[0])

    def print_heap(self):
        """Displays the heap"""
        for i in self.items:
            print(f'{i} ', end="")
        print()


def main():
    """main function"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/Median-Maintenance.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    line = f.read()
    num_input = [int(i) for i in line.split()]
    test = [4, 4, 4, 6]
    hh = []
    lh = []
    heapq.heapify(hh)
    heapq.heapify(lh)
    heap = Heap("min")
    m = Heap("max")
    equal = True
    for i in num_input:
        m.insert(i)
        heap.insert(i)
        heapq.heappush(lh, i)
        heapq.heappush(hh, i*-1)
        equal = len(m) == len(heap) == len(hh) == len(lh)
    while heap.is_empty() is False and equal:
        min = heapq.heappop(lh)
        max = heapq.heappop(hh) * -1
        equal = heap.extract() == min and m.extract() == max and len(
            m) == len(heap) == len(hh) == len(lh)
    print(equal)


if __name__ == "__main__":
    main()
