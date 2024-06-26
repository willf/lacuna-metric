import json
import re

import lxml
import lxml.etree as ET
from lxml.etree import QName

from lacuna_metric.utils import (
    children,
    is_element,
    is_text,
    mode_length,
    replace_element,
    replace_element_with_text,
    tag_localname,
    to_string,
)


def generate_test_ab():
    """
    Generate a test abstract element
    """
    text = """
    <ab xmlns="http://www.tei-c.org/ns/1.0" xml:space="preserve">
    <lb n="1"/><gap reason="lost" extent="unknown" unit="line"/>
    <lb n="1"/><gap reason="lost" extent="unknown" unit="character"/><gap reason="illegible" quantity="2" unit="character"/><gap reason="lost" extent="unknown" unit="character"/><gap reason="illegible" quantity="1" unit="character"/><gap reason="lost" extent="unknown" unit="character"/>
    <lb n="2"/><gap reason="illegible" quantity="5" unit="character"/><gap reason="lost" quantity="5" unit="character"/> <app type="alternative"><lem>ὠνουμένη</lem><rdg>ὠνουμένῃ</rdg></app> <app type="alternative"><lem>Ἰ<unclear>σ</unclear>α<supplied reason="lost">ροῦς</supplied></lem><rdg>Ἰ<unclear>σ</unclear>ά<supplied reason="lost">ριον</supplied></rdg></app><gap reason="lost" quantity="1" unit="character"/><gap reason="illegible" quantity="1" unit="character"/><unclear>ν</unclear> <gap reason="lost" quantity="3" unit="character"/>ρχοντ<gap reason="lost" quantity="1" unit="character"/><unclear>ν</unclear><gap reason="lost" extent="unknown" unit="character"/><supplied reason="lost">πηχῶν κατ’</supplied>
    <lb n="3"/>ἐμβαδ<supplied reason="lost">ὸ</supplied>ν <num value="60">ἑβδομήκοντα</num> <supplied reason="lost">ἢ ὅ</supplied>σω<unclear>ν</unclear> ἐὰν ὦσι <gap reason="illegible" quantity="1" unit="character"/><gap reason="lost" extent="unknown" unit="character"/> <supplied reason="lost">καὶ χρηστηρίων καὶ</supplied>
    <lb n="4"/>ἀνηκόντων <unclear>πάν</unclear>των καὶ ε<supplied reason="lost">ἰ</supplied><unclear>σόδ</unclear>ο<unclear>υ</unclear> καί ἐξόδου ὧ<unclear>ν</unclear> <supplied reason="lost">ὅλων γείτονες νότου οἰκία Πα</supplied>
    <lb n="5" break="no"/>θώτου, λιβὸς δημοσία ῥύμη ἐν ᾗ εἴσοδος καὶ ἔξ<supplied reason="lost">οδος τῆς οἰκίας δεῖνος</supplied>
    <lb n="6"/>Παήσιος βορρᾶ οἱ λοιποὶ τόποι τῆς ὠνουμένης Ἰ<unclear>σα</unclear>ρ<gap reason="lost" quantity="1" unit="character"/><gap reason="illegible" quantity="8" unit="character"/><gap reason="lost" quantity="1" unit="character"/><gap reason="illegible" quantity="1" unit="character"/><gap reason="lost" extent="unknown" unit="character"/>
    <lb n="7" break="no"/>των ὄντων ἐν τοῖς ἀπὸ βορρᾶ πρὸς λίβα μέρ<supplied reason="lost">εσι</supplied>  τ<unclear>ῆς</unclear> <supplied reason="lost">κ</supplied>ώμη<supplied reason="lost">ς</supplied> <gap reason="lost" extent="unknown" unit="character"/>
    <lb n="8"/>Πατρὴ <choice><reg>κάτω</reg><orig>κάτωι</orig></choice>, τ<supplied reason="lost">ὴν</supplied> δὲ συνπεφων<supplied reason="lost">ημ</supplied>ένην τιμὴν ἀργ<supplied reason="lost">υρίου σεβαστοῦ νομίσμα</supplied>
    <lb n="9" break="no"/>τος δραχμὰς <num value="300">τρ<supplied reason="lost">ια</supplied>κοσίας</num> ἀπεσχη<unclear>κ</unclear><supplied reason="lost">έ</supplied>ναι τὸν πωλοῦν<unclear>τ</unclear><supplied reason="lost">α</supplied> <gap reason="lost" extent="unknown" unit="character"/> <supplied reason="lost">παρὰ τῆς ὠνου</supplied>
    <lb n="10" break="no"/>μένης διὰ <choice><reg>χειρὸς</reg><orig>χειρὰς</orig></choice> καὶ εἶναι τὴν τοῦ πεπραμένου ψιλοῦ τόπ<supplied reason="lost">ου κυρείαν καὶ κρά</supplied>
    <lb n="11" break="no"/><supplied reason="lost">τησι</supplied>ν περὶ τ<supplied reason="lost">ὴν</supplied> <unclear>ὠ</unclear><supplied reason="lost">νου</supplied>μένη<unclear>ν</unclear> <supplied reason="lost">κ</supplied>αὶ τοὺ<supplied reason="lost">ς πα</supplied>ρʼ αὐτῆς χ<unclear>ρ</unclear><supplied reason="lost">ωμένους</supplied> <gap reason="lost" extent="unknown" unit="character"/>
    </ab>
    """
    ab_element = ET.fromstring(text)
    return ab_element


