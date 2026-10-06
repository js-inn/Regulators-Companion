import sqlite3
import hashlib
from datetime import datetime

def init_friction_db():
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
    conn.commit()
    conn.close()

def log_friction(institution, event_type, amount, currency, status, details):
    init_friction_db()
    timestamp = datetime.now().isoformat()
    
    # Create a unique data string to cryptographically anchor this specific dispute event
    raw_data = f"{institution}-{event_type}-{amount}-{currency}-{status}-{timestamp}"
    record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    
    conn = sqlite3.connect('wire_audit.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO institutional_friction (institution, event_type, amount, currency, status, timestamp, details, record_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (institution, event_type, amount, currency, status, timestamp, details, record_hash))
    conn.commit()
    conn.close()
    
    print(f"[+] Logged friction event for {institution}")
    print(f"    - Type: {event_type} | Amount: {amount} {currency}")
    print(f"    - Status: {status}")
    print(f"    - SHA-256 Anchor: {record_hash}")

if __name__ == "__main__":
    # Logging the TD Bank treasury deposit withhold & isolated broker capital event
    log_friction(
        institution="TD Bank / TD Direct Investing",
        event_type="Treasury Deposit Withheld & Asset Isolation",
        amount="150000.00", # Update with your specific withheld amount if needed
        currency="CAD",
        status="Withheld / Non-Transferable",
        details="Treasury deposit visible in WebBroker portal but artificially isolated and blocked from external corporate movement."
    )
