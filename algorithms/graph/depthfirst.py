#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

from interface import Graph


class Cycle:
    """G是无环图吗，（假设不存在自环或平行边）"""

    def __init__(self, g: Graph):
        self._marked = [False for x in range(g.V())]
        self._has_cycle = False

        for v in range(g.V()):
            if not self._marked[v]:
                self._dfs(g, v, v)

    def _dfs(self, g: Graph, v: int, u: int):
        self._marked[v] = True
        for w in g.adj(v):
            if not self._marked[w]:
                self._dfs(g, v, u)
            elif w != u:
                self._has_cycle = True

    def has_cycle(self):
        return self._has_cycle
