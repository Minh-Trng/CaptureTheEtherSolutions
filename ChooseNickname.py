from web3 import Web3
from config import CONFIG

NEW_NAME = "minhtrng"

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

address = "0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee"
abi = ["function setNickname(bytes32 nickname) public"]
abi = '[{"constant":false,"inputs":[{"name":"nickname","type":"bytes32"}],"name":"setNickname","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"nicknameOf","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"}]'
contract = w3.eth.contract(address=address, abi=abi)

new_name_bytes = NEW_NAME.encode("utf-8")

tx = contract.functions.setNickname(new_name_bytes).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"])
})

signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])

result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)


