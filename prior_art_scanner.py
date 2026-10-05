import os
import json

def scan_for_prior_art_keywords():
    target_dir = "."
    keywords = ["ledger", "settlement", "cryptographic", "routing", "ip-manifest", "conditional"]
    matches = {kw: [] for kw in keywords}

    print(f"[*] Scanning local files for prior art and asset mapping keywords...")

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(('.md', '.json', '.txt', '.py')) and not file.startswith('.'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().lower()
                        for kw in keywords:
                            if kw in content:
                                matches[kw].append(file)
                except Exception:
                    pass

    print("\n=== Prior Art & Asset Keyword Mapping ===")
    for kw, flist in matches.items():
        print(f" - Keyword [{kw}]: Found in {len(flist)} local document(s)")

    # Save mapping results
    with open(".prior_art_mapping.json", "w") as f:
        json.dump(matches, f, indent=4)
    print("\n[+] Mapping complete. Saved to .prior_art_mapping.json")

if __name__ == "__main__":
    scan_for_prior_art_keywords()

