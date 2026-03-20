import logging
import os
from urllib.parse import urlparse

import requests

from sources import SOURCES

# Sources mapped to output files


# Allow OUTPUT_DIR to be set via environment variable for testability
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "imported")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_host(line):
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
    for name, url in SOURCES.items():
        output_file = os.path.join(OUTPUT_DIR, f"{name}_hosts.txt")

        logging.info(f"\nProcessing source: {name}")

        existing_hosts = set()
        new_hosts = set()

        # Load existing file if it exists
        if os.path.exists(output_file):
            with open(output_file) as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        existing_hosts.add(parts[1])

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                logging.error(f"Failed to fetch {name}")
                continue

            for line in response.text.splitlines():
                host = extract_host(line)

                if host and host not in existing_hosts:
                    new_hosts.add(host)

            # Append new hosts (file is created automatically if it doesn't exist)
            with open(output_file, "a") as f:
                for host in sorted(new_hosts):
                    f.write(f"0.0.0.0 {host}\n")

            logging.info(f"Added {len(new_hosts)} new hosts to {output_file}")

        except Exception as e:
            logging.error(f"Error processing {name}: {e}")


if __name__ == "__main__":
    main()
