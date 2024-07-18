import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

# Color mapping for labels
label_colors = {
    't1': (255, 0, 0),  # Red
    't2': (255, 128, 0),  # Orange
    't3': (255, 255, 0),  # Yellow
    't4': (128, 255, 0),  # Light Green
    't5': (0, 255, 0),  # Green
    't6': (0, 255, 128),  # Light Teal
    't7': (0, 255, 255),  # Cyan
    't8': (0, 128, 255),  # Light Blue
    't9': (0, 0, 255),  # Blue

    'i1': (128, 0, 255),  # Purple
    'i2': (255, 0, 255),  # Magenta
    'i3': (255, 0, 128),  # Pink
    'i4': (255, 128, 128),  # Light Pink
    'i5': (255, 128, 255),  # Light Purple
    'i6': (128, 128, 255),  # Light Indigo
    'i7': (0, 128, 128),  # Teal
    'i8': (128, 255, 255),  # Light Cyan
    'i9': (128, 255, 128),  # Light Green
    'i10': (255, 128, 128),  # Light Red
    'i11': (255, 255, 128)  # Light Yellow
}


def parse_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    img_name = data['image_name']
    img_width = data['imagewidth']
    img_height = data['imageheight']
    polygons = data['polygons']

    return img_name, img_width, img_height, polygons


def create_segmentation_mask(img_width, img_height, polygons):
    mask = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    for polygon in polygons:
        label = polygon['label']
        points = np.array(polygon['points'], np.int32)
        points = points.reshape((-1, 1, 2))

        color = label_colors.get(label, (255, 255, 255))  # Default to white if label color not defined
        cv2.fillPoly(mask, [points], color)

    return mask


def process_folder(input_folder, output_folder):
    json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]

    for json_file in json_files:
        img_name, img_width, img_height, polygons = parse_json(os.path.join(input_folder, json_file))
        mask = create_segmentation_mask(img_width, img_height, polygons)

        mask_save_path = os.path.join(output_folder, os.path.splitext(json_file)[0] + '_mask.png')
        cv2.imwrite(mask_save_path, cv2.cvtColor(mask, cv2.COLOR_RGB2BGR))  # Save as PNG

    messagebox.showinfo('Processing Complete',
                        f'Processed {len(json_files)} JSON files.\nMasks saved in {output_folder}.')


def select_input_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        input_folder_var.set(folder_path)


def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_var.set(folder_path)


# GUI setup
root = tk.Tk()
root.title('LabelMe JSON to Segmentation Masks Converter')

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Input folder selection
tk.Label(frame, text='Select Input Folder:').pack()
input_folder_var = tk.StringVar()
input_folder_entry = tk.Entry(frame, textvariable=input_folder_var, width=50)
input_folder_entry.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text='Browse', command=select_input_folder).pack(side=tk.LEFT)

# Output folder selection
tk.Label(frame, text='Select Output Folder:').pack()
output_folder_var = tk.StringVar()
output_folder_entry = tk.Entry(frame, textvariable=output_folder_var, width=50)
output_folder_entry.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text='Browse', command=select_output_folder).pack(side=tk.LEFT)


def start_processing():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()

    if not input_folder or not output_folder:
        messagebox.showerror('Error', 'Please select both input and output folders.')
        return

    process_folder(input_folder, output_folder)


# Process button
tk.Button(root, text='Start Processing', command=start_processing).pack(pady=10)

root.mainloop()