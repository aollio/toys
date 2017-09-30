#!/usr/bin/env python3

from os import path
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue

import time

from url_manager import UrlManager
from data_output import DataOutput

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class NodeManager:
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
        manager = BaseManager(address=('127.0.0.1', 8001), authkey=b'baike')
        return manager

    def url_manager_proc(self, url_q: Queue, conn_q: Queue, root_url):
        print('url manager process start...')
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        print('url manager process started...')
        while True:
            while url_manager.has_new_url():
                new_url = url_manager.get_new_url()
                print('new_url', new_url)
                # 将新的URL发给工作节点
                url_q.put(new_url)
                # 加一个判断条件, 当爬取2000个链接后就关闭, 并保存进度
                if url_manager.old_url_size() > 2000:
                    # 通知爬行节点工作结束
                    url_q.put('end')
                    print('控制节点发起结束通知')
                    # 关闭管理节点, 同事存储set状态
                    url_manager.save_process(path.join('dist', 'new_urls.txt'), url_manager.new_urls)
                    url_manager.save_process(path.join('dist', 'old_urls.txt'), url_manager.old_urls)
                    return
            # 将从result_solve_proc 获取到的URL添加到URL管理器
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException as e:
                time.sleep(0.1)

    def result_solve_proc(self, result_q: Queue, conn_q: Queue, store_q: Queue):
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get()
                    if content['new_urls'] == 'end':
                        print('结果分析进程接收通知然后结束!')
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])  # url为set类型
                    store_q.put(content['data'])  # 解析出来数据为dict类型
                else:
                    time.sleep(0.1)
            except BaseException as e:
                time.sleep(0.1)

    def store_proc(self, store_q: Queue):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程接收通知然后结束!')
                    output.flush_data()
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)


def main():
    print('init...')
    # 初始化各个管理进程需要的通信通道
    # url_q队列是URL管理进程将URL传递给爬虫节点的通道
    url_q = Queue()
    # result_q是爬虫节点将数据返回给数据提取进程的通道
    result_q = Queue()
    # 数据提取进程将新的URL数据提交给URL管理进程的通道
    conn_q = Queue()
    #
    store_q = Queue()

    # 创建分布式管理器
    node = NodeManager()
    manager = node.start_manager(url_q, result_q)
    # 创建URL管理进程, 数据提取进程和数据存储进程
    root_url = "https://baike.baidu.com/item/网络爬虫/5162711"
    url_manager_proc = Process(target=node.url_manager_proc, args=(url_q, conn_q, root_url))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q))
    store_proc = Process(target=node.store_proc, args=(store_q,))
    # 启动三个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    print('init finish.')
    manager.get_server().serve_forever()


if __name__ == '__main__':
    main()
