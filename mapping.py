from skimage.metrics import structural_similarity as ssim
import cv2
import glob
import os
import matplotlib.pyplot as plt


def load_screenshots(screenshots):
    index = {}
    orb = cv2.ORB_create(nfeatures=1500)
    for imagePath in glob.glob(os.path.join(screenshots, '*.png')):
        filename = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)
        size = image.shape
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, des = orb.detectAndCompute(image, None)
        index[filename] = {'ssim': image, 'orb': des}
    return index, size


def match_bfmatcher(des1,des2):
    matcher = cv2.BFMatcher() 
    matches = matcher.knnMatch(des1,des2, k=2) 
    good = []
    for m,n in matches:
        if m.distance < 0.4*n.distance:
            good.append([m])
    return len(good) / len(matches)

def mapping(image, index, size):
    alpha = 0.5
    orb = cv2.ORB_create(nfeatures=1500)
    results = {}
    image = cv2.resize(image, (size[1], size[0]))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, des = orb.detectAndCompute(image, None)
    for (k, v) in index.items():
        sim_ssim = ssim(image, v['ssim'])
        sim_orb = match_bfmatcher(des, v['orb'])
        results[k] = alpha * sim_ssim + (1-alpha) * sim_orb
    results = sorted([(v, k) for (k, v) in results.items()], reverse=True)
    return results[0][1]

def gui_mapping(screenshots, keyframes):
    index, size = load_screenshots(screenshots)
    index_sequence = [mapping(keyframe, index, size) for keyframe in keyframes]
    index_sequence = [int(i.split('artifacts_')[1].split('.')[0]) for i in index_sequence]
    return index_sequence

if __name__ == "__main__":
    # Debug
    index, size = load_screenshots('/Users/mac/Documents/Python/DroidbotMapping/dataset/firebase/KISS/artifacts')
    frame_id = 11
    vidcap = cv2.VideoCapture('/Users/mac/Documents/Python/DroidbotMapping/dataset/GT/KISS/2.gif')
    success, frame = vidcap.read()
    no = 1
    while success: 
        success, frame = vidcap.read()  
        if not success:
            break
        no += 1
        if no == frame_id:
            keyframe = frame
            break
    vidcap.release()
    print('Start Mapping')
    print(mapping(keyframe, index, size))
