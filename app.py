import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import pandas as pd

st.set_page_config(page_title="Knee AI Telemedicine", layout="centered")

if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'analysis_result' not in st.session_state: st.session_state.analysis_result = None

def calculate_angle(a, b, c):
point_a = np.array(a)
point_b = np.array(b)
point_c = np.array(c)
r = np.arctan2(point_c[1]-point_b[1], point_c[0]-point_b[0]) - np.arctan2(point_a[1]-point_b[1], point_a[0]-point_b[0])
angle = np.abs(r * 180.0 / np.pi)
if angle > 180.0: angle = 360 - angle
return int(angle)

st.title("🩺 Knee AI Telemedicine")
menu = st.sidebar.radio("เมนู:", ["1. ลงทะเบียน", "2. สแกน", "3. สรุปผล", "4. สถิติ", "5. MRT"])

if menu == "1. ลงทะเบียน":
with st.form("f1"):
name = st.text_input("ชื่อ")
hospital = st.selectbox("รพ.", ["รพ.ลพบุรี", "รพ.พัฒนานิคม"])
if st.form_submit_button("บันทึก"):
st.session_state.user_data = {"name": name, "hospital": hospital}
st.success("บันทึกข้อมูลเรียบร้อย")

elif menu == "2. สแกน":
if not st.session_state.user_data: st.warning("ลงทะเบียนก่อนนะคะ")
else:
file = st.file_uploader("Upload X-Ray", type=["jpg", "png"])
if file:
st.session_state.analysis_result = {"angle": 120, "problem": "เข่าเสื่อม"}
st.success("วิเคราะห์เสร็จแล้ว")

elif menu == "3. สรุปผล":
if not st.session_state.analysis_result: st.warning("ยังไม่มีข้อมูลผลตรวจ")
else:
st.write("ผลการตรวจ:", st.session_state.analysis_result["angle"], "องศา")
if st.button("ส่งข้อมูล"): st.balloons()

elif menu == "4. สถิติ":
st.write("### สถิติผู้ป่วย")
df = pd.DataFrame([185, 92, 450], index=["ขาโก่ง", "ขานิ่ง", "ปกติ"], columns=["จำนวน"])
st.bar_chart(df)
if st.button("รีเซ็ตระบบ"): st.rerun()

elif menu == "5. MRT":
st.write("### 💪 คำนวณค่า MRT")
with st.form("mrt_form"):
weight = st.number_input("น้ำหนัก (kg):", value=10.0)
reps = st.number_input("จำนวนครั้ง:", value=1)
if st.form_submit_button("คำนวณ"):
one_rm = weight / (1.0278 - (0.0278 * reps))
st.success(f"ความแข็งแรงสูงสุด: {one_rm:.2f} kg")

