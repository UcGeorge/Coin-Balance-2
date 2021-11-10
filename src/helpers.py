import cfscrape
from threading import Thread
from typing import Any, Dict


import http.client


def get(host: str, url: str) -> str:
    scraper = cfscrape.create_scraper()
    _html = scraper.get(f"https://{host+url}").content.decode('UTF-8')
    # ! file_name = (host+url).replace('/', '-')
    # ! with open(f'error/{file_name}.html', "w", encoding='utf-8') as out_file:
    # !     out_file.write(_html)
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
