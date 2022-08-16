
"""
filename: knapsack.py
"""

import os


def reconstruct_sol(sol, items, w, n):
    """Reconstructs the list of items that are part of the optimized solution"""
    max_value = sol[n][w]
    opt_sol = []
    i = n
    j = w
    while i > 0 and j > 0:
        index = j - items[i-1][1]
        if index >= 0:
            if sol[i-1][j] < sol[i-1][index] + items[i-1][0]:
                opt_sol.append(items[i-1])
                j = index
                i -= 1
            else:
                j -= 1
                i -= 1
        else:
            i -= 1
    return max_value, opt_sol


def optimal_knapsack(items, w, n):
    """Calculates the maximum value that can be collected from items"""
    sol = [[0 for _ in range(w+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(w+1):
            index = j - items[i-1][1]
            sol[i][j] = max(sol[i-1][j], sol[i-1][index] +
                            items[i-1][0] if index >= 0 else sol[i-1][0])
    return sol


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/knapsack_big.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [[int(j[0]), int(j[1])]
             for j in [i.strip().split() for i in f.readlines()]]
    f.close()

    # test = [[6, 4], [3, 4], [2, 3], [4, 2], [4, 3]]
    # lines = test

    bag_size = lines[0][0]
    items_size = lines[0][1]
    items = lines[1:]

    sol = optimal_knapsack(items, bag_size, items_size)
    max_value, knapsack = reconstruct_sol(sol, items, bag_size, items_size)
    print(f'{knapsack}\n{max_value}')


if __name__ == "__main__":
    main()
