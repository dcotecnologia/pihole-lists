"""Shared helpers reused by the list-processing entry-point scripts.

Kept intentionally small: a home for logic that was duplicated verbatim across
`build.py`, `cleanup.py`, and `readme_list.py`, not a general-purpose framework.
"""

import logging
import os


def get_filenames_without_extension(directory):
    """Returns filenames without extensions for every regular file in a directory.

    Args:
        directory: Path to the directory to scan. Subdirectories are ignored.

    Returns:
        A list of filenames with their extension stripped, in directory-listing
        order.
    """
    return [os.path.splitext(filename)[0] for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]


def delete_file(file_path):
    """Deletes a file if it exists.

    Args:
        file_path: Path to the file to delete. A missing file is a no-op.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def line_has_prefix(line, prefix):
    """Checks whether a line starts with the given prefix.

    Args:
        line: The line to check.
        prefix: The prefix to look for.

    Returns:
        True if `line` starts with `prefix`, False otherwise.
    """
    return line.startswith(prefix)


def filter_selected_lists(input_lists, all_lists, all_lists_set=None):
    """Filters `input_lists` down to the names that exist in `all_lists`.

    Falls back to `all_lists` itself when nothing survives the filter (e.g. an
    empty or fully-invalid `LISTS` env var).

    Args:
        input_lists: Candidate list names to filter, e.g. from a `LISTS` env var.
        all_lists: The full, known-valid set of list names, used as the fallback.
        all_lists_set: Optional pre-built `set(all_lists)`, to avoid rebuilding it
            on every call. Defaults to `set(all_lists)` when not given.

    Returns:
        The filtered list names, or `all_lists` if none of `input_lists` matched.
    """
    valid_names = all_lists_set if all_lists_set is not None else set(all_lists)
    selected = [item for item in input_lists if item in valid_names]
    return selected if selected else all_lists


def configure_logging():
    """Configures root logging once, shared by every entry-point script.

    A no-op if the root logger already has handlers attached (e.g. under pytest), per
    the semantics of `logging.basicConfig`.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
