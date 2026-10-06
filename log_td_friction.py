import sqlite3
import hashlib
from datetime import datetime

def log_td_event():
    conn = sqlite3.connect('wire_audit.db')
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
    
    institution = "TD Bank / TD Direct Investing"
    event_type = "Withheld Capital & Coerced Service Fee Demand"
    amount = "5000000.00"
    currency = "CAD"
    status = "Withheld / Fee Coercion Active"
    timestamp = datetime.now().isoformat()
    details = "5,000,000 CAD treasury deposit isolated and restricted from movement, while portal prompts demand payment of outstanding service charges."
    
    raw_data = f"{institution}-{event_type}-{amount}-{currency}-{status}-{timestamp}-{details}"
    record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    
    cursor.execute('''
        INSERT INTO institutional_friction (institution, event_type, amount, currency, status, timestamp, details, record_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (institution, event_type, amount, currency, status, timestamp, details, record_hash))
    
    conn.commit()
    conn.close()
    
    print(f"[+] Logged escalated friction event for {institution}")
    print(f"    - Amount Withheld: {amount} {currency}")
    print(f"    - Condition: {status}")
    print(f"    - Details: {details}")
    print(f"    - SHA-256 Anchor: {record_hash}")

if __name__ == "__main__":
    log_td_event()
