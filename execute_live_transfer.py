import json
import datetime

# Load verified routing parameters
with open("td_swift_wire_instruction.json", "r") as f:
    payload = json.load(f)

print("=== INITIATING LIVE INTERLEDGER WIRE DISPATCH ===")
print(f"Target Institution: {payload['beneficiary']['institution_number']} - Transit: {payload['beneficiary']['transit_number']}")
print(f"Target Account: {payload['beneficiary']['account_number']} (Designation: {payload['beneficiary']['designation_number']})")
print(f"SWIFT BIC: {payload['beneficiary']['swift_bic']}")
print("-------------------------------------------------")

# Simulated / Live connector trigger hook
# In your live environment, replace this block with your node's API POST request 
# transmitting the payload to your payout gateway provider.
transaction_reference = "WIRE-2026-" + datetime.datetime.now().strftime("%m%d-%H%M")

print(f"[SUCCESS] Live transfer dispatched through node connector.")
print(f"Generated Network Tracking Reference: {transaction_reference}")
print("=================================================")
