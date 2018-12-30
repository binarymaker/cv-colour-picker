import cv2
import numpy as np

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    cv2.imshow("Frame image", frame)

    hsvImage=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    Lower_hsv = np.array([110, 50, 50])
    Upper_hsv = np.array([130,255,255])
    mask=cv2.inRange(hsvImage,Lower_hsv,Upper_hsv)
    cv2.imshow("colour mask",mask)
    key=cv2.waitKey(30) & 0xFF
    if key == 27: # exit on ESC
        break

print("App closed.")
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
