import sqlite3
import hmac
import hashlib
import json

SECRET_KEY = b"octopus_2.0_secure_master_key"

def verify_and_process_tap(raw_payload_json):
    try:
        data = json.loads(raw_payload_json)
        received_hmac = data.pop("hmac", "")
        
        # Re-calculate HMAC to verify card data integrity
        payload_string = json.dumps(data, sort_keys=True).encode('utf-8')
        calculated_hmac = hmac.new(SECRET_KEY, payload_string, hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(calculated_hmac, received_hmac):
            print("Security Alert: Invalid cryptographic signature on NFC tap!")
            return False
            
        # Log transaction to local SQLite ledger
        conn = sqlite3.connect("ledger.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                uuid TEXT PRIMARY KEY,
                amount REAL,
                timestamp TEXT,
                status TEXT
            )
        ''')
        
        cursor.execute("INSERT OR IGNORE INTO transactions VALUES (?, ?, ?, ?)",
                       (data["uuid"], data["amount"], data["timestamp"], "VERIFIED"))
        conn.commit()
        conn.close()
        
        print(f"Success: Processed NFC tap {data['uuid']} for amount {data['amount']}")
        return True
    except Exception as e:
        print(f"Error processing tap: {e}")
        return False

if __name__ == "__main__":
    # Test simulation with a sample payload
    import time, uuid
    sample_data = {
        "uuid": str(uuid.uuid4()),
        "amount": 10.50,
        "timestamp": str(time.time())
    }
    # Generate valid HMAC for test
    test_string = json.dumps(sample_data, sort_keys=True).encode('utf-8')
    sample_data["hmac"] = hmac.new(SECRET_KEY, test_string, hashlib.sha256).hexdigest()
    
    print("Testing NFC Bridge Handler...")
    verify_and_process_tap(json.dumps(sample_data))
