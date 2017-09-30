#!/usr/bin/env python3

import time
from multiprocessing import Pool, Queue, Process, Manager

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def worker(id, task_q: Queue):
    begintime = time.time()
    while True:
        try:
            if not task_q.empty():
                print("%s worker do %s" % (id, task_q.get()))
        except Exception as e:
            print(e)

        if time.time() - begintime > 100:
            return


def boss(task_q: Queue):
    for x in range(3):
        [task_q.put(str(x) + "-" + str(y)) for y in range(5)]
        time.sleep(3)


def main():
    pool = Pool(processes=5)
    task_q = Manager().Queue()
    for i in range(4):
        pool.apply_async(func=worker, args=(i, task_q))
    pool.apply_async(func=boss, args=(task_q,))
    # 关闭pool，使其不在接受新的任务。
    pool.close()
    # 主进程阻塞，等待子进程的退出， join方法要在close或
    pool.join()
    print('done.')


if __name__ == '__main__':
    main()
