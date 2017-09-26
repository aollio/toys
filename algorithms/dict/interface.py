#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod
from collections import Iterable

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class DictInterface(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs:
            self.__setitem__(key, value)

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def items(self) -> Iterable:
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass

    @property
    def empty(self):
        return len(self) == 0

    def __contains__(self, item):
        return self[item] is not None

    def __str__(self):
        a = {}
        for key, value in self.items():
            a[key] = value
        return str(a)

    def __repr__(self):
        return self.__str__()


class SortedDictInterface(DictInterface, metaclass=ABCMeta):
    class ItemsSortedIterator:
        def __init__(self, sorted_dict):
            self.sorted_dict = sorted_dict

        def __iter__(self):
            sdict = self.sorted_dict
            if len(sdict) == 0:
                raise StopIteration

            curr_index = 0
            while curr_index < len(sdict):
                key = sdict.select(curr_index)
                value = sdict[key]
                curr_index += 1
                yield key, value

    @abstractmethod
    def select(self, rank):
        """获取排名为`rank`的键"""
        pass

    @abstractmethod
    def rank(self, key) -> int:
        """获取`key`的排名"""
        pass

    def floor(self, key):
        """小于等于`key`的最大键"""
        curr_key = self.select(self.rank(key))
        if curr_key == key:
            return key
        else:
            if curr_key == 0:
                raise AttributeError("the 'key' is too small")
            else:
                return self.select(self.rank(key) - 1)

    def ceiling(self, key):
        """大于等于`key`的最小键"""
        rank = self.rank(key)
        curr_key = self.select(rank)
        if curr_key == key:
            return key
        else:
            if curr_key == len(self):
                raise AttributeError("the 'key' is too large")
            else:
                return self.select(rank - 1)

    def min(self):
        if self.empty:
            raise AttributeError("the dict is empty")
        else:
            return self.select(0)

    def max(self):
        if self.empty:
            raise AttributeError("the dict is empty")
        else:
            return self.select(len(self) - 1)

    def del_min(self):
        del self[self.min()]

    def del_max(self):
        del self[self.max()]

    def items(self):
        return self.ItemsSortedIterator(self)
