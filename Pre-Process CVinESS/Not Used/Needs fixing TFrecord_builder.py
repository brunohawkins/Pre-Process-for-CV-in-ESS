import tkinter as tk
from tkinter import filedialog, messagebox
import tensorflow as tf
import pandas as pd
import os


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def image_to_tfexample(image_data, label, width, height, xmin, ymin, xmax, ymax):
    return tf.train.Example(features=tf.train.Features(feature={
        'image': _bytes_feature(image_data),
        'label': _bytes_feature(label.encode('utf-8')),
        'width': _int64_feature(width),
        'height': _int64_feature(height),
        'xmin': _float_feature(xmin),
        'ymin': _float_feature(ymin),
        'xmax': _float_feature(xmax),
        'ymax': _float_feature(ymax),
    }))


def create_tfrecord(csv_file, image_dir, output_file):
    df = pd.read_csv(csv_file)
    writer = tf.io.TFRecordWriter(output_file)

    for index, row in df.iterrows():
        image_path = os.path.join(image_dir, row['filename'] + '.png')

        with tf.io.gfile.GFile(image_path, 'rb') as fid:
            image_data = fid.read()

        tf_example = image_to_tfexample(
            image_data,
            row['class'],
            row['width'],
            row['height'],
            row['xmin'],
            row['ymin'],
            row['xmax'],
            row['ymax']
        )

        writer.write(tf_example.SerializeToString())

    writer.close()
    messagebox.showinfo("Success", f'TFRecord file {output_file} created successfully.')


def select_csv_file():
    csv_file_path.set(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]))


def select_image_dir():
    image_dir_path.set(filedialog.askdirectory())


def select_output_file():
    output_file_path.set(
        filedialog.asksaveasfilename(defaultextension=".tfrecord", filetypes=[("TFRecord files", "*.tfrecord")]))


def generate_tfrecord():
    csv_file = csv_file_path.get()
    image_dir = image_dir_path.get()
    output_file = output_file_path.get()

    if not csv_file or not image_dir or not output_file:
        messagebox.showerror("Error", "Please select all the required files.")
        return

    create_tfrecord(csv_file, image_dir, output_file)


app = tk.Tk()
app.title("TFRecord Generator")

csv_file_path = tk.StringVar()
image_dir_path = tk.StringVar()
output_file_path = tk.StringVar()

tk.Label(app, text="CSV File:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=csv_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_csv_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(app, text="Image Directory:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=image_dir_path, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_image_dir).grid(row=1, column=2, padx=10, pady=10)

tk.Label(app, text="Output TFRecord File:").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=output_file_path, width=50).grid(row=2, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_output_file).grid(row=2, column=2, padx=10, pady=10)

tk.Button(app, text="Generate TFRecord", command=generate_tfrecord).grid(row=3, columnspan=3, pady=20)

app.mainloop()
