import sqlite3
import datetime

def log_wire_transaction(reference_id, swift_bic, amount):
    conn = sqlite3.connect("td_audit_ledger.db")
    cursor = conn.cursor()
    
    # Ensure wire tracking table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wire_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            reference_id TEXT,
            swift_bic TEXT,
            amount REAL,
            status TEXT
        )
    """)
    
    timestamp = datetime.datetime.now().isoformat()
    status = "SWIFT_INSTRUCTION_STAGED"
    
    cursor.execute("""
        INSERT INTO wire_transactions (timestamp, reference_id, swift_bic, amount, status)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, reference_id, swift_bic, amount, status))
    
    conn.commit()
    conn.close()
    print("-" * 45)
    print(f" [SUCCESS] Logged Wire Reference: {reference_id}")
    print(f"           SWIFT BIC: {swift_bic} | Amount: ${amount:.2f}")
    print("           Ledger updated: td_audit_ledger.db")
    print("-" * 45)

if __name__ == "__main__":
    print("=== SWIFT WIRE AUDIT RECORDER ===")
    ref_id = input("Enter Wire Reference / Tranche ID: ").strip()
    if ref_id:
        log_wire_transaction(ref_id, "TDOMCATTTOR", 3000.00)
    else:
        print("[ERROR] Reference ID cannot be empty.")
