from utils.constants import _parse_person_trackers


def test_parses_id_label_pairs():
    assert _parse_person_trackers("person.a:A,person.b:B") == [("person.a", "A"), ("person.b", "B")]


def test_skips_empty_and_malformed_entries():
    # empty entry, no-colon entry, and missing-id entry are all dropped
    assert _parse_person_trackers("person.a:A,,bogus,:X,person.c:C") == [("person.a", "A"), ("person.c", "C")]


def test_empty_string_yields_empty_list():
    assert _parse_person_trackers("") == []
