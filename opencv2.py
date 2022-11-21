# Documentation used to learn about opencv and mediapipe:

# Mediapipe handtracking documentation: https://google.github.io/mediapipe/solutions/hands.html
# Blog on on how to get started setting up hand-tracking in opencv: https://www.section.io/engineering-education/creating-a-hand-tracking-module/#prerequisites



import cv2
import mediapipe as mp
import math


cap = cv2.VideoCapture(0) # we create cap object
mpHands = mp.solutions.hands # mpHands is the module that contains all the tools to track and identify a hand in  a given image
hands = mpHands.Hands() # hands is the module we will be using to actually identify a hand from an image
mpDraw = mp.solutions.drawing_utils #mpDraw is the module that canx shows on screen the landmarks of the hand that are detected

while True:
    success, image = cap.read() # cap.read returns two values: a boolean (T/F) depending on whether it could successfully read the image or not (which we store in success), and image content gathered in a list format (numpy.ndarray) (which we store in image)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #we use cv2 module to convert the image content from BGR to RGB,  because mediapipe only works with RGB images
    results = hands.process(imageRGB)

    
    # results.multi_hand_landmarks is either a Nonetype: None (if no hand is detected), or a list that contains the coordinates of the landmarks of the hand

    # drawing slider
    cv2.putText(image,"Use the pace slider!", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    cv2.line(image, (40,80), (550,80), (0, 100, 204), 30)
    
    
    # checking whether a hand is detected
    if results.multi_hand_landmarks != None:
        for hand_landmarks in results.multi_hand_landmarks: # we are now looping through the objects hand_landmarks in results.multi_hand_landmarks, which are each of the hands the program
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape # .shape is a module that outputs the height, width and channel of the image
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8: # 8 is the number with which mediapipe identifies the landmark on the point of the index finger
                    cv2.circle(image, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                    Xindex = cx
                    Yindex = cy

                if id == 12:
                    cv2.circle(image, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                    Xring = cx
                    Yring = cy
            
            # Calculating distance between two hand points for each hand position
            distance = math.sqrt((Xring - Xindex)**2 + (Yring-Yindex)**2)
            # creating thresh hold for grabbing:
            if distance <= 65 and  0 < Yring < 200 and 40 < Xring < 550:
                print('Grabbing!')
                # draw the circle wherever the fingers are
                newX = int((Xring + Xindex)/2)
                cv2.circle(image, (cx, 80), 20, (100, 100, 0), cv2.FILLED)
                
            else:
                # here we are testing if the variable is defined, if it isn't, draw it in origin position, i.e., x = 40
                try: newX
                except NameError: newX = 40
                cv2.circle(image, (newX,80), 20, (100, 100, 0), cv2.FILLED)
                


            

            mpDraw.draw_landmarks(image, hand_landmarks, mpHands.HAND_CONNECTIONS) # this is mediapipe's module to draw: it draws on the current 'image' some dots on the coordinates of 'hand_landmarks', and draws connections through them with the module 'mpHands.HAND_CONNECTIONS' 


    cv2.imshow("Output", image) # imshow is a module in opencv to show the image. This output is a a real-time video of the user
    cv2.waitKey(1)
