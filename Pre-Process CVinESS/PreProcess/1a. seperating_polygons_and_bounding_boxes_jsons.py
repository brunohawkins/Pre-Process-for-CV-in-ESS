import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

def parse_labelme_json(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Extract image metadata and shapes
        if 'version' in data and data['version'] == '5.2.1':
            image_name = data['imagePath'].split('\\')[-1]  # Windows path format
            imagewidth = data['imageWidth']
            imageheight = data['imageHeight']
            shapes = data['shapes']
        elif 'version' in data and data['version'] == '5.5.0':
            image_name = os.path.basename(data['imagePath'])  # Mac/Linux path format
            imagewidth = data['imageWidth']
            imageheight = data['imageHeight']
            shapes = data['shapes']
        else:
            raise ValueError("Unsupported LabelMe JSON version")

        polygons = []
        bounding_boxes = []

        for shape in shapes:
            label = shape['label']
            points = shape['points']

            if shape['shape_type'] == 'rectangle':
                # Handle rectangle shapes
                if 'version' in data and data['version'] == '5.2.1':
                    xmin = shape['points'][0][0]
                    ymin = shape['points'][0][1]
                    xmax = shape['points'][1][0]
                    ymax = shape['points'][1][1]
                elif 'version' in data and data['version'] == '5.5.0':
                    xmin = min(point[0] for point in points)
                    ymin = min(point[1] for point in points)
                    xmax = max(point[0] for point in points)
                    ymax = max(point[1] for point in points)

                bounding_boxes.append({'label': label, 'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})

            elif shape['shape_type'] == 'polygon':
                # Handle polygon shapes
                polygons.append({'label': label, 'points': points})

        return image_name, imagewidth, imageheight, polygons, bounding_boxes

    except Exception as e:
        print(f"Error parsing {json_file}: {str(e)}")
        return None, None, None, None, None

def save_segmentation_json(original_filename, imagewidth, imageheight, polygons, output_folder):
    if polygons:
        seg_output_folder = os.path.join(output_folder, 'segmentation_masks')
        os.makedirs(seg_output_folder, exist_ok=True)
        seg_output_file = os.path.join(seg_output_folder, original_filename)  # Retain original filename
        data = {
            'image_name': original_filename,
            'imagewidth': imagewidth,
            'imageheight': imageheight,
            'polygons': polygons
        }
        try:
            with open(seg_output_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving segmentation JSON for {original_filename}: {str(e)}")
    else:
        print(f"No segmentation data for {original_filename}. Skipping creation of JSON file.")

def save_object_detection_json(original_filename, imagewidth, imageheight, bounding_boxes, output_folder):
    if bounding_boxes:
        obj_output_folder = os.path.join(output_folder, 'bounding_boxes')
        os.makedirs(obj_output_folder, exist_ok=True)
        obj_output_file = os.path.join(obj_output_folder, original_filename)  # Retain original filename
        data = {
            'image_name': original_filename,
            'imagewidth': imagewidth,
            'imageheight': imageheight,
            'bounding_boxes': bounding_boxes
        }
        try:
            with open(obj_output_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving object detection JSON for {original_filename}: {str(e)}")
    else:
        print(f"No bounding box data for {original_filename}. Skipping creation of JSON file.")

def process_json_files(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            try:
                json_file = os.path.join(input_folder, filename)
                print(f"Processing file: {json_file}")  # Debug print
                image_name, imagewidth, imageheight, polygons, bounding_boxes = parse_labelme_json(json_file)

                if image_name:
                    save_segmentation_json(filename, imagewidth, imageheight, polygons, output_folder)
                    save_object_detection_json(filename, imagewidth, imageheight, bounding_boxes, output_folder)
                    print(f"Processed: {filename}")
                else:
                    print(f"No valid data found in {filename}. Skipping.")

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    messagebox.showinfo("Batch Processing", "All JSON files processed successfully.")

def select_input_folder():
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    if input_folder:
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if output_folder:
            process_json_files(input_folder, output_folder)

# Create the main application window
root = tk.Tk()
root.title("Batch LabelMe JSON Processor")

# Add a button to select input folder and start processing
process_button = tk.Button(root, text="Select Input Folder", command=select_input_folder)
process_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
