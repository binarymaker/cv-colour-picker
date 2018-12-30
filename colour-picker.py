import cv2
import numpy as np

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    cv2.imshow("Frame image", frame)

    key=cv2.waitKey(30) & 0xFF
    if key == 27: # exit on ESC
        break

print("App closed.")
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
