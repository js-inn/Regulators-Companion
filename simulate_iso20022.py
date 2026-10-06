import xml.etree.ElementTree as ET
from datetime import datetime

def generate_iso20022_pacs008(amount, currency, debtor_name, debtor_account, creditor_name, creditor_iban, bic):
    # Root element for ISO 20022 pacs.008 (FI to FI Customer Credit Transfer)
    document = ET.Element("Document", xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10")
    
    fi_to_fi_ctr = ET.SubElement(document, "FIToFIPmtCstmrCdtTrf")
    
    # Group Header
    grpHdr = ET.SubElement(fi_to_fi_ctr, "GrpHdr")
    ET.SubElement(grpHdr, "MsgId").text = f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    ET.SubElement(grpHdr, "CreDtTm").text = datetime.now().isoformat()
    ET.SubElement(grpHdr, "NbOfTxs").text = "1"
    
    # Credit Transfer Transaction Information
    cdtTrfTxInf = ET.SubElement(fi_to_fi_ctr, "CdtTrfTxInf")
    
    # Instruction Identification
    pmtId = ET.SubElement(cdtTrfTxInf, "PmtId")
    ET.SubElement(pmtId, "EndToEndId").text = "E2E-SIM-2026-001"
    
    # Interbank Settlement Amount
    instdAmt = ET.SubElement(cdtTrfTxInf, "IntrBkSttlmAmt", Ccy=currency)
    instdAmt.text = f"{amount:.2f}"
    
    # Debtor (Sender - e.g., BMO Account details)
    dbtr = ET.SubElement(cdtTrfTxInf, "Dbtr")
    ET.SubElement(dbtr, "Nm").text = debtor_name
    
    dbtrAcct = ET.SubElement(cdtTrfTxInf, "DbtrAcct")
    id_elem = ET.SubElement(dbtrAcct, "Id")
    ET.SubElement(id_elem, "Othr").text = debtor_account
    
    # Creditor (Receiver)
    cdtr = ET.SubElement(cdtTrfTxInf, "Cdtr")
    ET.SubElement(cdtr, "Nm").text = creditor_name
    
    cdtrAcct = ET.SubElement(cdtTrfTxInf, "CdtrAcct")
    cdtr_id = ET.SubElement(cdtrAcct, "Id")
    ET.SubElement(cdtr_id, "IBAN").text = creditor_iban
    
    # Intermediary Agent / BIC
    cdtrAgt = ET.SubElement(cdtTrfTxInf, "CdtrAgt")
    finInstnId = ET.SubElement(cdtrAgt, "FinInstnId")
    ET.SubElement(finInstnId, "BICFI").text = bic
    
    # Return formatted XML string
    tree = ET.ElementTree(document)
    ET.indent(tree, space="    ")
    return ET.tostring(document, encoding="utf-8").decode("utf-8")

if __name__ == "__main__":
    # Example execution payload mapping your business parameters
    xml_payload = generate_iso20022_pacs008(
        amount=1500.00,
        currency="CAD",
        debtor_name="10839477 Canada Inc.",
        debtor_account="001-00149-1928814", # Institution-Transit-Account structure
        creditor_name="Verified Partner Entity",
        creditor_iban="CA12BMO0011928814XXXX",
        bic="BOFMCAMTXXX"
    )
    
    print("--- Generated ISO 20022 pacs.008 Simulation Payload ---")
    print(xml_payload)
    
    # Save to file for local test logging
    with open("simulated_wire_transfer.xml", "w") as f:
        f.write(xml_payload)
    print("\n[+] Payload successfully saved to simulated_wire_transfer.xml")
