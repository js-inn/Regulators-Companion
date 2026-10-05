import subprocess

if __name__ == "__main__":
    print("==================================================")
    print("   OCTOPUS 2.0 - CASH TERMINAL SELECTOR          ")
    print("==================================================")
    
    while True:
        print("\nSelect Card to Tap & Stream:")
        print("  [1] BMO Card")
        print("  [2] Vanilla Gift Card (4611260248299474)")
        print("  [3] Custom Card UID / Manual Entry")
        
        choice = input("\nSelect option (1-3) or press Enter to exit: ").strip()
        
        if not choice:
            print("[TERMINAL] Exiting NFC session. Ledger state saved.")
            break
            
        card_uid = "4611260248299474" # default
        if choice == '1':
            card_uid = "BMO_CARD_PHYSICAL"
        elif choice == '2':
            card_uid = "4611260248299474"
        elif choice == '3':
            card_uid = input("Enter custom card UID: ").strip()
            if not card_uid:
                continue
        else:
            print("[ERROR] Invalid selection.")
            continue
            
        print(f"\n[PHYSICAL TAP REGISTERED] Processing card: {card_uid}")
        subprocess.run(['python3', 'ilp_stream.py', card_uid])
        
        cont = input("\nProcess another tap? (y/n): ").strip().lower()
        if cont != 'y':
            print("[TERMINAL] Exiting NFC session. Ledger state saved.")
            break
