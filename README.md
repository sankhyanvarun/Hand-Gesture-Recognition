# Hand Gesture Control System

This project implements a hand gesture control system that allows users to control the computer using hand movements. The system recognizes gestures from both hands to perform different functions:

- **Right Hand**: Controls cursor movement and clicking.
- **Left Hand**: Manages window actions such as minimizing and maximizing.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Features

- Real-time hand gesture recognition using MediaPipe.
- Cursor movement controlled by the right hand with adjustable sensitivity.
- Left-hand gestures for window management (minimize/maximize).
- Easy to set up and run.

## Requirements

- Python 3.6 or higher
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/hand-gesture-control.git
   cd hand-gesture-control
Install required packages: You can use pip to install the necessary libraries. It's recommended to use a virtual environment.
bash
Copy code
pip install opencv-python mediapipe pyautogui numpy
Usage
Run the script:

bash
Copy code
python cursor_control_hand.py
Hand Gestures:

Right Hand:
Move the cursor using your index finger.
Pinch the thumb and index finger together to perform a left-click.
Left Hand:
Open hand (all fingers extended) to maximize the current window.
Close hand (fist) to minimize the current window.
Stop the program:

Press q to exit the video feed.
How It Works
The system uses the MediaPipe library to detect and track hand landmarks in real-time through your webcam. The coordinates of the hand landmarks are used to determine the position of the cursor and to detect gestures for clicking and window management.

Right Hand:

The index finger controls the cursor's position, amplified by a scaling factor to ensure smoother movement.
The left-click action is triggered when the thumb and index finger come close to each other.
Left Hand:

The program recognizes the hand's posture to perform window actions: maximizing the window when the hand is open and minimizing it when closed.
Contributing
Contributions are welcome! If you have suggestions for improvements or want to report bugs, please open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for more information.
