import os
import shutil
import random
import tkinter as tk
from tkinter import filedialog, simpledialog
from tqdm import tqdm


def copy_files(file_pairs, destination_folder):
    """Copies files to the destination folder."""
    for png, json_file in file_pairs:
        shutil.copy(png, destination_folder)
        shutil.copy(json_file, destination_folder)


def split_files(files, split_ratios):
    """Splits files into training, validation, and test sets based on given ratios."""
    total_files = len(files)
    train_end = int(total_files * split_ratios[0])
    val_end = train_end + int(total_files * split_ratios[1])

    random.shuffle(files)

    train_files = files[:train_end]
    val_files = files[train_end:val_end]
    test_files = files[val_end:]

    return train_files, val_files, test_files


def process_directory(input_dir, output_dir, split_ratios):
    """Processes the input directory and splits files according to the given ratios."""
    # Get all PNG and JSON files
    files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    # Create mapping from PNG to JSON
    png_to_json = {}
    for png in files:
        base_name = png.rsplit('_', 1)[0]
        json_name = f"{base_name}_resized.json"
        if json_name in json_files:
            png_to_json[png] = os.path.join(input_dir, json_name)

    file_pairs = [(os.path.join(input_dir, png), os.path.join(input_dir, json)) for png, json in png_to_json.items()]

    # Split file pairs
    train_files, val_files, test_files = split_files(file_pairs, split_ratios)

    # Create directories
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    test_dir = os.path.join(output_dir, 'test')

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Copy files to corresponding directories
    copy_files(train_files, train_dir)
    copy_files(val_files, val_dir)
    copy_files(test_files, test_dir)

    print("Files have been successfully split and copied.")


def main():
    root = tk.Tk()
    root.withdraw()

    input_dir = filedialog.askdirectory(title="Select the Input Directory")
    if not input_dir:
        print("No input directory selected. Exiting.")
        return

    output_dir = filedialog.askdirectory(title="Select the Output Directory")
    if not output_dir:
        print("No output directory selected. Exiting.")
        return

    split_ratios = []
    while len(split_ratios) < 3:
        ratio_input = simpledialog.askstring("Input",
                                             f"Enter split ratios for train, val, test (sum should be 1.0), e.g. '0.7 0.2 0.1':")
        try:
            split_ratios = [float(x) for x in ratio_input.split()]
            if abs(sum(split_ratios) - 1.0) > 0.01:
                raise ValueError
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter three numbers that add up to 1.0.")

    process_directory(input_dir, output_dir, split_ratios)


if __name__ == "__main__":
    main()
