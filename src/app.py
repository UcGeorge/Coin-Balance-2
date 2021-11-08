from json.encoder import JSONEncoder
from resources import etherscan, bscscan
from PyInquirer import prompt
from examples import custom_style_3
from resources.helpers import combine, ThreadWithReturnValue
from threading import Thread
import time

ENCODING = "utf-8"
INPUT_FILE = 'input/input.txt'


def loading_indicator():
    while True:
        print(' . ')
        time.sleep(1)


if __name__ == '__main__':
    input('[PROMPT] Press enter to confirm input is at input/input.txt ')
    address_list = open(INPUT_FILE, "r").read().split('\n')

    etherscan_thread = ThreadWithReturnValue(
        target=etherscan.get_balance, args=(address_list,))
    bscscan_thread = ThreadWithReturnValue(
        target=bscscan.get_balance, args=(address_list,))

    start_time = time.time()
    etherscan_thread.start()
    bscscan_thread.start()

    Thread(target=loading_indicator, daemon=True).start()

    result = combine(etherscan_thread.join(), bscscan_thread.join())

    with open(f'output/output.json', "w", encoding=ENCODING) as out_file:
        out_file.write(JSONEncoder().encode(result))

    print(f"[INFO] Finished in {time.time() - start_time} seconds")
    print("[INFO] Results can be found in output/output.json")
