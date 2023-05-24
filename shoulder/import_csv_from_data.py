import os
import shutil


def copy_folder_with_csv(src_folder: str, dst_folder: str):
    # make sure the source and dst are different
    if src_folder == dst_folder:
        raise ValueError("Source and destination folders must be different.")

    # Create the destination folder
    os.makedirs(dst_folder, exist_ok=True)

    # Iterate over folder in the source folder
    for folder in os.listdir(src_folder):
        # Iterates over files in the folder
        os.makedirs(os.path.join(dst_folder, folder), exist_ok=True)
        for filename in os.listdir(os.path.join(src_folder, folder)):
            if filename.endswith(".csv") or filename.endswith(".txt"):
                src_file = os.path.join(src_folder, folder, filename)

                dst_file = os.path.join(dst_folder, folder, filename)
                shutil.copy2(src_file, dst_file)

    print("Folder copied with .csv files.")


# Example usage
source_folder = "/home/puchaud/Documents/shoulder/new_data"
destination_folder = "/home/puchaud/Documents/shoulder/new_data_csv_only"

copy_folder_with_csv(source_folder, destination_folder)
