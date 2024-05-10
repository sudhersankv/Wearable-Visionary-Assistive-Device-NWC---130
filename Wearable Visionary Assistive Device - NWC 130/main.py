import cv2
import sys
from ocr.OCR import ocr
from Voice.voiceout import *
from Voice.sp_recog import *
from Voice.voice_to_text import *
from objectdetection.objdetect import *
from pdfex.pdfextract import *
from facerec.reco import *

os.environ['KMP_DUPLICATE_LIB_OK']='True'


mode=3
count = 0
import time

def delete_generated_files():
    # Delete generated frame images
    for filename in glob.glob('frame*.jpg'):
        os.remove(filename)
    
    # Delete generated mp3 files
    for filename in glob.glob('output*.mp3'):
        os.remove(filename)

def cam():
    global mode
    global count
    # Load Camera
    cap = cv2.VideoCapture(0)
    while True:
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
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == 50:
            mode = 2
        elif key == 49:
            mode = 1
        elif key == 51:
            mode = 3
        elif key == 27:
            break
        elif key == 52:
            cap.release()
            cv2.destroyAllWindows()
            callme()
            break
        time.sleep(.2)  # Wait for 1 seconds before capturing the next frame
        count += 1  # Increment count here, outside the if condition
    

    cap.release()
    cv2.destroyAllWindows()
    delete_generated_files()
    
def callme():
    while True:
        speechreco()
        query = voice_to_text()

        response, docs = get_response_from_pdf(db, query)

        print(textwrap.fill(response, width=50))
        VO(response)
        if response == "Bye Master, I'm always at your service!":
            break     


text1 = extract_text_from_pdf('sample.pdf')
db = create_db_from_pdf(text1) 
cam()
