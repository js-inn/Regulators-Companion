import sqlite3
import json
from datetime import datetime, timezone

DB_NAME = "audit_ledger.db"

def log_registry_incident():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Create Discrepancy Table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registry_discrepancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            entity_name TEXT NOT NULL,
            corporation_number TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            description TEXT NOT NULL,
            verified_address TEXT NOT NULL,
            discrepancy_note TEXT NOT NULL
        )
    ''')
    
    # 2. Insert the Kitchener Vacant Lot / ISED Incident Record
    timestamp = datetime.now(timezone.utc).isoformat()
    cursor.execute('''
        INSERT INTO registry_discrepancies 
        (timestamp, entity_name, corporation_number, incident_type, description, verified_address, discrepancy_note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp,
        "10839477 Canada Inc.",
        "1083947-7",
        "Physical Key Mailing & Address Discrepancy",
        "ISED registry insisted on mailing corporate security key to a designated address in Kitchener, Ontario, refusing Edmonton, AB delivery.",
        "Kitchener Registry Address (Investigated)",
        "Physical inspection/mapping revealed the registered address maps to a vacant lot. Confirms institutional administrative unreliability and need for independent cryptographic asset anchoring."
    ))
    
    conn.commit()
    
    print("\n==================================================================")
    print("      OFFICIAL REGISTRY INCIDENT LOGGED TO SQLITE LEDGER          ")
    print("==================================================================")
    cursor.execute("SELECT id, timestamp, incident_type, discrepancy_note FROM registry_discrepancies")
    for row in cursor.fetchall():
        print(f"  * Incident ID: {row[0]}")
        print(f"  * Timestamp:   {row[1]}")
        print(f"  * Type:        {row[2]}")
        print(f"  * Note:        {row[3]}")
    print("==================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    log_registry_incident()
