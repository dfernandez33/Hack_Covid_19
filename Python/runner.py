# Add necesary import statements above
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import numpy as np
from sklearn import svm
import cv2
import os
import serial

# Initialize firebase app
cred = credentials.Certificate("hack-covid-19-e4018-firebase-adminsdk-pt6vv-e257520af7.json")
app = firebase_admin.initialize_app(cred)
# get reference to firestore
db = firestore.client()

###############################
# TODO: implement qr code reader using camera
###############################

# use this function to write the result of the test to the db
# result input should be a boolean value
def write_test_result_to_db(result):
    current_test = test_stand_data["tests"][-1] # most recent test will always be at the end of the array
    try:
        test_ref = db.collection("tests").document(current_test)
        test_ref.update({
            "result": result
        })
        return 1
    except:
        return 0
def clear_leds():
    ser.write(b'B')
    ser.write(b'D')

hard_coded_stand_id = "HrPMcrft5L0k4nH6MZNC"
qrcode_data = "7dd85cd4-86c1-4801-9882-2b795baef2d8" # unlock code obtained from scanning qrcode
try:
    test_stand_ref = db.collection("test-stands").document(hard_coded_stand_id)
    test_stand_data = test_stand_ref.get().to_dict()
    print(test_stand_data["unlockCode"])
    if test_stand_data["unlockCode"] == qrcode_data:
        # functionality to run test using Alfie, and run write_test_result_to_db
        # -----------------------------------------------------------------------
        ser = serial.Serial('/dev/cu.usbmodem14601', 9600)
        clear_leds()
        cam = cv2.VideoCapture(1)
        cv2.namedWindow("test")
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)

            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 114:
                # R pressed. This resets LEDs
                clear_leds()
            elif k%256 == 32:
                # SPACE pressed
                clear_leds()
                cropped = frame[100:360, 120:520]
                edges = cv2.Canny(cropped,100,200)

                if edges.sum() < 190000:
                    print("CONGRATULATIONS! You're COVID-19 NEGATIVE")
                    ser.write(b'C')
                    write_test_result_to_db("NEGATIVE")
                else:
                    print("We're sorry. You tested POSITIVE :(")
                    ser.write(b'A')
                    write_test_result_to_db("POSITIVE")

        cam.release()
        cv2.destroyAllWindows()
        # -----------------------------------------------------------------------
    else:
        print("QR Code does not correspond to this testing stand. Please try again or verify that you are using the"
              "correct stand.")
        exit()
except:
    print("No such document")
