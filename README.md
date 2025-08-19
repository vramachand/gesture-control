# AI-Powered Interactive Games & Tools (Finger Tracking)

This repository contains **two projects** designed to teach high school students about **basic AI concepts** using **OpenCV** and **MediaPipe** for computer vision and hand tracking.

---

## Projects Included

1. **Tic Tac Toe with Finger Tracking**  
   Play Tic Tac Toe against a computer by moving your **index finger** in front of a webcam to control a cursor.
   
2. **Air Canvas**  
   Draw on the screen using your finger in mid-air, choosing different colors from an on-screen palette.

---

## Requirements

Install Python 3.9+ and dependencies:
- pip install opencv-python mediapipe numpy
- opencv-python – for webcam input and drawing the board/game UI.
- mediapipe – for hand tracking and gesture recognition.
- numpy – for array operations and image manipulation.
- random – built-in Python library for computer moves.

# Tic Tac Toe

A fun, interactive **Tic Tac Toe game** that uses your **hand gestures** via webcam as the input mechanism.  
Built with **Python, OpenCV, and MediaPipe**, this project lets you play against the computer by simply moving your hand on the screen and making a **fist** to confirm selections.

---

## Features
- **Hand Tracking with MediaPipe Hands** – tracks your hand landmarks in real-time.  
- **Cursor Control** – your hand acts as a "cursor" to hover over selections.  
- **Fist Gesture Confirmation** – instead of accidental hover, making a **fist locks in your choice**.  
- **Play Against the Computer** – basic AI chooses random available spots.  
- **Graphical Board Rendering** – Tic Tac Toe board and selections drawn with OpenCV.  
- **Restart Option** – when the game ends, select *Play Again* by hovering and making a fist.  

---

## Dependencies

Make sure you have **Python 3.8+** installed. Install the required libraries with... pip install opencv-python mediapipe numpy

## Gameplay Instructions
- Symbol Selection Screen
-    Hover your hand over the X or O box.
-    Make a fist to confirm your choice.
- Playing the Game
-    Hover your hand over a square on the Tic Tac Toe board.
-    Make a fist to place your symbol (X or O).
-    The computer will then make its move.
- Winning / Draw Conditions
-    The game checks for win/draw conditions after every move.
- Restarting the Game
-    After a game ends, a green Play Again box appears.
-    Hover your hand over it and make a fist to restart.
- Exiting the Game
-    Press ESC or Q on your keyboard at any time to quit.

## Design & Development Decisions
- Gesture Detection
-    A fist gesture was chosen for confirmation since hover-only controls caused accidental selections.
-    Fist detection works by checking if 3+ fingers are folded (tip landmark below PIP landmark).
- Cursor Control
-    The average of hand landmarks was used to position the cursor.
-    Cursor coordinates are scaled to match the game canvas.
- Symbol Selection
-    On startup, the player chooses X or O.
-    Selection requires a fist gesture, preventing misclicks.
- Game Logic
-    The board is a 3x3 list of lists.
-    After every move:
-    It checks if the user has won.
-    If not, the computer makes a random move.
-    Win conditions are checked for rows, columns, and diagonals.

## UI & Layout
- The game board and text are drawn using OpenCV primitives (cv2.line, cv2.circle, cv2.putText).
- The board is centered within a canvas instead of directly overlaying on the webcam feed for clarity.
- Endgame screen displays results (You Win!, Computer Wins!, or Draw!) and restart option.

## Possible Improvements
- Smarter computer AI (e.g., Minimax algorithm instead of random moves).
- Support for two players (gesture-vs-gesture).
- Multi-gesture controls (e.g., ✌️ for undo, ✊ for confirm).
- Integration with sound effects for moves and wins.
- Adjustable difficulty levels.

## Air Canvas
- Features
  - Real-time hand tracking using MediaPipe.
  - Draw in the air with your index finger.
  - On-screen color palette for choosing drawing colors.
  - No clicking — color changes by hovering over the palette.

- How to Run
  - python air_canvas.py
- Usage:
  - Keep your index finger extended to draw.
  - Make a fist to stop drawing.
  - Hover your finger over a color in the palette to switch colors.
  - Draw in mid-air — the strokes will appear on the screen.
  - Press q to exit.

## File Structure
- ├── game_play2.py     # Final Functioning Tic Tac Toe with finger tracking
- ├── color_canvas.py     # Air Canvas drawing game
- ├── README.md         # This file

## How It Works
- Both programs use:
- MediaPipe Hands for detecting hand landmarks.
- OpenCV to process video frames and render interactive elements.
- Index fingertip coordinates to control a cursor.
- Hover-based interaction — no mouse or keyboard required.

## Educational Value
- These projects help students:
- Learn how AI-powered hand tracking works.
- Understand real-time video processing.
- See practical uses of computer vision in games and tools.
