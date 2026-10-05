import sqlite3
import hashlib

def bridge_octopus_to_dashboard():
    # Connect to Octopus local ledger
    octopus_conn = sqlite3.connect('ledger.db')
    octopus_cur = octopus_conn.cursor()
    octopus_cur.execute("SELECT id, timestamp, card_uid, amount, packet_auth, settled_externally FROM ilp_stream_ledger")
    streams = octopus_cur.fetchall()
    octopus_conn.close()
    
    # Connect to corporate ledger where octopus_transactions lives
    dash_conn = sqlite3.connect('corporate_ledger.db')
    dash_cur = dash_conn.cursor()
    
    for stream in streams:
        stream_id, ts, card_uid, amount, packet_auth, settled_externally = stream
        
        block_index = stream_id
        previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        currency = "CAD"
        nonce = stream_id * 10
        corporate_issuer = "10839477 Canada Inc."
        creator_uuid = "jujita-stairs-orchestrator"
        
        # Use packet_auth as hash, or fallback to generated sha256
        row_hash = packet_auth if packet_auth else hashlib.sha256(f"{card_uid}{amount}{ts}".encode()).hexdigest()
        
        # Insert into the block-structured octopus_transactions table
        dash_cur.execute("""
            INSERT OR IGNORE INTO octopus_transactions 
            (block_index, previous_hash, timestamp, sender_card, recipient_card, amount, currency, nonce, hash, corporate_issuer, creator_uuid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            block_index,
            previous_hash,
            ts,
            card_uid,
            "VAULT-COLD-STORAGE",
            amount,
            currency,
            nonce,
            row_hash,
            corporate_issuer,
            creator_uuid
        ))
    
    dash_conn.commit()
    dash_conn.close()
    print("[BRIDGE] Successfully synchronized NFC streams into corporate block ledger!")

if __name__ == "__main__":
    bridge_octopus_to_dashboard()
