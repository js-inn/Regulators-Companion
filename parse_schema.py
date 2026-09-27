import xml.etree.ElementTree as ET
import json
import sys
import os

def clean_and_parse_xsd(xsd_path):
    print(f"[*] Parsing Schema: {xsd_path}")
    
    try:
        with open(xsd_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read()
        
        # Strip any leading whitespace or garbage before the XML declaration/root tag
        xml_start = content.find('<')
        if xml_start != -1:
            content = content[xml_start:]
        else:
            print(f"[-] Error: No XML tags found in {xsd_path}")
            return

        root = ET.fromstring(content)
    except Exception as e:
        print(f"[-] Error loading/parsing XML file: {e}")
        return

    ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    elements = []
    complex_types = []

    for elem in root.findall('.//xs:element', ns):
        name = elem.get('name')
        type_ref = elem.get('type')
        min_occurs = elem.get('minOccurs', '1')
        max_occurs = elem.get('maxOccurs', '1')
        if name:
            elements.append({
                "Name": name,
                "Type": type_ref,
                "MinOccurs": min_occurs,
                "MaxOccurs": max_occurs
            })

    for ct in root.findall('.//xs:complexType', ns):
        ct_name = ct.get('name')
        if ct_name:
            child_elements = []
            for seq in ct.findall('.//xs:element', ns):
                child_elements.append({
                    "ElementName": seq.get('name'),
                    "DataType": seq.get('type')
                })
            complex_types.append({
                "ComplexTypeName": ct_name,
                "ChildCount": len(child_elements)
            })

    schema_map = {
        "TargetFile": xsd_path,
        "TargetNamespace": root.get('targetNamespace'),
        "TotalElements": len(elements),
        "Elements": elements,
        "ComplexTypes": complex_types
    }

    base_name = os.path.splitext(os.path.basename(xsd_path))[0]
    output_file = f"{base_name}_parsed.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(schema_map, f, indent=2)

    print(f"[+] Success! Extracted {len(elements)} elements and {len(complex_types)} complex types.")
    print(f"[+] Saved structured map to {output_file}\n")

if __name__ == "__main__":
    for f in os.listdir("."):
        if f.endswith(".xsd"):
            clean_and_parse_xsd(f)
