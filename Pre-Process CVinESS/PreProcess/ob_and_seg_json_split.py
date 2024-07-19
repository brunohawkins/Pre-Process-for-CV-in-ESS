import os
import glob
import json
import numpy as np
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog


def json_to_mask(json_file, image_shape):
    """Convert a LabelMe JSON file to a segmentation mask."""
    with open(json_file) as f:
        data = json.load(f)

    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    for shape in data['shapes']:
        points = shape['points']
        polygon = [tuple(point) for point in points]
        ImageDraw.Draw(Image.fromarray(mask)).polygon(polygon, outline=1, fill=1)

    return mask


def process_json_files(json_dir, image_shape, mask_output_dir):
    """Process JSON files in the directory to create segmentation masks."""
    if not os.path.exists(mask_output_dir):
        os.makedirs(mask_output_dir)

    json_files = glob.glob(os.path.join(json_dir, '*.json'))

    for json_file in json_files:
        mask = json_to_mask(json_file, image_shape)
        mask_image = Image.fromarray(mask)

        mask_filename = os.path.splitext(os.path.basename(json_file))[0] + '_mask.png'
        mask_output_path = os.path.join(mask_output_dir, mask_filename)

        mask_image.save(mask_output_path)
        print(f"Saved mask to {mask_output_path}")


def select_directory():
    """Open a dialog box to select a directory and return the selected path."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory()
    return folder_selected


def main():
    """Main function to select directories and process JSON files."""
    print("Select the directory containing JSON files:")
    json_directory = select_directory()
    if not json_directory:
        print("No directory selected.")
        return

    print("Select the directory to save the output masks:")
    output_directory = select_directory()
    if not output_directory:
        print("No output directory selected.")
        return

    image_shape = (128, 128, 3)  # Example shape, adjust as necessary

    process_json_files(json_directory, image_shape, output_directory)


if __name__ == "__main__":
    main()
