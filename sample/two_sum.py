"""
filename: two_sum.py
"""

from multiprocessing import Pool, cpu_count
import multiprocessing
import os


def has_target(t, arr):
    """Checks to see if a target value is a 2 sum target"""
    for i in arr:
        y = t - i
        if y in arr and y != i:
            return True
    return False


def two_sum(arr, start, end):
    """returns 2 sum count for a range -10000..10000"""
    count = 0
    j = 0
    for i in range(start, end):
        if multiprocessing.current_process().name == "ForkPoolWorker-1":
            percentage_completed = abs(j) / (end-start) * 100
            print(f'\r>> {i} ({start},{end}) (% {percentage_completed:.2f})',
                  end="", flush=True)
        if has_target(i, arr):
            count += 1
        j += 1
    return count


def calc_range(start, end):
    """Calculates the range for each processor given start is negative ans end is positive"""
    n = cpu_count()
    cpu_range = end - start + 1
    chunk = cpu_range // cpu_count()
    remainder = cpu_range % cpu_count()
    ranges = []
    for i in range(n):
        s = i * chunk
        e = (i + 1) * chunk
        ranges.append([s-end, e-end])
    if remainder > 0:
        ranges[len(ranges)-1][1] += remainder
    return ranges


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/2sum.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    line = f.read()
    numbers = set([int(i) for i in line.split()])
    start = -10000
    end = 10000
    with Pool(processes=cpu_count()) as p:
        p_range = calc_range(start, end)
        print(p_range)
        results = p.starmap(two_sum, [(numbers, p_range[i][0], p_range[i][1])
                                      for i in range(cpu_count())])
        p.close()
        p.join()
    total = sum(results)
    print(f'results: {results}\ntotal: {total}')


if __name__ == "__main__":
    main()
