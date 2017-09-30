#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
from urllib import parse

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


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
