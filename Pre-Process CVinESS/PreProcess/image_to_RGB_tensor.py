import os
import numpy as np
import cv2
from tkinter import Tk, filedialog
import tkinter as tk


def load_image_and_mask(image_folder, mask_folder):
    images = []
    masks = []

    # Get list of image files
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

    for img_file in image_files:
        # Construct the corresponding mask filename
        mask_file = img_file.replace('.png', '_seg_mask.png')

        # Check if the mask file exists
        if mask_file in os.listdir(mask_folder):
            # Load images
            img_path = os.path.join(image_folder, img_file)
            mask_path = os.path.join(mask_folder, mask_file)

            # Read images
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)  # or cv2.IMREAD_GRAYSCALE if you need grayscale
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

            if img is not None and mask is not None:
                images.append(img)
                masks.append(mask)

    return np.array(images), np.array(masks)


def main():
    # Create a GUI window
    root = Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select the folder with images
    print("Select the folder with original images")
    image_folder = filedialog.askdirectory(title="Select the Folder with Original Images")

    # Ask the user to select the folder with masks
    print("Select the folder with segmentation masks")
    mask_folder = filedialog.askdirectory(title="Select the Folder with Segmentation Masks")

    # Ask the user to select the output folder for NumPy files
    print("Select the folder to save NumPy files")
    output_folder = filedialog.askdirectory(title="Select the Output Folder for NumPy Files")

    # Load images and masks
    images, masks = load_image_and_mask(image_folder, mask_folder)

    # Save arrays to .npy files
    np.save(os.path.join(output_folder, 'images.npy'), images)
    np.save(os.path.join(output_folder, 'masks.npy'), masks)

    print(f"Images and masks saved to {output_folder}")


if __name__ == "__main__":
    main()
