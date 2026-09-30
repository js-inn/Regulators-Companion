import json
import hashlib
import os

print("=== VERIFYING IMMUTABLE AUDIT MANIFEST ===")

manifest_filename = "immutable_audit_manifest.json"

if not os.path.exists(manifest_filename):
    print(f"Error: {manifest_filename} not found.")
    exit(1)

with open(manifest_filename, "r") as f:
    manifest = json.load(f)

print(f"Manifest Version: {manifest.get('manifest_version')}")
print(f"Generated At: {manifest.get('generation_timestamp')}")
print("-" * 45)

all_matched = True

for component in manifest.get("audit_components", []):
    file_path = component.get("filename")
    recorded_hash = component.get("sha256_checksum")
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            current_bytes = f.read()
            current_hash = hashlib.sha256(current_bytes).hexdigest()
            
        if current_hash == recorded_hash:
            print(f" [PASS] {file_path}")
            print(f"        Hash: {current_hash[:12]}...")
        else:
            print(f" [FAIL] {file_path} (HASH MISMATCH!)")
            print(f"        Recorded: {recorded_hash[:12]}...")
            print(f"        Current:  {current_hash[:12]}...")
            all_matched = False
    else:
        print(f" [MISSING] {file_path} (File not found on disk)")
        all_matched = False

print("-" * 45)
if all_matched:
    print("Verification Result: SUCCESS (All audit components intact)")
else:
    print("Verification Result: ALERT (Integrity compromise or missing files)")
print("=" * 45)
