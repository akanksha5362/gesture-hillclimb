import cv2
import mediapipe as mp
import subprocess
import time
from collections import deque


# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


# Camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open camera.")
    exit()


# Steering settings
LEFT_THRESHOLD = 0.56
RIGHT_THRESHOLD = 0.64

x_history = deque(maxlen=5)
STEERING_INTERVAL = 0.30
last_steering_time = 0


# Pedal touch coordinates
BRAKE_X, BRAKE_Y = 50, 900
ACCELERATOR_X, ACCELERATOR_Y = 400, 900


def run_adb_swipe(x1, y1, x2, y2, duration):
    """Send a touch/swipe command to the Android device."""
    subprocess.run(
        [
            "adb", "shell", "input", "swipe",
            str(x1), str(y1),
            str(x2), str(y2),
            str(duration)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def steer_left():
    run_adb_swipe(1750, 850, 2050, 850, 250)


def steer_right():
    run_adb_swipe(2050, 850, 1750, 850, 250)


def press_brake():
    run_adb_swipe(BRAKE_X, BRAKE_Y, BRAKE_X, BRAKE_Y, 1000)


def press_accelerator():
    run_adb_swipe(
        ACCELERATOR_X,
        ACCELERATOR_Y,
        ACCELERATOR_X,
        ACCELERATOR_Y,
        1000
    )


def finger_is_extended(hand, tip, pip):
    """Check whether a finger is extended."""
    return hand.landmark[tip].y < hand.landmark[pip].y


def get_pedal_gesture(hand):
    """Detect whether the left hand is a fist or an open palm."""

    fingers = [
        (
            mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.INDEX_FINGER_PIP
        ),
        (
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_PIP
        ),
        (
            mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.RING_FINGER_PIP
        ),
        (
            mp_hands.HandLandmark.PINKY_TIP,
            mp_hands.HandLandmark.PINKY_PIP
        )
    ]

    extended = sum(
        finger_is_extended(hand, tip, pip)
        for tip, pip in fingers
    )

    if extended >= 3:
        return "ACCELERATOR"

    if extended <= 1:
        return "BRAKE"

    return "NONE"


print("\nTwo-Hand Gesture Controller")
print("---------------------------")
print("Right hand : index finger controls steering")
print("Left hand  : open palm = accelerator")
print("             fist      = brake")
print("Press Q to quit.\n")


while True:
    success, frame = cap.read()

    if not success:
        print("Failed to read camera frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    steering = "NO HAND"
    pedal = "NO HAND"
    current_time = time.time()

    if result.multi_hand_landmarks:

        for i, hand in enumerate(result.multi_hand_landmarks):

            label = result.multi_handedness[i].classification[0].label

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            # Right hand: steering
            if label == "Right":

                index_tip = hand.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]

                x_history.append(index_tip.x)
                smooth_x = sum(x_history) / len(x_history)

                if smooth_x < LEFT_THRESHOLD:
                    steering = "LEFT"

                elif smooth_x > RIGHT_THRESHOLD:
                    steering = "RIGHT"

                else:
                    steering = "CENTER"

                if current_time - last_steering_time >= STEERING_INTERVAL:

                    if steering == "LEFT":
                        steer_left()
                        last_steering_time = current_time

                    elif steering == "RIGHT":
                        steer_right()
                        last_steering_time = current_time

                # Show fingertip position
                h, w = frame.shape[:2]
                point = (
                    int(index_tip.x * w),
                    int(index_tip.y * h)
                )

                cv2.circle(
                    frame,
                    point,
                    10,
                    (0, 0, 255),
                    -1
                )

            # Left hand: accelerator/brake
            elif label == "Left":

                pedal = get_pedal_gesture(hand)

                if pedal == "ACCELERATOR":
                    press_accelerator()

                elif pedal == "BRAKE":
                    press_brake()

                wrist = hand.landmark[
                    mp_hands.HandLandmark.WRIST
                ]

                h, w = frame.shape[:2]

                cv2.putText(
                    frame,
                    pedal,
                    (
                        int(wrist.x * w) - 70,
                        int(wrist.y * h) - 30
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 255, 255),
                    2
                )

    else:
        x_history.clear()

    # Status display
    cv2.putText(
        frame,
        f"Steering: {steering}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Pedal: {pedal}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 0),
        2
    )

    cv2.imshow("Dr Driving Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
hands.close()

print("Controller stopped.")