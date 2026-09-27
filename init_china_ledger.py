import sqlite3

DB_NAME = "audit_ledger.db"

def setup_china_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Table for tracking CIPS/CNAPS settlement nodes and routing codes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS china_settlement_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_ref TEXT UNIQUE NOT NULL,
            clearing_rail TEXT CHECK(clearing_rail IN ('CIPS', 'CNAPS')),
            cnaps_bank_code TEXT,
            amount_cny REAL,
            iso20022_compliant BOOLEAN,
            settled_via_pboc BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Table for tracking PRC cross-border IP licensing, withholding tax, and VAT
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS china_ip_tax_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_identifier TEXT NOT NULL,
            transaction_nature TEXT CHECK(transaction_nature IN ('Royalty', 'Software-License', 'Service-Fee', 'Sold-As-Is')),
            cit_withholding_rate REAL DEFAULT 10.00,
            vat_rate REAL DEFAULT 6.00,
            surcharges_rate REAL DEFAULT 0.67, -- Combined urban maintenance & education surcharges approx 11% of VAT
            treaty_applied TEXT,
            compliance_status TEXT
        )
    ''')
    
    # Insert baseline structural records for evaluation
    cursor.execute('''
        INSERT OR IGNORE INTO china_ip_tax_rules 
        (asset_identifier, transaction_nature, cit_withholding_rate, vat_rate, surcharges_rate, treaty_applied, compliance_status)
        VALUES 
        ('Jujita-Stairs-IP-Core', 'Royalty', 10.00, 6.00, 0.67, 'Canada-PRC Tax Treaty', 'Subject to 10% CIT WHT + 6% VAT'),
        ('Standard-Off-The-Shelf-Artifact', 'Sold-As-Is', 0.00, 13.00, 0.00, 'N/A', 'Commercial Import VAT Only')
    ''')
    
    conn.commit()
    conn.close()
    print("[+] China CIPS/CNAPS rails and PRC tax compliance tables successfully vaulted into audit_ledger.db!")

if __name__ == "__main__":
    setup_china_ledger()
