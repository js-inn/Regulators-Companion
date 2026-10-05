import subprocess
from datetime import datetime

def sync_to_github():
    print("[GITHUB BRIDGE] Initiating cloud ledger synchronization...")
    try:
        # Stage all changes including new scripts and databases
        subprocess.run(["git", "add", "-A"], check=True)
        
        timestamp = datetime.now().isoformat()
        commit_msg = f"Cloud Sync: Automated ledger commit at {timestamp}"
        
        # Commit changes
        commit_result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
        
        if "no changes to commit" in commit_result.stdout or "nothing to commit" in commit_result.stdout:
            print("[GITHUB BRIDGE] No new changes to sync. Ledger is up to date.")
            return

        # Push to main
        push_result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, check=True)
        print("[GITHUB BRIDGE] Successfully synchronized ledger with GitHub Cloud!")
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Cloud synchronization failed: {e}")
        if e.stdout: print(e.stdout)
        if e.stderr: print(e.stderr)

if __name__ == "__main__":
    sync_to_github()
