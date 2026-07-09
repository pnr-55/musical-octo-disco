import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Knee AI - Pro Version", layout="centered")
st.title("🩺 Knee AI: ระบบวิเคราะห์เข่าอัจฉริยะ")

DB_FILE = "patient_data.csv"
def load_data():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["id", "name", "weight", "height", "prov", "date", "angle"])

# 🔑 Sidebar ล็อกอิน
uid = st.sidebar.text_input("🔑 รหัสประจำตัวคนไข้ (4 หลัก):")

if uid:
    df = load_data()
    user_info = df[df['id'] == uid]
    
    # 📝 ข้อมูลคนไข้
    with st.expander("👤 ข้อมูลส่วนตัว (คลิกเพื่อแก้ไข)"):
        with st.form("profile_form"):
            name = st.text_input("ชื่อ-นามสกุล", value=user_info['name'].iloc[-1] if not user_info.empty else "")
            col1, col2 = st.columns(2)
            weight = col1.number_input("น้ำหนัก (kg)", value=float(user_info['weight'].iloc[-1]) if not user_info.empty else 60.0)
            height = col2.number_input("ส่วนสูง (cm)", value=float(user_info['height'].iloc[-1]) if not user_info.empty else 160.0)
            prov = st.text_input("จังหวัด", value=user_info['prov'].iloc[-1] if not user_info.empty else "")
            submit_p = st.form_submit_button("บันทึกข้อมูล")

    # 📷 ส่วนการอัปโหลดภาพเพื่อวิเคราะห์
    st.header("📷 อัปโหลดรูปภาพเพื่อวิเคราะห์")
    uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพเข่าของคุณ (JPG/PNG):", type=["jpg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="รูปภาพที่อัปโหลด", use_container_width=True)
        angle = st.number_input("กรอกองศาเข่าที่วัดได้ (จากการวิเคราะห์ในรูป):", min_value=0, max_value=180)
        
        if st.button("ประมวลผลและออกใบรับรอง"):
            new_row = {"id": uid, "name": name, "weight": weight, "height": height, "prov": prov, 
                       "date": str(datetime.date.today()), "angle": angle}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("บันทึกข้อมูลและวิเคราะห์เรียบร้อย!")

            # 📜 ใบรับรองผล
            st.markdown("---")
            st.subheader("📜 ใบรับรองผลการคัดกรองเบื้องต้น")
            report = f"""
            **ชื่อ:** {name} | **วันที่:** {datetime.date.today()}
            **ผลการวิเคราะห์:** มุมเข่า {angle}° 
            **คำแนะนำ:** {'พบความผิดปกติ ควรพบแพทย์กายภาพ' if angle < 160 else 'แนวเข่าปกติ สุขภาพดีเยี่ยม'}
            **โรงพยาบาล/คลินิกแนะนำใน {prov}:** 
            https://www.google.com/maps/search/โรงพยาบาลใกล้ฉัน+ใน+{prov}
            """
            st.info(report)
            st.download_button("📥 ดาวน์โหลดใบรับรองผล (.txt)", report, file_name="Medical_Report.txt")

    # 📈 กราฟประวัติ
    st.header("📈 ประวัติพัฒนาการ")
    user_history = df[df['id'] == uid]
    if not user_history.empty:
        st.line_chart(user_history.set_index('date')['angle'])
else:
    st.info("👈 กรุณากรอกรหัสประจำตัวที่แถบด้านข้าง เพื่อเริ่มใช้งานระบบวิเคราะห์ค่ะ")
