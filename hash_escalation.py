import hashlib
import json
from datetime import datetime, timezone

escalation_text = """Subject: URGENT: Formal Inquiry and Escalation Regarding Account Status – 10839477 Canada Inc. (BN: 749810883RC0001)

Dear TD Bank Commercial / Treasury Services Management,

I am writing to formally request an immediate status update and written explanation regarding the current hold placed on funds associated with our corporate entity, 10839477 Canada Inc. (Business Number: 749810883RC0001). 

The referenced transaction record (TD-TRX-2026-0928-CORP), representing the $5,000,000.00 CAD treasury deposit, has been fully reconciled. Please be advised that all corporate documentation, asset valuations, and audit logs surrounding this capital have been cryptographically time-stamped and sealed via secure, immutable ledger verification (Manifest Seal: afbcb410debe7deba3b41a08a780be4c55d9627362b7742699f71149dcf5992c).

The continued lack of transparency and unjustified restriction of corporate liquidity is impeding active business operations. We require the following within 48 business hours:
1. A clear, written justification for the current hold on these funds.
2. The specific compliance or administrative requirements needed to lift the hold immediately.
3. Direct contact information for the compliance officer or department currently managing this file.

We expect a prompt, formal response to resolve this matter expediently.

Sincerely,

Jujita Fermin Stairs  
Sole Owner & Individual with Significant Control  
10839477 Canada Inc.
"""

def hash_notice():
    print("\n================================================================")
    print("      ESCALATION NOTICE CRYPTOGRAPHIC HASH GENERATOR          ")
    print("================================================================")
    
    # Compute SHA-256
    notice_hash = hashlib.sha256(escalation_text.encode('utf-8')).hexdigest()
    
    record = {
        "entity": "10839477 Canada Inc.",
        "business_number": "749810883RC0001",
        "recipient": "TD Bank Commercial / Treasury Services",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "notice_sha256": notice_hash
    }
    
    # Save record to JSON
    output_filename = "escalation_notice_proof.json"
    with open(output_filename, "w") as f:
        json.dump(record, f, indent=2)
        
    print(f"  * Status: Message hashed successfully.")
    print(f"  * SHA-256 Hash: {notice_hash}")
    print(f"  * Proof File Saved: {output_filename}")
    print("================================================================\n")

if __name__ == "__main__":
    hash_notice()

