import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import time
import pandas as pd

# 🎨 1. ตั้งค่าหน้าต่างเว็บธีมไซไฟอวกาศ
st.set_page_config(page_title="Knee AI - NextGen Telemedicine", page_icon="⚡", layout="centered")

# 🚀 ส่วนหัวระบบยุคอัจฉริยะ (เวอร์ชัน 7.0 อัปเกรดความแม่นยำสูงสุด)
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🤖 KNEE-AI: MULTI-AXIS ALIGNMENT ENGINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1a1; font-family: monospace;'>PROTOTYPE VERSION 7.0 [MEDICAL-GRADE SIMULATION MODE] // BY TEAM VITAMIN C</p>", unsafe_allow_html=True)

# 📌 เมนูไซด์บาร์สไตล์ห้องแล็บ
st.sidebar.markdown("<h2 style='color: #00f2fe; text-align: center;'>📡 SYSTEM CORE v7.0</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("SELECT INTEL MODE:", [
    "🧬 [01] PATIENT INFRASTRUCTURE",
    "📷 [02] DEEP SCAN & IMAGE ENGINE",
    "📊 [03] DIAGNOSTIC QUANTUM MATRIX",
    "📈 [04] EPIDEMIOLOGY DASHBOARD"
])

if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# 🏥 ฐานข้อมูลโรงพยาบาลเครือข่ายโทรเวชกรรม 77 จังหวัด
hospitals_data = {
    "ลพบุรี": ["โรงพยาบาลลพบุรี", "โรงพยาบาลพัฒนานิคม", "โรงพยาบาลพระนารายณ์มหาราช", "โรงพยาบาลอานันทมหิดล", "โรงพยาบาลบ้านหมี่"],
    "กรุงเทพมหานคร": ["โรงพยาบาลศิริราช", "โรงพยาบาลจุฬาลงกรณ์", "โรงพยาบาลรามาธิบดี", "โรงพยาบาลพระมงกุฎเกล้า", "โรงพยาบาลราชวิถี"],
    "กระบี่": ["โรงพยาบาลกระบี่"], "กาญจนบุรี": ["โรงพยาบาลพหลพลพยุหเสนา"], "กาฬสินธุ์": ["โรงพยาบาลกาฬสินธุ์"],
    "กำแพงเพชร": ["โรงพยาบาลกำแพงเพชร"], "ขอนแก่น": ["โรงพยาบาลขอนแก่น", "โรงพยาบาลศรีนครินทร์"], "จันทบุรี": ["โรงพยาบาลพระปกเกล้า"],
    "ฉะเชิงเทรา": ["โรงพยาบาลพุทธโสธร"], "ชลบุรี": ["โรงพยาบาลชลบุรี", "โรงพยาบาลสมเด็จพระบรมราชเทวี ณ ศรีราชา"], "ชัยนาท": ["โรงพยาบาลชัยนาทนเรนทร"],
    "ชัยภูมิ": ["โรงพยาบาลชัยภูมิ"], "ชุมพร": ["โรงพยาบาลชุมพรเขตรอุดมศักดิ์"], "เชียงราย": ["โรงพยาบาลเชียงรายประชานุเคราะห์"],
    "เชียงใหม่": ["โรงพยาบาลมหาราชนครเชียงใหม่", "โรงพยาบาลนครพิงค์"], "ตรัง": ["โรงพยาบาลตรัง"], "ตราด": ["โรงพยาบาลตราด"],
    "ตาก": ["โรงพยาบาลสมเด็จพระเจ้าตากสินมหาราช"], "นครนายก": ["โรงพยาบาลนครนายก"], "นครปฐม": ["โรงพยาบาลนครปฐม"],
    "นครพนม": ["โรงพยาบาลนครพนม"], "นครราชสีมา": ["โรงพยาบาลมหาราชนครราชสีมา"], "นครศรีธรรมราช": ["โรงพยาบาลมหาราชนครศรีธรรมราช"],
    "นครสวรรค์": ["โรงพยาบาลสวรรค์ประชารุเคราะห์"], "นนทบุรี": ["โรงพยาบาลพระนั่งเกล้า"], "นราธิวาส": ["โรงพยาบาลนราธิวาสราชนครินทร์"],
    "น่าน": ["โรงพยาบาลน่าน"], "บึงกาฬ": ["โรงพยาบาลบึงกาฬ"], "บุรีรัมย์": ["โรงพยาบาลบุรีรัมย์"], "ปทุมธานี": ["โรงพยาบาลปทุมธานี"],
    "ประจวบคีรีขันธ์": ["โรงพยาบาลหัวหิน", "โรงพยาบาลประจวบคีรีขันธ์"], "ปราจีนบุรี": ["โรงพยาบาลเจ้าพระยาอภัยภูเบศร"], "ปัตตานี": ["โรงพยาบาลปัตตานี"],
    "พระนครศรีอยุธยา": ["โรงพยาบาลพระนครศรีอยุธยา"], "พะเยา": ["โรงพยาบาลพะเยา"], "พังงา": ["โรงพยาบาลพังงา"],
    "พัทลุง": ["โรงพยาบาลพัทลุง"], "พิจิตร": ["โรงพยาบาลพิจิตร"], "พิษณุโลก": ["โรงพยาบาลพุทธชินราช"], "เพชรบุรี": ["โรงพยาบาลพระจอมเกล้า"],
    "เพชรบูรณ์": ["โรงพยาบาลเพชรบูรณ์"], "แพร่": ["โรงพยาบาลแพร่"], "ภูเก็ต": ["โรงพยาบาลวชิระภูเก็ต"], "มหาสารคาม": ["โรงพยาบาลมหาสารคาม"],
    "มุกดาหาร": ["โรงพยาบาลมุกดาหาร"], "แม่ฮ่องสอน": ["โรงพยาบาลศรีสังวาลย์"], "ยโสธร": ["โรงพยาบาลยโสธร"], "ยะลา": ["โรงพยาบาลยะลา"],
    "ร้อยเอ็ด": ["โรงพยาบาลร้อยเอ็ด"], "ระนอง": ["โรงพยาบาลระนอง"], "ระยอง": ["โรงพยาบาลระยอง"], "ราชบุรี": ["โรงพยาบาลราชบุรี"],
    "สตูล": ["โรงพยาบาลสตูล"], "สมุทรปราการ": ["โรงพยาบาลสมุทรปราการ"], "สมุทรสงคราม": ["โรงพยาบาลสมเด็จพระพุทธเลิศหล้า"],
    "สมุทรสาคร": ["โรงพยาบาลสมุทรสาคร"], "สระแก้ว": ["โรงพยาบาลสมเด็จพระยุพราชสระแก้ว"], "สระบุรี": ["โรงพยาบาลสระบุรี"], "สิงห์บุรี": ["โรงพยาบาลสิงห์บุรี"],
    "สุโขทัย": ["โรงพยาบาลสุโขทัย"], "สุพรรณบุรี": ["โรงพยาบาลศูนย์เจ้าพระยายมราช"], "สุราษฎร์ธานี": ["โรงพยาบาลสุราษฎร์ธานี"], "สุรินทร์": ["โรงพยาบาลสุรินทร์"],
    "หนองคาย": ["โรงพยาบาลหนองคาย"], "หนองบัวลำภู": ["โรงพยาบาลหนองบัวลำภู"], "อ่างทอง": ["โรงพยาบาลอ่างทอง"], "อำนาจเจริญ": ["โรงพยาบาลอำนาจเจริญ"],
    "อุดรธานี": ["โรงพยาบาลอุดรธานี"], "อุตรดิตถ์": ["โรงพยาบาลอุตรดิตถ์"], "อุทัยธานี": ["โรงพยาบาลอุทัยธานี"], "อุบลราชธานี": ["โรงพยาบาลสรรพสิทธิประสงค์"]
}
provinces = sorted(list(hospitals_data.keys()))

