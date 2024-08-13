import tkinter as tk
from tkinter import filedialog
import os


def replace_labels_in_file(file_path):
    """Replace occurrences of i2, i4, i6 with 1, 2, 3 in a file."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace labels
    content = content.replace('i2', '0')
    content = content.replace('i4', '1')
    content = content.replace('i6', '2')

    with open(file_path, 'w') as file:
        file.write(content)


def process_directory(directory):
    """Process all .txt files in the given directory."""
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            replace_labels_in_file(file_path)
    print(f"Processing complete for directory: {directory}")


def select_directory():
    """Open a dialog to select a directory and process it."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory = filedialog.askdirectory(title="Select Directory")
    if directory:
        process_directory(directory)
    else:
        print("No directory selected.")


if __name__ == "__main__":
    select_directory()
