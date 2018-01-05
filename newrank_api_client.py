import hashlib
import logging
import random
import math
import functools
import requests

from urllib.parse import urlencode

BASE_URL = 'https://www.newrank.cn'
GET_ACCOUNT_ARTICLES_URL = '/xdnphb/detail/getAccountArticle'
SEARCH_OFFICIAL_WEIXIN_ACCOUNT = '/xdnphb/data/weixinuser/searchWeixinDataByCondition'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
token = 'AA79F89BA13E514FE5BB69C90B7E8578'


def check_response_return_json(func, ret=None):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        if resp.status_code != 200 or resp.text == '':
            logging.error(
                f' [{func.__name__} error]: code {resp.status_code}, text: {resp.text}, args: {args}, kwargs: {kwargs}')
            retu = [] if ret is None else ret
            return retu
        else:
            return resp.json()

    return wrapper


class NewrankClient():
    def __init__(self, token):
        self.token = token
        self.headers = {
            'User-Agent': user_agent,
            'Cookie': 'token=%s; tt_token=true; ' % token,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.newrank.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',

        }

    def post(self, api_suffix, params):
        if isinstance(params, str):
            return requests.post(BASE_URL + api_suffix, data=params, headers=self.headers)
        else:
            qurey_str = self.form_encoding(api_suffix, params)
            return requests.post(BASE_URL + api_suffix, data=qurey_str, headers=self.headers)

    def nonce(self):
        chars = '0123456789abcdef'
        res = ''
        for _ in range(9):
            res += chars[math.floor(16 * random.random())]
        return res

    def xyz(self, api_suffix, params_list: list):
        md5_str = api_suffix + '?AppKey=joker&' + '&'.join(map(lambda x: '='.join(x), params_list))
        return hashlib.md5(md5_str.encode()).hexdigest()

    def form_encoding(self, api_suffix, params: dict):
        params_list = [entry for entry in params.items()]
        params_list.sort(key=lambda x: x[0])
        params_list.append(('nonce', self.nonce()))
        xyz_param = self.xyz(api_suffix, params_list)
        params_list.append(('xyz', xyz_param))
        return urlencode(params_list)

    @check_response_return_json
    def get_account_articles(self, uuid):
        params = {
            'uuid': uuid,
            'flag': 'true'
        }
        return self.post(GET_ACCOUNT_ARTICLES_URL, params)

    @check_response_return_json
    def search_weixin_official_account(self, keyword, filter='', order=''):
        """
        :param keyword: keyword
        :param filter: one or more in [nickname, tags, auth(认证主体), top500, ori(原创), server(服务号), certified(认证号)]
        separate by '|'. e.g. 'tags|top500'
        :param order: relation(综合-默认), NRI(新榜指数), collect(收藏人数)
        :return:
        """
        params = {
            'keyName': keyword,
            'order': order,
            'filter': filter,
            'hasDeal': 'false',
        }

        return self.post(SEARCH_OFFICIAL_WEIXIN_ACCOUNT, params)

    def __str__(self):
        return f'<{self.__class__.__name__}>'

    __repr__ = __str__
