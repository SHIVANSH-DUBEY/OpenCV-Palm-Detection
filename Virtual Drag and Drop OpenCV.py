import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

cx, cy, w, h = 100, 100, 200, 200


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # if the index finger tip is in the rectangle area,
        if cx - w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            self.posCenter = cursor


rectList = []
for x in range(5):
    rectList.append(DragRect([x*250 + 150, 150]))

rect = DragRect([150, 150])
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:

        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)
        if l < 30:
            cursor = lmList[8]  # index finger tip landmark
            # call the update here
            for rect in rectList:
                rect.update(cursor)

    # draw solid
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx - w//2, cy-h//2),
                      (cx+w//2, cy+h//2), colorR, cv2.FILLED)
        cvzone.cornerRect(img, (cx - w//2, cy-h//2,
                                w, h), 20, rt=0)

    cv2.imshow("image", img)
    cv2.waitKey(1)
