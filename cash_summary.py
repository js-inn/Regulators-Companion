import sqlite3

def show_cash_summary():
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    
    print("\n==============================================")
    print("      OCTOPUS 2.0 - CASH & LEDGER SUMMARY     ")
    print("==============================================")
    
    # 1. Summary of Standard Offline Taps
    try:
        cursor.execute("SELECT COUNT(*), SUM(amount) FROM ledger")
        tap_count, tap_total = cursor.fetchone()
        tap_total = tap_total if tap_total else 0.0
        print(f"[STANDARD TAPS] Total Taps: {tap_count | 0} | Total Volume: ${tap_total:.2f}")
    except sqlite3.OperationalError:
        print("[STANDARD TAPS] No legacy tap table found.")

    # 2. Summary of ILP Cash Streams
    try:
        cursor.execute("SELECT COUNT(*), SUM(amount), COUNT(DISTINCT card_uid) FROM ilp_stream_ledger")
        packet_count, stream_total, unique_cards = cursor.fetchone()
        stream_total = stream_total if stream_total else 0.0
        print(f"[ILP STREAMS]   Total Packets: {packet_count | 0} | Settled Cash: ${stream_total:.2f} | Unique Cards: {unique_cards | 0}")
        
        # Detailed breakdown per card
        cursor.execute("SELECT card_uid, COUNT(packet_index), SUM(amount) FROM ilp_stream_ledger GROUP BY card_uid")
        rows = cursor.fetchall()
        print("\n--- Breakdown by Card UID ---")
        for row in rows:
            print(f" Card: {row[0]} | Packets: {row[1]} | Subtotal: ${row[2]:.2f}")
            
    except sqlite3.OperationalError:
        print("[ILP STREAMS] No ILP stream ledger table found.")
        
    print("==============================================\n")
    conn.close()

if __name__ == "__main__":
    show_cash_summary()
