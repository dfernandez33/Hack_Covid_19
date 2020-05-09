import numpy as np
import cv2
import os




cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

img_counter = 0

print(my_path)

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
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cropped = frame[100:360, 120:520]

        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "/negative'")
        cv2.imwrite(os.path.join(path , img_name), cropped)
        print("{} written!".format(img_name))
        # if cropped.sum() > 52000000:
        #     print("CONGRATULATIONS! You're COVID-19 NEGATIVE")
        # else:
        #     print("We're sorry. You tested POSITIVE :(")
        print(cropped.sum())
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
