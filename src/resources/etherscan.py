from typing import Any, Dict
from bs4 import BeautifulSoup as soup
from resources import helpers as help
import concurrent.futures

SOURCE = "etherscan.io"
URL = "/address/{0}"
BALANCE_SELECTOR = "#ContentPlaceHolder1_divSummary > div.row.mb-4 > div.col-md-6.mb-3.mb-md-0 > div > div.card-body > div:nth-child(1) > div.col-md-8"
TOKEN_SELECTOR = "li.list-custom"


def get_balance(addresses: 'list[str]') -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    print("[INFO] Processing from https://etherscan.io")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for address in addresses:
            futures.append(executor.submit(process, address=address))
        for future in concurrent.futures.as_completed(futures):
            for x, y in future.result().items():
                result[x] = y
    return result


def process(address: str):
    result = {}
    result[address] = {}
    result[address]['Etherscan tokens'] = {}

    _html = help.get(SOURCE, URL.format(address))
    _soup = soup(_html, 'html.parser')

    eth_balance = _soup.select(BALANCE_SELECTOR)
    try:
        result[address]['ETH'] = eth_balance[0].text.split()[0]
    except IndexError:
        result[address]['ETH'] = 0
    pass

    tokens = _soup.select(TOKEN_SELECTOR)
    for i in tokens:
        try:
            token_name = i.select("a > div > div > span")[
                0].text.strip()
            token_balance = i.select("a > div > span")[
                0].text.split()[0]
            # print(f"\n{token_name} : {token_balance}")
        except IndexError:
            continue
        result[address]['Etherscan tokens'][token_name] = token_balance
    return result
