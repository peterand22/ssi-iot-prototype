from eth_account import Account
import json

acct = Account.create()
eth_address = acct.address
private_key = acct.key.hex()

chain_id = 800002
did = f"did:ethr:eip155:{chain_id}:{eth_address}"

identity = {
    "did": did,
    "eth_address": eth_address,
    "private_key": private_key
}

with open("issuer_identity.json", "w") as f:
    json.dump(identity, f, indent=2)

print("Issuer DID generated")
print("DID:", did)
