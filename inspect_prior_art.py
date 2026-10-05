import json

try:
    with open(".prior_art_mapping.json", "r") as f:
        mapping = json.load(f)

    print("=== Prior Art Mapping Details ===")
    for kw, files in mapping.items():
        print(f"\nKeyword: '{kw.upper()}' ({len(files)} matching files)")
        # Display up to 10 files per keyword category
        for file in files[:10]:
            print(f"   - {file}")
        if len(files) > 10:
            print(f"   ... and {len(files) - 10} more files.")

except FileNotFoundError:
    print("[-] .prior_art_mapping.json not found. Make sure prior_art_scanner.py was run first.")

