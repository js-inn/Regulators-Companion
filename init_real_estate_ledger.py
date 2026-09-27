import sqlite3

DB_NAME = "audit_ledger.db"

def setup_real_estate_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Recreate table with leverage and debt metrics
    cursor.execute('DROP TABLE IF EXISTS real_estate_nodes')
    
    cursor.execute('''
        CREATE TABLE real_estate_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_ref TEXT UNIQUE NOT NULL,
            jurisdiction TEXT NOT NULL,
            asset_class TEXT CHECK(asset_class IN ('Logistics', 'Commercial-Office', 'Multi-Family', 'Data-Center')),
            valuation_usd REAL,
            annual_lease_yield_pct REAL,
            mortgage_principal_usd REAL,
            ltv_ratio_pct REAL,
            managing_entity TEXT
        )
    ''')
    
    # Insert benchmark properties with institutional LTV modeling (~50% to 60% leverage)
    cursor.execute('''
        INSERT INTO real_estate_nodes 
        (property_ref, jurisdiction, asset_class, valuation_usd, annual_lease_yield_pct, mortgage_principal_usd, ltv_ratio_pct, managing_entity)
        VALUES 
        ('RE-TYO-01', 'Japan', 'Commercial-Office', 85000000.00, 4.5, 42500000.00, 50.0, 'Jujita-Stairs Holdings / Local Trust'),
        ('RE-SHA-02', 'China', 'Logistics', 140000000.00, 5.8, 77000000.00, 55.0, '10839477 Canada Inc. APAC Vehicle'),
        ('RE-FRA-03', 'Eurozone', 'Data-Center', 210000000.00, 7.2, 126000000.00, 60.0, 'Sovereign Infrastructure EU S.à r.l.')
    ''')
    
    conn.commit()
    conn.close()
    print("[+] Institutional LTV and debt-financing parameters successfully vaulted into audit_ledger.db!")

if __name__ == "__main__":
    setup_real_estate_ledger()
