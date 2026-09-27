import sqlite3

DB_NAME = "audit_ledger.db"

def setup_real_estate_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table for tracking physical global real estate holdings & lease yields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_estate_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_ref TEXT UNIQUE NOT NULL,
            jurisdiction TEXT NOT NULL,
            asset_class TEXT CHECK(asset_class IN ('Logistics', 'Commercial-Office', 'Multi-Family', 'Data-Center')),
            valuation_usd REAL,
            annual_lease_yield_pct REAL,
            managing_entity TEXT
        )
    ''')
    
    # Insert baseline benchmark properties representing global footprints
    cursor.execute('''
        INSERT OR IGNORE INTO real_estate_nodes 
        (property_ref, jurisdiction, asset_class, valuation_usd, annual_lease_yield_pct, managing_entity)
        VALUES 
        ('RE-TYO-01', 'Japan', 'Commercial-Office', 85000000.00, 4.5, 'Jujita-Stairs Holdings / Local Trust'),
        ('RE-SHA-02', 'China', 'Logistics', 140000000.00, 5.8, '10839477 Canada Inc. APAC Vehicle'),
        ('RE-FRA-03', 'Eurozone', 'Data-Center', 210000000.00, 7.2, 'Sovereign Infrastructure EU S.à r.l.')
    ''')
    
    conn.commit()
    conn.close()
    print("[+] Global real estate tracking nodes successfully vaulted into audit_ledger.db!")

if __name__ == "__main__":
    setup_real_estate_ledger()
