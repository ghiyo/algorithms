"""
filename: 2sat.py
"""

from collections import defaultdict
import os


class DiGraph():
    """A Directed Graph"""

    def __init__(self, vertices):
        self.V = vertices  # 2 for each vertex for x and ~x
        self.graph = defaultdict(list)

    def add_edge(self, src, dest):
        """adds a directed edge between a src node and dest node."""
        self.graph[src].append(dest)

    def get_transpose(self):
        """returns a transposed version of the graph (all edges reversed)"""
        t_graph = DiGraph(self.V)
        for i in self.graph:
            for j in self.graph[i]:
                t_graph.add_edge(j, i)
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
        stack = []
        visited = {}
        n = graph.V // 2
        for i in range(-n, n+1, 1):
            if i != 0:
                visited[i] = False
        for v in range(-n, n+1, 1):
            if v != 0 and visited[v] is False:
                self.dfs_topo(graph, v, visited, stack)
        return stack

    def dfs_topo(self, graph, s, visited, stack):
        """helper dfs method to find the topological ordering of a graph"""
        visited[s] = True
        for v in graph.graph[s]:
            if visited[v] is False:
                self.dfs_topo(graph, v, visited, stack)
        stack.append(s)

    def dfs_scc(self, s, visited):
        """Depth first search for a vertex in graph"""
        stack = [] + self.graph[s]
        scc = set()
        visited[s] = True
        while stack != []:
            v = stack.pop(0)
            if visited[v] is False:
                scc.add(v)
                visited[v] = True
                for w in self.graph[v]:
                    stack.append(w)
        return scc

    def eval_2sat(self, scc):
        """Checks to see if the strongly connected component contains
        complimentary variables i.e. x and ~x"""
        for v in scc:
            if -1*v in scc:
                return False
        return True

    def scc_2_sat(self):
        """finds strongly connected components and checks for 2-SAT"""
        t_graph = self.get_transpose()
        topo_ordering = self.topo_sort(t_graph)
        visited = {}
        n = self.V // 2
        for i in range(-n, n+1, 1):
            if i != 0:
                visited[i] = False
        satisfiable = True
        while topo_ordering and satisfiable:
            v = topo_ordering.pop()
            if visited[v] is False:
                scc = self.dfs_scc(v, visited)
                scc.add(v)
                satisfiable = self.eval_2sat(scc)
        return satisfiable


def read_file(filename):
    """Reads and returns the contents of a file in a list of strings"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath(f"../input/{filename}", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = [i.strip() for i in f.readlines()]
    f.close()
    return lines


def preprocess_input(arr):
    """takes the raw input for the 2-sat problem and returns two dictionaries.
    one for the variables and one for the clauses."""
    clauses = [(int(j[0]), int(j[1])) for j in [i.split() for i in arr]]
    return clauses


def create_graph(n, clauses):
    """Creates a graph"""
    graph = DiGraph(n*2)
    for clause in clauses:
        e1 = (clause[0] * -1, clause[1])
        e2 = (clause[1] * -1, clause[0])
        graph.add_edge(e1[0], e1[1])
        graph.add_edge(e2[0], e2[1])
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
        [6, -9],
        [7, -9],
        [-9, 9],
        [9, 7]
    ]}


def main():
    """Main function"""
    raw_input = read_file("2sat6.txt")
    # test = ["4", "1 2", "-1 3", "3 4", "-2 -4", "-3 1"]
    # raw_input = test
    n = int(raw_input[0])
    clauses = preprocess_input(raw_input[1:])
    graph = create_graph(n, clauses)
    satisfiable = graph.scc_2_sat()
    print(satisfiable)


if __name__ == "__main__":
    main()
