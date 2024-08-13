# based on https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

import tkinter as tk
from tkinter import filedialog
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def create_gui():
    def convert_xml_to_csv():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            xml_df = xml_to_csv(folder_selected)
            xml_df.to_csv(os.path.join(folder_selected, 'labels.csv'), index=None)
            status_label.config(text='Conversion successful!')

    root = tk.Tk()
    root.title('XML to CSV Converter')

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    select_folder_button = tk.Button(frame, text='Select Folder', command=convert_xml_to_csv)
    select_folder_button.pack(side=tk.LEFT)

    status_label = tk.Label(frame, text='')
    status_label.pack(side=tk.RIGHT)

    root.mainloop()

if __name__ == '__main__':
    create_gui()