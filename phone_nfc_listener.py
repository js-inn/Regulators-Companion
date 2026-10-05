import subprocess

def process_real_tap(card_uid):
    print(f"\n[PHYSICAL TAP DETECTED] Card UID: {card_uid}")
    # Temporarily update or pass the card uid to ilp_stream if needed, then run it
    subprocess.run(['python3', 'ilp_stream.py'])

if __name__ == "__main__":
    print("==================================================")
    print("   OCTOPUS 2.0 - PHYSICAL NFC & CASH TERMINAL     ")
    print("==================================================")
    
    while True:
        card_uid = input("\n[READY] Enter or scan your card number (or press Enter for default): ").strip()
        
        if not card_uid:
            card_uid = "4611260248299474" # Fallback default
            print(f"[NOTE] Using default active card: {card_uid}")
            
        process_real_tap(card_uid)
        
        cont = input("\nProcess another card tap? (y/n): ").strip().lower()
        if cont != 'y':
            print("[TERMINAL] Exiting NFC listener session. Ledger state saved.")
            break
