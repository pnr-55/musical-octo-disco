import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Knee AI - Comprehensive System", layout="wide")
st.title("🩺 Knee AI: ระบบประเมินและติดตามสุขภาพเข่า")

# 1. โหลดข้อมูล
USER_FILE = "user_profiles.csv"
HIST_FILE = "knee_history.csv"

def load_data(f, cols): return pd.read_csv(f) if os.path.exists(f) else pd.DataFrame(columns=cols)

user_df = load_data(USER_FILE, ["id", "name", "age", "province"])
hist_df = load_data(HIST_FILE, ["id", "date", "angle", "status"])

uid = st.sidebar.text_input("🔑 รหัสคนไข้:")

if uid:
    # 2. จัดการข้อมูลส่วนตัว
    user_info = user_df[user_df['id'] == uid]
    if user_info.empty:
        with st.form("register"):
            name = st.text_input("ชื่อ-นามสกุล")
            age = st.number_input("อายุ", 1, 100)
            province = st.text_input("จังหวัด")
            if st.form_submit_button("บันทึกข้อมูล"):
                new_user = pd.DataFrame([{"id": uid, "name": name, "age": age, "province": province}])
                pd.concat([user_df, new_user]).to_csv(USER_FILE, index=False)
                st.rerun()
    else:
        info = user_info.iloc[0]
        st.write(f"### สวัสดีคุณ {info['name']} (อายุ {info['age']} ปี | จ.{info['province']})")
        
        # 3. ส่วนวิเคราะห์รูปภาพ
        uploaded_file = st.file_uploader("อัปโหลดรูปเข่า:", type=["jpg", "png"])
        if uploaded_file:
            # (จำลองการวิเคราะห์ AI)
            angle = st.slider("องศาเข่าที่วัดได้ (จำลอง):", 150, 180, 170)
            is_varus = angle < 170
            
            st.subheader("📊 ผลการวิเคราะห์เบื้องต้น")
            if is_varus:
                st.error("พบสัญญาณเข่าโก่ง! เสี่ยงข้อเข่าเสื่อม")
                st.write("📋 **คำแนะนำ:** ทำกายภาพท่า Knee Extension และลดการลงน้ำหนัก")
                st.write(f"🏥 **คลินิกใกล้บ้าน:** รพ.ประจำจังหวัด{info['province']} หรือคลินิกกายภาพใกล้บ้าน")
            else:
                st.success("เข่าปกติครับ")
            
            if st.button("บันทึกผลการวิเคราะห์นี้"):
                new_hist = pd.DataFrame([{"id": uid, "date": str(datetime.date.today()), "angle": angle, "status": "วิเคราะห์แล้ว"}])
                pd.concat([hist_df, new_hist]).to_csv(HIST_FILE, index=False)
                st.success("บันทึกผลสำเร็จ!")

        # 4. ดูสถิติย้อนหลัง
        st.subheader("📈 สถิติพัฒนาการ")
        user_hist = hist_df[hist_df['id'] == uid]
        if not user_hist.empty:
            st.line_chart(user_hist.set_index('date')['angle'])
            st.table(user_hist)
else:
    st.info("👈 กรุณากรอกรหัสประจำตัว")
