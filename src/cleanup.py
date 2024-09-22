import logging
import logging.config
import os

import dns.exception
import dns.resolver
import validators
import yaml


def get_filenames_without_extension(directory):
    """Retrieve filenames without their extensions from the given directory."""
    return [
        os.path.splitext(filename)[0]
        for filename in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, filename))
    ]


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


def selected_lists(input):
    """Return a list of valid lists from the input or use the default ADLISTS."""
    lists = [item for item in input if item in ADLISTS]
    return lists if lists else ADLISTS

def is_valid_domain_or_ip(value):
    """Check if the value is a valid domain or an IP address."""
    try:
        with open("log.txt", 'w') as log:
            if validators.ip_address.ipv4(value):
                return True

            if validators.ip_address.ipv6(value):
                return True

            if not validators.domain(value, consider_tld=True, rfc_1034=True, rfc_2782=True):
                logging.warning(f"Domain \"{value}\" is invalid.")
                log.write(f"{value} - refused by validators \n")
                return False

            # Validate domain only if CHECK_DOMAIN_DNS is True
            if CHECK_DOMAIN_DNS:
                try:
                    dns.resolver.resolve(value, 'A')
                    return True  # Domain resolves to an IP
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
                    log.write(f"{value} - refused by dns \n")
                    logging.warning(f"Domain \"{value}\" DNS is invalid.")
                    return False

        return True  # Neither valid IP nor valid domain
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return False
    except dns.resolver.NoNameservers:
        logging.error(f"No nameservers available for domain: {value}")
        return

def extract_domain_from_line(line, prefix):
    """Extract the domain from a line that starts with the given prefix."""
    return line.split()[1] if line.startswith(prefix) else None


def process_file(input_file, prefix):
    """Process the file, filtering lines by the given prefix and removing duplicates, only if domains are valid."""
    unique_lines = set()

    with open(input_file, "r") as infile:
        for line in infile:
            line = line.strip()
            if line and check_line_starts_with(line, prefix):
                domain = extract_domain_from_line(line, prefix)
                if domain and is_valid_domain_or_ip(domain):
                    unique_lines.add(line)
                else:
                    logging.warning(f"Entry \"{domain}\" is invalid and it's not being included to the list.")

    return sorted(unique_lines)


def main():
    """Main execution flow to process the lists and update the hosts files."""
    input_lists = os.getenv("LISTS", ",".join(ADLISTS)).split(",")
    selected = selected_lists(input_lists)

    for list_name in selected:
        logging.info(f"Started cleaning \"{list_name}\" list.")
        file_path = f"lists/{list_name}.txt"

        # Process the file to extract and filter unique lines
        unique_lines = process_file(file_path, PREFIX_TO_CHECK)

        # If the file exists, delete it
        delete_file(file_path)

        # Write back the filtered, sorted lines to the file
        with open(file_path, "w") as outfile:
            outfile.write("\n".join(unique_lines) + "\n")

        # Output the integrity message
        integrity_message(file_path)


# Global variables
ADLISTS = get_filenames_without_extension("lists")
PREFIX_TO_CHECK = "0.0.0.0"
CHECK_DOMAIN_DNS: bool = bool(int(os.getenv("CHECK_DOMAIN_DNS", 0)))

if __name__ == "__main__":
    """Carrega e aplica a configuração de logging a partir de um arquivo YAML."""
    with open(".log-config.yml", "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    main()
