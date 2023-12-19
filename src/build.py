import os
from itertools import combinations


def get_filenames_without_extension(directory):
    filenames = []
    for filename in os.listdir(directory):
        # Check if it's a file (not a directory)
        if os.path.isfile(os.path.join(directory, filename)):
            # Split the filename and extension
            name, extension = os.path.splitext(filename)
            # Add only the filename without extension to the list
            filenames.append(name)
    return filenames


ADLISTS = get_filenames_without_extension("lists")
OUTPUT_DIR = "out"
OUTPUT_FILE = f"{OUTPUT_DIR}/hosts.txt"
PREFIX_TO_CHECK = "0.0.0.0"


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def check_line_starts_with(line, prefix):
    return line.startswith(prefix)


def selected_lists(input):
    lists = [item for item in input if item in ADLISTS]
    if not lists:
        lists = ADLISTS
    return lists


def filter_condition(line):
    return check_line_starts_with(line, PREFIX_TO_CHECK)


def main():
    input_lists = os.getenv("LISTS", ADLISTS).split(",")
    slc_lists = selected_lists(input_lists)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for r in range(1, len(slc_lists) + 1):
        for combo in combinations(slc_lists, r):
            file_name = "+".join(combo)
            file_name = OUTPUT_DIR + "/" + file_name + ".txt"
            with open(file_name, "w+") as outfile:
                for list in combo:
                    listname = "lists/" + list + ".txt"
                    with open(listname, "r") as infile:
                        current_line = infile.readline().strip()
                        for line in infile:
                            if not check_line_starts_with(line, PREFIX_TO_CHECK):
                                continue
                            if line.strip() == current_line:
                                current_line += line.strip()
                            else:
                                outfile.write(current_line + "\n")
                                current_line = line.strip()

                        # Write the last line
                        outfile.write(current_line + "\n")


if __name__ == "__main__":
    main()
