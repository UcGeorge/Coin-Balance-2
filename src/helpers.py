from threading import Thread
from typing import Any, Dict


import http.client


def get(host: str, url: str) -> str:
    conn = http.client.HTTPSConnection(host)
    headers = {
        'Cookie': 'ASP.NET_SessionId=ojesw3gqpzvqual4zg1zvfz4; __cflb=02DiuFnsSsHWYH8WqVXbZzkeTrZ6gtmGUuxZNBWynJU3E'
    }
    conn.request("GET", url, '', headers)
    res = conn.getresponse()
    data = res.read()
    _html = data.decode("utf-8")
    return _html


def combine(a: 'Dict[str, Any]', b: 'Dict[str, Any]') -> Dict[str, Any]:
    print(f'[INFO] Merging results for Etherscan and BscScan')
    result: Dict[str, Any] = {}
    for i in a.keys():
        result[i] = {}
        for j in a[i].keys():
            result[i][j] = a[i][j]
        for j in b[i].keys():
            result[i][j] = b[i][j]
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
