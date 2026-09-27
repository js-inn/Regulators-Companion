import sqlite3
import os

DB_NAME = "audit_ledger.db"

def parse_and_vault_uspto_data(file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"[*] Processing USPTO ingestion log: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    processed_count = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        # Format expected: APP_NUM|REEL|FRAME|RECORDED_DATE|ASSIGNOR|ASSIGNEE|CONVEYANCE
        parts = line.split("|")
        if len(parts) >= 7:
            app_num, reel, frame, rec_date, assignor, assignee, conveyance = parts
            
            cursor.execute('''
                INSERT OR IGNORE INTO uspto_assignments 
                (application_number, reel_number, frame_number, recorded_date, assignor, assignee, conveyance_text)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (app_num, int(reel), int(frame), rec_date, assignor, assignee, conveyance))
            processed_count += 1

    conn.commit()
    conn.close()
    print(f"[+] Successfully vaulted {processed_count} USPTO assignment records into audit_ledger.db!")

if __name__ == "__main__":
    sample_file = "sample_uspto_assignments.txt"
    if not os.path.exists(sample_file):
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("# USPTO Assignment Log Format\n")
            f.write("18045436|66070|125|2024-01-09|SHEN, GENE|10839477 Canada Inc.|ASSIGNMENT OF ASSIGNORS INTEREST\n")
            
    parse_and_vault_uspto_data(sample_file)
