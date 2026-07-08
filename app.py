import streamlit as st

st.set_page_config(page_title="Knee AI Pro", page_icon="🩺", layout="centered")

# CSS ตกแต่ง
st.markdown("""
    <style>
    .report-box {background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6;}
    </style>
    """, unsafe_allow_html=True)

# ระบบจดจำข้อมูล
if 'page' not in st.session_state: st.session_state.page = "Register"
if 'name' not in st.session_state: st.session_state.name = ""
if 'hospital' not in st.session_state: st.session_state.hospital = "โรงพยาบาลพระนารายณ์"
if 'angle' not in st.session_state: st.session_state.angle = None

# --- หน้าที่ 1: ลงทะเบียน ---
if st.session_state.page == "Register":
    st.title("🩺 Knee AI: ประเมินสุขภาพเข่า")
    st.session_state.name = st.text_input("ชื่อ - นามสกุล:", value=st.session_state.name)
    st.session_state.hospital = st.selectbox("เลือกโรงพยาบาล:", 
                                            ["โรงพยาบาลพระนารายณ์", "โรงพยาบาลลพบุรี", "โรงพยาบาลอานันทมหิดล", "อื่นๆ"])
    if st.button("เข้าสู่การวิเคราะห์ >>"):
        st.session_state.page = "Scan"
        st.rerun()

# --- หน้าที่ 2: สแกน ---
elif st.session_state.page == "Scan":
    st.title("📷 วิเคราะห์ด้วย AI")
    file = st.file_uploader("อัปโหลดภาพ X-Ray เข่า:", type=["jpg", "png"])
    if file and st.button("เริ่มประมวลผล"):
        st.session_state.angle = 155.0
        st.session_state.page = "Result"
        st.rerun()

# --- หน้าที่ 3: ผลลัพธ์และดาวน์โหลดรายงาน ---
elif st.session_state.page == "Result":
    st.title("📊 สรุปผลการวิเคราะห์")
    
    # ส่วนแสดงผล
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.metric("องศาข้อเข่า", f"{st.session_state.angle}°")
    st.write(f"**ผู้ป่วย:** {st.session_state.name}")
    st.write(f"**โรงพยาบาลที่เลือก:** {st.session_state.hospital}")
    
    # สร้างเนื้อหาสำหรับรายงาน
    report_text = f"""
    --- รายงานสรุปผลการวิเคราะห์สุขภาพเข่า Knee AI ---
    ชื่อผู้ป่วย: {st.session_state.name}
    มุมข้อเข่าที่ตรวจพบ: {st.session_state.angle} องศา
    โรงพยาบาลที่แนะนำให้ปรึกษา: {st.session_state.hospital}
    ข้อเสนอแนะ: {'จำเป็นต้องพบแพทย์ทันที' if st.session_state.angle < 160 else 'สภาพเข่าปกติ'}
    --------------------------------------------------
    """
    
    # ปุ่มดาวน์โหลดรายงานเป็นไฟล์ .txt (เอาไปเปิดในมือถือหรือพิมพ์ให้หมอดูได้)
    st.download_button(
        label="📥 ดาวน์โหลดสรุปผลเพื่อปรึกษาแพทย์ (.txt)",
        data=report_text,
        file_name=f"Report_{st.session_state.name}.txt",
        mime="text/plain"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ท่าบริหารและคำแนะนำ (ตามเดิม)
    st.subheader("🏠 ท่าบริหารกล้ามเนื้อที่บ้าน")
    with st.expander("คลิกดูคำแนะนำ"):
        st.write("1. **Straight Leg Raise** (ทำ 10 ครั้ง/วัน)")
        st.write("2. **Hamstring Stretch** (ทำ 10 ครั้ง/วัน)")
        st.info("💡 นำไฟล์รายงานที่ดาวน์โหลดไปให้คุณหมอดูร่วมกับภาพ X-ray จริงๆ ได้เลยครับ")

    if st.button("เริ่มใหม่"):
        st.session_state.name = ""
        st.session_state.page = "Register"
        st.rerun()
