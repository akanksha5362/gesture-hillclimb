import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open camera.")
    exit()

print("\nTwo-Hand Detection Test")
print("-----------------------")
print("Show both hands to the camera.")
print("Press Q to quit.\n")


while True:
    success, frame = cap.read()

    if not success:
        print("Failed to read camera frame.")
        break

    # Mirror the camera view
    frame = cv2.flip(frame, 1)

    # MediaPipe expects RGB images
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    hand_count = 0

    if result.multi_hand_landmarks:

        hand_count = len(result.multi_hand_landmarks)

        for i, hand in enumerate(result.multi_hand_landmarks):

            # Draw hand skeleton
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            wrist = hand.landmark[
                mp_hands.HandLandmark.WRIST
            ]

            index_tip = hand.landmark[
                mp_hands.HandLandmark.INDEX_FINGER_TIP
            ]

            # Identify the hand
            handedness = result.multi_handedness[i]
            label = handedness.classification[0].label
            confidence = handedness.classification[0].score

            h, w = frame.shape[:2]

            wrist_x = int(wrist.x * w)
            wrist_y = int(wrist.y * h)

            # Hand label
            cv2.putText(
                frame,
                f"{label} ({confidence:.2f})",
                (wrist_x - 50, wrist_y - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # Index finger X position
            cv2.putText(
                frame,
                f"Index X: {index_tip.x:.2f}",
                (wrist_x - 50, wrist_y + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

            print(
                f"Hand {i + 1}: {label} | "
                f"confidence={confidence:.2f} | "
                f"index_x={index_tip.x:.2f}"
            )

    else:
        print("No hands detected")

    # Display the number of detected hands
    cv2.putText(
        frame,
        f"Hands detected: {hand_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.imshow("Two Hand Detection Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
hands.close()