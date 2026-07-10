import streamlit as st
import pandas as pd
import numpy as np
import imageio.v3 as iio # ใช้ตัวนี้แทน cv2 เพื่อตัดปัญหา Error
import mediapipe as mp
import datetime
import os

# ตั้งค่า MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

st.set_page_config(page_title="Knee AI - Smart Scan", layout="wide")
st.title("🤖 Knee AI: ระบบวิเคราะห์เข่าอัจฉริยะ")

# ฟังก์ชันคำนวณมุม
def calculate_angle(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0: angle = 360 - angle
    return angle

# จัดการข้อมูลคนไข้
DB_FILE = "patient_data.csv"
if os.path.exists(DB_FILE): 
    df = pd.read_csv(DB_FILE)
else: 
    df = pd.DataFrame(columns=["id", "date", "angle"])

# ส่วนล็อกอินและทำงานหลัก
uid = st.sidebar.text_input("🔑 รหัสประจำตัวคนไข้ (4 หลัก):")

if uid:
    st.header("📸 วิเคราะห์องศาเข่าด้วย AI")
    uploaded_file = st.file_uploader("อัปโหลดรูปขา (เห็นสะโพก-เข่า-ข้อเท้า):", type=["jpg", "png"])
    
    if uploaded_file:
        # ใช้ imageio อ่านภาพแทนเพื่อความเสถียรบนระบบ Cloud
        image = iio.imread(uploaded_file)
        results = pose.process(image)
        
        if results.pose_landmarks:
            lms = results.pose_landmarks.landmark
            hip = [lms[23].x, lms[23].y]
            knee = [lms[25].x, lms[25].y]
            ankle = [lms[27].x, lms[27].y]
            
            angle = calculate_angle(hip, knee, ankle)
            st.image(image, caption="AI ตรวจพบจุดข้อต่อเรียบร้อย", use_container_width=True)
            st.metric("องศาเข่าที่วิเคราะห์ได้", f"{round(angle, 2)}°")
            
            if st.button("บันทึกผลการวิเคราะห์"):
                new_data = pd.DataFrame([{"id": uid, "date": str(datetime.date.today()), "angle": round(angle, 2)}])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success("บันทึกข้อมูลเรียบร้อย!")
        else:
            st.error("AI หาข้อต่อไม่เจอ! กรุณาถ่ายรูปให้เห็นเต็มตัวตั้งแต่สะโพกถึงข้อเท้านะคะ")

    st.header("📈 ประวัติการวิเคราะห์")
    user_hist = df[df['id'] == uid]
    if not user_hist.empty:
        st.line_chart(user_hist.set_index('date')['angle'])
else:
    st.info("👈 กรุณากรอกรหัสประจำตัวที่แถบด้านซ้ายเพื่อเริ่มระบบค่ะ")
