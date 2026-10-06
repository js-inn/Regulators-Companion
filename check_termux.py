import os
import sys
import sqlite3
import json

DB_NAME = 'wire_audit.db'
JSON_EXPORT = 'audit_snapshot.json'

def verify_cloud_readiness():
    print("=== PIPELINE & CLOUD READINESS CHECK ===")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Working Directory: {os.getcwd()}")

    # 1. Validate SQLite Availability & Engine
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"[OK] SQLite Database connected. Active tables: {tables}")
        conn.close()
    except Exception as e:
        print(f"[!] SQLite Error: {e}")

    # 2. Check JSON Snapshot Integrity
    if os.path.exists(JSON_EXPORT):
        try:
            with open(JSON_EXPORT, 'r') as f:
                data = json.load(f)
            print(f"[OK] JSON Snapshot loaded successfully ({len(data)} records found).")
        except Exception as e:
            print(f"[!] JSON Parsing Error: {e}")
    else:
        print(f"[MISSING] {JSON_EXPORT} not found in current path.")

    # 3. Environment Variable Check for Cloud Runners
    print("\n--- Environment Audit ---")
    essential_vars = ['GITHUB_ACTIONS', 'CI', 'HOME']
    for var in essential_vars:
        val = os.getenv(var)
        if val:
            print(f"[RUNNER] {var}: {val}")
        else:
            print(f"[LOCAL] {var}: Not set (Running locally)")

    print("=========================================")

if __name__ == "__main__":
    verify_cloud_readiness()
