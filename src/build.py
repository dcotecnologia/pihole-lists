import os
from itertools import combinations


def get_filenames_without_extension(directory):
    """Retrieves the list of filenames (without extensions) from a given directory.

    Args:
        directory (str): Path to the directory containing files.

    Returns:
        list: List of filenames without their extensions.
    """
    return [os.path.splitext(filename)[0] for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]


ADLISTS = get_filenames_without_extension("lists")
ADLISTS_SET = set(ADLISTS)
OUTPUT_DIR = "out"
PREFIX_TO_CHECK = "0.0.0.0"


def delete_file(file_path):
    """Deletes the specified file if it exists.

    Args:
        file_path (str): Path to the file to be deleted.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def selected_lists(input_lists):
    """Filters input lists based on existing filenames (ADLISTS).

    If no valid input is provided, it returns the default ADLISTS.

    Args:
        input_lists (list): List of filenames to filter.

    Returns:
        list: Filtered list of filenames or the default ADLISTS.
    """
    lists = [item for item in input_lists if item in ADLISTS_SET]
    return lists if lists else ADLISTS


def filter_condition(line):
    """Checks if a given line starts with the specified prefix.

    Args:
        line (str): Line to check.

    Returns:
        bool: True if the line starts with the PREFIX_TO_CHECK, False otherwise.
    """
    return line.startswith(PREFIX_TO_CHECK)


def load_filtered_lines(list_name):
    """Load and filter a list file once to avoid repeated disk reads."""
    list_path = os.path.join("lists", f"{list_name}.txt")
    with open(list_path, encoding="utf-8") as infile:
        return {line.strip() for line in infile if filter_condition(line)}


def process_combination(combo, lines_by_list):
    """Write one output file for the given list combination."""
    combined_lines = set().union(*(lines_by_list[list_name] for list_name in combo))

    output_filename = os.path.join(OUTPUT_DIR, "+".join(combo) + ".txt")
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(sorted(combined_lines)) + "\n")


def main():
    """Main function that orchestrates the process.

    It reads environment variables for the lists, selects the relevant lists, generates
    all possible combinations, and processes them.
    """
    # Get the lists to process from environment variables or fall back to default
    input_lists = [item.strip() for item in os.getenv("LISTS", ",".join(ADLISTS)).split(",") if item.strip()]
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
