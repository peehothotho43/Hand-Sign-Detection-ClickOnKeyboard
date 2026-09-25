import cv2

# ทดสอบเปิดกล้อง
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not opened!")
else:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Test Frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    cap.release()
