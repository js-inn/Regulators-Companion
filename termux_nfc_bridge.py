import time
import subprocess
from octopus_terminal import process_physical_tap

def run_termux_listener():
    print("==========================================")
    print("  OCTOPUS 2.0 - TERMUX NFC TERMINAL")
    print("  Status: Active & Listening for Taps")
    print("==========================================")
    
    # Default fallback test card identifier mapped to your simulation profile
    default_card = "4611260248299474"
    
    while True:
        try:
            # Here we poll the system sensor interface or wait for input triggers
            # You can tap or press Enter to simulate/trigger a live hardware event 
            user_input = input("\n[ACTION] Tap NFC device / Press Enter to process test tap (Ctrl+C to exit): ")
            
            # If a physical sensor scan string or manual trigger is caught:
            card_uid = user_input.strip() if user_input.strip() else default_card
            
            print(f"[PROCESSING] Intercepted card identifier: {card_uid}")
            process_physical_tap(card_uid)
            
        except KeyboardInterrupt:
            print("\n[INFO] Octopus 2.0 Terminal stopped safely by user.")
            break
        except Exception as e:
            print(f"[ERROR] Encountered runtime exception: {e}")
            time.sleep(1)

if __name__ == "__main__":
    run_termux_listener()
