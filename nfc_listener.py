import sqlite3
import datetime
import hashlib

def log_nfc_tap(card_uid, amount=1.0):
    conn = sqlite3.connect('ledger.db')
    cur = conn.cursor()
    
    # Ensure table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ilp_stream_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_uid TEXT,
            packet_index INTEGER,
            amount REAL,
            packet_auth TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            settled_externally INTEGER DEFAULT 0
        )
    ''')
    
    # Generate packet auth HMAC/hash
    ts = datetime.datetime.now().isoformat()
    raw_data = f"{card_uid}-{amount}-{ts}"
    packet_auth = hashlib.sha256(raw_data.encode()).hexdigest()
    
    # Get next packet index
    cur.execute("SELECT MAX(packet_index) FROM ilp_stream_ledger WHERE card_uid = ?", (card_uid,))
    res = cur.fetchone()
    packet_index = (res[0] + 1) if res and res[0] is not None else 1
    
    # Insert new tap
    cur.execute("""
        INSERT INTO ilp_stream_ledger (card_uid, packet_index, amount, packet_auth, timestamp, settled_externally)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (card_uid, packet_index, amount, packet_auth, ts, 1))
    
    conn.commit()
    conn.close()
    print(f"[NFC TAPPED] Card: {card_uid} | Amount: ${amount} | Auth: {packet_auth[:12]}...")

if __name__ == "__main__":
    # Test a physical BMO card tap log
    log_nfc_tap("BMO_CARD_PHYSICAL", 1.0)
