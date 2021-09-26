#Windows 10
#Logitech C920 and Laptop builtin Cam
#Python 3.9.7
#OpenCV 4.5.3

#This simple program just loads eaither the Laptop Cam or the USB Cam. The main use for this program
#has been to test python + VScode install on Windows 10

import cv2
import mediapipe as mp
print (cv2.__version__)

#cam = cv2.VideoCapture(0)   #Laptop built in cam
cam = cv2.VideoCapture(1)   #Logitech USB cam.

print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while (cam.isOpened()):
    ret, frame = cam.read()

    if ret == True:
        #dimensions = frame.shape
        #print (dimensions)

        cv2.imshow('video', frame)
        cv2.moveWindow('video', 0, 0)

        if cv2.waitKey(1) == ord('q'):   #Press ESC to quit
            break
    else:
        break

cam.release()
cv2.destroyAllWindows()