import sys
from octopus_terminal import process_physical_tap

def main():
    if len(sys.argv) > 1:
        card_uid = sys.argv[1].strip()
        print(f"\n[NFC HARDWARE TAP] Captured from Phone Sensor: {card_uid}")
        process_physical_tap(card_uid)
    else:
        print("[INFO] Running in interactive mode. Press Enter to simulate test tap.")
        default_card = "4611260248299474"
        input("Press Enter to execute tap: ")
        process_physical_tap(default_card)

if __name__ == "__main__":
    main()
