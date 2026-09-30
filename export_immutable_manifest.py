import json
import hashlib
import datetime
import os

print("=== GENERATING IMMUTABLE AUDIT MANIFEST ===")

files_to_anchor = [
    "td_routing_profile.json",
    "td_expanded_limits.json",
    "td_tranche_01_log.json",
    "td_tranche_02_log.json",
    "td_disbursement_cpa005.txt"
]

manifest = {
    "manifest_version": "1.0.0",
    "generation_timestamp": datetime.datetime.now().isoformat(),
    "audit_components": []
}

for file_path in files_to_anchor:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()
            
        manifest["audit_components"].append({
            "filename": file_path,
            "sha256_checksum": file_hash
        })
        print(f" -> Anchored: {file_path} [{file_hash[:12]}...]")
    else:
        print(f" [WARNING] {file_path} not found on disk, skipping.")

manifest_filename = "immutable_audit_manifest.json"
with open(manifest_filename, "w") as f:
    json.dump(manifest, f, indent=2)

print("-" * 45)
print(f"Manifest successfully compiled: {manifest_filename}")
print("=" * 45)
