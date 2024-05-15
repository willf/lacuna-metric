import lxml.etree as ET
import pytest

from lacuna_metric.converter import (
    ABConverter,
    generate_test_ab,
    is_element,
    is_text,
    remove_gaps_from_supplied_text,
)


@pytest.fixture
def converter():
    return ABConverter()


def test_remove_gaps_from_supplied_text():
    assert remove_gaps_from_supplied_text("[abd.efg]") == "[abd].[efg]"
    assert remove_gaps_from_supplied_text("[...]") == "..."
    assert remove_gaps_from_supplied_text("[a]") == "[a]"
    assert remove_gaps_from_supplied_text("[]") == ""
    assert remove_gaps_from_supplied_text("[.]") == "."


def test_post_process(converter):
    text = "\n\n\nTest\n\n\n"
    processed_text = converter.post_process(text)
    assert processed_text == "Test"


def test_ABConvert_init(converter):
    assert not converter.raise_on_error
    assert converter.errors == []


def test_ABConvert_init_raise_on_error():
    converter = ABConverter(raise_on_error=False)
    assert not converter.raise_on_error
    assert converter.errors == []
    converter.convert(23)
    assert len(converter.errors) == 1


def test_default_text(converter):
    el = ET.fromstring("<ab>Test</ab>")
    assert converter.default_text(el) == "Test"


def test_abbr_text(converter):
    el = ET.fromstring('<abbr cert="low">Test</abbr>')
    assert converter.abbr_text(el) == "Test"


def test_add_text(converter):
    el = ET.fromstring("<add>Test</add>")
    assert converter.add_text(el) == "Test"


def create_app_element(type="alternative", lem_text=None, rdg_text=None):
    app_elem = ET.Element("app", type=type)
    if lem_text is not None:
        lem_elem = ET.SubElement(app_elem, "lem")
        lem_elem.text = lem_text
    if rdg_text is not None:
        rdg_elem = ET.SubElement(app_elem, "rdg")
        rdg_elem.text = rdg_text
    return app_elem


def test_app_text_with_lem(converter):
    app_elem = create_app_element(lem_text="lem text")
    assert converter.app_text(app_elem) == "lem text"


def test_app_text_with_rdg(converter):
    app_elem = create_app_element(rdg_text="rdg text")
    assert converter.app_text(app_elem) == "rdg text"


def test_app_text_with_both_lem_and_rdg(converter):
    app_elem = create_app_element(lem_text="lem text", rdg_text="rdg text")
    # Assuming lem has priority when both lem and rdg are present
    assert converter.app_text(app_elem) == "lem text"


def test_app_text_with_neither_lem_nor_rdg(converter):
    app_elem = create_app_element()
    assert converter.app_text(app_elem) == ""
    assert len(converter.errors) == 1


def test_app_text_with_non_alternative_type(converter):
    app_elem = create_app_element(
        type="non-alternative", lem_text="lem text", rdg_text="rdg text"
    )
    assert converter.app_text(app_elem) == ""


def test_choice_test_with_orig(converter):
    choice_elem = ET.fromstring("<choice><orig>orig text</orig></choice>")
    assert converter.choice_text(choice_elem) == "orig text"


def test_choice_test_without_orig(converter):
    choice_elem = ET.fromstring("<choice><corr>corr text</corr></choice>")
    assert converter.choice_text(choice_elem) == ""
    assert len(converter.errors) == 1


def test_gap_text(converter):
    gap_elem = ET.fromstring("<gap reason='illegible' quantity='5' unit='character'/>")
    assert converter.gap_text(gap_elem) == "....."


def test_gap_text_line(converter):
    gap_elem = ET.fromstring("<gap reason='illegible' quantity='1' unit='line'/>")
    assert converter.gap_text(gap_elem) == ("-- " * 10).strip()


def test_gap_text_invalid_quantity(converter):
    gap_elem = ET.fromstring(
        "<gap reason='illegible' quantity='invalid' unit='character'/>"
    )
    assert converter.gap_text(gap_elem) == ""
    assert len(converter.errors) == 1


def test_lb_text(converter):
    lb_elem = ET.fromstring("<lb/>")
    assert converter.lb_text(lb_elem) == "\n"


def test_lb_text_with_break(converter):
    lb_elem = ET.fromstring("<lb break='no'/>")
    assert converter.lb_text(lb_elem) == "\n"


def test_lem_text(converter):
    lem_elem = ET.fromstring("<lem>lem text</lem>")
    assert converter.lem_text(lem_elem) == "lem text"


def test_num_text(converter):
    num_elem = ET.fromstring('<num type="ordinal" value="21">twenty-first</num>')
    assert converter.num_text(num_elem) == "twenty-first"


def test_supplied_text(converter):
    supplied_elem = ET.fromstring('<supplied reason="lost">supplied text</supplied>')
    assert converter.supplied_text(supplied_elem) == "[supplied text]"


def test_supplied_text_with_missing(converter):
    supplied_elem = ET.fromstring('<supplied reason="lost">supplied...text</supplied>')
    assert converter.supplied_text(supplied_elem) == "[supplied]...[text]"


def test_supplied_text_with_other_reason(converter):
    supplied_elem = ET.fromstring(
        '<supplied reason="omitted">supplied...text</supplied>'
    )
    assert converter.supplied_text(supplied_elem) == ""


def test_unclear_text(converter):
    unclear_elem = ET.fromstring("<unclear>unclear text</unclear>")
    assert converter.unclear_text(unclear_elem) == "unclear text"


def test_call():
    converter = ABConverter()
    converter(generate_test_ab())
    assert converter.errors == []


def test_larger_block(converter):
    txt = """
    <ab xml:space="preserve">
      <lb />How do I <supplied reason="lost">love.</supplied>thee? Let me <unclear>count</unclear> the ways
      <lb />I love thee <choice><abbr>2</abbr><expan>to</expan></choice> the depth and breadth and height
      <lb />My soul can reach, when feeling out of <choice><orig>sight</orig><reg>site</reg></choice>
      <lb />For the <app type="alternative"><lem>ends</lem><rdg>enz</rdg></app> of being <choice><sic>&amp;</sic><reg>and</reg></choice> ideal grace
    </ab>
  """.strip()

    el = ET.fromstring(txt)
    result = converter.convert(el).split("\n")
    assert len(result) == 4
    assert result[0] == "How do I [love].thee? Let me count the ways"
    assert result[1] == "I love thee 2 the depth and breadth and height"
    assert result[2] == "My soul can reach, when feeling out of sight"
    assert result[3] == "For the ends of being & ideal grace"
    assert converter.errors == []


def test_removing_missing_chars_at_beginning_and_end(converter):
    txt = """
    <ab xml:space="preserve">
      <lb /><gap reason="illegible" quantity="1" unit="line"/>
      <lb /><gap reason="illegible" quantity="5" unit="character"/>Surely you jest.
      <lb />Don't call me<gap reason="illegible" quantity="1" unit="character"/>Shirley<gap reason="illegible" quantity="3" unit="character"/>
    </ab>
  """.strip()

    el = ET.fromstring(txt)
    result = converter.convert(el)
    assert result == "Surely you jest.\nDon't call me.Shirley"
    assert converter.errors == []
