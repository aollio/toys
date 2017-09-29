#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

from components import *


class SpiderManager:
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 添加根url
        self.manager.add_new_url(root_url)
        while self.manager.has_new_url() and self.manager.old_url_size() < 100:
            try:
                # 从URL管理器获取新的url
                new_url = self.manager.get_new_url()
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器解析网页数据
                urls, data = self.parser.parse(new_url, html_cont=html)
                # 讲抽取的urls数据添加到URL管理器中
                self.manager.add_new_urls(urls)
                # 调用数据存储器存储文件
                self.output.store_data(data)

                print('已经爬取%s个链接, 未爬链接数：%s' % (self.manager.old_url_size(), self.manager.new_url_size()))

            except Exception as e:
                print('crawl failed', e)

        self.output.output_html()


if __name__ == '__main__':
    spider = SpiderManager()
    spider.crawl('https://baike.baidu.com/item/快穿文')
