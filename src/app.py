from resources import etherscan, bscscan
import json
from PyInquirer import prompt
from examples import custom_style_3

TOKEN_FILE = "input/tokens.json"
TOKENS = json.loads(open(TOKEN_FILE, "r").read())

if __name__ == '__main__':
    q_table = [
        {
            'type': 'input',
            'qmark': '[?]',
            'name': 'input',
            'message': 'Enter location of input file'
        }
    ]
    user_config = prompt(q_table, style=custom_style_3)
    input_file_location = user_config['input']
    address_list = open(input_file_location, "r").read().split('\n\n')

    etherscan_results = etherscan.get_balance(
        address_list, TOKENS['etherscan'])
    bscscan_results = bscscan.get_balance(address_list, TOKENS['bscscan'])
