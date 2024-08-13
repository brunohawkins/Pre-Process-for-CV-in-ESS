import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="Select Input Directory")
    return folder_selected

def process_files(input_directory):
    # Create output directory
    output_directory = os.path.join(input_directory, "images")
    os.makedirs(output_directory, exist_ok=True)

    # Get list of files and sort them
    files = os.listdir(input_directory)
    png_files = [f for f in files if f.lower().endswith('.png')]
    xml_files = [f for f in files if f.lower().endswith('.xml')]

    # Sort files to ensure consistent renaming
    png_files.sort()
    xml_files.sort()

    # Rename and copy files
    for idx, file in enumerate(png_files):
        new_png_name = f"img{idx + 1}.png"
        new_xml_name = f"img{idx + 1}.xml"

        # Check if the corresponding XML file exists
        xml_file = next((f for f in xml_files if os.path.splitext(f)[0] == os.path.splitext(file)[0]), None)

        if xml_file:
            # Copy PNG file
            shutil.copy(os.path.join(input_directory, file), os.path.join(output_directory, new_png_name))
            # Copy XML file
            shutil.copy(os.path.join(input_directory, xml_file), os.path.join(output_directory, new_xml_name))

    messagebox.showinfo("Success", "Files have been renamed and copied successfully!")

def main():
    input_directory = select_directory()
    if input_directory:
        process_files(input_directory)
    else:
        messagebox.showwarning("No Directory", "No directory was selected.")

if __name__ == "__main__":
    main()
