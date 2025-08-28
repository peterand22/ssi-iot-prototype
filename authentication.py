import json, requests, re
from eth_account import Account
from eth_account.messages import encode_defunct

# Etherscan API key
ETHERSCAN_KEY = "###########################"

# Lokalni seznam izdajateljev ki jim zaupamo
TRUSTED_ISSUERS = {
    "did:ethr:eip155:80002:0x6feD556f71897aB2300F1f5f81c15A24226cC7e7": {
        "name": "Mac Laptop - Peter",
        "role": "Authorized issuer",
    }
}

# Funkcija ki najde CID na blockchainu
def get_cid(address):
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": "80002",
        "module": "account", 
        "action": "txlist",
        "address": address,
        "sort": "desc",
        "apikey": ETHERSCAN_KEY
    }
    
    cid_pattern = re.compile(r'Qm[1-9A-HJ-NP-Za-km-z]{44}')

    response = requests.get(url, params=params)
    data = response.json()
    
    for tx in data["result"]:
        if tx["from"].lower() == address.lower():
            input_data = tx["input"]
            if input_data != "0x":
                decoded = bytes.fromhex(input_data[2:]).decode("utf-8", errors="ignore")
                match = cid_pattern.search(decoded)
                if match:
                    return match.group(0)

    return None

# Funkcija ki pridobi DID dokument iz IPFS
def get_did_doc(cid):
    r = requests.get(f"https://gateway.pinata.cloud/ipfs/{cid}")
    return r.json()

def verify_vc():
    
    # Nalozimo VC in preberemo osnovne podatke
    with open("device_vc.json") as file:
        vc = json.load(file)

    proof = vc["proof"]
    issuer_did  = vc["issuer"]
    issuer_addr = issuer_did.split(":")[-1].lower()
    proof_key_id = proof["verificationMethod"]
    valid_from = vc["validFrom"]

    holder_info   = vc["credentialSubject"]
    device_model  = holder_info.get("deviceModel", "Unknown")
    serial_number = holder_info.get("serialNumber", "Unknown")

    print(f"Device: {device_model}, {serial_number}")
    print(f"Issuer: {issuer_did}")
    print(f"Valid From: {valid_from}")

    # Lokalno preverjanje iz seznama zaupanja vrednih izdajateljev 
    if issuer_did in TRUSTED_ISSUERS:
        print(f"Trusted issuer: {TRUSTED_ISSUERS[issuer_did]['name']}")
    else:
        print("Issuer: Unknown issuer")

    # Klic funkcije, ki pridobi CID
    cid = get_cid(issuer_addr)
    if not cid:
        print("Couldnt get CID")
        return False
    print(f"CID: {cid}")

    # Klic funkcije, ki pridobi DID dokument
    did_doc = get_did_doc(cid)
    if not did_doc:
        print("Couldnt get DID document")
        return False

    # Preberemo metodo avtentikacije iz DID dokumenta izdajatelja
    verification_method = did_doc["verificationMethod"][0]

    # Preverimo ali je ista metoda navedena v VC
    if proof_key_id != verification_method["id"]:
        print("Proof references unknown verification method.")
        return False

    # Preverimo ali je ista metoda pooblascena za izdajo VC
    if proof_key_id != did_doc["assertionMethod"][0]:
        print("Verification method is not authorised for assertionMethod.")
        return False

    # 4. Razdelek verifikacije podpisa
    method_type = verification_method["type"]
    if method_type == "EcdsaSecp256k1RecoveryMethod2020":
        blockchain_account = verification_method["blockchainAccountId"]
        expected_addr = blockchain_account.split("@")[0].lower()

        vc_copy = vc.copy()
        vc_copy.pop("proof", None)
        vc_data = json.dumps(vc_copy, separators=(",", ":"))
        msg = encode_defunct(text=vc_data)
        signature = proof["proofValue"]

        try:
            recovered = Account.recover_message(msg, signature=signature)
        except:
            recovered = None

        if recovered and recovered.lower() == expected_addr:
            print("Authentication successful")
            return True

        print("Authentication failed")
        return False

if __name__ == "__main__":
    verify_vc()