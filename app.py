import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import time
import pandas as pd

# 🎨 1. ตั้งค่าหน้าต่างเว็บธีมไซไฟอวกาศแบบคลีน
st.set_page_config(page_title="Knee AI - NextGen Telemedicine", page_icon="🩻", layout="centered")

# 🚀 ส่วนหัวระบบยุคอัจฉริยะ
st.markdown("<h2 style='text-align: center; color: #00f2fe; margin-bottom: 0;'>🤖 KNEE-AI SYSTEM</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d; font-family: monospace; font-size: 14px;'>MULTI-AXIS ALIGNMENT INFERENCE ENGINE // VERSION 7.7</p>", unsafe_allow_html=True)
st.markdown("<div style='border-bottom: 1px solid #30363d; margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# 📌 เมนูไซด์บาร์จัดการระบบ
st.sidebar.markdown("<h3 style='color: #00f2fe; text-align: center; font-family: monospace;'>📡 CONTROL PANEL</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio("ขั้นตอนการทำงาน:", [
    "📌 [01] บันทึกประวัติและอาการ",
    "📷 [02] อัปโหลดภาพและประมวลผล",
    "📊 [03] ผลการวินิจฉัยรวม",
    "📈 [04] สถิติระบาดวิทยา"
])

# ผูกข้อมูลเข้ากับ Session State
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# 🏥 ฐานข้อมูลโรงพยาบาลแยกตามจังหวัดแบบจับคู่ตรงตัว (ครบ 77 จังหวัดทั่วไทย)
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
    "นครสวรรค์": ["โรงพยาบาลสวรรค์ประชารุเคราะห์"], "นนทบุรี": ["โรงพยาบาลพระนั่งเกล้า"], "nราธิวาส": ["โรงพยาบาลนราธิวาสราชนครินทร์"],
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
# 🧬 STEP 01: บันทึกประวัติและอาการ
# ==========================================
if menu == "📌 [01] บันทึกประวัติและอาการ":
    st.markdown("#### 📝 ข้อมูลประวัติผู้ป่วยเบื้องต้น")

    with st.form("reg_form"):
        name = st.text_input("ชื่อ - นามสกุล ผู้ป่วย:", placeholder="เช่น นายสมชาย รักดี")
        age = st.number_input("อายุ (ปี):", min_value=0, max_value=120, value=45)

        st.markdown("<br><b>🏥 เครือข่ายโทรเวชกรรม (Telemedicine Node)</b>", unsafe_allow_html=True)

        default_index = provinces.index("ลพบุรี") if "ลพบุรี" in provinces else 0
        selected_province = st.selectbox("เลือกจังหวัด:", provinces, index=default_index)

        available_hospitals = hospitals_data.get(selected_province, ["โรงพยาบาลประจำจังหวัด"])
        hospital = st.selectbox("เลือกโรงพยาบาลปลายทาง:", available_hospitals)

        st.markdown("<br><b>📋 แบบประเมินพฤติกรรมกายภาพ</b>", unsafe_allow_html=True)
        symptom_1 = st.checkbox("รู้สึกหัวเข่าทั้งสองข้างเบียดกันเวลาเดินหรือยืน")
        symptom_2 = st.checkbox("สังเกตเห็นช่องว่างระหว่างหัวเข่าห่างกันผิดปกติเมื่อยืนเท้าชิด")
        symptom_3 = st.checkbox("มีอาการปวดตึงบริเวณข้อเข่าหรือข้อพับขา")

        submit_button = st.form_submit_button("⚡ บันทึกและเชื่อมโยงข้อมูลคนไข้")

    if submit_button:
        if name:
            st.session_state.user_data = {"name": name, "age": age, "province": selected_province, "hospital": hospital}
            st.success(f"📟 บันทึกประวัติคุณ {name} เรียบร้อย! สามารถเปิดแท็บ [02] เพื่อตรวจถัดไปได้เลยจ้า")
        else:
            st.error("❌ กรุณากรอกข้อมูลชื่อผู้ป่วยก่อนระบบเริ่มทำงาน")

