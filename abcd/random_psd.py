#!/usr/bin/env python3

from string import ascii_letters, digits
from random import choice
import argparse

chars = ascii_letters + digits + "@%$&()!+-[]"


def random_psd(word_count=4, word_length=3):
    return '-'.join([''.join([choice(chars) for _ in range(word_length)]) for _ in range(word_count)])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--word_length", help="the length per word. default 4", default=4, type=int)
    parser.add_argument("-c", "--word_count", help="the count of words. default 4", default=4, type=int)
    args = parser.parse_args()
    print(random_psd(args.word_count, args.word_length))
