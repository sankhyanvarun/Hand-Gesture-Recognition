import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math

# Initialize mediapipe hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SMOOTHING = 7  # Smoothing factor to reduce jitter in cursor movement

# Functionality options
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

# Helper Functions
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to map hand gestures to functionality
def handle_functionality(gesture, functionality):
    if functionality == "volume_up":
        pyautogui.press('volumeup')
    elif functionality == "volume_down":
        pyautogui.press('volumedown')
    elif functionality == "zoom_in":
        pyautogui.hotkey('ctrl', '+')
    elif functionality == "zoom_out":
        pyautogui.hotkey('ctrl', '-')
    elif functionality == "brightness_up":
        pyautogui.hotkey('win', 'shift', 'a')  # Custom brightness shortcut
    elif functionality == "brightness_down":
        pyautogui.hotkey('win', 'shift', 'b')  # Custom brightness shortcut
    elif functionality == "scroll_up":
        pyautogui.scroll(500)
    elif functionality == "scroll_down":
        pyautogui.scroll(-500)
    elif functionality == "media_play_pause":
        pyautogui.press('playpause')
    elif functionality == "next_track":
        pyautogui.press('nexttrack')
    elif functionality == "prev_track":
        pyautogui.press('prevtrack')
    elif functionality == "open_virtual_keyboard":
        pyautogui.hotkey('win', 'ctrl', 'o')

# Detect and map gestures
def detect_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    
    # Victory Sign (Volume Up)
    if (index_finger_tip.y < middle_finger_tip.y < ring_finger_tip.y < pinky_tip.y):
        return "Victory Sign"
    
    # Index Finger Up (Volume Down)
    elif (index_finger_tip.y < wrist.y and middle_finger_tip.y > wrist.y and
          ring_finger_tip.y > wrist.y and pinky_tip.y > wrist.y):
        return "Index Finger Up"
    
    # Thumbs Up (Zoom In)
    elif thumb_tip.y < wrist.y and index_finger_tip.y > wrist.y:
        return "Thumbs Up"
    
    # Thumbs Down (Zoom Out)
    elif thumb_tip.y > wrist.y and index_finger_tip.y < wrist.y:
        return "Thumbs Down"
    
    # Five Fingers Open (Brightness Up)
    elif (thumb_tip.y < wrist.y and index_finger_tip.y < wrist.y and
          middle_finger_tip.y < wrist.y and ring_finger_tip.y < wrist.y and pinky_tip.y < wrist.y):
        return "Five Fingers Open"
    
    # Four Fingers Open (Brightness Down)
    elif (thumb_tip.y > wrist.y and index_finger_tip.y < wrist.y and
          middle_finger_tip.y < wrist.y and ring_finger_tip.y < wrist.y and pinky_tip.y < wrist.y):
        return "Four Fingers Open"
    
    # Three Finger Swipe (Open Virtual Keyboard)
    elif (index_finger_tip.y < wrist.y and middle_finger_tip.y < wrist.y and ring_finger_tip.y < wrist.y and pinky_tip.y > wrist.y):
        return "Three Finger Swipe"

    return None

# Function to control based on gestures
def process_hand_movement(frame, hand_landmarks, handedness_label):
    if hand_landmarks:
        # If right hand, control cursor
        if handedness_label == "Right":
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Move cursor
            cursor_x = int(index_finger_tip.x * SCREEN_WIDTH)
            cursor_y = int(index_finger_tip.y * SCREEN_HEIGHT)
            pyautogui.moveTo(cursor_x, cursor_y)

            # Detect and handle clicks
            handle_click(hand_landmarks)
        
        # If left hand, detect gestures for controlling functionalities
        elif handedness_label == "Left":
            detected_gesture = detect_gesture(hand_landmarks)
            if detected_gesture and detected_gesture in FUNCTIONALITY_MAP.values():
                # Map the detected gesture to functionality and trigger it
                for functionality, gesture in FUNCTIONALITY_MAP.items():
                    if gesture == detected_gesture:
                        handle_functionality(gesture, functionality)
                        break

# Handle click for right hand
def handle_click(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = calculate_distance(thumb_tip.x, thumb_tip.y, index_finger_tip.x, index_finger_tip.y)

    if distance < 0.02:
        pyautogui.click()

# Main function
def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for mirrored effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB for mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Process hand landmarks if detected
        if result.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                handedness_label = handedness.classification[0].label
                process_hand_movement(frame, hand_landmarks, handedness_label)

        # Show the frame
        cv2.imshow('Hand Gesture Control', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
