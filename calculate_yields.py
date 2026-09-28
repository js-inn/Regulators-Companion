import sqlite3

DB_NAME = "audit_ledger.db"

def compute_portfolio_cashflows():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT property_ref, jurisdiction, valuation_usd, annual_lease_yield_pct FROM real_estate_nodes")
    rows = cursor.fetchall()
    
    total_val = 0.0
    total_income = 0.0
    
    print("\n==================================================================")
    print("      REAL ESTATE PORTFOLIO CASH FLOW & YIELD ANALYSIS          ")
    print("==================================================================")
    
    for row in rows:
        prop_ref, jurisdiction, valuation, yield_pct = row
        annual_income = valuation * (yield_pct / 100.0)
        total_val += valuation
        total_income += annual_income
        print(f"  * {prop_ref} ({jurisdiction}): Val ${valuation:,.2f} | Yield {yield_pct}% -> Annual Income: ${annual_income:,.2f}")
        
    print("------------------------------------------------------------------")
    print(f"  -> Total Portfolio Valuation:   ${total_val:,.2f} USD")
    print(f"  -> Total Gross Annual Income:   ${total_income:,.2f} USD")
    print(f"  -> Blended Yield Average:       {(total_income / total_val) * 100:.2f}%")
    print("==================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    compute_portfolio_cashflows()
