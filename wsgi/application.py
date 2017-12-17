#!/usr/bin/env python3


__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    response_body = b'Hello World'
    start_response(status, response_headers)
    return response_body


import os

a = 'asd'
print(a.startswith('a'))

def main():
    pass


if __name__ == '__main__':
    main()
