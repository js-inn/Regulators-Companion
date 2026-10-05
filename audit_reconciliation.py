import os
import sqlite3
import json
import hashlib
from datetime import datetime

DB_NAME = 'wire_audit.db'
JSON_EXPORT = 'audit_snapshot.json'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutional_friction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institution TEXT,
            event_type TEXT,
            amount TEXT,
            currency TEXT,
            status TEXT,
            timestamp TEXT,
            details TEXT,
            record_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_and_export(institution, event_type, amount, currency, status, details):
    init_db()
    timestamp = datetime.now().isoformat()
    
    # Generate cryptographic anchor
    raw_data = f"{institution}-{event_type}-{amount}-{currency}-{status}-{timestamp}-{details}"
    record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO institutional_friction (institution, event_type, amount, currency, status, timestamp, details, record_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (institution, event_type, amount, currency, status, timestamp, details, record_hash))
    conn.commit()
    
    # Export full audit trail to JSON for cross-reference
    cursor.execute('SELECT id, institution, event_type, amount, currency, status, timestamp, details, record_hash FROM institutional_friction')
    rows = cursor.fetchall()
    conn.close()
    
    audit_list = []
    for row in rows:
        audit_list.append({
            "id": row[0],
            "institution": row[1],
            "event_type": row[2],
            "amount": row[3],
            "currency": row[4],
            "status": row[5],
            "timestamp": row[6],
            "details": row[7],
            "record_hash": row[8]
        })
        
    with open(JSON_EXPORT, 'w') as f:
        json.dump(audit_list, f, indent=4)
        
    print(f"[+] Successfully logged record for {institution} and updated {JSON_EXPORT}")
    print(f"[#] SHA-256 Anchor: {record_hash}")

if __name__ == "__main__":
    log_and_export(
        institution="TD Bank",
        event_type="Treasury Deposit Dispute",
        amount="5000000",
        currency="CAD",
        status="Withheld / Active Friction",
        details="Statutory response timeline tracking under Bank Act."
    )

