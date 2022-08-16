"""
filename: counting_inversions.py
"""


import os


def sort_and_count_inversions(arr):
    """merge sort without using new memory"""
    si_num = 0
    if len(arr) <= 1:
        return si_num
    else:
        n = len(arr) // 2
        lhs = arr[:n]
        rhs = arr[n:]
        si_num += sort_and_count_inversions(lhs)
        si_num += sort_and_count_inversions(rhs)

        i = j = k = 0
        while i < len(lhs) and j < len(rhs):
            if lhs[i] < rhs[j]:
                arr[k] = lhs[i]
                i += 1
            else:
                arr[k] = rhs[j]
                si_num += len(lhs[i:])
                j += 1
            k += 1

        while i < len(lhs):
            arr[k] = lhs[i]
            i += 1
            k += 1

        while j < len(rhs):
            arr[k] = rhs[j]
            j += 1
            k += 1
        return si_num


def main():
    """main function"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/IntegerArray.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    nums = f.read().strip().split("\n")
    f.close()
    arr = []
    for i in range(len(nums)):
        arr.append(int(nums[i]))
    inversions = sort_and_count_inversions(arr)
    p_sort = sorted(arr)
    print(p_sort == arr)
    print(inversions)


if __name__ == "__main__":
    main()
