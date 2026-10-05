import json
import datetime

tranche_data = {
    "batch_sequence": "01",
    "transaction_date": datetime.date.today().isoformat(),
    "amount": 3000.00,
    "currency": "CAD",
    "destination": {
        "institution": "001",
        "transit": "00149",
        "account": "1928-814"
    },
    "status": "Staged for daily limit execution"
}

with open("tranche_01_log.json", "w") as f:
    json.dump(tranche_data, f, indent=2)

print("Tranche 1 logged successfully: $3,000.00 CAD ready for staging.")
