"""Downloads and normalizes third-party feeds from `sources.SOURCES` into `imported/`.

Usage: `make import` (or `uv run python src/import.py`).
"""

import logging
import os
from urllib.parse import urlparse

import requests

from common import configure_logging
from settings import DEFAULT_IMPORT_OUTPUT_DIR, IMPORT_OUTPUT_DIR_ENV_VAR, PREFIX_TO_CHECK
from sources import SOURCES

configure_logging()

logger = logging.getLogger(__name__)

# Read fresh at this module's own import time (not precomputed in settings.py),
# so a test can still override it per-run via os.environ before importing/
# reloading this module.
OUTPUT_DIR = os.environ.get(IMPORT_OUTPUT_DIR_ENV_VAR, DEFAULT_IMPORT_OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_host(line):
    """Extracts the hostname from a hosts-file, URL, or plain-domain line.

    Args:
        line: A single line from a downloaded feed. Recognized formats are a
            hosts-file entry (`"0.0.0.0 example.com"`), a full URL
            (`"https://example.com/path"`), or a bare domain
            (`"example.com:8080"`).

    Returns:
        The extracted hostname (port stripped), or `None` if the line is
        blank, a comment, or has no extractable host.
    """
    line = line.strip()

    if not line or line.startswith("#"):
        return None

    parts = line.split()

    # Hosts file format
    if len(parts) >= 2 and parts[0] in ["0.0.0.0", "127.0.0.1"]:
        host = parts[1]

    # URL format
    elif line.startswith("http://") or line.startswith("https://"):
        parsed = urlparse(line)
        host = parsed.netloc

    # Plain domain
    else:
        host = parts[0]

    # Remove port
    if ":" in host:
        host = host.split(":")[0]

    return host if host else None


def main():
    """Downloads every feed in `SOURCES` and appends its new hosts to `imported/`.

    For each source: loads the existing `imported/<name>_hosts.txt` (if any)
    to avoid re-adding known hosts, fetches the feed, extracts hostnames from
    every line, and appends the ones not already present. Fetch/parse errors
    for one source are logged and don't stop the others.
    """
    for name, url in SOURCES.items():
        output_file = os.path.join(OUTPUT_DIR, f"{name}_hosts.txt")

        logger.info(f"Processing source: {name}")

        existing_hosts = set()
        new_hosts = set()

        # Load existing file if it exists
        if os.path.exists(output_file):
            with open(output_file, encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        existing_hosts.add(parts[1])

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                logger.error(f"Failed to fetch {name}")
                continue

            for line in response.text.splitlines():
                host = extract_host(line)

                if host and host not in existing_hosts:
                    new_hosts.add(host)

            # Append new hosts (file is created automatically if it doesn't exist)
            with open(output_file, "a", encoding="utf-8") as f:
                for host in sorted(new_hosts):
                    f.write(f"{PREFIX_TO_CHECK} {host}\n")

            logger.info(f"Added {len(new_hosts)} new hosts to {output_file}")

        except Exception as e:
            logger.error(f"Error processing {name}: {e}")


if __name__ == "__main__":
    main()
