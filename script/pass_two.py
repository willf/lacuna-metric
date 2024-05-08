import json
import os
import re
import sys

import lxml.etree as ET
from lingua_py import Language, LanguageDetectorBuilder

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lacuna_metric.converter import ABConverter, convert_to_test_cases

ld = LanguageDetectorBuilder.from_all_languages().build()


our_namespaces = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",
}

lang_dict = {
    str(Language.Greek): "grc",
    str(Language.Latin): "la",
    str(Language.Arabic): "ara",
}

language_ids_to_keep = ["grc", "la", "cop"]
# unfortunately, there are not enough ar texts to make a good evaluation


def filepath_to_corpus_id(pathname):
    if "idp.data/APD" in pathname:
        return "APD"
    if "idp.data/DCLP" in pathname:
        return "DCLP"
    if "idp.data/DDB_EpiDoc_XML" in pathname:
        return "DDbDP"
    if "edhEpidocDump_" in pathname:
        return "EDH"
    return "unknown"


def read_file(file_path):
    """
    read the file and return the content as an XML document
    """
    with open(file_path, "r") as file:
        return ET.parse(file)


# XML functions


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


def papyri_info_data_path(pathname):
    orig_pathname = pathname
    # Splitting the pathname into parts
    parts = []
    while True:
        parts.append(os.path.basename(pathname))
        pathname, tail = os.path.split(pathname)
        if not tail:
            break
        if os.path.basename(pathname) == "idp.data":
            break
    parts = parts[::-1]  # Reverse to get the correct order

    # Joining the parts again
    joined_path = os.path.join(*parts)
    data_part = orig_pathname.removesuffix(joined_path)
    return data_part


def hgv_filename(doc, filepath):
    """
    given a idno_hgv, return the filename
    the top level folder is source_dir/../HGV_meta_EpiDoc
    the enclosing folder is "HGV" + int(idno_hgv) // 1000 + 1
    the filename is idno_hgv + ".xml"
    to get the top level folder, we need the source_dir, which
    we get from the filepath.
    For example, if the filepath is `/Users/willf/projects/papyri/idp.data/DCLP/990/989335.xml`
    then the top level folder is `/Users/willf/projects/papyri/idp.data/HGV_meta_EpiDoc`
    """
    source_dir = papyri_info_data_path(filepath)
    if source_dir == "/":
        return "unknown"

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


def material_from_hgv(doc, filepath):
    """
    given a idno_hgv, return the material
    """
    hgv_file = hgv_filename(doc, filepath)
    if hgv_file == "unknown":
        return "unknown"
    try:
        # sys.stderr.write(f"Trying to get material from {hgv_file}\n")
        hgv_doc = read_file(hgv_file)
    except ET.ParseError:
        return "unknown"
    except FileNotFoundError:
        sys.stderr.write(f"Error: {hgv_file} not found\n")
        return "unknown"
    return material(hgv_doc, None)


def title(doc):
    """
    extract the title from the teiHeader/fileDesc/titleStmt/title
    """
    title = doc.find(".//tei:title", namespaces=our_namespaces)
    return title.text if title is not None else "unknown"


def material(doc, filepath):
    """
    extract the material from the teiHeader/fileDesc/supportDesc/support/material
    """
    material = doc.find(".//tei:material", namespaces=our_namespaces)
    if material is None and filepath:
        return material_from_hgv(doc, filepath)
    if material is not None and material.text:
        return material.text
    return "unknown"


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


def language(element):
    """
    Return the reported language, or guess"""
    lang = reported_language(element)
    if lang == "unknown":
        text = "".join(element.itertext())
        lang = str(ld.detect_language_of(text))
        if lang in lang_dict:
            return lang_dict[lang]
        return lang
    return lang


def ab_elements(doc):
    return doc.findall(".//tei:ab", namespaces=our_namespaces)


def edition_filter(abs):
    return [ab for ab in abs if is_edition(ab)]


def language_filter(abs):
    return [ab for ab in abs if language(ab) in language_ids_to_keep]


def all_text(element):
    return "".join(element.itertext())


def length_filter(abs):
    return [ab for ab in abs if ab is not None and len(all_text(ab)) >= 10]


def filtered_abs(doc):
    abs = ab_elements(doc)
    # print(f"abs: {len(abs)}")
    abs = edition_filter(abs)
    # print(f"edition: {len(abs)}")
    # print(f"languages: {[reported_language(ab) for ab in abs]} ")
    abs = language_filter(abs)
    # print(f"language: {len(abs)}")
    abs = length_filter(abs)
    # print(f"length: {len(abs)}")
    return abs


def mode(list):
    """
    Return the mode of the list
    """
    if len(list) == 0:
        return 0
    return max(set(list), key=list.count)


def process(file_path):
    """
    main function
    """
    try:
        doc = read_file(file_path)
    except ET.XMLSyntaxError as e:
        sys.stderr.write(f"Error parsing {file_path}. Error: {e}\n")
        return
    except ET.ParseError as e:
        sys.stderr.write(f"Error parsing {file_path}. Error: {e}\n")
        return
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {file_path}\n")
        return
    _material = material(doc, file_path).lower()
    _corpus_id = filepath_to_corpus_id(file_path)
    _file_id = idno(doc)
    _title = title(doc)
    # print("Processing", _file_id, _title, _material)
    for ab in filtered_abs(doc):
        _lang = language(ab)
        # print(f"Original was {ET.tostring(ab, encoding='unicode', pretty_print=True)}")
        converter = ABConverter()
        conversion = converter.convert(ab)
        # print(f"Converting ab element to test cases: {conversion}")
        cases = convert_to_test_cases(conversion)
        # print(f"Found {len(cases)} test cases")
        for c in cases:
            d = {}
            d["corpus_id"] = _corpus_id
            d["file_id"] = _file_id
            d["file_path"] = file_path
            d["title"] = _title
            d["material"] = _material
            d["language"] = _lang
            alts = [a for a in c["alternatives"] if a is not None]
            lengths = [len(a) for a in alts]
            some_none_alt = any(["None" in a for a in c["alternatives"]])
            if "None" not in c["test_case"] and not some_none_alt:
                d["number_alternatives"] = len(alts)
                d["max_length"] = max(lengths)
                d["min_length"] = min(lengths)
                d["mode_length"] = mode(lengths)
                d["test_case"] = c["test_case"]
                d["alternatives"] = alts
                print(json.dumps(d, ensure_ascii=False))
        # print(f"{_corpus_id}\t{_file_id}\t{_title}\t{_material}\t{_lang}")


def main(root_dir):
    # process all files in the directory and its subdirectories
    for root, dirs, files in os.walk(root_dir):
        # print(f"Looking at {root}")
        for file in files:
            # print("Looking at", file)
            if file.endswith(".xml"):
                # print("Processing", file)
                process(os.path.join(root, file))


if __name__ == "__main__":
    # print("CORPUS_ID\tFILE_ID\tTITLE\tMATERIAL\tLANGUAGE".lower())
    for arg in sys.argv[1:]:
        main(arg)
