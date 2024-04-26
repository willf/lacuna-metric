import os
import re
import sys

import lxml.etree as ET
from lingua_py import Language, LanguageDetectorBuilder

ld = LanguageDetectorBuilder.from_all_languages().build()


our_namespaces = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",
}


def read_file(file_path):
    """
    read the file and return the content as an XML document
    """
    with open(file_path, "r") as file:
        return ET.parse(file)


def is_edition(element):
    """
    Is the current element part of an enclosing div of type 'edition'?
    """
    parent = element.getparent()
    while parent is not None:
        if (
            parent.tag == "{http://www.tei-c.org/ns/1.0}div"
            and parent.get("type") == "edition"
        ):
            return True
        parent = parent.getparent()
    return False


def reported_language(element):
    """
    Extract the language of the current element or the first ancestor with a language attribute.
    """
    while element is not None:
        lang = element.get("{http://www.w3.org/XML/1998/namespace}lang")
        if lang is not None:
            return lang
        element = element.getparent()
    return "unknown"


def ab_types(doc):
    """
    1. For each ab element, extract the type attribute, or "unknown" if it does not exist.
    2. FOr each ab element, extract the tag of its parent element.
    3. For each ab element, extract the type attribute of its parent element, or "unknown" if it does not exist.
    """
    for ab in doc.findall(".//tei:ab", namespaces=our_namespaces):
        ab_type = ab.get("type", "unknown")
        reported_lang = reported_language(ab)
        is_ed = is_edition(ab)

        yield reported_lang, str(is_ed).lower()


def process(file_path):
    """
    main function
    """
    try:
        doc = read_file(file_path)
    except ET.XMLSyntaxError:
        sys.stderr.write(f"Error parsing {file_path}\n")
        return
    except ET.ParseError:
        sys.stderr.write(f"Error parsing {file_path}\n")
        return
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {file_path}\n")
        return
    for (
        reported_lang,
        is_ed,
    ) in ab_types(doc):
        print(f"{file_path}\t{reported_lang}\t{is_ed}")


def main(root_dir):
    # process all files in the directory and its subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".xml"):
                process(os.path.join(root, file))


if __name__ == "__main__":
    print("file\treported_language\tis_edition")
    for arg in sys.argv[1:]:
        main(arg)
