"""
Simple endpoint health checks for the API.

This script sends HTTP requests to critical endpoints and reports their
status codes and response times. It can be used in a scheduled job to
detect downtime or slow responses.
"""
from __future__ import annotations

import os
import sys
import time

import requests


API_URL = os.environ.get("API_URL", "http://localhost:8000")


def check_endpoint(path: str, timeout: float = 10.0) -> None:
    url = f"{API_URL}{path}"
    start = time.perf_counter()
    try:
        resp = requests.get(url, timeout=timeout)
        duration = time.perf_counter() - start
        if resp.status_code != 200:
            print(f"ALERT: {path} returned {resp.status_code}")
        else:
            print(f"OK: {path} responded in {duration:.3f}s")
    except Exception as exc:  # noqa: BLE001
        print(f"ALERT: {path} failed with {exc}")


def main() -> None:
    check_endpoint("/health")
    check_endpoint("/tournaments")


if __name__ == "__main__":
    main()
