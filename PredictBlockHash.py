from web3 import Web3
from config import CONFIG
from solcx import compile_source
import time

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

contract_address = "0x0Ec5c9dbe1dB49f83500AcCdAF236a83c901A6cb"

with open('CTE_Contracts/PredictTheBlockHashChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_sol = compile_source(challenge_code, solc_version="0.4.21")

contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]

contract = w3.eth.contract(address=contract_address, abi=abi)


tx = contract.functions.lockInGuess(w3.toBytes(0)).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS"]),
    'value': w3.toWei(1, 'ether'),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})

signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY"])

tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

while True:

    time.sleep(60)

    try:
        tx_blocknumber = w3.eth.getTransaction(tx_hash)["blockNumber"]
        latest_blocknumber = w3.eth.blockNumber

        #https://blog.positive.com/predicting-random-numbers-in-ethereum-smart-contracts-e5358c6b8620?gi=83cdf37104c4
        #all blockhashes of blocks older than 256 blocks are 0
        if latest_blocknumber - tx_blocknumber > 256:
            tx = contract.functions.settle().buildTransaction({
                "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS"]),
                'gas': 3000000,
                'gasPrice': w3.toWei('5', 'gwei')
            })

            signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY"])
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(w3.toHex(tx_hash))
            break

    except Exception as e:
        continue