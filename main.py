import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
from pynput.keyboard import Controller,Key
from PIL import ImageFont
import mediapipe as mp



cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)


keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Ğ", "Ü"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ş", "İ", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", "Ö", "Ç", ">", ",", ".", "/"]]
finalText = ""
keyboard = Controller()

def transparent_layout(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1],
                                                   button.size[0],button.size[0]), 20 ,rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                                   (255, 144, 30), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    out = img.copy()
    alpaha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpaha, imgNew, 1 - alpaha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.size = size
        self.text = text


buttonlist = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonlist.append(Button([75 * j + 50, 75 * i + 50], key))



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = transparent_layout(img, buttonlist)

    if lmList:
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 8, y + 38), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                ##when clicked
                if l < 35:
                    keyboard.press(button.text)
                    if button.text == "-":
                        finalText = finalText[:-1]
                    elif button.text == ">":
                        finalText += " "
                    else:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 8, y + 38), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                        finalText += button.text
                        sleep(0.1)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
