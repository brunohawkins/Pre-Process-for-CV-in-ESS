IHE-summer-studentship-2024-CV-in-ESS

version 0.1
author: Bruno Hawkins updated 12/8/2024

1.Data preparation
Raw data was in the form of 5-minute ESS videos (.mp4)
We developed an integrator to concatenate the videos into a single video of the procedure.
Using another programme we developed, the video is cut into video frames in the form of .png files at 1 frame-per-second.
There is a Windows and Mac(silicon) version of the Integrator and Frame extractor
(if you have an intel mac, you need to change the directory file pathname for ffmpeg).
We labeled the data using LabelMe. We used polygon masks for the working channel and anatomy,
and bounding boxes for the surgical tools.
The json file records the coordinates of the polygon masks and bounding boxes.
We used labelled polygon masks for segmentation and use rectangles for the object detection.


2. Object Detection Preprocess

2.1 json seperation

We developed a script that can seperate the segmenation data and object detection data from the saved LabelMe json file.
It allows selection of an input folder containing JSON files and an output folder for saving the new files. The files
are saved in respective directories (segmenetation_masks and bounding_boxes)

2.2 image and json image resizing (for object detection)

We created a script to crop the center of pictures in endoscopic images and to resize them to a scale comapatible with our model.
Coordinates of bounding box in the bounding box jsons are also resized.

2.3. Cleaning data

We needed to clean our data for any mislabelled images and any images that dont have labels. We wrote a programme that only keeps images labelled either i2, i4, or i6 and deletes the rest.
(as of this update, we have only labelled i2 and i6, and hardly any i4).
We also made another that deletes any pngs that don't have respective json. This is more to make sure our data
is as clean as possible, but this step shouldn't be necessary if the previous scripts work correctly.

2.4 Splitting into training, validation and test sets

This script splits the data randomly into training, validation and test folders.

2.5 json to yolov8 txt conversion.

In order to train the model, we need to convert the LabelMe json format to one compatible
with the model type we are using. For the IHE Summer Studentship 2024, we explored the You Only Look Once (YOLO)
object detection algorithm. To train using this model, we had to convert the json to this format.

2.6 the .yaml file (for YOLO Object Detection algorithm)

A dataset.yaml file was created to set labels and configure directory paths. Check the .yaml file
to see how it is formatted. (note: nc stands for the number of classes)