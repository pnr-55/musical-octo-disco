import streamlit as st
import pandas as pd
import datetime
import os

# 🎨 ตั้งค่า UI สวยงาม
st.set_page_config(page_title="Knee AI - Health Report", layout="centered")
st.title("🏥 Knee AI: ระบบคัดกรองสุขภาพเข่า")

# ฟังก์ชันจัดการไฟล์ CSV เพื่อให้ข้อมูลอยู่ถาวร
DB_FILE = "patient_data.csv"
def load_data():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["id", "name", "weight", "height", "prov", "date", "angle"])

# [STEP 1] ล็อกอินและลงทะเบียน
uid = st.sidebar.text_input("🔑 รหัสประจำตัวคนไข้ (4 หลัก):")
if uid:
    st.sidebar.success(f"เข้าสู่ระบบด้วยรหัส: {uid}")
    df = load_data()
    
    # ดูว่าเคยมีข้อมูลไหม
    user_info = df[df['id'] == uid]
    
    st.header("📝 ข้อมูลคนไข้")
    with st.form("profile_form"):
        name = st.text_input("ชื่อ-นามสกุล", value=user_info['name'].iloc[0] if not user_info.empty else "")
        col1, col2 = st.columns(2)
        weight = col1.number_input("น้ำหนัก (kg)", value=float(user_info['weight'].iloc[-1]) if not user_info.empty else 60.0)
        height = col2.number_input("ส่วนสูง (cm)", value=float(user_info['height'].iloc[-1]) if not user_info.empty else 160.0)
        prov = st.text_input("จังหวัด", value=user_info['prov'].iloc[0] if not user_info.empty else "")
        submit_p = st.form_submit_button("บันทึกข้อมูล")

    # [STEP 2] วิเคราะห์เข่า
    st.header("📷 วิเคราะห์องศาเข่า")
    angle = st.number_input("กรอกองศาเข่าที่วัดได้:", min_value=0, max_value=180)
    if st.button("ประมวลผลและออกใบรับรอง"):
        new_row = {"id": uid, "name": name, "weight": weight, "height": height, "prov": prov, 
                   "date": str(datetime.date.today()), "angle": angle}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("บันทึกข้อมูลเรียบร้อย!")

        # [STEP 3] ออกใบรับรองเบื้องต้น
        st.markdown("---")
        st.subheader("📜 ใบรับรองผลการคัดกรองเบื้องต้น")
        report = f"""
        **ชื่อ:** {name} | **วันที่:** {datetime.date.today()}
        **ผลการวิเคราะห์:** มุมเข่า {angle}° 
        **คำแนะนำ:** {'พบความผิดปกติ ควรพบแพทย์' if angle < 160 else 'แนวเข่าปกติ'}
        **สถานพยาบาลแนะนำ:** [คลิกดูโรงพยาบาลใน {prov}](https://www.google.com/maps/search/โรงพยาบาลใกล้ฉัน+ใน+{prov})
        """
        st.info(report)
        st.download_button("📥 ดาวน์โหลดใบรับรองผล (.txt)", report, file_name="Medical_Report.txt")

    # [STEP 4] ดูสถิติพัฒนาการ
    st.header("📈 กราฟประวัติพัฒนาการ")
    user_history = df[df['id'] == uid]
    if not user_history.empty:
        st.line_chart(user_history.set_index('date')['angle'])
else:
    st.info("กรุณากรอกรหัส 4 หลักที่แถบด้านข้างเพื่อเริ่มใช้งานค่ะ")
