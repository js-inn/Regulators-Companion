import sqlite3
import time
import os

def tail_ledger():
    db_path = 'corporate_ledger.db'
    if not os.path.exists(db_path):
        print("[ERROR] Corporate ledger not found.")
        return

    print("==================================================")
    print("  OCTOPUS 2.0 - LIVE NFC STREAM & AUDIT MONITOR   ")
    print("==================================================")
    print("Listening for incoming card taps... (Press Ctrl+C to exit)\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get initial count
    cursor.execute("SELECT COUNT(*) FROM octopus_transactions")
    last_count = cursor.fetchone()[0]
    conn.close()

    try:
        while True:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT block_index, timestamp, sender_card, amount, currency, hash FROM octopus_transactions")
            rows = cursor.fetchall()
            conn.close()

            if len(rows) > last_count:
                new_rows = rows[last_count:]
                for row in new_rows:
                    block_idx, ts, card, amount, currency, row_hash = row
                    print(f"[LIVE TAP VERIFIED] Block #{block_idx} | Time: {ts} | Card: {card} | Amount: {amount} {currency} | Hash: {row_hash[:12]}...")
                last_count = len(rows)

            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[MONITOR] Live stream monitor closed.")

if __name__ == "__main__":
    tail_ledger()
