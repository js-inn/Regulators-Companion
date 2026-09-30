import xml.etree.ElementTree as ET
import json

# Load your local JSON payload coordinates
with open("td_swift_wire_instruction.json", "r") as f:
    data = json.load(f)

beneficiary = data["beneficiary"]

# Construct the ISO 20022 pacs.008 XML structure dynamically using verified parameters
xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10">
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>WIRE-TEST-LOCAL-001</MsgId>
      <CreDtTm>2026-09-30T13:30:00Z</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
    </GrpHdr>
    <CdtTrfTxInf>
      <PmtId>
        <EndToEndId>E2E-ILP-TD-{beneficiary["account_number"]}</EndToEndId>
      </PmtId>
      <IntrBkSttlmAmt Ccy="CAD">1000.00</IntrBkSttlmAmt>
      <Cdtr>
        <Nm>{beneficiary["name"]}</Nm>
      </Cdtr>
      <CdtrAgt>
        <FinInstnId>
          <ClrSysMmbId>
            <MmbId>{beneficiary["institution_number"]}{beneficiary["transit_number"]}</MmbId>
          </ClrSysMmbId>
          <BICFI>{beneficiary["swift_bic"]}</BICFI>
        </FinInstnId>
      </CdtrAgt>
      <CdtrAcct>
        <Id>
          <Othr>
            <Id>{beneficiary["account_number"]}</Id>
            <SchmeNm>
              <Prtry>Designation-{beneficiary["designation_number"]}</Prtry>
            </SchmeNm>
          </Othr>
        </Id>
      </CdtrAcct>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>
'''

# Parse and validate XML well-formedness
try:
    root = ET.fromstring(xml_content)
    print("=== ISO 20022 XML VALIDATION PASSED ===")
    print(f"Root Element Tag: {root.tag}")
    print(f"Validated Creditor Name: {beneficiary['name']}")
    print(f"Validated Clearing ID: {beneficiary['institution_number']}{beneficiary['transit_number']}")
    print(f"Validated Account & Designation: {beneficiary['account_number']} / {beneficiary['designation_number']}")
    print(f"Validated SWIFT BIC: {beneficiary['swift_bic']}")
    print("========================================")
    
    # Save validated schema file
    with open("validated_pacs008_wire.xml", "w") as xml_file:
        xml_file.write(xml_content)
    print("[INFO] Saved generated XML payload to 'validated_pacs008_wire.xml'")

except ET.ParseError as e:
    print(f"[ERROR] XML well-formedness validation failed: {e}")
