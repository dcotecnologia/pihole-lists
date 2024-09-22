import os


def get_filenames_without_extension(directory):
    """
    Returns a list of filenames (without extensions) from a given directory.
    """
    return [
        os.path.splitext(filename)[0]
        for filename in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, filename))
    ]


ADLISTS = sorted(get_filenames_without_extension("lists"))

# Header for the markdown table
print("| List  | Description                                                                                  | Link |")
print("| ----- | -------------------------------------------------------------------------------------------- | ---- |")

# Generate and print each row of the table
for list_name in ADLISTS:
    print(f"| {list_name} | [Link](https://raw.githubusercontent.com/dcotecnologia/pihole-lists/master/lists/{list_name}.txt) |")
