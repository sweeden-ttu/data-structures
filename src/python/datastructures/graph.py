"""
Graph data structures: Graph, DirectedGraph, UndirectedGraph
"""

from typing import Any, Iterator, Optional, List, Set, Dict
from collections import deque
from .base import AbstractDataStructure


class Graph(AbstractDataStructure):
    """Base graph data structure."""

    def __init__(self):
        self._adjacency: Dict[Any, List[Any]] = {}

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph."""
        if vertex not in self._adjacency:
            self._adjacency[vertex] = []

    def add_edge(self, v1: Any, v2: Any) -> None:
        """Add an edge between two vertices."""
        self.add_vertex(v1)
        self.add_vertex(v2)
        self._add_edge_impl(v1, v2)

    def _add_edge_impl(self, v1: Any, v2: Any) -> None:
        """Implement edge addition (to be overridden)."""
        pass

    def vertices(self) -> List[Any]:
        """Return all vertices."""
        return list(self._adjacency.keys())

    def edges(self) -> List[tuple]:
        """Return all edges."""
        result = set()
        for v1, neighbors in self._adjacency.items():
            for v2 in neighbors:
                result.add(self._normalize_edge(v1, v2))
        return list(result)

    def _normalize_edge(self, v1: Any, v2: Any) -> tuple:
        """Normalize edge representation."""
        return (v1, v2)

    def neighbors(self, vertex: Any) -> List[Any]:
        """Return neighbors of a vertex."""
        return self._adjacency.get(vertex, [])

    def is_empty(self) -> bool:
        return len(self._adjacency) == 0

    def size(self) -> int:
        return len(self._adjacency)

    def clear(self) -> None:
        self._adjacency.clear()

    def __iter__(self) -> Iterator[Any]:
        return iter(self.vertices())

    def __contains__(self, vertex: Any) -> bool:
        return vertex in self._adjacency

    def __repr__(self) -> str:
        return f"Graph(vertices={len(self._adjacency)})"


class DirectedGraph(Graph):
    """Directed graph."""

    def _add_edge_impl(self, v1: Any, v2: Any) -> None:
        """Add directed edge."""
        if v2 not in self._adjacency[v1]:
            self._adjacency[v1].append(v2)

    def in_degree(self, vertex: Any) -> int:
        """Return in-degree of vertex."""
        count = 0
        for neighbors in self._adjacency.values():
            if vertex in neighbors:
                count += 1
        return count

    def out_degree(self, vertex: Any) -> int:
        """Return out-degree of vertex."""
        return len(self._adjacency.get(vertex, []))

    def topological_sort(self) -> List[Any]:
        """Return topological sort of vertices."""
        in_degree = {v: self.in_degree(v) for v in self.vertices()}
        queue = deque([v for v in self.vertices() if in_degree[v] == 0])
        result = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in self.neighbors(vertex):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self.vertices()):
            raise ValueError("Graph has a cycle")

        return result

    def dfs(self, start: Any) -> Iterator[Any]:
        """Depth-first search."""
        visited: Set[Any] = set()
        stack = [start]

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                yield vertex
                for neighbor in reversed(self.neighbors(vertex)):
                    if neighbor not in visited:
                        stack.append(neighbor)

    def bfs(self, start: Any) -> Iterator[Any]:
        """Breadth-first search."""
        visited: Set[Any] = set()
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                yield vertex
                queue.extend(self.neighbors(vertex) - visited)

    def __repr__(self) -> str:
        return f"DirectedGraph(vertices={len(self._adjacency)})"


class UndirectedGraph(Graph):
    """Undirected graph."""

    def _add_edge_impl(self, v1: Any, v2: Any) -> None:
        """Add undirected edge."""
        if v2 not in self._adjacency[v1]:
            self._adjacency[v1].append(v2)
        if v1 not in self._adjacency[v2]:
            self._adjacency[v2].append(v1)

    def _normalize_edge(self, v1: Any, v2: Any) -> tuple:
        """Normalize edge (order-independent)."""
        return tuple(sorted([v1, v2]))

    def degree(self, vertex: Any) -> int:
        """Return degree of vertex."""
        return len(self._adjacency.get(vertex, []))

    def is_connected(self) -> bool:
        """Check if graph is connected."""
        if self.is_empty():
            return True
        visited: Set[Any] = set()
        start = next(iter(self.vertices()))

        def dfs(v: Any) -> None:
            visited.add(v)
            for neighbor in self.neighbors(v):
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(start)
        return len(visited) == len(self.vertices())

    def __repr__(self) -> str:
        return f"UndirectedGraph(vertices={len(self._adjacency)})"
