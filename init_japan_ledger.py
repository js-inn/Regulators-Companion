import sqlite3

DB_NAME = "audit_ledger.db"

def setup_japan_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Table for tracking Zengin routing and settlement rails
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zengin_settlement_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_ref TEXT UNIQUE NOT NULL,
            clearing_rail TEXT DEFAULT 'Zengin-Net',
            settlement_destination TEXT,
            amount_jpy REAL,
            zendi_metadata_attached BOOLEAN,
            settled_via_boj BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Table for tracking cross-border IP monetization & tax characterization
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_monetization_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_identifier TEXT NOT NULL,
            characterization_type TEXT CHECK(characterization_type IN ('Royalty', 'Sold-As-Is')),
            statutory_withholding_rate REAL DEFAULT 20.42,
            treaty_applied TEXT,
            treaty_reduced_rate REAL,
            form_17_filed BOOLEAN,
            compliance_status TEXT
        )
    ''')
    
    # Insert baseline structural records for evaluation
    cursor.execute('''
        INSERT OR IGNORE INTO ip_monetization_rules 
        (asset_identifier, characterization_type, statutory_withholding_rate, treaty_applied, treaty_reduced_rate, form_17_filed, compliance_status)
        VALUES 
        ('Jujita-Stairs-IP-Core', 'Royalty', 20.42, 'Canada-Japan Treaty', 0.00, 1, 'Exempt via Treaty Relief'),
        ('Standard-Off-The-Shelf-Artifact', 'Sold-As-Is', 0.00, 'N/A', 0.00, 0, 'Commercial Business Profit')
    ''')
    
    conn.commit()
    conn.close()
    print("[+] Japan banking pipeline and IP monetization tables successfully vaulted into audit_ledger.db!")

if __name__ == "__main__":
    setup_japan_ledger()
