import os
import requests
import json

# Load verified routing instructions
with open("td_swift_wire_instruction.json", "r") as f:
    payload = json.load(f)

# Load API endpoint and credentials from environment
url = os.getenv("GATEWAY_API_URL", "https://sandbox.payout-gateway.com/v1/transfers")
api_key = os.getenv("GATEWAY_API_KEY", "test_key")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("=== TRANSMITTING PAYLOAD TO LIVE GATEWAY ===")
print(f"Endpoint: {url}")
print(f"Beneficiary: {payload['beneficiary']['name']}")
print(f"Institution / Transit: {payload['beneficiary']['institution_number']} - {payload['beneficiary']['transit_number']}")
print(f"Account: {payload['beneficiary']['account_number']} (Designation: {payload['beneficiary']['designation_number']})")
print("--------------------------------------------------")

# Uncomment below to execute live POST request in production
# response = requests.post(url, headers=headers, json=payload)
# if response.status_code == 200:
#     print("[SUCCESS] Transfer accepted by gateway:", response.json())
# else:
#     print(f"[ERROR] Gateway rejected transfer: {response.status_code} - {response.text}")

print("[READY] Dispatch script configured for live network transmission.")
