"""Validates and dedupes hostnames across the curated lists in `lists/`.

Usage: `make cleanup` (or `uv run python src/cleanup.py`), optionally with `LISTS=a,b,c`
and `CHECK_DOMAIN_DNS=1`/`DNS_WORKERS=N` env vars.
"""

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

import dns.exception
import dns.resolver
import validators

from common import (
    configure_logging,
    delete_file,
    filter_selected_lists,
    get_filenames_without_extension,
    line_has_prefix,
)
from settings import (
    DNS_WORKERS_ENV_VAR,
    LISTS_DIR,
    PREFIX_TO_CHECK,
    check_domain_dns_enabled,
    env_selected_lists,
)

configure_logging()

logger = logging.getLogger(__name__)

# Read fresh at this module's own import time (not precomputed in settings.py),
# so a test can still override it per-run via os.environ before importing/
# reloading this module.
CHECK_DOMAIN_DNS: bool = check_domain_dns_enabled()


def check_line_starts_with(line, prefix):
    """Checks if a line starts with the specified prefix.

    Args:
        line: Line to check.
        prefix: Prefix to look for.

    Returns:
        True if `line` starts with `prefix`, False otherwise.
    """
    return line_has_prefix(line, prefix)


def integrity_message(fname):
    """Logs whether a compiled hosts file exists on disk.

    Args:
        fname: Path to the file expected to have been written.
    """
    if os.path.exists(fname):
        logger.info(f"Hosts file compiled successfully and available in {fname}")
    else:
        logger.error(f"Hosts file couldn't be compiled: {fname}")


def selected_lists(input_lists):
    """Returns the valid lists from the input, or the default ADLISTS.

    Args:
        input_lists: Candidate list names to filter, e.g. from a `LISTS` env
            var.

    Returns:
        The filtered list names, or `ADLISTS` if none of `input_lists`
        matched.
    """
    return filter_selected_lists(input_lists, ADLISTS, ADLISTS_SET)


@lru_cache(maxsize=500_000)
def is_valid_domain_or_ip(value):
    """Checks whether a value is a valid domain name or IP address.

    When `CHECK_DOMAIN_DNS` is enabled, a domain is only considered valid if
    it also resolves via DNS. Results are memoized, since the same domain can
    repeat across many list entries.

    Args:
        value: The domain name or IP address string to validate.

    Returns:
        True if `value` is a valid IPv4/IPv6 address, or a valid domain (and,
        when DNS checking is enabled, one that resolves). False otherwise.
    """
    try:
        if validators.ip_address.ipv4(value):
            return True

        if validators.ip_address.ipv6(value):
            return True

        if not validators.domain(value, consider_tld=True, rfc_1034=True, rfc_2782=True):
            return False

        # Validate domain only if CHECK_DOMAIN_DNS is True
        if CHECK_DOMAIN_DNS:
            try:
                dns.resolver.resolve(value, "A")
            except dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout:
                return False

        return True
    except dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout:
        return False
    except dns.resolver.NoNameservers:
        logger.error(f"No nameservers available for domain: {value}")
        return False


def extract_domain_from_line(line, prefix):
    """Extracts the domain from a line that starts with the given prefix.

    Args:
        line: A raw hosts-file line, e.g. `"0.0.0.0 example.com # comment"`.
        prefix: The expected leading prefix, e.g. `"0.0.0.0"`.

    Returns:
        A `(domain, normalized_line)` tuple, where `normalized_line` is
        `"{prefix} {domain}"` with any trailing comment stripped. Returns
        `(None, None)` if the line doesn't start with `prefix` or has no
        second field.
    """
    normalized = line.split("#", maxsplit=1)[0].strip()
    if not normalized.startswith(prefix):
        return None, None

    parts = normalized.split()
    if len(parts) < 2:
        return None, None

    domain = parts[1].strip()
    normalized_line = f"{prefix} {domain}"
    return domain, normalized_line


