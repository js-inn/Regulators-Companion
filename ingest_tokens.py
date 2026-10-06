import sqlite3
import urllib.request
import json
import os

DB_NAME = "wire_audit.db"
TARGET_ADDRESS = "0x17ad9827e8492a8c63baba84c9d84a210d37fb3e"

def init_token_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS token_transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_hash TEXT UNIQUE,
            block_number TEXT,
            timestamp TEXT,
            token_name TEXT,
            token_symbol TEXT,
            token_decimal TEXT,
            contract_address TEXT,
            from_addr TEXT,
            to_addr TEXT,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_token_transfers():
    init_token_table()
    
    api_key = os.environ.get("ETHERSCAN_API_KEY")
    if not api_key:
        print("[!] Error: ETHERSCAN_API_KEY is not set.")
        return

    # Updated to Etherscan API V2 endpoint with chainid=1 (Ethereum Mainnet)
    url = f"https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokentx&address={TARGET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    imported = 0
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode()
            data = json.loads(raw_data)
            
            print(f"[*] API Response Message: {data.get('message')}")
            print(f"[*] API Response Status: {data.get('status')}")
            
            if data.get("status") == "1":
                for tx in data.get("result", []):
                    cursor.execute('''
                        INSERT OR IGNORE INTO token_transfers 
                        (tx_hash, block_number, timestamp, token_name, token_symbol, token_decimal, contract_address, from_addr, to_addr, value)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        tx.get("hash"),
                        tx.get("blockNumber"),
                        tx.get("timeStamp"),
                        tx.get("tokenName"),
                        tx.get("tokenSymbol"),
                        tx.get("tokenDecimal"),
                        tx.get("contractAddress"),
                        tx.get("from"),
                        tx.get("to"),
                        tx.get("value")
                    ))
                    imported += 1
                conn.commit()
                print(f"[+] Successfully fetched and stored {imported} token transfer records!")
            else:
                print(f"[!] Etherscan API Full Response: {raw_data}")
    except Exception as e:
        print(f"[!] Error fetching token transfers: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("[*] Querying Etherscan V2 API for incoming token transfers...")
    fetch_token_transfers()
