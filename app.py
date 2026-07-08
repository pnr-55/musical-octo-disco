import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import pandas as pd

st.set_page_config(page_title="Knee AI Telemedicine", layout="centered")

# กำหนด Session State
if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'analysis_result' not in st.session_state: st.session_state.analysis_result = None

# ฟังก์ชันคำนวณมุม
def calculate_angle(a, b, c):
a = np.array(a)
b = np.array(b)
c = np.array(c)
r = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
angle = np.abs(r * 180.0 / np.pi)
if angle > 180.0: angle = 360 - angle
return int(angle)

st.title("🩺 Knee AI Telemedicine")
menu = st.sidebar.radio("เมนู:", ["1. ลงทะเบียน", "2. สแกน", "3. สรุปผล", "4. สถิติ"])

# --- เมนู 1 ---
if menu == "1. ลงทะเบียน":
with st.form("f1"):
name = st.text_input("ชื่อ")
hospital = st.selectbox("รพ.", ["รพ.ลพบุรี", "รพ.พัฒนานิคม"])
if st.form_submit_button("บันทึก"):
st.session_state.user_data = {"name": name, "hospital": hospital}
st.success("บันทึกแล้ว")

# --- เมนู 2 ---
elif menu == "2. สแกน":
if not st.session_state.user_data: st.warning("ลงทะเบียนก่อน")
else:
st.write("เลือกภาพ:")
file = st.file_uploader("Upload", type=["jpg", "png"])
if file:
st.session_state.analysis_result = {"angle": 120, "problem": "เข่าเสื่อม", "image": "test"}
st.success("วิเคราะห์เสร็จแล้ว")

# --- เมนู 3 ---
elif menu == "3. สรุปผล":
if not st.session_state.analysis_result: st.warning("ยังไม่มีข้อมูล")
else:
st.write("ผลการตรวจ:", st.session_state.analysis_result["angle"], "องศา")
if st.button("ส่งข้อมูล"): st.balloons()

# --- เมนู 4 ---
elif menu == "4. สถิติ":
st.write("### สถิติ")
df = pd.DataFrame([185, 92, 450], index=["ขาโก่ง", "ขานิ่ง", "ปกติ"], columns=["จำนวน"])
st.bar_chart(df)
if st.button("รีเซ็ตระบบ"): st.rerun()
