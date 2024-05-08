import json
import os
import sys

import lxml.etree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lacuna_metric.converter import ABConverter, convert_to_test_cases


def main():
    # walk the trees of the sys.args[1] directory
    for root, dirs, files in os.walk(sys.argv[1]):
        # print("Looking at directory: ", root)
        for file in files:
            # print("Looking at file: ", file)
            # if the file ends with .xml
            if file.endswith(".xml"):
                # open the file
                tree = ET.parse(os.path.join(root, file))
                # print("Converting XML to test cases")
                root = tree.getroot()
                # print("Root tag: ", root.tag)
                xmlns_namespace = root.nsmap[None]
                namespaces = {"tei": xmlns_namespace}
                # print(xmlns_namespace)  # Outputs: http://www.tei-c.org/ns/1.0
                # get the ab elements
                abs = tree.findall(".//tei:ab", namespaces=namespaces)
                # print(f"Found {len(abs)} ab elements")
                for ab in abs:
                    converter = ABConverter()
                    # remove namespace from the ab element
                    conversion = converter.convert(ab)
                    # print(f"Converting ab element to test cases: {conversion}")
                    cases = convert_to_test_cases(conversion)
                    # print(f"Found {len(cases)} test cases")
                    for case in cases:
                        print(json.dumps(case, ensure_ascii=False))


if __name__ == "__main__":
    main()
