import cv2
import mediapipe as mp
import serial
import time

# Change COM port based on your Arduino (e.g., "COM3" or "COM4")
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    tipIds = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tipIds[0]].x < hand_landmarks.landmark[tipIds[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tipIds[id]].y < hand_landmarks.landmark[tipIds[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
            totalFingers = count_fingers(handLms)

            cv2.putText(frame, f'Fingers: {totalFingers}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

            if totalFingers == 0:
                arduino.write(b'0')
            elif totalFingers == 1:
                arduino.write(b'1')
            elif totalFingers == 2:
                arduino.write(b'2')
            elif totalFingers == 3:
                arduino.write(b'3')
            elif totalFingers == 4:
                arduino.write(b'4')
            elif totalFingers == 5:
                arduino.write(b'5')

    cv2.imshow("Gesture LED Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
