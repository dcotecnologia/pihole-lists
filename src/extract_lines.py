"""Generates a keyword-derived list (`microsoft.txt`) from every other list in `lists/`.

Template for adding another keyword-derived list: copy this module, point
`LIST_DESTINATION`/`KEYWORDS` at the new target, and add an entry point for it.
"""

import os

from settings import LISTS_DIR, MICROSOFT_KEYWORDS, MICROSOFT_LIST_DESTINATION

LIST_DESTINATION = MICROSOFT_LIST_DESTINATION
OUTPUT_FILE = os.path.join(LISTS_DIR, LIST_DESTINATION)
KEYWORDS = MICROSOFT_KEYWORDS


def main():
    """Scans every list in `LISTS_DIR` for `KEYWORDS` matches and writes the result.

    Returns:
        The set of matching lines that were written to `OUTPUT_FILE`.
    """
    lines_found = set()
    for fname in os.listdir(LISTS_DIR):
        fpath = os.path.join(LISTS_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        if fname == LIST_DESTINATION:
            continue
        with open(fpath, encoding="utf-8", errors="ignore") as f:
            for line in f:
                if any(keyword in line.lower() for keyword in KEYWORDS):
                    lines_found.add(line.rstrip())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for line in sorted(lines_found):
            out.write(line + "\n")
    return lines_found


def run_and_report():
    """Runs `main` and prints a one-line summary of what was written."""
    lines_found = main()
    print(f"{len(lines_found)} lines containing '{', '.join(KEYWORDS)}' were saved in {OUTPUT_FILE}")


def _run_main_for_coverage():
    """Invokes `run_and_report` when executed as a script.

    Kept as a separate function (instead of a bare `if __name__ == "__main__":` block)
    so the entry-point branch itself is coverable by a unit test that calls this
    function directly with `__name__` monkeypatched.
    """
    if __name__ == "__main__":
        run_and_report()


_run_main_for_coverage()
