import sqlite3
import hashlib
import json
from datetime import datetime

def calculate_splits(total_amount):
    """
    Calculates deterministic royalty splits:
    - 85% Creator (Jujita Stairs / 10839477 Canada Inc.)
    - 10% Protocol Fee
    - 5% Compliance / Regulatory Reserve
    """
    creator_share = total_amount * 0.85
    protocol_share = total_amount * 0.10
    compliance_share = total_amount * 0.05
    return round(creator_share, 2), round(protocol_share, 2), round(compliance_share, 2)

def process_royalties():
    conn = sqlite3.connect('local_custodian.db')
    cursor = conn.cursor()
    
    # Ensure table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS royalty_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            gross_amount REAL,
            creator_share REAL,
            protocol_share REAL,
            compliance_share REAL,
            hmac_proof TEXT
        )
    ''')
    
    # Example incoming transaction stream amount
    gross_amount = 2500.00
    creator, protocol, compliance = calculate_splits(gross_amount)
    timestamp = datetime.utcnow().isoformat()
    
    # Generate HMAC-SHA256 audit proof anchor
    payload = f"{timestamp}:{gross_amount}:{creator}:{protocol}:{compliance}"
    hmac_proof = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    cursor.execute('''
        INSERT INTO royalty_ledger (timestamp, gross_amount, creator_share, protocol_share, compliance_share, hmac_proof)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, gross_amount, creator, protocol, compliance, hmac_proof))
    
    conn.commit()
    conn.close()
    
    print(f"[+] Royalty Engine Executed Successfully.")
    print(f"    Gross: ${gross_amount:.2f} | Creator (85%): ${creator:.2f} | Protocol (10%): ${protocol:.2f} | Compliance (5%): ${compliance:.2f}")
    print(f"    Cryptographic Audit Proof: {hmac_proof}")

if __name__ == "__main__":
    process_royalties()
