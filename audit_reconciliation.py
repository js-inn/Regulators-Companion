import os
import sqlite3
import json
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime

DB_NAME = 'wire_audit.db'
JSON_EXPORT = 'audit_snapshot.json'

# CONFIGURATION: Set your real Ethereum tracking parameters here
REAL_WALLET_ADDRESS = "0xYourActualEthereumWalletAddressHere"
ETHERSCAN_API_KEY = "YourOptionalEtherscanApiKeyHere" # Leave blank if using public tier limits

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
    print(f"[*] Querying live network state for address: {wallet_address}...")
    
    # Using Etherscan v2 API standard endpoint for normal transactions
    api_url = f"https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=desc"
    if ETHERSCAN_API_KEY and ETHERSCAN_API_KEY != "YourOptionalEtherscanApiKeyHere":
        api_url += f"&apikey={ETHERSCAN_API_KEY}"
    
    try:
        req = urllib.request.Request(
            api_url, 
            headers={'User-Agent': 'Regulators-Companion-Auditor/1.0'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "1":
                return data.get("result", [])
            else:
                print(f"[!] API Notice: {data.get('message', 'No records or limit reached')}")
    except Exception as e:
        print(f"[!] Network query error: {e}")
    
    return []

def reconcile_and_log_royalties(wallet_address):
    if "YourActual" in wallet_address:
        print("[!] ERROR: Please update REAL_WALLET_ADDRESS in the script with your actual EVM address.")
        return

    init_db()
    external_txs = query_external_royalty_stream(wallet_address)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    new_injections = 0
    
    for tx in external_txs[:25]: # Process latest 25 transactions
        tx_hash = tx.get("hash")
        to_addr = tx.get("to")
        value = tx.get("value")
        gas_used = tx.get("gasUsed")
        timestamp_epoch = tx.get("timeStamp")
        contract_addr = tx.get("contractAddress", "")
        
        # Ingest incoming transfers or smart contract execution results
        if int(value) > 0 and to_addr and to_addr.lower() == wallet_address.lower():
            cursor.execute("SELECT id FROM eth_royalty_ledger WHERE tx_hash = ?", (tx_hash,))
            exists = cursor.fetchone()
            
            if not exists:
                timestamp = datetime.fromtimestamp(int(timestamp_epoch)).isoformat() if timestamp_epoch else datetime.now().isoformat()
                raw_data = f"{tx_hash}-{to_addr}-{value}-{timestamp}"
                record_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
                
                cursor.execute('''
                    INSERT OR IGNORE INTO eth_royalty_ledger (tx_hash, contract_address, recipient, amount_wei, gas_used, timestamp, record_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (tx_hash, contract_address or "Direct-Transfer", to_addr, value, gas_used, timestamp, record_hash))
                new_injections += 1
                print(f"[+] Verified & Ingested Live Royalty Tx: {tx_hash} | Value: {value} Wei")

    conn.commit()
    
    # Export full immutable ledger state to JSON snapshot
    cursor.execute('SELECT id, tx_hash, contract_address, recipient, amount_wei, gas_used, timestamp, record_hash FROM eth_royalty_ledger')
    rows = cursor.fetchall()
    conn.close()
    
    export_list = [{
        "id": r[0], "tx_hash": r[1], "contract_address": r[2], "recipient": r[3],
        "amount_wei": r[4], "gas_used": r[5], "timestamp": r[6], "record_hash": r[7]
    } for r in rows]
    
    with open(JSON_EXPORT, 'w') as f:
        json.dump(export_list, f, indent=4)
        
    print(f"[#] Live synchronization complete. {new_injections} new royalty events anchored.")

if __name__ == "__main__":
    reconcile_and_log_royalties(REAL_WALLET_ADDRESS)

