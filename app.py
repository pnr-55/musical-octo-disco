import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="Knee AI Innovation", layout="centered")

# 2. เก็บสถานะหน้าจอ
if 'page' not in st.session_state: st.session_state.page = "Register"
if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'analysis' not in st.session_state: st.session_state.analysis = None

def go_to(p): st.session_state.page = p

# --- หน้าที่ 1: ลงทะเบียน ---
if st.session_state.page == "Register":
    st.title("🩺 1. ข้อมูลผู้ป่วย")
    name = st.text_input("ชื่อ - นามสกุล:")
    weight = st.number_input("น้ำหนักตัว (kg):", value=60.0)
    height = st.number_input("ส่วนสูง (cm):", value=160.0)
    if st.button("ถัดไป >>"):
        st.session_state.user_data = {"name": name, "weight": weight, "height": height}
        go_to("Scan")
        st.rerun()

# --- หน้าที่ 2: สแกนวิเคราะห์ ---
elif st.session_state.page == "Scan":
    st.title("📷 2. วิเคราะห์ AI & คณิตศาสตร์")
    file = st.file_uploader("อัปโหลด X-Ray:", type=["jpg", "png"])
    if file and st.button("วิเคราะห์มุมเข่า"):
        # จำลองค่ามุมที่ AI คำนวณได้
        angle = 155.0 
        st.session_state.analysis = {"angle": angle}
        go_to("Result")
        st.rerun()

# --- หน้าที่ 3: ผลลัพธ์และระดับความรุนแรง ---
elif st.session_state.page == "Result":
    st.title("📊 3. ผลการวิเคราะห์")
    angle = st.session_state.analysis['angle']
    st.metric("มุมข้อเข่า", f"{angle}°")
    
    # ระบบประเมินระดับความรุนแรง
    st.subheader("ระดับความรุนแรง (Severity Grading)")
    if angle >= 170:
        st.success("🟢 ระดับปกติ: โครงสร้างกระดูกสมดุล")
    elif 160 <= angle < 170:
        st.warning("⚠️ ระดับ 1: เริ่มเบี่ยงเบนเล็กน้อย")
    elif 150 <= angle < 160:
        st.error("🚨 ระดับ 2: ขาโก่งชัดเจน ควรพบนักกายภาพ")
    else:
        st.error("⛔ ระดับ 3: ผิดรูปสูง เสี่ยงข้อเข่าเสื่อมรุนแรง")

    st.write("---")
    st.subheader("💪 เสริม: คำนวณความแข็งแรง (MRT)")
    mrt_w = st.number_input("น้ำหนักที่ยกได้ (kg):", value=20.0)
    mrt_r = st.number_input("จำนวนครั้ง (reps):", value=5)
    if st.button("คำนวณ MRT"):
        one_rm = mrt_w / (1.0278 - (0.0278 * mrt_r))
        st.info(f"ค่าความแข็งแรงสูงสุดของคุณ: {one_rm:.2f} kg")
    
    if st.button("<< เริ่มต้นใหม่"):
        go_to("Register")
        st.rerun()
