import os
import json
import shutil
from tkinter import Tk, filedialog

# Set of allowed label ids
allowed_labels = {'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10', 'i11'}


# Function to select the directory
def select_directory(prompt):
    root = Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(title=prompt)
    return dir_path


# Function to filter and copy files
def filter_and_copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over files in the source directory
    for filename in os.listdir(src_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(src_dir, filename)

            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
                # Check if any bounding box contains an allowed label
                if any(box['label'] in allowed_labels for box in data.get('bounding_boxes', [])):
                    # Copy JSON file
                    shutil.copy(json_path, dest_dir)

                    # Extract corresponding PNG file name
                    png_filename = filename.replace("_ob_resized.json", "_resized.png")
                    png_path = os.path.join(src_dir, png_filename)

                    # Check if the PNG file exists and copy it
                    if os.path.exists(png_path):
                        shutil.copy(png_path, dest_dir)
                    else:
                        print(f"Warning: PNG file {png_filename} not found for {filename}")


# Main function to run the script
def main():
    # Prompt user to select source directory
    src_dir = select_directory("Select the source directory containing JSON and PNG files")
    if not src_dir:
        print("Source directory selection cancelled. Exiting.")
        return

    # Prompt user to select destination parent directory
    dest_parent_dir = select_directory("Select the destination directory to save cleaned files")
    if not dest_parent_dir:
        print("Destination directory selection cancelled. Exiting.")
        return

    # Define destination directory
    dest_dir = os.path.join(dest_parent_dir, "cleaned_images_and_jsons")

    # Filter and copy files
    filter_and_copy_files(src_dir, dest_dir)
    print(f"Filtered files have been copied to {dest_dir}")


if __name__ == "__main__":
    main()
