import cv2
import mediapipe as mp
import numpy as np

# ตั้งค่า MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calculate_angle(a, b, c):
    """คำนวณมุมระหว่าง 3 จุด (สะโพก-เข่า-ข้อเท้า)"""
    a = np.array(a) # สะโพก
    b = np.array(b) # เข่า
    c = np.array(c) # ข้อเท้า
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
    return angle

# อ่านภาพ
image = cv2.imread('your_leg_photo.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pose.process(image_rgb)

if results.pose_landmarks:
    landmarks = results.pose_landmarks.landmark
    
    # ดึงพิกัด (ตัวอย่างขาขวา)
    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    
    angle = calculate_angle(hip, knee, ankle)
    
    # วิเคราะห์เบื้องต้น
    print(f"องศาเข่าที่วัดได้: {angle:.2f} องศา")
    if angle < 165: # ค่าสมมติสำหรับการทดลอง
        print("คำแนะนำ: พบลักษณะขาโก่ง ควรปรึกษาแพทย์เฉพาะทาง")
    else:
        print("ลักษณะขาอยู่ในเกณฑ์ปกติ")
