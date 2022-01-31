import cv2
import socket

HOST = '127.0.0.1'
PORT = 7000
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
xToplamlari = 0
yToplamlari = 0
counter = 0
counter2=0

while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        xToplamlari = xToplamlari + x
        yToplamlari = yToplamlari + y
        counter = counter + 1
        if counter > 1:
            xToplamlari = (int(1000 * (xToplamlari / 1) / 500))  # X matematiksel işlem
            yToplamlari = int(500 * (yToplamlari / 1) / 300)  # Y matematiksel işlem
            yToplamlari = 500-yToplamlari
            if(yToplamlari<0):
                yToplamlari = -yToplamlari
            if(xToplamlari<0):
                xToplamlari = -xToplamlari
            print("yollanan y: ", yToplamlari)
            print("yollanan x: ", xToplamlari)
            xDegeri = str(xToplamlari)
            yDegeri = str(yToplamlari)
            xToplamlari = 0
            yToplamlari = 0
            counter = 0
            if counter2%2==1:
                conn.send(bytes(xDegeri, "utf-8"))
            else:
                conn.send(bytes(yDegeri, "utf-8"))
            counter2 = counter2+1


    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
cap.release()