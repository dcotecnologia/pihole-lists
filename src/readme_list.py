import os


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


print("| List  | Description                                                                                  | Link |")
print("| ----- | -------------------------------------------------------------------------------------------- | ---- |")
for list in sorted(ADLISTS):
    print(f"| {list} | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/{list}.txt) |")
