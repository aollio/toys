#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

from adj_graph import AdjGraph, Graph


def read_graph(numbers: list) -> Graph:
    """
    Parse numbers to graph.
    first number of numbers is the count of vertex.
    second number of numbers is the count of edge.
    :param numbers: list
    :return:
    """
    graph = AdjGraph(numbers[0])
    count = 2
    for index in range(numbers[1]):
        graph.add_edge(numbers[count], numbers[count + 1])
        count += 2
    return graph


_tiny_g = [13, 13, 0, 5, 4, 3, 0, 1, 9, 12, 6, 4, 5, 4, 0, 2, 11, 12, 9, 10, 0, 6, 7, 8, 9, 11, 5, 3]
_tiny_cg = [6, 8, 0, 2, 0, 1, 0, 5, 2, 1, 2, 3, 2, 4, 3, 5, 3, 4]


def tiny_graph():
    return read_graph(_tiny_g)


def tiny_cgraph():
    return read_graph(_tiny_cg)


if __name__ == '__main__':
    g = read_graph(_tiny_g)
    print(g)
