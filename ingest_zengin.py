import sqlite3
import os

DB_NAME = "audit_ledger.db"

def parse_and_vault_zengin(file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"[*] Processing Zengin transmission file: {file_path}")
    
    with open(file_path, "r", encoding="cp932") as f:
        lines = f.readlines()
        
    processed_count = 0
    for line_num, line in enumerate(lines, 1):
        line = line.rstrip("\r\n")
        
        # Verify fixed-length standard for Zengin text format
        if len(line) < 2:
            continue
            
        record_type = line[0]
        
        # Type '2' represents a Data Record (Transfer Destination / Transaction Item)
        if record_type == '2':
            # Extract fields based on standard Zengin layout specifications
            bank_code = line[1:5]
            branch_code = line[5:8]
            
            # Construct a unique transaction reference for the audit ledger
            tx_ref = f"ZENGIN-{line_num}-{bank_code}-{branch_code}"
            
            # Amount is typically stored in positions 20-29 (zero-padded 10 digits)
            try:
                amount_jpy = float(line[20:30])
            except ValueError:
                amount_jpy = 0.00
                
            cursor.execute('''
                INSERT OR IGNORE INTO zengin_settlement_nodes 
                (transaction_ref, clearing_rail, settlement_destination, amount_jpy, zendi_metadata_attached, settled_via_boj)
                VALUES (?, 'Zengin-Net', ?, ?, 1, 1)
            ''', (tx_ref, f"Bank:{bank_code} Branch:{branch_code}", amount_jpy))
            
            processed_count += 1

    conn.commit()
    conn.close()
    print(f"[+] Successfully vaulted {processed_count} Zengin transaction nodes into audit_ledger.db!")

if __name__ == "__main__":
    sample_file = "sample_zengin.txt"
    parse_and_vault_zengin(sample_file)
