import math
import os


def merge(a, b, key):
    """merges two arrays together in ascending order"""
    c = []
    n = len(a) + len(b)
    i = j = 0
    while i < len(a) and j < len(b):
        if key == "x":
            lhs = a[i].x
            rhs = b[j].x
        else:
            lhs = a[i].y
            rhs = b[j].y
        if lhs < rhs:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    while i < len(a):
        c.append(a[i])
        i += 1
    while j < len(b):
        c.append(b[j])
        j += 1
    return c


def merge_sort(arr, key):
    """merge sort without auxiliary"""
    if len(arr) <= 1:
        return arr
    else:
        n = len(arr) // 2
        return merge(merge_sort(arr[:n], key), merge_sort(arr[n:], key), key)


class Point:
    """cartesian point on a 2D plane"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, rhs):
        """finds the distance between two points"""
        return math.sqrt((rhs.x - self.x)**2 + (rhs.y - self.y)**2)

    def __str__(self):
        return f"({self.x}, {self.y})"


def _closestSplitPair(px, py, delta):
    n = len(px) // 2
    x_mean = px[n]
    sy = []
    for p in py:
        if p.x > x_mean.x - delta and p.x < x_mean.x + delta:
            sy.append(p)
    best = delta
    best_p = None
    best_q = None
    for i in range(len(sy)):
        p = sy[i]
        for j in range(i+1, min(len(sy), 7)):
            q = sy[j]
            if p.distance(q) < best:
                best_p = p
                best_q = q
    return best_p, best_q


def _closestPair_aux(px, py):
    """auxiliary function for closest pair that takes a half of 2 sorted arrays or points"""
    if len(px) == 1 and len(py) == 1:
        return px[0], py[0]
    else:
        n = len(px) // 2
        p1, q1 = _closestPair_aux(px[:n], py[:n])
        p2, q2 = _closestPair_aux(px[n:], py[n:])
        d1 = p1.distance(q1)
        d2 = p2.distance(q2)
        delta = min(d1, d2)
        p3, q3 = _closestSplitPair(px, py, delta)
        if p3 is not None and q3 is not None:
            d3 = p3.distance(q3)
        else:
            d3 = math.inf
        if d1 <= d2 and d1 <= d3:
            return p1, q1
        elif d2 <= d1 and d2 <= d3:
            return p2, q2
        else:
            return p3, q3


def closestPair(points):
    """Finds the closest pair of points given an array of points using divide and conquer"""
    px = merge_sort(points, "x")
    py = merge_sort(points, "y")
    p, q = _closestPair_aux(px, py)
    return p, q


def closestPairBrute(points):
    """Finds the closest pair of points given an array of points using brute force"""
    p = q = None
    n = len(points)
    best = math.inf
    for i in range(n):
        for j in range(i+1, n):
            if points[i].distance(points[j]) < best:
                best = points[i].distance(points[j])
                p = points[j]
                q = points[i]
    return p, q


def main():
    """main function"""
    arr = [(0, 10), (8, 2), (11, 7), (7, 11), (18, 8), (10, 16)]
    points = []
    for a in arr:
        points.append(Point(a[0], a[1]))
    for p in points:
        print(p)
    print("---")
    p, q = closestPair(points)
    p2, q2 = closestPairBrute(points)
    if p is not None and q is not None:
        print(
            f"{p} and {q} are closes pair with {p.distance(q):.2f} distance using divide and conquer")
    if p2 is not None and q2 is not None:
        print(
            f"{p2} and {q2} are closes pair with {p2.distance(q2):.2f} distance using brute force")


if __name__ == "__main__":
    main()
