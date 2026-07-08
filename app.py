import streamlit as st
import pandas as pd

st.set_page_config(page_title="Knee AI", layout="centered")

if 'user_data' not in st.session_state: st.session_state.user_data = None

st.title("🩺 Knee AI Telemedicine")
menu = st.sidebar.radio("เมนู:", ["1. ลงทะเบียน", "2. สแกน", "3. สรุปผล", "4. สถิติ", "5. MRT"])

if menu == "1. ลงทะเบียน":
st.write("---")
name = st.text_input("ชื่อของคุณ")
hospital = st.selectbox("โรงพยาบาล", ["รพ.ลพบุรี", "รพ.พัฒนานิคม"])
if st.button("บันทึกข้อมูล"):
st.session_state.user_data = {"name": name, "hospital": hospital}
st.success("บันทึกข้อมูลแล้ว!")

elif menu == "2. สแกน":
st.write("---")
file = st.file_uploader("เลือกไฟล์ X-Ray", type=["jpg", "png"])
if file:
st.success("อัปโหลดสำเร็จ! กำลังวิเคราะห์...")

elif menu == "3. สรุปผล":
st.write("---")
st.write("ผลการตรวจปกติ")

elif menu == "4. สถิติ":
st.write("---")
df = pd.DataFrame([10, 20, 30], index=["ขาโก่ง", "ขานิ่ง", "ปกติ"], columns=["จำนวน"])
st.bar_chart(df)

elif menu == "5. MRT":
st.write("---")
w = st.number_input("น้ำหนัก (kg):", value=10.0)
r = st.number_input("จำนวนครั้ง:", value=1)
if st.button("คำนวณ MRT"):
res = w / (1.0278 - (0.0278 * r))
st.success(f"ค่า MRT คือ: {res:.2f} kg")

