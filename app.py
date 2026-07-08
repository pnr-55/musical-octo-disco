import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import time
import pandas as pd

st.set_page_config(page_title="Knee AI - NextGen", layout="centered")

st.markdown("<h2 style='text-align: center; color: #00f2fe;'>🤖 KNEE-AI SYSTEM</h2>", unsafe_allow_html=True)
st.sidebar.markdown("### 📡 CONTROL PANEL")
menu = st.sidebar.radio("ขั้นตอนการทำงาน:", [
"📌 [01] บันทึกประวัติ",
"📷 [02] อัปโหลดภาพ",
"📊 [03] ผลการวินิจฉัย",
"📈 [04] สถิติ",
"💪 [05] คำนวณค่า MRT"
])

if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'analysis_result' not in st.session_state: st.session_state.analysis_result = None

if menu == "📌 [01] บันทึกประวัติ":
 st.markdown("#### 📝 ข้อมูลผู้ป่วย")
with st.form("reg_form"):
 name = st.text_input("ชื่อ - นามสกุล:")
submit = st.form_submit_button("บันทึก")
if submit: st.session_state.user_data = {"name": name}
elif menu == "📷 [02] อัปโหลดภาพ":
st.markdown("#### 📷 สแกนเข่า")
uploaded_file = st.file_uploader("เลือกไฟล์ภาพ:", type=["jpg", "png"])
if uploaded_file:
if st.button("ประมวลผล"): st.session_state.analysis_result = {"angle": 145, "confidence": 99.9}
elif menu == "📊 [03] ผลการวินิจฉัย":
st.markdown("#### 📊 ผลการตรวจ")
if st.session_state.analysis_result: st.write(f"มุมข้อเข่า: {st.session_state.analysis_result['angle']} องศา")
else: st.warning("ยังไม่มีข้อมูล")
elif menu == "📈 [04] สถิติ":
st.markdown("#### 📊 สถิติระบาดวิทยา")
df = pd.DataFrame([185, 92, 450], index=["ขาโก่ง", "ขานิ่ง", "ปกติ"], columns=["จำนวน"])
st.bar_chart(df)
elif menu == "💪 [05] คำนวณค่า MRT":
st.markdown("#### 💪 เครื่องมือคำนวณค่า MRT")
weight = st.number_input("น้ำหนักที่ใช้ทดสอบ (kg):", value=10.0)
reps = st.number_input("จำนวนครั้งสูงสุด (reps):", min_value=1, value=1)
if st.button("คำนวณค่า"):
one_rm = weight / (1.0278 - (0.0278 * reps))
st.success(f"ความแข็งแรงสูงสุดของคุณอยู่ที่ประมาณ {one_rm:.2f} kg")

