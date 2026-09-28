import sqlite3
import json
import os

DB_NAME = "audit_ledger.db"

def init_db(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_file TEXT,
            target_namespace TEXT,
            total_elements INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schema_id INTEGER,
            name TEXT,
            type TEXT,
            min_occurs TEXT,
            max_occurs TEXT,
            FOREIGN KEY (schema_id) REFERENCES schemas (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complex_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schema_id INTEGER,
            complex_type_name TEXT,
            child_count INTEGER,
            FOREIGN KEY (schema_id) REFERENCES schemas (id)
        )
    ''')

def ingest_json_to_db(json_file):
    if not os.path.exists(json_file):
        print(f"[-] File not found: {json_file}")
        return

    print(f"[*] Ingesting {json_file} into SQLite...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    init_db(cursor)

    # Insert schema overview
    cursor.execute('''
        INSERT INTO schemas (target_file, target_namespace, total_elements)
        VALUES (?, ?, ?)
    ''', (data.get("TargetFile"), data.get("TargetNamespace"), data.get("TotalElements")))
    schema_id = cursor.lastrowid

    # Insert elements
    for elem in data.get("Elements", []):
        cursor.execute('''
            INSERT INTO elements (schema_id, name, type, min_occurs, max_occurs)
            VALUES (?, ?, ?, ?, ?)
        ''', (schema_id, elem.get("Name"), elem.get("Type"), elem.get("MinOccurs"), elem.get("MaxOccurs")))

    # Insert complex types
    for ct in data.get("ComplexTypes", []):
        cursor.execute('''
            INSERT INTO complex_types (schema_id, complex_type_name, child_count)
            VALUES (?, ?, ?)
        ''', (schema_id, ct.get("ComplexTypeName"), ct.get("ChildCount")))

    conn.commit()
    conn.close()
    print(f"[+] Successfully loaded {json_file} into database (Schema ID: {schema_id})\n")

if __name__ == "__main__":
    json_files = ["t661_part7_parsed.json", "t5013_schedule12_parsed.json"]
    for jf in json_files:
        ingest_json_to_db(jf)
    print("[*] All targeted compliance schemas successfully vaulted into SQLite!")
