
# ! from json.encoder import JSONEncoder
from typing import Any, Dict
from src import etherscan, bscscan
# ! from PyInquirer import prompt
# ! from examples import custom_style_3
from src.helpers import combine, ThreadWithReturnValue
# ! from threading import Thread
import time
from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = True if os.getenv('DEBUG') == 'True' else False


@app.route("/")
def index():
    return 'Hello World'


@app.route("/api/v1")
def process():
    try:
        addresses = request.form.get('addresses')
        return main(addresses)
    except:
        return open('error/etherscan.io-address-0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae.html', 'r').read()

# * COMMENTS IN RED REPRESENT PARTS OF THE CODE THAT WILL NOT BE NEEDED IN THE API VERSION

# ! ENCODING = "utf-8"
# ! INPUT_FILE = 'input/input.txt'


# ! def loading_indicator():
# !     while True:
# !         print(' . ')
# !         time.sleep(1)


def main(addresses: str) -> Dict[str, Any]:
    # ! input('[PROMPT] Press enter to confirm input is at input/input.txt ')
    address_list = addresses.split(',')

    etherscan_thread = ThreadWithReturnValue(
        target=etherscan.get_balance, args=(address_list,))
    bscscan_thread = ThreadWithReturnValue(
        target=bscscan.get_balance, args=(address_list,))

    start_time = time.time()
    etherscan_thread.start()
    bscscan_thread.start()

    # ! Thread(target=loading_indicator, daemon=True).start()

    result = combine(etherscan_thread.join(), bscscan_thread.join())
    result['address couunt'] = len(result.keys())

    # ! with open(f'output/output.json', "w", encoding=ENCODING) as out_file:
    # !    out_file.write(JSONEncoder().encode(result))

    print(f"[INFO] Finished in {time.time() - start_time} seconds")
    # ! print("[INFO] Results can be found in output/output.json")
    return result


# app.run()
