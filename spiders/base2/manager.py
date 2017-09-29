#!/usr/bin/env python3

import queue
from multiprocessing.managers import BaseManager

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class SpiderManager:
    def start_manager(self, url_q, result_q):
        """
        创建一个分布式管理器
        :param url_q:  url队列
        :param result_q: 结果队列
        :return:
        """
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        # 绑定端口8001, 设置验证口令 'baike'. 这个相当于对象的初始化
        manager = BaseManager(address=('', 8001), authkey='baike')
        return manager
