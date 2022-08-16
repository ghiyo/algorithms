
"""
filename: mwis.py
"""

import os


def max_weight_indep_set(arr, n):
    """Returns an array with optimal solutions for independent
    max weight set for each vertex in path"""
    mw = [0]
    if n > 0:
        mw.append(arr[0])
        for i in range(1, n):
            opt = max(mw[i], mw[i-1] + arr[i])
            mw.append(opt)
    return mw


def reconstruct_mwis(mwis, arr, n):
    """Given an optimal array, reconstruct the solution with the
    original vertices"""
    indices = []
    if len(arr) > 0 and len(mwis) > 1:
        i = n
        while i >= 1:
            prev = mwis[i-1]
            prev_prev = mwis[i-2]
            if i - 2 < 0:
                prev_prev = 0
            if prev >= prev_prev + arr[i-1]:
                i -= 1
            else:
                indices.append(i)
                i -= 2
    return indices[::-1]


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/mwis.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [int(i) for i in f.readlines()]
    # test = [4, 1, 4, 5, 4]
    # test2 = [4, 4, 1, 5, 4]
    # test3 = [7, 2, 4, 5, 1, 4, 6, 2, 1]
    # lines = test3
    f.close()
    match_set = [1, 2, 3, 4, 17, 117, 517, 997]
    n = lines[0]
    arr = lines[1:]
    mwis = max_weight_indep_set(arr, n)
    mwis_sol = reconstruct_mwis(mwis, arr, n)
    bit_check = ""
    for i in match_set:
        if i in mwis_sol:
            bit_check += "1"
        else:
            bit_check += "0"
    print(f'bits included: {bit_check}')


if __name__ == "__main__":
    main()
