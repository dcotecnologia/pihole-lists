import os

ADLISTS = ["ads_malware", "fakenews", "gambling", "porn", "social"]
OUTPUT_DIR = "out"
OUTPUT_FILE = f"{OUTPUT_DIR}/hosts.txt"
PREFIX_TO_CHECK = "0.0.0.0"


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def check_line_starts_with(line, prefix):
    return line.startswith(prefix)


def integrity_message():
    if os.path.exists(OUTPUT_FILE):
        print(f"Hosts file compiled sucessfully and available in {OUTPUT_FILE}")
    else:
        print(f"Hosts file couldn't be compiled")


def selected_lists(input):
    lists = [item for item in input if item in ADLISTS]
    if not lists:
        lists = ADLISTS
    return lists


def main():
    input_lists = os.getenv("LISTS", ADLISTS).split(",")
    lists = selected_lists(input_lists)
    lists = list("lists/" + list + ".txt" for list in lists)

    delete_file(OUTPUT_FILE)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(OUTPUT_FILE, "w") as outfile:
        for fname in lists:
            with open(fname, "r") as infile:
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

    integrity_message()


if __name__ == "__main__":
    main()
