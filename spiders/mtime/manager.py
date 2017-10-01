#!/usr/bin/env python3

import time
from data_output import DataOutput
from html_downloader import HtmlDownloader
from html_parser import HtmlParser

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Spider:
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        content = self.downloader.download(root_url)
        urls = self.parser.parse_url(root_url, content)
        for url in urls:
            try:
                # http://service.library.mtime.com/Movie.api
                # ?Ajax_CallBack=true
                # &Ajax_CallBackType=Mtime.Library.Services
                # &Ajax_CallBackMethod=GetMovieOverviewRating
                # &Ajax_CrossDomain=1
                # &Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2F246526%2F&t=201710117174393728&Ajax_CallBackArgument0=246526
                t = time.strftime('%Y%m%d%H%M%S3282', time.localtime())
                rank_url = 'http://service.library.mtime.com/Movie.api' \
                           '?Ajax_CallBack=true' \
                           '&Ajax_CallBackType=Mtime.Library.Services' \
                           '&Ajax_CallBackMethod=GetMovieOverviewRating' \
                           '&Ajax_CrossDomain=1' \
                           '&Ajax_RequestUrl=%s' \
                           '&t=%s' \
                           '&Ajax_CallbackArgument0=%s' % (url[0].replace('://', '%3A%2F%2F')[:-1], t, url[1])
                rank_content = self.downloader.download(rank_url)
                if rank_content is None:
                    print('None')
                data = self.parser.parse_json(rank_url, rank_content)
                self.output.store_data(data)
            except Exception as e:
                raise e
                # print(e)
                # print('Crawl failed')

        self.output.output_end()
        print('Crawl finish')


def main():
    spider = Spider()
    spider.crawl('http://theater.mtime.com/China_Beijing/')


if __name__ == '__main__':
    main()
