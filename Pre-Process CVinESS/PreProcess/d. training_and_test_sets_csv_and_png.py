import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import shutil
import random

class DataSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV and PNG Splitter")

        self.create_widgets()

    def create_widgets(self):
        # Directory selection
        self.lbl_directory = tk.Label(self.root, text="Select Directory Containing CSV and PNGs:")
        self.lbl_directory.pack(pady=5)

        self.btn_directory = tk.Button(self.root, text="Browse", command=self.select_directory)
        self.btn_directory.pack(pady=5)

        # Split ratio selection
        self.lbl_ratio = tk.Label(self.root, text="Train/Test Split Ratio (0 to 1):")
        self.lbl_ratio.pack(pady=5)

        self.ratio_entry = tk.Entry(self.root)
        self.ratio_entry.pack(pady=5)

        # Start splitting
        self.btn_split = tk.Button(self.root, text="Split Data", command=self.split_data)
        self.btn_split.pack(pady=20)

    def select_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Directory Selected", f"Selected Directory: {self.directory}")

    def split_data(self):
        ratio = self.ratio_entry.get()
        try:
            ratio = float(ratio)
            if not (0 <= ratio <= 1):
                raise ValueError("Ratio must be between 0 and 1.")
        except ValueError as e:
            messagebox.showerror("Invalid Ratio", str(e))
            return

        if not hasattr(self, 'directory'):
            messagebox.showerror("No Directory", "Please select a directory first.")
            return

        csv_file = [f for f in os.listdir(self.directory) if f.endswith('.csv')]
        if not csv_file:
            messagebox.showerror("CSV Not Found", "No CSV file found in the selected directory.")
            return

        csv_file = csv_file[0]
        csv_path = os.path.join(self.directory, csv_file)

        df = pd.read_csv(csv_path)

        # List PNG files
        png_files = [f for f in os.listdir(self.directory) if f.endswith('.png')]
        if not png_files:
            messagebox.showerror("PNG Not Found", "No PNG files found in the selected directory.")
            return

        # Ensure all PNGs have a corresponding entry in the CSV
        df['filename'] = df['filename'].str.replace('.png', '')
        missing_images = set(df['filename']) - set([os.path.splitext(f)[0] for f in png_files])
        if missing_images:
            messagebox.showwarning("Missing Images", f"Images missing for these entries: {missing_images}")

        # Shuffle and split
        df = df.sample(frac=1).reset_index(drop=True)
        split_idx = int(len(df) * ratio)
        train_df = df[:split_idx]
        test_df = df[split_idx:]

        train_dir = os.path.join(self.directory, 'train')
        test_dir = os.path.join(self.directory, 'test')
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)

        # Save CSV files
        train_df.to_csv(os.path.join(train_dir, csv_file), index=False)
        test_df.to_csv(os.path.join(test_dir, csv_file), index=False)

        # Move PNG files
        for _, row in train_df.iterrows():
            shutil.copy(os.path.join(self.directory, row['filename'] + '.png'), train_dir)
        for _, row in test_df.iterrows():
            shutil.copy(os.path.join(self.directory, row['filename'] + '.png'), test_dir)

        messagebox.showinfo("Success", "Data has been successfully split.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataSplitterApp(root)
    root.mainloop()
