from collections import deque

"""Generic unweighted directed graph stored as adjacency sets"""

class Graph:
    """Directed graph. A vertex can be any hashable value"""
    def __init__(self):
        self._outgoing = {} # vertex -> set of vertices it points TO
        self._incoming = {} # vertex -> set of vertices that points to IT


    def add_vertex(self, vertex):
        """Add a new vertex with no edges. Raise ValueError if it already exists"""
        if vertex in self._outgoing:
            raise ValueError(f"Vertex {vertex!r} already exists")
        self._outgoing[vertex] = set()
        self._incoming[vertex] = set()


    def has_vertex(self, vertex):
        """Return True if the vertex is in the graph"""
        return vertex in self._outgoing


    def vertices(self):
        """Return a list of all vertices, in the order they were added"""
        return list(self._outgoing)


    def _check_vertex(self, vertex):
        """Raise KeyError if the vertex is not in the graph"""
        if vertex not in self._outgoing:
            raise KeyError(f"Vertex {vertex!r} does not exist")


    def add_edge(self, from_vertex, to_vertex):
        """Add a directed edge from_vertex -> to_vertex"""
        self._check_vertex(from_vertex)
        self._check_vertex(to_vertex)
        if from_vertex == to_vertex:
            raise ValueError("A vertex cannot have an edge to itself")
        if to_vertex in self._outgoing[from_vertex]:
            raise ValueError(f"Edge {from_vertex!r} -> {to_vertex!r} already exists")
        self._outgoing[from_vertex].add(to_vertex)
        self._incoming[to_vertex].add(from_vertex)


    def list_incoming_adjacent_vertex(self, vertex):
        """Return the vertices that have an edge coming INTO this vertex"""
        self._check_vertex(vertex)
        return list(self._incoming[vertex])


    def list_outgoing_adjacent_vertex(self, vertex):
        """Return the vertices this vertex has an edge going OUT to"""
        self._check_vertex(vertex)
        return list(self._outgoing[vertex])


    def remove_edge(self, from_vertex, to_vertex):
        """Remove the edge from_vertex -> to_vertex. Raise ValueError if it does not exist"""
        self._check_vertex(from_vertex)
        self._check_vertex(to_vertex)
        if to_vertex not in self._outgoing[from_vertex]:
            raise ValueError(f"Edge {from_vertex!r} -> {to_vertex!r} does not exist")
        self._outgoing[from_vertex].remove(to_vertex)
        self._incoming[to_vertex].remove(from_vertex)

    def has_path(self, start, target):
        """Return True if target can be reached from start by following edges (BFS)"""
        self._check_vertex(start)
        self._check_vertex(target)
        visited = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current == target:
                return True
            for neighbour in self._outgoing[current]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return False

if __name__ == "__main__":
    graph = Graph()
    for code in ["CS101", "MA101", "CS201", "CS202", "CS301", "CS302", "CS303", "CS401"]:
        graph.add_vertex(code)

    edges = [("CS101", "CS201"), ("CS101", "CS202"), ("CS201", "CS301"),
             ("MA101", "CS301"), ("CS201", "CS302"), ("CS202", "CS302"),
             ("CS202", "CS303"), ("CS301", "CS401")]
    for prerequisite, course in edges:
        graph.add_edge(prerequisite, course)

    print("Vertices:", graph.vertices())
    print("Incoming to CS302:", sorted(graph.list_incoming_adjacent_vertex("CS302")))
    print("Incoming to CS101:", sorted(graph.list_incoming_adjacent_vertex("CS101")))
    print("Outgoing from CS201:", sorted(graph.list_outgoing_adjacent_vertex("CS201")))

    for bad_edge in [("CS101", "CS101"), ("CS101", "CS201"), ("CS101", "CS999")]:
        try:
            graph.add_edge(*bad_edge)
        except (ValueError, KeyError) as error:
            print("Rejected:", error)

    print("\nPath CS101 -> CS401?", graph.has_path("CS101", "CS401"))
    print("Path CS401 -> CS101?", graph.has_path("CS401", "CS101"))
    print("Path MA101 -> CS302?", graph.has_path("MA101", "CS302"))
    print("Would CS401 -> CS101 create a cycle?", graph.has_path("CS101", "CS401"))

    graph.remove_edge("CS202", "CS303")
    print("\nAfter removing CS202 -> CS303:")
    print("Incoming to CS303:", sorted(graph.list_incoming_adjacent_vertex("CS303")))
    print("Outgoing from CS202:", sorted(graph.list_outgoing_adjacent_vertex("CS202")))
    try:
        graph.remove_edge("CS202", "CS303")
    except ValueError as error:
        print("Rejected:", error)