import cv2
import numpy as np
import mediapipe as mp
import time
import random

# ---------------- Mediapipe Setup ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ---------------- Game Initialization ----------------
def init_game():
    global board, user_symbol, computer_symbol, user_turn, move_made
    global selected_cell, selection_made, winner
    global restart_hover_start
    board = [['' for _ in range(3)] for _ in range(3)]
    user_symbol = None
    computer_symbol = None
    user_turn = True
    move_made = False
    selected_cell = None
    selection_made = False
    winner = None
    restart_hover_start = None

cell_size = 150
offset = 50
width, height = 5 * cell_size + 2 * offset, 3 * cell_size + 2 * offset
window_name = "Tic Tac Toe"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# (Kept in case you want to bring back time-based selection visuals)
hover_threshold_restart = 1.5

init_game()

# ---------------- Gesture Detection ----------------
def is_fist(hand_landmarks, image_w, image_h):
    """
    Detects a fist by checking if at least 3 of the 4 fingers (index, middle, ring, pinky)
    have their TIP below their PIP (folded). Thumb is ignored for robustness.
    """
    folded = 0

    # Index, Middle, Ring, Pinky
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip, pip in zip(finger_tips, finger_pips):
        tip_y = hand_landmarks.landmark[tip].y * image_h
        pip_y = hand_landmarks.landmark[pip].y * image_h
        if tip_y > pip_y:  # folded (lower on image)
            folded += 1

    return folded >= 3

