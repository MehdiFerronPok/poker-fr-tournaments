"""
Entry point for all ingestion connectors.

Reads the source catalogue and runs each enabled source. The raw events are
written to a JSON Lines file (`output/raw_events.jsonl`) for consumption by
the normalisation pipeline. Metrics about the run (number of events per
source, duration) are printed to stdout.
"""
from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Iterable, Type

import yaml

from .csv_ingestor import CsvIngestor
from .html_ingestor import HtmlIngestor
from .ics_ingestor import IcsIngestor
from .rss_ingestor import RssIngestor


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


INGESTOR_CLASSES: Dict[str, Type] = {
    "rss": RssIngestor,
    "html": HtmlIngestor,
    "csv": CsvIngestor,
    "ics": IcsIngestor,
}


def load_catalog(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_source(source: Dict) -> Iterable[Dict]:
    typ = source.get("type")
    if typ not in INGESTOR_CLASSES:
        logger.warning("Unknown source type %s", typ)
        return []
    klass = INGESTOR_CLASSES[typ]
    # handle CSV field mapping if provided
    if typ == "csv":
        ingestor = klass(source["url"], source["name"], source.get("field_map", {}))
    else:
        ingestor = klass(source["url"], source["name"])
    return list(ingestor.parse())


def main() -> None:
    catalog_path = Path(__file__).parent / "sources" / "catalog.yml"
    catalog = load_catalog(str(catalog_path))
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "raw_events.jsonl"

    total_events = 0
    metrics = {}
    start_time = time.time()
    with open(output_file, "w", encoding="utf-8") as f:
        for source in catalog.get("sources", []):
            if not source.get("enabled", True):
                continue
            events = run_source(source)
            metrics[source["name"]] = len(events)
            total_events += len(events)
            for ev in events:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    duration = time.time() - start_time
    logger.info("Ingestion complete: %d events from %d sources in %.2fs", total_events, len(metrics), duration)
    for name, count in metrics.items():
        logger.info("  %s: %d events", name, count)


if __name__ == "__main__":
    main()
