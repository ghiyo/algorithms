"""
filename: tsp_greedy.py
"""

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


def closest_city(current_city, cities, visited):
    """Finds the closest city"""
    closest_dist = np.inf
    next_city = None
    for city, cords in cities.items():
        if visited[city-1] is False:
            dist = distance(cities[current_city], cords)
            if dist < closest_dist:
                closest_dist = dist
                next_city = city
    return next_city, closest_dist


def tsp_greedy(cities, starting_city, n):
    """Calculates the traveling salesman problem using a greedy approach"""
    dist_travelled = 0
    visited = [False]*n
    visited[starting_city-1] = True
    current_city = starting_city
    for i in range(n-1):
        percentage_completed = abs(i+1) / (n-1) * 100
        print(
            f'\r>> ({i+1}/{n-1}) (% {percentage_completed:.2f})', end="", flush=True)
        next_city, dist = closest_city(current_city, cities, visited)
        if next_city is not None:
            visited[next_city-1] = True
            dist_travelled += dist
            current_city = next_city
    print()
    dist_travelled += distance(cities[current_city], cities[starting_city])
    return dist_travelled


def main():
    """Main function"""
    raw_data = read_file("tsp_greedy.txt")
    # test = ["6",
    #         "1 2 1",
    #         "2 4 0",
    #         "3 2 0",
    #         "4 0 0",
    #         "5 4 3",
    #         "6 0 3"]
    # raw_data = test
    n = int(raw_data[0])
    cities = {}
    for i in raw_data[1:]:
        edge = i.split()
        cities[int(edge[0])] = (float(edge[1]), float(edge[2]))
    l = tsp_greedy(cities, 1, n)
    print(l)


if __name__ == "__main__":
    main()
