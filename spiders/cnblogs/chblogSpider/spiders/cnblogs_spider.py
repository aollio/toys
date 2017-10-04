#!/usr/bin/env python3

import scrapy

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'  # the name of spider
    allowed_domains = ['conblogs.com'] # 允许的域名
    start_urls = [
        'http://www.cnblogs.com/qiyeboy/default.html?page=1'
    ]

    def parse(self, response):
        '''
        对网页的解析工作
        :param response:
        :return:
        '''
        print('do something')