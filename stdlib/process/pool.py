#!/usr/bin/env python3

import time
import multiprocessing

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def say(message):
    for i in range(3):
        print(message)
        time.sleep(1)


def main():
    pool = multiprocessing.Pool(processes=4)
    for i in range(3):
        msg = 'hello %s' % i
        pool.apply_async(func=say, args=(msg,))
    pool.close()
    pool.join()
    print('done. sub process(es)')


if __name__ == '__main__':
    main()
