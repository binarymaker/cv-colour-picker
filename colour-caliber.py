import cv2
import numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore, uic
import sys

app = QtWidgets.QApplication([])
window = uic.loadUi("colour-caliber.ui")

pix_x = pix_y = 0
calib_gain = [1,1,1]


def colour_change():
  global calib_gain
  calib_gain[0] = window.slider_blue.value()/100
  calib_gain[1] = window.slider_green.value()/100
  calib_gain[2] = window.slider_red.value()/100
  window.label_blue.setText(str(calib_gain[0]))
  window.label_green.setText(str(calib_gain[1]))
  window.label_red.setText(str(calib_gain[2]))


window.slider_green.setRange(0,200)
window.slider_green.setValue(100)
window.slider_green.valueChanged.connect(colour_change)
window.slider_blue.setRange(0,200)
window.slider_blue.setValue(100)
window.slider_blue.valueChanged.connect(colour_change)
window.slider_red.setRange(0,200)
window.slider_red.setValue(100)
window.slider_red.valueChanged.connect(colour_change)

cap = cv2.VideoCapture(0) 

def picker(event,x,y,flags,param):
  global pix_x,pix_y
  if event == cv2.EVENT_LBUTTONDOWN:
    pix_y, pix_x =  y, x


def color_calibration(image,ch_gain):
  cimage = np.asarray(image, dtype=int)
  cimage[:,:,0] = image[:,:,0] * ch_gain[0]
  cimage[:,:,1] = image[:,:,1] * ch_gain[1]
  cimage[:,:,2] = image[:,:,2] * ch_gain[2]
  cimage = np.clip(cimage, a_min = 0, a_max = 255)
  cimage = np.asarray(cimage, dtype=np.uint8)
  return cimage

colour_change()
window.show()
capture_disable = False
while True:
  if capture_disable == False:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
#  frame = cv2.imread('colour-chart.jpg')
  cv2.imshow("Frame image", frame)
  calbframe = color_calibration(frame, calib_gain) 
  cv2.imshow("calib image", calbframe)

  # mouse interface
  cv2.setMouseCallback("calib image", picker, calbframe)
  cv2.setMouseCallback("Frame image", picker, frame)

  print("> calib colour",calbframe[pix_y,pix_x])
  key=cv2.waitKey(30) & 0xFF
  if key == 32: # space for capture image
    capture_disable = ~capture_disable
  if key == 27: # exit on ESC
    # cleanup the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()
    break
print("App closed.")
#app.exec_()
sys.exit()


