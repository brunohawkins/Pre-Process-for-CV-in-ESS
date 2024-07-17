import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def browse_folder():
    folder_path.set(filedialog.askdirectory())

def start_integration():
    folder_path_val = folder_path.get()
    base_output_folder_val = output_folder.get()
    output_name_val = output_name.get()

    try:
        if not folder_path_val or not base_output_folder_val or not output_name_val:
            raise ValueError("Please provide valid input values.")

        temp_file_list = os.path.join(base_output_folder_val, 'temp.txt')

        # Collect and sort all video files in the selected folder
        video_files = sorted([os.path.join(folder_path_val, file) for file in os.listdir(folder_path_val)
                              if file.endswith(('.mp4', '.avi', '.mov', '.mkv'))])

        # Write video file paths to a temporary text file (for ffmpeg concat)
        with open(temp_file_list, 'w') as file:
            for video_file in video_files:
                file.write(f"file '{video_file}'\n")

        # Output file path for concatenated video
        output_file = os.path.join(base_output_folder_val, f"{output_name_val}.mp4")

        # Command to concatenate and re-encode videos using ffmpeg
        ffmpeg_path = '/opt/homebrew/bin/ffmpeg'  # Adjust this path based on your installation
        ffmpeg_concat_command = [
            ffmpeg_path, '-f', 'concat', '-safe', '0', '-i', temp_file_list,
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', '-b:a', '128k',
            output_file
        ]

        # Execute ffmpeg command
        try:
            subprocess.run(ffmpeg_concat_command, check=True)
            messagebox.showinfo("Success", f"Videos integrated successfully and saved to {output_file}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error during integration: {e}")

        # Clean up temporary file
        os.remove(temp_file_list)

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))


# GUI setup using tkinter
root = tk.Tk()
root.title("Video Integrator")

# Variables for GUI input fields
folder_path = tk.StringVar()
output_folder = tk.StringVar()
output_name = tk.StringVar()

# Labels and input fields
tk.Label(root, text="Video Folder:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=folder_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=output_folder, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: output_folder.set(filedialog.askdirectory())).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Output Name:").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=output_name, width=50).grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Start Integration", command=start_integration).grid(row=3, column=0, columnspan=3, padx=10, pady=20)

root.mainloop()
