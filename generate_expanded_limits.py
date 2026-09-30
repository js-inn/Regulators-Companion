import json
import datetime

expanded_profile = {
    "profile_name": "TD All-Inclusive - Expanded Tier Target",
    "updated_date": datetime.date.today().isoformat(),
    "institution_coordinates": {
        "bank": "TD Canada Trust",
        "institution_number": "004",
        "transit_number": "82389",
        "account_number": "6215155",
        "payments_canada_acss": "000482389"
    },
    "target_velocity_limits": {
        "currency": "CAD",
        "per_transaction_cap": 10000.00,
        "daily_rolling_limit": 10000.00,
        "weekly_rolling_limit": 35000.00,
        "monthly_rolling_limit": 100000.00
    },
    "status": "Staged for telephone/branch authorization review"
}

with open("td_expanded_limits.json", "w") as f:
    json.dump(expanded_profile, f, indent=2)

print("Expanded limit tracking profile successfully generated.")