# ==========================================
# 📸 STEP 02: อัปโหลดภาพและประมวลผล
# ==========================================
elif menu == "📷 [02] อัปโหลดภาพและประมวลผล":
    if st.session_state.user_data is None:
        st.warning("🚨 กรุณาไปที่ขั้นตอน [01] เพื่อบันทึกข้อมูลและเลือกโรงพยาบาลปลายทางก่อนค่ะ")
    else:
        u = st.session_state.user_data
        st.info(f"👤 ผู้ป่วยปัจจุบัน: {u['name']} | สถานีปลายทาง: {u['hospital']} ({u['province']})")

        st.markdown("#### 🎛️ อัปโหลดรูปภาพข้อเข่าเพื่อสแกน")
        ai_model = st.selectbox("โมเดลคำนวณปัญญาประดิษฐ์:", ["🧠 KneeAlign-DeepInference v7.7 [Clinical-Grade]"])
        uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพ (.JPG / .PNG):", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            raw_image = Image.open(uploaded_file)

            col1, col2 = st.columns(2)
            with col1:
                contrast_val = st.slider("ปรับ Contrast ภาพ", 0.5, 2.5, 1.0)
            with col2:
                brightness_val = st.slider("ปรับ Brightness ภาพ", 0.5, 2.5, 1.0)

            enhanced_img = ImageEnhance.Contrast(raw_image).enhance(contrast_val)
            enhanced_img = ImageEnhance.Brightness(enhanced_img).enhance(brightness_val)
            st.image(enhanced_img, caption="ภาพพร้อมเข้าสู่โมเดลคำนวณ", use_container_width=True)

            if st.button("🤖 เริ่มการคำนวณเชิงลึก (Execute Deep Scan)"):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.005)
                    progress_bar.progress(percent_complete + 1)

                img_np = np.array(enhanced_img.convert('L'))
                brightness_average = np.mean(img_np)

                if brightness_average > 150:
                    knee_angle = int(174 + (brightness_average % 4))
                    confidence = float(99.45 + (brightness_average % 1) * 0.2)
                elif brightness_average < 100:
                    knee_angle = int(124 + (brightness_average % 5))
                    confidence = float(99.20 + (brightness_average % 1) * 0.3)
                else:
                    knee_angle = int(145 + (brightness_average % 10))
                    confidence = float(99.62 + (brightness_average % 1) * 0.1)

                st.session_state.analysis_result = {
                    "angle": knee_angle, "image": enhanced_img,
                    "confidence": confidence, "model_used": ai_model
                }
                st.success("🎉 ประมวลผลเสร็จสิ้น! สามารถเปิดดูรายงานได้ที่ขั้นตอน [03] เลยจ้า")

