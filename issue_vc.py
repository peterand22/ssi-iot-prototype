import json
from eth_account import Account
from eth_account.messages import encode_defunct
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

with open("issuer_identity.json") as f:
    issuer = json.load(f)

with open("pi_did.txt") as f:
    subject_did = f.read().strip()

current_time = datetime.now(ZoneInfo("Europe/Ljubljana")).isoformat(timespec="seconds")

vc = {
    "@context": ["https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"],
    "id": f"urn:uuid:{str(uuid.uuid4())}",
    "type": ["VerifiableCredential"],
    "issuer": issuer["did"],
    "validFrom": current_time,
    "credentialSubject": {
        "id": subject_did,
        "deviceModel": "Raspberry Pi 5",
        "serialNumber": "pi-12345678"
    }
}

vc_str = json.dumps(vc, separators=(",", ":"), ensure_ascii=False)
message = encode_defunct(text=vc_str)

signed = Account.sign_message(message, private_key=issuer["private_key"])

vc["proof"] = {
    "type": "DataIntegrityProof",
    "created": current_time,
    "verificationMethod": issuer["did"] + "#controller",
    "cryptosuite": "EcdsaSecp256k1RecoverySignature2020",
    "proofPurpose": "assertionMethod",
    "proofValue": signed.signature.hex()
}

with open("device_vc.json", "w") as f:
    json.dump(vc, f, indent=2)

print("VC issued and saved to device_vc.json")