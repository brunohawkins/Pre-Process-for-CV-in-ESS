import json
import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import tkinter as tk
from tkinter import filedialog, messagebox


def create_pascal_voc_xml(annotation, img_folder, img_filename, output_folder):
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = img_folder
    ET.SubElement(root, "filename").text = img_filename

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(annotation["imagewidth"])
    ET.SubElement(size, "height").text = str(annotation["imageheight"])
    ET.SubElement(size, "depth").text = "3"  # Assuming RGB images

    for obj in annotation["bounding_boxes"]:
        object_item = ET.SubElement(root, "object")
        ET.SubElement(object_item, "name").text = obj["label"]
        ET.SubElement(object_item, "pose").text = "Unspecified"
        ET.SubElement(object_item, "truncated").text = "0"
        ET.SubElement(object_item, "difficult").text = "0"

        bndbox = ET.SubElement(object_item, "bndbox")
        xmin = obj["xmin"]
        ymin = obj["ymin"]
        xmax = obj["xmax"]
        ymax = obj["ymax"]
        ET.SubElement(bndbox, "xmin").text = str(int(xmin))
        ET.SubElement(bndbox, "ymin").text = str(int(ymin))
        ET.SubElement(bndbox, "xmax").text = str(int(xmax))
        ET.SubElement(bndbox, "ymax").text = str(int(ymax))

    tree = ET.ElementTree(root)
    xml_str = ET.tostring(root, encoding="utf-8")
    xml_str_pretty = parseString(xml_str).toprettyxml(indent="  ")

    xml_filename = os.path.splitext(img_filename)[0] + ".xml"
    xml_filepath = os.path.join(output_folder, xml_filename)
    with open(xml_filepath, "w") as f:
        f.write(xml_str_pretty)


def convert_labelme_to_pascal_voc(labelme_json_folder, img_folder, output_folder):
    output_subfolder = os.path.join(output_folder, "ob_XML_files")
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    for filename in os.listdir(labelme_json_folder):
        if filename.endswith(".json"):
            json_path = os.path.join(labelme_json_folder, filename)
            with open(json_path) as f:
                data = json.load(f)
                img_filename = data["image_name"]
                if img_filename.endswith(".png"):
                    create_pascal_voc_xml(data, img_folder, img_filename, output_subfolder)


def select_json_folder():
    folder_selected = filedialog.askdirectory()
    json_folder_entry.delete(0, tk.END)
    json_folder_entry.insert(0, folder_selected)


def select_img_folder():
    folder_selected = filedialog.askdirectory()
    img_folder_entry.delete(0, tk.END)
    img_folder_entry.insert(0, folder_selected)


def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)


def start_conversion():
    labelme_json_folder = json_folder_entry.get()
    img_folder = img_folder_entry.get()
    output_folder = output_folder_entry.get()

    if not labelme_json_folder or not img_folder or not output_folder:
        messagebox.showerror("Error", "Please select all folders before starting the conversion.")
        return

    try:
        convert_labelme_to_pascal_voc(labelme_json_folder, img_folder, output_folder)
        messagebox.showinfo("Success", "Conversion completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during conversion: {e}")


# GUI setup
root = tk.Tk()
root.title("LabelMe to Pascal VOC Converter")

tk.Label(root, text="LabelMe JSON Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
json_folder_entry = tk.Entry(root, width=50)
json_folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_json_folder).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Image Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
img_folder_entry = tk.Entry(root, width=50)
img_folder_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_img_folder).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=2, column=2, padx=10, pady=5)

tk.Button(root, text="Start Conversion", command=start_conversion).grid(row=3, column=0, columnspan=3, pady=20)

root.mainloop()