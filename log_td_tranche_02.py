import json
import datetime

td_tranche_data_02 = {
    "batch_sequence": "02",
    "transaction_date": datetime.date.today().isoformat(),
    "amount": 3000.00,
    "currency": "CAD",
    "destination": {
        "bank": "TD Canada Trust",
        "institution_number": "004",
        "transit_number": "82389",
        "account_number": "6215155",
        "plan": "TD All-Inclusive Banking Plan"
    },
    "status": "Staged for daily limit execution - Batch 02"
}

with open("td_tranche_02_log.json", "w") as f:
    json.dump(td_tranche_data_02, f, indent=2)

print("TD Tranche 2 logged successfully: $3,000.00 CAD ready for staging.")
