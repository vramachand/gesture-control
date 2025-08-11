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

## Tic Tac Toe Game
- Features
  - Hover over X or O to choose your symbol.
  - White background for high visibility.
  - Cursor follows your index fingertip.
  - AI opponent plays randomly in empty cells.
  - No clicking — hover over a target for ~0.5 seconds to select.

- How to Run
  - python game_white2.py
- Gameplay Flow:
  - Hover over X or O to pick your symbol.
  - Move your index finger to hover over an empty square.
  - Hold your finger still for ~0.5 seconds to place your mark.
  - The AI makes its move.
  - Press q to exit.

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
- ├── game_white2.py    # Tic Tac Toe with finger tracking
- ├── air_canvas.py     # Air Canvas drawing app
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
