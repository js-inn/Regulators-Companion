import os
import hashlib
import json
import tarfile
import subprocess
from datetime import datetime

def generate_file_hash(filepath):
    """Generate SHA-256 hash for a single file efficiently in chunks."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return str(e)

def build_vault_index(target_dir):
    """Recursively map all documents and compute their cryptographic signatures."""
    vault_ledger = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "root_directory": target_dir,
        "files": {}
    }
    
    print(f"[*] Scanning and indexing directory: {target_dir}")
    for root, _, files in os.walk(target_dir):
        for file in files:
            # Skip hidden metadata files or the script itself
            if file.startswith('.') or file == "vault_lock.py":
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, target_dir)
            file_hash = generate_file_hash(full_path)
            
            vault_ledger["files"][rel_path] = {
                "sha256": file_hash,
                "size_bytes": os.path.getsize(full_path)
            }
            
    index_filename = ".vault_index.json"
    with open(index_filename, "w", encoding="utf-8") as f:
        json.dump(vault_ledger, f, indent=4)
        
    print(f"[+] Index successfully written to {index_filename}")
    return index_filename

def encrypt_archive(target_dir, password):
    """Compress the directory and encrypt it using OpenSSL AES-256-CBC."""
    archive_name = "device_vault_payload.tar.gz"
    encrypted_name = "device_vault_payload.tar.gz.enc"
    
    print(f"[*] Compressing {target_dir} into tarball...")
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(target_dir, arcname=os.path.basename(target_dir))
        
    print(f"[*] Applying military-grade AES-256 encryption...")
    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-salt",
        "-in", archive_name,
        "-out", encrypted_name,
        "-k", password
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        # Clean up the unencrypted tarball, leaving only the encrypted vault and index
        os.remove(archive_name)
        print(f"[+] Vault sealed securely: {encrypted_name}")
    else:
        print(f"[-] Encryption error: {result.stderr}")

if __name__ == "__main__":
    # Specify the target directory you want to lock down (e.g., your documents path)
    target_directory = input("Enter path of directory to lock (e.g., ./my_docs): ").strip()
    if not os.path.exists(target_directory):
        print("[-] Directory path does not exist.")
    else:
        vault_password = input("Enter your master decryption passphrase: ").strip()
        build_vault_index(target_directory)
        encrypt_archive(target_directory, vault_password)
        print("[+] Operation complete. Your local device vault is isolated and secured.")

