import cv2
import mediapipe as mp

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify the camera index

# Initialize variables
results = None
prev_hand_landmarks = None

while True:
    ret, frame = cap.read()
    
    # Assuming 'results' is obtained from some processing step
    # For demonstration purposes, initializing 'results' as None
    if results is not None and results.multi_hand_landmarks:
        if prev_hand_landmarks is not None:
            if thumb_uper(hand_landmarks):
                cv2.putText(frame, "Thumbs Up", (50, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
            elif thumb_niche(hand_landmarks):
                cv2.putText(frame, "Thumbs Down", (50, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            if abs(curr_y - prev_y) > 0.005:
                waving_counter += 1
            else:
                if waving_counter > 1:
                    cv2.putText(frame, "Waving", (50, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            prev_hand_landmarks = hand_landmarks