import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Knee AI Diagnostic", layout="centered")

# --- ระบบจัดการข้อมูล (กันข้อมูลหาย) ---
if 'data' not in st.session_state:
    st.session_state.data = {
        'name': "", 'hospital': "โรงพยาบาลพระนารายณ์", 
        'w': 60.0, 'h': 160.0, 'angle': None, 'mrt': None
    }
if 'page' not in st.session_state: st.session_state.page = "Register"

# --- หน้าที่ 1: ลงทะเบียน ---
if st.session_state.page == "Register":
    st.title("🩺 1. ข้อมูลผู้ป่วย")
    st.session_state.data['name'] = st.text_input("ชื่อ - นามสกุล:", value=st.session_state.data['name'])
    st.session_state.data['w'] = st.number_input("น้ำหนัก (kg):", value=st.session_state.data['w'])
    st.session_state.data['h'] = st.number_input("ส่วนสูง (cm):", value=st.session_state.data['h'])
    st.session_state.data['hospital'] = st.selectbox("เลือกโรงพยาบาล:", ["โรงพยาบาลพระนารายณ์", "โรงพยาบาลลพบุรี", "โรงพยาบาลอานันทมหิดล", "อื่นๆ"])
    if st.button("บันทึกและวิเคราะห์ >>"):
        st.session_state.page = "Scan"
        st.rerun()

# --- หน้าที่ 2: สแกน ---
elif st.session_state.page == "Scan":
    st.title("📷 2. วิเคราะห์ด้วย AI")
    file = st.file_uploader("อัปโหลด X-Ray:", type=["jpg", "png"])
    if file and st.button("วินิจฉัยโรค"):
        st.session_state.data['angle'] = 155.0  # ค่าจำลองจาก AI
        st.session_state.page = "Result"
        st.rerun()

# --- หน้าที่ 3: ผลลัพธ์และวิเคราะห์เปรียบเทียบ ---
elif st.session_state.page == "Result":
    st.title("📊 3. ผลการวินิจฉัยเปรียบเทียบ")
    d = st.session_state.data
    norm_min, norm_max = 170, 175
    
    # ส่วนแสดงเปรียบเทียบ (ปกติ vs ตรวจพบ)
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🟢 เกณฑ์ปกติ")
        st.metric("ช่วงมุมมาตรฐาน", "170° - 175°")
    with col2:
        st.write("### 🚨 ผลตรวจของคุณ")
        status = "ปกติ" if norm_min <= d['angle'] <= norm_max else "ผิดปกติ"
        st.metric("มุมข้อเข่าของคุณ", f"{d['angle']}°")
        if status == "ผิดปกติ": st.error("พบภาวะผิดรูป") 
        else: st.success("อยู่ในเกณฑ์ปกติ")

    # ตารางวิเคราะห์เชิงลึก
    st.write("---")
    st.subheader("📋 ตารางวิเคราะห์เชิงลึกทางการแพทย์")
    comp_data = {
        "ลักษณะ": ["ปกติ", "ขาโก่ง (Bowlegs)", "ขาฉิ่ง (Knock-knees)"],
        "ช่วงมุม (องศา)": ["170° - 175°", "< 170°", "> 175°"],
        "ผลกระทบ": ["สมดุลปกติ", "แรงกระแทกเข่าด้านในสูง", "แรงกระแทกเข่าด้านนอกสูง"]
    }
    st.table(pd.DataFrame(comp_data))

    # ส่วนเสริม (คลินิก/MRT)
    st.link_button("📍 ค้นหาคลินิกกายภาพบำบัดใกล้ฉัน", "https://www.google.com/maps/search/คลินิกกายภาพบำบัดใกล้ฉัน")
    
    st.subheader("💪 คำนวณความแข็งแรง (MRT)")
    mrt_w = st.number_input("น้ำหนักที่ยกได้ (kg):", value=20.0)
    mrt_r = st.number_input("จำนวนครั้ง (reps):", value=5)
    if st.button("คำนวณ"): st.session_state.data['mrt'] = mrt_w / (1.0278 - (0.0278 * mrt_r))
    if st.session_state.data['mrt']: st.success(f"ค่าความแข็งแรงสูงสุด: {st.session_state.data['mrt']:.2f} kg")

    # ดาวน์โหลดรายงาน
    report = f"รายงานผลการตรวจเข่า: {d['name']}\nมุมเข่า: {d['angle']} องศา\nสถานะ: {status}"
    st.download_button("📥 ดาวน์โหลดรายงานฉบับสมบูรณ์ให้แพทย์", report, "Medical_Report.txt")

    if st.button("<< เริ่มต้นใหม่"):
        st.session_state.data = {'name': "", 'hospital': "โรงพยาบาลพระนารายณ์", 'w': 60.0, 'h': 160.0, 'angle': None, 'mrt': None}
        st.session_state.page = "Register"
        st.rerun()
