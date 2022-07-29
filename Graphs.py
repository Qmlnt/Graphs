"""
Module containing Graph class and some algorithms to it.

By Qmelint (Qmlnt)
"""


class Graph:
    """Class for managing a graph."""

    def __init__(self) -> None:
        self.graph = {}

    def integrity_check(self) -> bool:
        """Checks graph structure for errors."""
        for name in self.graph:
            for vertex in self.graph[name]:
                if vertex not in self.graph:
                    return False
                if name not in self.graph[vertex]:
                    return False
                if self.graph[vertex][name] != self.graph[name][vertex]:
                    return False
        return True

    def add_vertex(self, vertex: str) -> bool:
        """Try to add the vertex and return True or False."""
        if vertex not in self.graph:
            self.graph[vertex] = {}
            return True
        return False

    def rem_vertex(self, vertex: str) -> bool:
        """Try to remove the vertex and return True or False."""
        if vertex in self.graph:
            for name in self.graph[vertex]:
                del self.graph[name][vertex]
            del self.graph[vertex]
            return True
        return False

    def add_edge(self, vertex1: str, vertex2: str, weight: int) -> bool:
        """Add or rewrite an edge between vertex1 and vertex2 to weight and return True or False."""
        if (vertex1 != vertex2) and (vertex1 in self.graph and vertex2 in self.graph):
            self.graph[vertex1][vertex2] = weight
            self.graph[vertex2][vertex1] = weight
            return True
        return False

    def rem_edge(self, vertex1: str, vertex2: str) -> bool:
        """Try to remove the edge between vertex1 and vertex2 and return True or False."""
        if vertex1 in self.graph and vertex2 in self.graph[vertex1]:
            del self.graph[vertex1][vertex2]
            del self.graph[vertex2][vertex1]
            return True
        return False

    def get_weight(self, vertex1: str, vertex2: str) -> int:
        """Return weight between vertex1 and vertex2 or False."""
        if vertex1 == vertex2:
            return 0
        if vertex1 in self.graph and vertex2 in self.graph[vertex1]:
            return self.graph[vertex1][vertex2]
        return False

    def get_vertices(self) -> list:
        """Return graph vertices"""
        return list(self.graph.keys())

    def get_edges(self) -> list:
        """Return graph edges, example: [(1,2), (3,1), (4,2)]"""
        edges = []
        for name in self.graph:
            for vertex in self.graph[name]:
                edge = (name, vertex)
                if not (edge in edges or edge[::-1] in edges):
                    edges.append(edge)
        return edges

    def dijkstras_algorithm(self, vertex1: str, vertex2: str) -> float:
        """Find the shortest distance from vertex1 to vertex2."""
        if vertex1 not in self.graph or vertex2 not in self.graph:
            return -1
        if vertex1 == vertex2:
            return 0

        data = {vertex: [10**10, '-'] for vertex in self.graph.keys()}
        data[vertex1] = [0, vertex1]
        unvisited = sorted(self.get_vertices(), key=lambda x: data[x][0])

        while unvisited:
            current = unvisited[0]
            for vertex in self.graph[current]:
                if vertex in unvisited:
                    new_dist = self.graph[current][vertex]+data[current][0]
                    if new_dist < data[vertex][0]:
                        data[vertex] = [new_dist, current]

            unvisited.remove(current)
            unvisited = sorted(unvisited, key=lambda x: data[x][0])

        return data


# Some testing
if __name__ == "__main__":
    import json
    graph = Graph()
    with open(r"graphs\Fri Jul 29 10-28-40 2022.json", 'r') as file:
        graph.graph = json.load(file)[-1]
    print(graph.dijkstras_algorithm("1", "7"))
