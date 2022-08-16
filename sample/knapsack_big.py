
"""
filename: knapsack_big.py
"""

import os


def optimal_knapsack_big(items, w, n):
    """Calculates the maximum value that can be collected from items
    this version uses an array for previous solutions, reconstruction
    is either impossible or very hard because of loss of data. For 
    reconstruction its better to use two arrays instead of one."""
    dp = [0 for _ in range(w+1)]
    for i in range(1, n+1):
        percentage_completed = i / (n) * 100
        print(f'\r>> {i}/{n} (% {percentage_completed:.2f})',
              end="", flush=True)
        wi = items[i-1][1]
        vi = items[i-1][0]
        for j in range(w, 0, -1):
            if j >= wi:
                dp[j] = max(dp[j], dp[j - wi] + vi)
            else:
                break
    print()
    return dp[w]


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

    max_value = optimal_knapsack_big(items, bag_size, items_size)
    print(f'{max_value}')


if __name__ == "__main__":
    main()
