import streamlit as st
import pandas as pd

st.set_page_config(page_title="Knee AI Diagnostic", layout="centered")

# --- ระบบจำข้อมูล ---
if 'page' not in st.session_state: st.session_state.page = "Register"
if 'name' not in st.session_state: st.session_state.name = ""

# --- หน้าที่ 1: ลงทะเบียน ---
if st.session_state.page == "Register":
    st.title("🩺 1. ข้อมูลผู้ป่วย")
    st.session_state.name = st.text_input("ชื่อ - นามสกุล:")
    w = st.number_input("น้ำหนัก (kg):", value=60.0)
    h = st.number_input("ส่วนสูง (cm):", value=160.0)
    if st.button("วิเคราะห์"):
        st.session_state.bmi = w / ((h/100) ** 2)
        st.session_state.page = "Scan"
        st.rerun()

# --- หน้าที่ 2: วิเคราะห์ ---
elif st.session_state.page == "Scan":
    st.title("📷 2. วิเคราะห์ด้วย AI")
    file = st.file_uploader("อัปโหลด X-Ray:", type=["jpg", "png"])
    if file and st.button("วินิจฉัยโรค"):
        st.session_state.angle = 155.0  # สมมติผลที่ได้จาก AI
        st.session_state.page = "Result"
        st.rerun()

# --- หน้าที่ 3: ผลเปรียบเทียบ (เปรียบเทียบให้เห็นชัดๆ) ---
elif st.session_state.page == "Result":
    st.title("📊 3. ผลการวินิจฉัยเปรียบเทียบ")
    angle = st.session_state.angle
    norm_min, norm_max = 170, 175
    
    # สรุปผล
    if norm_min <= angle <= norm_max:
        st.success(f"✅ เข่าปกติ (มุม {angle}° อยู่ในเกณฑ์ {norm_min}-{norm_max}°)")
    else:
        diff = abs(angle - 172.5) # ค่าเฉลี่ยมาตรฐาน
        status = "ขาโก่ง" if angle < norm_min else "ขาฉิ่ง"
        st.error(f"🚨 ผิดปกติ: พบภาวะ{status} (มุม {angle}° เบี่ยงเบนจากค่าปกติ {diff:.1f}°)")

    # ตารางเปรียบเทียบให้เห็นภาพ
    st.subheader("📋 ตารางเปรียบเทียบค่ามาตรฐาน")
    comparison = {
        "สถานะ": ["ปกติ", "ของคุณ"],
        "มุมข้อเข่า": ["170 - 175°", f"{angle}°"]
    }
    st.table(pd.DataFrame(comparison))

    if st.button("เริ่มต้นใหม่"):
        st.session_state.page = "Register"
        st.rerun()
