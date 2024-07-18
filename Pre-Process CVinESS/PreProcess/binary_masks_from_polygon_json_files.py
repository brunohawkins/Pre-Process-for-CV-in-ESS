import os
import json
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk


def parse_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    img_name = data['image_name']
    img_width = data['imagewidth']
    img_height = data['imageheight']
    polygons = data['polygons']

    return img_name, img_width, img_height, polygons


def create_segmentation_mask(img_width, img_height, polygons):
    mask = np.zeros((img_height, img_width), dtype=np.uint8)

    for polygon in polygons:
        points = np.array(polygon['points'], np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.fillPoly(mask, [points], 255)

    return mask


def process_folder(input_folder, output_folder):
    json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]

    for json_file in json_files:
        img_name, img_width, img_height, polygons = parse_json(os.path.join(input_folder, json_file))
        mask = create_segmentation_mask(img_width, img_height, polygons)

        mask_save_path = os.path.join(output_folder, os.path.splitext(json_file)[0] + '_mask.png')
        cv2.imwrite(mask_save_path, mask)

    print(f'Processed {len(json_files)} JSON files.')


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
root.title('JSON to Segmentation Mask Converter')

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
        tk.messagebox.showerror('Error', 'Please select both input and output folders.')
        return

    process_folder(input_folder, output_folder)
    tk.messagebox.showinfo('Processing Complete', f'Processed JSON files saved in {output_folder}.')


# Process button
tk.Button(root, text='Start Processing', command=start_processing).pack(pady=10)

root.mainloop()