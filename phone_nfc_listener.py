import subprocess
import sys

if __name__ == "__main__":
    print("==================================================")
    print("   OCTOPUS 2.0 - MULTI-CARD CASH TERMINAL        ")
    print("==================================================")
    
    while True:
        card_uid = input("\n[READY] Enter card name/UID (e.g., 'BMO_CARD' or '4611260248299474'): ").strip()
        
        if not card_uid:
            card_uid = "4611260248299474"
            print(f"[NOTE] Using default fallback card: {card_uid}")
            
        print(f"\n[PHYSICAL TAP DETECTED] Card: {card_uid}")
        subprocess.run(['python3', 'ilp_stream.py', card_uid])
        
        cont = input("\nProcess another tap? (y/n): ").strip().lower()
        if cont != 'y':
            print("[TERMINAL] Exiting session. Ledger state saved.")
            break
