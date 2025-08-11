# Tic Tac Toe with Finger Tracking (OpenCV + Mediapipe)

This project is an interactive **Tic Tac Toe** game that uses **computer vision** and **hand tracking** to allow the player to interact without a mouse or keyboard.  
The user moves their **index finger** in front of a webcam to control a cursor, select **X or O**, and play against a simple AI opponent.  

The background is **solid white** for easy visibility.

---

## Features

- **Finger tracking** via [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)
- **Cursor** that follows your index finger
- **Hover-based selection** for both:
  - Choosing your symbol (**X** or **O**)
  - Choosing a cell on the Tic Tac Toe board
- **Simple AI opponent** that plays randomly in empty cells
- **White background** for better contrast
- **No clicking required** — selections are made by holding your finger over an option for ~0.5 seconds

---

## Requirements

Install Python 3.9+ and the following dependencies:

pip install opencv-python mediapipe numpy

---

## How to run

Connect a webcam to your computer.

Run:
- python game_option.py
- The game will open in a new window:
- First, hover your finger over X or O to choose your symbol.
- The game starts immediately after your selection.
- Move your index finger to hover over an empty cell to place your mark.
- The computer will automatically make its move.
- Close the game by pressing the q key.

## File Structure

- ├── game_option.py   # Main game script
- ├── README.md        # This file

## How It Works
- MediaPipe Hands detects hand landmarks in real time.
- The script finds the position of the index fingertip (landmark[8]).
- The fingertip coordinates are mapped to screen coordinates and used as a virtual cursor.
- Hover detection is implemented using a timer — if the cursor stays over a target for more than 0.5 seconds, it’s considered a selection.
- The computer picks a random available cell for its move.

## Possible Extensions
- Add score tracking for multiple rounds.
- Improve AI to use a minimax algorithm instead of random moves.
- Add sound effects when placing a piece.
- Support two-player mode over a network.
- Allow choosing board size (3x3, 4x4, etc.).
