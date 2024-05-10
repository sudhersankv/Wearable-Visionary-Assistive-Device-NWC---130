
import time
import cv2
import pynput
import sys
from pynput.keyboard import Key, Listener
import threading
sys.path.append('voice')
from objectdetection.objdetect import detect_objects
from voice import *
sys.path.append('ocr')
from OCR import *
sys.path.append('objectdetection')
from objdetect import *
sys.path.append('facerec')
from reco import *


def on_press(key):
    global mode, exit_program
    try:
        if key.char == '2':
            mode = 2
        elif key.char == '1':
            mode = 1
        elif key.char == '3':
            mode = 3

    except AttributeError:
        if key == Key.esc:
            exit_program = True  # Set the flag to True to indicate program should exit
            return False  # Stop listener

def listen_for_keypress():
    with Listener(on_press=on_press) as listener:
        listener.join()


def cam():

    cap = cv2.VideoCapture(0)
    while True:
        if exit_program:
            break
        ret, frame = cap.read()
        if not ret:
            break
        if count % 5 != 0:  # This condition is unnecessary now; we'll use sleep instead
            nm = "frame" + str(count) + ".jpg"
            cv2.imwrite(nm, frame)
            if mode == 1:
                recognise(nm)
            elif mode == 2:
                ocr(nm)
            elif mode == 3:
                # Object detection
                detect_objects(frame)
        time.sleep(.2)  # Wait for .2 seconds before capturing the next frame
        count += 1  # Increment count here, outside the if condition

    cap.release()
    return 0