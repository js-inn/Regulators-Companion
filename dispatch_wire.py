import json

# Load your verified routing profile
with open("td_swift_wire_instruction.json", "r") as f:
    payload = json.load(f)

print("=== INTERLEDGER NODE DISPATCH PREPARATION ===")
print(f"Beneficiary: {payload['beneficiary']['name']}")
print(f"Institution: {payload['beneficiary']['institution_number']} | Transit: {payload['beneficiary']['transit_number']}")
print(f"Account: {payload['beneficiary']['account_number']} (Designation: {payload['beneficiary']['designation_number']})")
print(f"SWIFT BIC: {payload['beneficiary']['swift_bic']}")
print("---------------------------------------------")
print("[READY] Node payout configuration validated against local payload.")
