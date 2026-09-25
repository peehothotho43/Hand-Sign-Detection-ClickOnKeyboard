import cv2
import os
import time

# พารามิเตอร์
save_dir = "Down"
interval_sec = 2  # ถ่ายทุก 2 วินาที
max_images = 100  # จำนวนภาพสูงสุดที่ต้องการเก็บ

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(save_dir, exist_ok=True)

# เปิดกล้อง
cap = cv2.VideoCapture(0)  # 0 = กล้องหลัก

if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

img_count = 0

print("เริ่มถ่ายภาพ กด 'q' เพื่อหยุด")

while img_count < max_images:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถอ่านภาพจากกล้องได้")
        break

    # แสดงภาพ
    cv2.imshow("Camera", frame)

    # บันทึกภาพ
    filename = f"image_{img_count:03}.jpg"
    filepath = os.path.join(save_dir, filename)
    cv2.imwrite(filepath, frame)
    print(f"บันทึกภาพ {filename}")

    img_count += 1

    # รอ interval
    if cv2.waitKey(int(interval_sec * 1000)) & 0xFF == ord('q'):
        break

# ปิดกล้อง
cap.release()
cv2.destroyAllWindows()
print("สิ้นสุดการถ่ายภาพ")
