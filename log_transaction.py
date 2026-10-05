import sqlite3
import datetime

def log_confirmation(confirmation_id, batch_filename, total_amount):
    conn = sqlite3.connect("td_audit_ledger.db")
    cursor = conn.cursor()
    
    # Ensure audit table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            confirmation_id TEXT,
            batch_filename TEXT,
            total_amount REAL,
            status TEXT
        )
    """)
    
    timestamp = datetime.datetime.now().isoformat()
    status = "EXECUTED_VIA_PORTAL"
    
    cursor.execute("""
        INSERT INTO transactions (timestamp, confirmation_id, batch_filename, total_amount, status)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, confirmation_id, batch_filename, total_amount, status))
    
    conn.commit()
    conn.close()
    print("-" * 45)
    print(f" [SUCCESS] Recorded Confirmation ID: {confirmation_id}")
    print(f"           File: {batch_filename} | Amount: ${total_amount:.2f}")
    print("           Ledger updated: td_audit_ledger.db")
    print("-" * 45)

if __name__ == "__main__":
    print("=== TD DISBURSEMENT AUDIT RECORDER ===")
    conf_id = input("Enter Bank Confirmation ID / Receipt Number: ").strip()
    if conf_id:
        log_confirmation(conf_id, "td_disbursement_cpa005.txt", 3000.00)
    else:
        print("[ERROR] Confirmation ID cannot be empty.")
