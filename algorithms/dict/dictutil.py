#!/usr/bin/env python3


import random
import string

from interface import DictInterface, SortedDictInterface

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

CHAR = string.digits + string.ascii_letters


def random_str(length=8):
    return ''.join(random.sample(CHAR, length))


def test_sorted_dict(dict_class: SortedDictInterface):
    target = dict_class

    test_data = {'a': 1, 'c': 5, 'e': 10,
                 'b': 2, 'd': 9, 'f': 11}

    for key, value in test_data.items():
        target[key] = value

    assert target.ceiling(target.max()) == target.max()
    assert target.floor(target.min()) == target.min()
    assert target.max() == target.select(len(test_data) - 1)
    assert target.min() == target.select(0)

    target.del_max()
    target.del_min()

    assert target.min() == 'b'
    assert target.max() == 'e'

    for index in range(len(test_data) - 2):
        del target[target.select(0)]

    assert target.empty


def test_base_dict(dict_class: DictInterface):
    target = dict_class

    assert len(target) == 0
    assert target.empty
    sample = {}

    test_len = 5

    # initialize test data to sample
    for x in range(test_len):
        sample[random_str(x + 8)] = random_str()

    # add sample data to the tester
    for key, value in sample.items():
        target[key] = value

    assert len(target) == test_len

    for key, value in target.items():
        assert value == sample[key]

    # assert the delete operation
    now_len = test_len

    for key, value in sample.items():
        del target[key]
        now_len -= 1
        assert len(target) == now_len
    assert target.empty


def test_dict(dict_class: DictInterface):
    test_base_dict(dict_class)

    if isinstance(dict_class, SortedDictInterface):
        test_sorted_dict(dict_class)

    print('ok.')
