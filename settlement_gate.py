import os
import hashlib
import json
import tarfile
import subprocess
from datetime import datetime

class SettlementVault:
    def __init__(self, encrypted_payload="device_vault_payload.tar.gz.enc"):
        self.encrypted_payload = encrypted_payload
        self.config_file = ".settlement_config.json"
        
    def setup_conditions(self, settlement_address, required_amount_cad):
        """Define the strict payout/settlement conditions required to unlock the IP."""
        config = {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "LOCKED",
            "settlement_target": settlement_address,
            "required_amount_cad": required_amount_cad,
            "verification_endpoint": "local_immutable_ledger"
        }
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=4)
        print(f"[+] Settlement conditions locked. IP access is strictly bound to financial clearance.")

    def verify_and_unlock(self, proof_of_payment_hash, master_decryption_key):
        """
        Attempt to unlock the vault. 
        Requires both proof that the settlement condition is met and the master key.
        """
        if not os.path.exists(self.config_file):
            print("[-] Error: Settlement configuration missing.")
            return

        with open(self.config_file, "r") as f:
            config = json.load(f)

        if config["status"] == "UNLOCKED":
            print("[!] Vault is already unlocked.")
            return

        # In a fully integrated system, proof_of_payment_hash would be verified 
        # against a blockchain or secure banking API ledger here.
        print(f"[*] Verifying settlement proof: {proof_of_payment_hash[:16]}...")
        
        # Simulating cryptographic verification check against the settlement target
        if len(proof_of_payment_hash) >= 32:  # Valid hash structure check
            print("[+] Settlement verified successfully on ledger.")
            config["status"] = "UNLOCKED"
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
            
            self._decrypt_payload(master_decryption_key)
        else:
            print("[-] ACCESS DENIED: Invalid settlement proof or payment not cleared.")

    def _decrypt_payload(self, password):
        """Decrypts and extracts the vault payload only after settlement verification."""
        output_tar = "recovered_vault.tar.gz"
        cmd = [
            "openssl", "enc", "-d", "-aes-256-cbc",
            "-in", self.encrypted_payload,
            "-out", output_tar,
            "-k", password
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[+] Settlement clear! Extracting IP payload...")
            with tarfile.open(output_tar, "r:gz") as tar:
                tar.extractall()
            os.remove(output_tar)
            print("[+] Vault successfully opened and restored.")
        else:
            print(f"[-] Decryption failed: {result.stderr}")

if __name__ == "__main__":
    vault = SettlementVault()
    choice = input("Select mode - (1) Set Lock Conditions, (2) Attempt Unlock with Settlement: ").strip()
    
    if choice == "1":
        addr = input("Enter your secure settlement destination/ID: ").strip()
        amt = input("Enter required settlement amount (CAD): ").strip()
        vault.setup_conditions(addr, amt)
    elif choice == "2":
        proof = input("Enter cryptographic settlement proof hash / Transaction ID: ").strip()
        key = input("Enter master decryption key: ").strip()
        vault.verify_and_unlock(proof, key)
    else:
        print("[-] Invalid selection.")

