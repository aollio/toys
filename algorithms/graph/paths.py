#!/usr/bin/env python3
from typing import Iterable

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

from interface import Graph, Paths


class DepthFirstPaths(Paths):
    def __init__(self, g: Graph, s: int):
        super().__init__(g, s)
        self.g = g
        self.s = s
        self._marked = [False for x in range(g.V())]
        self._edge_to = [None for x in range(g.V())]
        self._dfs(s)

    def _dfs(self, v):
        # 已经访问过
        self._marked[v] = True
        # 遍历所有的邻点
        for w in self.g.adj(v):
            # 如果已经访问过，则跳过
            if self._marked[w]:
                continue
            # 从v可以到达w
            self._edge_to[w] = v
            self._dfs(w)

    def path_to(self, v: int):
        # dfs没有访问过v，说明v不可达
        if self._marked[v] is False:
            return []
        result = []
        target = v
        result.append(v)
        while self._edge_to[target] is not None and self._edge_to[target] != self.s:
            result.append(self._edge_to[target])
            target = self._edge_to[target]
        result.append(self.s)
        return reversed(result)

    def has_path_to(self, v: int) -> bool:
        return self._marked[v]


class BreadthFirstPaths(Paths):
    def __init__(self, g: Graph, s: int):
        super().__init__(g, s)
        self.g = g
        self.s = s
        self._marked = [False for x in range(g.vertex_count())]
        self._edge_to = [None for x in range(g.vertex_count())]
        self._bfs(s)
        self._edge_to[s] = s

    def _bfs(self, s):
        waitlist = [s]
        while waitlist:
            v = waitlist.pop(0)
            for w in self.g.adj(v):
                if not self._marked[w]:
                    self._edge_to[w] = v
                    self._marked[w] = True  # 这是标记，因为最短路径已知
                    waitlist.append(w)

    def path_to(self, v: int):
        if not self.has_path_to(v):
            return []
        result = [v]
        target = v
        while target is not None and self._edge_to[target] != self.s:
            result.append(self._edge_to[target])
            target = self._edge_to[target]
        result.append(self.s)
        return reversed(result)

    def has_path_to(self, v: int) -> bool:
        return self._marked[v]


if __name__ == '__main__':
    import sys
    import util

    arg = int(sys.argv[1])
    graph = util.tiny_cgraph()
    # paths = BreadthFirstPaths(graph, arg)
    paths = DepthFirstPaths(graph, arg)

    for v in range(graph.vertex_count()):
        print(arg, 'to', v, ': ', end='')
        if paths.has_path_to(v):
            _path = paths.path_to(v)
            print('-'.join(map(lambda x: str(x), _path)))
