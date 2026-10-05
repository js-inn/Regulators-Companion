import os
import json
import stat
from datetime import datetime

class DocumentAuditPipeline:
    def __init__(self, target_directory="."):
        self.target_directory = target_directory
        self.audit_report_file = ".pipeda_audit_report.json"

    def scan_workspace(self):
        """Scans the local directory, mapping files, sizes, and permission states."""
        inventory = []
        scan_timestamp = datetime.utcnow().isoformat() + "Z"

        print(f"[*] Scanning workspace: {os.path.abspath(self.target_directory)}")

        for root, dirs, files in os.walk(self.target_directory):
            # Skip hidden git or system directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue  # Skip hidden config/ledger files
                
                file_path = os.path.join(root, file)
                try:
                    file_stat = os.stat(file_path)
                    file_size = file_stat.st_size
                    
                    # Check POSIX file permissions (e.g., read/write/execute flags)
                    file_mode = stat.filemode(file_stat.st_mode)
                    is_world_readable = bool(file_stat.st_mode & stat.S_IROTH)
                    
                    inventory.append({
                        "file_name": file,
                        "path": file_path,
                        "size_bytes": file_size,
                        "permissions": file_mode,
                        "world_readable": is_world_readable,
                        "status": "EXPOSED" if is_world_readable else "RESTRICTED"
                    })
                except Exception as e:
                    print(f"[-] Error reading {file_path}: {e}")

        report = {
            "audit_timestamp": scan_timestamp,
            "total_files_scanned": len(inventory),
            "documents": inventory
        }

        with open(self.audit_report_file, "w") as f:
            json.dump(report, f, indent=4)

        print(f"[+] Audit complete. Scanned {len(inventory)} documents.")
        print(f"[+] Report saved to {self.audit_report_file}")
        
        # Summary check
        exposed_count = sum(1 for doc in inventory if doc["world_readable"])
        if exposed_count > 0:
            print(f"[!] Warning: {exposed_count} document(s) have world-readable permissions.")
        else:
            print("[+] All tracked documents are locally restricted.")

if __name__ == "__main__":
    auditor = DocumentAuditPipeline()
    auditor.scan_workspace()

