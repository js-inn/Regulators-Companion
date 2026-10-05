import subprocess
import os

def run_git_sync():
    print("\n==================================================================")
    print("      GIT SCRIPT: SYNCHRONIZING SOVEREIGN MANIFEST TO GITHUB      ")
    print("==================================================================")
    
    if not os.path.exists(".git"):
        print("  -> Error: Current directory is not a Git repository.")
        return

    commands = [
        ["git", "add", "corporate_sovereign_manifest.json"],
        ["git", "add", "audit_ledger.db"],
        ["git", "commit", "-m", "Sync sovereign audit manifest and verified TD treasury ledger"],
        ["git", "push"]
    ]
    
    for cmd in commands:
        print(f"  * Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout.strip():
            print(f"    Output: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"    Info/Error: {result.stderr.strip()}")
            
    print("==================================================================\n")
    print("  -> Git synchronization workflow complete.")

if __name__ == "__main__":
    run_git_sync()