def in_supplied_element(element):
    """
    Check if an element is inside a supplied element
    """
    if element.tag == "supplied":
        return True
    if element.getparent() is None:
        return False
    return in_supplied_element(element.getparent())


def test_context(element):
    """
    What is the test context of an element?
    """
    if in_supplied_element(element):
        return "evaluation"
    return "context"


def remove_gaps_from_supplied_text(text):
    """
    If there is a . inside brackets, move it outside, creating new brackets.
    >>> remove_gaps_from_supplied_text("[abd.efg]")
    "[abd].[efg]"
    >>> remove_gaps_from_supplied_text("[abd....efg.....hij]")
    "[abd]....[efg].....[hij]"
    >>> remove_gaps_from_supplied_text("[...abd...efg...hij...]")
    "...[abd]...[efg]...[hij]..."
    >>> remove_gaps_from_supplied_text("[]")
    ''
    >>> remove_gaps_from_supplied_text("[.]")
    "."
    >>> remove_gaps_from_supplied_text("[a]")
    "[a]"
    """
    # first, let's remove the outer brackets
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    # ensure there are no brackets inside brackets
    if "[" in text:
        raise ValueError(f"Nested brackets in {text}")
    if "]" in text:
        raise ValueError(f"Nested brackets in {text}")
    # let's place brackets around the non-dot groups
    return re.sub(r"([^.]+)", r"[\1]", text)