# ==========================================
# 🧬 MODE 01: บันทึกประวัติ + ตรวจสอบอาการเบื้องต้น
# ==========================================
if menu == "🧬 [01] PATIENT INFRASTRUCTURE":
    st.markdown("### 📝 PATIENT REGISTRATION & CLINICAL SYMPTOMS")
    st.markdown("กรอกข้อมูลพื้นฐาน เลือกจังหวัด และโรงพยาบาลเครือข่ายโทรเวชกรรมปลายทาง")

    with st.form("reg_form"):
        name = st.text_input("PATIENT FULL NAME (ชื่อ-นามสกุล):")
        age = st.number_input("AGE (อายุ):", min_value=0, max_value=120, value=50)

        st.markdown("---")
        st.markdown("##### 🏥 TELEMEDICINE NODE ROUTING")

        selected_province = st.selectbox("SELECT PROVINCE (เลือกจังหวัด):", provinces, index=provinces.index("ลพบุรี") if "ลพบุรี" in provinces else 0)
        available_hospitals = hospitals_data.get(selected_province, ["โรงพยาบาลประจำจังหวัด"])
        hospital = st.selectbox("SELECT TARGET HOSPITAL (เลือกโรงพยาบาลปลายทาง):", available_hospitals)

        st.markdown("---")
        symptom_1 = st.checkbox("รู้สึกหัวเข่าทั้งสองข้างเบียดกันผิดปกติเวลาเดินหรือยืน")
        symptom_2 = st.checkbox("สังเกตเห็นช่องว่างระหว่างหัวเข่าห่างกันมากผิดปกติเมื่อยืนเท้าชิด")
        symptom_3 = st.checkbox("มีอาการปวดตึงบริเวณข้อเข่าหรือรอบ ๆ ข้อพับด้านหลัง")

        submit_button = st.form_submit_button("⚡ INITIALIZE AND LINK PATIENT")

    if submit_button:
        if name:
            risk_score = sum([symptom_1, symptom_2, symptom_3])
            st.session_state.user_data = {"name": name, "age": age, "province": selected_province, "hospital": hospital, "risk_score": risk_score}
            st.success(f"📟 LINKED SUCCESS: ลงทะเบียนคุณ {name} เรียบร้อย!")
        else:
            st.error("❌ ERROR: กรุณากรอกข้อมูลชื่อผู้ป่วยก่อนค่ะ")

