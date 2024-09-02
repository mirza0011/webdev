import os

root_directory = ""
sub_folder = "json_output"

folder_path = os.path.join(root_directory, sub_folder)

for filename in os.listdir(folder_path):
    if filename.startswith("."):
        new_filename = filename.lstrip(".")
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        os.rename(old_file_path, new_file_path)