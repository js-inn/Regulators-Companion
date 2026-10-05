import json
import os

def locate_and_read_report():
    target_file = ".pipeda_audit_report.json"
    found_path = None

    # Search common directories in Termux / Pydroid storage
    search_dirs = [
        "/data/data/com.termux/files/home/jujita-stairs-ip-declaration",
        "/data/data/com.termux/files/home",
        "/data/user/0/ru.iiec.pydroid3/files",
        "."
    ]

    for d in search_dirs:
        full_path = os.path.join(d, target_file)
        if os.path.exists(full_path):
            found_path = full_path
            break

    # Fallback: deep search if not found in common paths
    if not found_path:
        for root, dirs, files in os.walk("/data/data/com.termux"):
            if target_file in files:
                found_path = os.path.join(root, target_file)
                break

    if found_path:
        print(f"[+] Found report at: {found_path}")
        with open(found_path, "r") as f:
            report = json.load(f)

        print("\n=== Audit Report Summary ===")
        print(f"Timestamp: {report.get('audit_timestamp')}")
        print(f"Total Files Scanned: {report.get('total_files_scanned')}")
        print("\nSample of First 10 Scanned Documents:")

        for doc in report.get('documents', [])[:10]:
            print(f" - [{doc.get('status')}] {doc.get('file_name')} ({doc.get('size_bytes')} bytes) | Perms: {doc.get('permissions')}")
    else:
        print("[-] Report not found anywhere on searchable paths. Let's re-run the audit script directly in Termux first.")

if __name__ == "__main__":
    locate_and_read_report()

