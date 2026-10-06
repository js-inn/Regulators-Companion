import sqlite3
import hashlib
from datetime import datetime

def update_record():
    conn = sqlite3.connect('wire_audit.db')
    cursor = conn.cursor()
    
    # Ensure table exists
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
    
    institution = "TD Bank / TD Direct Investing"
    event_type = "Treasury Deposit Withheld & Asset Isolation"
    amount = "5000000.00"
    currency = "CAD"
    status = "Withheld / Non-Transferable"
    timestamp = datetime.now().isoformat()
    details = "Treasury deposit visible in WebBroker portal but artificially isolated and blocked from external corporate movement."
    
    # Generate new SHA-256 anchor for the updated record
    raw_data = f"{institution}-{event_type}-{amount}-{currency}-{status}-{timestamp}"
    record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    
    # Insert the corrected record
    cursor.execute('''
        INSERT INTO institutional_friction (institution, event_type, amount, currency, status, timestamp, details, record_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (institution, event_type, amount, currency, status, timestamp, details, record_hash))
    
    conn.commit()
    conn.close()
    
    print(f"[+] Updated friction record logged for {institution}")
    print(f"    - Type: {event_type} | Amount: {amount} {currency}")
    print(f"    - Status: {status}")
    print(f"    - New SHA-256 Anchor: {record_hash}")

if __name__ == "__main__":
    update_record()
