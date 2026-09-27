import os
import json
import hashlib
from datetime import datetime

MANIFEST_FILE = "sovereign_audit_master_manifest.json"

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest():
    print("[*] Generating master audit manifest...")
    
    # Target artifacts to track in the audit vault
    tracked_extensions = (".json", ".db", ".py", ".xsd")
    nodes = []

    for root, dirs, files in os.walk("."):
        # Skip hidden git directory
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(tracked_extensions) and file != "generate_manifest.py":
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_hash = calculate_sha256(file_path)
                
                nodes.append({
                    "FileName": file,
                    "RelativePath": file_path,
                    "SizeBytes": file_size,
                    "SHA256": file_hash
                })

    manifest_data = {
        "Entity": "10839477 Canada Inc.",
        "Jurisdiction": "Canada",
        "GeneratedAt": datetime.utcnow().isoformat() + "Z",
        "TotalNodes": len(nodes),
        "Nodes": nodes
    }

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    print(f"[+] Master manifest successfully updated: {MANIFEST_FILE}")
    print(f"[+] Total cryptographic audit nodes cataloged: {len(nodes)}")

if __name__ == "__main__":
    generate_manifest()
