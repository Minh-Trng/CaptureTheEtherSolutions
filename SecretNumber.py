from web3 import Web3
from config import CONFIG

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

answer_hash = w3.toHex(0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365)

n = 0

while True:
    if w3.toHex(w3.keccak(n)) == answer_hash:
        print(f"Answer: {n}")
        break
    n += 1