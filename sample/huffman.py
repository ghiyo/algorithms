
"""
filename: huffman.py
"""


import heapq
import os


class HuffNode:
    """Huffman node for data compression"""

    def __init__(self, label, weight):
        self.label = label
        self.weight = weight
        self.left = None
        self.right = None

    def __str__(self):
        return f'label: {self.label} weight: {self.weight}'

    def __lt__(self, rhs):
        return self.weight < rhs.weight

    def __le__(self, rhs):
        return self.weight <= rhs.weight

    def __gt__(self, rhs):
        return self.weight > rhs.weight

    def __ge__(self, rhs):
        return self.weight >= rhs.weight

    def __eq__(self, rhs):
        return self.weight == rhs.weight

    def __ne__(self, rhs):
        return self.weight != rhs.weight

    def get_labels(self):
        """returns the list of labels in this sub-tree"""
        return self.label.split(',')


def huffcode_tree(arr, n):
    """finds the longest and shortest bit length for any 
    alphabet in the huffman tree"""
    huffcodes = []
    for i in arr:
        huffcodes.append(HuffNode(i[1], i[0]))
    heapq.heapify(huffcodes)

    while len(huffcodes) > 1:
        a = heapq.heappop(huffcodes)
        b = heapq.heappop(huffcodes)
        c = HuffNode(a.label+'-'+b.label, a.weight + b.weight)
        c.left = a
        c.right = b
        heapq.heappush(huffcodes, c)
    return heapq.heappop(huffcodes)


def max_depth(node):
    """Counts the number of nodes to get to the deepest leaf in the tree"""
    if node is None:
        depth = 0
    elif node.left is None and node.right is None:
        depth = 1
    else:
        depth = max(max_depth(node.left), max_depth(node.right)) + 1
    return depth


def min_depth(node):
    """Counts the number of nodes to get to the shallowest leaf in the tree"""
    if node is None:
        depth = 0
    elif node.left is None and node.right is None:
        depth = 1
    else:
        depth = min(min_depth(node.left), min_depth(node.right)) + 1
    return depth


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/huffman.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [i.strip() for i in f.readlines()]
    # test = ["10", "37", "59", "43", "27", "30", "96", "96", "71", "8", "76"]
    # test2 = ["15", "895", "121", "188", "953", "378", "849", "153",
    #          "579", "144", "727", "589", "301", "442", "327", "930"]
    # lines = test2
    length = int(lines[0])
    alphabet = []
    for i in range(1, len(lines)):
        alphabet.append((int(lines[i]), str(i)))
    f.close()
    root = huffcode_tree(alphabet, length)
    max_bit_len = max_depth(root) - 1
    min_bit_len = min_depth(root) - 1
    print(f'max bit length: {max_bit_len}\nmin bit length: {min_bit_len}')


if __name__ == "__main__":
    main()
