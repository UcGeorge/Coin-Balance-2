from json.decoder import JSONDecoder
from threading import Thread
from typing import Any, Dict


import http.client
import decimal

# create a new context for this task
ctx = decimal.Context()

# 20 digits should be enough for everyone :D
ctx.prec = 20


def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


def get(host: str, url: str, json: bool = False) -> str:
    conn = http.client.HTTPSConnection(host)
    headers = {
        'Cookie': 'ASP.NET_SessionId=ojesw3gqpzvqual4zg1zvfz4; __cflb=02DiuFnsSsHWYH8WqVXbZzkeTrZ6gtmGUuxZNBWynJU3E'
    }
    conn.request("GET", url, '', headers)
    res = conn.getresponse()
    data = res.read()
    _html = JSONDecoder().decode(data.decode("utf-8")) if json else data.decode("utf-8")
    return _html


def combine(a: 'Dict[str, Any]', b: 'Dict[str, Any]', address: str) -> Dict[str, Any]:
    print(f'[INFO] Merging results for Etherscan and BscScan')
    result: Dict[str, Any] = {}
    result[address] = {}

    for j in a.keys():
        result[address][j] = a[j]
    for j in b.keys():
        result[address][j] = b[j]
    return result


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        # print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
