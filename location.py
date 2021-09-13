import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby
from collections import Counter
from skimage.metrics import structural_similarity as ssim

def extract_Y(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, _, _ = cv2.split(img_yuv)
    return y

def read_frames_from_video(video):
    frames = []
    y_frames = []
    vidcap = cv2.VideoCapture(video)
    success, frame = vidcap.read()
    frames.append(frame)
    y_frame = extract_Y(frame)
    y_frames.append(y_frame[25:])
    while success: 
        success, frame = vidcap.read()  
        if not success:
            break
        frames.append(frame)
        y_frame = extract_Y(frame)
        y_frames.append(y_frame[25:])    
    vidcap.release()
    return frames, y_frames

def calculate_sim_seq(frame_list):
    sim_list = []
    for i in range(0, len(frame_list)-1):
        sim = ssim(frame_list[i],frame_list[i+1])
        sim_list.append(sim)
    return sim_list

def is_stable(start, end, list_):
    if start < 0:
        start = 0
    if end > len(list_):
        end = len(list_)
    count_candidate = 0
    for x in list_[start:end]:
        if x <= 0.95:
            return False
    return count_candidate <= 1

def detect_keyframes(sim_sequence, stable_threshold=2):
    stable_list = [is_stable(idx-stable_threshold, idx+stable_threshold, sim_sequence) for idx in range(len(sim_sequence))]
    stable_list.reverse()
    keyframe_list = []
    
    idx = 0
    for k, g in groupby(stable_list):
        if k:
            keyframe_list.append(idx)
        idx += sum(1 for i in g)
    keyframes_index = [len(stable_list)-x for x in keyframe_list]
    keyframes_index.reverse()
    return keyframes_index

def keyframe_location(video, stable_threshold=2, visualize=False):
    vidcap = cv2.VideoCapture(video)

    # read video
    frames, y_frames = read_frames_from_video(video)
    # consecutive frame difference
    sim_list = calculate_sim_seq(y_frames)

    # visualize
    if visualize:
        plt.plot(np.arange(len(sim_list)), np.array(sim_list))
        plt.xlabel("frame")
        plt.ylabel("similarity")
        plt.show()

    # detect keyframes
    keyframes_index = detect_keyframes(sim_list,stable_threshold=2)
    
    keyframes = [frames[i] for i in keyframes_index]
    return keyframes, keyframes_index
