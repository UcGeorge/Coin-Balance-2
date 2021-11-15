from json.encoder import JSONEncoder
from json.decoder import JSONDecoder
import time
from tqdm import tqdm
import requests

ENCODING = "utf-8"
INPUT_FILE = 'input/input.txt'


def get(address: str):
    url = "https://coin-balance-2.herokuapp.com/api/v1"

    payload = {'address': address}

    response = requests.request(
        "GET", url, headers={}, data=payload, files=[])

    return JSONDecoder().decode(response.text)[address]


if __name__ == '__main__':
    result = {}
    input(f'[PROMPT] Press enter to confirm input is at {INPUT_FILE} ')
    address_list = open(INPUT_FILE, "r").read(
    ).strip().replace(" ", '').split('\n')

    start_time = time.time()
    for i in tqdm(range(len(address_list))):
        address = address_list[i]
        result[address] = get(address)
        time.sleep(1)

    with open(f'output/output.json', "w", encoding=ENCODING) as out_file:
        out_file.write(JSONEncoder().encode(result))

    print(f"[INFO] Finished in {time.time() - start_time} seconds")
    print("[INFO] Results can be found in output/output.json")
