#Simple code to launch USB cam of Laptop cam.

import cv2
print (cv2.__version__)

cam = cv2.VideoCapture(0)   #Laptop built in cam
#cam = cv2.VideoCapture(1)   #Logitech USB cam.

while True:
    ret, frame = cam.read()

    cv2.imshow('video', frame)

    if cv2.waitKey(1) == ord('q'):   #Press ESC to quit
        break

cam.release()
cv2.destroyAllWindows()