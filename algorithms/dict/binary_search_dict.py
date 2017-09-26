#!/usr/bin/env python3

from interface import SortedDictInterface
from dictutil import test_dict

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class BinarySearchDict(SortedDictInterface):
    def __init__(self, **kwargs):
        self.keys = []
        self.values = []
        # super init to put item
        super(BinarySearchDict, self).__init__(**kwargs)

    def select(self, rank):
        return self.keys[rank]

    def rank(self, key):
        return self._rank(key, 0, len(self.keys) - 1)

    def _rank(self, key, low, high):
        if low > high:
            return low
        mid = low + (high - low) // 2
        keys = self.keys
        if keys[mid] == key:
            return mid
        elif keys[mid] < key:
            return self._rank(key, mid + 1, high)
        elif keys[mid] > key:
            return self._rank(key, low, mid - 1)

    def __len__(self):
        return len(self.keys)

    def __setitem__(self, key, value):
        position = self.rank(key)
        if position < len(self) and self.keys[position] == key:
            # update new value
            self.values[position] = value
        else:
            # insert new key-value
            # if the key big than all other keys.
            # locate at the right of list
            self.keys.insert(position, key)
            self.values.insert(position, value)

    def __getitem__(self, key):
        position = self.rank(key)
        if position < len(self) and self.keys[position] == key:
            return self.values[position]
        else:
            return None

    def __delitem__(self, key):
        position = self.rank(key)
        if self.keys[position] == key:
            self.keys.pop(position)
            self.values.pop(position)
        else:
            raise AttributeError("key '%s' not exist. " % key)


def main():
    dicti = BinarySearchDict()
    dicti.keys = [1, 3, 6, 8, 11, 12]
    print(dicti.rank(9))
    for key in dicti.keys:
        assert key == dicti.select(dicti.rank(key))
    for index in range(len(dicti.keys)):
        assert index == dicti.rank(dicti.select(index))


if __name__ == '__main__':
    test_dict(BinarySearchDict())
    # main()
