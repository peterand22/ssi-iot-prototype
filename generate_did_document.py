import json

with open("issuer_identity.json") as f:
    identity = json.load(f)

did = identity["did"]
eth_address = identity["eth_address"]

did_document = {
    "@context": "https://www.w3.org/ns/did/v1",
    "id": did,
    "verificationMethod": [
        {
            "id": f"{did}#controller",
            "type": "EcdsaSecp256k1RecoveryMethod2020",
            "controller": did,
            "blockchainAccountId": f"{eth_address}@eip155:80002"
        }
    ],
    "authentication": [
        f"{did}#controller"
    ],
    "assertionMethod": [
        f"{did}#controller"
    ]
}

with open("issuer_did_document.json", "w") as f:
    json.dump(did_document, f, indent=2)

print("DID Document created: issuer_did_document.json")
