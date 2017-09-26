#!/usr/bin/env python3
import dictutil
from interface import DictInterface

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class SequentialSearchDict(DictInterface):
    class Node:
        def __init__(self, key=None, value=None, next=None):
            self.next = next
            self.value = value
            self.key = key

    class ItemsIterator:
        def __init__(self, node=None):
            self.node = node
            self.curr = node

        def __iter__(self):
            if self.curr is None:
                raise StopIteration

            while self.curr is not None:
                key, value = self.curr.key, self.curr.value
                self.curr = self.curr.next
                yield key, value

    def __init__(self):
        self.first = None

    def __setitem__(self, key, value):
        curr = self.first
        while curr is not None:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next
        # create new node to the first
        new = self.Node(key=key, value=value, next=self.first)
        self.first = new

    def __getitem__(self, item):
        first = self.first
        curr = first
        while curr is not None:
            if curr.key == item:
                return curr.value
            curr = curr.next
        return None

    def __delitem__(self, key):
        first = self.first
        if first.key == key:
            self.first = self.first.next
        parent = first
        first = first.next
        while first is not None:
            if first.key == key:
                parent.next = first.next
            parent = first
            first = first.next

    def items(self):
        return self.ItemsIterator(node=self.first)

    def __len__(self):
        size = 0
        curr = self.first
        while curr is not None:
            size += 1
            curr = curr.next
        return size


if __name__ == '__main__':
    dictutil.test_dict(SequentialSearchDict())
