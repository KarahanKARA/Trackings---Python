import socket

import cv2
import mediapipe as mp
import time
cap = cv2.VideoCapture(0)  ############################# CAMERA 1'i KULLANIYOR
########################################################## KISA KENARIN X'İ X OLARAK GİDECEK
HOST = '127.0.0.1'
PORT = 7000
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
xToplamlari = 0
counter = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                print("x : ",cx)
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
                xToplamlari = xToplamlari + cx
                counter = counter + 1
                if counter > 50:
                    xToplamlari = (int(1000 * (xToplamlari / 50) / 600))  # X matematiksel işlem

                    xDegeri = str(xToplamlari) + "x"
                    xToplamlari = 0
                    counter = 0
                    conn.send(bytes(xDegeri, "utf-8"))


            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)