import sqlite3
import sys

DB_NAME = "audit_ledger.db"

def search_elements(keyword=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = '''
        SELECT s.target_file, e.name, e.type, e.min_occurs, e.max_occurs
        FROM elements e
        JOIN schemas s ON e.schema_id = s.id
    '''
    
    if keyword:
        query += " WHERE e.name LIKE ? OR e.type LIKE ?"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute(query)
        
    results = cursor.fetchall()
    conn.close()
    
    print(f"\n[*] Found {len(results)} matching element(s):\n")
    print(f"{'SCHEMA':<22} | {'ELEMENT NAME':<30} | {'TYPE':<25} | {'OCCURS'}")
    print("-" * 90)
    
    for row in results:
        schema, name, dtype, min_occ, max_occ = row
        occurs = f"{min_occ}..{max_occ}"
        print(f"{schema:<22} | {name:<30} | {str(dtype):<25} | {occurs}")
    print()

if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else ""
    search_elements(kw)