def get_max_dns_workers():
    """Returns the worker count for DNS checks, allowing an env override.

    Returns:
        The value of the `DNS_WORKERS` env var if set to a valid positive
        integer; otherwise `min(32, cpu_count * 5)`.
    """
    default_workers = min(32, (os.cpu_count() or 1) * 5)
    raw_workers = os.getenv(DNS_WORKERS_ENV_VAR)
    if not raw_workers:
        return default_workers

    try:
        return max(1, int(raw_workers))
    except ValueError:
        logging.warning(f'Invalid DNS_WORKERS value "{raw_workers}", using default {default_workers}.')
        return default_workers


def process_file(input_file, prefix, log_file):
    """Filters, dedupes, and validates the domains in a list file.

    Reads every line starting with `prefix`, normalizes and dedupes it by
    domain, then validates each domain via `is_valid_domain_or_ip` (in
    parallel when `CHECK_DOMAIN_DNS` is enabled). Invalid domains are
    excluded from the result and recorded to `log_file`.

    Args:
        input_file: Path to the list file to read.
        prefix: The expected leading prefix on each valid line, e.g.
            `"0.0.0.0"`.
        log_file: An open, writable file object to record rejected domains
            to.

    Returns:
        A sorted list of normalized, deduplicated, valid lines.
    """
    # normalized_line is a pure function of (prefix, domain), so a domain never has
    # more than one distinct normalized form: a plain dict is enough, no need for a
    # set-of-one per domain (real savings on multi-million-line lists like basic.txt).
    domain_to_line = {}

    with open(input_file, encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if line and check_line_starts_with(line, prefix):
                domain, normalized_line = extract_domain_from_line(line, prefix)
                if not domain:
                    logger.warning(f'Entry "{domain}" is invalid and it\'s not being included to the list.')
                    continue

                domain_to_line[domain] = normalized_line

    unique_lines = set()

    def accept(domain):
        unique_lines.add(domain_to_line[domain])

    def reject(domain):
        log_file.write(f"{domain} - refused by validators/dns\n")
        logger.warning(f'Domain "{domain}" is invalid and it\'s not being included to the list.')

    # Results are consumed straight into unique_lines/log_file as they arrive, instead
    # of first collecting a second valid/invalid set of domains alongside domain_to_line.
    if CHECK_DOMAIN_DNS:
        max_workers = get_max_dns_workers()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_domain = {executor.submit(is_valid_domain_or_ip, domain): domain for domain in domain_to_line}
            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                accept(domain) if future.result() else reject(domain)
    else:
        for domain in domain_to_line:
            accept(domain) if is_valid_domain_or_ip(domain) else reject(domain)

    return sorted(unique_lines)


def main():
    """Cleans up the selected lists and rewrites them in place.

    Reads the `LISTS` environment variable (or falls back to every list under `lists/`),
    then for each selected list: validates and dedupes its domains, rewrites the list
    file with the result, and logs rejected domains to `log.txt`.
    """
    input_lists = env_selected_lists(ADLISTS)
    selected = selected_lists(input_lists)

    with open("log.txt", "w", encoding="utf-8") as log_file:
        for list_name in selected:
            logger.info(f'Started cleaning "{list_name}" list.')
            file_path = os.path.join(LISTS_DIR, f"{list_name}.txt")

            # Process the file to extract and filter unique lines
            unique_lines = process_file(file_path, PREFIX_TO_CHECK, log_file)

            # If the file exists, delete it
            delete_file(file_path)

            # Write back the filtered, sorted lines to the file
            with open(file_path, "w", encoding="utf-8") as outfile:
                outfile.writelines(f"{line}\n" for line in unique_lines)

            # Output the integrity message
            integrity_message(file_path)


# Global variables
ADLISTS = get_filenames_without_extension(LISTS_DIR)
ADLISTS_SET = set(ADLISTS)

if __name__ == "__main__":
    main()
