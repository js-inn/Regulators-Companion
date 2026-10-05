import sqlite3
import json
import datetime
import os

# Database file path
DB_NAME = "td_audit_ledger.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wire_dispatches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            beneficiary_name TEXT NOT NULL,
            institution_number TEXT NOT NULL,
            transit_number TEXT NOT NULL,
            account_number TEXT NOT NULL,
            designation_number TEXT NOT NULL,
            swift_bic TEXT NOT NULL,
            tracking_reference TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_dispatch():
    # Load the verified routing payload
    with open("td_swift_wire_instruction.json", "r") as f:
        payload = json.load(f)
    
    beneficiary = payload["beneficiary"]
    timestamp = datetime.datetime.now().isoformat()
    tracking_ref = f"WIRE-2026-0930-{datetime.datetime.now().strftime('%H%M%S')}"
    status = "RECORDED_ZERO_AMBIGUITY"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO wire_dispatches (
            timestamp, beneficiary_name, institution_number, transit_number, 
            account_number, designation_number, swift_bic, tracking_reference, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp,
        beneficiary["name"],
        beneficiary["institution_number"],
        beneficiary["transit_number"],
        beneficiary["account_number"],
        beneficiary["designation_number"],
        beneficiary["swift_bic"],
        tracking_ref,
        status
    ))
    
    conn.commit()
    conn.close()
    
    print("=== SQLITE AUDIT LEDGER UPDATED ===")
    print(f"Database: {DB_NAME}")
    print(f"Logged Tracking Reference: {tracking_ref}")
    print(f"Status: {status}")
    print("===================================")

if __name__ == "__main__":
    init_db()
    log_dispatch()
