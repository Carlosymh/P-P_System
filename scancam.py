from sre_constants import SUCCESS
import cv2 #pip install opencv-python-headless or pip install opencv-python
import numpy as np  
from pyzbar.pyzbar import decode #pip install pyzbar or pip install pyzbar[scripts]

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
i=0
while i<1:
    success,img= cap.read()
    for barcode in decode(img):
        myData= barcode.data.decode('utf-8')
        print(myData)
        pts= np.array([barcode.polygon],np.int32)
        pts= pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        i+=1
    cv2.imshow('Result',img)
    cv2.waitKey(1)
