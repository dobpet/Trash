import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  while cap.isOpened():
    success, image = cap.read()
    image_height, image_width, _ = image.shape
    #to improve performance
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
###########################################################################################################################################################################
        ids0, ids1, ids2, ids3, ids4 = [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0] #quest
        ids5, ids6, ids7, ids8, ids9 = [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0] #quest
        ids10, ids11, ids12, ids13, ids14 = [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0] #quest
        ids15, ids16, ids17, ids18, ids19, ids20 = [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0], [0, 0,0] #quest
        x_max = 0
        y_max = 0
        x_min = image_width
        y_min = image_height
###########################################################################################################################################################################
        for ids, landmrk in enumerate(hand_landmarks.landmark):
            cx = int(landmrk.x * image_width) # position x
            cy = int(landmrk.y * image_height) # position Y
            cz = int(landmrk.z)  # position z
            if cx > x_max:
                x_max = cx
            if cx < x_min:
                x_min = cx
            if cy > y_max:
                y_max = cy
            if cy < y_min:
                y_min = cy
############################################################################################################################################################################
#QUEST:
            #0 -create  variables/list/field for every landmarks (0-20)  (handmark_number=ids,position x, position y)
            if ids == 0:
              ids0 = [cx, cy, cz]
            elif ids == 1:
              ids1 = [cx, cy, cz]
            elif ids == 2:
              ids2 = [cx, cy, cz]
            elif ids == 3:
              ids3 = [cx, cy, cz]
            elif ids == 4:
              ids4 = [cx, cy, cz]
            elif ids == 5:
              ids5 = [cx, cy, cz]
            elif ids == 6:
              ids6 = [cx, cy, cz]
            elif ids == 7:
              ids7 = [cx, cy, cz]
            elif ids == 8:
              ids8 = [cx, cy, cz]
            elif ids == 9:
              ids9 = [cx, cy, cz]
            elif ids == 10:
              ids10 = [cx, cy, cz]
            elif ids == 11:
              ids11 = [cx, cy, cz]
            elif ids == 12:
              ids12 = [cx, cy, cz]
            elif ids == 13:
              ids13 = [cx, cy, cz]
            elif ids == 14:
              ids14 = [cx, cy, cz]
            elif ids == 15:
              ids15 = [cx, cy, cz]
            elif ids == 16:
              ids16 = [cx, cy, cz]
            elif ids == 17:
              ids17 = [cx, cy, cz]
            elif ids == 18:
              ids18 = [cx, cy, cz]
            elif ids == 19:
              ids19 = [cx, cy, cz]
            elif ids == 20:
              ids20 = [cx, cy, cz]

            #1 -calculate distance between two points
            #distance = int(math.sqrt((ids8[0] - ids4[0]) ** 2 + (ids8[1] - ids4[1]) ** 2)) #alternative way to calculate distance of points in 3D world look math "sqrt" and "hypot"
            distance = int(math.hypot((ids8[0] - ids4[0]), (ids8[1] - ids4[1])))
            print(f"Distance between ids8 and ids4: {distance}")
            if distance < 50:
                print("too small")

########draw hand point, line from poin to point, write the lenth of line.... just exemple to remember
        cv2.circle(image, (ids8[0],ids8[1]), 10, (255, 0, 128), cv2.FILLED)
        cv2.line(image, (ids8[0],ids8[1]), (ids4[0],ids4[1]), (255, 0, 128), 3)
        #need to flip only text
        image = cv2.flip(image, 1)
        cv2.putText(image, str(int(distance)), ((image_width-ids4[0]-90),ids4[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 2,cv2.LINE_AA,False)
        image = cv2.flip(image, 1)
#########draw rectangle of hand
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2) #draw rectangle around hand.... just exemple

            #2 -recognize fist (wrist_position and position of EVERY finger TIP at some distance away from wrist)
            #3 -calculate how many fingers is opened....and print it, finger tip is at some distance away from MPC
            #4 -recognize gesto and print its name (compared position of every landmarks and recognize gesto)
            #5 -make it work at any distance away from camera #chek distance from wrist to finger tip and compare it with lenth from wrist to tip
            #6 -slice program for better reading, make separate gesture program


############################################################################################################################################################################
    # Flip the image horizontally for a selfie-view display
    cv2.imshow('HandTracking', cv2.flip(image, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()