# ---------------- Drawing Functions ----------------
def draw_selection_screen(img, hover_pos):
    img[:] = (255, 255, 255)

    # Define consistent box positions
    x_box = (width // 3 - 75, height // 2 - 75, 150, 150)
    o_box = (2 * width // 3 - 75, height // 2 - 75, 150, 150)

    # Draw X box
    cv2.rectangle(img, (x_box[0], x_box[1]),
                  (x_box[0] + x_box[2], x_box[1] + x_box[3]), (0,0,255), 3)
    cv2.line(img, (x_box[0] + 20, x_box[1] + 20),
             (x_box[0] + 130, x_box[1] + 130), (0,0,255), 7)
    cv2.line(img, (x_box[0] + 20, x_box[1] + 130),
             (x_box[0] + 130, x_box[1] + 20), (0,0,255), 7)

    # Draw O box
    cv2.rectangle(img, (o_box[0], o_box[1]),
                  (o_box[0] + o_box[2], o_box[1] + o_box[3]), (255,0,0), 3)
    cv2.circle(img, (o_box[0] + 75, o_box[1] + 75), 60, (255,0,0), 7)

    cv2.putText(img, "Choose! (make a FIST to confirm)",
                (width//6, height//4), cv2.FONT_HERSHEY_SIMPLEX, 1, (50,50,50), 2)

    # Hover highlight
    if hover_pos:
        x, y = hover_pos
        if x_box[0] < x < x_box[0] + x_box[2] and x_box[1] < y < x_box[1] + x_box[3]:
            cv2.circle(img, (x, y), 25, (0,0,255), 3)
        elif o_box[0] < x < o_box[0] + o_box[2] and o_box[1] < y < o_box[1] + o_box[3]:
            cv2.circle(img, (x, y), 25, (255,0,0), 3)

    return x_box, o_box

def draw_board(img):
    img[:] = (255, 255, 255)
    for i in range(4):
        cv2.line(img, (offset + i * cell_size, offset),
                 (offset + i * cell_size, offset + 3 * cell_size), (0,0,0), 3)
        cv2.line(img, (offset, offset + i * cell_size),
                 (offset + 3 * cell_size, offset + i * cell_size), (0,0,0), 3)

    for r in range(3):
        for c in range(3):
            center = (offset + c * cell_size + cell_size//2,
                      offset + r * cell_size + cell_size//2)
            if board[r][c] == 'X':
                cv2.line(img, (center[0]-40, center[1]-40),
                         (center[0]+40, center[1]+40), (0,0,255), 5)
                cv2.line(img, (center[0]-40, center[1]+40),
                         (center[0]+40, center[1]-40), (0,0,255), 5)
            elif board[r][c] == 'O':
                cv2.circle(img, center, 50, (255,0,0), 5)

# ---------------- Game Logic ----------------
def get_cell_from_pos(x, y):
    if x is None or y is None:
        return None
    if offset < x < offset + 3*cell_size and offset < y < offset + 3*cell_size:
        col = (x - offset) // cell_size
        row = (y - offset) // cell_size
        return int(row), int(col)
    return None

def computer_move():
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = computer_symbol

def check_winner(sym):
    lines = board + [list(col) for col in zip(*board)] \
            + [[board[i][i] for i in range(3)]] \
            + [[board[i][2-i] for i in range(3)]]
    return any(all(cell == sym for cell in line) for line in lines)

# ---------------- Main Loop ----------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    cursor_pos = None
    gesture_confirmed = False

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        h, w, _ = frame.shape
        # Cursor = average of all landmarks
        x = int(np.mean([lm.x for lm in hand_landmarks.landmark]) * w)
        y = int(np.mean([lm.y for lm in hand_landmarks.landmark]) * h)
        cursor_pos = (x, y)
        gesture_confirmed = is_fist(hand_landmarks, w, h)
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Map cursor to canvas coordinates
    if cursor_pos:
        fx = int(cursor_pos[0] * width / frame.shape[1])
        fy = int(cursor_pos[1] * height / frame.shape[0])
    else:
        fx, fy = None, None

    # Debug text for fist detection
    if gesture_confirmed:
        cv2.putText(canvas, "FIST DETECTED", (50, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 3)

    # -------------- Symbol Selection Phase --------------
    if not selection_made:
        x_box, o_box = draw_selection_screen(canvas, (fx, fy) if fx and fy else None)

        if fx is not None and fy is not None:
            # Draw cursor
            cv2.circle(canvas, (fx, fy), 15, (0, 255, 0), -1)

            # Confirm selection with fist
            if x_box[0] < fx < x_box[0] + x_box[2] and x_box[1] < fy < x_box[1] + x_box[3]:
                if gesture_confirmed:
                    user_symbol = 'X'
                    computer_symbol = 'O'
                    selection_made = True
            elif o_box[0] < fx < o_box[0] + o_box[2] and o_box[1] < fy < o_box[1] + o_box[3]:
                if gesture_confirmed:
                    user_symbol = 'O'
                    computer_symbol = 'X'
                    selection_made = True

    # -------------- Game Phase --------------
    else:
        draw_board(canvas)

        # Draw cursor
        if fx is not None and fy is not None:
            cv2.circle(canvas, (fx, fy), 15, (0, 255, 0), -1)

        if not winner:
            cell = get_cell_from_pos(fx, fy)

            # Place move only on fist
            if cell and user_turn and gesture_confirmed and board[cell[0]][cell[1]] == '':
                board[cell[0]][cell[1]] = user_symbol
                user_turn = False
                move_made = True

            if move_made:
                if not check_winner(user_symbol):
                    computer_move()
                user_turn = True
                move_made = False

            if check_winner(user_symbol):
                winner = '                             You Win!'
            elif check_winner(computer_symbol):
                winner = '                          Computer Wins!'
            elif all(all(cell != '' for cell in row) for row in board):
                winner = '                                Draw!'

        # ----------- Endgame Screen with Restart -----------
        if winner:
            cv2.putText(canvas, winner, (offset, height - 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

            restart_box = (width//3 + 250, height - 110, 300, 70)
            cv2.rectangle(canvas, (restart_box[0], restart_box[1]),
                          (restart_box[0] + restart_box[2], restart_box[1] + restart_box[3]), (0,200,0), 3)
            cv2.putText(canvas, "Play Again", (restart_box[0] + 60, restart_box[1] + 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,0), 2)

            if fx is not None and fy is not None:
                if restart_box[0] < fx < restart_box[0] + restart_box[2] and restart_box[1] < fy < restart_box[1] + restart_box[3]:
                    cv2.circle(canvas, (fx, fy), 25, (0,200,0), 3)
                    # Require fist to restart
                    if gesture_confirmed:
                        init_game()

    cv2.imshow(window_name, canvas)

    # Press ESC or 'q' to quit
    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
cv2.destroyAllWindows()

