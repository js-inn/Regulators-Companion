import json
import hashlib
from datetime import datetime

class CapitalRouterSimulation:
    def __init__(self, corporate_id, checking_account_id):
        self.corporate_id = corporate_id
        self.checking_account_id = checking_account_id
        self.ledger_file = ".capital_routing_ledger.json"
        self.initialize_ledger()

    def initialize_ledger(self):
        """Initialize the local simulation ledger."""
        if not self.initialize_check():
            ledger = {
                "system_status": "ACTIVE",
                "routing_rules": {
                    "source": self.corporate_id,
                    "destination": self.checking_account_id,
                    "bypass_intermediate_holding": True
                },
                "transactions": []
            }
            with open(self.ledger_file, "w") as f:
                json.dump(ledger, f, indent=4)

    def initialize_check(self):
        try:
            with open(self.ledger_file, "r") as f:
                return True
        except FileNotFoundError:
            return False

    def simulate_settlement(self, amount_cad, reference_note):
        """Simulate an incoming settlement routing directly to the target account."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Create cryptographic proof for the routing event
        payload = f"{self.corporate_id}:{self.checking_account_id}:{amount_cad}:{timestamp}"
        tx_hash = hashlib.sha256(payload.encode()).hexdigest()

        transaction_record = {
            "timestamp": timestamp,
            "amount_cad": amount_cad,
            "origin": self.corporate_id,
            "destination": self.checking_account_id,
            "routing_status": "DIRECT_SETTLEMENT",
            "reference": reference_note,
            "ledger_hash": tx_hash
        }

        with open(self.ledger_file, "r+") as f:
            ledger = json.load(f)
            ledger["transactions"].append(transaction_record)
            f.seek(0)
            json.dump(ledger, f, indent=4)
            f.truncate()

        print(f"[+] Settlement Routed Successfully.")
        print(f"    - Amount: ${amount_cad} CAD")
        print(f"    - Destination: Checking Account [{self.checking_account_id}]")
        print(f"    - Ledger Hash: {tx_hash}")

if __name__ == "__main__":
    print("--- Capital Routing & Settlement Simulation ---")
    corp = input("Enter Corporate ID (e.g., 10839477 Canada Inc): ").strip()
    checking = input("Enter Target Personal Checking Account ID: ").strip()
    
    router = CapitalRouterSimulation(corp, checking)
    
    amt = input("Enter settlement simulation amount (CAD): ").strip()
    note = input("Enter settlement reference/memo: ").strip()
    
    router.simulate_settlement(amt, note)

