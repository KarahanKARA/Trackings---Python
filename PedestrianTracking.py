import cv2
import imutils
import socket

HOST = '127.0.0.1'
PORT = 7000


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
xToplamlari = 0
yToplamlari = 0
counter = 0
counter2=0
while cap.isOpened():
    ret, image = cap.read()
    if ret:
        image = imutils.resize(image, width=min(800, image.shape[1]))
        (regions, _) = hog.detectMultiScale(image,winStride=(8, 8),padding=(16, 16),scale=1.05)
        for (x, y, w, h) in regions:
            cv2.rectangle(image, (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

            xToplamlari = xToplamlari + x
            yToplamlari = yToplamlari + y
            counter = counter + 1
            if counter > 10:
                print("Y ortalaması: ", yToplamlari / 10)
                xToplamlari = (int(1000 * (xToplamlari / 10) / 500))  # X matematiksel işlem
                yToplamlari = int(500 * (yToplamlari / 10) / 300)  # Y matematiksel işlem
                yToplamlari = 500 - yToplamlari
                print("yazılan y: ", yToplamlari)
                xDegeri = str(xToplamlari) +"x"
                yDegeri = str(yToplamlari) +"y"
                uzunString = xDegeri + yDegeri
                xToplamlari = 0
                yToplamlari = 0
                counter = 0
                conn.send(bytes(xDegeri, "utf-8"))
                conn.send(bytes(yDegeri, "utf-8"))
                counter2 = counter2 + 1

                if counter2 > 2000:
                    counter2 = 0

        cv2.imshow("Image", image)

        if cv2.waitKey(40) == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()


# def detect(frame):
#     bounding_box_cordinates, weights = HOGCV.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.15)
#
#     person = 1
#     for x, y, w, h in bounding_box_cordinates:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.putText(frame, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
#         person += 1
#
#     cv2.putText(frame, 'Status : Detecting ', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
#     cv2.putText(frame, f'Total Persons : {person - 1}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
#     cv2.imshow('output', frame)
#     return frame
#
# def detectByCamera():
#     video = cv2.VideoCapture(0)
#     print('Detecting people...')
#     while True:
#         check, frame = video.read()
#         frame = detect(frame)
#         key = cv2.waitKey(1)
#         if key == ord('q'):
#             break
#
#     video.release()
#     cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     HOGCV = cv2.HOGDescriptor()
#     HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#     detectByCamera()