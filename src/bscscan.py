from src import helpers as help
import concurrent.futures
from typing import Any, Dict
from bs4 import BeautifulSoup as soup

SOURCE = "bscscan.com"
URL = "/address/{0}"
BALANCE_SELECTOR = "#ContentPlaceHolder1_divSummary > div.row.mb-4 > div.col-md-6.mb-3.mb-md-0 > div > div.card-body > div:nth-child(1) > div.col-md-8"
TOKEN_SELECTOR = "li.list-custom"


def get_balance(address: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    print("[INFO] Processing from https://bscscan.com")

    result['BEP-20'] = {}
    result['BEP-others'] = {}
    result['BNB'] = "ERROR"
    _soup: soup = None

    i: int = 0
    while result['BNB'] == "ERROR":
        print(f'[INFO] Getting online data for {address}. Retried {i} times')
        _html = help.get(SOURCE, URL.format(address))
        _soup = soup(_html, 'lxml')

        eth_balance = _soup.select(BALANCE_SELECTOR)
        try:
            result['BNB'] = eth_balance[0].text.split()[0]
            print(f'[SUCCESS] Successfully gotten bnb balance for {address}')
        except IndexError:
            result['BNB'] = "ERROR"
            print(f'[WARNING] Unable to get bnb balance for {address}')
        pass
        i += 1

    try:
        result['BscScan total token balance'] = _soup.select(
            '#availableBalanceDropdown')[0].text.split()[0]
    except IndexError:
        result['BscScan total token balance'] = 0
        print(f'[WARNING] Unable to get total bnb token balance for {address}')
    pass

    tokens = _soup.select('li.list-custom')

    print(f'[INFO] Getting bnb token balance for {address}')
    for i in tokens:
        if 'list-custom-BEP-20' in i["class"]:
            try:
                token_name = i.select("a > div > div > span")[
                    0].text.strip()
                token_balance = i.select("a > div > span")[
                    0].text.split()[0]
                result['BEP-20'][token_name] = token_balance
                print(
                    f'[SUCCESS] Successfully gotten balance for BEP-20 token for {address}')
            except IndexError:
                print(
                    f'[WARNING] Unable to get balance for BEP-20 token for {address}')
                continue
        else:
            try:
                token_name = i.select("a > div > div > span")[
                    0].text.strip()
                token_balance = i.select("a > div > span")[
                    0].text.split()[0]
                result['BEP-others'][token_name] = token_balance
                print(
                    f'[SUCCESS] Successfully gotten bnb balance for token for {address}')
            except IndexError:
                print(
                    f'[WARNING] Unable to get bnb balance for token for {address}')
                continue

    return result
