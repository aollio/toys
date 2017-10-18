#!/usr/bin/env python3

from interface import Graph, Search


class DepthFirstSearch(Search):
    def __init__(self, graph: Graph, s: int):
        super().__init__(graph, s)
        self._marked = [False for x in range(graph.vertex_count())]
        self._count = 0
        self._dfs(graph, s)

    def _dfs(self, graph: Graph, v: int) -> None:
        self._marked[v] = True
        self._count = self._count +  1
        for w in graph.adj(v):
            # 如果这个顶点没有被遍历过, 则递归寻找
            if not self.marked(w):
                self._dfs(graph, w)

    def count(self) -> int:
        return self._count

    def marked(self, v: int) -> bool:
        return self._marked[v]


if __name__ == '__main__':
    import util
    import sys

    arg = int(sys.argv[1])
    g = util.tiny_graph()
    search = DepthFirstSearch(g, arg)

    for v in range(g.V()):
        if search.marked(v):
            print(v, end=' ')
    print()

    if search.count() != g.V():
        print('NOT', end=' ')
    print('CONNECTED')
