import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Disable PyAutoGUI failsafe feature
pyautogui.FAILSAFE = False

# Set up the screen size and scaling factor for cursor movement
screen_width, screen_height = pyautogui.size()
scaling_factor = 2.5  # Adjust this to move the cursor further with smaller hand movements

# Helper function to calculate distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Process hand gestures for right-hand actions (cursor control, clicking)
def process_right_hand(frame, hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

    # Cursor control: Move the cursor based on the index finger tip position (amplified movement)
    index_finger_x = int(index_finger_tip.x * screen_width * scaling_factor)
    index_finger_y = int(index_finger_tip.y * screen_height * scaling_factor)

    # Move the cursor with the scaled position
    pyautogui.moveTo(index_finger_x, index_finger_y)

    # Clicking action: If the thumb and index finger are close, perform a left-click
    distance_thumb_index = calculate_distance(
        index_finger_tip.x, index_finger_tip.y,
        thumb_tip.x, thumb_tip.y
    )
    if distance_thumb_index < 0.05:  # Adjust the threshold for the click gesture
        pyautogui.click()  # Left-click action

# Process hand gestures for left-hand actions (window management)
def process_left_hand(frame, hand_landmarks):
    global last_action_time

    # Get relevant hand landmarks
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    # Gesture detection: Open Hand (all fingers extended) -> Maximize window
    if (index_finger_tip.y < index_finger_mcp.y and
        middle_finger_tip.y < middle_finger_mcp.y and
        ring_finger_tip.y < ring_finger_mcp.y and
        pinky_finger_tip.y < pinky_finger_mcp.y and
        thumb_tip.y < wrist.y):
        
        # Prevent multiple actions in a short time span
        if time.time() - last_action_time > 2:
            pyautogui.hotkey('win', 'up')  # Maximize window
            last_action_time = time.time()

    # Gesture detection: Closed Hand (fist) -> Minimize window
    elif (index_finger_tip.y > index_finger_mcp.y and
          middle_finger_tip.y > middle_finger_mcp.y and
          ring_finger_tip.y > ring_finger_mcp.y and
          pinky_finger_tip.y > pinky_finger_mcp.y):
        
        if time.time() - last_action_time > 2:
            pyautogui.hotkey('win', 'down')  # Minimize window
            last_action_time = time.time()

# Main function to capture video feed and process hand movements
def main():
    global last_action_time
    last_action_time = 0  # To track last gesture time and avoid rapid window actions
    
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to RGB for Mediapipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hand landmarks
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Right hand for cursor control and clicking
                if handedness.classification[0].label == 'Right':
                    process_right_hand(frame, hand_landmarks)

                # Left hand for window management (minimize/maximize)
                elif handedness.classification[0].label == 'Left':
                    process_left_hand(frame, hand_landmarks)

        # Display the video feed with hand tracking
        cv2.imshow('Hand Gesture Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
