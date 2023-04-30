# classes = ['bowling', 'batting', 'boundary', 'closeup', 'crowd']
import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model
import sys

# load the saved model
model = load_model('E:\4thyear_project\my_model.h5\my_model.h5')
print("Hello World! Welcome to Python Examples.")
# set the video file path
video_path = sys.argv[1]

# read the video file
cap = cv2.VideoCapture(video_path)

# create a directory to store the extracted frames
frames_dir = 'frames'
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)

# extract frames from the video at 2 second intervals
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % 60 == 0:  # extract a frame every 2 seconds
        frame_path = os.path.join(frames_dir, f'frame{frame_count}.jpg')
        cv2.imwrite(frame_path, frame)
    frame_count += 1

# loop through each extracted frame and classify it
class_names = ['bowling', 'batting', 'boundary',
               'closeup', 'crowd']  # replace with your class names
results = {}
for frame_name in os.listdir(frames_dir):
    frame_path = os.path.join(frames_dir, frame_name)
    frame = cv2.imread(frame_path)
    # resize to the input shape of your model
    frame = cv2.resize(frame, (224, 224))
    frame = np.expand_dims(frame, axis=0)  # add a batch dimension
    predictions = model.predict(frame)
    class_idx = np.argmax(predictions[0])
    class_name = class_names[class_idx]
    if class_name not in results:
        results[class_name] = []
    results[class_name].append(frame_name)

# print the list of frames belonging to each class
for class_name, frame_names in results.items():
    print(f'Class {class_name}:')
    for frame_name in frame_names:
        print(frame_name)
