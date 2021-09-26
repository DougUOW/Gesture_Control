#This program uses hand gestures to change the volume on the PC. By using mediaPipe, we can the use OpenCv to determine
#the postion of the hand and fingers, then we combine this with pycaw to adjust the volume of the PC.
#This program uses the class file "hand_tracking_module.py"
#It has the added feature that it uses the pinky finger to set the volume. The volume can only be set when
#this finger is down.
#Written on Windows 10 machine, using VScode

#Code taken from Murtaza's Workshop - Robotics and AI
#https://www.youtube.com/watch?v=9iEPzbG-xLE&t=82s

import cv2
import time
import numpy as np
import hand_tracking_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#############################
wCam, hCam = 640, 480
#############################
pTime = 0   #Previous Time
cTime = 0   #Current Time

cam = cv2.VideoCapture(0)   #Logitech USB cam.
cam.set(3, wCam)
cam.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colourVol = (255,0,0)

while (cam.isOpened()):
    ret, img = cam.read()
    if ret == True:
        #Find Hand
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=True)
        if len(lmList) != 0:

            #Filter based on size
            area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1])//100 
            print (area)
            if 300 < area < 1100:
                
                #Find distance between index and thumb
                length, img, lineInfo = detector.findDistance(4,8,img)
                print(length)
               
                #Convert Volume
                volBar = np.interp(length, [30, 225], [400, 150])
                volPer = np.interp(length, [30, 225], [0, 100])
                
                #Reduce resolution to make it smoother
                smoothness = 10
                volPer = smoothness * round(volPer/smoothness)
                
                #If pinky is down set volume
                fingers = detector.fingersUp()
                if not fingers[4]:
                    volume.SetMasterVolumeLevelScalar(volPer/100, None)
                    #Change colour of dot to indicate vol has been set
                    cv2.circle(img, (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED)
                    colourVol = (0,255,0)
                else:
                    colourVol = (255,0,0)

        #Drawings
        cv2.rectangle(img, (50, 150), (85, 400), (255,0,0),3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (125,125,255), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40,450), cv2.cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
        cVol = int(volume.GetMasterVolumeLevelScalar()*100)
        cv2.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_PLAIN, 2, colourVol, 2)

        #Calculate and display Frames Per Second (FPS)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

        cv2.imshow('video', img)
        cv2.moveWindow('video', 1000, 100)

        if cv2.waitKey(1) == ord('q'):   #Press q to quit
            break
    else:
        break

cam.release()
cv2.destroyAllWindows()
