import cfscrape
from threading import Thread
from typing import Any, Dict
from requests import Request


import http.client
from bs4 import BeautifulSoup as soup

BALANCE_SELECTOR = "#ContentPlaceHolder1_divSummary > div.row.mb-4 > div.col-md-6.mb-3.mb-md-0 > div > div.card-body > div:nth-child(1) > div.col-md-8"


def get(host: str, url: str, error: bool = False) -> str:
    if error:
        print(f'[INFO] Getting online data in IUAM for {url}')
        token, agent = cfscrape.get_tokens(
            f"https://{host+url}", 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        request = Request(url=f"https://{host+url}", cookies=token, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
        _html = request.data
        _soup = soup(_html, 'lxml')
        eth_balance = _soup.select(BALANCE_SELECTOR)
        try:
            _ = eth_balance[0].text.split()[0]
            return _html
        except IndexError:
            # writeToFile(host+url, 'html', 'error', _html)
            get(host, url, True)
    else:
        print(f'[INFO] Getting online data in NORMAL MODE for {url}')
        scraper = cfscrape.create_scraper()
        _html = scraper.get(f"https://{host+url}").content.decode('UTF-8')
        _soup = soup(_html, 'lxml')
        eth_balance = _soup.select(BALANCE_SELECTOR)
        try:
            _ = eth_balance[0].text.split()[0]
            return _html
        except IndexError:
            # writeToFile(host+url, 'html', 'error', _html)
            get(host, url, True)


def writeToFile(fileName: str, type: str, folder: str, content):
    with open(f'{folder}/{fileName}.{type}', "w", encoding='utf-8') as out_file:
        out_file.write(content)


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
