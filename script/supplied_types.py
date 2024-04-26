import os
import sys
import xml.etree.ElementTree as ET


def get_all_supplied_elements(xml_file):
    """
    Get all supplied elements from an XML file.
    Anywhere in the tree, not just the root.

    """
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        sys.stderr.write(f"Error parsing {xml_file}\n")
        return []
    root = tree.getroot()
    return root.findall(".//supplied", namespaces={"": "http://www.tei-c.org/ns/1.0"})


def main(root_dir):
    # process all files in the directory and its subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # sys.stderr.write(f"Processing {os.path.join(root, file)}\n")
            if file.endswith(".xml"):
                els = get_all_supplied_elements(os.path.join(root, file))
                for el in els:
                    reason = el.get("reason", "unknown")
                    # viewable = ET.tostring(el, encoding="unicode")
                    print(reason)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        main(arg)
