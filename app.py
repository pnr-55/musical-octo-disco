import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os

st.set_page_config(page_title="Knee AI - Patient System", layout="wide")
st.title("🩺 Knee AI: ระบบคัดกรองข้อมูลคนไข้")

DB_FILE = "patient_data.csv"
if os.path.exists(DB_FILE): 
    df = pd.read_csv(DB_FILE)
else: 
    df = pd.DataFrame(columns=["id", "date", "status"])

uid = st.sidebar.text_input("🔑 รหัสประจำตัวคนไข้:")

if uid:
    st.write(f"สวัสดีคนไข้รหัส: {uid}")
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพเพื่อเก็บข้อมูล:", type=["jpg", "png"])
    
    if uploaded_file and st.button("บันทึกข้อมูลเข้าสู่ระบบ"):
        new_data = pd.DataFrame([{"id": uid, "date": str(datetime.date.today()), "status": "Uploaded"}])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("บันทึกข้อมูลเรียบร้อย! ระบบกำลังอยู่ในช่วงประมวลผลอัตโนมัติ")
else:
    st.info("👈 กรุณากรอกรหัสประจำตัวที่แถบด้านซ้าย")
