# Hand Gesture Control System

This project implements a **Hand Gesture Control System** using a webcam and OpenCV for real-time gesture recognition. It uses MediaPipe to detect hand landmarks and supports a wide range of customizable gestures to perform actions such as controlling volume, zooming in/out, adjusting brightness, scrolling, media controls, and more. 

## Features

- **Cursor Control**: Control the mouse pointer using the right hand.
- **Clicking**: Perform a mouse click when the thumb and index finger come close to each other.
- **Volume Control**:
  - Left-hand victory sign gesture increases the system volume.
  - Left-hand index finger up gesture decreases the system volume.
- **Zoom In/Out**:
  - Thumbs up gesture zooms in.
  - Thumbs down gesture zooms out.
- **Brightness Control**:
  - Five fingers open to increase brightness.
  - Four fingers open to decrease brightness.
- **Scrolling**: Custom gestures can be added for scrolling up and down.
- **Media Controls**:
  - Custom gestures to control media (play/pause, next, previous track).
- **Virtual Keyboard Input**: Open the virtual keyboard using a three-finger swipe gesture.

## Customization

The project allows users to **customize gestures** to perform different functionalities. You can easily remap gestures to desired actions by modifying the `FUNCTIONALITY_MAP` dictionary in the code.

### Available Functionality Options
- Volume Up/Down
- Zoom In/Out
- Brightness Up/Down
- Scroll Up/Down
- Media Controls (Play/Pause, Next/Previous Track)
- Open Virtual Keyboard

## Setup Instructions

### Prerequisites

- Python 3.x
- Required libraries: OpenCV, MediaPipe, pyautogui, numpy

Install the required dependencies using the following command:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

### Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hand-gesture-control.git
   ```
2. Navigate to the project directory:
   ```bash
   cd hand-gesture-control
   ```
3. Run the script:
   ```bash
   python hand_gesture_control.py
   ```
4. A webcam window will appear, and you can start using gestures to control your system.

### Gesture Mappings

By default, the following gestures are mapped to system functionalities:

| Gesture                | Functionality           |
|------------------------|-------------------------|
| Victory Sign (Left Hand)| Volume Up               |
| Index Finger Up (Left)  | Volume Down             |
| Thumbs Up (Left Hand)   | Zoom In                 |
| Thumbs Down (Left Hand) | Zoom Out                |
| Five Fingers Open (Left)| Increase Brightness     |
| Four Fingers Open (Left)| Decrease Brightness     |
| Three-Finger Swipe (Left) | Open Virtual Keyboard |
| Right Hand Index Finger | Mouse Cursor Control    |
| Thumb + Index Together  | Mouse Click             |

You can modify these gestures and assign new actions in the `FUNCTIONALITY_MAP` dictionary in the script.

## How it Works

The system utilizes **MediaPipe** for real-time hand tracking and landmark detection. Each hand gesture corresponds to certain landmark positions, and these positions are compared to predefined conditions (e.g., victory sign, thumbs up) to trigger system actions like controlling volume or performing mouse clicks.

- **Hand Detection**: The `mediapipe` library detects hand landmarks (key points) in real time using the webcam.
- **Gesture Recognition**: Hand landmarks are analyzed to detect specific gestures like thumbs up or victory sign.
- **System Control**: Based on the detected gestures, corresponding system actions (e.g., volume control, cursor movement) are triggered using `pyautogui`.

## Customization Instructions

To add or modify the gestures, edit the following part of the code:

```python
FUNCTIONALITY_MAP = {
    "volume_up": "Victory Sign",
    "volume_down": "Index Finger Up",
    "zoom_in": "Thumbs Up",
    "zoom_out": "Thumbs Down",
    "brightness_up": "Five Fingers Open",
    "brightness_down": "Four Fingers Open",
    "scroll_up": "Scroll Up Gesture",
    "scroll_down": "Scroll Down Gesture",
    "media_play_pause": "Play/Pause Gesture",
    "next_track": "Next Track Gesture",
    "prev_track": "Previous Track Gesture",
    "open_virtual_keyboard": "Three Finger Swipe",
}
```

You can replace the gesture names with your own custom gestures, or create new gestures in the `detect_gesture()` function.

## Future Improvements

- Add more gestures for additional controls like window minimization, maximizing, and custom hotkeys.
- Improve gesture recognition accuracy for more complex gestures.
- Implement gesture-based multi-tasking controls like three-finger swipe for switching windows.

## Contributions

Feel free to open issues, suggest improvements, or submit pull requests to improve the project.

## Acknowledgments

- **MediaPipe**: For the real-time hand tracking API.
- **OpenCV**: For image processing.
- **pyautogui**: For system control via Python.

