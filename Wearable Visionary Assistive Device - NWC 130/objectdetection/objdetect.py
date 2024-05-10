import cv2
from Voice.voiceout import *  # Adjust the import path based on your project structure

# Load model and labels
config_file = 'C:\\Users\\sudhe\Desktop\\major_project\\BlindBoy\\objectdetection\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'C:\\Users\\sudhe\\Desktop\\major_project\\BlindBoy\\objectdetection\\frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)

classLabels = []  # Initialize the list of class labels
label_file = 'C:\\Users\\sudhe\\Desktop\\major_project\\BlindBoy\\objectdetection\\coco-labels-paper.txt'
with open(label_file, 'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

# Setup the model
model.setInputSize(320, 320)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

def detect_objects(frame):
    """
    Perform object detection on the given frame and vocalize the detected object labels.
    """
    ClassIndex, confidence, bbox = model.detect(frame, confThreshold=0.5)
    if len(ClassIndex) != 0:
        for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
            if ClassInd <= len(classLabels):
                label = classLabels[ClassInd - 1]
                VO(label)  # Vocalize the detected object label
