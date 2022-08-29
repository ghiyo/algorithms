"""
filename: apsp.py
"""

from collections import defaultdict
from multiprocessing import Pool
import multiprocessing
import os


def read_file(filename):
    """Reads and returns the contents of a file in a list of strings"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath(f"../input/{filename}", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [i.strip() for i in f.readlines()]
    f.close()
    return lines


def preprocess_adj_list(raw_data):
    """Reads a adjacency list and converts and splits for use"""
    adj_list = [i.split() for i in raw_data]
    for i, value in enumerate(adj_list):
        for j, k in enumerate(value):
            adj_list[i][j] = int(k)
    return adj_list


def infinite_default():
    """Infinite default for defaultdict"""
    return float('inf')


def create_adj_set(adj_list, n):
    """Creates a set using the i,j tuple as key"""
    adj_set = defaultdict(infinite_default)
    for count, e in enumerate(adj_list):
        percentage_completed = abs(count+1) / (len(adj_list)) * 100
        print(
            f'\r>> ({count+1}/{len(adj_list)}) (% {percentage_completed:.2f})', end="", flush=True)
        key = (e[0], e[1])
        length = e[2]
        adj_set[key] = length
    print()
    return adj_set


def floyd_warshall_algo(adj_set, n, m):
    """FW All Shortest Path implementation"""

    A = [[float('inf') for _ in range(n)]
         for _ in range(n)]
    ncycle = False  # Negative Cycle

    # Base Case
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i][j] = 0
            elif adj_set[(i+1, j+1)] is not float('inf'):
                A[i][j] = adj_set[(i+1, j+1)]

    # Recurrence
    for k in range(1, n):
        if multiprocessing.current_process().name == "ForkPoolWorker-1":
            percentage_completed = abs(k+1) / (n) * 100
            print(
                f'\r>> ({k+1}/{n}) (% {percentage_completed:.2f})', end="", flush=True)
        for i in range(n):
            for j in range(n):
                A[i][j] = min(A[i][j], A[i][k] + A[k][j])
    if multiprocessing.current_process().name == "ForkPoolWorker-1":
        print()
    for i in range(n):
        if A[i][i] < 0:
            ncycle = True
            break

    apsp = defaultdict(infinite_default)  # All Paths Shortest Paths
    for i in range(n):
        for j in range(n):
            apsp[(i+1, j+1)] = A[i][j]

    shortest_path = find_shortest_path(apsp)

    return shortest_path, ncycle


def find_shortest_path(apsp):
    """Finds the shortest path in the all shortest path list"""
    shortest_key = next(iter(apsp))
    for k, v in apsp.items():
        if k[0] != k[1] and v < apsp[shortest_key]:
            shortest_key = k
    return {shortest_key: apsp[shortest_key]}


def prepare_load(raw_data):
    """given a raw input, gets the approapriate data for the algo"""
    input_size = raw_data[0].split()
    num_nodes = int(input_size[0])
    num_edges = int(input_size[1])
    adj_list = preprocess_adj_list(raw_data[1:])
    adj_set = create_adj_set(adj_list, num_nodes)
    return adj_set, num_nodes, num_edges


def main():
    """main method"""

    # g_1 g_2 and g_3
    apsp_1_raw = read_file('apsp_g1.txt')
    apsp_2_raw = read_file('apsp_g2.txt')
    apsp_3_raw = read_file('apsp_g3.txt')
    set_1 = prepare_load(apsp_1_raw)
    set_2 = prepare_load(apsp_2_raw)
    set_3 = prepare_load(apsp_3_raw)

    with Pool(processes=3) as p:
        results = p.starmap(floyd_warshall_algo, [set_1, set_2, set_3])
    for i, v in enumerate(results):
        if v[1] is True:
            print(f'contains negative cycle: {i+1}')
        else:
            print(f'shortest path for {i+1}: {v[0]}')

    # large too big, runs our of memory even with n^2 space complexity
    # apsp_large_raw = read_file('apsp_large.txt')
    # apsp_large = prepare_load(apsp_large_raw)
    # results = floyd_warshall_algo(apsp_large[0], apsp_large[1], apsp_large[2])
    # if results[1] is True:
    #     print(f'contains negative cycle: {results[1]}')
    # else:
    #     print(f'shortest path: {results[0]}')


if __name__ == "__main__":
    main()
