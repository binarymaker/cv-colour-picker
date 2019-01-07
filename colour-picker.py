import cv2
import numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore, uic
import sys

app = QtWidgets.QApplication([])
window = uic.loadUi("colour-pick.ui")
slider_value = [0,0,0,0,0,0]
cam_capture = True

Upper_hsv = Lower_hsv = np.array([0,0,0])
cap = cv2.VideoCapture(0) 

def picker(event,x,y,flags,param):
    global Upper_hsv, Lower_hsv
    global slider_value
    if event == cv2.EVENT_LBUTTONDOWN:
        pix = param[y, x]
        print("hsv pix",pix)
#        slider_value[0] = pix[0]
#        slider_value[3] = pix[0]
#        slider_value[1] = pix[1]
#        slider_value[4] = pix[1]
#        slider_value[2] = pix[2]
#        slider_value[5] = pix[2]

#        Upper_hsv =  np.array([pix[0] + 20, pix[1] + 50, pix[2] + 50])
#        Lower_hsv =  np.array([pix[0] - 20, pix[1] - 50, pix[2] - 50])
#        print("lower",Lower_hsv,"upper",Upper_hsv)

def disp_slider_value():
    global slider_value
    slider_value[0] = window.slider_h_min.value()
    slider_value[3] = window.slider_h_max.value()
    slider_value[1] = window.slider_s_min.value()
    slider_value[4] = window.slider_s_max.value()
    slider_value[2] = window.slider_l_min.value()
    slider_value[5] = window.slider_l_max.value()
    window.lineEdit_h_min.setText(str(slider_value[0]))
    window.lineEdit_h_max.setText(str(slider_value[3]))
    window.lineEdit_s_min.setText(str(slider_value[1]))
    window.lineEdit_s_max.setText(str(slider_value[4]))
    window.lineEdit_l_min.setText(str(slider_value[2]))
    window.lineEdit_l_max.setText(str(slider_value[5]))

def slider_setup():
    window.slider_h_min.setRange(0,179)
    window.slider_h_max.setRange(0,179)
    window.slider_s_min.setRange(0,255)
    window.slider_s_max.setRange(0,255)
    window.slider_l_min.setRange(0,255)
    window.slider_l_max.setRange(0,255)
    window.slider_h_min.setValue(0)
    window.slider_h_max.setValue(179)
    window.slider_s_min.setValue(0)
    window.slider_s_max.setValue(255)
    window.slider_l_min.setValue(0)
    window.slider_l_max.setValue(255)
    window.slider_h_min.valueChanged.connect(disp_slider_value)
    window.slider_h_max.valueChanged.connect(disp_slider_value)
    window.slider_s_min.valueChanged.connect(disp_slider_value)
    window.slider_s_max.valueChanged.connect(disp_slider_value)
    window.slider_l_min.valueChanged.connect(disp_slider_value)
    window.slider_l_max.valueChanged.connect(disp_slider_value)

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def change_slider_value():
    global slider_value

    try:
        slider_value[0] = int(window.lineEdit_h_min.text())
    except:
        slider_value[0] = 0
    try:
        slider_value[3] = int(window.lineEdit_h_max.text())
    except:
        slider_value[3] = 0

    try:
        slider_value[1] = int(window.lineEdit_s_min.text())
    except:
        slider_value[1] = 0
    try:
        slider_value[4] = int(window.lineEdit_s_max.text())
    except:
        slider_value[4] = 0

    try:
        slider_value[2] = int(window.lineEdit_l_min.text())
    except:
        slider_value[3] = 0
    try:
        slider_value[5] = int(window.lineEdit_l_max.text())
    except:
        slider_value[5] = 0

    slider_value[0] = constrain(slider_value[0], 0, 179)
    slider_value[3] = constrain(slider_value[3], 0, 179)
    slider_value[1] = constrain(slider_value[1], 0, 255)
    slider_value[4] = constrain(slider_value[4], 0, 255)
    slider_value[2] = constrain(slider_value[2], 0, 255)
    slider_value[5] = constrain(slider_value[5], 0, 255)

    window.slider_h_min.setValue(slider_value[0])
    window.slider_h_max.setValue(slider_value[3])
    window.slider_s_min.setValue(slider_value[1])
    window.slider_s_max.setValue(slider_value[4])
    window.slider_l_min.setValue(slider_value[2])
    window.slider_l_max.setValue(slider_value[5])

def value_edit():
    window.lineEdit_h_min.textChanged.connect(change_slider_value)
    window.lineEdit_h_max.textChanged.connect(change_slider_value)
    window.lineEdit_s_min.textChanged.connect(change_slider_value)
    window.lineEdit_s_max.textChanged.connect(change_slider_value)
    window.lineEdit_l_min.textChanged.connect(change_slider_value)
    window.lineEdit_l_max.textChanged.connect(change_slider_value)

def hsv_range_ui():
    min_range = np.array([slider_value[0],slider_value[1],slider_value[2]],dtype=np.uint8)
    max_range = np.array([slider_value[3],slider_value[4],slider_value[5]],dtype=np.uint8)
    return (min_range,max_range)

def cam_disable():
    global cam_capture
    cam_capture = ~cam_capture

    if cam_capture == True:
        window.button_capture.setText('Capture')
    else:
        window.button_capture.setText('View camera')

def image_capture():
    window.button_capture.clicked.connect(cam_disable)
    
slider_setup()
disp_slider_value()
value_edit()
image_capture()

window.show()

while True:
    if(cam_capture == True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
#    frame = cv2.imread("HSV_image.png")
    cv2.imshow("Frame image", frame)

    hsvImage=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    l_hsv,h_hsv = hsv_range_ui()
    print("ui range",l_hsv,h_hsv)
    mask=cv2.inRange(hsvImage,l_hsv,h_hsv)
    cv2.imshow("colour mask",mask)

    # mouse interface
    cv2.setMouseCallback("Frame image", picker, hsvImage)

    key=cv2.waitKey(30) & 0xFF
    if key == 27: # exit on ESC
        break

# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
print("App closed.")
#app.exec_()
sys.exit()
