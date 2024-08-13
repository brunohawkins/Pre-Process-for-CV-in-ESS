import os
import re
import tkinter as tk
from tkinter import filedialog

def remove_ob_from_filenames(directory):
    # List all files in the directory
    files = os.listdir(directory)

    # Regex pattern to find '_ob' in filenames
    pattern = re.compile(r'(_ob)')

    # Iterate through each file
    for file in files:
        if file.endswith('.txt'):
            new_name = pattern.sub('', file)  # Remove '_ob' from filename
            old_path = os.path.join(directory, file)
            new_path = os.path.join(directory, new_name)

            # Rename the file
            os.rename(old_path, new_path)
            print(f'Renamed {file} to {new_name}')

def select_directory():
    # Open a dialog to select directory
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    directory = filedialog.askdirectory(title='Select Directory')

    if directory:
        remove_ob_from_filenames(directory)
        tk.messagebox.showinfo('Success', 'File names updated successfully!')

if __name__ == "__main__":
    select_directory()
