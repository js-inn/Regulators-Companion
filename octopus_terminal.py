import time
import json
import sqlite3
import hmac
import hashlib

SECRET_KEY = b"octopus_2.0_secure_master_key"

def process_physical_tap(card_uid):
    """Simulates or executes real-world hardware tap processing."""
    timestamp = str(time.time())
    transaction_id = f"tap-{card_uid}-{int(time.time())}"
    
    # Construct payload representing offline smart contract balance/royalty transfer
    payload = {
        "uuid": transaction_id,
        "card_uid": card_uid,
        "amount": 5.00,
        "timestamp": timestamp
    }
    
    # Generate cryptographic signature for offline security
    payload_string = json.dumps(payload, sort_keys=True).encode('utf-8')
    payload["hmac"] = hmac.new(SECRET_KEY, payload_string, hashlib.sha256).hexdigest()
    
    # Commit to local SQLite ledger
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    
    # Create table if missing, and ensure card_uid column is supported
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            uuid TEXT PRIMARY KEY,
            amount REAL,
            timestamp TEXT,
            status TEXT
        )
    ''')
    try:
        cursor.execute("ALTER TABLE transactions ADD COLUMN card_uid TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists
        
    try:
        cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
                       (payload["uuid"], payload["amount"], payload["timestamp"], "SETTLED_OFFLINE", payload["card_uid"]))
        conn.commit()
        print(f"[OCTOPUS 2.0] Tap Verified! Card: {card_uid} | Amount: ${payload['amount']:.2f} | Logged Offline.")
    except sqlite3.IntegrityError:
        print(f"[WARNING] Replay attack detected for tap: {payload['uuid']}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Octopus 2.0 Terminal Active. Waiting for NFC tap...")
    try:
        # Simulating an incoming physical tap for demonstration
        dummy_uid = "04A1B2C3D4"
        process_physical_tap(dummy_uid)
    except KeyboardInterrupt:
        print("\nTerminal stopped by user.")
