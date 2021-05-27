import cv2
import numpy as np
import time
import mediapipe as mp

from kafka import KafkaProducer
from pyfirmata import Arduino, SERVO
from time import sleep

producer = KafkaProducer(bootstrap_servers='localhost:9092')

#port='Port_#0002.Hub_#0001'
pin=10
pin1=12
board=Arduino('COM3')

board.digital[pin].mode=SERVO

def rotateServo(pin, angle):
    board.digital[pin].write(angle)
    #sleep(0.015)

cap=cv2.VideoCapture(0)
mpHands= mp.solutions.hands
hands= mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
ptime=0
ctime=0
a=0
b=0
c=0
d=0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('handgesx.avi', fourcc, 20.0, size)



while True:
    success, img= cap.read()
    imgRGB= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w), int(lm.y*h)
                #print(id, cx,cy) :
                cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

                if id == 8 :
                    a = cx
                if id == 4:
                    b = cx
                    dist=b-a

                    print('LLLLL')
                    print(dist)
                    if dist<abs(-15):
                       print('four')
                       cv2.putText(img, 'thumb close', (90, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                       #for i in range(0, 180):
                       rotateServo(pin,145)
                       rotateServo(pin1, 145)
                       producer.send('TestTopic', b'0')

                    if dist>abs(30):
                       print('five')
                       cv2.putText(img, 'thumb open', (90, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                       #for i in range(80,1, -1):
                       rotateServo(pin,100)
                       rotateServo(pin1, 100)
                       producer.send('TestTopic', b'1')
                #print(id, cx, cy)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)



    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime=ctime
    #cv2.putText(img, f'fps: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow('Hand', img)
    cv2.waitKey(1)
    out.write(img)