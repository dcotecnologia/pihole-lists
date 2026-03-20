import logging
import logging.config
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

import dns.exception
import dns.resolver
import validators
import yaml


def get_filenames_without_extension(directory):
    """Retrieve filenames without their extensions from the given directory."""
    return [os.path.splitext(filename)[0] for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]


def delete_file(file_path):
    """Delete the file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)


def check_line_starts_with(line, prefix):
    """Check if a line starts with the specified prefix."""
    return line.startswith(prefix)


def integrity_message(fname):
    """Display a message confirming the existence of a file."""
    if os.path.exists(fname):
        print(f"Hosts file compiled successfully and available in {fname}")
    else:
        print(f"Hosts file couldn't be compiled: {fname}")


def selected_lists(input_lists):
    """Return a list of valid lists from the input or use the default ADLISTS."""
    lists = [item for item in input_lists if item in ADLISTS_SET]
    return lists if lists else ADLISTS


@lru_cache(maxsize=500_000)
def is_valid_domain_or_ip(value):
    """Check if the value is a valid domain or an IP address."""
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
        logging.error(f"No nameservers available for domain: {value}")
        return False


def extract_domain_from_line(line, prefix):
    """Extract the domain from a line that starts with the given prefix."""
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
    """Return worker count for DNS checks, allowing env override."""
    default_workers = min(32, (os.cpu_count() or 1) * 5)
    raw_workers = os.getenv("DNS_WORKERS")
    if not raw_workers:
        return default_workers

    try:
        return max(1, int(raw_workers))
    except ValueError:
        logging.warning(f'Invalid DNS_WORKERS value "{raw_workers}", using default {default_workers}.')
        return default_workers


def process_file(input_file, prefix, log_file):
    """Process the file, filtering lines by the given prefix and removing duplicates,
    only if domains are valid."""
    unique_lines = set()
    domain_to_lines = {}
    valid_domains = set()
    invalid_domains = set()

    with open(input_file, encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if line and check_line_starts_with(line, prefix):
                domain, normalized_line = extract_domain_from_line(line, prefix)
                if not domain:
                    logging.warning(f'Entry "{domain}" is invalid and it\'s not being included to the list.')
                    continue

                domain_to_lines.setdefault(domain, set()).add(normalized_line)

    if CHECK_DOMAIN_DNS:
        max_workers = get_max_dns_workers()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_domain = {executor.submit(is_valid_domain_or_ip, domain): domain for domain in domain_to_lines}
            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                if future.result():
                    valid_domains.add(domain)
                else:
                    invalid_domains.add(domain)
    else:
        for domain in domain_to_lines:
            if is_valid_domain_or_ip(domain):
                valid_domains.add(domain)
            else:
                invalid_domains.add(domain)

    for domain in valid_domains:
        unique_lines.update(domain_to_lines[domain])

    for domain in invalid_domains:
        log_file.write(f"{domain} - refused by validators/dns\n")
        logging.warning(f'Domain "{domain}" is invalid and it\'s not being included to the list.')

    return sorted(unique_lines)


def main():
    """Main execution flow to process the lists and update the hosts files."""
    input_lists = [item.strip() for item in os.getenv("LISTS", ",".join(ADLISTS)).split(",") if item.strip()]
    selected = selected_lists(input_lists)

    with open("log.txt", "w", encoding="utf-8") as log_file:
        for list_name in selected:
            logging.info(f'Started cleaning "{list_name}" list.')
            file_path = f"lists/{list_name}.txt"

            # Process the file to extract and filter unique lines
            unique_lines = process_file(file_path, PREFIX_TO_CHECK, log_file)

            # If the file exists, delete it
            delete_file(file_path)

            # Write back the filtered, sorted lines to the file
            with open(file_path, "w", encoding="utf-8") as outfile:
                outfile.write("\n".join(unique_lines) + "\n")

            # Output the integrity message
            integrity_message(file_path)


# Global variables
ADLISTS = get_filenames_without_extension("lists")
ADLISTS_SET = set(ADLISTS)
PREFIX_TO_CHECK = "0.0.0.0"
CHECK_DOMAIN_DNS: bool = bool(int(os.getenv("CHECK_DOMAIN_DNS", 0)))

if __name__ == "__main__":
    with open(".log-config.yml") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    main()
