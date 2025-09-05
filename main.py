import cv2
import mediapipe as mp
import pyautogui
import time
import os

# -----------------------
# Paths
# -----------------------
overlay_image_path = os.path.join("assets", "Gesture Control Overlay.png")
overlay_img = cv2.imread(overlay_image_path)

if overlay_img is None:
    raise FileNotFoundError(f"Can't find overlay image at {overlay_image_path}")

overlay_img = cv2.resize(overlay_img, (1280, 720))

# -----------------------
# Mediapipe setup
# -----------------------
mp_draw = mp.solutions.drawing_utils
mp_hands_module = mp.solutions.hands
hand_tracker = mp_hands_module.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------
# Improved Finger Counting
# -----------------------
def count_fingers(hand_landmarks, hand_label="Right"):
    fingers = []

    # Thumb
    if hand_label == "Right":
        fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)
    else:  # Left hand
        fingers.append(1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0)

    # Other fingers: Index, Middle, Ring, Pinky
    for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0)

    return sum(fingers)

# -----------------------
# Main function
# -----------------------
def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)

    prev_finger_count = -1
    gesture_start = False
    last_action_time = 0
    confirmation_msg = ""

    # Webcam box
    cam_x1, cam_y1, cam_x2, cam_y2 = 50, 150, 950, 650
    # Confirmation box
    confirm_box_x1, confirm_box_y1, confirm_box_x2, confirm_box_y2 = 980, 150, 1250, 260

    while True:
        current_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror feed

        results = hand_tracker.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            hand_label = results.multi_handedness[0].classification[0].label if results.multi_handedness else "Right"

            finger_count = count_fingers(hand_landmarks, hand_label)

            if finger_count != prev_finger_count:
                if not gesture_start:
                    gesture_start_time = time.time()
                    gesture_start = True
                elif (current_time - gesture_start_time) > 0.5:
                    # Media controls
                    if finger_count == 1:
                        pyautogui.press("volumeup")
                        confirmation_msg = "Volume Up"
                    elif finger_count == 2:
                        pyautogui.press("volumedown")
                        confirmation_msg = "Volume Down"
                    elif finger_count == 3:
                        pyautogui.press("nexttrack")
                        confirmation_msg = "Next Track"
                    elif finger_count == 4:
                        pyautogui.press("prevtrack")
                        confirmation_msg = "Previous Track"
                    elif finger_count == 5:
                        pyautogui.press("playpause")
                        confirmation_msg = "Play / Pause"

                    prev_finger_count = finger_count
                    gesture_start = False
                    last_action_time = time.time()

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands_module.HAND_CONNECTIONS)

        # Overlay webcam feed
        overlay_copy = overlay_img.copy()
        resized_frame = cv2.resize(frame, (cam_x2 - cam_x1, cam_y2 - cam_y1))
        overlay_copy[cam_y1:cam_y2, cam_x1:cam_x2] = resized_frame

        # Draw confirmation text
        if confirmation_msg and (time.time() - last_action_time) < 3:
            font_style = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            (text_width, text_height), baseline = cv2.getTextSize(confirmation_msg, font_style, font_scale, thickness)
            text_x = confirm_box_x1 + (confirm_box_x2 - confirm_box_x1 - text_width) // 2
            text_y = confirm_box_y1 + (confirm_box_y2 - confirm_box_y1 + text_height) // 2 - baseline
            cv2.putText(overlay_copy, confirmation_msg, (text_x, text_y),
                        font_style, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

        cv2.imshow("Gesture Media Controller", overlay_copy)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# -----------------------
# Entry point
# -----------------------
if __name__ == "__main__":
    main()
