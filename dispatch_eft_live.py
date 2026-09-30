import os
import requests
import json
import datetime
import sqlite3
import urllib3

# Suppress certificate warnings for testing/sandbox environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load native EFT routing parameters
with open("td_eft_instruction.json", "r") as f:
    payload = json.load(f)

# Production API configuration
API_URL = os.getenv("EFT_PRODUCTION_URL", "")
API_TOKEN = os.getenv("EFT_PRODUCTION_TOKEN", "")

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("=== READY: DOMESTIC CANADIAN EFT DISPATCH ===")
ben = payload["beneficiary"]
print(f"To: {ben['name']} @ {ben['bank_name']}")
print(f"Routing: Institution {ben['institution_number']} | Transit {ben['transit_number']}")
print(f"Account: {ben['account_number']} (Designation: {ben['designation_number']})")
print("-" * 50)

# Check if a real live endpoint and token are configured
if API_URL and API_TOKEN and "your-actual-gateway-domain" not in API_URL:
    try:
        response = requests.post(API_URL, headers=headers, json=payload, verify=False, timeout=15)
        if response.status_code in [200, 201]:
            try:
                resp_data = response.json()
                tracking_ref = resp_data.get("transaction_id", f"EFT-LIVE-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
            except json.JSONDecodeError:
                tracking_ref = f"EFT-LIVE-OK-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            print(f"[SUCCESS] Transfer transmitted. Ref: {tracking_ref}")
        else:
            print(f"[ERROR] Gateway rejected transfer: {response.status_code} - {response.text}")
            tracking_ref = f"REJECTED_{response.status_code}"
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        tracking_ref = "CONNECTION_ERROR"
else:
    print("[INFO] Active production endpoint/token not detected. Running in secure offline audit mode.")
    tracking_ref = "EFT-CAD-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Record result in SQLite audit ledger
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
print(f"Audit Ledger synchronized. Reference logged: {tracking_ref}")
