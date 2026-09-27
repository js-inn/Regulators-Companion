import sqlite3
import os

DB_NAME = "audit_ledger.db"

def parse_and_vault_euro_settlement(file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"[*] Processing Eurozone transmission log: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    processed_count = 0
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        # Format expected: REF|RAIL|BIC_CODE|AMOUNT_EUR
        parts = line.split("|")
        if len(parts) >= 4:
            tx_ref, rail, bic_code, amount_str = parts[0], parts[1], parts[2], parts[3]
            try:
                amount_eur = float(amount_str)
            except ValueError:
                amount_eur = 0.00
                
            cursor.execute('''
                INSERT OR IGNORE INTO euro_settlement_nodes 
                (transaction_ref, clearing_rail, bic_code, amount_eur, iso20022_compliant, settled_via_ecb)
                VALUES (?, ?, ?, ?, 1, 1)
            ''', (tx_ref, rail, bic_code, amount_eur))
            processed_count += 1

    conn.commit()
    conn.close()
    print(f"[+] Successfully vaulted {processed_count} Eurozone settlement nodes into audit_ledger.db!")

if __name__ == "__main__":
    sample_file = "sample_euro.txt"
    if not os.path.exists(sample_file):
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("# T2 / SEPA ISO20022 Simulated Log\n")
            f.write("T2-2026-001|T2-RTGS|DEUTDEDEMM|45000.00\n")
            f.write("SEPA-2026-002|SEPA-SCT|BNPAFRPPXXX|12500.50\n")
            
    parse_and_vault_euro_settlement(sample_file)
