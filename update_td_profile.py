import json

# Load existing profile
try:
    with open("td_routing_profile.json", "r") as f:
        profile = json.load(f)
except FileNotFoundError:
    profile = {}

# Add Payments Canada ACSS electronic routing parameters
profile["payments_canada_routing"] = {
    "clearing_system": "Automated Clearing Settlement System (ACSS)",
    "electronic_routing_string": "000482389",
    "institution_number": "004",
    "transit_number": "82389",
    "account_number": "6215155",
    "currency": "CAD"
}

# Save back to file
with open("td_routing_profile.json", "w") as f:
    json.dump(profile, f, indent=2)

print("TD routing profile successfully updated with Payments Canada ACSS parameters.")
