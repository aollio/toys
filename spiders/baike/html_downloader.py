#!/usr/bin/env python3

import requests

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


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
