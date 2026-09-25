import cv2
import pyautogui
import time
from pathlib import Path
from ultralytics import YOLO

# Load your trained model
#model = YOLO('C:/Users/Perapat.T/Documents/hand_sign_detection/untitled folder/hand_detection_model_training_022/weights/best.pt')
model = YOLO('D:/P/hand_sign_detection/untitled folder/hand_detection_model_training_022/weights/best.pt')
# model_path = Path(__file__).resolve().parent / "hand_detection_model_training_022" / "weights" / "best.pt"
# model = YOLO(model_path)

# Set webcam resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Class-action mapping
gesture_to_action = {
    "Right": "right",
    "Left": "left",
}

# Presentation pause state
is_paused = False
last_action_time = 0
cooldown = 2  # seconds between actions
last_detected = None

print("🖐 Presentation control started! Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=640)[0]
    annotated_frame = results.plot()
    current_time = time.time()

    # Loop through detections
    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        # --- Pause ---
        if class_name == "Stop" and not is_paused and current_time - last_action_time > cooldown:
            pyautogui.press("b")  # PowerPoint black screen = pause
            print("⏸ Paused")
            is_paused = True
            last_action_time = current_time
            last_detected = "Stop"

        # --- Resume ---
        elif class_name == "Thumbs up" and is_paused and current_time - last_action_time > cooldown:
            pyautogui.press("b")
            print("▶️ Resumed")
            is_paused = False
            last_action_time = current_time
            last_detected = "Thumbs up"

        # --- Slide Navigation ---
        elif not is_paused and class_name in gesture_to_action:
            if class_name != last_detected and current_time - last_action_time > cooldown:
                key = gesture_to_action[class_name]
                pyautogui.press(key)
                print(f"➡️ Gesture '{class_name}' → key '{key}'")
                last_action_time = current_time
                last_detected = class_name

    # Show webcam with detection
    cv2.imshow("Hand Sign Control", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("❌ Quit")
        break

cap.release()
cv2.destroyAllWindows()
