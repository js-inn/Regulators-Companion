import json
import datetime
import os

print("=== GENERATING CPA STANDARD 005 BATCH FILE ===")

# Load the active tranche log or expanded limits
with open("td_tranche_01_log.json", "r") as f:
    tranche_data = json.load(f)

# CPA Standard 005 parameters (Simulated Originator Profile)
originator_id = "1083947700"  # 10-digit alphanumeric
file_creation_number = "0001"
# Julian date format: 0yyddd
now = datetime.datetime.now()
julian_date = f"0{str(now.year)[-1]}{now.strftime('%j')}"

print(f"Originator ID: {originator_id}")
print(f"File Creation Number: {file_creation_number}")
print(f"Creation Date (Julian): {julian_date}")
print("-" * 45)

# Constructing fixed-length 1464-byte records simulation (Header A)
header_record = f"A000000001{originator_id}{file_creation_number}{julian_date}".ljust(1464)

detail_records = []
total_amount_cents = 0
record_count = 1

# Process items from tranche log
items = tranche_data.get("tranche_items", [
    {"transit": "02389", "institution": "004", "account": "6794682", "amount": 3000.00}
])

for item in items:
    record_count += 1
    seq_str = str(record_count).zfill(9)
    amt_cents = int(round(item["amount"] * 100))
    total_amount_cents += amt_cents
    amt_str = str(amt_cents).zfill(10)
    
    # Financial institution routing: 0 + Transit (5) + Institution (3) = 9-digit format
    inst_routing = f"0{item['transit']}{item['institution']}".zfill(9)
    acc_str = item["account"].ljust(12)
    
    # Detail Record Type 'C' (Credit)
    detail_line = f"C{seq_str}{originator_id}{file_creation_number}470{amt_str}{julian_date}{inst_routing}{acc_str}".ljust(1464)
    detail_records.append(detail_line)
    print(f" -> Added Credit Record: ${item['amount']:.2f} to Account {item['account']}")

# Trailer Record Type 'Z'
record_count += 1
trailer_seq = str(record_count).zfill(9)
total_amt_str = str(total_amount_cents).zfill(14)
trailer_record = f"Z{trailer_seq}{originator_id}{file_creation_number}{total_amt_str}".ljust(1464)

# Write out the CPA 005 disbursement file
output_filename = "td_disbursement_cpa005.txt"
with open(output_filename, "w") as f:
    f.write(header_record + "\n")
    for dr in detail_records:
        f.write(dr + "\n")
    f.write(trailer_record + "\n")

print("-" * 45)
print(f"Disbursement schedule successfully compiled: {output_filename}")
print(f"Total Batch Value: ${total_amount_cents / 100:.2f}")
print("=" * 45)
