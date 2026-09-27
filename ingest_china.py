import sqlite3
import os

DB_NAME = "audit_ledger.db"

def parse_and_vault_china_settlement(file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"[*] Processing CIPS transmission log: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    processed_count = 0
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        parts = line.split("|")
        if len(parts) >= 4:
            tx_ref, rail, cnaps_code, amount_str = parts[0], parts[1], parts[2], parts[3]
            try:
                amount_cny = float(amount_str)
            except ValueError:
                amount_cny = 0.00
                
            cursor.execute('''
                INSERT OR IGNORE INTO china_settlement_nodes 
                (transaction_ref, clearing_rail, cnaps_bank_code, amount_cny, iso20022_compliant, settled_via_pboc)
                VALUES (?, ?, ?, ?, 1, 1)
            ''', (tx_ref, rail, cnaps_code, amount_cny))
            processed_count += 1

    conn.commit()
    conn.close()
    print(f"[+] Successfully vaulted {processed_count} China settlement nodes into audit_ledger.db!")

if __name__ == "__main__":
    sample_file = "sample_cips.txt"
    if not os.path.exists(sample_file):
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("# CIPS ISO20022 Simulated Log\n")
            f.write("CIPS-2026-001|CIPS|102100099996|350000.00\n")
            
    parse_and_vault_china_settlement(sample_file)
