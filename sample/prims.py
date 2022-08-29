"""
filename: prims.py
"""

from copy import deepcopy
import os
import heapq


def calc_mst_length(mst):
    """Calculates the total length of all the edges in a MST"""
    total_length = 0
    for i in mst:
        total_length += i[2]
    return total_length


def delete_from_heap(v, heap):
    """Deletes a certain node from the heap. NOTE: There can be a 
    better way to search and delete by keeping trakc of the index. 
    This implementation does a linear search."""
    w = None
    for i in range(len(heap)):
        if heap[i][1][0] == v or heap[i][1][1] == v:
            w = deepcopy(heap[i])
            temp = heap[len(heap)-1]
            heap[len(heap)-1] = heap[i]
            heap[i] = temp
            break
    if w is not None:
        heap.pop()
        heapq.heapify(heap)
    else:
        w = (1000000000, [])
    return w


def get_adj_list(v, adj_list, frontier, visited):
    """Gets the list of adjacent nodes to v and the lengths and adds it to the frontier"""
    for edge in adj_list:
        if v == edge[0] and visited[edge[1]-1] is False:
            w = delete_from_heap(edge[1], frontier)
            if w[0] > edge[2]:
                heapq.heappush(frontier, (edge[2], [edge[0], edge[1]]))
            else:
                heapq.heappush(frontier, w)
        elif v == edge[1] and visited[edge[0]-1] is False:
            w = delete_from_heap(edge[0], frontier)
            if w[0] > edge[2]:
                heapq.heappush(frontier, (edge[2], [edge[0], edge[1]]))
            else:
                heapq.heappush(frontier, w)


def prims_mst(V, adj_list):
    """Gets the minimum spanning tree from a undirected connected graph"""
    visited = [False] * V
    X = []
    v = adj_list[0][0]
    X.append(v)
    visited[v-1] = True
    mst = []
    frontier = []
    get_adj_list(v, adj_list, frontier, visited)
    while len(X) != V:
        edge = heapq.heappop(frontier)
        mst.append([edge[1][0], edge[1][1], edge[0]])
        if visited[edge[1][0]-1] is False:
            X.append(edge[1][0])
            visited[edge[1][0]-1] = True
            get_adj_list(edge[1][0], adj_list, frontier, visited)
        elif visited[edge[1][1]-1] is False:
            X.append(edge[1][1])
            visited[edge[1][1]-1] = True
            get_adj_list(edge[1][1], adj_list, frontier, visited)

    return X, mst


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/prims.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [i.split() for i in f.readlines()]
    f.close()
    num_vertices = int(lines[0][0])
    adj_list = [[int(i[0]), int(i[1]), int(i[2])] for i in lines[1:]]
    test = [[1, 2, 1], [1, 4, 3], [1, 3, 4], [2, 4, 2], [3, 4, 5]]
    test_num = 4
    X, mst = prims_mst(num_vertices, adj_list)
    print(mst)
    print(len(mst))
    print(
        f'Number of Vertices: {len(X)}\nTotal Length: {calc_mst_length(mst)}')


if __name__ == "__main__":
    main()
