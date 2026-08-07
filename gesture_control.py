
print("Hand Gesture Starting...")

##next try for pynput
import cv2 
import mediapipe as mp
from pynput.keyboard import Key, Controller

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hand_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# Initialize keyboard controller
keyboard = Controller()

# Keys to control
KEY_RIGHT = Key.right
KEY_LEFT = Key.left


print("Started Successfully\n")
print("SHOW FULL HAND TO PRESS RIGHT KEY AND FIST FOR LEFT KEY CONTROL")

print("To stop running press 'q' or close the camera window\n")

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand_detector.process(rgb_frame)

        state = "No Hand"

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect hand open or fist
            finger_tips = [8, 12, 16, 20]
            finger_pips = [6, 10, 14, 18]
            count_open = 0

            h, w, _ = frame.shape
            for tip, pip in zip(finger_tips, finger_pips):
                tip_y = hand_landmarks.landmark[tip].y * h
                pip_y = hand_landmarks.landmark[pip].y * h
                if tip_y < pip_y:
                    count_open += 1

            if count_open >= 4:
                state = "Hand Open"
            elif count_open == 0:
                state = "Fist"
            else:
                state = "Partial"

            # Draw state
            color = (0, 255, 0) if state=="Hand Open" else (0,0,255) if state=="Fist" else (255,0,0)
            cv2.putText(frame, state, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            print(state)

            # Tap keys each frame for reliable game input
            try:
                if state == "Hand Open":
                    keyboard.release(KEY_LEFT)
                    keyboard.press(KEY_RIGHT)
                    # keyboard.release(KEY_RIGHT)
                elif state == "Fist":
                    keyboard.release(KEY_RIGHT)
                    keyboard.press(KEY_LEFT)
                    # keyboard.release(KEY_LEFT)
                else:
                    keyboard.release(KEY_LEFT)
                    keyboard.release(KEY_RIGHT)
            except Exception as e:
                keyboard.release(KEY_LEFT)
                keyboard.release(KEY_RIGHT)
                print(f"Keyboard action error: {e}")
                
        else:
            state="No Hand"
            try:
                keyboard.release(KEY_LEFT)
                keyboard.release(KEY_RIGHT)
            except:
                pass

        # Show webcam
        cv2.imshow("Hand Detection", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty("Hand Detection", cv2.WND_PROP_VISIBLE) < 1:
            break

except Exception as e:
    print(f"Fatal error: {e}")

finally:
    if 'cap' in locals() and cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    print("Program exited safely.")
