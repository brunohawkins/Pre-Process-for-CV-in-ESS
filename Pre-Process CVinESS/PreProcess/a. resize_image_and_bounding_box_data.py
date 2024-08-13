import json
import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class img_conversion:
    def __init__(self, target_width, target_height, input_dir_img, save_path_directory):
        self.target_width = target_width
        self.target_height = target_height
        self.crop_width = 1200
        self.crop_height = 1080
        self.start_x = 385
        self.start_y = 0
        self.save_path_directory = save_path_directory
        self.original_height = 1080
        self.original_width = 1920
        self.ratio = min(self.target_width / self.crop_width, self.target_height / self.crop_height)
        self.new_size = (int(self.crop_width * self.ratio), int(self.crop_height * self.ratio))
        self.input_dir_img = input_dir_img

    def resize_img(self, img_path, suffix='_resized'):
        img = cv2.imread(img_path)
        if img is None or img.size == 0:
            print(f'the {img_path} can not find the images')
        cropped_img = img[self.start_y:self.start_y + self.crop_height, self.start_x:self.start_x + self.crop_width]
        resized_img = cv2.resize(cropped_img, self.new_size, interpolation=cv2.INTER_AREA)
        letterboxed_img = cv2.copyMakeBorder(
            resized_img,
            (self.target_height - self.new_size[1]) // 2,
            (self.target_height - self.new_size[1]) // 2 + (self.target_height - self.new_size[1]) % 2,
            (self.target_width - self.new_size[0]) // 2,
            (self.target_width - self.new_size[0]) // 2 + (self.target_width - self.new_size[0]) % 2,
            cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )
        img_basename = os.path.basename(img_path)
        file_name, ext = os.path.splitext(img_basename)
        resized_image_name = f"{file_name}{suffix}{ext}"
        save_path = os.path.join(self.save_path_directory, resized_image_name)
        os.makedirs(self.save_path_directory, exist_ok=True)
        cv2.imwrite(save_path, letterboxed_img)
        print(f"The image is successfully resized and saved to {save_path}")

    def loop_img(self):
        n = 0
        for name in os.listdir(self.input_dir_img):
            if name.endswith(('jpg', 'jpeg', 'png')):
                n += 1
                full_input_path = os.path.join(self.input_dir_img, name)
                self.resize_img(full_input_path)
        print(f"There are {n} images saved to the path {self.save_path_directory}")

class json_conversion:
    def __init__(self, target_width, target_height, input_dir_json, save_path_directory):
        self.target_width = target_width
        self.target_height = target_height
        self.crop_width = 1200
        self.crop_height = 1080
        self.start_x = 385
        self.start_y = 0
        self.save_path_directory = save_path_directory
        self.original_height = 1080
        self.original_width = 1920
        self.ratio = min(self.target_width / self.crop_width, self.target_height / self.crop_height)
        self.new_size = (int(self.crop_width * self.ratio), int(self.crop_height * self.ratio))
        self.input_dir_json = input_dir_json

    def resize_annotations(self, jsons, suffix='_resized'):
        top_padding = (self.target_height - self.new_size[1]) // 2
        left_padding = (self.target_width - self.new_size[0]) // 2
        for bbox in jsons["bounding_boxes"]:
            bbox['xmin'] = int((bbox['xmin'] - self.start_x) * self.ratio) + left_padding
            bbox['ymin'] = int((bbox['ymin'] - self.start_y) * self.ratio) + top_padding
            bbox['xmax'] = int((bbox['xmax'] - self.start_x) * self.ratio) + left_padding
            bbox['ymax'] = int((bbox['ymax'] - self.start_y) * self.ratio) + top_padding
        file_name, ext = os.path.splitext(jsons["image_name"])
        jsons["image_name"] = f'{file_name}{suffix}{ext}'
        jsons["imagewidth"] = self.target_width
        jsons["imageheight"] = self.target_height
        return jsons

    def load_json(self, json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data

    def save_json(self, data, json_path):
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)

    def resize_json(self, json_path, suffix='_resized'):
        data = self.load_json(json_path)
        if data is None:
            print(f"Error: Could not read json {json_path}")
            return
        annotations = self.resize_annotations(data)
        json_basename = os.path.basename(json_path)
        file_name, ext = os.path.splitext(json_basename)
        new_name = f'{file_name}{suffix}{ext}'
        os.makedirs(self.save_path_directory, exist_ok=True)
        save_json_path = os.path.join(self.save_path_directory, new_name)
        self.save_json(annotations, save_json_path)
        print(f"The JSON annotations are successfully resized and saved to {save_json_path}")

    def loop_json(self):
        n = 0
        for name in os.listdir(self.input_dir_json):
            if name.endswith('json'):
                n += 1
                full_input_path = os.path.join(self.input_dir_json, name)
                self.resize_json(full_input_path)
        print(f"There are {n} JSONs saved to the path {self.save_path_directory}")

def select_directory(var):
    folder_selected = filedialog.askdirectory()
    var.set(folder_selected)

def process_img_conversion():
    target_width = int(target_size_width.get())
    target_height = int(target_size_height.get())
    input_dir = input_dir_img.get()
    save_dir = output_dir_img.get()

    img_conv = img_conversion(target_width, target_height, input_dir, save_dir)
    img_conv.loop_img()

def process_json_conversion():
    target_width = int(target_size_width.get())
    target_height = int(target_size_height.get())
    input_dir = input_dir_json.get()
    save_dir = output_dir_json.get()

    json_conv = json_conversion(target_width, target_height, input_dir, save_dir)
    json_conv.loop_json()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image and JSON Conversion")

    input_dir_img = tk.StringVar()
    output_dir_img = tk.StringVar()
    input_dir_json = tk.StringVar()
    output_dir_json = tk.StringVar()
    target_size_width = tk.IntVar(value=512)
    target_size_height = tk.IntVar(value=512)

    tk.Label(root, text="Input Image Directory:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    tk.Entry(root, textvariable=input_dir_img, width=50).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_directory(input_dir_img)).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Output Image Directory:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    tk.Entry(root, textvariable=output_dir_img, width=50).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_directory(output_dir_img)).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(root, text="Input JSON Directory:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tk.Entry(root, textvariable=input_dir_json, width=50).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_directory(input_dir_json)).grid(row=2, column=2, padx=5, pady=5)

    tk.Label(root, text="Output JSON Directory:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    tk.Entry(root, textvariable=output_dir_json, width=50).grid(row=3, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_directory(output_dir_json)).grid(row=3, column=2, padx=5, pady=5)

    tk.Label(root, text="Target Width:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    tk.Entry(root, textvariable=target_size_width, width=10).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    tk.Label(root, text="Target Height:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
    tk.Entry(root, textvariable=target_size_height, width=10).grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    tk.Button(root, text="Process Images", command=process_img_conversion).grid(row=6, column=0, columnspan=3, padx=5, pady=5)
    tk.Button(root, text="Process JSONs", command=process_json_conversion).grid(row=7, column=0, columnspan=3, padx=5, pady=5)

    root.mainloop()
