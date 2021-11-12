from typing import Any, Dict
from bs4 import BeautifulSoup as soup
from src import helpers as help
import concurrent.futures
from dotenv import load_dotenv
import os

load_dotenv()

SOURCE = "api.ethplorer.io"
API_KEY = os.getenv('API_KEY')
URL = "/getAddressInfo/{0}?apiKey={1}"


def token_name(token: Dict[str, Any]) -> str:
    return f"{token['tokenInfo']['name']} ({token['tokenInfo']['symbol']})"


def token_balance(token: Dict[str, Any]) -> str:
    balance = token['rawBalance']
    return f"{balance[:-18]}.{balance[-18:]}" if len(balance) > 18 else f"0.{balance}"


def get_balance(address: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    print("[INFO] Processing from https://ethplorer.io")
    data = help.get(SOURCE, URL.format(address, API_KEY), True)

    result['ETH'] = data['ETH']['balance']
    try:
        result['ERC-20'] = {token_name(item): token_balance(item)
                            for item in data['tokens']}
    except KeyError:
        result['ERC-20'] = {}

    return result
