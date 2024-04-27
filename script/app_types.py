import os
import sys

from lxml import etree as ET


def get_all_app_elements(xml_file):
    """
    Get all app elements from an XML file.
    Anywhere in the tree, not just the root.

    """
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        sys.stderr.write(f"Error parsing {xml_file}\n")
        return []
    root = tree.getroot()
    return root.findall(".//app", namespaces={"": "http://www.tei-c.org/ns/1.0"})


def main(root_dir):
    # process all files in the directory and its subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # sys.stderr.write(f"Processing {os.path.join(root, file)}\n")
            if file.endswith(".xml"):
                els = get_all_app_elements(os.path.join(root, file))
                for el in els:
                    t = el.get("type", "unknown")
                    parent = el.getparent()
                    if parent.tag == "{http://www.tei-c.org/ns/1.0}ab":
                        viewable = (
                            ET.tostring(el, encoding="unicode")
                            .strip()
                            .replace("\n", "")
                        )
                    else:
                        viewable = (
                            ET.tostring(el.getparent(), encoding="unicode")
                            .strip()
                            .replace("\n", "")
                        )
                    print(t, viewable)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        main(arg)
