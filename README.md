# SSI-IoT Prototip

Ta repozitorij vsebuje prototipno implementacijo za **Self-Sovereign Identity (SSI) v IoT**, ki prikazuje proces:  
- ustvarjanja decentraliziranih identifikatorjev (DID),
- sidranja DID dokumentov v IPFS in Polygon,
- izdaje preverljivih poverilnic (VC),    
- avtentikacije z uporabo resolucije DID dokumenta.  

Projekt je bil razvit v okviru diplomske naloge na temo **Decentralizirane identitete v
Internetu stvari: prototip z avtentikacijo in sidranjem na verigo blokov**.

---

## Pregled datotek

- **generate_issuer_did.py**  
  Ustvari Ethereum ključne pare in oblikuje DID za izdajatelja/imetnika.

- **generate_did_document.py**  
  Oblikuje DID dokument na osnovi ustvarjenih ključev.

- **upload_did_to_ipfs.py**  
  Objavi DID dokument na IPFS in vrne CID.

- **anchor_did_to_polygon.py**  
  Sidra CID na verigo Polygon.

- **authentication.py**  
  Izvede resolucijo DID dokumenta in lokalno avtentikacijo podpisa.

---

## Opombe

- Gre za prototip, ki ni namenjen produkcijski uporabi.  
- Implementacija je namenjena prikazu koncepta delovanja decentralizirane identitete in lokalne avtentikacije v IoT.  
- Podrobnejša razlaga je predstavljena v diplomski nalogi.  
