import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Knee AI - Personal Data", layout="wide")
st.title("🩺 Knee AI: ระบบเก็บข้อมูลคนไข้")

# ไฟล์เก็บข้อมูล 2 ส่วน
USER_FILE = "user_profiles.csv" # เก็บ ชื่อ อายุ จังหวัด
HISTORY_FILE = "knee_history.csv" # เก็บ ประวัติการวัดค่าเข่า

# ฟังก์ชันโหลดไฟล์
def load_data(file, columns):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=columns)

user_df = load_data(USER_FILE, ["id", "name", "age", "province"])
hist_df = load_data(HISTORY_FILE, ["id", "date", "angle"])

# ส่วนการเข้าใช้งาน
uid = st.sidebar.text_input("🔑 กรอกรหัสประจำตัว (UID):")

if uid:
    # ตรวจสอบว่าเคยลงทะเบียนหรือยัง
    user_info = user_df[user_df['id'] == uid]
    
    if user_info.empty:
        st.subheader("📝 ลงทะเบียนครั้งแรก")
        with st.form("register_form"):
            name = st.text_input("ชื่อ-นามสกุล")
            age = st.number_input("อายุ", min_value=1, max_value=100)
            province = st.text_input("จังหวัด")
            submitted = st.form_submit_button("ลงทะเบียน")
            if submitted:
                new_user = pd.DataFrame([{"id": uid, "name": name, "age": age, "province": province}])
                user_df = pd.concat([user_df, new_user], ignore_index=True)
                user_df.to_csv(USER_FILE, index=False)
                st.success("ลงทะเบียนสำเร็จ! กรุณารีเฟรชหน้าจอ")
    else:
        # ถ้าเคยลงทะเบียนแล้ว ดึงข้อมูลเก่ามาโชว์
        info = user_info.iloc[0]
        st.write(f"### สวัสดีคุณ {info['name']}")
        st.write(f"อายุ: {info['age']} ปี | จังหวัด: {info['province']}")
        
        st.write("---")
        st.subheader("📸 อัปโหลดรูปภาพเพื่อประเมินเข่า")
        # ตรงนี้ปายสามารถใส่ฟังก์ชันอัปโหลดรูปและคำนวณได้เลย
        st.info("ระบบพร้อมประเมินเบื้องต้นแล้ว (คำเตือน: เป็นการประเมินเบื้องต้นเท่านั้น)")
else:
    st.info("👈 กรุณากรอกรหัสประจำตัวในแถบด้านซ้ายเพื่อเริ่มระบบ")
