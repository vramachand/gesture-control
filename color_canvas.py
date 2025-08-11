import cv2
import numpy as np
import mediapipe as mp

# Setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Color palette
palette = {
    "Blue":   ((20, 20), (70, 70), (255, 0, 0)),
    "Green":  ((80, 20), (130, 70), (0, 255, 0)),
    "Red":    ((140, 20), (190, 70), (0, 0, 255)),
    "Yellow": ((200, 20), (250, 70), (0, 255, 255)),
    "White":  ((260, 20), (310, 70), (255, 255, 255))
}

# Drawing state
canvas = None
prev_x, prev_y = 0, 0
draw_color = (255, 0, 0)
drawing = False

# Helper: Finger state
def is_finger_up(landmarks, idx_tip, idx_dip):
    return landmarks[idx_tip].y < landmarks[idx_dip].y

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Draw palette
    for name, ((x1, y1), (x2, y2), color) in palette.items():
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.putText(frame, name, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            x = int(lm[8].x * w)
            y = int(lm[8].y * h)

            # Check if index finger is up and middle down
            index_up = is_finger_up(lm, 8, 6)
            middle_up = is_finger_up(lm, 12, 10)

            if index_up and not middle_up:
                # Color selection
                for name, ((x1, y1), (x2, y2), color) in palette.items():
                    if x1 < x < x2 and y1 < y < y2:
                        draw_color = color
                        drawing = False
                        prev_x, prev_y = 0, 0
                        break
                else:
                    # Draw
                    if drawing and prev_x != 0 and prev_y != 0:
                        cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, 5)
                    prev_x, prev_y = x, y
                    drawing = True
            else:
                drawing = False
                prev_x, prev_y = 0, 0

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        drawing = False
        prev_x, prev_y = 0, 0

    # Overlay canvas
    combined = cv2.addWeighted(frame, 1, canvas, 1, 0)
    cv2.imshow("Air Canvas", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        canvas = np.zeros_like(frame)
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