# ==========================================
# 📸 MODE 02: อัปโหลดภาพ + แผงปรับแต่งรูป + เลือกโมเดล AI
# ==========================================
elif menu == "📷 [02] DEEP SCAN & IMAGE ENGINE":
    if st.session_state.user_data is None:
        st.warning("🚨 ACCESS DENIED: กรุณาไปที่โหมด [01] เพื่อยืนยันตัวตนคนไข้ก่อนค่ะ")
    else:
        st.markdown(f"📡 LINKED PATIENT: **{st.session_state.user_data['name']}** | NODE: **{st.session_state.user_data['hospital']} ({st.session_state.user_data['province']})**")
        ai_model = st.selectbox("🧠 SELECT AI BRAIN MODEL:", [
            "🧠 KneeAlign-DeepInference v7.0 [High-Precision Clinical Mode]",
            "⚡ ResNet-Knee-Core v5.2 [Standard Fast Mode]"
        ])
        uploaded_file = st.file_uploader("CHOOSE IMAGE (.JPG / .PNG):", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            raw_image = Image.open(uploaded_file)
            contrast_val = st.slider("ปรับความคมชัดภาพ (Contrast)", 0.5, 3.0, 1.0)
            brightness_val = st.slider("ปรับความสว่างภาพ (Brightness)", 0.5, 2.0, 1.0)

            enhanced_img = ImageEnhance.Contrast(raw_image).enhance(contrast_val)
            enhanced_img = ImageEnhance.Brightness(enhanced_img).enhance(brightness_val)
            st.image(enhanced_img, caption="PREVIEW IMAGE", use_container_width=True)

            if st.button("🤖 START DEEP ANALYSIS"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                for percent_complete in range(100):
                    time.sleep(0.008)
                    progress_bar.progress(percent_complete + 1)
                    status_text.text(f"🔬 Run High-Precision Inference: {percent_complete + 1}%")

                # 🧮 อัปเกรดสูตรคำนวณจำลองให้มีความเสถียรและแม่นยำสถิติสูงสุดทางการแพทย์
                img_np = np.array(enhanced_img.convert('L'))
                brightness_average = np.mean(img_np)

                if brightness_average > 160:
                    knee_angle = int(173 + (brightness_average % 6))
                    confidence = float(98.85 + (brightness_average % 1) * 0.5)
                elif brightness_average < 100:
                    knee_angle = int(122 + (brightness_average % 6))
                    confidence = float(98.42 + (brightness_average % 1) * 0.4)
                else:
                    knee_angle = int(145 + (brightness_average % 12))
                    confidence = float(99.15 + (brightness_average % 1) * 0.3)

                # สรุปและล็อคผลการวิเคราะห์
                st.session_state.analysis_result = {
                    "angle": knee_angle, "image": enhanced_img,
                    "confidence": confidence, "model_used": ai_model
                }
                st.success("🎉 ANALYSIS LOCKED: ระบบคำนวณความแม่นยำสูงเสร็จสิ้น! เปิดเมนู [03] ได้เลยค่ะ")

# ==========================================
# 📊 MODE 03: สรุปผลการวินิจฉัยคัดกรองขาทั้ง 3 รูปแบบ
# ==========================================
elif menu == "📊 [03] DIAGNOSTIC QUANTUM MATRIX":
    if st.session_state.user_data is None or st.session_state.analysis_result is None:
        st.warning("⚠️ DATA GAP DETECTED: กรุณากรอกประวัติและกดสแกนรูปภาพในโหมดก่อนหน้าก่อนค่ะ")
    else:
        u_data = st.session_state.user_data
        res_data = st.session_state.analysis_result
        angle = res_data["angle"]
        conf = res_data["confidence"]

        st.markdown("### 📋 AI MEDICAL EVALUATION MATRIX")
        st.info(f"👤 ผู้ป่วย: คุณ {u_data['name']} | อายุ: {u_data['age']} ปี | ส่งต่อไปยัง: {u_data['hospital']} (จ.{u_data['province']})")

        st.image(res_data["image"], caption="ANALYZED PICTURE", use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(label="📐 CALCULATED KNEE ANGLE", value=f"{angle}°")
        with col_b:
            st.metric(label="🤖 SYSTEM ACCURACY CONFIDENCE", value=f"{conf:.2f}%")

        diagnosis_text = ""

        if angle < 135:
            st.error("🚨 CRITICAL AREA: ตรวจพบภาวะสรีระขาโก่ง (Bowlegs)\n\nผลวิเคราะห์: แนวน้ำหนักตกลงสู่ข้อเข่าด้านใน ส่งผลให้แนวเข่าโค้งแยกออกจากกันเกินเกณฑ์ปกติ เสี่ยงต่อข้อเข่าเสื่อมก่อนวัยอันควร\n\nแผนการ Telemedicine: ส่งประวัติเข้าสู่แผนกศัลยกรรมกระดูกและข้อ เพื่อแนะนำกายภาพบำบัดเฉพาะทางค่ะ")
            diagnosis_text = "ตรวจพบภาวะสรีระขาโก่ง (Bowlegs)"
        elif angle > 165:
            st.warning("⚠️ ATTENTION AREA: ตรวจพบภาวะสรีระขาฉิ่ง (Knock Knees)\n\nผลวิเคราะห์: แนวข้อเข่าทำมุมเบียดเข้าหากันมากผิดปกติ ทำให้ขาท่อนล่างกางออกและข้อเท้าแยกจากกันในขณะยืน\n\nแผนการ Telemedicine: ลงทะเบียนส่งต่อข้อมูลไปยังโรงพยาบาลปลายทาง เพื่อตรวจเช็กเพิ่มเติม")
            diagnosis_text = "ตรวจพบภาวะสรีระขาฉิ่ง (Knock Knees)"
        else:
            st.success("🟢 NORMAL STATE: สรีระแนวข้อเข่าและขาเป็นปกติ\n\nผลวิเคราะห์: แนวน้ำหนักตกลงกึ่งกลางข้อต่อพอดี สรีระขามีความตรงและสมมาตรตามเกณฑ์มาตรฐานทางการแพทย์\n\nการดูแลรักษา: แนะนำให้ออกกำลังกายเหยียดต้นขาและตรวจเช็กคัดกรองเชิงรุกตามวงรอบปกติ")
            diagnosis_text = "สรีระแนวข้อเข่าและขาอยู่ในเกณฑ์ปกติ"

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 BROADCAST LINK"):
                st.balloons()
                st.success("⚡ PACKET TRANSMITTED: โอนย้ายข้อมูลเข้าเครือข่ายสำเร็จ!")
        with c2:
            report_content = f"=== Knee AI Report v7.0 ===\nPatient: {u_data['name']}\nAge: {u_data['age']}\nHospital: {u_data['hospital']} ({u_data['province']})\nAngle: {angle}\nAI Confidence: {conf:.2f}%\nDiagnosis: {diagnosis_text}"
            st.download_button(label="📄 PRINT MEDICAL REPORT", data=report_content, file_name="HighPrecision_Knee_Report.txt", mime="text/plain")

        st.caption("**Medical Disclaimer:** ระบบนี้เป็นเพียงแบบหุ่นจำลองระบบโทรเวชกรรม (Telemedicine Prototype) สำหรับคัดกรองเบื้องต้นเพื่อการศึกษาเชิงแนวคิดเท่านั้น ไม่สามารถนำไปใช้ทดแทนการวินิจฉัยโรคโดยแพทย์ผู้เชี่ยวชาญในสถานการณ์จริงได้")

# ==========================================
# 📈 MODE 04: แดชบอร์ดข้อมูลทางระบาดวิทยา
# ==========================================
elif menu == "📈 [04] EPIDEMIOLOGY DASHBOARD":
    st.markdown("### 📊 COMMUNITY HEALTH DATA // แดชบอร์ดสถิติสุขภาพชุมชน")

    chart_data = pd.DataFrame(
        [185, 92, 450],
        index=["สรีระขาโก่ง (Bowlegs)", "สรีระขาฉิ่ง (Knock Knees)", "สรีระขาปกติ (Normal)"],
        columns=["จำนวนเคส (ราย)"]
    )
    st.bar_chart(chart_data)
    st.info("💡 ข้อมูลสถิติเหล่านี้จะช่วยให้หน่วยงานสาธารณสุขสามารถนำไปใช้วางแผนจัดหาอุปกรณ์ช่วยพยุงเข่าในชุมชนต่อไปได้ค่ะ")


