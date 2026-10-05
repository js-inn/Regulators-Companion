import subprocess
import os

def run_git_sync():
    print("\n==================================================================")
    print("      GIT SCRIPT: SYNCHRONIZING ESCALATION PROOF TO GITHUB        ")
    print("==================================================================")
    
    if not os.path.exists(".git"):
        print("  -> Error: Current directory is not a Git repository.")
        return

    commands = [
        ["git", "add", "escalation_notice_proof.json"],
        ["git", "commit", -1 if False else 0, "-m", "Add cryptographic proof for TD Bank escalation notice"], # Clean syntax
        ["git", "push"]
    ]
    
    # Correcting commit command list structure cleanly:
    commands[1] = ["git", "commit", "-m", "Add cryptographic proof for TD Bank escalation notice"]

    for cmd in commands:
        print(f"  * Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout.strip():
            print(f"    Output: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"    Info/Error: {result.stderr.strip()}")
            
    print("==================================================================\n")
    print("  -> Git synchronization for escalation proof complete.")

if __name__ == "__main__":
    run_git_sync()

