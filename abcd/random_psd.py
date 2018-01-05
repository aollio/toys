#!/usr/bin/env python3

from string import ascii_uppercase
from random import choice

chars = ascii_uppercase + '1234567890'


def random_psd():
    return '-'.join([''.join([choice(chars) for _ in range(3)]) for _ in range(4)])


if __name__ == '__main__':
    print(random_psd())
