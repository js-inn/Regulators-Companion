import os
import sqlite3
import json
import hashlib
from datetime import datetime

DB_NAME = 'wire_audit.db'
JSON_EXPORT = 'audit_snapshot.json'

def log_direct_octopus_transfer(source_ref, destination_node, amount_cents, currency="CAD"):
    timestamp = datetime.now().isoformat()
    
    # Raw payload for cryptographic anchoring
    raw_data = f"{source_ref}-{destination_node}-{amount_cents}-{currency}-{timestamp}"
    record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS direct_octopus_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ref TEXT,
            destination_node TEXT,
            amount INTEGER,
            currency TEXT,
            timestamp TEXT,
            record_hash TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO direct_octopus_ledger (source_ref, destination_node, amount, currency, timestamp, record_hash)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source_ref, destination_node, amount_cents, currency, timestamp, record_hash))
    conn.commit()
    
    # Export current ledger state to JSON
    cursor.execute('SELECT id, source_ref, destination_node, amount, currency, timestamp, record_hash FROM direct_octopus_ledger')
    rows = cursor.fetchall()
    conn.close()
    
    export_list = [{
        "id": r[0], "source_ref": r[1], "destination_node": r[2],
        "amount": r[3], "currency": r[4], "timestamp": r[5], "record_hash": r[6]
    } for r in rows]
    
    with open(JSON_EXPORT, 'w') as f:
        json.dump(export_list, f, indent=4)
        
    print(f"[+] Direct Octopus 2.0 Transfer Logged: {amount_cents} {currency}")
    print(f"[#] Anchor Hash: {record_hash}")

if __name__ == "__main__":
    log_direct_octopus_transfer(
        source_ref="Direct-Manual-Bypass",
        destination_node="Octopus-2.0-Core-Settlement",
        amount_cents=100000
    )

