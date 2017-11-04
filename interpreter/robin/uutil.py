#!/usr/bin/env python3
import logging

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

_log = logging.getLogger('Util')


def log_def(func):
    def wrapper(*args, **kw):
        returnvalue = func(*args, **kw)
        _log.info('log call %s(), args: %r, kw: %r, return: %r', func.__name__, args, kw, returnvalue)
        return returnvalue
    return wrapper

