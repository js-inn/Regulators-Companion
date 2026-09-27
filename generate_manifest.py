import sqlite3, os, json, hashlib
from datetime import datetime, timezone

target_db = None
for root, dirs, files in os.walk("/"):
    if "audit_ledger.db" in files:
        full_path = os.path.join(root, "audit_ledger.db")
        try:
            conn = sqlite3.connect(full_path)
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='audit_nodes'")
            if cursor.fetchone()[0] > 0:
                cursor.execute("SELECT count(*) FROM audit_nodes")
                if cursor.fetchone()[0] > 0:
                    target_db = full_path
                    conn.close()
                    break
            conn.close()
        except:
            pass

if target_db:
    print(f"[+] Found populated database at: {target_db}")
    conn = sqlite3.connect(target_db)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, msg_id, contract_ref, creator_uuid, tx_status, payload_json, sha256_hash FROM audit_nodes ORDER BY id ASC")
    rows = cursor.fetchall()
    nodes = []
    for row in rows:
        node_id, timestamp, msg_id, contract_ref, creator_uuid, tx_status, payload_json, sha256_hash = row
        try: parsed_payload = json.loads(payload_json)
        except: parsed_payload = payload_json
        nodes.append({
            "NodeID": node_id, "Timestamp": timestamp, "MessageID": msg_id,
            "ContractReference": contract_ref, "CreatorUUID": creator_uuid,
            "Status": tx_status, "Payload": parsed_payload, "NodeSHA256": sha256_hash
        })
    master_manifest = {
        "AuditTarget": "Canadian Financial, Regulatory & Disclosure Apparatus",
        "AuditorEntity": "10839477 Canada Inc.",
        "ExportTimestamp": datetime.now(timezone.utc).isoformat(),
        "TotalNodes": len(nodes), "Nodes": nodes
    }
    manifest_json_str = json.dumps(master_manifest, sort_keys=True, separators=(",", ":"))
    master_hash = hashlib.sha256(manifest_json_str.encode("utf-8")).hexdigest()
    master_manifest["MasterLedgerSHA256"] = master_hash
    
    with open("sovereign_audit_master_manifest.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(master_manifest, indent=2, sort_keys=True))
    conn.close()
    print(f"[+] Successfully exported {len(nodes)} nodes to sovereign_audit_master_manifest.json!")
else:
    print("[-] Could not locate the populated database containing audit_nodes.")
