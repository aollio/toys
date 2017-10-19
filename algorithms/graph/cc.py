#!/usr/bin/env python3


from interface import Graph, CC

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class DepthFirstCC(CC):
    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.g = graph
        self._marked = [False for x in range(graph.vertex_count())]
        self._count = 0
        self._ids = [-1 for x in range(graph.vertex_count())]
        for v in range(graph.vertex_count()):
            if not self._marked[v]:
                self._dfc(v)
                self._count += 1

    def _dfc(self, v: int):
        self._marked[v] = True
        self._ids[v] = self._count
        for w in self.g.adj(v):
            if not self._marked[w]:
                self._dfc(w)

    def connected(self, v: int, w: int) -> int:
        return self._ids[v] == self._ids[w]

    def id(self, v: int) -> int:
        return self._ids[v]

    def count(self) -> int:
        return self._count


def main():
    import util
    g = util.tiny_graph()
    cc = DepthFirstCC(g)

    count = cc.count()
    print(count, 'components')
    components = [[] for x in range(count)]
    for v in range(g.vertex_count()):
        components[cc.id(v)].append(v)

    for com in components:
        print(com)


if __name__ == '__main__':
    main()
