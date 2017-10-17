#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

import time
import os
import os.path as path

GIT_DIR = '/root/static-motion'
AUTO_FILE = 'auto_update'


def main():
    curr_time = time.time()
    with open(path.join(GIT_DIR, AUTO_FILE), 'a', encoding='utf-8') as f:
        f.write(curr_time)
    print('write file ok.')
    os.chdir(GIT_DIR)
    a = os.system('git add %s' % AUTO_FILE)
    if a != 0:
        raise Exception('error: git add %s' % AUTO_FILE)
    a = os.system('git commit -m auto_update')
    if a != 0:
        raise Exception('error: git commit -m auto_update')

    a = os.system('git push')

    if a != 0:
        raise Exception('error: git push')


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60 * 10)
