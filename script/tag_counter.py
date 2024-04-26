import os
import sys
import xml.etree.ElementTree as ET


def count_tags(ab_element, tag_counter):
    """
    Count the number of tags in an abstract element.
    """
    my_tag = ab_element.tag
    if my_tag in tag_counter:
        tag_counter[my_tag] += 1
    else:
        tag_counter[my_tag] = 1
    for child in ab_element:
        tag = child.tag
        if tag in tag_counter:
            tag_counter[tag] += 1
        else:
            tag_counter[tag] = 1
    return tag_counter


def get_all_ab_elements(xml_file):
    """
    Get all ab elements from an XML file.
    Anywhere in the tree, not just the root.

    """
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        sys.stderr.write(f"Error parsing {xml_file}\n")
        return []
    root = tree.getroot()
    ab_elements = root.findall(".//ab", namespaces={"": "http://www.tei-c.org/ns/1.0"})
    return ab_elements


def count_tags_for_file(xml_file, tag_counter):
    """
    Count the number of tags in all abstract elements in an XML file.
    """
    ab_elements = get_all_ab_elements(xml_file)
    sys.stderr.write(f"Found {len(ab_elements)} ab elements in {xml_file}\n")
    for ab_element in ab_elements:
        tag_counter = count_tags(ab_element, tag_counter)


def main(root_dir):
    tag_counter = {}
    # process all files in the directory and its subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            sys.stderr.write(f"Processing {os.path.join(root, file)}\n")
            if file.endswith(".xml"):
                count_tags_for_file(os.path.join(root, file), tag_counter)
    # order the tags by count, desc
    tag_counter = dict(
        sorted(tag_counter.items(), key=lambda item: item[1], reverse=True)
    )
    # print the tags and their counts
    print("TAG\tCOUNT")

    for tag, count in tag_counter.items():
        # remove the namespace from the tag
        tag = tag.split("}")[1] if "}" in tag else tag
        print(f"{tag}\t{count}")


if __name__ == "__main__":
    main(sys.argv[1])
