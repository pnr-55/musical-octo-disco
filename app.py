import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

# ตั้งค่า MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# ฟังก์ชันคำนวณมุมจริงจากพิกัด AI
def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0: angle = 360 - angle
    return angle

st.set_page_config(page_title="Knee AI Precision", layout="centered")

# ระบบ Session State เพื่อกันข้อมูลหาย
if 'data' not in st.session_state:
    st.session_state.data = {'name': "", 'angle': None}
if 'page' not in st.session_state: st.session_state.page = "Register"

# --- หน้าที่ 1: ลงทะเบียน ---
if st.session_state.page == "Register":
    st.title("🩺 1. ข้อมูลผู้ป่วย")
    st.session_state.data['name'] = st.text_input("ชื่อ - นามสกุล:")
    if st.button("ถัดไป"):
        st.session_state.page = "Scan"
        st.rerun()

# --- หน้าที่ 2: วิเคราะห์จากภาพจริง ---
elif st.session_state.page == "Scan":
    st.title("📷 2. วิเคราะห์จากภาพจริง")
    file = st.file_uploader("อัปโหลดรูปขาหรือ X-Ray:", type=["jpg", "png"])
    
    if file:
        image_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        img = cv2.imdecode(image_bytes, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = pose.process(img_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            # ดึงพิกัดจริงจากภาพ
            hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            
            st.session_state.data['angle'] = calculate_angle(hip, knee, ankle)
            st.success(f"AI วิเคราะห์มุมเข่าได้: {st.session_state.data['angle']:.2f}°")
            
            if st.button("ดูผลวินิจฉัย"):
                st.session_state.page = "Result"
                st.rerun()
        else:
            st.error("AI หาข้อเข่าไม่พบ กรุณาใช้ภาพที่เห็นตั้งแต่สะโพกถึงข้อเท้าชัดๆ ครับ")

# --- หน้าที่ 3: ผลลัพธ์ ---
elif st.session_state.page == "Result":
    st.title("📊 3. ผลการวินิจฉัย")
    angle = st.session_state.data['angle']
    
    st.metric("มุมเข่าที่วัดได้", f"{angle:.2f}°")
    
    # วิเคราะห์เปรียบเทียบ
    if 170 <= angle <= 175:
        st.success("สภาพเข่าปกติ")
    else:
        status = "ขาโก่ง" if angle < 170 else "ขาฉิ่ง"
        st.error(f"ตรวจพบความผิดปกติ: {status}")
        st.link_button("📍 ค้นหาคลินิกกายภาพใกล้ฉัน", "https://www.google.com/maps/search/คลินิกกายภาพบำบัดใกล้ฉัน")
    
    if st.button("เริ่มใหม่"):
        st.session_state.page = "Register"
        st.rerun()
