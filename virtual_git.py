#!/usr/bin/env python3
import os
import sys
import hashlib
import json
from datetime import datetime

INDEX_FILE = ".virtual_index.json"

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def virtual_add(file_paths):
    if not os.path.exists(INDEX_FILE):
        index_data = {"author": "Jujita Fermin Stairs", "records": []}
    else:
        with open(INDEX_FILE, "r") as f:
            index_data = json.load(f)

    timestamp = datetime.utcnow().isoformat() + "Z"
    
    for path in file_paths:
        if not os.path.exists(path):
            print(f"[-] File not found: {path}")
            continue
        
        file_hash = calculate_sha256(path)
        if file_hash:
            record = {
                "file": path,
                "sha256": file_hash,
                "staged_at": timestamp,
                "status": "LOCKED - SETTLEMENT PENDING"
            }
            index_data["records"].append(record)
            print(f"[+] Staged (Virtual): {path}")
            print(f"    Hash: {file_hash}")

    with open(INDEX_FILE, "w") as f:
        json.dump(index_data, f, indent=4)
    
    print(f"\n[INFO] Ledger updated successfully in {INDEX_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 virtual_git.py <file1> <file2> ...")
        sys.exit(1)
    
    virtual_add(sys.argv[1:])