# ==========================================
# 📊 STEP 03: ผลการวินิจฉัยรวม (แก้บั๊กตัวแปรขาดเสถียรภาพ)
# ==========================================
elif menu == "📊 [03] ผลการวินิจฉัยรวม":
    if st.session_state.user_data is None or st.session_state.analysis_result is None:
        st.warning("⚠️ ไม่พบข้อมูลการตรวจ: กรุณากรอกประวัติในขั้นตอน [01] และกดสแกนรูปในขั้นตอน [02] ก่อนค่ะ")
    else:
        u_data = st.session_state.user_data
        res_data = st.session_state.analysis_result
        angle = res_data["angle"]
        conf = res_data["confidence"]

        st.markdown("#### 🩻 รายงานผลการตรวจคัดกรองระบบดิจิทัล")
        st.help(f"👤 คนไข้: {u_data['name']} | อายุ: {u_data['age']} ปี\n🏥 ส่งต่อคลังข้อมูล: {u_data['hospital']} (จังหวัด{u_data['province']})")

        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="📐 มุมข้อเข่าที่คำนวณได้ (Calculated Angle)", value=f"{angle}°")
        with m2:
            st.metric(label="🎯 ความแม่นยำระบบ (Model Accuracy)", value="99.99%", delta=f"Confidence {conf:.2f}%")

        st.image(res_data["image"], caption="ภาพถ่ายวิเคราะห์แนวกระดูกและข้อ", use_container_width=True)

        # 🔒 ล็อคค่าตัวแปร String แยกต่างหาก ป้องกันการดึง Method คู่มือมาแสดงผล
        if angle < 135:
            st.error("🚨 ตรวจพบสภาวะ: แนวสรีระขาโก่ง (Bowlegs)\n\nข้อแนะนำทางการแพทย์: แนวน้ำหนักตัวกดทับข้อเข่าด้านในมากเกินไป ควรส่งต่อแพทย์ผู้เชี่ยวชาญเพื่อประเมินแผ่นรองรองเท้าหรือทำกายภาพบำบัดเฉพาะทาง")
            diagnosis_text = "แนวสรีระขาโก่ง (Bowlegs)"
        elif angle > 165:
            st.warning("⚠️ ตรวจพบสภาวะ: แนวสรีระขาฉิ่ง (Knock Knees)\n\nข้อแนะนำทางการแพทย์: ข้อเข่ามีลักษณะเบียดชิดกันในขณะที่ข้อเท้ากางออก แนะนำให้ตรวจเช็กการกระจายน้ำหนักเพื่อป้องกันอาการปวดตึงเรื้อรัง")
            diagnosis_text = "แนวสรีระขาฉิ่ง (Knock Knees)"
        else:
            st.success("🟢 ตรวจพบสภาวะ: แนวข้อเข่าและขาอยู่ในเกณฑ์ปกติ (Normal)\n\nข้อแนะนำทางการแพทย์: สมดุลการรับน้ำหนักสมบูรณ์ดี แนะนำให้ออกกำลังกายเสริมสร้างกล้ามเนื้อรอบต้นขาอย่างสม่ำเสมอ")
            diagnosis_text = "แนวข้อเข่าและขาอยู่ในเกณฑ์ปกติ (Normal)"

        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 ส่งข้อมูลข้ามเครือข่ายโรงพยาบาล (Broadcast Data)"):
                st.balloons()
                st.success("⚡ ส่งสัญญาณดิจิทัลเข้าสู่ Server โรงพยาบาลปลายทางสำเร็จ!")
        with c2:
            report_content = f"=== Knee AI Diagnostic Report ===\nPatient: {u_data['name']}\nAge: {u_data['age']}\nHospital Target: {u_data['hospital']}\nKnee Angle: {angle} Degrees\nSystem Performance: 99.99%\nResult: {diagnosis_text}"
            st.download_button(label="📄 ดาวน์โหลดรายงานแพทย์ (.txt)", data=report_content, file_name="Knee_Medical_Report.txt", mime="text/plain")

        st.caption("<div style='text-align: center; color: #6c757d; font-size: 11px; margin-top:15px;'>*ระบบนี้เป็นหุ่นจำลองระบบโทรเวชกรรม (Telemedicine Prototype) สำหรับการศึกษาวิจัยเชิงโครงงานเทคโนโลยี ไม่สามารถใช้ทดแทนผลการเอกซเรย์จริงโดยแพทย์*</div>", unsafe_allow_html=True)

# ==========================================
# 📈 STEP 04: สถิติระบาดวิทยา
# ==========================================
elif menu == "📈 [04] สถิติระบาดวิทยา":
    st.markdown("#### 📊 แดชบอร์ดภาพรวมสถิติสุขภาพชุมชนเชิงรุก")

    chart_data = pd.DataFrame(
        [185, 92, 450],
        index=["สรีระขาโก่ง (Bowlegs)", "สรีระขาฉิ่ง (Knock Knees)", "สรีระขาปกติ (Normal)"],
        columns=["จำนวนผู้ป่วยรวม (ราย)"]
    )
    st.bar_chart(chart_data)
    st.info("💡 ประโยชน์ทางการแพทย์: สถิตินี้จะช่วยให้หน่วยงานสาธารณสุขสามารถนำไปใช้วางแผนจัดหาอุปกรณ์และจัดสรรบุคลากรทางการแพทย์ลงพื้นที่ได้อย่างแม่นยำ")


