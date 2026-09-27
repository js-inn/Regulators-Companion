import sqlite3
import json
import hashlib
from datetime import datetime, timezone

DB_NAME = "audit_ledger.db"
MANIFEST_NAME = "sovereign_audit_master_manifest.json"

def initialize_and_audit():
    print("[*] Initializing Sovereign Fortress Global, Orbital & Canadian Real Estate Ledger...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Setup Table Schema
    cursor.execute('DROP TABLE IF EXISTS real_estate_nodes')
    cursor.execute('''
        CREATE TABLE real_estate_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_ref TEXT UNIQUE NOT NULL,
            jurisdiction TEXT NOT NULL,
            asset_class TEXT CHECK(asset_class IN ('Logistics', 'Commercial-Office', 'Multi-Family', 'Data-Center', 'Space-Orbital')),
            valuation_usd REAL,
            annual_lease_yield_pct REAL,
            mortgage_principal_usd REAL,
            ltv_ratio_pct REAL,
            managing_entity TEXT
        )
    ''')
    
    # 2. Insert International, Orbital, and Canadian Sovereign Nodes
    nodes = [
        ('RE-TYO-01', 'Japan', 'Commercial-Office', 85000000.00, 4.5, 42500000.00, 50.0, 'Jujita-Stairs Holdings / Local Trust'),
        ('RE-SHA-02', 'China (Shanghai)', 'Logistics', 140000000.00, 5.8, 77000000.00, 55.0, '10839477 Canada Inc. APAC Vehicle'),
        ('RE-HKG-03', 'Hong Kong SAR', 'Commercial-Office', 310000000.00, 4.2, 155000000.00, 50.0, 'Sovereign Infrastructure Asia Ltd'),
        ('RE-SIN-04', 'Singapore', 'Data-Center', 280000000.00, 6.8, 140000000.00, 50.0, 'Sovereign Infrastructure Asia Ltd'),
        ('RE-MAC-05', 'Macau SAR', 'Commercial-Office', 125000000.00, 5.5, 68750000.00, 55.0, 'Sovereign Infrastructure Asia Ltd'),
        ('RE-MYS-06', 'Malaysia (Kuala Lumpur)', 'Logistics', 95000000.00, 6.5, 52250000.00, 55.0, 'Sovereign Infrastructure SEA Ltd'),
        ('RE-LON-07', 'United Kingdom (England)', 'Commercial-Office', 240000000.00, 5.0, 132000000.00, 55.0, 'Sovereign Infrastructure UK Ltd'),
        ('RE-FRA-08', 'Eurozone (Germany)', 'Data-Center', 210000000.00, 7.2, 126000000.00, 60.0, 'Sovereign Infrastructure EU S.à r.l.'),
        ('RE-PAR-09', 'Eurozone (France)', 'Commercial-Office', 165000000.00, 5.2, 90750000.00, 55.0, 'Sovereign Infrastructure EU S.à r.l.'),
        ('RE-AMS-10', 'Eurozone (Netherlands)', 'Logistics', 110000000.00, 6.5, 60500000.00, 55.0, 'Sovereign Infrastructure EU S.à r.l.'),
        ('RE-ZUR-11', 'Switzerland (Zurich)', 'Commercial-Office', 220000000.00, 4.0, 110000000.00, 50.0, 'Sovereign Infrastructure Alpine AG'),
        ('RE-CPH-12', 'Denmark (Copenhagen)', 'Data-Center', 130000000.00, 6.2, 71500000.00, 55.0, 'Sovereign Infrastructure Nordic ApS'),
        ('RE-STO-13', 'Sweden (Stockholm)', 'Logistics', 145000000.00, 5.9, 79750000.00, 55.0, 'Sovereign Infrastructure Nordic AB'),
        ('RE-DXB-14', 'UAE (Dubai)', 'Commercial-Office', 260000000.00, 6.5, 143000000.00, 55.0, 'Sovereign Infrastructure ME FZ-LLC'),
        ('RE-AUH-15', 'UAE (Abu Dhabi)', 'Data-Center', 190000000.00, 7.0, 104500000.00, 55.0, 'Sovereign Infrastructure ME FZ-LLC'),
        ('RE-BAH-16', 'Bahrain (Manama)', 'Logistics', 110000000.00, 7.5, 60500000.00, 55.0, 'Sovereign Infrastructure GCC W.L.L.'),
        # Orbital Space Production Nodes
        ('SP-LEO-01', 'Low Earth Orbit (LEO Sector 1)', 'Space-Orbital', 450000000.00, 12.5, 180000000.00, 40.0, 'Sovereign Orbital Manufacturing Corp'),
        ('SP-LUN-02', 'Lunar South Pole Base Alpha', 'Space-Orbital', 600000000.00, 15.0, 210000000.00, 35.0, 'Sovereign Deep Space Logistics Inc'),
        # Canadian Domestic Anchor Nodes (Directly Tied to Jujita Stairs / 10839477 Canada Inc.)
        ('RE-EDM-17', 'Canada (Edmonton AB)', 'Logistics', 75000000.00, 6.5, 37500000.00, 50.0, 'Jujita Stairs / 10839477 Canada Inc.'),
        ('RE-TOR-18', 'Canada (Toronto ON)', 'Commercial-Office', 210000000.00, 5.2, 115500000.00, 55.0, 'Jujita Stairs / 10839477 Canada Inc.'),
        ('RE-VAN-19', 'Canada (Vancouver BC)', 'Data-Center', 180000000.00, 7.0, 99000000.00, 55.0, 'Jujita Stairs / 10839477 Canada Inc.')
    ]
    
    cursor.executemany('''
        INSERT INTO real_estate_nodes 
        (property_ref, jurisdiction, asset_class, valuation_usd, annual_lease_yield_pct, mortgage_principal_usd, ltv_ratio_pct, managing_entity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', nodes)
    
    conn.commit()
    
    # 3. Perform Capital Stack & Leverage Analytics
    cursor.execute("SELECT property_ref, jurisdiction, asset_class, valuation_usd, annual_lease_yield_pct, mortgage_principal_usd, ltv_ratio_pct, managing_entity FROM real_estate_nodes")
    rows = cursor.fetchall()
    
    total_val = 0.0
    total_debt = 0.0
    total_income = 0.0
    
    print("\n==================================================================")
    print("      GLOBAL, ORBITAL & CANADIAN SOVEREIGN CAPITAL STACK          ")
    print("==================================================================")
    
    portfolio_data = []
    for row in rows:
        prop_ref, jurisdiction, asset_class, valuation, yield_pct, mortgage, ltv, entity = row
        gross_income = valuation * (yield_pct / 100.0)
        equity = valuation - mortgage
        
        total_val += valuation
        total_debt += mortgage
        total_income += gross_income
        
        portfolio_data.append({
            "property_ref": prop_ref,
            "jurisdiction": jurisdiction,
            "asset_class": asset_class,
            "valuation_usd": valuation,
            "debt_usd": mortgage,
            "net_equity_usd": equity,
            "gross_income_usd": gross_income,
            "managing_entity": entity
        })
        
        print(f"  * {prop_ref} [{asset_class}] ({jurisdiction})")
        print(f"    - Managing Entity: {entity}")
        print(f"    - Valuation:       ${valuation:,.2f} USD")
        print(f"    - Debt (LTV):      ${mortgage:,.2f} USD ({ltv}%)")
        print(f"    - Net Equity:      ${equity:,.2f} USD")
        print(f"    - Gross Yield:     ${gross_income:,.2f} USD/yr ({yield_pct}%)")
        print("-" * 66)
        
    total_equity = total_val - total_debt
    portfolio_ltv = (total_debt / total_val) * 100.0
    
    print(f"  -> Total Combined Portfolio Value: ${total_val:,.2f} USD")
    print(f"  -> Total Outstanding Debt:         ${total_debt:,.2f} USD ({portfolio_ltv:.1f}% Portfolio LTV)")
    print(f"  -> Total Net Equity Value:         ${total_equity:,.2f} USD")
    print(f"  -> Total Gross Annual Cash Flow:   ${total_income:,.2f} USD")
    print("==================================================================\n")
    
    # 4. Generate Cryptographic Master Manifest
    with open(DB_NAME, "rb") as f:
        db_hash = hashlib.sha256(f.read()).hexdigest()
        
    manifest = {
        "GeneratedAt": datetime.now(timezone.utc).isoformat(),
        "Architecture": "Jujita-Stairs Sovereign Fortress (Terrestrial + Orbital + Canadian)",
        "DatabaseLedger": DB_NAME,
        "DatabaseSHA256": db_hash,
        "PortfolioSummary": {
            "TotalPortfolioValueUSD": total_val,
            "TotalOutstandingDebtUSD": total_debt,
            "PortfolioLTVPct": round(portfolio_ltv, 2),
            "TotalNetEquityUSD": total_equity,
            "TotalGrossAnnualCashUSD": total_income,
            "ActiveNodesCount": len(nodes)
        },
        "Nodes": portfolio_data
    }
    
    with open(MANIFEST_NAME, "w") as mf:
        json.dump(manifest, mf, indent=4)
        
    print(f"[+] Master Manifest updated with Canadian nodes: {MANIFEST_NAME}")
    print(f"[+] SQLite Ledger SHA-256 Checksum: {db_hash}")
    conn.close()

if __name__ == "__main__":
    initialize_and_audit()
