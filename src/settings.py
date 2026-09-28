"""Centralized constants and environment-derived settings for the project's scripts.

Change a directory name, the hosts-file prefix, an env-var name/default, or a generated-
list definition here instead of in each script separately.

An env-derived *value* (as opposed to its var name/default) is deliberately never
precomputed as a module-level constant here: this module is imported once and cached in
`sys.modules`, so a value computed at import time would freeze at whatever the env var
was on the first import, ignoring later per-test/per-process overrides (e.g.
`monkeypatch.setenv`, or a fresh `runpy.run_module` reload of the calling script).
Instead, each script reads the env var itself, at its own (re-importable) module scope,
using the name and helper functions exposed here.
"""

import os

# Env var names, used by more than one script.
LISTS_ENV_VAR = "LISTS"
CHECK_DOMAIN_DNS_ENV_VAR = "CHECK_DOMAIN_DNS"
DNS_WORKERS_ENV_VAR = "DNS_WORKERS"
IMPORT_OUTPUT_DIR_ENV_VAR = "OUTPUT_DIR"

# Directories.
LISTS_DIR = "lists"
BUILD_OUTPUT_DIR = "out"
DEFAULT_IMPORT_OUTPUT_DIR = "imported"

# Hosts-file format.
PREFIX_TO_CHECK = "0.0.0.0"

# extract_lines.py: microsoft.txt keyword-derived list.
MICROSOFT_LIST_DESTINATION = "microsoft.txt"
MICROSOFT_KEYWORDS = ["microsoft", "bing", "windows", "edge", "azure", "office", "365", "xbox"]

# readme_list.py.
PROJECT_REPO = "dcotecnologia/pihole-lists"
RAW_URL_TEMPLATE = f"https://raw.githubusercontent.com/{PROJECT_REPO}/master/lists/{{list_name}}.txt"


def check_domain_dns_enabled():
    """Reads whether `cleanup.py` should validate domains via a live DNS lookup.

    Returns:
        True if the `CHECK_DOMAIN_DNS` env var is set to a truthy integer
        (e.g. `"1"`), False otherwise (including when unset).
    """
    return bool(int(os.getenv(CHECK_DOMAIN_DNS_ENV_VAR, 0)))


def env_selected_lists(default_lists):
    """Parses the `LISTS` env var into a list of candidate list names.

    Shared by `build.py` and `cleanup.py`, which both accept the same
    `LISTS=a,b,c` env var to restrict which lists they process.

    Args:
        default_lists: List names to fall back to when `LISTS` is unset.

    Returns:
        The comma-separated, stripped, non-empty names from `LISTS`, or
        `default_lists` when the env var is unset.
    """
    raw = os.getenv(LISTS_ENV_VAR, ",".join(default_lists))
    return [item.strip() for item in raw.split(",") if item.strip()]
