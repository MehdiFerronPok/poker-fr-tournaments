from datetime import datetime

from normalize.utils import normalize_variant, parse_buy_in, parse_datetime


def test_parse_datetime_iso():
    iso_str = "2025-09-25T20:00:00+02:00"
    dt = parse_datetime(iso_str)
    assert isinstance(dt, datetime)


def test_parse_buy_in_string():
    assert parse_buy_in("100 €") == 10000
    assert parse_buy_in("50") == 5000
    assert parse_buy_in(None) is None


def test_normalize_variant():
    assert normalize_variant("No Limit Hold'em") == "Holdem"
    assert normalize_variant("Omaha PLO") == "Omaha"
    assert normalize_variant("Mixed") == "Mixed"
    assert normalize_variant(None) is None
