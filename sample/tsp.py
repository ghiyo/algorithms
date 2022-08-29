"""
filename: tsp.py
"""

# TODO: Cheated a little bit on this one, will need to do it again
# and optimize it a lot more
# takes about 11GB of ram to finish...

from itertools import combinations
import os
import numpy as np


def read_file(filename):
    """Reads and returns the contents of a file in a list of strings"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath(f"../input/{filename}", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [i.strip() for i in f.readlines()]
    f.close()
    return lines


def distance(a, b):
    """Finds and returns the distance between two euclidean points"""
    return np.sqrt((b[0] - a[0])**2 + (b[1]-a[1])**2)


def generate_adj_matrix(data, n):
    """Generates an adjacency matrix given a list of euclidean points"""
    dist = [(float(j[0]), float(j[1])) for j in [i.split() for i in data]]
    G = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                G[i][j] = 0
            else:
                G[i][j] = distance(dist[i], dist[j])
    return G


def TSP(G, n):
    """Calculates the traveling salesman problem"""
    C = [[np.inf for _ in range(n)] for __ in range(1 << n)]
    C[1][0] = 0
    for size in range(1, n):
        percentage_completed = abs(size+1) / (n) * 100
        print(
            f'\r>> ({size+1},{n}) (% {percentage_completed:.2f})', end="", flush=True)
        for S in combinations(range(1, n), size):
            S = (0,) + S
            k = sum([1 << i for i in S])
            for i in S:
                if i == 0:
                    continue
                for j in S:
                    if j == i:
                        continue
                    cur_index = k ^ (1 << i)
                    C[k][i] = min(C[k][i], C[cur_index][j] + G[j][i])
    all_index = (1 << n) - 1
    return min([(C[all_index][i] + G[0][i], i) for i in range(n)])


def main():
    """Main function"""
    raw_data = read_file("tsp.txt")
    n = int(raw_data[0])
    G = generate_adj_matrix(raw_data[1:], n)
    # test = [[0, 1, 2, 2], [1, 0, 1, 1], [2, 1, 0, 2], [2, 1, 2, 0]]
    # n = len(test)
    l = TSP(G, n)
    print(l)


if __name__ == "__main__":
    main()
