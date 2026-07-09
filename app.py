import streamlit as st
import numpy as np
import pandas as pd
import datetime
import os
import time  # เพิ่มเวลาเพื่อหน่วงการทำงานให้สมจริง

# 🎨 ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Knee AI - Telemedicine Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🤖 KNEE-AI: ADVANCED PRO v7.0</h1>", unsafe_allow_html=True)

# 💾 จัดการ Session
if 'patients' not in st.session_state: st.session_state.patients = {}
if 'current_id' not in st.session_state: st.session_state.current_id = None

menu = st.sidebar.radio("SELECT MODE:", ["🧬 [01] ลงทะเบียน", "📷 [02] สแกนเข่า", "📊 [03] ผลลัพธ์/กายภาพ", "📈 [04] ประวัติพัฒนาการ"])

# 🧬 [01] ลงทะเบียน
if menu == "🧬 [01] ลงทะเบียน":
    st.subheader("📝 ระบบลงทะเบียน")
    pid = st.text_input("กรอกรหัสคนไข้ (เช่น 1234):")
    if pid and st.button("เข้าสู่ระบบ"):
        st.session_state.current_id = pid
        if pid not in st.session_state.patients:
            st.session_state.patients[pid] = {"history": [], "data": {"province": "ลพบุรี"}}
            st.success(f"สร้างโปรไฟล์รหัส: {pid}")
        else:
            st.success(f"ยินดีต้อนรับกลับมาค่ะ รหัส: {pid}")

# 📷 [02] สแกนเข่า (ระบบจำลองการประมวลผล)
elif menu == "📷 [02] สแกนเข่า":
    if not st.session_state.current_id: st.warning("กรุณาล็อกอินก่อนค่ะ")
    else:
        file = st.file_uploader("อัปโหลดภาพเข่า (จุดอ้างอิงสติกเกอร์):", type=["jpg", "png"])
        if file and st.button("วิเคราะห์ผล"):
            with st.spinner('กำลังประมวลผลภาพและตรวจจับจุดอ้างอิง (Fiducial Markers)...'):
                time.sleep(3) # จำลองเวลาประมวลผล 3 วินาที
                angle = np.random.choice([135, 142, 168, 172]) # ค่าที่สมจริง
                date = datetime.date.today().isoformat()
                st.session_state.patients[st.session_state.current_id]["history"].append({"date": date, "angle": angle})
                st.success(f"วิเคราะห์เรียบร้อย! มุมเข่าที่คำนวณได้คือ {angle}°")

# 📊 [03] ผลลัพธ์/กายภาพ
elif menu == "📊 [03] ผลลัพธ์/กายภาพ":
    if st.session_state.current_id and st.session_state.patients[st.session_state.current_id]["history"]:
        last = st.session_state.patients[st.session_state.current_id]["history"][-1]
        st.subheader(f"ผลการวิเคราะห์ล่าสุด: {last['angle']}°")
        
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists("normal_knee.jpg"): st.image("normal_knee.jpg", caption="มาตรฐานขาปกติ")
        with col2:
            if os.path.exists("varus_knee.jpg"): st.image("varus_knee.jpg", caption="ลักษณะขาโก่ง (Varus)")
        
        if last['angle'] < 150:
            st.error("⚠️ พบภาวะแนวเข่าผิดปกติ: แนะนำกายภาพบำบัด")
            st.table(pd.DataFrame({
                "ท่าบริหาร": ["ยืดกล้ามเนื้อต้นขา", "กระดกข้อเท้า", "ยกขาตรง"],
                "ความถี่": ["3 รอบ/วัน", "2 รอบ/วัน", "3 รอบ/วัน"]
            }))
            st.markdown("🏥 [ค้นหาคลินิกใกล้ฉันในลพบุรี](https://www.google.com/maps/search/คลินิกกายภาพบำบัดใกล้ฉัน+ใน+ลพบุรี)")
        else:
            st.success("✅ แนวเข่าปกติอยู่ในเกณฑ์มาตรฐาน")

# 📈 [04] ประวัติ
elif menu == "📈 [04] ประวัติพัฒนาการ":
    if st.session_state.current_id:
        hist = st.session_state.patients[st.session_state.current_id]["history"]
        if hist:
            df = pd.DataFrame(hist)
            st.line_chart(df.set_index('date'))
            st.download_button("📥 ดาวน์โหลดประวัติ CSV", data=df.to_csv().encode('utf-8'), file_name="history.csv")
