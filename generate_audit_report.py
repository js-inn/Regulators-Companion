import sqlite3

DB_NAME = "audit_ledger.db"

def generate_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("==================================================================")
    print("         SOVEREIGN AUDIT & CROSS-BORDER SETTLEMENT REPORT         ")
    print("==================================================================")
    
    # 1. Fetch IP Monetization Rules
    print("\n[+] IP Monetization & Tax Characterization Framework:")
    cursor.execute("SELECT asset_identifier, characterization_type, statutory_withholding_rate, treaty_reduced_rate, compliance_status FROM ip_monetization_rules")
    ip_rows = cursor.fetchall()
    
    print(f"{'ASSET IDENTIFIER':<25} | {'TYPE':<12} | {'STATUTORY %':<11} | {'TREATY RATE':<11} | {'STATUS'}")
    print("-" * 80)
    for row in ip_rows:
        asset, c_type, stat_rate, treaty_rate, status = row
        print(f"{asset:<25} | {c_type:<12} | {stat_rate:<11.2f} | {treaty_rate:<11.2f} | {status}")
        
    # 2. Fetch Zengin Settlement Nodes
    print("\n[+] Zengin-Net Settlement Nodes & Rail Activity:")
    cursor.execute("SELECT transaction_ref, clearing_rail, settlement_destination, amount_jpy, settled_via_boj FROM zengin_settlement_nodes")
    zengin_rows = cursor.fetchall()
    
    print(f"{'TRANSACTION REF':<20} | {'RAIL':<12} | {'DESTINATION':<20} | {'AMOUNT (JPY)':<12} | {'BOJ'}")
    print("-" * 85)
    total_jpy = 0.0
    for row in zengin_rows:
        tx_ref, rail, dest, amt, boj = row
        total_jpy += amt
        boj_str = "Yes" if boj else "No"
        print(f"{tx_ref:<20} | {rail:<12} | {dest:<20} | {amt:<12,.2f} | {boj_str}")
        
    print("-" * 85)
    print(f"Total Cleared Zengin Volume: ¥{total_jpy:,.2f}")
    print("==================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    generate_report()
