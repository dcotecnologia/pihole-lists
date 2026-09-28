"""File-backed CRUD for the curated lists under `LISTS_DIR`.

Deliberately standalone from `src/` (the main project's build/cleanup
pipeline): this only touches `lists/*.txt`, the same files that pipeline
reads, but as a separately deployable local admin tool it doesn't share a
Python path with the main project inside its own container - only the
`lists/` directory is mounted in.
"""

import os
import re
from pathlib import Path

PREFIX = "0.0.0.0"

# Matches the main project's PREFIX_TO_CHECK (src/settings.py) - lines that
# don't start with it are preserved as-is but never listed/counted as items.
LISTS_DIR = Path(os.environ.get("LISTS_DIR", "/app/lists"))

LIST_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
# Deliberately permissive: real validation (DNS, TLD rules) is cleanup.py's
# job. This only blocks control characters, whitespace, and the "0.0.0.0 "
# prefix from being smuggled into the domain field itself.
DOMAIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?$")


class ListNotFoundError(Exception):
    """Raised when a requested list file doesn't exist."""


class ListAlreadyExistsError(Exception):
    """Raised when creating a list whose file already exists."""


class InvalidNameError(Exception):
    """Raised when a list name or domain fails the naming pattern check."""


def _validate_list_name(name):
    if not LIST_NAME_RE.match(name):
        raise InvalidNameError(f"Invalid list name: {name!r}. Use letters, digits, '-', '_' only.")


def _validate_domain(domain):
    if not DOMAIN_RE.match(domain) or ".." in domain:
        raise InvalidNameError(f"Invalid domain: {domain!r}.")


def _list_path(name):
    _validate_list_name(name)
    return LISTS_DIR / f"{name}.txt"


def _iter_domains(path):
    """Yields the domain from every prefixed line in a list file, in order."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(f"{PREFIX} "):
                yield line[len(PREFIX) + 1 :]


def list_lists():
    """Returns every curated list's name and entry count.

    Returns:
        A list of `{"name": str, "item_count": int}` dicts, sorted by name.
    """
    LISTS_DIR.mkdir(parents=True, exist_ok=True)
    summaries = []
    for path in sorted(LISTS_DIR.glob("*.txt")):
        count = sum(1 for _ in _iter_domains(path))
        summaries.append({"name": path.stem, "item_count": count})
    return summaries


def create_list(name):
    """Creates an empty list file.

    Args:
        name: The list's name (without extension).

    Raises:
        InvalidNameError: If `name` doesn't match the allowed pattern.
        ListAlreadyExistsError: If the list file already exists.
    """
    path = _list_path(name)
    if path.exists():
        raise ListAlreadyExistsError(f"List already exists: {name!r}.")
    LISTS_DIR.mkdir(parents=True, exist_ok=True)
    path.touch()


def delete_list(name):
    """Deletes a list file.

    Args:
        name: The list's name (without extension).

    Raises:
        InvalidNameError: If `name` doesn't match the allowed pattern.
        ListNotFoundError: If the list file doesn't exist.
    """
    path = _list_path(name)
    if not path.exists():
        raise ListNotFoundError(f"List not found: {name!r}.")
    path.unlink()


def get_items(name, query="", page=1, page_size=50):
    """Returns a page of a list's domains, optionally filtered by substring.

    Args:
        name: The list's name (without extension).
        query: Case-insensitive substring to filter domains by.
        page: 1-indexed page number.
        page_size: Number of items per page.

    Returns:
        A `{"items": list[str], "total": int, "page": int, "page_size": int}`
        dict. `total` is the count of domains matching `query` (not the
        list's full size).

    Raises:
        InvalidNameError: If `name` doesn't match the allowed pattern.
        ListNotFoundError: If the list file doesn't exist.
    """
    path = _list_path(name)
    if not path.exists():
        raise ListNotFoundError(f"List not found: {name!r}.")

    needle = query.strip().lower()
    matches = [domain for domain in _iter_domains(path) if not needle or needle in domain.lower()]

    start = (page - 1) * page_size
    return {
        "items": matches[start : start + page_size],
        "total": len(matches),
        "page": page,
        "page_size": page_size,
    }


def add_item(name, domain):
    """Appends a domain to a list, unless it's already present.

    Args:
        name: The list's name (without extension).
        domain: The domain to add.

    Returns:
        True if the domain was added, False if it was already present.

    Raises:
        InvalidNameError: If `name` or `domain` doesn't match the allowed
            pattern.
        ListNotFoundError: If the list file doesn't exist.
    """
    path = _list_path(name)
    if not path.exists():
        raise ListNotFoundError(f"List not found: {name!r}.")
    _validate_domain(domain)

    if any(existing == domain for existing in _iter_domains(path)):
        return False

    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{PREFIX} {domain}\n")
    return True


def remove_item(name, domain):
    """Removes every line for a domain from a list.

    Args:
        name: The list's name (without extension).
        domain: The domain to remove.

    Returns:
        True if a matching line was removed, False if the domain wasn't
        present.

    Raises:
        InvalidNameError: If `name` doesn't match the allowed pattern.
        ListNotFoundError: If the list file doesn't exist.
    """
    path = _list_path(name)
    if not path.exists():
        raise ListNotFoundError(f"List not found: {name!r}.")

    target = f"{PREFIX} {domain}"
    removed = False
    kept_lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.rstrip("\n") == target:
                removed = True
                continue
            kept_lines.append(line if line.endswith("\n") else f"{line}\n")

    if removed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(kept_lines)
    return removed
