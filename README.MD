# Coin-Balance 2
 A python script to check the balances of a set of wallets from [etherscan.io](http://etherscan.io) and [bscscan.com](http://bscscan.com)

 ## Running the script

 > NOTE: Python must be installed on the target machine for the script to run.

 To run the script, execute `run.bat`. This would first install all dependencies before running `main.py`<br>
 Dependencies include:
 - python-dotenv

You will be asked to specify the path to your input file. The input file should be a text `(*.txt)` file in the format where each line represents a seperate wallet address;
```txt
0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae

0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae

0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae

0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae

...
```

## Results

After the script is done, you can find the results in the output folder in the project root folder: `C:...\Coin Balance 2\output\`

A result file name is in the format: `YY-MM-DD HH-MM-SS-MS.txt`
<BR>Eg. `2021-09-15 23-31-39.763795.txt`

Results are in the format:
```txt
[WALLET ADDRESS]
ECR20 ['$ WETH', '$ AXS']
ECR721['$ Axie', '$ Land Plot', '$ Land Item']
```
    