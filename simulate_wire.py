import json
from datetime import datetime, timezone
import os

LEDGER_FILE = "wire_ledger.json"

def create_wire_record(reference_id, amount, currency, sender_corp, recipient, message_type):
    record = {
        "schema_version": "1.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "corporate_issuer": sender_corp,
        "message_metadata": {
            "message_type": message_type,
            "reference_id": reference_id,
            "routing_state": "LOCAL_SIMULATION_PENDING"
        },
        "transaction_details": {
            "amount": amount,
            "currency": currency,
            "recipient": recipient
        },
        "cryptographic_anchor": {
            "creator_uuid": "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a",
            "anchor_uuid": "3d9f8a21-c5e7-4b6a-9128-f0d3e2a1b9c7"
        }
    }
    
    # Load ledger safely, ensuring it's a list to prevent AttributeError
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                ledger = json.load(f)
                if not isinstance(ledger, list):
                    ledger = []
        except json.JSONDecodeError:
            ledger = []
    else:
        ledger = []
        
    ledger.append(record)
    
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)
        
    print(f"[SUCCESS] Wire payload logged to {LEDGER_FILE}")

if __name__ == "__main__":
    create_wire_record("REF-2026-1006", 150000.00, "CAD", "10839477 Canada Inc.", "Receiver Bank Corp", "pacs.008")
