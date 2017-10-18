from typing import Iterable

from interface import Graph


class AdjGraph(Graph):
    def __init__(self, vertex_count=0):
        self._vertex_count = vertex_count
        self._edge_count = 0
        # 邻接表, 初始化
        self._adj = [[] for x in range(vertex_count)]
        pass

    def add_edge(self, v, w) -> None:
        self._adj[v].append(w)
        self._adj[w].append(v)
        self._edge_count += 1
        return

    def adj(self, v) -> Iterable[int]:
        return self._adj[v]

    def vertex_count(self) -> int:
        return self._vertex_count

    def edge_count(self) -> int:
        return self._edge_count

    V = vertex_count
    E = edge_count
