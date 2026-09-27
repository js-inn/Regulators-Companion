import sqlite3

DB_NAME = "audit_ledger.db"

def analyze_portfolio_capital_stack():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT property_ref, jurisdiction, valuation_usd, annual_lease_yield_pct, mortgage_principal_usd, ltv_ratio_pct FROM real_estate_nodes")
    rows = cursor.fetchall()
    
    total_val = 0.0
    total_debt = 0.0
    total_income = 0.0
    
    print("\n==================================================================")
    print("      REAL ESTATE PORTFOLIO CAPITAL STACK & LTV ANALYSIS          ")
    print("==================================================================")
    
    for row in rows:
        prop_ref, jurisdiction, valuation, yield_pct, mortgage, ltv = row
        gross_income = valuation * (yield_pct / 100.0)
        equity = valuation - mortgage
        
        total_val += valuation
        total_debt += mortgage
        total_income += gross_income
        
        print(f"  * {prop_ref} ({jurisdiction}):")
        print(f"    - Valuation:     ${valuation:,.2f} USD")
        print(f"    - Debt (LTV):    ${mortgage:,.2f} USD ({ltv}%)")
        print(f"    - Net Equity:    ${equity:,.2f} USD")
        print(f"    - Gross Income:  ${gross_income:,.2f} USD/yr")
        print("-" * 66)
        
    total_equity = total_val - total_debt
    portfolio_ltv = (total_debt / total_val) * 100.0
    
    print(f"  -> Total Portfolio Value:   ${total_val:,.2f} USD")
    print(f"  -> Total Outstanding Debt:  ${total_debt:,.2f} USD ({portfolio_ltv:.1f}% Portfolio LTV)")
    print(f"  -> Total Net Equity Value:  ${total_equity:,.2f} USD")
    print(f"  -> Total Gross Annual Cash: ${total_income:,.2f} USD")
    print("==================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    analyze_portfolio_capital_stack()
