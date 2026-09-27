import xml.etree.ElementTree as ET
import json
import sys

def parse_iso20022_xsd(xsd_path):
    print(f"[*] Parsing ISO 20022 schema: {xsd_path}")
    
    try:
        tree = ET.parse(xsd_path)
        root = tree.getroot()
    except Exception as e:
        print(f"[-] Error loading XML file: {e}")
        return

    ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    elements = []
    complex_types = []

    for elem in root.findall('xs:element', ns):
        name = elem.get('name')
        type_ref = elem.get('type')
        elements.append({
            "Name": name,
            "Type": type_ref
        })

    for ct in root.findall('xs:complexType', ns):
        ct_name = ct.get('name')
        child_elements = []
        
        for seq in ct.findall('.//xs:sequence/xs:element', ns):
            child_elements.append({
                "ElementName": seq.get('name'),
                "DataType": seq.get('type'),
                "MinOccurs": seq.get('minOccurs', '1'),
                "MaxOccurs": seq.get('maxOccurs', '1')
            })
            
        complex_types.append({
            "ComplexTypeName": ct_name,
            "ChildElements": child_elements
        })

    schema_map = {
        "TargetNamespace": root.get('targetNamespace'),
        "GlobalElements": elements,
        "ComplexTypesCount": len(complex_types),
        "ComplexTypes": complex_types
    }

    output_file = "iso20022_schema_parsed.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(schema_map, f, indent=2)

    print(f"[+] Successfully parsed schema!")
    print(f"[+] Found {len(elements)} global elements and {len(complex_types)} complex type structures.")
    print(f"[+] Saved structured map to {output_file}")

if __name__ == "__main__":
    target_xsd = "pacs.002.001.10.xsd" 
    parse_iso20022_xsd(target_xsd)
