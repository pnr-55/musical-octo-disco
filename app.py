import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os

st.set_page_config(page_title="Knee AI - Patient Record", layout="wide")
st.title("🩺 Knee AI: ระบบติดตามและสรุปผลคนไข้")

DB_FILE = "patient_data.csv"
if os.path.exists(DB_FILE): df = pd.read_csv(DB_FILE)
else: df = pd.DataFrame(columns=["id", "date", "angle"])

uid = st.sidebar.text_input("🔑 กรอกรหัสประจำตัวคนไข้:")

if uid:
    st.subheader(f"ประวัติการรักษาของ: {uid}")
    
    # ส่วนกรอกข้อมูลใหม่
    new_angle = st.number_input("กรอกองศาที่วัดได้ล่าสุด (°):", min_value=0.0, max_value=180.0)
    if st.button("บันทึกข้อมูลและดูผลสรุป"):
        new_data = pd.DataFrame([{"id": uid, "date": str(datetime.date.today()), "angle": new_angle}])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("บันทึกข้อมูลเรียบร้อย!")

    # สรุปผลจากข้อมูล
    user_hist = df[df['id'] == uid]
    if len(user_hist) >= 2:
        last = user_hist.iloc[-1]['angle']
        prev = user_hist.iloc[-2]['angle']
        diff = prev - last
        
        st.write("---")
        st.subheader("📊 สรุปพัฒนาการ")
        if diff > 0:
            st.success(f"ดีขึ้นค่ะ! มุมเปลี่ยนไปในทางที่ดีขึ้น {abs(diff):.2f}°")
        else:
            st.warning(f"ต้องระวังนะคะ มุมเปลี่ยนไป {abs(diff):.2f}° จากครั้งก่อน")
        
        st.line_chart(user_hist.set_index('date')['angle'])
    else:
        st.info("กรอกข้อมูลอย่างน้อย 2 ครั้ง เพื่อให้ระบบสรุปผลนะคะ")
else:
    st.info("👈 กรุณากรอกรหัสประจำตัวในแถบด้านซ้าย")
