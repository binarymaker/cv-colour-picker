import cv2
import numpy as np


cap = cv2.VideoCapture(0) 

def picker(event,x,y,flags,param):
  print('x=',x,'y=',y, 'colour',param[y, x])
  if event == cv2.EVENT_LBUTTONDOWN:
    pix = param[y, x]


def color_calibration(image,ch_gain):
  cimage = np.asarray(image, dtype=int)
  cimage[:,:,0] = image[:,:,0] * ch_gain[0]
  cimage[:,:,1] = image[:,:,1] * ch_gain[1]
  cimage[:,:,2] = image[:,:,2] * ch_gain[2]
  cimage = np.clip(cimage, a_min = 0, a_max = 255)
  cimage = np.asarray(cimage, dtype=np.uint8)
  return cimage

while True:
  ret, frame = cap.read()
  frame = cv2.flip(frame, 1)
  cv2.imshow("Frame image", frame)
  calbframe = color_calibration(frame, [1.5,1.5,1.5]) 
  cv2.imshow("calib image", calbframe)

  # mouse interface
  cv2.setMouseCallback("calib image", picker, calbframe)
  cv2.setMouseCallback("Frame image", picker, frame)

  key=cv2.waitKey(30) & 0xFF
  if key == 27: # exit on ESC
    break

print("App closed.")
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
