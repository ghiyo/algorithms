"""
filename: heap.py
"""


from copy import deepcopy


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
            return self.items[p] < self.items[c]
        return self.items[p] > self.items[c]

    def _bubble_down_aux(self, p, l, r, t):
        if l >= len(self.items) and r >= len(self.items):
            return
        if r >= len(self.items):
            self._swap(p, l)
            return
        # if self.items[l] < self.items[r] and self.items[p] > self.items[l]:
        if self._heap_condition(r, l, t) and self._heap_condition(p, l, t):
            self._swap(p, l)
            self._bubble_down_aux(l, l*2-1, l*2, t)
        # elif self.items[p] > self.items[r]:
        elif self._heap_condition(p, r, t):
            self._swap(p, r)
            self._bubble_down_aux(r, r*2-1, r*2, t)

    def _bubble_down(self, t, index=1):
        """Restores the heap property by moving keys down"""
        if len(self.items) > 1:
            p = index - 1
            l = 2 * index - 1
            r = 2 * index
            if len(self.items) >= 3:
                self._bubble_down_aux(p, l, r, t)
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
        return deepcopy(self.items[0])

    def print_heap(self):
        """Displays the heap"""
        for i in self.items:
            print(f'{i} ', end="")
        print()


def main():
    """main function"""
    test = [4, 4, 8, 9, 4, 9, 12, 11, 13]
    heap = Heap("min")
    for i in test:
        heap.insert(i)
    heap.print_heap()
    while heap.is_empty() is False:
        print(f'{heap.extract()}')


if __name__ == "__main__":
    main()
