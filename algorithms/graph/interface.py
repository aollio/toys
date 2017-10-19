#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod
from typing import Iterable

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Graph(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, vertex_count):
        pass

    @abstractmethod
    def vertex_count(self) -> int:
        pass

    @abstractmethod
    def edge_count(self) -> int:
        pass

    V = vertex_count
    E = edge_count

    @abstractmethod
    def add_edge(self, v, w) -> None:
        """
        想图中添加一条边 v-w
        :return:
        """
        pass

    @abstractmethod
    def adj(self, v) -> Iterable[int]:
        """
        和V相邻的所有顶点
        :param v:
        :return: list[int]
        """
        pass

    def __str__(self) -> str:
        string = '%s vertices, %s edges \n' % (self.vertex_count(), self.edge_count())
        for v in range(self.vertex_count()):
            string += '%s: ' % v
            # for w in range(self.adj(v)):
            #     string += '%s ' % w
            string += ' '.join(map(lambda x: str(x), self.adj(v)))
            string += '\n'
        return string


class Paths(metaclass=ABCMeta):
    """在G中找出所有起点为s的路径"""

    @abstractmethod
    def __init__(self, g: Graph, s: int):
        pass

    @abstractmethod
    def has_path_to(self, v: int) -> bool:
        """是否存在从s到v的路径"""
        pass

    @abstractmethod
    def path_to(self, v: int):
        """s 到 v的路径，如果不存在则返回None"""
        pass


class Search(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, graph: Graph, s: int):
        pass

    @abstractmethod
    def marked(self, v: int) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


class CC(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, graph: Graph):
        pass

    @abstractmethod
    def connected(self, v: int, w: int) -> int:
        """w和v是相连的吗"""
        pass

    @abstractmethod
    def count(self) -> int:
        """连通分量数"""
        pass

    @abstractmethod
    def id(self, v: int) -> int:
        """v所在的连通分量的标志符"""
        pass


def degree(graph: Graph, vertex: int) -> int:
    """
    计算V的度数
    :param graph:
    :param vertex:
    :return:
    """
    _degree = 0
    for w in graph.adj(vertex):
        _degree += 1
    return _degree


def max_degree(graph: Graph) -> int:
    """
    计算所给图中所有顶点的最大度数
    :param graph:
    :return: int
    """
    max = 0
    for vertex in range(graph.vertex_count()):
        if degree(graph, vertex) > max:
            max = degree(graph, vertex)
    return max


def avg_degree(graph: Graph) -> float:
    """
    计算所有顶点的平均度数
    :param graph:
    :return:
    """
    return 2.0 * graph.edge_count() / graph.vertex_count()


def num_of_selfloops(graph: Graph) -> int:
    count = 0
    for v in range(graph.vertex_count()):
        for w in graph.adj(v):
            if v == w:
                count += 1
    return count / 2
