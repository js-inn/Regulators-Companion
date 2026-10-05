import os
import sqlite3
import json
import hashlib
import sys
from datetime import datetime

DB_NAME = 'wire_audit.db'
JSON_EXPORT = 'audit_snapshot.json'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmo_octopus_reconciliation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bmo_reference TEXT,
            octopus_node TEXT,
            amount_cents INTEGER,
            currency TEXT,
            status TEXT,
            timestamp TEXT,
            record_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def ingest_bmo_transaction(bmo_ref, amount_cents, currency="CAD", status="Reconciled"):
    init_db()
    timestamp = datetime.now().isoformat()
    octopus_node = "Octopus-2.0-Core-Settlement"
    
    # Cryptographic anchoring for the BMO-to-Octopus bridge
    raw_data = f"{bmo_ref}-{octopus_node}-{amount_cents}-{currency}-{status}-{timestamp}"
    record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bmo_octopus_reconciliation (bmo_reference, octopus_node, amount_cents, currency, status, timestamp, record_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (bmo_ref, octopus_node, amount_cents, currency, status, timestamp, record_hash))
    conn.commit()
    
    # Export full reconciliation state to JSON snapshot
    cursor.execute('SELECT id, bmo_reference, octopus_node, amount_cents, currency, status, timestamp, record_hash FROM bmo_octopus_reconciliation')
    rows = cursor.fetchall()
    conn.close()
    
    export_list = [{
        "id": r[0], "bmo_reference": r[1], "octopus_node": r[2],
        "amount_cents": r[3], "currency": r[4], "status": r[5],
        "timestamp": r[6], "record_hash": r[7]
    } for r in rows]
    
    with open(JSON_EXPORT, 'w') as f:
        json.dump(export_list, f, indent=4)
        
    print(f"[+] BMO Transaction Ingested [Ref: {bmo_ref}] -> Octopus 2.0 Tied")
    print(f"[#] Cryptographic Hash Anchor: {record_hash}")

if __name__ == "__main__":
    # Accept BMO reference ID and amount from command line, or use a default test payload
    bmo_ref = sys.argv[1] if len(sys.argv) > 1 else "BMO-TXN-2026-001"
    amount_cents = int(sys.argv[2]) if len(sys.argv) > 2 else 500000
    
    ingest_bmo_transaction(bmo_ref=bmo_ref, amount_cents=amount_cents)

