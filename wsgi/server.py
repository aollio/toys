#!/usr/bin/env python3

import socket
from io import StringIO

import sys

import datetime

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class WSGIServer:
    socket_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 10

    def __init__(self, address):
        self.socket = socket.socket(self.socket_family, type=self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(address)
        self.socket.listen(self.request_queue_size)
        host, port = self.socket.getsockname()[:2]
        self.host = host
        self.port = port

    def set_application(self, application):
        self.application = application

    def serve_forever(self):
        while True:
            self.connection, client_addr = self.socket.accept()
            self.handle_request()

    def handle_request(self):
        self.request_data = self.connection.recv(1024).decode('utf-8')
        self.request_lines = self.request_data.splitlines()
        try:
            self.get_url_parameter()
            env = self.get_environ()
            result = self.application(env, self.start_response)
            self.finish_response(result)
        except Exception as e:
            raise e

    def get_url_parameter(self):
        self.request_dict = {'path': self.request_lines[0]}
        for item in self.request_lines[1:]:
            if ':' in item:
                self.request_dict[item.split(':')[0]] = item.split(':')[1]
        self.request_method, self.request_path, self.request_version = self.request_dict.get('path').split()

    def get_environ(self):
        environ = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO(self.request_data),
            'wsgi.error': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprovess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': self.request_method,
            'PATH_INFO': self.request_path,
            'SERVER_NAME': self.host,
            'SERVER_PORT': self.port,
            'USER_AGENT': self.request_dict.get('User_Agent')
        }
        return environ

    def start_response(self, status, response_headers):
        headers = [
            ("Date", datetime.datetime.now().strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            )),
            ("Server", 'AOLLIO WSGI 1.0')
        ]
        self.headers = response_headers + headers
        self.status = status

    def finish_response(self, response_body):
        try:
            response = 'HTTP/1.1 {status}\r\n'.format(status=self.status)
            for header in self.headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            response += response_body
            print(type(response))
            by = response.encode()
            print(type(by))
            self.connection.sendall(response.encode())
        finally:
            self.connection.close()


def main():
    port = 8080

    def make_server(address, application):
        server = WSGIServer(address)
        server.set_application(application)
        return server

    import application
    make_server(('', int(port)), application.application).serve_forever()


if __name__ == '__main__':
    main()
