#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

import time
from multiprocessing import Queue, Process


def producer(qu: Queue):
    for x in range(10):
        print('生产了 %s' % x)
        qu.put(x)
        time.sleep(1)


def consumer(qu: Queue):
    while True:
        try:
            if not qu.empty():
                print('消费了 %s' % qu.get())

        except Exception as e:
            print(e)
            print('bad.')


def main():
    queue = Queue()
    consumer_proc = Process(target=consumer, args=(queue,))
    producer_proc = Process(target=producer, args=(queue,))
    consumer_proc.start()
    producer_proc.start()

if __name__ == '__main__':
    main()