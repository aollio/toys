from .interface import Graph, Search


class DepthFirstSearch(Search):
    def __init__(self, graph: Graph, s: int):
        self._marked = [False for x in range(graph.vertex_count())]
        self._dfs(graph, s)
        self._count = 0

    def _dfs(self, graph: Graph, v: int) -> None:
        self._marked[v] = True
        self._count += 1
        for w in graph.adj(v):
            # 如果这个顶点没有被遍历过, 则递归寻找
            if not self.marked(w):
                self._dfs(graph, w)

    def count(self) -> int:
        return self._count

    def marked(self, v: int) -> bool:
        return self._marked[v]
