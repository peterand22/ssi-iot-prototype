import json
import requests

PINATA_API_KEY = "Your API Key"
PINATA_SECRET_KEY = "Your Secret Key"

with open("issuer_did_document.json", "rb") as file:
    files = {
        "file": ("issuer_did_document.json", file)
    }

    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY
    }

    response = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files=files,
        headers=headers
    )

    ipfs_hash = response.json()["IpfsHash"]
    print("Successfully uploaded to IPFS via Pinata")
    print("CID:", ipfs_hash)

    with open("issuer_did_ipfs_cid.txt", "w") as out:
        out.write(ipfs_hash)