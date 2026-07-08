import streamlit as st
import numpy as np
import pandas as pd
import datetime

# 🎨 ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Knee AI - Telemedicine Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🤖 KNEE-AI: ADVANCED PRO v7.0</h1>", unsafe_allow_html=True)

# 💾 จัดการ Session
if 'patients' not in st.session_state: st.session_state.patients = {}
if 'current_id' not in st.session_state: st.session_state.current_id = None

menu = st.sidebar.radio("SELECT MODE:", ["🧬 [01] ลงทะเบียน/ล็อกอิน", "📷 [02] สแกนเข่า", "📊 [03] ผลลัพธ์และท่ากายภาพ", "📈 [04] ประวัติพัฒนาการ"])

# 🧬 [01] ลงทะเบียน
if menu == "🧬 [01] ลงทะเบียน/ล็อกอิน":
    st.subheader("📝 ระบบลงทะเบียนคนไข้")
    pid = st.text_input("กรอกรหัสคนไข้ของคุณ (หรือตั้งใหม่):")
    if pid and st.button("เข้าสู่ระบบ"):
        st.session_state.current_id = pid
        if pid not in st.session_state.patients:
            st.session_state.patients[pid] = {"history": [], "data": {}}
            st.success(f"สร้างโปรไฟล์ใหม่รหัส: {pid}")
        else:
            st.success(f"ยินดีต้อนรับกลับมาค่ะ รหัส: {pid}")

    if st.session_state.current_id:
        with st.form("reg"):
            weight = st.number_input("น้ำหนัก (kg):", value=60.0)
            height = st.number_input("ส่วนสูง (cm):", value=160.0)
            province = st.text_input("จังหวัดของคุณ:")
            if st.form_submit_button("บันทึกข้อมูล"):
                bmi = weight / ((height/100)**2)
                st.session_state.patients[st.session_state.current_id]["data"] = {"bmi": bmi, "province": province}
                st.write(f"ค่า BMI ของคุณคือ: {bmi:.2f}")

# 📷 [02] สแกนเข่า
elif menu == "📷 [02] สแกนเข่า":
    if not st.session_state.current_id: st.warning("กรุณาล็อกอินก่อนค่ะ")
    else:
        file = st.file_uploader("อัปโหลดภาพเข่าของคุณ:", type=["jpg", "png"])
        if file and st.button("วิเคราะห์"):
            angle = np.random.randint(120, 175) # จำลองค่าองศา
            date = datetime.date.today().isoformat()
            res = {"date": date, "angle": angle}
            st.session_state.patients[st.session_state.current_id]["history"].append(res)
            st.write(f"ผลการวิเคราะห์เบื้องต้น: มุมเข่า {angle}°")

# 📊 [03] ผลลัพธ์และคำแนะนำ
elif menu == "📊 [03] ผลลัพธ์และท่ากายภาพ":
    if st.session_state.current_id and st.session_state.patients[st.session_state.current_id]["history"]:
        last = st.session_state.patients[st.session_state.current_id]["history"][-1]
        st.subheader(f"ผลลัพธ์ล่าสุด: {last['angle']}°")
        
        st.write("---")
        st.markdown("### การเปรียบเทียบภาพข้อเข่า")
        col1, col2 = st.columns(2)
        with col1:
            st.image("normal_knee.jpg", caption="มาตรฐานขาปกติ")
        with col2:
            st.image("varus_knee.jpg", caption="ลักษณะขาโก่ง (Varus)")
        st.write("---")

        if last['angle'] < 150:
            st.error("พบภาวะขาโก่ง/เข่าชิด: แนะนำทำกายภาพบำบัด")
            st.markdown("### 🏃‍♂️ ท่าบริหาร: ยืดกล้ามเนื้อต้นขา")
            st.write("1. นอนราบ 2. ยกขาขึ้น 3. ค้างไว้ 10 วินาที")
            prov = st.session_state.patients[st.session_state.current_id]["data"].get("province", "")
            st.markdown(f"🏥 [ค้นหาคลินิก/รพ. ใน {prov} บน Google Maps](https://www.google.com/maps/search/โรงพยาบาล+ใน+{prov})")
        else:
            st.success("แนวเข่าปกติค่ะ")

# 📈 [04] ประวัติ
elif menu == "📈 [04] ประวัติพัฒนาการ":
    if st.session_state.current_id:
        hist = st.session_state.patients[st.session_state.current_id]["history"]
        if hist:
            df = pd.DataFrame(hist)
            st.line_chart(df.set_index('date'))
        else:
            st.write("ยังไม่มีประวัติการสแกนค่ะ")

st.sidebar.markdown("---")
st.sidebar.caption("⚠️ คำเตือน: นี่คือการคัดกรองเบื้องต้น ไม่แทนการวินิจฉัยของแพทย์")
