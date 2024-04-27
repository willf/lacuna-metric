import re

import lxml
import lxml.etree as ET


def generate_test_ab():
    """
    Generate a test abstract element
    """
    text = """
    <ab xml:space="preserve">
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


def children(element):
    """
    Get the children of an element, including text items
    """
    if element.text:
        yield element.text
    for child in element:
        yield child
        if child.tail:
            yield child.tail


def is_text(thing):
    """
    Check if an thing is text
    >>> is_text("test")
    True
    >>> is_text(ET.Element("test"))
    False
    """
    return isinstance(thing, str)


def is_element(thing):
    """
    Check if an thing is an element
    >>> is_element(ET.Element("test"))
    True
    >>> is_element("test")
    False
    """
    return isinstance(thing, lxml.etree._Element)


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
        match element.tag:
            case "ab":
                return self.default_text(element)
            case "abbr":
                return self.abbr_text(element)
            case "add":
                return self.add_text(element)
            case "del":
                pass  # ignore
            case "app":
                return self.app_text(element)
            case "certainty":
                pass  # ignore
            case "choice":
                return self.choice_text(element)
            case "del":
                return self.default_text(element)
            case "expan":
                pass  # ignore
            case "figure":
                pass  # ignore
            case "foreign":
                return self.default_text(element)
            case "g":
                pass  # ignore
            case "gap":
                return self.gap_text(element)
            case "handShift":
                pass  # ignore
            case "hi":
                return self.default_text(element)
            case "lb":
                return self.lb_text(element)
            case "lem":
                return self.lem_text(element)
            case "milestone":
                pass  # ignore
            case "note":
                pass  # ignore
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
            case _:
                raise ValueError(f"No function for tag {element.tag}")

    def default_text(self, element):
        """
        Extract text from an element.
        """
        return "".join([self._convert(child) for child in children(element)])

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
        lem = element.find("lem")
        if lem is not None:
            return "".join([self._convert(child) for child in children(lem)])
        rdg = element.find("rdg")
        if rdg is not None:
            return "".join([self._convert(child) for child in children(rdg)])
        self.error(ValueError("No lem or rdg in app element"))
        return ""

    def choice_text(self, element):
        """
        Extract text from choice elements. We take the first choice.
        that is an abbr, choice, orig, sic, or unclear element
        """
        for child in element:
            if child.tag in ["abbr", "choice", "orig", "sic", "unclear"]:
                return self._convert(child)
        self.error(ValueError("No acceptable choice in choice element"))
        return ""

    def gap_text(self, element):
        """
        Extract text from gap elements.
        """
        if element.get("unit") == "line":
            return ("-- " * 10).strip()
        if element.get("quantity") == "unknown":
            return "." * 10
        amt_txt = element.get("quantity") or "10"
        amt = 0
        try:
            amt = int(amt_txt)
        except ValueError:
            self.error(ValueError(f"Invalid quantity: {amt_txt}"))
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
            return remove_gaps_from_supplied_text(
                "[" + self.default_text(element) + "]"
            )
        else:
            return ""  # some other reason, probably 'omitted' or 'undefined'

    def unclear_text(self, element):
        """
        Extract text from unclear elements.
        """
        return self.default_text(element)

    def __call__(self, element):
        return self.convert(element)


if __name__ == "__main__":
    ab_element = generate_test_ab()
    converter = ABConverter()
    print(converter(ab_element))
