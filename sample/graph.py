"""
filename: graph.py

"""


from collections import defaultdict
import os
import sys
import threading
sys.setrecursionlimit(800000)
threading.stack_size(67108864)


class Graph:
    """Graph represnetation of data"""

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.scc_num = 0
        self.scc_size_list = []

    def add_edge(self, src, dest):
        """adds an undirected edge between a src node and dest node."""
        assert src > 0 and dest > 0, "vertices must be labeled > 0"
        self.graph[src].append(dest)

    def get_transpose(self):
        """returns a transposed version of the graph (all edges reversed)"""
        t_graph = Graph(self.V)
        for i in self.graph:
            print(f'\rGraph transpose progress: {i/self.V * 100:.2f}', end="")
            for j in self.graph[i]:
                t_graph.add_edge(j, i)
        print()
        return t_graph

    def print_graph(self):
        """prints the adjacency list of the graph showing all nodes and their edges"""
        for vertex, edges in self.graph.items():
            print(f'Vertex {vertex}: ', end="")
            for edge in edges:
                print(f'-> {edge} ', end="")
            print()

    def topo_sort(self, graph):
        """returns a stack of a topological ordering of the graph"""
        n = graph.V
        stack = []
        visited = [False] * graph.V
        for v in range(n-1, 0, -1):
            print(
                f'\rTransposed Graph topological sorting progress: {(self.V - v+1)/self.V * 100:.2f}', end="")
            if visited[v] is False:
                self.dfs_topo(graph, v, visited, stack)
        print()
        return stack

    def dfs_topo(self, graph, s, visited, stack):
        """helper dfs method to find the topological ordering of a graph"""
        visited[s] = True
        for v in graph.graph[s+1]:
            if visited[v-1] is False:
                self.dfs_topo(graph, v-1, visited, stack)
        stack.append(s+1)

    def dfs_kosaraju_scc(self):
        """Implementation of the DFS loop to topological ordering"""
        t_graph = self.get_transpose()
        topo_ordering = self.topo_sort(t_graph)
        visited = [False] * self.V
        while topo_ordering:
            v = topo_ordering.pop()
            print(
                f'\rProcessing SCCS: {(self.V - len(topo_ordering))/self.V * 100:.2f}', end="")
            if visited[v-1] is False:
                self.scc_num += 1
                scc_size = self.dfs_scc(v, visited)
                self.scc_size_list.append(scc_size)
        print(
            f'\nNumber of SCCS: {self.scc_num}\nSize of SCCS: {sorted(self.scc_size_list)[-5:]}')

    def dfs_scc(self, s, visited):
        """Depth first search for a vertex in graph"""
        scc_size = 1
        visited[s-1] = True
        for v in self.graph[s]:
            if visited[v-1] is False:
                scc_size += self.dfs_scc(v, visited)
        return scc_size

    def bfs(self, vertex):
        """Breadth first search for a vertex in graph"""
        raise NotImplementedError("Implementation is pending")


def create_graph(graph_size, edge_list):
    """Creates a graph"""
    graph = Graph(graph_size)
    for i in range(len(edge_list)):
        graph.add_edge(edge_list[i][0], edge_list[i][1])
    return graph


test_input = {
    "graph_size": 9,
    "edge_list": [
        [1, 3],
        [2, 1],
        [2, 9],
        [3, 2],
        [4, 6],
        [5, 4],
        [6, 5],
        [6, 8],
        [7, 8],
        [8, 9],
        [9, 7]
    ]}


def main():
    """main function"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/SCCS.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    edges = f.read().strip().split("\n")
    f.close()
    graph_input = [[] for _ in range(len(edges))]
    for i in range(len(edges)):
        print(
            f'\rReading input progress: {(i)/len(edges) * 100:.2f}', end="")
        arr = edges[i].split()
        graph_input[i] = [int(a) for a in arr]
    print()
    graph_size = 875714
    # graph = create_graph(test_input["graph_size"], test_input["edge_list"])
    graph = create_graph(graph_size, graph_input)
    graph.dfs_kosaraju_scc()


if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()
