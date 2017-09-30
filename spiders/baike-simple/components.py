#!/usr/bin/env python3

import os
import re
import codecs
from urllib import parse
from bs4 import BeautifulSoup

import requests

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class UrlManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def get_new_url(self):
        """获取一个未爬取的URL"""
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        """

        :param url:
        :return:
        """
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
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


class HtmlDownloader:
    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5 Windows NT)'
        headers = {'User_Agent': user_agent}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            return res.text
        return None


class HtmlParser:
    def parse(self, page_url, html_cont):
        """
        解析网页内容， 抽取URL和需要的数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载页面的内容
        :return: 返回URLS和DATA
        """

        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        """

        :param page_url:
        :param soup:soup
        :return: set
        """
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/item/.+'))
        for link in links:
            new_url = link['href']
            full_url = parse.urljoin(page_url, new_url)
            new_urls.add(full_url)
        return new_urls

    def _get_new_data(self, page_url, soup: BeautifulSoup):
        """

        :param page_url:
        :param soup:
        :return: data 返回有效数据
        """
        data = {}
        data['url'] = page_url
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.text
        summary = soup.find('div', class_='lemma-summary')
        data['summary'] = summary.text
        return data


class DataOutput:
    def __init__(self):
        self.datas = []
        if not os.path.exists('dist'):
            os.mkdir('dist')

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = codecs.open(os.path.join('dist', 'baike.html'), 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write("<head><meta charset='utf-8'/> </head>")
        fout.write('<body>')
        fout.write('<table border="1">')

        fout.write('<tr>')
        fout.write('<th>%s</td>' % 'Link')
        fout.write('<th>%s</td>' % 'Title')
        fout.write('<th>%s</td>' % 'Summary')
        fout.write('</tr>')

        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td>%s</td>' % data['summary'])
            fout.write('</tr>')
            self.datas.remove(data)

        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
