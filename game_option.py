import cv2
import numpy as np
import mediapipe as mp
import time
import random

# Mediapipe hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Tic Tac Toe board initialization
board = [['' for _ in range(3)] for _ in range(3)]
cell_size = 150  # size of each square
offset = 50      # margin from window edges

# Window size
width, height = 3 * cell_size + 2 * offset, 3 * cell_size + 2 * offset

# Hover timing thresholds
hover_threshold_select = 1.5
hover_threshold_move = 1.0

# Game variables
user_symbol = None
computer_symbol = None
user_turn = True
move_made = False
selected_cell = None
hover_start_time = None
selection_made = False

def draw_selection_screen(img, hover_pos):
    img[:] = (255, 255, 255)
    # Draw X box
    x_box = (width // 4 - 75, height // 2 - 75, 150, 150)
    cv2.rectangle(img, (x_box[0], x_box[1]), (x_box[0] + x_box[2], x_box[1] + x_box[3]), (0,0,255), 3)
    cv2.line(img, (x_box[0] + 20, x_box[1] + 20), (x_box[0] + 130, x_box[1] + 130), (0,0,255), 7)
    cv2.line(img, (x_box[0] + 20, x_box[1] + 130), (x_box[0] + 130, x_box[1] + 20), (0,0,255), 7)

    # Draw O box
    o_box = (3 * width // 4 - 75, height // 2 - 75, 150, 150)
    cv2.rectangle(img, (o_box[0], o_box[1]), (o_box[0] + o_box[2], o_box[1] + o_box[3]), (255,0,0), 3)
    cv2.circle(img, (o_box[0] + 75, o_box[1] + 75), 60, (255,0,0), 7)

    # Instructions
    cv2.putText(img, "Choose your symbol by hovering", (width//6, height//4), cv2.FONT_HERSHEY_SIMPLEX, 1, (50,50,50), 2)
    #cv2.putText(img, "Hover over X or O for 1.5 seconds", (width//6, height//4 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50,50,50), 1)

    # Draw hover circle if over selection
    if hover_pos:
        x, y = hover_pos
        # Check if inside X box
        if x_box[0] < x < x_box[0] + x_box[2] and x_box[1] < y < x_box[1] + x_box[3]:
            cv2.circle(img, (x, y), 25, (0,0,255), 3)
        elif o_box[0] < x < o_box[0] + o_box[2] and o_box[1] < y < o_box[1] + o_box[3]:
            cv2.circle(img, (x, y), 25, (255,0,0), 3)

def draw_board(img):
    img[:] = (255, 255, 255)

    # Draw grid lines
    for i in range(4):
        # Vertical lines
        cv2.line(img, (offset + i * cell_size, offset), (offset + i * cell_size, offset + 3 * cell_size), (0,0,0), 3)
        # Horizontal lines
        cv2.line(img, (offset, offset + i * cell_size), (offset + 3 * cell_size, offset + i * cell_size), (0,0,0), 3)

    # Draw existing X and O
    for r in range(3):
        for c in range(3):
            center = (offset + c * cell_size + cell_size//2, offset + r * cell_size + cell_size//2)
            if board[r][c] == 'X':
                cv2.line(img, (center[0]-40, center[1]-40), (center[0]+40, center[1]+40), (0,0,255), 5)
                cv2.line(img, (center[0]-40, center[1]+40), (center[0]+40, center[1]-40), (0,0,255), 5)
            elif board[r][c] == 'O':
                cv2.circle(img, center, 50, (255,0,0), 5)

def get_cell_from_pos(x, y):
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
    lines = board + [list(col) for col in zip(*board)] + [[board[i][i] for i in range(3)]] + [[board[i][2-i] for i in range(3)]]
    return any(all(cell == sym for cell in line) for line in lines)

# Start capturing video
cap = cv2.VideoCapture(0)

hover_start_time = None
hover_pos = None
selection_hover_pos = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    cursor_pos = None
    fist_closed = False

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]

        # Finger detection: index finger up and others down
        fingers = []
        tips = [4, 8, 12, 16, 20]
        for i, tip in enumerate(tips):
            tip_y = hand_landmarks.landmark[tip].y
            dip_y = hand_landmarks.landmark[tip - 2].y
            fingers.append(tip_y < dip_y)
        if fingers[1] and not any(fingers[2:]):
            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            cursor_pos = (x, y)
        else:
            fist_closed = True

        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Scale cursor position to canvas coordinates
    if cursor_pos:
        fx = int(cursor_pos[0] * width / frame.shape[1])
        fy = int(cursor_pos[1] * height / frame.shape[0])
    else:
        fx, fy = None, None

    if not selection_made:
        # Draw selection screen
        draw_selection_screen(canvas, (fx, fy) if fx and fy else None)

        # Check if cursor is over X or O
        x_box = (width // 4 - 75, height // 2 - 75, 150, 150)
        o_box = (3 * width // 4 - 75, height // 2 - 75, 150, 150)

        if fx and fy:
            if x_box[0] < fx < x_box[0] + x_box[2] and x_box[1] < fy < x_box[1] + x_box[3]:
                if hover_pos != 'X':
                    hover_start_time = time.time()
                    hover_pos = 'X'
                elif time.time() - hover_start_time > hover_threshold_select:
                    user_symbol = 'X'
                    computer_symbol = 'O'
                    selection_made = True
            elif o_box[0] < fx < o_box[0] + o_box[2] and o_box[1] < fy < o_box[1] + o_box[3]:
                if hover_pos != 'O':
                    hover_start_time = time.time()
                    hover_pos = 'O'
                elif time.time() - hover_start_time > hover_threshold_select:
                    user_symbol = 'O'
                    computer_symbol = 'X'
                    selection_made = True
            else:
                hover_pos = None
                hover_start_time = None

    else:
        draw_board(canvas)
        # Show green cursor circle if finger detected and no fist
        if fx and fy and not fist_closed:
            cv2.circle(canvas, (fx, fy), 15, (0, 255, 0), -1)

        cell = get_cell_from_pos(fx, fy) if fx and fy else None
       # global selected_cell
       # global hover_start_time

        if cell and not fist_closed and user_turn:
            if selected_cell != cell:
                selected_cell = cell
                hover_start_time = time.time()
            else:
                if time.time() - hover_start_time > hover_threshold_move and board[cell[0]][cell[1]] == '':
                    board[cell[0]][cell[1]] = user_symbol
                    user_turn = False
                    move_made = True
                    selected_cell = None
                    hover_start_time = None
        else:
            selected_cell = None
            hover_start_time = None

        if move_made:
            if not check_winner(user_symbol):
                computer_move()
            user_turn = True
            move_made = False

        winner = None
        if check_winner(user_symbol):
            winner = 'You Win!'
        elif check_winner(computer_symbol):
            winner = 'Computer Wins!'
        elif all(all(cell != '' for cell in row) for row in board):
            winner = 'Draw!'

        if winner:
            cv2.putText(canvas, winner, (offset, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

    cv2.imshow('Tic Tac Toe', canvas)
    cv2.imshow('Webcam', frame)

    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


