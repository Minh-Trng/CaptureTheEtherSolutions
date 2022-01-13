from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CHALLENGE_CONTRACT_ADDRESS = "0xdC512b707D4C8CDA70Ab90427050E7FF4DAEcD86"

with open('CTE_Contracts/AssumeOwnershipChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_challenge_code = compile_source(challenge_code, solc_version="0.4.21")
compilation_output = compiled_challenge_code["<stdin>:AssumeOwnershipChallenge"]
challenge_contract_abi = compilation_output["abi"]
challenge_contract = w3.eth.contract(address=CHALLENGE_CONTRACT_ADDRESS, abi=challenge_contract_abi)

tx = challenge_contract.functions.AssumeOwmershipChallenge().buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tx = challenge_contract.functions.authenticate().buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

assert challenge_contract.functions.isComplete().call()
