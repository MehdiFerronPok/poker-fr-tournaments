from normalize.normalizer import normalize_event


def test_normalize_event():
    raw = {
        "title": "Test Event",
        "start": "2025-09-25T20:00:00+02:00",
        "end": "2025-09-25T23:00:00+02:00",
        "buy_in": "100 €",
        "variant": "No Limit Hold'em",
        "venue_name": "Test Casino",
        "city": "Paris",
        "source_url": "https://example.com",
        "source_hash": "abc123",
    }
    ev = normalize_event(raw)
    assert ev["title"] == "Test Event"
    assert ev["buy_in_cents"] == 10000
    assert ev["variant"] == "Holdem"
    assert ev["start"].tzinfo is not None
