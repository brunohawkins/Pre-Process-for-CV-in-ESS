import os
import subprocess
import multiprocessing
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_frames(video_path, output_folder, fps, start_time, duration, process_number):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    part_output_folder = os.path.join(output_folder, f"part_{process_number}")
    if not os.path.exists(part_output_folder):
        os.makedirs(part_output_folder)

    ffmpeg_command = [
        'ffmpeg', '-ss', str(start_time), '-t', str(duration), '-i', video_path, '-vf', f'fps={fps}',
        os.path.join(part_output_folder, f'{video_name}_frame_%07d.png')
    ]

    print(f"Running FFmpeg command: {' '.join(ffmpeg_command)}")

    try:
        process = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            print(f"Cannot process the file {video_path}: {process.stderr.decode('utf-8')}")
            return part_output_folder, 0
    except Exception as e:
        print(f"Failed to run FFmpeg command: {str(e)}")
        return part_output_folder, 0

    frame_count = len([f for f in os.listdir(part_output_folder) if f.endswith('.png')])
    return part_output_folder, frame_count

def worker_function(queue, video_path, output_folder, fps, start_time, duration, process_number):
    result = extract_frames(video_path, output_folder, fps, start_time, duration, process_number)
    queue.put(result)

def parallel_frame_extraction(video_path, output_folder, fps, num_processes):
    ffprobe_command = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'format=duration', '-of',
        'default=noprint_wrappers=1:nokey=1', video_path
    ]

    try:
        result = subprocess.run(ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration = float(result.stdout.strip())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get video duration: {str(e)}")
        return

    chunk_duration = duration / num_processes
    processes = []
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_processes):
        start_time = i * chunk_duration
        p = multiprocessing.Process(target=worker_function,
                                    args=(queue, video_path, output_folder, fps, start_time, chunk_duration, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    global_frame_offset = 0
    part_folders = []
    while not queue.empty():
        part_output_folder, frame_count = queue.get()
        part_folders.append((part_output_folder, frame_count))

    part_folders.sort(key=lambda x: int(x[0].split('_')[-1]))  # Sort by process number

    for part_output_folder, frame_count in part_folders:
        frame_files = sorted([f for f in os.listdir(part_output_folder) if f.endswith('.png')],
                             key=lambda x: int(x.split('_')[-1].split('.')[0]))  # Sort by frame number
        for i, frame_file in enumerate(frame_files):
            new_name = os.path.join(output_folder,
                                    f'{os.path.basename(video_path)}_frame_{global_frame_offset + i:07d}.png')
            os.rename(os.path.join(part_output_folder, frame_file), new_name)
        global_frame_offset += frame_count
        os.rmdir(part_output_folder)

    messagebox.showinfo("Complete",
                        f"Frame extraction completed for {video_path}. Total frames extracted: {global_frame_offset}")

def start_frame_extraction():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if not video_path:
        return

    output_folder = output_folder_var.get()
    if not output_folder:
        return

    fps = int(fps_var.get())
    num_processes = int(num_processes_var.get())

    parallel_frame_extraction(video_path, output_folder, fps, num_processes)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Frame Extraction")

    output_folder_var = tk.StringVar()
    fps_var = tk.StringVar(value="1")
    num_processes_var = tk.StringVar(value="4")

    def browse_output_folder():
        folder_selected = filedialog.askdirectory()
        output_folder_var.set(folder_selected)

    tk.Label(root, text="Output Folder:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=browse_output_folder).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="FPS:").grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=fps_var, width=10).grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Number of Processes:").grid(row=2, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=num_processes_var, width=10).grid(row=2, column=1, padx=10, pady=10)

    tk.Button(root, text="Start Frame Extraction", command=start_frame_extraction).grid(row=3, column=0, columnspan=3,
                                                                                        padx=10, pady=20)

    root.mainloop()
