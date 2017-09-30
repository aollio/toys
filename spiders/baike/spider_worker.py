#!/usr/bin/env python3


from multiprocessing.managers import BaseManager
from html_downloader import HtmlDownloader
from html_parser import HtmlParser

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class SpiderWorker:
    def __init__(self, address='127.0.0.1', port=8001, authkey=b'baike'):
        """初始化分布式进程中工作节点的连接工作"""
        # 注册用于获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 连接到服务器
        print('Connect to server %s:%s...' % (address, port))
        self.manager = BaseManager(address=(address, port), authkey=authkey)
        # 开始连接
        self.manager.connect()
        # 获取Queue对象
        self.task_q = self.manager.get_task_queue()
        self.result_q = self.manager.get_result_queue()
        # 初始化下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):

        while True:
            try:
                if not self.task_q.empty():
                    url = self.task_q.get()

                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作...')
                        # 接着通知其他节点停止工作
                        self.result_q.put({'new_urls': 'end', 'data': 'end'})
                        return

                    print('爬虫节点正在解析: %s' % url)
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parse(url, content)
                    self.result_q.put({'new_urls': new_urls, 'data': data})

                else:
                    print('task queue is empty', self.task_q.empty())
            except EOFError:
                print('连接工作节点失败')
                return
            except Exception as e:
                print(e)
                print('crawl fail')


if __name__ == '__main__':
    spider = SpiderWorker()
    spider.crawl()
