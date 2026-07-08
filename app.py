import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import time
import pandas as pd

# 🎨 1. ตั้งค่าหน้าต่างเว็บ
st.set_page_config(page_title="Knee AI - NextGen Telemedicine", page_icon="⚡", layout="centered")

# 🚀 ส่วนหัว
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🤖 KNEE-AI: MULTI-AXIS ALIGNMENT ENGINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1a1; font-family: monospace;'>PROTOTYPE VERSION 6.5 // BY TEAM VITAMIN C</p>", unsafe_allow_html=True)

# 📌 เมนู
st.sidebar.markdown("<h2 style='color: #00f2fe; text-align: center;'>📡 SYSTEM CORE v6.5</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("SELECT INTEL MODE:", [
    "🧬 [01] PATIENT INFRASTRUCTURE", 
    "📷 [02] DEEP SCAN & IMAGE ENGINE", 
    "📊 [03] DIAGNOSTIC QUANTUM MATRIX",
    "📈 [04] EPIDEMIOLOGY DASHBOARD"
])

if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

hospitals_data = {
    "ลพบุรี": ["โรงพยาบาลลพบุรี", "โรงพยาบาลพัฒนานิคม", "โรงพยาบาลพระนารายณ์มหาราช"],
    "กรุงเทพมหานคร": ["โรงพยาบาลศิริราช", "โรงพยาบาลจุฬาลงกรณ์"]
}
provinces = sorted(list(hospitals_data.keys()))

# 🧬 MODE 01
if menu == "🧬 [01] PATIENT INFRASTRUCTURE":
    st.markdown("### 📝 PATIENT REGISTRATION")
    with st.form("reg_form"):
        name = st.text_input("NAME (ชื่อ-นามสกุล):")
        age = st.number_input("AGE (อายุ):", min_value=0, max_value=120, value=50)
        selected_province = st.selectbox("PROVINCE:", provinces)
        hospital = st.selectbox("HOSPITAL:", hospitals_data.get(selected_province, ["รพ. ประจำจังหวัด"]))
        submit_button = st.form_submit_button("⚡ INITIALIZE")
        
    if submit_button and name:
        st.session_state.user_data = {"name": name, "age": age, "hospital": hospital}
        st.success(f"ลงทะเบียนคุณ {name} เรียบร้อย!")

# 📸 MODE 02
elif menu == "📷 [02] DEEP SCAN & IMAGE ENGINE":
    if st.session_state.user_data is None:
        st.warning("🚨 กรุณาลงทะเบียนก่อนค่ะ")
    else:
        uploaded_file = st.file_uploader("CHOOSE IMAGE:", type=["jpg", "png"])
        if uploaded_file and st.button("🤖 START ANALYSIS"):
            # จำลองค่าวิเคราะห์
            knee_angle = 120 
            st.session_state.analysis_result = {"angle": knee_angle, "confidence": 95.0}
            st.success("ประมวลผลเสร็จสิ้น!")

# 📊 MODE 03
elif menu == "📊 [03] DIAGNOSTIC QUANTUM MATRIX":
    if st.session_state.analysis_result:
        angle = st.session_state.analysis_result["angle"]
        st.markdown("### 📋 AI EVALUATION")
        
        if angle < 130:
            st.error("""🚨 CRITICAL AREA: ตรวจพบภาวะสรีระขาโก่ง (Bowlegs)

ผลวิเคราะห์: แนวน้ำหนักตกลงสู่ข้อเข่าด้านใน ส่งผลให้แนวเข่าโค้งแยกออกจากกันเกินเกณฑ์ปกติ เสี่ยงต่อข้อเข่าเสื่อมก่อนวัยอันควร ควรปรึกษาแพทย์กระดูกและข้อโดยด่วน""")
        else:
            st.success("✅ OPTIMIZED ALIGNMENT: สรีระปกติ")
