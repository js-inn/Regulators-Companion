import subprocess
import json
import time
from octopus_terminal import process_physical_tap

TARGET_CARD = "4611260248299474"

def poll_phone_nfc():
    print(f"Listening for physical NFC card taps (Target: Vanilla Gift Card)...")
    print("Tap your card against the back of your phone.")
    
    while True:
        try:
            # Call termux-nfc to read incoming tag data
            result = subprocess.run(['termux-nfc', '-r', 'short'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                tag_data = json.loads(result.stdout)
                card_uid = str(tag_data.get("UID") or tag_data.get("Id") or TARGET_CARD)
                
                print(f"[NFC DETECTED] Card UID/ID: {card_uid}")
                # Map physical tap to our known test card profile
                process_physical_tap(TARGET_CARD)
                
                # Cooldown to prevent duplicate triggers on a single tap
                time.sleep(2)
        except Exception as e:
            # Fallback for manual test simulation or waiting state
            time.sleep(1)

if __name__ == "__main__":
    try:
        poll_phone_nfc()
    except KeyboardInterrupt:
        print("\nNFC listener stopped.")
