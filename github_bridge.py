import subprocess
import datetime

def sync_ledger_to_cloud():
    print("[GITHUB BRIDGE] Initiating cloud ledger synchronization...")
    try:
        # Force add the ignored ledger.db file for cloud audit tracking
        subprocess.run(["git", "add", "-f", "ledger.db"], check=True)
        
        # Create commit with timestamp
        timestamp = datetime.datetime.now().isoformat()
        commit_msg = f"Cloud Sync: Automated ledger commit at {timestamp}"
        
        # Check if there are changes to commit first
        status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status_res.stdout.strip():
            print("[GITHUB BRIDGE] No new ledger changes to commit.")
            return

        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Push to GitHub Cloud
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[GITHUB BRIDGE] Successfully synchronized ledger with GitHub Cloud!")
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Cloud synchronization failed: {e}")

if __name__ == "__main__":
    sync_ledger_to_cloud()
