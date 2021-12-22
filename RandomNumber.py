from web3 import Web3
from config import CONFIG

w3 = Web3(Web3.HTTPProvider(CONFIG["INFURA_URL_ROPSTEN"]))

CONTRACT_CREATION_BLOCKNUMBER = 11660382

block = w3.eth.getBlock(CONTRACT_CREATION_BLOCKNUMBER)
prev_block = w3.eth.getBlock(CONTRACT_CREATION_BLOCKNUMBER - 1)

keccak_hash = Web3.solidityKeccak(["uint256", "uint256"], [w3.toInt(prev_block.hash), block.timestamp])

last_byte = keccak_hash[-1] #conversion to uint8

print(last_byte)



