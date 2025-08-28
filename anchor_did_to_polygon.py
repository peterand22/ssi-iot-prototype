from eth_account import Account
from web3 import Web3
import json

with open("issuer_identity.json") as f:
    identity = json.load(f)

eth_address = identity["eth_address"]
private_key = identity["private_key"]

with open("issuer_did_ipfs_cid.txt") as f:
    cid = f.read().strip()

w3 = Web3(Web3.HTTPProvider("https://polygon-amoy.infura.io/v3/######################"))

nonce = w3.eth.get_transaction_count(eth_address)
tx = {
    "nonce": nonce,
    "to": eth_address,
    "value": 0,
    "gas": 100000,
    "gasPrice": w3.to_wei("50", "gwei"),
    "chainId": 80002,
    "data": w3.to_hex(text=cid)
}

signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Anchored DID to Polygon Amoy")
print("Transaction Hash:", w3.to_hex(tx_hash))
