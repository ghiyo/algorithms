"""
filename: minimum_cut.py
"""

from multiprocessing import Pool, cpu_count
import copy
import math
import multiprocessing
import os
from numpy import random
import numpy


def PickRandomEdge(graph):
    """Randomly selects the an edge (u,v) uniformly at random and returns the indices"""
    vertices = []
    u_index = random.randint(0, len(graph))
    vertices.append(u_index)
    v_vertex = graph[u_index][random.randint(1, len(graph[u_index]))]
    for v_index in range(len(graph)):
        if graph[v_index][0] == v_vertex:
            vertices.append(v_index)
    return vertices


def MergeEdgeList(graph, edge):
    """Merges the two vertices of an edge into one vertex and joins their adjacent edges"""
    v_vertex = graph[edge[1]][0]
    u_vertex = graph[edge[0]][0]
    v_adj_edges = graph[edge[1]]
    for i in range(1, len(v_adj_edges)):
        if v_adj_edges[i] != u_vertex:
            graph[edge[0]].append(v_adj_edges[i])
    graph.pop(edge[1])
    for adj_edges in graph:
        for i in range(1, len(adj_edges)):
            if adj_edges[i] == v_vertex:
                adj_edges[i] = u_vertex
    u_new_index = 0
    for i in range(len(graph)):
        if graph[i][0] == u_vertex:
            u_new_index = i
    return u_new_index


def RemoveLoops(graph, vertex_index):
    """Removes self loops on a vertex"""
    i = 1
    while i < len(graph[vertex_index]):
        if graph[vertex_index][i] == graph[vertex_index][0]:
            graph[vertex_index].pop(i)
        else:
            i += 1


def RContraction(graph):
    """Random Contraction Algorithm implementations"""
    if len(graph) < 2:
        cut = 0
    else:
        while len(graph) > 2:
            redge = PickRandomEdge(graph)
            merged_index = MergeEdgeList(graph, redge)
            RemoveLoops(graph, merged_index)
        cut = len(graph[0][1:])
    return cut


def min_cut_trial(graph, trials):
    graph_copy = copy.deepcopy(graph)
    min_cut = RContraction(graph_copy)
    for i in range(trials):
        if multiprocessing.current_process().name == "ForkPoolWorker-1":
            percentage_completed = i / trials * 100
            print(f'\r>> {trials} / {i} (% {percentage_completed:.2f})',
                  end="", flush=True)
        graph_copy = copy.deepcopy(graph)
        new_min_cut = RContraction(graph_copy)
        if new_min_cut < min_cut:
            min_cut = new_min_cut
    return min_cut


def minimum_cut(graph):
    """Returns the minimum cut of a graph"""
    graph_copy = copy.deepcopy(graph)
    min_cut = RContraction(graph_copy)
    n = len(graph)
    trial_num = int(numpy.ceil((n ** 2) * numpy.log(n))) - 1
    with Pool(processes=cpu_count()) as p:
        p_trial_num = math.ceil(trial_num / cpu_count())
        results = p.starmap(min_cut_trial, [(graph, p_trial_num)
                                            for _ in range(cpu_count())])
        p.close()
        p.join()
    min_cut = min(results)
    return min_cut


def main():
    """main function"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/KargerMinCut.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    nums = f.read().strip().split("\n")
    f.close()
    graph = [[] for _ in range(len(nums))]
    for i in range(len(nums)):
        arr = nums[i].split()
        graph[i] = [int(a) for a in arr]
    print(minimum_cut(graph))


if __name__ == "__main__":
    main()
