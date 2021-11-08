import os
import requests
from typing import Any, Dict
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

API_KEY = os.getenv('ETHERSCAN_API_KEY')

API = "https://api.etherscan.io/api/"
GET_BALANCE_ENDPOINT = "?module=account\
&action=balance\
&address={0}\
&tag=latest\
&apikey=" + API_KEY
GET_TOKEN_BALANCE = "?module=account\
&action=tokenbalance\
&contractaddress={0}\
&address={1}\
&tag=latest\
&apikey=" + API_KEY


def get_balance(addresses: 'list[str]', tokens: 'Dict[str, list[Dict[str, str]]]') -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    print("[INFO] Processing from https://etherscan.io")

    for i in tqdm(range(0, len(addresses))):
        address = addresses[i]
        result[address] = {}
        url = API + GET_BALANCE_ENDPOINT.format(address)
        response = requests.request("GET", url, headers={}, data={})
        eth_balance = response.json()['result']
        result[address]['ETH'] = eth_balance

        for network in tokens.keys():
            result[address][network] = {}
            for token in tokens[network]:
                contract_address = token['contractAddress']
                url = API + GET_TOKEN_BALANCE.format(contract_address, address)
                response = requests.request("GET", url, headers={}, data={})
                token_balance = response.json()['result']
                result[address][network][token['contractName']
                                         ] = token_balance

    print(result)
    return result
