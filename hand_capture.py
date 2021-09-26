#Windows 10
#Logitech C920 and Laptop builtin Cam
#Python 3.9.7
#OpenCV 4.5.3

#This program uses the MediaPipe package to recognise a hand using openCV. With this modeule, OpenCV
#will identify 21 points within the hand, with the ability to determine their position in the frame.
#The code also includes the ability to display Frames Per Second.

import cv2
import mediapipe as mp
import time
print (cv2.__version__)

cam = cv2.VideoCapture(1)   #Logitech USB cam.

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0   #Previous Time
cTime = 0   #Current Time

while (cam.isOpened()):
    ret, frame = cam.read()
    if ret == True:
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frameRGB)

        if (results.multi_hand_landmarks):
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    print(id, lm)
                    h, w, c = frame.shape   #Find height,width,channels of image
                    cx, cy = int(lm.x*w), int(lm.y*h)

                mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

        #Calculate and display Frames Per Second (FPS)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,  (255,0,0), 2)

        cv2.imshow('video', frame)
        cv2.moveWindow('video', 0, 0)

        if cv2.waitKey(1) == ord('q'):   #Press ESC to quit
            break
    else:
        break

cam.release()
cv2.destroyAllWindows()