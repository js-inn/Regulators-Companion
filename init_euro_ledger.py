import sqlite3

DB_NAME = "audit_ledger.db"

def setup_euro_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Table for tracking SEPA and T2 / TARGET2 settlement nodes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS euro_settlement_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_ref TEXT UNIQUE NOT NULL,
            clearing_rail TEXT CHECK(clearing_rail IN ('SEPA-SCT', 'SEPA-Instant', 'T2-RTGS')),
            bic_code TEXT,
            amount_eur REAL,
            iso20022_compliant BOOLEAN,
            settled_via_ecb BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Table for tracking EU cross-border IP royalties and VAT reverse charge rules
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS euro_ip_tax_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_identifier TEXT NOT NULL,
            transaction_nature TEXT CHECK(transaction_nature IN ('Royalty', 'Software-License', 'Service-Fee', 'Sold-As-Is')),
            withholding_tax_rate REAL DEFAULT 0.00, -- Often 0% under EU Interest and Royalties Directive or specific double tax treaties
            vat_treatment TEXT,
            compliance_status TEXT
        )
    ''')
    
    # Insert baseline compliance profiles for Eurozone transactions
    cursor.execute('''
        INSERT OR IGNORE INTO euro_ip_tax_rules 
        (asset_identifier, transaction_nature, withholding_tax_rate, vat_treatment, compliance_status)
        VALUES 
        ('Jujita-Stairs-IP-Core', 'Royalty', 0.00, 'B2B Reverse Charge (0% WHT via Directive)', 'Exempt / Directive Aligned'),
        ('Standard-Off-The-Shelf-Artifact', 'Sold-As-Is', 0.00, 'Import OSS / Standard VAT', 'Standard Commercial EU VAT')
    ''')
    
    conn.commit()
    conn.close()
    print("[+] Eurozone SEPA/T2 rails and EU tax compliance tables successfully vaulted into audit_ledger.db!")

if __name__ == "__main__":
    setup_euro_ledger()
