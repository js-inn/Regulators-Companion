import json
import datetime

wire_profile = {
    "instruction_type": "SWIFT_MT103_INBOUND_PAYLOAD",
    "timestamp": datetime.datetime.now().isoformat(),
    "beneficiary": {
        "name": "Jujita Fermin Stairs",
        "institution": "The Toronto-Dominion Bank (TD Canada Trust)",
        "institution_number": "004",
        "transit_number": "02389",
        "account_number": "6794682",
        "designation_number": "779",
        "swift_bic": "TDOMCATTTOR"
    },
    "routing_instructions": {
        "currency": "CAD",
        "destination_clarity": "Explicit corrected routing parameters - Zero ambiguity",
        "compliance_note": "Personal retail tranche routing"
    }
}

with open("td_swift_wire_instruction.json", "w") as f:
    json.dump(wire_profile, f, indent=2)

print("=== PAYLOAD RE-SYNCHRONIZED ===")
