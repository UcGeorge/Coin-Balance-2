from typing import Any, Dict
from bs4 import BeautifulSoup as soup
from src import helpers as help
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
    print(f'[INFO] Processing {address}')
    result = {}
    result[address] = {}
    result[address]['ERC-20'] = {}
    result[address]['ERC-others'] = {}
    result[address]['ETH'] = "ERROR"
    _soup: soup = None

    i: int = 0
    while result[address]['ETH'] == "ERROR":
        print(f'[INFO] Getting online data for {address}. Retried {i} times')
        _html = help.get(SOURCE, URL.format(address))
        _soup = soup(_html, 'lxml')

        eth_balance = _soup.select(BALANCE_SELECTOR)
        try:
            result[address]['ETH'] = eth_balance[0].text.split()[0]
            print(f'[SUCCESS] Successfully gotten balance for {address}')
        except IndexError:
            result[address]['ETH'] = "ERROR"
            print(f'[WARNING] Unable to get balance for {address}')
        pass
        i += 1

    try:
        result[address]['Etherscan total token balance'] = _soup.select(
            '#availableBalanceDropdown')[0].text.split()[0]
    except IndexError:
        result[address]['Etherscan total token balance'] = 0
        print(f'[WARNING] Unable to get total token balance for {address}')
    pass

    tokens = _soup.select('li.list-custom')

    print(f'[INFO] Getting token balance for {address}')
    for i in tokens:
        if 'list-custom-ERC20' in i["class"]:
            try:
                token_name = i.select("a > div > div > span")[
                    0].text.strip()
                token_balance = i.select("a > div > span")[
                    0].text.split()[0]
                result[address]['ERC-20'][token_name] = token_balance
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
                result[address]['ERC-others'][token_name] = token_balance
                print(
                    f'[SUCCESS] Successfully gotten balance for token for {address}')
            except IndexError:
                print(
                    f'[WARNING] Unable to get balance for token for {address}')
                continue

    return result
