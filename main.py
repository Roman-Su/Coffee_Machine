import os
from cvzone.HandTrackingModule import HandDetector
import cv2
import imutils

cap = cv2.VideoCapture(0)

#cap.set(3, 640) #Does not work properly, So have to use imutils
#cap.set(4, 4800)

imgBackground = cv2.imread("Resources/Background.png")

# Importing all the mode to the list
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes  = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))

# Importing all the icons to the list
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))


modeType = 0  # Changing selection step
selection = -1
counter=0
selectionspeed = 7
detector = HandDetector(detectionCon=0.8, maxHands=1)
modePositions = [(1136,196),(1000,384),(1136,581)]
counterpose = 0
selectionlist = [-1, -1, -1]


while True:
    success, img = cap.read()
    img = imutils.resize(img, width=640)
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    #esize = cv2.resize(img, (640, 480))
    # Overlaying the webcam feed on the background image
    imgBackground[139:139 + 360, 50:50 + 640] = img
    imgBackground[0:720, 847:1280] = listImgModes[modeType]

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    if hands and counterpose==0 and modeType<3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print (fingers1)

        if fingers1 == [0,1,0,0,0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0,1,1,1,0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0
        if counter>0:
            counter += 1
            print (counter)

            cv2.ellipse(imgBackground,modePositions[selection-1],(103,103),
                        0,0,counter*selectionspeed,(0,255,0),20)
            if counter*selectionspeed>360:
                selectionlist[modeType]=selection
                modeType+=1
                counter=0
                selection=-1
                counterpose=1
# To pause after selection is made
    if counterpose>0:
        counterpose+=1
        if counterpose>40:
            counterpose = 0
   # Add selection icon at the bolttom
    if selectionlist[0] != -1:
        imgBackground[636:636+65,133:133+65] = listImgIcons[selectionlist[0]-1]
    if selectionlist[1] != -1:
        imgBackground[636:636+65,340:340+65] = listImgIcons[2+selectionlist[1]]
    if selectionlist[2] != -1:
        imgBackground[636:636+65,542:542+65] = listImgIcons[5+selectionlist[2]]

    #Displaying
    #cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)
