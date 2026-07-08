import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Knee AI", layout="centered")

if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'analysis_result' not in st.session_state: st.session_state.analysis_result = None

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
if not st.session_state.user_data: st.warning("ลงทะเบียนก่อน")
else:
file = st.file_uploader("Upload X-Ray", type=["jpg", "png"])
if file:
st.session_state.analysis_result = {"angle": 120, "problem": "เข่าเสื่อม"}
st.success("วิเคราะห์เสร็จแล้ว")

elif menu == "3. สรุปผล":
if not st.session_state.analysis_result: st.warning("ยังไม่มีข้อมูล")
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
w = st.number_input("น้ำหนัก (kg):", value=10.0)
r = st.number_input("จำนวนครั้ง:", value=1)
if st.button("คำนวณค่า MRT"):
ans = w / (1.0278 - (0.0278 * r))
st.success(f"ความแข็งแรงสูงสุด: {ans:.2f} kg")

