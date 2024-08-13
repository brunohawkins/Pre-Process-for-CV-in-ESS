import os
import tkinter as tk
from tkinter import filedialog, messagebox


def delete_pngs_without_json(folder_path):
    # Check if the directory exists
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "The selected folder does not exist.")
        return

    # Iterate over all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            # Construct the corresponding JSON filename
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_filepath = os.path.join(folder_path, json_filename)

            # Check if the JSON file exists
            if not os.path.isfile(json_filepath):
                # Construct the full path for the PNG file
                png_filepath = os.path.join(folder_path, filename)
                try:
                    os.remove(png_filepath)
                    print(f"Deleted: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")

    messagebox.showinfo("Complete", "Process completed. Check the console for details.")


def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title="Select Folder")

    if folder_path:
        delete_pngs_without_json(folder_path)


if __name__ == "__main__":
    select_folder()
