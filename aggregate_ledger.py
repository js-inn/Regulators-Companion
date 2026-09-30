import json
import glob
import os

print("=== TD CANADA TRUST AUDIT LEDGER REPORT ===")
print("-" * 45)

# Load Routing Profile
try:
    with open("td_routing_profile.json", "r") as f:
        routing = json.load(f)
    print(f"Institution: {routing.get('payments_canada_routing', {}).get('institution_number')} | "
          f"Transit: {routing.get('payments_canada_routing', {}).get('transit_number')} | "
          f"Account: {routing.get('payments_canada_routing', {}).get('account_number')}")
except FileNotFoundError:
    print("Routing profile not found.")

# Load Expanded Limits
try:
    with open("td_expanded_limits.json", "r") as f:
        limits = json.load(f)
    daily_cap = limits.get("target_velocity_limits", {}).get("daily_rolling_limit", 3000.00)
    print(f"Active Target Daily Cap: ${daily_cap:,.2f} {limits.get('target_velocity_limits', {}).get('currency', 'CAD')}")
except FileNotFoundError:
    daily_cap = 3000.00
    print("Expanded limits profile not found. Defaulting to standard $3,000 limit.")

print("-" * 45)
print("AGGREGATING TRANCHE BATCHES:")

total_staged = 0.0
tranche_files = sorted(glob.glob("td_tranche_*_log.json"))

for file_name in tranche_files:
    with open(file_name, "r") as f:
        data = json.load(f)
        amount = data.get("amount", 0.0)
        total_staged += amount
        print(f" -> Batch {data.get('batch_sequence')} ({data.get('transaction_date')}): ${amount:,.2f} {data.get('currency')} [{data.get('status')}]")

print("-" * 45)
print(f"Total Staged Capital: ${total_staged:,.2f} CAD")
remaining_capacity = daily_cap - total_staged
print(f"Remaining Daily Capacity: ${remaining_capacity:,.2f} CAD")

if total_staged <= daily_cap:
    print("Status: COMPLIANT (Within active velocity limits)")
else:
    print("Status: WARNING (Exceeds current daily cap - Authorization review required)")
print("=" * 45)
