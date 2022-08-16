"""
filename: max_space_k_clustering.py
"""

import heapq
import os
from union_find import UnionFind


def max_k_spacing_clusters(adj_list, V, total_clusters):
    """Will compute and return the max k spacing of 4 clusters"""
    hp = [(i[2], [i[0], i[1]]) for i in adj_list]
    heapq.heapify(hp)
    uf_set = UnionFind()
    uf_set.make_set(1, V+1)
    k = 0
    while uf_set.group_size() > total_clusters and len(hp) > 0:
        edge = heapq.heappop(hp)
        p = edge[1][0]
        q = edge[1][1]
        x = uf_set.find(p)
        y = uf_set.find(q)
        if x != y:
            uf_set.union(p, q)
    if len(hp) > 0:
        edge = heapq.heappop(hp)
        p = edge[1][0]
        q = edge[1][1]
        while uf_set.find(p) == uf_set.find(q) and len(hp) > 0:
            edge = heapq.heappop(hp)
            p = edge[1][0]
            q = edge[1][1]
        if uf_set.find(p) != uf_set.find(q):
            k = edge[0]
    return k


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/clustering.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [i.split() for i in f.readlines()]
    node_num = int(lines[0][0])
    num_input = [[int(i[0]), int(i[1]), int(i[2])] for i in lines[1:]]
    f.close()
    k = max_k_spacing_clusters(num_input, node_num, 4)
    print(f'max 4 cluster spacing: {k}')


if __name__ == "__main__":
    main()
