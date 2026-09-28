"""Print a markdown table of curated lists, for pasting into README.md.

Usage: `make readme` (or `uv run python src/readme_list.py`).
"""

from common import get_filenames_without_extension
from settings import LISTS_DIR, RAW_URL_TEMPLATE


def main():
    """Prints the markdown table header and one row per curated list.

    Reads the list names from `lists/` and prints a `| List | Link |` table row for
    each, sorted alphabetically, for pasting into `README.md`'s "Ready-to-use list"
    section.
    """
    adlists = sorted(get_filenames_without_extension(LISTS_DIR))

    print("| List  | Description                                                                                  | Link |")
    print("| ----- | -------------------------------------------------------------------------------------------- | ---- |")

    for list_name in adlists:
        url = RAW_URL_TEMPLATE.format(list_name=list_name)
        print(f"| {list_name} | [{list_name}.txt]({url}) |")


if __name__ == "__main__":
    main()
