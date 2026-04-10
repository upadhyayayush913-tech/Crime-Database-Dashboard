import xml.etree.ElementTree as ET
import os

def generate_dashboard_xml_safe(source_template, output_file, dataset_file):
    print("Reading XML Base Schema...")
    
    # We must register the user namespace so it doesn't get stripped.
    ET.register_namespace('user', 'http://www.tableausoftware.com/xml/user')
    
    tree = ET.parse(source_template)
    root = tree.getroot()

    # 1. Update the connection path reliably
    print("Wiring Data Sources...")
    for conn in root.iter('connection'):
        if 'filename' in conn.attrib:
            if 'crime_data_cleaned' in conn.attrib['filename']:
                conn.attrib['filename'] = os.path.abspath(dataset_file).replace('\\', '/')

    # 2. Update extract timestamp so Tableau knows it's a fresh schema
    print("Finalizing Generation...")
    for extract in root.iter('extract'):
        for conn in extract.iter('connection'):
            if 'update-time' in conn.attrib:
                conn.attrib['update-time'] = '04/02/2026 12:00:00 PM'

    # Note: We must NOT remove 'SheetIdentifierTracking' or any other tags 
    # from the manifest, as doing so explicitly breaks Tableau's schema validator
    # which relies on these tags to allow elements like <simple-id>.

    # Write the securely generated XML
    xml_str = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
        
    print(f"Successfully generated clean XML workbook: {output_file}")

if __name__ == "__main__":
    generate_dashboard_xml_safe('Tableau miniproject.twb', 'gen.twb', 'crime_data_cleaned.xlsx')
