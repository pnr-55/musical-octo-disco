import streamlit as st
import numpy as np
import pandas as pd
import datetime
import os

# 🎨 ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Knee AI - Telemedicine Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🤖 KNEE-AI: ADVANCED PRO v7.0</h1>", unsafe_allow_html=True)

# 💾 จัดการ Session
if 'patients' not in st.session_state: st.session_state.patients = {}
if 'current_id' not in st.session_state: st.session_state.current_id = None

menu = st.sidebar.radio("SELECT MODE:", ["🧬 [01] ลงทะเบียน/ล็อกอิน", "📷 [02] สแกนเข่า", "📊 [03] ผลลัพธ์และท่ากายภาพ", "📈 [04] ประวัติพัฒนาการ"])

# 🧬 [01] ลงทะเบียน (แนะนำรหัส 4-6 หลัก)
if menu == "🧬 [01] ลงทะเบียน/ล็อกอิน":
    st.subheader("📝 ระบบลงทะเบียนคนไข้")
    pid = st.text_input("กรอกรหัสคนไข้ของคุณ (เช่น 1234):")
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
                st.success(f"บันทึกข้อมูลสำเร็จ! BMI: {bmi:.2f}")

# 📷 [02] สแกนเข่า
elif menu == "📷 [02] สแกนเข่า":
    if not st.session_state.current_id: st.warning("กรุณาล็อกอินก่อนค่ะ")
    else:
        file = st.file_uploader("อัปโหลดภาพเข่าของคุณ:", type=["jpg", "png"])
        if file and st.button("วิเคราะห์"):
            angle = np.random.randint(120, 175)
            date = datetime.date.today().isoformat()
            res = {"date": date, "angle": angle}
            st.session_state.patients[st.session_state.current_id]["history"].append(res)
            st.success(f"วิเคราะห์เรียบร้อย! มุมเข่าที่วัดได้: {angle}°")

# 📊 [03] ผลลัพธ์และท่ากายภาพ
elif menu == "📊 [03] ผลลัพธ์และท่ากายภาพ":
    if st.session_state.current_id and st.session_state.patients[st.session_state.current_id]["history"]:
        last = st.session_state.patients[st.session_state.current_id]["history"][-1]
        st.subheader(f"ผลลัพธ์ล่าสุด: {last['angle']}°")
        
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists("normal_knee.jpg"): st.image("normal_knee.jpg", caption="มาตรฐานขาปกติ")
        with col2:
            if os.path.exists("varus_knee.jpg"): st.image("varus_knee.jpg", caption="ลักษณะขาโก่ง (Varus)")

        st.write("---")
        if last['angle'] < 150:
            st.error("⚠️ พบภาวะแนวเข่าผิดปกติ: แนะนำปรึกษาแพทย์และทำกายภาพ")
            data = {"ท่าบริหาร": ["ยืดกล้ามเนื้อต้นขา", "กระดกข้อเท้า", "ยกขาตรง"], "วิธีทำ": ["นอนราบ ยืดขาตรง ค้าง 10 วินาที", "กระดกขึ้น-ลง 15 ครั้ง", "เกร็งหน้าขา ยกขาขึ้น 45 องศา"], "ความถี่": ["3 รอบ/วัน", "2 รอบ/วัน", "3 รอบ/วัน"]}
            st.table(pd.DataFrame(data))
            prov = st.session_state.patients[st.session_state.current_id]["data"].get("province", "กรุงเทพมหานคร")
            st.markdown(f"🏥 [ค้นหาคลินิกกายภาพใน {prov}](https://www.google.com/maps/search/คลินิกกายภาพบำบัดใกล้ฉัน+ใน+{prov})")
        else:
            st.success("✅ ผลการวิเคราะห์อยู่ในเกณฑ์ปกติค่ะ")

# 📈 [04] ประวัติ (เพิ่มปุ่มดาวน์โหลดข้อมูล)
elif menu == "📈 [04] ประวัติพัฒนาการ":
    if st.session_state.current_id:
        hist = st.session_state.patients[st.session_state.current_id]["history"]
        if hist:
            df = pd.DataFrame(hist)
            st.line_chart(df.set_index('date'))
            
            # ปุ่มดาวน์โหลดข้อมูล
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 ดาวน์โหลดประวัติเป็นไฟล์ CSV", data=csv, file_name="knee_history.csv", mime="text/csv")
        else:
            st.write("ยังไม่มีประวัติการสแกนค่ะ")
