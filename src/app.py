from resources import etherscan, bscscan
from PyInquirer import prompt
from examples import custom_style_3

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
    address_list = open(input_file_location, "r").read().replace('\n\n', ',')
    etherscan.get_balance(address_list)
    bscscan.get_balance(address_list)
