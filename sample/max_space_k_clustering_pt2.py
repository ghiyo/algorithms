"""
filename: max_space_k_clustering_pt2.py
"""

import os

from networkx.utils import UnionFind


def xor_op(x, y, bit_size):
    """Does the xor operation between two lists of 1s and 0s"""
    mask = [0] * bit_size
    for i in range(bit_size):
        if x[i] != y[i]:
            mask[i] = 1
    return mask


def three_diff_bit_set(bit_size):
    """Returns a set of 24 bit masks that differ by at most 2 bits
    i.e. 000...0 for no difference. 00...001 1 bit in any position for 1
    bit difference and 000...0011 2 bit in any combination for 2 bit difference."""
    one_mask = []
    for i in range(bit_size):
        mask = [0]*bit_size
        for j in range(bit_size):
            if i == j:
                mask[j] = 1
        one_mask.append(mask)
    two_mask = []
    for i in range(bit_size):
        for j in range(i+1, bit_size):
            curr = one_mask[i]
            mask = one_mask[j]
            two_mask.append(xor_op(curr, mask, bit_size))
    masks_list = one_mask+two_mask
    mask_set = set()
    for i in masks_list:
        mask_set.add(int("".join([str(j) for j in i]), 2))
    return mask_set


def max_k_spacing_clusters_big(node_set, V, mask_set):
    """Computes the k-cluster with Hamming distance of 24 bit numbers"""
    uf_set = UnionFind(list(node_set))
    count = 1
    for vertex in node_set:
        percentage_completed = count / len(node_set) * 100
        print(f'\r>> {count} / {len(node_set)} (% {percentage_completed:.2f})',
              end="", flush=True)
        for mask in mask_set:
            p = vertex
            q = p ^ mask
            if q in node_set:
                uf_set.union(p, q)
        count += 1
    print()
    groups = []
    for i in uf_set.to_sets():
        groups.append(i)
    print(len(groups))
    return len(groups)


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/clustering_big.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [f.readline().split()] + ["".join(i.split())
                                      for i in f.readlines()]
    node_num = int(lines[0][0])
    bit_size = int(lines[0][1])
    num_input = set()
    for i in lines[1:]:
        num_input.add(int(i, 2))
    f.close()
    mask_set = three_diff_bit_set(bit_size)
    k = max_k_spacing_clusters_big(num_input, node_num, mask_set)
    print(f'number of k-clustering with spacing atleast 3: {k}')


if __name__ == "__main__":
    main()
