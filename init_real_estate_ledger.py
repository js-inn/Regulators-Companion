import sqlite3

DB_NAME = "audit_ledger.db"

def setup_real_estate_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Recreate table with expanded global and regional nodes
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
    
    # Insert global portfolio including Singapore, Hong Kong, Macau, and Malaysia
    cursor.execute('''
        INSERT INTO real_estate_nodes 
        (property_ref, jurisdiction, asset_class, valuation_usd, annual_lease_yield_pct, mortgage_principal_usd, ltv_ratio_pct, managing_entity)
        VALUES 
        ('RE-TYO-01', 'Japan', 'Commercial-Office', 85000000.00, 4.5, 42500000.00, 50.0, 'Jujita-Stairs Holdings / Local Trust'),
        ('RE-SHA-02', 'China (Shanghai)', 'Logistics', 140000000.00, 5.8, 77000000.00, 55.0, '10839477 Canada Inc. APAC Vehicle'),
        ('RE-HKG-03', 'Hong Kong SAR', 'Commercial-Office', 310000000.00, 4.2, 155000000.00, 50.0, 'Sovereign Infrastructure Asia Ltd'),
        ('RE-SIN-04', 'Singapore', 'Data-Center', 280000000.00, 6.8, 140000000.00, 50.0, 'Sovereign Infrastructure Asia Ltd'),
        ('RE-MAC-05', 'Macau SAR', 'Commercial-Office', 125000000.00, 5.5, 68750000.00, 55.0, 'Sovereign Infrastructure Asia Ltd'),
        ('RE-MYS-06', 'Malaysia (Kuala Lumpur)', 'Logistics', 95000000.00, 6.5, 52250000.00, 55.0, 'Sovereign Infrastructure SEA Ltd'),
        ('RE-LON-07', 'United Kingdom (England)', 'Commercial-Office', 240000000.00, 5.0, 132000000.00, 55.0, 'Sovereign Infrastructure UK Ltd'),
        ('RE-FRA-08', 'Eurozone (Germany)', 'Data-Center', 210000000.00, 7.2, 126000000.00, 60.0, 'Sovereign Infrastructure EU S.à r.l.'),
        ('RE-PAR-09', 'Eurozone (France)', 'Commercial-Office', 165000000.00, 5.2, 90750000.00, 55.0, 'Sovereign Infrastructure EU S.à r.l.'),
        ('RE-AMS-10', 'Eurozone (Netherlands)', 'Logistics', 110000000.00, 6.5, 60500000.00, 55.0, 'Sovereign Infrastructure EU S.à r.l.')
    ''')
    
    conn.commit()
    conn.close()
    print("[+] Singapore, Hong Kong, Macau, and Malaysia nodes successfully vaulted into audit_ledger.db!")

if __name__ == "__main__":
    setup_real_estate_ledger()
