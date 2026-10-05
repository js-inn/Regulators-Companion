import json
import datetime
import sqlite3

# Load native EFT routing parameters
with open("td_eft_instruction.json", "r") as f:
    payload = json.load(f)

ben = payload["beneficiary"]

print("=== INITIATING DOMESTIC CANADIAN EFT DISPATCH ===")
print(f"Beneficiary: {ben['name']}")
print(f"Bank: {ben['bank_name']}")
print(f"Institution Code: {ben['institution_number']}")
print(f"Transit Number: {ben['transit_number']}")
print(f"Account Number: {ben['account_number']} (Designation: {ben['designation_number']})")
print("-------------------------------------------------")

# Generate local tracking reference for domestic batch
tracking_ref = "EFT-CAD-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Log directly to local SQLite audit ledger
conn = sqlite3.connect("td_audit_ledger.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS eft_dispatches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        institution TEXT,
        transit TEXT,
        account TEXT,
        designation TEXT,
        tracking_ref TEXT
    )
''')
cursor.execute('''
    INSERT INTO eft_dispatches (timestamp, institution, transit, account, designation, tracking_ref)
    VALUES (?, ?, ?, ?, ?, ?)
''', (datetime.datetime.now().isoformat(), ben['institution_number'], ben['transit_number'], ben['account_number'], ben['designation_number'], tracking_ref))
conn.commit()
conn.close()

print(f"[SUCCESS] EFT Payload compiled and logged locally.")
print(f"EFT Tracking Reference: {tracking_ref}")
print("=================================================")
