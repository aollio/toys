#!/usr/bin/env python3

import argparse
import time

import sys

from sequential_search_dict import SequentialSearchDict
from binary_search_dict import BinarySearchDict

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def test_count(tester, min_len=8):
    for line in sys.stdin:
        for word in line.strip().split(' '):
            if len(word) < min_len:
                continue
            if word not in tester:
                tester[word] = 0
            else:
                tester[word] += 1

    # find max
    max = ' '
    tester[max] = 0

    for key, value in tester.items():
        if value > tester[max]:
            max = key

    print('max:', max, 'count:', tester[max])


def main(min_len=8):

    # tester = dict()
    # tester = SequentialSearchDict()
    tester = BinarySearchDict()

    before = time.time()
    test_count(tester, min_len)
    end = time.time()

    print('time:', int((end - before) * 1000), ' ms')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', default=8, dest='len', type=int)
    args = parser.parse_args()

    min_len = args.len
    main(min_len)
