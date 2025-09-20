import os
from pathlib import Path

from ingestion.rss_ingestor import RssIngestor


def test_rss_ingestor_parses_entries(tmp_path):
    # Use local fixture file as feed
    fixture_path = Path(__file__).parent / "fixtures" / "demo_rss.xml"
    # feedparser can parse file paths directly
    ingestor = RssIngestor(fixture_path.as_posix(), source_name="test_rss")
    events = list(ingestor.parse())
    assert len(events) == 2
    for ev in events:
        assert ev["title"]
        assert ev["source_hash"]
