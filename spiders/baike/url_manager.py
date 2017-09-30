#!/usr/bin/env python3

import hashlib
import pickle

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def md5(url):
    md5lib = hashlib.md5()
    md5lib.update(url.encode('utf-8'))
    return md5lib.hexdigest()[8:-8]


class UrlManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def get_new_url(self):
        """获取一个未爬取的URL"""
        new_url = self.new_urls.pop()
        self.old_urls.add(md5(new_url))
        return new_url

    def add_new_url(self, url):
        """

        :param url:
        :return:
        """
        if url is None:
            return
        if url not in self.new_urls and md5(url) not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return self.new_url_size() != 0

    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)

    def save_process(self, path, data):
        """
        保存进度到`path`给定的文件
        :param path: 文件路径
        :param data: 数据
        :return:
        """
        with open(path, 'wb') as file:
            pickle.dump(data, file)

    def load_process(self, path):
        """
        从本地文件加载进度
        :param path: 文件路径
        :return: 从文件中读取的数据
        """
        print('[+] 从文件加载进度：%s' % path)

        try:
            with open(path, 'rb') as file:
                tmp = pickle.load(file)
                return tmp
        except:
            print('[!] 无进度文件， 创建：%s' % path)

        return set()
