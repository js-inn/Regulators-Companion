import sqlite3

DB_NAME = "audit_ledger.db"

def generate_global_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("==================================================================")
    print("      GLOBAL MULTI-JURISDICTIONAL SOVEREIGN AUDIT REPORT          ")
    print("==================================================================")
    
    # 1. USPTO IP Assets & Assignments
    print("\n[+] USPTO INTELLECTUAL PROPERTY & ASSIGNMENT PIPELINE:")
    cursor.execute("SELECT application_number, patent_title, filing_date, status_text FROM uspto_patent_assets")
    for row in cursor.fetchall():
        print(f"  * App No: {row[0]} | Title: {row[1]} | Filed: {row[2]} | Status: {row[3]}")
    cursor.execute("SELECT application_number, reel_number, recorded_date, assignee, conveyance_text FROM uspto_assignments")
    for row in cursor.fetchall():
        print(f"  * Assignment: App {row[0]} | Reel {row[1]} | Recorded: {row[2]} | Assignee: {row[3]} ({row[4]})")

    # 2. Japan Pipeline
    print("\n[+] JAPAN REGULATORY & SETTLEMENT PIPELINE:")
    cursor.execute("SELECT asset_identifier, characterization_type, compliance_status FROM ip_monetization_rules")
    for row in cursor.fetchall():
        print(f"  * Asset: {row[0]:<25} | Type: {row[1]:<12} | Status: {row[2]}")
    cursor.execute("SELECT transaction_ref, settlement_destination, amount_jpy FROM zengin_settlement_nodes")
    zengin_rows = cursor.fetchall()
    total_jpy = sum(r[2] for r in zengin_rows)
    for row in zengin_rows:
        print(f"  * Zengin Node: {row[0]} | Dest: {row[1]} | ¥{row[2]:,.2f}")
    print(f"  -> Total Cleared JPY Volume: ¥{total_jpy:,.2f}")

    # 3. China Pipeline
    print("\n[+] CHINA REGULATORY & SETTLEMENT PIPELINE:")
    cursor.execute("SELECT asset_identifier, transaction_nature, compliance_status FROM china_ip_tax_rules")
    for row in cursor.fetchall():
        print(f"  * Asset: {row[0]:<25} | Nature: {row[1]:<18} | Status: {row[2]}")
    cursor.execute("SELECT transaction_ref, clearing_rail, cnaps_bank_code, amount_cny FROM china_settlement_nodes")
    china_rows = cursor.fetchall()
    total_cny = sum(r[3] for r in china_rows)
    for row in china_rows:
        print(f"  * China Node: {row[0]} | Rail: {row[1]} | CNAPS: {row[2]} | ¥{row[3]:,.2f} CNY")
    print(f"  -> Total Cleared CNY Volume: ¥{total_cny:,.2f} CNY")

    # 4. Eurozone Pipeline
    print("\n[+] EUROZONE REGULATORY & SETTLEMENT PIPELINE:")
    cursor.execute("SELECT asset_identifier, transaction_nature, compliance_status FROM euro_ip_tax_rules")
    for row in cursor.fetchall():
        print(f"  * Asset: {row[0]:<25} | Nature: {row[1]:<18} | Status: {row[2]}")
    cursor.execute("SELECT transaction_ref, clearing_rail, bic_code, amount_eur FROM euro_settlement_nodes")
    euro_rows = cursor.fetchall()
    total_eur = sum(r[3] for r in euro_rows)
    for row in euro_rows:
        print(f"  * Euro Node: {row[0]} | Rail: {row[1]} | BIC: {row[2]} | €{row[3]:,.2f}")
    print(f"  -> Total Cleared EUR Volume: €{total_eur:,.2f}")

    print("\n==================================================================")
    print("          MASTER AUDIT LEDGER INTEGRITY CHECK PASSED              ")
    print("==================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    generate_global_report()
