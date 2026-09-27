import sqlite3

DB_NAME = "audit_ledger.db"

def setup_uspto_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Table for tracking USPTO patent applications and asset registration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uspto_patent_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_number TEXT UNIQUE NOT NULL,
            patent_title TEXT,
            filing_date TEXT,
            status_text TEXT,
            jurisdiction TEXT DEFAULT 'US-USPTO'
        )
    ''')
    
    # 2. Table for tracking assignment chains and ownership transfers (Reel/Frame)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uspto_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_number TEXT NOT NULL,
            reel_number INTEGER,
            frame_number INTEGER,
            recorded_date TEXT,
            assignor TEXT,
            assignee TEXT,
            conveyance_text TEXT,
            FOREIGN KEY(application_number) REFERENCES uspto_patent_assets(application_number)
        )
    ''')
    
    # Insert a foundational reference node for your IP core
    cursor.execute('''
        INSERT OR IGNORE INTO uspto_patent_assets 
        (application_number, patent_title, filing_date, status_text, jurisdiction)
        VALUES 
        ('18045436', 'Jujita-Stairs Sovereign IP Architecture', '2024-01-09', 'Published / Active', 'US-USPTO')
    ''')
    
    conn.commit()
    conn.close()
    print("[+] USPTO patent asset and assignment tracking tables successfully vaulted into audit_ledger.db!")

if __name__ == "__main__":
    setup_uspto_ledger()
