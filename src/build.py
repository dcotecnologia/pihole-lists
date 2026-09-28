"""Combines curated lists in `lists/` into every non-empty subset.

Usage: `make compile` (or `uv run python src/build.py`), optionally with a `LISTS=a,b,c`
env var to restrict which lists are combined.
"""

import os
from itertools import combinations

from common import (
    filter_selected_lists,
    get_filenames_without_extension,
    line_has_prefix,
)
from settings import BUILD_OUTPUT_DIR, LISTS_DIR, PREFIX_TO_CHECK, env_selected_lists

ADLISTS = get_filenames_without_extension(LISTS_DIR)
ADLISTS_SET = set(ADLISTS)
OUTPUT_DIR = BUILD_OUTPUT_DIR


def selected_lists(input_lists):
    """Filters input lists based on existing filenames (ADLISTS).

    If no valid input is provided, it returns the default ADLISTS.

    Args:
        input_lists: List of filenames to filter.

    Returns:
        The filtered list of filenames, or the default ADLISTS.
    """
    return filter_selected_lists(input_lists, ADLISTS, ADLISTS_SET)


def filter_condition(line):
    """Checks if a given line starts with the specified prefix.

    Args:
        line: Line to check.

    Returns:
        True if the line starts with `PREFIX_TO_CHECK`, False otherwise.
    """
    return line_has_prefix(line, PREFIX_TO_CHECK)


def load_filtered_lines(list_name):
    """Loads and filters a list file once, to avoid repeated disk reads.

    Args:
        list_name: Name of the list (without extension) under `lists/`.

    Returns:
        The set of stripped lines in the file that start with `PREFIX_TO_CHECK`.
    """
    list_path = os.path.join(LISTS_DIR, f"{list_name}.txt")
    with open(list_path, encoding="utf-8") as infile:
        return {line.strip() for line in infile if filter_condition(line)}


def process_combination(combo, lines_by_list):
    """Writes one output file for the given list combination.

    Args:
        combo: Tuple of list names making up this combination.
        lines_by_list: Mapping of list name to its pre-loaded, filtered lines
            (as produced by `load_filtered_lines`).
    """
    combined_lines = set().union(*(lines_by_list[list_name] for list_name in combo))

    output_filename = os.path.join(OUTPUT_DIR, "+".join(combo) + ".txt")
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.writelines(f"{line}\n" for line in sorted(combined_lines))


def main():
    """Orchestrates the list-combination process.

    Reads the `LISTS` environment variable (or falls back to every list under `lists/`),
    selects the relevant lists, generates every non-empty combination of them, and
    writes one output file per combination under `OUTPUT_DIR`.
    """
    # Get the lists to process from environment variables or fall back to default
    input_lists = env_selected_lists(ADLISTS)
    slc_lists = selected_lists(input_lists)

    # Read each selected list only once and reuse across all combinations.
    lines_by_list = {list_name: load_filtered_lines(list_name) for list_name in slc_lists}

    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Generate combinations of lists and process each combination
    for r in range(1, len(slc_lists) + 1):
        for combo in combinations(slc_lists, r):
            process_combination(combo, lines_by_list)


if __name__ == "__main__":
    main()
