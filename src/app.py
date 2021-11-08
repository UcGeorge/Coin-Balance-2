from resources import etherscan, bscscan
from PyInquirer import prompt
from examples import custom_style_3
from resources.helpers import combine

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

    etherscan_results = etherscan.get_balance(address_list)
    bscscan_results = bscscan.get_balance(address_list)
    result = combine(etherscan_results, bscscan_results)
    print(result)
