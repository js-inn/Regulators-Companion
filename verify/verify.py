#!/usr/bin/env python3
"""Standalone integrity verifier for a Regula evidence bundle.

Run this script from the directory containing the extracted evidence files
and manifest.json. It checks SHA-256 hashes of every file listed in the
manifest and reports any mismatches or missing files.

Exit code 0 = all files verified. Exit code 1 = integrity error(s).
"""
import hashlib
import json
import sys
from pathlib import Path


def main():
    manifest_path = Path("manifest.json")
    if not manifest_path.exists():
        print("FAIL: manifest.json not found in current directory")
        sys.exit(1)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files", [])

    if not files:
        print("FAIL: manifest contains no file entries")
        sys.exit(1)

    errors = 0
    for entry in files:
        filename = entry["filename"]
        expected_sha = entry["sha256"]
        if Path(filename).is_absolute() or ".." in Path(filename).parts:
            print(f"  SKIP (invalid path): {filename}", file=sys.stderr)
            continue
        fpath = Path(filename)
        if not fpath.exists():
            print(f"  MISSING: {filename}")
            errors += 1
            continue
        actual_sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
        if actual_sha != expected_sha:
            print(f"  MODIFIED: {filename}")
            errors += 1
        else:
            print(f"  OK: {filename}")

    if errors:
        print(f"FAIL: {errors} integrity error(s)")
        sys.exit(1)
    else:
        print(f"OK: {len(files)} files verified")
        sys.exit(0)


if __name__ == "__main__":
    main()