class ABConverter:
    """
    A converter for anonymous block elements. We _convert to a Leiden-like format.
    With the following differences:
    - We do not include the line number in the output
    - All `lb` elements are replaced with just a newline character.
    - Original text only.
    """

    def __init__(self, raise_on_error=False):
        self.raise_on_error = raise_on_error
        self.errors = []

    def error(self, err):
        """
        Record an error. Raise an exception if raise_on_error is True.
        """
        self.errors.append(err)
        if self.raise_on_error:
            raise err

    def post_process(self, text):
        """
        Post-process the text. Remove wholly empty lines.
        """

        def is_empty_line(line):
            return re.match(r"(-- )+", line)

        lines = [
            line
            for line in text.split("\n")
            if line and not line.isspace() and not is_empty_line(line)
        ]
        txt = "\n".join(lines)
        # remove leading and trailing '.' characters
        txt = txt.strip(".")
        # wrap in a <ab> element
        txt = f"<ab>{txt}</ab>"
        return txt

    def convert(self, element):
        """
        Convert an element to supplied-only Leiden format.
        """
        return self.post_process(self._convert(element))
        # return "".join(list(self._convert(element)))

    def _convert(self, element):
        """
        Convert an element to text.
        """
        if is_text(element):
            return element
        if not (is_element(element)):
            self.error(
                ValueError(
                    f"Expected text or element, got {element} of type {type(element)}"
                )
            )
            return ""
        match tag_localname(element):
            case "ab":
                return self.default_text(element)
            case "abbr":
                return self.abbr_text(element)
            case "add":
                return self.add_text(element)
            case "del":
                return ""
            case "app":
                return self.app_text(element)
            case "certainty":
                return ""
            case "choice":
                return self.choice_text(element)
            case "del":
                return self.default_text(element)
            case "expan":
                return ""
            case "figure":
                return ""
            case "foreign":
                return self.default_text(element)
            case "g":
                return ""
            case "gap":
                return self.gap_text(element)
            case "handShift":
                return ""
            case "hi":
                return self.default_text(element)
            case "lb":
                return self.lb_text(element)
            case "lem":
                return self.lem_text(element)
            case "milestone":
                return ""
            case "note":
                return ""
            case "num":
                return self.num_text(element)
            case "orig":
                return self.default_text(element)
            case "q":
                return self.default_text(element)
            case "seg":
                return self.default_text(element)
            case "sic":
                return self.default_text(element)
            case "subst":
                return self.default_text(element)
            case "supplied":
                return self.supplied_text(element)
            case "surplus":
                return self.default_text(element)
            case "unclear":
                return self.unclear_text(element)
            case "lem":
                return self.default_text(element)
            case "rdg":
                return self.default_text(element)
            case "hi":
                return self.default_text(element)
            case _:
                return self.default_text(element)
                # raise ValueError(f"No function for tag {element.tag}")

    def default_text(self, element):
        """
        Extract text from an element.
        """
        if element is None:
            return ""
        return "".join([str(self._convert(child)) for child in children(element)])

    def abbr_text(self, element):
        """
        Extract text from abbr elements.
        """
        return self.default_text(element)

    def add_text(self, element):
        """
        Extract text from add elements.
        """
        return self.default_text(element)

    def app_text(self, element):
        """
        Extract text from app elements.
        """
        t = element.get("type", "unknown")
        if t != "alternative":
            return ""
        ok_tags = ["lem", "rdg"]
        return self.text_from_acceptable_children(element, ok_tags)

    def choice_text(self, element):
        """
        Extract text from choice elements. We take the first choice.
        that is an abbr, choice, orig, sic, or unclear element
        """
        ok_tags = ["abbr", "choice", "orig", "sic", "unclear"]
        return self.text_from_acceptable_children(element, ok_tags)

    def text_from_acceptable_children(self, element, acceptable_tags):
        """
        Extract text from acceptable children of an element.
        """
        ok_children = [
            child for child in element if tag_localname(child) in acceptable_tags
        ]
        if test_context(element) == "context":
            if ok_children:
                return self._convert(ok_children[0])
            else:
                self.error(
                    ValueError(
                        f"No acceptable choice; must be one of {', '.join(acceptable_tags)}"
                    )
                )
                return ""
        elif test_context(element) == "evaluation":
            converted = [self._convert(child) for child in ok_children]
            if len(converted) == 1:
                return converted[0]
            else:
                return "<alt>" + "</alt><alt>".join(converted) + "</alt>"
        else:
            self.error(ValueError("Unknown context for choice element"))
            return ""

    def gap_text(self, element):
        """
        Extract text from gap elements.
        """
        if element.get("unit") == "line":
            return "<gap />"
        amt_txt = element.get("quantity", "unknown")
        if amt_txt == "unknown":
            return "<gap />"
        amt = 0
        try:
            amt = int(amt_txt)
        except ValueError:
            self.error(ValueError(f"Invalid quantity: {amt_txt}"))
            return "<gap />"
        return "." * amt

    def lb_text(self, element):
        """
        Extract text from lb elements.
        """
        return "\n"

    def lem_text(self, element):
        """
        Extract text from lem elements.
        """
        return self.default_text(element)

    def num_text(self, element):
        """
        Extract text from num elements.
        """
        return self.default_text(element)

    def supplied_text(self, element):
        """
        Extract text from supplied elements.
        """
        if element.get("reason") in ["lost", "illegible"]:
            repaired = remove_gaps_from_supplied_text(
                "[" + self.default_text(element) + "]"
            )
            # replace brackets with supplied tag
            return re.sub(r"\[([^\[\]]+)\]", r"<supplied>\1</supplied>", repaired)

        else:
            return ""  # some other reason, probably 'omitted' or 'undefined'

    def unclear_text(self, element):
        """
        Extract text from unclear elements.
        """
        return self.default_text(element)

    def __call__(self, element):
        return self.convert(element)


