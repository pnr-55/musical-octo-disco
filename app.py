import streamlit as st

st.set_page_config(page_title="Knee AI Diagnostic", layout="centered")

# --- ระบบจำข้อมูล ---
if 'page' not in st.session_state: st.session_state.page = "Register"
if 'name' not in st.session_state: st.session_state.name = ""
if 'bmi_status' not in st.session_state: st.session_state.bmi_status = ""

def calculate_bmi_risk(w, h):
    bmi = w / ((h/100) ** 2)
    if bmi > 25: return f"น้ำหนักเกินเกณฑ์ (BMI: {bmi:.1f}) - เสี่ยงสูงต่อข้อเข่าเสื่อม"
    return f"น้ำหนักอยู่ในเกณฑ์ปกติ (BMI: {bmi:.1f})"

# --- หน้าที่ 1: ประวัติส่วนตัว (เพิ่มน้ำหนัก/ส่วนสูง) ---
if st.session_state.page == "Register":
    st.title("🩺 1. ข้อมูลผู้ป่วยและดัชนีมวลกาย")
    st.session_state.name = st.text_input("ชื่อ - นามสกุล:")
    w = st.number_input("น้ำหนัก (kg):", value=60.0)
    h = st.number_input("ส่วนสูง (cm):", value=160.0)
    st.session_state.hospital = st.selectbox("เลือกโรงพยาบาล:", ["โรงพยาบาลพระนารายณ์", "โรงพยาบาลลพบุรี", "อื่นๆ"])
    
    if st.button("บันทึกข้อมูลและวิเคราะห์ความเสี่ยง"):
        st.session_state.bmi_status = calculate_bmi_risk(w, h)
        st.session_state.page = "Scan"
        st.rerun()

# --- หน้าที่ 2: วิเคราะห์ ---
elif st.session_state.page == "Scan":
    st.title("📷 2. วิเคราะห์ด้วย AI")
    file = st.file_uploader("อัปโหลด X-Ray:", type=["jpg", "png"])
    if file and st.button("วินิจฉัยโรค"):
        st.session_state.angle = 155.0 # สมมติผล AI
        st.session_state.page = "Result"
        st.rerun()

# --- หน้าที่ 3: ผลวินิจฉัย (เลิศๆ) ---
elif st.session_state.page == "Result":
    st.title("📊 3. ผลการวินิจฉัยทางการแพทย์")
    angle = st.session_state.angle
    
    # วิเคราะห์โรค
    diagnosis = "ขาปกติ"
    if angle < 170: diagnosis = "ขาโก่ง (Bowlegs)"
    elif angle > 175: diagnosis = "ขาฉิ่ง (Knock-knees)"
    
    st.subheader(f"ผลการประเมิน: {diagnosis}")
    st.write(f"**สุขภาพจาก BMI:** {st.session_state.bmi_status}")
    
    # คำแนะนำตามความเสี่ยง
    if "ขาโก่ง" in diagnosis or "ขาฉิ่ง" in diagnosis:
        st.error("🚨 สภาวะข้อเข่าผิดรูป: เสี่ยงต่อข้อเข่าเสื่อม")
        st.write("คำแนะนำ: ต้องทำกายภาพบำบัดและปรับเปลี่ยนรองเท้าเพื่อลดแรงกระแทก")
        st.link_button("📍 ค้นหาคลินิกกายภาพใกล้ฉัน", "https://www.google.com/maps/search/คลินิกกายภาพบำบัดใกล้ฉัน")
    
    # ปุ่มดาวน์โหลดรายงานให้หมอ
    report = f"ผลตรวจของ {st.session_state.name}\nการวินิจฉัย: {diagnosis}\nความเสี่ยงจาก BMI: {st.session_state.bmi_status}"
    st.download_button("📥 ดาวน์โหลดรายงานฉบับสมบูรณ์ให้แพทย์", report, "Medical_Report.txt")

    if st.button("เริ่มต้นใหม่"):
        st.session_state.page = "Register"
        st.rerun()
