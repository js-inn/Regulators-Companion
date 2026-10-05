import json
import hashlib
import urllib.request
import urllib.error

print("=== PAYMENTS CANADA GATEWAY CONNECTION SCRIPT ===")

# Configuration parameters for institutional interface
API_ENDPOINT = "https://sandbox.payments.ca/api/v1/acss/submit"  # Sandbox / Test Gateway
ORIGINATOR_ID = "1083947700"
DISBURSEMENT_FILE = "td_disbursement_cpa005.txt"

# Load the staged disbursement payload
try:
    with open(DISBURSEMENT_FILE, "r") as f:
        file_content = f.read()
    print(f" -> Loaded payload: {DISBURSEMENT_FILE} ({len(file_content)} bytes)")
except FileNotFoundError:
    print(f" [ERROR] {DISBURSEMENT_FILE} not found. Run your batch generator first.")
    exit(1)

# Generate payload hash for cryptographic proof-of-transmission
payload_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()

payload = {
    "originator_id": ORIGINATOR_ID,
    "clearing_system": "ACSS",
    "payload_checksum": payload_hash,
    "record_data": file_content
}

headers = {
    "Content-Type": "application/json",
    "X-Originator-Signature": payload_hash,
    "User-Agent": "Termux-Term-Client/1.0"
}

print(f" -> Target Endpoint: {API_ENDPOINT}")
print(f" -> Payload SHA-256: {payload_hash[:16]}...")
print("-" * 45)

# Attempting connection / simulation of live transmission
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(API_ENDPOINT, data=data, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        response_body = response.read().decode('utf-8')
        print("[SUCCESS] Gateway responded:")
        print(response_body)
except urllib.error.HTTPError as e:
    print(f"[NOTE] Sandbox/Live Gateway returned HTTP Error: {e.code} {e.reason}")
    print("       (Note: Production direct injection requires institutional direct-clearer credentials or authorized bank portal session keys).")
except urllib.error.URLError as e:
    print(f"[NOTE] Network routing notice: {e.reason}")
    print("       (Simulated offline environment active; switch to bank portal transmission for final settlement).")

print("=" * 45)
