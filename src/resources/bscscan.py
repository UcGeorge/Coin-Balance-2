import os
import requests
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BSCSCAN_API_KEY')

API = "https://api.bscscan.com/api/"
GET_BALANCE_ENDPOINT = "?module=account\
&action=balancemulti\
&address={0}\
&tag=latest\
&apikey={1}"


def get_balance(addresses: str) -> Dict[str, Any]:

    url = API + GET_BALANCE_ENDPOINT.format(addresses, API_KEY)
    response = requests.request("GET", url, headers={}, data={})

    print(response.text)