def texts_from_supplied(element):
    """
    Assume there is either only text or alts with only text
    """
    for child in children(element):
        if is_text(child):
            yield child
        else:
            yield child.text


def create_training_text(ab_element):
    """
    Create a training case
     1. find all the supplied elements
     2. for each of these:
        a. find the text of the first alt of the supplied element
        b. replace the supplied element with the text of the first alt
    """
    element = ET.fromstring(ab_element)
    elements = element.findall(".//supplied")
    for supplied in elements:
        base_supplied_values = list(texts_from_supplied(supplied))
        first_alt_text = base_supplied_values[0]
        replace_element_with_text(supplied, f"[{first_alt_text}]")
    return element


def create_test_cases(ab_element):
    """
    Create test cases
    """
    element = ET.fromstring(ab_element)
    elements = element.findall(".//supplied")
    for base in elements:
        others = [el for el in elements if el != base]
        base_supplied_values = list(texts_from_supplied(base))
        base_mode_length = mode_length(base_supplied_values)
        new_base = ET.Element("eval")
        ET.SubElement(new_base, "mask").text = f"[{'.' * base_mode_length}]"
        for supplied_value in base_supplied_values:
            ET.SubElement(new_base, "alt").text = supplied_value
        replace_element(base, new_base)
        for other in others:
            other_values = list(texts_from_supplied(other))
            other_mode_length = mode_length(other_values)
            replace_element_with_text(other, "." * other_mode_length)
        yield element


def convert_to_test_case(original_text, match_object):
    # copy the original text
    text = original_text
    # replace the match with the mask
    text = (
        text[: match_object.start()]
        + "["
        + "." * len(match_object.group(1))
        + "]"
        + text[match_object.end() :]
    )
    # create the alternatives
    alternatives = match_object.group(1).split("|")
    # replace all the other matches with dots
    text = re.sub(
        r"<supplied>([^<]+)</supplied>", lambda m: "." * len(m.group(1)), text
    )
    # remove any newlines
    text = text.strip("\n")
    # remove the <ab> tags
    if text.startswith("<ab>"):
        text = text[4:]
    if text.endswith("</ab>"):
        text = text[:-5]
    # remove any  newlines
    text = text.strip("\n")
    return {"test_case": text, "alternatives": alternatives}


def convert_to_test_cases(original_text):
    """
    Convert an original text to test cases
    """
    return [
        convert_to_test_case(original_text, m)
        for m in re.finditer(r"<supplied>([^<]+)</supplied>", original_text)
    ]


if __name__ == "__main__":
    ab_element = generate_test_ab()
    converter = ABConverter()
    txt = converter.convert(ab_element)
    el = ET.fromstring(txt)
    txt2 = ET.tostring(el, pretty_print=True, encoding="utf-8").decode("utf-8")
    cases = convert_to_test_cases(txt2)
    # display the test cases as JSON with pretty-printing and utf-8 encoding
    print(json.dumps(cases, indent=2, ensure_ascii=False))
