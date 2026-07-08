import streamlit as st
import pandas as pd
st.set_page_config(page_title="Knee AI", layout="centered")

# ปายดูตรงนี้: บรรทัดที่อยู่ใต้ if หรือ elif ให้ปายเคาะ Spacebar 4 ครั้งก่อนพิมพ์โค้ดนะ
if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'analysis_result' not in st.session_state: st.session_state.analysis_result = None

st.title("🩺 Knee AI Telemedicine")
menu = st.sidebar.radio("เมนู:", ["1. ลงทะเบียน", "2. สแกน", "3. สรุปผล", "4. สถิติ", "5. MRT"])

if menu == "1. ลงทะเบียน":
    name = st.text_input("ชื่อผู้ป่วย:")
    if st.button("บันทึก"): st.session_state.user_data = {"name": name}

elif menu == "2. สแกน":
    file = st.file_uploader("เลือกไฟล์ภาพ:")
    if file and st.button("ประมวลผล"): st.session_state.analysis_result = {"angle": 145}

elif menu == "3. สรุปผล":
    if st.session_state.analysis_result: st.write("มุมเข่า: 145 องศา")
    else: st.warning("ยังไม่มีข้อมูล")

elif menu == "4. สถิติ":
    df = pd.DataFrame([10, 20, 30], index=["ขาโก่ง", "ขานิ่ง", "ปกติ"], columns=["จำนวน"])
    st.bar_chart(df)

elif menu == "5. MRT":
    w = st.number_input("น้ำหนัก (kg):", value=10.0)
    r = st.number_input("จำนวนครั้ง:", value=1)
    if st.button("คำนวณ"): st.success(f"ความแข็งแรง: {w / (1.0278 - (0.0278 * r)):.2f} kg")

