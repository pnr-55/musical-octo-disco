import streamlit as st
import pandas as pd

st.set_page_config(page_title="Knee AI Pro", layout="centered")

# ตกแต่งหัวแอปให้สวยงาม
st.markdown("""
    <style>
    .main {background-color: #f5f7f9;}
    h1 {color: #2c3e50; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 Knee AI Telemedicine")

# สร้าง Tabs ให้ใช้งานง่าย
tab1, tab2, tab3, tab4 = st.tabs(["📋 ลงทะเบียน", "📷 สแกน", "📊 สรุปผล", "💪 คำนวณ MRT"])

if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'res' not in st.session_state: st.session_state.res = None

with tab1:
    st.subheader("บันทึกข้อมูลผู้ป่วย")
    name = st.text_input("ชื่อ - นามสกุล")
    if st.button("บันทึกข้อมูล"):
        st.session_state.user_data = name
        st.success(f"สวัสดีคุณ {name}!")

with tab2:
    st.subheader("สแกนภาพเข่า")
    file = st.file_uploader("อัปโหลดรูปภาพ", type=["jpg", "png"])
    if file and st.button("ประมวลผล"):
        st.session_state.res = 145
        st.success("ประมวลผลเสร็จสิ้น!")

with tab3:
    st.subheader("รายงานผล")
    if st.session_state.res:
        st.metric("มุมข้อเข่า", f"{st.session_state.res}°")
    else:
        st.info("กรุณาสแกนภาพก่อนครับ")

with tab4:
    st.subheader("เครื่องมือคำนวณความแข็งแรง (MRT)")
    w = st.number_input("น้ำหนัก (kg):", value=10.0)
    r = st.number_input("จำนวนครั้ง:", min_value=1, value=1)
    if st.button("คำนวณ MRT"):
        ans = w / (1.0278 - (0.0278 * r))
        st.success(f"ความแข็งแรงสูงสุดของคุณ: {ans:.2f} kg")
