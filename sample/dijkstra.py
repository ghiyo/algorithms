"""
filename: graph.py

"""


from collections import defaultdict
import os


class Graph:
    """Graph represnetation of data"""

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.shortest_paths = defaultdict(lambda: 1000000)

    def add_edge(self, src, dest):
        """adds an undirected edge between a src node and dest node."""
        assert len(
            dest) == 2, "dest must have exactly 2 entries for destination vertex and length"
        assert src > 0 and dest[0] > 0, "vertices must be labeled > 0"
        self.graph[src].append(dest)

    def print_graph(self):
        """prints the adjacency list of the graph showing all nodes and their edges"""
        for vertex, edges in self.graph.items():
            print(f'Vertex {vertex}: ', end="")
            for edge in edges:
                for vertex, weight in edge.items():
                    print(f'-> vertex: {vertex} weight: {weight} ', end="")
            print('\n'+'-'*40)

    def find_min_edge(self, edges, X):
        """finds the next smallest edge that goes out from the frontier of visited vertices X"""
        min_length = 1000000
        for edge in edges:
            if X[edge[0]] + edge[2] < min_length:
                w = edge[1]
                min_length = X[edge[0]] + edge[2]
        return w, min_length

    def simple_dijkstra(self, s):
        """Uses the straightforward linear way of processing Dijkstra O(m*n) running time.
        Finds path from s to t"""
        self.shortest_paths = {s: 0}
        cross_edges = [[s]+edge for edge in self.graph[s]]
        while cross_edges:
            w, w_length = self.find_min_edge(
                cross_edges, self.shortest_paths)
            self.shortest_paths[w] = w_length
            for edge in self.graph[w]:
                if edge[0] not in self.shortest_paths:
                    cross_edges.append([w] + edge)
            for v, _ in self.shortest_paths.items():
                i = 0
                while cross_edges and i < len(cross_edges):
                    if cross_edges[i][1] != v:
                        i += 1
                    else:
                        cross_edges.pop(i)
        for v in range(1, self.V+1):
            if v not in self.shortest_paths:
                self.shortest_paths[v] = 1000000
        return self.shortest_paths

    def get_shortest_distance(self, s, t):
        """Finds the shortest distance between s and t"""
        return self.simple_dijkstra(s)[t]

    def heap_dijkstra(self, s, t):
        """Uses a heap data structure to speed up the algorithm running time to O(m*log(n)).
        Finds path from s to t"""
        raise NotImplementedError("Method not implemented yet")


def create_graph(graph_size, graph_input):
    """Creates a graph"""
    graph = Graph(graph_size)
    for vertex, edges in graph_input.items():
        for edge in edges:
            graph.add_edge(vertex, edge)
    return graph


test_input = {
    1: [[2, 1], [3, 5]],
    2: [[5, 2]],
    3: [[4, 2], [2, 2]],
    4: [[6, 1]],
    5: [[3, 1], [4, 2], [6, 5]],
    6: []


}


def main():
    """main function"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/DijkstraData.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    line = f.readline().strip()
    graph_input = {}
    while line != "":
        vertex_input = line.split()
        graph_input[int(vertex_input[0])] = [[int(i)
                                              for i in j.split(',')] for j in vertex_input[1:]]
        line = f.readline().strip()
    f.close()

    graph = create_graph(len(graph_input), graph_input)
    # graph = create_graph(len(test_input), test_input)
    graph.simple_dijkstra(1)
    print(graph.shortest_paths[7])
    print(graph.shortest_paths[37])
    print(graph.shortest_paths[59])
    print(graph.shortest_paths[82])
    print(graph.shortest_paths[99])
    print(graph.shortest_paths[115])
    print(graph.shortest_paths[133])
    print(graph.shortest_paths[165])
    print(graph.shortest_paths[188])
    print(graph.shortest_paths[197])


if __name__ == "__main__":
    main()
