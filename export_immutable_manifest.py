import json
import glob
import hashlib
import datetime
import os

print("=== GENERATING IMMUTABLE AUDIT MANIFEST ===")

manifest = {
    "manifest_version": "1.0.0",
    "generation_timestamp": datetime.datetime.now().isoformat(),
    "jurisdiction": "Canada (AB)",
    "audit_components": []
}

# Files to include in the manifest audit bundle
target_files = [
    "td_routing_profile.json",
    "td_expanded_limits.json"
] + sorted(glob.glob("td_tranche_*_log.json"))

for file_path in target_files:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            file_hash = hashlib.sha256(file_bytes).hexdigest()
        
        with open(file_path, "r") as f:
            content = json.load(f)
            
        manifest["audit_components"].append({
            "filename": file_path,
            "sha256_checksum": file_hash,
            "data": content
        })
        print(f" -> Anchored: {file_path} [{file_hash[:12]}...]")

manifest_filename = "immutable_audit_manifest.json"
with open(manifest_filename, "w") as f:
    json.dump(manifest, f, indent=2)

print("-" * 45)
print(f"Manifest successfully compiled: {manifest_filename}")
print("=" * 45)
