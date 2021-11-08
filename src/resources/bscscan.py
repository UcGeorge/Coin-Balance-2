from resources import helpers as help
from typing import Any, Dict
from tqdm import tqdm
from bs4 import BeautifulSoup as soup

SOURCE = "bscscan.com"
URL = "/address/{0}"
BALANCE_SELECTOR = "#ContentPlaceHolder1_divSummary > div.row.mb-4 > div.col-md-6.mb-3.mb-md-0 > div > div.card-body > div:nth-child(1) > div.col-md-8"
TOKEN_SELECTOR = "li.list-custom"


def get_balance(addresses: 'list[str]') -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    print("[INFO] Processing from https://bscscan.com")

    for i in tqdm(range(0, len(addresses))):
        address = addresses[i]
        result[address] = {}
        result[address]['BscScan tokens'] = {}

        _html = help.get(SOURCE, URL.format(address))
        _soup = soup(_html, 'html.parser')

        eth_balance = _soup.select(BALANCE_SELECTOR)
        try:
            result[address]['BNB'] = eth_balance[0].text.split()[0]
        except IndexError:
            result[address]['BNB'] = 0
        pass

        tokens = _soup.select(TOKEN_SELECTOR)
        for i in tokens:
            try:
                token_name = i.select("a > div > div > span")[0].text.strip()
                token_balance = i.select("a > div > span")[0].text.split()[0]
                # print(f"\n{token_name} : {token_balance}")
            except IndexError:
                continue
            result[address]['BscScan tokens'][token_name] = token_balance

    # print(result)
    return result
