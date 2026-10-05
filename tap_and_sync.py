import sys
from nfc_listener import log_nfc_tap
from dashboard_bridge import bridge_octopus_to_dashboard

if __name__ == "__main__":
    card_uid = sys.argv[1] if len(sys.argv) > 1 else "BMO_CARD_PHYSICAL"
    amount = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    
    print(f"[RUNNING] Processing tap for {card_uid}...")
    log_nfc_tap(card_uid, amount)
    bridge_octopus_to_dashboard()
    print("[SUCCESS] Tap logged, hashed, and synced to dashboard ledger!")
