import sqlite3

DB_NAME = "audit_ledger.db"

def analyze_digital_infrastructure_dscr():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Query all nodes, focusing heavily on Data-Centers and overall portfolio
    cursor.execute('''
        SELECT property_ref, jurisdiction, asset_class, valuation_usd, annual_lease_yield_pct, mortgage_principal_usd, ltv_ratio_pct 
        FROM real_estate_nodes
    ''')
    rows = cursor.fetchall()
    
    # Institutional Assumptions
    OPEX_RATIO = 0.25      # 25% operating expense ratio for data centers and commercial assets
    DEBT_SERVICE_CONSTANT = 0.072  # Assumes ~7.2% annual debt service constant (Interest + Amortization)
    
    print("\n==================================================================")
    print("      INSTITUTIONAL DSCR & DIGITAL INFRASTRUCTURE AUDIT REPORT    ")
    print("==================================================================\n")
    
    total_portfolio_noi = 0.0
    total_portfolio_debt_service = 0.0
    
    for row in rows:
        prop_ref, jurisdiction, asset_class, valuation, yield_pct, mortgage, ltv = row
        
        # Calculate Financial Metrics
        gross_income = valuation * (yield_pct / 100.0)
        noi = gross_income * (1.0 - OPEX_RATIO)
        annual_debt_service = mortgage * DEBT_SERVICE_CONSTANT
        
        dscr = noi / annual_debt_service if annual_debt_service > 0 else 0.0
        
        # Highlight Data-Center nodes specifically
        is_datacenter = (asset_class == 'Data-Center')
        tag = "[TARGET DC NODE]" if is_datacenter else "[STANDARD]"
        
        print(f"  {tag} {prop_ref} [{asset_class}] ({jurisdiction})")
        print(f"    - Valuation:         ${valuation:,.2f} USD")
        print(f"    - Gross Yield:       ${gross_income:,.2f} USD/yr ({yield_pct}%)")
        print(f"    - Net Oper. Income:  ${noi:,.2f} USD/yr (NOI)")
        print(f"    - Annual Debt Svc:   ${annual_debt_service:,.2f} USD/yr")
        print(f"    - DSCR Ratio:        {dscr:.2f}x {'(PASSED)' if dscr >= 1.35 else '(REVIEW)'}")
        print("-" * 66)
        
        total_portfolio_noi += noi
        total_portfolio_debt_service += annual_debt_service
        
    portfolio_dscr = total_portfolio_noi / total_portfolio_debt_service if total_portfolio_debt_service > 0 else 0.0
    
    print(f"\n  -> Aggregate Portfolio NOI:       ${total_portfolio_noi:,.2f} USD/yr")
    print(f"  -> Aggregate Annual Debt Service: ${total_portfolio_debt_service:,.2f} USD/yr")
    print(f"  -> Consolidated Portfolio DSCR:   {portfolio_dscr:.2f}x")
    print(f"  -> Institutional Health Status:   {'OPTIMAL (AAA-Grade Coverage)' if portfolio_dscr >= 1.40 else 'STABLE'}")
    print("==================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    analyze_digital_infrastructure_dscr()
