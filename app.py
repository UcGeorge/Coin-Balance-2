
from typing import Any, Dict
from src import etherscan, bscscan
from src.helpers import combine, ThreadWithReturnValue
import time
from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DEBUG = True if os.getenv('DEBUG') == 'True' else False
app.config['DEBUG'] = DEBUG


@app.route("/")
def index():
    return 'Hello World'


@app.route("/api/v1")
def process():
    if DEBUG:
        print('[DEBUG]')
        address = request.form.get('address')
        return main(address)
    else:
        try:
            address = request.form.get('address')
            return main(address)
        except:
            return 'An error occoured'

# * COMMENTS IN RED REPRESENT PARTS OF THE CODE THAT WILL NOT BE NEEDED IN THE API VERSION


def main(address: str) -> Dict[str, Any]:
    start_time = time.time()

    eth = etherscan.get_balance(address)
    bnb = bscscan.get_balance(address)

    result = combine(eth, bnb, address)

    print(f"[INFO] Finished in {time.time() - start_time} seconds")
    return result
