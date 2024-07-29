import os
import shutil
import tkinter as tk
from tkinter import filedialog


def select_directory(prompt):
    """Open a dialog to select a directory and return the path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    return filedialog.askdirectory(title=prompt)


def main():
    # Select directories
    json_dir = select_directory("Select the directory containing JSON files")
    png_dir = select_directory("Select the directory containing PNG files")
    output_dir = select_directory("Select the output directory")

    if not (json_dir and png_dir and output_dir):
        print("Directory selection was cancelled. Exiting.")
        return

    # Create 'ob_pngs' folder in the output directory if it doesn't exist
    ob_pngs_dir = os.path.join(output_dir, 'ob_pngs')
    os.makedirs(ob_pngs_dir, exist_ok=True)

    # Get a list of JSON files
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    # Generate the base names for comparison
    json_bases = {os.path.splitext(f)[0].replace('_ob', '') for f in json_files}

    # Copy matching PNG files to the 'ob_pngs' directory
    for png_file in os.listdir(png_dir):
        if png_file.endswith('.png'):
            base_name = os.path.splitext(png_file)[0]
            if base_name in json_bases:
                src_path = os.path.join(png_dir, png_file)
                dest_path = os.path.join(ob_pngs_dir, png_file)
                shutil.copy(src_path, dest_path)
                print(f'Copied {png_file} to {ob_pngs_dir}')

    print("Copy operation completed.")


if __name__ == "__main__":
    main()
