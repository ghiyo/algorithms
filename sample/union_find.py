"""
filename: union_find.py
"""

from copy import deepcopy


class UnionFind:
    """A union data structure node"""

    def __init__(self):
        self.parent_node = {}
        self.rank = {}
        self.group_set = set()

    def display(self):
        """Prints the contents of the UnionFind set"""
        for i, v in self.parent_node.items():
            print(f'node: {i:>2} parent: {v:>2} rank: {self.rank[i]:>2}')

    def make_set_list(self, l):
        """Given a list of labels will make a set of objects with the labels"""
        self.parent_node.clear()
        self.rank.clear()
        for i in l:
            self.parent_node[i] = i
            self.rank[i] = 0
        self._recompute_groups()

    def make_set(self, start, end):
        """Makes a set of objects that point to themselves as parents"""
        self.parent_node.clear()
        self.rank.clear()
        for i in range(start, end):
            self.parent_node[i] = i
            self.rank[i] = 0
        self._recompute_groups()

    def _recompute_groups(self):
        self.group_set.clear()
        for v in self.parent_node.values():
            self.group_set.add(self.find(v))

    def groups(self):
        """Returns the list of group labels"""
        return deepcopy(self.group_set)

    def group_size(self):
        """Returns the number of distinct clusters"""
        return len(self.group_set)

    def find(self, x):
        """Finds which parent x belongs to"""
        if self.parent_node[x] != x:
            self.parent_node[x] = self.find(self.parent_node[x])
        return self.parent_node[x]

    def union(self, a, b):
        """Joins two nodes into one group"""
        x = self.find(a)
        y = self.find(b)
        if x == y:
            return
        if self.rank[x] < self.rank[y]:
            self.parent_node[x] = y
        elif self.rank[x] > self.rank[y]:
            self.parent_node[y] = x
        else:
            self.parent_node[y] = x
            self.rank[x] = self.rank[x] + 1
        # print(f'>>> {x} {y} {a} {b} <<<')
        self._recompute_groups()

    def __len__(self):
        return len(self.parent_node)

    def __getitem__(self, name):
        return self.parent_node[name]

    def __iter__(self):
        return iter(self.parent_node)

    def keys(self):
        "Returns the list of keys for parent node set"
        return self.parent_node.keys()

    def items(self):
        "Returns the list of items for parent node set"
        return self.parent_node.items()

    def values(self):
        "Returns the list of values for parent node set"
        return self.parent_node.values()
