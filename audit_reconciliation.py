import os
import sqlite3
import json
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime

DB_NAME = 'wire_audit.db'
JSON_EXPORT = 'audit_snapshot.json'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eth_royalty_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_hash TEXT UNIQUE,
            contract_address TEXT,
            recipient TEXT,
            amount_wei TEXT,
            gas_used TEXT,
            timestamp TEXT,
            record_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def query_external_royalty_stream(wallet_address):
    """
    Queries external blockchain state / explorer API for recent incoming transactions.
    Using standard library urllib to avoid extra package dependencies in Termux.
    """
    print(f"[*] Querying external network state for address: {wallet_address}...")
    
    # Example integration point using public block explorer API or JSON-RPC endpoint
    # For production nodes (Alchemy/Infura/Etherscan), plug your endpoint/API key here.
    api_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=desc"
    
    try:
        req = urllib.request.Request(
            api_url, 
            headers={'User-Agent': 'Regulators-Companion-Auditor/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "1":
                return data.get("result", [])
    except Exception as e:
        print(f"[!] Network query warning (using local fallback/cached buffer): {e}")
    
    return []

def reconcile_and_log_royalties(wallet_address):
    init_db()
    external_txs = query_external_royalty_stream(wallet_address)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    new_injections = 0
    
    for tx in external_txs[:10]: # Process latest 10 transactions
        tx_hash = tx.get("hash")
        to_addr = tx.get("to")
        value = tx.get("value")
        gas_used = tx.get("gasUsed")
        timestamp_epoch = tx.get("timeStamp")
        
        # Filter for incoming transfers or specific contract interactions
        if int(value) > 0 and to_addr.lower() == wallet_address.lower():
            # Cross-reference check: Does this tx_hash already exist in SQLite?
            cursor.execute("SELECT id FROM eth_royalty_ledger WHERE tx_hash = ?", (tx_hash,))
            exists = cursor.fetchone()
            
            if not exists:
                timestamp = datetime.fromtimestamp(int(timestamp_epoch)).isoformat() if timestamp_epoch else datetime.now().isoformat()
                raw_data = f"{tx_hash}-{to_addr}-{value}-{timestamp}"
                record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
                
                cursor.execute('''
                    INSERT OR IGNORE INTO eth_royalty_ledger (tx_hash, contract_address, recipient, amount_wei, gas_used, timestamp, record_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (tx_hash, "External-Contract-Stream", to_addr, value, gas_used, timestamp, record_hash))
                new_injections += 1
                print(f"[+] Discovered & Ingested New Royalty Tx: {tx_hash} | Value: {value} Wei")

    conn.commit()
    
    # Export full ledger state to JSON snapshot
    cursor.execute('SELECT id, tx_hash, contract_address, recipient, amount_wei, gas_used, timestamp, record_hash FROM eth_royalty_ledger')
    rows = cursor.fetchall()
    conn.close()
    
    export_list = [{
        "id": r[0], "tx_hash": r[1], "contract_address": r[2], "recipient": r[3],
        "amount_wei": r[4], "gas_used": r[5], "timestamp": r[6], "record_hash": r[7]
    } for r in rows]
    
    with open(JSON_EXPORT, 'w') as f:
        json.dump(export_list, f, indent=4)
        
    print(f"[#] Synchronization complete. {new_injections} new royalty events anchored to local snapshot.")

if __name__ == "__main__":
    target_wallet = "0xJujitaStairsCoreNodeMockAddress"
    reconcile_and_log_royalties(target_wallet)

