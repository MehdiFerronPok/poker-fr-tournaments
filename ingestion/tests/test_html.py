from pathlib import Path

from ingestion.html_ingestor import HtmlIngestor


def test_html_ingestor_parses_events(tmp_path):
    fixture_path = Path(__file__).parent / "fixtures" / "demo_html.html"
    # Serve the local file via file:// scheme using requests' ability to read local path
    ingestor = HtmlIngestor(fixture_path.as_posix(), source_name="test_html")
    # Monkeypatch the fetch method to just read the file
    ingestor.fetch = lambda: fixture_path.read_text(encoding="utf-8")  # type: ignore
    events = list(ingestor.parse())
    assert len(events) == 2
    for ev in events:
        assert ev["title"]
        assert ev["venue_name"] is not None
        assert ev["source_hash"]
