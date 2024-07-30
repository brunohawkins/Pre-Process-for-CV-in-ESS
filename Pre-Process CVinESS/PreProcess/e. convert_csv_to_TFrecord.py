import os
import tensorflow as tf
from PIL import Image
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from object_detection.utils import dataset_util

# Label map dictionary
label_map = {
    'i2': 1, 'i3': 2, 'i4': 3, 'i5': 4, 'i6': 5, 'i7': 6, 'i8': 7, 'i9': 8, 'i10': 9, 'i11': 10
}


def create_tf_example(row, path):
    filename = row['filename']
    # Try to find the file with common extensions
    for ext in ['.png', '.jpg', '.jpeg']:
        image_path = os.path.join(path, filename + ext)
        if os.path.exists(image_path):
            break
    else:
        raise FileNotFoundError(f"Image file {filename} not found with common extensions")

    with tf.io.gfile.GFile(image_path, 'rb') as fid:
        encoded_image = fid.read()

    image = Image.open(image_path)
    width, height = image.size

    # Trim whitespace from class name and check if it exists in label_map
    class_name = row['class'].strip()
    if class_name not in label_map:
        raise ValueError(f"Class name '{class_name}' not found in label_map")

    xmins = [row['xmin'] / width]
    xmaxs = [row['xmax'] / width]
    ymins = [row['ymin'] / height]
    ymaxs = [row['ymax'] / height]
    classes_text = [class_name.encode('utf8')]
    classes = [label_map[class_name]]

    # Get the extension used
    image_ext = ext[1:]  # 'png', 'jpg', or 'jpeg'

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename.encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(filename.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_image),
        'image/format': dataset_util.bytes_feature(image_ext.encode('utf8')),  # 'png', 'jpg', or 'jpeg'
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def convert_csv_to_tfrecord(csv_input, output_path):
    df = pd.read_csv(csv_input)
    output_file = os.path.join(output_path, 'output.tfrecord')
    writer = tf.io.TFRecordWriter(output_file)
    grouped = df.groupby('filename')

    for filename, group in grouped:
        for _, row in group.iterrows():
            try:
                tf_example = create_tf_example(row, output_path)
                writer.write(tf_example.SerializeToString())
            except (FileNotFoundError, ValueError) as e:
                print(e)

    writer.close()
    print(f"Successfully created the TFRecord file: {output_file}")


def select_csv_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        output_path = os.path.dirname(file_path)
        convert_csv_to_tfrecord(file_path, output_path)
    else:
        print("No file selected")


if __name__ == '__main__':
    select_csv_file()
