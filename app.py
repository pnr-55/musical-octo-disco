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
            # ==========================================
# 📊 MODE 03: DIAGNOSTIC QUANTUM MATRIX (ฉบับอัปเกรด)
# ==========================================
elif menu == "📊 [03] DIAGNOSTIC QUANTUM MATRIX":
    if st.session_state.analysis_result:
        res = st.session_state.analysis_result
        angle = res["angle"]
        
        st.markdown("### 📋 AI MEDICAL EVALUATION & RECOMMENDATIONS")
        
        # 1. ส่วนเปรียบเทียบ (เปรียบเทียบผลกับค่ามาตรฐาน)
        st.markdown("#### 📐 KNEE ALIGNMENT COMPARISON")
        st.write(f"ผลวัดได้: **{angle}°** | เกณฑ์ปกติ: **150° - 170°**")
        
        if angle < 130:
            st.error("🚨 ผลประเมิน: เสี่ยงภาวะขาโก่ง (Bowlegs)")
            reason = "แนวน้ำหนักตกเข้าด้านในข้อเข่า ทำให้เข่าห่างออกจากกัน"
            tips = ["ออกกำลังกายเสริมกล้ามเนื้อสะโพก", "หลีกเลี่ยงการนั่งขัดสมาธิ", "พบแพทย์เพื่อตรวจเอกซเรย์"]
        elif angle <= 160:
            st.warning("⚠️ ผลประเมิน: เสี่ยงภาวะเข่าชิด (Knock-knees)")
            reason = "แนวเข่าเบียดชิดกัน ทำให้น้ำหนักลงที่เข่าด้านนอก"
            tips = ["ยืดกล้ามเนื้อต้นขาด้านนอก", "ควบคุมน้ำหนักเพื่อลดแรงกด", "ปรึกษาแพทย์กายภาพบำบัด"]
        else:
            st.success("✅ ผลประเมิน: แนวเข่าปกติ (Normal)")
            reason = "องศาอยู่ในเกณฑ์สุขภาพดี"
            tips = ["คงความแข็งแรงของกล้ามเนื้อต้นขา", "ออกกำลังกายแบบคาร์ดิโอที่แรงกระแทกต่ำ"]

        st.info(f"💡 **หลักการอ้างอิง:** {reason}")
        
        # 2. คำแนะนำกายภาพบำบัด
        st.markdown("#### 🏃‍♂️ PHYSICAL THERAPY RECOMMENDATIONS")
        for tip in tips:
            st.write(f"- {tip}")
            
        # 3. ค้นหาโรงพยาบาล/คลินิกใกล้บ้าน
        st.markdown("#### 🏥 CLINICS & HOSPITALS NEAR YOU")
        province = st.session_state.user_data['province']
        st.write(f"เราแนะนำหน่วยบริการในจังหวัด **{province}** ดังนี้:")
        st.write(f"👉 **{st.session_state.user_data['hospital']}** (หน่วยบริการหลักที่คุณเลือก)")
        st.caption("หมายเหตุ: เพื่อผลการวินิจฉัยที่แม่นยำ กรุณาปรึกษาแพทย์เฉพาะทางกระดูกและข้อ")

