#!/usr/bin/env python3

import requests

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def right_or(res: requests.Response, msg):
    if res.status_code != 200:
        print(msg)


def get_accounts():
    token_url = 'https://api.yeziapp.com/client/tokens'
    account_url = 'https://api.yeziapp.com/client/accounts'

    tokens_response = requests.post(token_url, json={'serialNumber': 'C02SDDLEFVH3', 'seller': 'yezi'})
    right_or(tokens_response, '获取Token时失败')
    # [('CLOVER_TOKEN', '53045d82-d4aa-4ff0-abbf-132ba45502f5'),
    #  ('CLOVER_TOKEN.sig', '388YrW8J0YQpJFh-f465kF5LL5U')]
    tokens = tokens_response.cookies.items()

    headers = {
        'referer': 'https://yezi-apps.yeziapp.com/nav',
        'cookie': ';'.join(['='.join(token) for token in tokens])
    }

    accounts_response = requests.get(account_url, headers=headers)
    right_or(accounts_response, '获取账号时失败')

    return [{'apple_id': item['appleID'], 'password': item['password']} for item in accounts_response.json()]


print(get_accounts())
