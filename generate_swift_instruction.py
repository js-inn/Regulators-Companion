import json
import datetime

print("=== GENERATING SWIFT WIRE INSTRUCTION PAYLOAD ===")

# Personal Account Routing Profile for TD Canada Trust
wire_profile = {
    "instruction_type": "SWIFT_MT103_INBOUND_PAYLOAD",
    "timestamp": datetime.datetime.now().isoformat(),
    "beneficiary": {
        "name": "Jujita Fermin Stairs",
        "institution": "The Toronto-Dominion Bank (TD Canada Trust)",
        "institution_number": "004",
        "transit_number": "23867",
        "account_number": "6794690",
        "swift_bic": "TDOMCATTTOR"
    },
    "routing_instructions": {
        "currency": "CAD",
        "intermediary_handling": "Direct Clearing via TD Head Office Toronto",
        "compliance_note": "Personal retail tranche routing under $3,000 threshold"
    }
}

filename = "td_swift_wire_instruction.json"
with open(filename, "w") as f:
    json.dump(wire_profile, f, indent=2)

print("-" * 45)
print(f" -> Generated Wire Instruction File: {filename}")
print(f" -> SWIFT BIC: {wire_profile['beneficiary']['swift_bic']}")
print(f" -> Institution / Transit: {wire_profile['beneficiary']['institution_number']} / {wire_profile['beneficiary']['transit_number']}")
print("=" * 45)
