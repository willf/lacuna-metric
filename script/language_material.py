import os
import re
import sys
import xml.etree.ElementTree as ET

from lingua_py import Language, LanguageDetectorBuilder

ld = LanguageDetectorBuilder.from_all_languages().build()


our_namespaces = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",
}

lang_dict = {
    str(Language.Greek): "grc",
    str(Language.Latin): "lat",
    str(Language.Arabic): "ara",
}

source_dir = "/Users/willf/projects/papyri/idp.data"


def find_parent(root, child):
    """
    Find the parent of a given element
    """
    for parent in root.iter():
        for element in parent:
            if element == child:
                return parent
    return None


def read_file(file_path):
    """
    read the file and return the content as an XML document
    """
    with open(file_path, "r") as file:
        return ET.parse(file)


def idno(doc):
    """
    extract the idno from the teiHeader/fileDesc/publicationStmt/idno[@type='filename']
    with the type 'filename'
    """
    idno = doc.find(".//tei:idno[@type='filename']", namespaces=our_namespaces)
    if idno is None:
        return "unknown"
    return idno.text


def idno_hgv(doc):
    """
    extract the idno from the teiHeader/fileDesc/publicationStmt/idno[@type='HGV']
    with the type 'hgv'
    """
    idno = doc.find(".//tei:idno[@type='HGV']", namespaces=our_namespaces)
    if idno is None:
        return "unknown"
    text = idno.text
    # return the first part of the idno, broken by spaces
    if text is None:
        return "unknown"
    return text.split(" ")[0]


def hgv_filename(doc):
    """
    given a idno_hgv, return the filename
    the top level folder is source_dir/../HGV_meta_EpiDoc
    the enclosing folder is "HGV" + int(idno_hgv) // 1000 + 1
    the filename is idno_hgv + ".xml"
    """
    top_level_folder = os.path.join(source_dir, "HGV_meta_EpiDoc")
    idno = idno_hgv(doc)
    if idno == "unknown":
        return "unknown"
    # get the integer part ... the digits from the start
    integer_part = re.match(r"\d+", idno)
    if integer_part is None:
        return "unknown"
    integer_part = integer_part.group()
    folder = f"HGV{int(integer_part) // 1000}"
    if int(integer_part) % 1000 != 0:
        folder = f"HGV{int(integer_part) // 1000 + 1}"
    filename = f"{idno}.xml"
    return os.path.join(top_level_folder, folder, filename)


def material_from_hgv(doc):
    """
    given a idno_hgv, return the material
    """
    hgv_file = hgv_filename(doc)
    sys.stderr.write(f"Trying to get material from {hgv_file}\n")
    if hgv_file == "unknown":
        return "unknown"
    try:
        hgv_doc = read_file(hgv_file)
    except ET.ParseError:
        return "unknown"
    except FileNotFoundError:
        sys.stderr.write(f"Error: {hgv_file} not found\n")
        return "unknown"
    return material(hgv_doc)


def title(doc):
    """
    extract the title from the teiHeader/fileDesc/titleStmt/title
    """
    title = doc.find(".//tei:title", namespaces=our_namespaces)
    return title.text


def material(doc):
    """
    extract the material from the teiHeader/fileDesc/supportDesc/support/material
    """
    material = doc.find(".//tei:material", namespaces=our_namespaces)
    if material is None:
        return material_from_hgv(doc)
    if material.text:
        return material.text
    return "unknown"


def ab_languages(doc):
    """
    1. For each ab element, extract the language from the xml:lang attribute
    2. If the ab element does not have an xml:lang attribute,
       find the first ancestor element that has an xml:lang attribute
    """
    all_texts = []
    all_languages = []
    for ab in doc.findall(".//tei:ab", namespaces=our_namespaces):
        text = "".join(ab.itertext())
        all_texts.append(text)
    all_texts = " ".join(all_texts)
    language = ld.detect_language_of(all_texts)
    for ab in doc.findall(".//tei:ab", namespaces=our_namespaces):
        text = "".join(ab.itertext()).replace(" ", "")
        if len(text) < 10:
            continue
        lang = ab.get("xml:lang")
        if lang is not None:
            all_languages.append(lang)
            break
        parent = ab
        while parent is not None:
            lang = parent.get("xml:lang")
            if lang is not None:
                all_languages.append(lang)
                break
            parent = find_parent(doc.getroot(), parent)
        if lang is None:
            if language is not None:
                lang = lang_dict.get(str(language), "unknown")
                all_languages.append(lang)
    # remove None values
    all_languages = [lang for lang in all_languages if lang is not None]
    return all_languages


def process(file_path):
    """
    main function
    """
    try:
        doc = read_file(file_path)
    except ET.ParseError:
        # write error message to stderr
        print(f"Error: {file_path} is not a valid XML file", file=sys.stderr)
        return
    except FileNotFoundError:
        print(f"Error: {file_path} not found", file=sys.stderr)
        return
    # print processing information to stderr
    print(f"Processing {file_path}", file=sys.stderr)
    _idno = idno(doc)
    _title = title(doc)
    _material = material(doc).lower()

    languages = ab_languages(doc)
    for lang in languages:
        print(f"{file_path}\t{_idno}\t{_title}\t{_material}\t{lang}")


def main(root_dir):
    print("FILE\tIDNO\tTITLE\tMATERIAL\tLANGUAGE")
    # process all files in the directory and its subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".xml"):
                process(os.path.join(root, file))


if __name__ == "__main__":
    main(sys.argv[1])
