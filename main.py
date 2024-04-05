import cv2
import mediapipe as mp

def thumb_uper(hand_landmarks):
    # Define the landmarks for the thumb
    thumb_tip = 4
    thumb_mcp = 2

    # Check if the y-coordinate of the thumb tip is above the y-coordinate of the thumb MCP
    return hand_landmarks.landmark[thumb_tip].y < hand_landmarks.landmark[thumb_mcp].y

def thumb_niche(hand_landmarks):
    # Define the landmarks for the thumb
    thumb_tip = 4
    thumb_mcp = 2

    # Check if the y-coordinate of the thumb tip is below the y-coordinate of the thumb MCP
    return hand_landmarks.landmark[thumb_tip].y > hand_landmarks.landmark[thumb_mcp].y

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)  # Adjust confidence thresholds
prev_hand_landmarks = None
waving_counter = 0

while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if prev_hand_landmarks is not None:
                # Check if thumbs up
                if thumb_uper(hand_landmarks):
                    cv2.putText(frame, "Thumbs Up", (50, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Check if thumbs down
                elif thumb_niche(hand_landmarks):
                    cv2.putText(frame, "Thumbs Down", (50, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Get the y-coordinate of the middle finger (landmark 9)
                curr_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
                prev_y = prev_hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

                # Check for waving
                if abs(curr_y - prev_y) > 0.005:
                    waving_counter += 1
                else:
                    waving_counter = 0

                if waving_counter > 1:
                    cv2.putText(frame, "Waving", (50, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Store current hand landmarks for the next frame
            prev_hand_landmarks = hand_landmarks

            # Draw hand landmarks on the frame
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("VISPHOT", frame)

    # Break the loop if 'e' is pressed
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

    if waving_counter > 1:
        waving_counter = 0

cap.release()
cv2.destroyAllWindows()
