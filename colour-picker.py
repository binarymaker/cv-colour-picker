import cv2
import numpy as np

Upper_hsv = Lower_hsv = np.array([0,0,0])
cap = cv2.VideoCapture(0) 

def picker(event,x,y,flags,param):
  global Upper_hsv, Lower_hsv
  if event == cv2.EVENT_LBUTTONDOWN:
    pix = param[y, x]
    Upper_hsv =  np.array([pix[0] + 20, pix[1] + 50, pix[2] + 50])
    Lower_hsv =  np.array([pix[0] - 20, pix[1] - 50, pix[2] - 50])
    print("lower",Lower_hsv,"upper",Upper_hsv)


while True:
  ret, frame = cap.read()
  frame = cv2.flip(frame, 1)
  cv2.imshow("Frame image", frame)

  hsvImage=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
  mask=cv2.inRange(hsvImage,Lower_hsv,Upper_hsv)
  cv2.imshow("colour mask",mask)

  # mouse interface
  cv2.setMouseCallback("Frame image", picker, hsvImage)

  key=cv2.waitKey(30) & 0xFF
  if key == 27: # exit on ESC
    break

print("App closed.")
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
