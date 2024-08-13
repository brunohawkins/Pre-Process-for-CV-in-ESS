import os
import json
import tkinter as tk
from tkinter import filedialog

# Mapping of labels
label_mapping = {
    "i2": 0,
    "i4": 1,
    "i6": 2
}

def convert_bbox_to_yolo(image_width, image_height, bbox):
    # Convert bounding box coordinates to YOLO format
    xmin, ymin, xmax, ymax = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
    x_center = (xmin + xmax) / 2.0 / image_width
    y_center = (ymin + ymax) / 2.0 / image_height
    width = (xmax - xmin) / image_width
    height = (ymax - ymin) / image_height
    return x_center, y_center, width, height

def process_json_file(json_path, output_dir):
    with open(json_path, 'r') as file:
        data = json.load(file)

    image_name = data['image_name']
    image_width = data['imagewidth']
    image_height = data['imageheight']
    bboxes = data['bounding_boxes']

    # Create a .txt file with the same base name as the image
    base_name = os.path.splitext(image_name)[0]
    txt_path = os.path.join(output_dir, f'{base_name}.txt')

    with open(txt_path, 'w') as file:
        for bbox in bboxes:
            class_id = label_mapping.get(bbox['label'])
            if class_id is not None:
                x_center, y_center, width, height = convert_bbox_to_yolo(image_width, image_height, bbox)
                file.write(f'{class_id} {x_center} {y_center} {width} {height}\n')

def main():
    # Set up GUI for directory selection
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Directory with JSON Files")
    if not folder_selected:
        print("No directory selected. Exiting.")
        return

    # Process each JSON file in the selected directory
    for filename in os.listdir(folder_selected):
        if filename.endswith('.json'):
            json_path = os.path.join(folder_selected, filename)
            process_json_file(json_path, folder_selected)

            # Delete the JSON file after processing
            os.remove(json_path)
            print(f'Processed and deleted {filename}')

if __name__ == "__main__":
    main()
