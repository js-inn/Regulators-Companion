import xml.etree.ElementTree as ET
from datetime import datetime
import hashlib
import sqlite3
import os

def init_db():
    conn = sqlite3.connect('wire_audit.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msg_id TEXT,
            timestamp TEXT,
            amount TEXT,
            currency TEXT,
            debtor_account TEXT,
            payload_hash TEXT,
            xml_filename TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generate_iso20022_pacs008(amount, currency, debtor_name, debtor_account, creditor_name, creditor_iban, bic):
    document = ET.Element("Document", xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10")
    
    fi_to_fi_ctr = ET.SubElement(document, "FIToFIPmtCstmrCdtTrf")
    
    msg_id = f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cre_dt_tm = datetime.now().isoformat()
    
    grpHdr = ET.SubElement(fi_to_fi_ctr, "GrpHdr")
    ET.SubElement(grpHdr, "MsgId").text = msg_id
    ET.SubElement(grpHdr, "CreDtTm").text = cre_dt_tm
    ET.SubElement(grpHdr, "NbOfTxs").text = "1"
    
    cdtTrfTxInf = ET.SubElement(fi_to_fi_ctr, "CdtTrfTxInf")
    
    pmtId = ET.SubElement(cdtTrfTxInf, "PmtId")
    ET.SubElement(pmtId, "EndToEndId").text = f"E2E-{msg_id}"
    
    instdAmt = ET.SubElement(cdtTrfTxInf, "IntrBkSttlmAmt", Ccy=currency)
    instdAmt.text = f"{amount:.2f}"
    
    dbtr = ET.SubElement(cdtTrfTxInf, "Dbtr")
    ET.SubElement(dbtr, "Nm").text = debtor_name
    
    dbtrAcct = ET.SubElement(cdtTrfTxInf, "DbtrAcct")
    id_elem = ET.SubElement(dbtrAcct, "Id")
    ET.SubElement(id_elem, "Othr").text = debtor_account
    
    cdtr = ET.SubElement(cdtTrfTxInf, "Cdtr")
    ET.SubElement(cdtr, "Nm").text = creditor_name
    
    cdtrAcct = ET.SubElement(cdtTrfTxInf, "CdtrAcct")
    cdtr_id = ET.SubElement(cdtrAcct, "Id")
    ET.SubElement(cdtr_id, "IBAN").text = creditor_iban
    
    cdtrAgt = ET.SubElement(cdtTrfTxInf, "CdtrAgt")
    finInstnId = ET.SubElement(cdtrAgt, "FinInstnId")
    ET.SubElement(finInstnId, "BICFI").text = bic
    
    tree = ET.ElementTree(document)
    ET.indent(tree, space="    ")
    xml_string = ET.tostring(document, encoding="utf-8").decode("utf-8")
    
    return msg_id, cre_dt_tm, xml_string

if __name__ == "__main__":
    init_db()
    
    # Mapping your specified BMO details: Inst 001, Transit 00149, Account 1928-814
    bmo_account_string = "001-00149-1928-814"
    
    msg_id, timestamp, xml_payload = generate_iso20022_pacs008(
        amount=2500.00,
        currency="CAD",
        debtor_name="10839477 Canada Inc.",
        debtor_account=bmo_account_string,
        creditor_name="Verified Partner Entity",
        creditor_iban="CA12BMO001001491928814",
        bic="BOFMCAMTXXX"
    )
    
    # Generate cryptographic SHA-256 hash anchor of the payload
    payload_hash = hashlib.sha256(xml_payload.encode('utf-8')).hexdigest()
    
    filename = f"simulated_wire_{msg_id}.xml"
    with open(filename, "w") as f:
        f.write(xml_payload)
        
    # Log into SQLite database
    conn = sqlite3.connect('wire_audit.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (msg_id, timestamp, amount, currency, debtor_account, payload_hash, xml_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (msg_id, timestamp, "2500.00", "CAD", bmo_account_string, payload_hash, filename))
    conn.commit()
    conn.close()
    
    print("--- Updated ISO 20022 Simulation Payload ---")
    print(xml_payload)
    print(f"\n[+] Cryptographic SHA-256 Hash Anchor: {payload_hash}")
    print(f"[+] Payload saved to {filename}")
    print(f"[+] Logged successfully into local SQLite database: wire_audit.db")
